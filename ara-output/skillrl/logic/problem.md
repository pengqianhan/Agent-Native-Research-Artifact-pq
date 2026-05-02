# Problem Specification

## Observations

### O1: Existing memory-based methods store raw trajectories that are token-heavy and noisy
- **Statement**: Memory-augmented LLM-agent frameworks (Mem0, ExpeL, MemP, SimpleMem, etc.) primarily save raw rollouts directly into external databases for retrieval as few-shot examples or context. These trajectories contain exploratory actions, backtracking and redundant steps that obscure the critical decisions which led to success or failure.
- **Evidence**: §1 ("Existing memory-based methods … primarily store raw trajectories, which are often redundant and noise-heavy"); §1 quoting Chhikara et al. 2025; Figure 1(a) gray dashed loop ("store raw trajectories and discard failures").
- **Implication**: Agents cannot distill high-level reusable behavioral patterns from raw memory at scale; context windows are blown out before useful experience can be applied.

### O2: Raw-memory baselines yield substantially weaker LLM-agent performance than skill abstraction
- **Statement**: On ALFWorld, the strongest prompt-based memory baseline Mem0+GRPO achieves 54.7% all-task success, and SimpleMem+GRPO achieves 62.5%, while raw-memory methods such as MemRL only reach 21.4%. The skill-augmented SkillRL reaches 89.9% on the same split, a 35.2 absolute-point gap to Mem0+GRPO.
- **Evidence**: Table 1 (page 6) — ALFWorld "All" column: MemRL 21.4, EvolveR 43.8, Mem0+GRPO 54.7, SimpleMem+GRPO 62.5, SkillRL 89.9.
- **Implication**: Raw-trajectory memory alone is insufficient for sparse-reward agentic tasks; the bottleneck is *what* is remembered.

### O3: Static skill libraries leave a 5.5-point ceiling on ALFWorld
- **Statement**: The "w/o Dynamic Evolution" ablation (skill library frozen during RL) reaches 84.4% on ALFWorld and 70.3 on WebShop, vs 89.9 / 72.7 with full SkillRL.
- **Evidence**: Table 3 (page 7).
- **Implication**: As the policy improves it encounters new state regions where the original skill library provides insufficient guidance; the library must co-evolve with the policy.

### O4: Cold-start SFT on skill-augmented traces is required for the agent to use the skill library
- **Statement**: Removing the cold-start SFT phase drops ALFWorld success from 89.9% to 65.2 (-24.7 absolute) and WebShop from 72.7 to 46.5 (-26.2). The paper attributes this to the base model not having learned how to retrieve and apply skills before RL begins (Guo et al., 2025).
- **Evidence**: Table 3 (page 7); §3.3 "Cold-Start Initialization".
- **Implication**: Skill-augmented RL needs an explicit demonstration phase teaching skill utilization; "simply providing skills to an unchanged model yields limited benefit" (§3.3).

### O5: Hierarchical separation matters: removing task-specific skills costs 13.1 points on ALFWorld
- **Statement**: The "w/o Hierarchical Structure" ablation (task-specific skills removed, only general skills retained) drops ALFWorld success from 89.9 to 76.8 (-13.1) and WebShop from 72.7 to 61.4 (-11.3).
- **Evidence**: Table 3 (page 7); §4.3 "Ablation Studies" point (1).
- **Implication**: General strategic principles alone are not enough — category-specific heuristics encode task-particular preconditions and failure modes that complement general skills.

### O6: Raw memory ranks worst among ablations
- **Statement**: Replacing the skill library with raw trajectory snippets ("w/o Skill Library") drops to 61.7 / 50.2 — the largest ablation degradation (≈25%+).
- **Evidence**: Table 3 (page 7); §4.3 "Ablation Studies" point (2).
- **Implication**: Abstraction (not just retrieval) is the load-bearing operation; raw experience injects noise that hinders effective transfer.

