# Concepts

## SkillBank (S = S_g ∪ ⋃_{k=1}^K S_k)
- **Notation**: $\mathcal{S} = \mathcal{S}_g \cup \bigcup_{k=1}^{K} \mathcal{S}_k$
- **Definition**: A two-level hierarchical skill library partitioned into a flat set of *general skills* `S_g` (universal strategic principles applicable across all task types in an environment) and a per-category collection of *task-specific skill sets* `S_k` for task category `k`. Each skill `s ∈ S` is a structured record of three fields — a concise **title**, a **principle** describing the strategy, and **when_to_apply** specifying applicability conditions (§3.2). The bank can be expanded at runtime by appending evolved skills `S_new` produced from validation-failure analysis.
- **Boundary conditions**: Defined per environment (ALFWorld, WebShop, Search). A skill is always retrieved together with all of `S_g` (general skills are always included as foundational guidance); task-specific skills are subject to retrieval with threshold `δ` and budget `K`.
- **Related concepts**: General Skill, Task-specific Skill, Skill Retrieval, Recursive Skill Evolution.

## General Skill (s ∈ S_g)
- **Notation**: `s ∈ S_g` with fields `(title, principle, when_to_apply)`
- **Definition**: A universal strategic principle applicable across all task types within an environment — examples include systematic search patterns, prioritizing unvisited locations, state-management principles (e.g., verifying preconditions before actions), and goal-tracking heuristics (e.g., maintaining progress counters, terminating only upon verified completion) (§3.2 "Skill Organization" point 1).
- **Boundary conditions**: General skills are always included in the retrieved context regardless of task category, providing foundational guidance.
- **Related concepts**: SkillBank, Task-specific Skill.

## Task-specific Skill (s ∈ S_k)
- **Notation**: `s ∈ S_k` for task category `k`
- **Definition**: A specialised skill that encodes domain-specific action sequences, task-particular preconditions and constraints, common failure modes unique to the task type, and optimized procedures that exploit task structure (§3.2 "Skill Organization" point 2).
- **Boundary conditions**: Retrieved only for tasks whose detected/embedding-similar category equals `k`. In template-mode retrieval all task-specific skills under `k` are returned; in embedding-mode retrieval the top-K across all categories are returned.
- **Related concepts**: General Skill, Skill Retrieval, Task Type.

## Successful Skill Distillation (s⁺)
- **Notation**: $s^+ = \mathcal{M}_T(\tau^+, d)$ (Eq. 2)
- **Definition**: For a successful trajectory `τ⁺ ∈ T⁺ = {τ_i : r(τ_i) = 1}`, the teacher model `M_T` produces a structured skill record `s⁺` capturing the strategic patterns that led to task completion: critical decision points, the reasoning behind correct actions, and generalizable patterns that transfer beyond the specific task instance (§3.1).
- **Boundary conditions**: Defined only for trajectories whose binary task-success indicator equals 1. Direct inclusion of full successful trajectories in agent context is also feasible but is bypassed in favor of distilled patterns.
- **Related concepts**: Failure Lesson, SkillBank, Teacher Model.

## Failure Lesson (s⁻)
- **Notation**: $s^- = \mathcal{M}_T(\tau^-, d)$ (Eq. 3)
- **Definition**: For a failed trajectory `τ⁻ ∈ T⁻ = {τ_i : r(τ_i) = 0}`, the teacher synthesises a concise four-part counterfactual: (1) point of failure, (2) flawed reasoning or action, (3) what should have been done, and (4) general principles to prevent similar failures (§3.1).
- **Boundary conditions**: Defined only for trajectories with `r(τ) = 0`. Direct inclusion of failed trajectories in context is rejected because their length and noise make context inclusion infeasible.
- **Related concepts**: Successful Skill Distillation, SkillBank, Common Mistake.

## Skill Retrieval (S_ret = TopK)
- **Notation**: $\mathcal{S}_{\mathrm{ret}} = \mathrm{TopK}(\{s \in \mathcal{S}_k : \mathrm{sim}(e_d, e_s) > \delta\}, K)$ (Eq. 4)
- **Definition**: Given a task description `d`, the retriever computes embeddings `e_d` and `e_s`, filters task-specific skills by cosine similarity above threshold `δ`, and returns the top-K. The full general-skill set `S_g` is unconditionally included. The policy then conditions on the retrieved skills: `a_t ∼ π_θ(a_t | o_{≤t}, d, S_g, S_ret)` (Eq. 5).
- **Boundary conditions**: K = 6 and δ = 0.4 in the released configurations (Appendix B.1). In the released code the retriever supports two modes: **template** (keyword task-type detection, return all skills under the matched category, no GPU needed) and **embedding** (Qwen3-Embedding-0.6B, cross-category top-K).
- **Related concepts**: Task Type Detection, Embedding Retrieval, SkillBank.

