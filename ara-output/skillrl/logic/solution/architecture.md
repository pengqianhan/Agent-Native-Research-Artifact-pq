# Architecture

The SkillRL pipeline is the data flow shown in Figure 2 of the paper. It consists of an
offline preparation stage (rollout → distill → SkillBank → cold-start SFT) and an online
RL stage (rollout with skill retrieval → GRPO update → optional skill evolution). The
released code packages each component as a small focused module under
`agent_system/memory/` and `skill_generation/` of the SkillRL repo, plumbed through the
verl-agent (GiGPO) trainer.

## Component graph

```
              ┌─────────────────────────────┐
              │ Base agent π_base (Qwen2.5- │
              │ 7B-Instruct)                │
              └──────────────┬──────────────┘
                             │ Rollout in env E
                             ▼
                ┌────────────┴────────────┐
                │ Trajectories T = T+ ∪ T-│
                │ split by r(τ) ∈ {0,1}   │
                └────┬──────────────┬─────┘
                     │              │
        Eq.(2): s+= M_T(τ+, d)      Eq.(3): s- = M_T(τ-, d)
                     │              │
                     ▼              ▼
                ┌────────────────────────┐
                │ Initial SkillBank      │
                │  S_g  ∪  ⋃_k S_k       │
                │  + common_mistakes[]   │
                └────────────┬───────────┘
                             │
                             ▼   D_SFT = {(d_i, S_i, τ_i*)}
                ┌────────────┴───────────┐
                │ Cold-start SFT (Eq. 6) │
                │  → π_θ_sft = π_ref     │
                └────────────┬───────────┘
                             │
                             ▼   For epoch ∈ [1..N]:
        ┌──────────────────────────────────────────┐
        │ Online RL loop (Algorithm 1, lines 19-31)│
        │                                          │
        │  1. Retrieve  S_ret = TopK(S_k by sim,K)│
        │  2. Sample G trajectories                │
        │     a_t ~ π_θ(·|o≤t,d,S_g,S_ret)         │
        │  3. Compute R_i, A_i (Eq. 8)             │
        │  4. GRPO update with KL to π_ref (Eq. 9) │
        │  5. If validation epoch:                 │
        │       T_val = failed val rollouts        │
        │       S_new = M_T(T_val, SkillBank)      │
        │       SkillBank ← SkillBank ∪ S_new      │
        └──────────────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │ Trained policy π_θ*      │
              │ Evolved SkillBank S*     │
              └──────────────────────────┘
```

## Components

### 1. Rollout and trajectory split
- **Purpose**: Collect both successful and failed trajectories from the base policy in environment `E`.
- **Inputs**: `π_base`, environment `E`, task description `d`
- **Outputs**: `T = T⁺ ∪ T⁻` partitioned by binary task success
- **Interactions**: Feeds skill distillation; only τ⁺ pass success indicator threshold for the success branch
- **Key design choice**: Both τ⁺ and τ⁻ are deliberately kept, contradicting prior "successful-only" memory baselines. Failed trajectories provide failure-mode information not derivable from successes alone (§3.1).

### 2. Experience-based skill distillation (`skill_generation/{alfworld,webshop,search}.py`)
- **Purpose**: Use teacher `M_T` (OpenAI o3 in the released code) to convert each trajectory into a structured skill record.
- **Inputs**: Trajectories `T⁺/T⁻`, task description `d`
- **Outputs**: For τ⁺ → `s⁺` (strategic patterns); for τ⁻ → `s⁻` (failure lessons with 4 components: failure point, flawed reasoning, what should have been done, generalizable principles)
- **Interactions**: Outputs are aggregated into the initial JSON SkillBank, organized by category
- **Key design choice**: Asymmetric processing — direct context inclusion of τ⁻ is rejected as infeasible due to length and noise; failures are turned into counterfactuals (§3.1).