### O7: SkillRL maintains a leaner prompt than the raw-memory baseline
- **Statement**: SkillRL maintains an average prompt length below ~1,300 tokens, vs ~1,450 tokens for the raw memory baseline (Qwen2.5-7B with Raw Memory) — about 10.3% reduction.
- **Evidence**: Figure 4 (page 8); §4.3 "Context Efficiency".
- **Implication**: Skill abstraction improves both performance *and* context efficiency simultaneously, contradicting the usual quality/length tradeoff for in-context examples.

### O8: SkillRL converges faster than the no-evolution variant
- **Statement**: With recursive skill evolution the agent reaches >80% ALFWorld success within ~60 training steps, while the no-evolution baseline needs ~90 steps to reach a lower peak.
- **Evidence**: Figure 5 (page 8); §4.3 "Evolution Dynamics".
- **Implication**: Periodic injection of failure-derived skills provides timely strategic guidance that helps the policy escape local optima earlier in training.

## Gaps

### G1: No mechanism to distill *both* successes and failures into agent context
- **Statement**: Prior memory pipelines either preserve only successful trajectories (a small subset of available data) or store all rollouts as raw text — there is no method that converts both into compact, asymmetric artifacts (strategic patterns from successes, counterfactual lessons from failures).
- **Caused by**: O1, O2.
- **Existing attempts**: Reflexion (verbal reflection on failure, in-context only), ExpeL (insight extraction from successes), MemP (procedural memory), Voyager (skill library but not RL-coupled).
- **Why they fail**: They are either prompt-based and do not update the agent's parameters, or they ingest trajectories without separating success vs failure, or they keep the skill library static after construction.

### G2: No co-evolution of skill library with RL policy
- **Statement**: Even self-evolving memory frameworks (MemRL, EvolveR, MemAlpha) keep the policy frozen while updating memory, or keep memory frozen while updating the policy, but do not couple them.
- **Caused by**: O3, O8.
- **Existing attempts**: MemRL — RL only updates the memory bank; EvolveR — jointly updates policy and memory but stores rough trajectories.
- **Why they fail**: Either the policy never adapts to use the memory, or the memory contains the same noisy raw experience that hurts performance (O2, O6).

### G3: Raw-memory in-context augmentation does not scale to long-horizon agentic tasks
- **Statement**: Combining state-of-the-art prompt memory with state-of-the-art RL (Mem0+GRPO, SimpleMem+GRPO) still trails skill abstraction by ≈35 absolute points on ALFWorld, despite using more tokens.
- **Caused by**: O1, O2, O7.
- **Existing attempts**: Mem0+GRPO, SimpleMem+GRPO.
- **Why they fail**: Token budgets are spent on noisy raw text rather than high-density actionable patterns.

## Key Insight

- **Insight**: *Effective experience transfer requires abstraction.* Human experts do not memorize every action in every situation; they develop **skills** — compact, reusable strategies that capture the essence of how to accomplish specific subtasks. By making the skill library a first-class, dynamically-evolving component that co-trains with the policy via RL, the agent gets timely high-density guidance with a bounded context cost.
- **Derived from**: O1, O2, O3, O6, O7.
- **Enables**: A pipeline where (i) a teacher LLM converts τ⁺/τ⁻ into asymmetric skill artifacts, (ii) a hierarchical SkillBank supports general+task-specific retrieval, and (iii) recursive evolution at validation epochs keeps the library responsive to emerging failure modes.

## Assumptions

- A1: A high-capability teacher model (`M_T` = OpenAI o3) is available offline for both initial skill distillation and on-line skill evolution; the teacher is not part of the deployed agent.
- A2: A binary task-success indicator `r(τ) ∈ {0,1}` is available for every rollout (used to split τ into τ⁺/τ⁻).
- A3: The base agent is an instruction-tuned LLM (Qwen2.5-7B-Instruct) that can be context-conditioned on retrieved skills and fine-tuned with cross-entropy then GRPO.
- A4: Tasks have a textual goal `d` from which both keyword-based task-type detection and semantic embedding retrieval are well-defined.
- A5: Validation epochs occur at a fixed interval (every 5 training steps in the released configs) and sufficient failed validation rollouts can be sampled per category for evolution to fire.
- A6: Context length `|c| ≤ L_max` is enforced; the skill abstraction must keep the augmented prompt within this bound.