## Recursive Skill Evolution (S ← S ∪ S_new)
- **Notation**: $\mathcal{S}_{\mathrm{new}} = \mathcal{M}_T(\mathcal{T}_{\mathrm{val}}, \mathrm{SKILLBANK})$ (Eq. 7); $\mathrm{SKILLBANK} \leftarrow \mathrm{SKILLBANK} \cup \mathcal{S}_{\mathrm{new}}$
- **Definition**: After each validation epoch, for each task category `C` whose validation success `Acc(C) < δ`, the trainer collects failed validation trajectories `T_val` using diversity-aware stratified sampling (grouped by category, prioritized by negative-reward severity, selected via round-robin to maintain categorical entropy) and prompts `M_T` to (1) identify failure patterns not addressed by current skills, (2) propose new skills, and (3) suggest refinements to ineffective ones. The library is then updated.
- **Boundary conditions**: Triggered only if validation epoch hits *and* `Acc(C) < δ` for some category. δ = 0.4. Up to `max_new_skills_per_update = 3` skills per fire. Bounded sample size for analysis: 10 failed trajectories when SR < 0.4 and 5 when SR > 0.4 (Table 4).
- **Related concepts**: SkillBank, Failure Lesson, Validation Epoch.

## Skill-Augmented GRPO Objective
- **Notation**: $\mathcal{J}(\theta) = \mathbb{E}_{d,\{\tau^{(i)}\}} \left[\frac{1}{G}\sum_{i=1}^{G}\min(\rho_i A_i, \mathrm{clip}(\rho_i,1-\epsilon,1+\epsilon)A_i) - \beta D_{KL}(\pi_\theta \| \pi_{\mathrm{ref}})\right]$ (Eq. 9), where $\rho_i = \pi_\theta(\tau^{(i)} | d, \mathcal{S}_g, \mathcal{S}_{\mathrm{ret}}) / \pi_{\mathrm{old}}(\tau^{(i)} | d, \mathcal{S}_g, \mathcal{S}_{\mathrm{ret}})$ and $A_i = (R_i - \mathrm{mean}(\{R_j\}_{j=1}^G)) / \mathrm{std}(\{R_j\}_{j=1}^G)$ (Eq. 8).
- **Definition**: A GRPO objective in which the importance ratio `ρ_i` is computed over the *skill-augmented* context — the policy is conditioned on `(d, S_g, S_ret)` — and the KL penalty is anchored to `π_ref = π_θ_sft`, the cold-start SFT model. Group size G = 8.
- **Boundary conditions**: Each rollout receives a binary reward `R_i = r(τ^(i)) ∈ {0,1}`. PPO-style clip uses `ε`. β is the KL coefficient (KL loss coef = 0.01 in released configs).
- **Related concepts**: GRPO, Cold-Start SFT, Reference Policy, Skill Retrieval.

## Cold-start SFT (θ_sft)
- **Notation**: $\theta_{\mathrm{sft}} = \arg\min_\theta \mathcal{L}_{CE}(\mathcal{D}_{SFT}; \theta)$ (Eq. 6) with $\mathcal{D}_{SFT} = \{(d_i, \mathcal{S}_i, \tau_i^*)\}_{i=1}^N$
- **Definition**: A supervised cross-entropy fine-tuning stage that uses `N` skill-augmented reasoning traces generated by `M_T` to teach the base agent how to retrieve, interpret and apply skills during decision making. The resulting `π_{θ_sft}` serves as both starting point for RL and reference policy `π_ref` for the KL anchor.
- **Boundary conditions**: Required before RL — bypassing this stage costs ≈25 absolute success points on both ALFWorld and WebShop (Table 3, "w/o Cold-Start SFT" row). SFT data: 7,500 examples for ALFWorld and 2,400 examples for WebShop (Table 4).
- **Related concepts**: Skill-Augmented GRPO, Reference Policy, Teacher Model.

## Common Mistake (err_NNN)
- **Notation**: A record `{mistake_id, description, why_it_happens, how_to_avoid}` (Appendix Tables 6, 8).
- **Definition**: An optional third channel of the SkillBank that catalogs failure modes encountered in trajectory analysis with their root causes and concrete mitigation strategies. In the released JSON skill bank, common mistakes are surfaced to the agent as a "Mistakes to Avoid" section in the prompt (top 5 per episode).
- **Boundary conditions**: Empirically observed in the released ALFWorld (11), WebShop (12) and Search (11) skill JSONs. Used during prompt formatting in `SkillsOnlyMemory.format_for_prompt` (released code).
- **Related concepts**: Failure Lesson, SkillBank.