### 3. Hierarchical SkillBank (`memory_data/{env}/claude_style_skills.json`)
- **Purpose**: Persistent two-level skill store; serializable JSON enabling reuse across runs.
- **Inputs**: Skill records from distillation; new skills from evolution
- **Outputs**: `S_g`, `S_k` for category `k`, and an optional `common_mistakes[]` list
- **Interactions**: Read by the retrieval module at every step; written by the evolution module at validation epochs
- **Key design choice**: Two levels (general / task-specific) reflect the empirical finding that universal heuristics and task-particular procedures play complementary roles (§3.2 "Skill Organization").

### 4. Skill retrieval (`agent_system/memory/skills_only_memory.py`)
- **Purpose**: Compose the in-context skill set for the current task description.
- **Inputs**: Task description `d`, current SkillBank
- **Outputs**: `(S_g, S_ret, mistakes_to_avoid[:5], task_type)` formatted into a multi-section prompt block
- **Interactions**: Called inside the rollout loop; result is concatenated with the system prompt and current observation history before LLM forwarding
- **Key design choice**: Two retrieval modes implemented:
  - **Template mode**: keyword-based task-type detection; returns all task-specific skills under the matched category and the first `top_k` general skills (no embedding model).
  - **Embedding mode**: encodes `d` and every skill with Qwen3-Embedding-0.6B, ranks by cosine similarity, returns top-K from the entire bank cross-category.
- The released `SkillsOnlyMemory.retrieve` method always includes dynamic skills (those with id starting with `dyn_`) before filling the budget with static general skills, so dynamic additions are not silently dropped when the bank exceeds `top_k`.

### 5. Cold-start SFT
- **Purpose**: Teach the base agent the *skill utilization* protocol before RL.
- **Inputs**: `D_SFT = {(d_i, S_i, τ_i*)}` of teacher-generated skill-augmented reasoning traces
- **Outputs**: `π_θ_sft` checkpoint that doubles as `π_ref` for the KL anchor
- **Interactions**: Acts as RL warm start; the trained model is also released on Hugging Face per environment (Alfworld-7B-SFT, Webshop-7B-SFT, Search-7B-SFT)
- **Key design choice**: Cross-entropy fine-tuning at lr=1e-4, batch=16, 3 epochs (Table 4); SFT data sizes 7,500 (ALFWorld) / 2,400 (WebShop) — small relative to typical instruction-tuning corpora but specifically formatted to demonstrate skill retrieval and application.

### 6. Skill-augmented GRPO update
- **Purpose**: Optimize the policy over the skill-augmented context.
- **Inputs**: Sampled rollouts `{τ⁽ⁱ⁾}_{i=1}^G`, rewards `{R_i}`, reference policy `π_ref`
- **Outputs**: Updated `θ`
- **Interactions**: Implemented via verl's `verl.trainer.main_ppo` entrypoint with `algorithm.adv_estimator=grpo` and `actor_rollout_ref.actor.use_kl_loss=True, kl_loss_coef=0.01, kl_loss_type=low_var_kl`
- **Key design choice**: Importance ratio `ρ_i` is computed over the *skill-augmented* context (Eq. 9), and the KL penalty is anchored to the cold-start SFT model `π_θ_sft`. An invalid-action penalty (`use_invalid_action_penalty=True, invalid_action_penalty_coef=0.1`) is applied to discourage syntactically invalid action emissions.

### 7. Recursive skill evolution (`agent_system/memory/skill_updater.py`)
- **Purpose**: At validation epochs, mint new skills from observed failure modes.
- **Inputs**: `T_val` (failed validation trajectories), current SkillBank
- **Outputs**: `S_new` of up to `max_new_skills_per_update = 3` skills per fire, with auto-assigned `dyn_NNN` IDs
- **Interactions**: Triggered when `Acc(C) < δ` for some category; calls Azure OpenAI o3 with a structured prompt asking for `(skill_id, title, principle, when_to_apply)` JSON; resulting skills are appended to `S_g` (general) by default in the released code path. The dynamic update invalidates the cached embedding matrix so the next retrieval recomputes embeddings.
- **Key design choice**: The prompt explicitly asks the teacher to (1) identify failure patterns not addressed by current skills, (2) propose new skills, and (3) suggest refinements (§3.3 "Recursive Skill Evolution").
