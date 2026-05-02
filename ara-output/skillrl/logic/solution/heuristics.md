# Heuristics

## H01: Asymmetric distillation of successes vs failures
- **Rationale**: Successful trajectories carry the *positive* signal (what to do), while failed trajectories' raw text would inject too much noise — they are length-heavy with backtracking and dead-ends. Compressing failure into a four-part counterfactual (failure point, flawed reasoning, what should have been done, generalizable principle) extracts the negative-knowledge content at a fraction of the token cost.
- **Sensitivity**: high — the paper's largest ablation drop (Table 3, "w/o Skill Library (Raw Trajectories)" → ALFWorld -28.2, WebShop -22.5) shows that swapping distilled skills for raw trajectories destroys most of the gain. The asymmetric shape of distillation is the core of this gain.
- **Bounds**: Requires a teacher model strong enough to identify (a) point of failure and (b) generalizable principle; weaker teachers may produce shallow lessons.
- **Code ref**: [src/execution/skill_distillation.py](../../src/execution/skill_distillation.py)
- **Source**: §3.1 "Experience-based Skill Distillation"; Eqs. 2 and 3.

## H02: Always include all general skills, retrieve only task-specific by similarity
- **Rationale**: General skills encode universal strategic principles that should apply regardless of task category (systematic search, state tracking, error recovery); task-specific skills are only useful when the right category is matched. Always-on `S_g` keeps universal guidance available; conditional `S_ret` saves tokens.
- **Sensitivity**: high — removing task-specific skills entirely (Table 3 "w/o Hierarchical Structure") drops ALFWorld 13.1 absolute and WebShop 11.3 absolute, demonstrating that the *split* matters.
- **Bounds**: General-skill set must remain small enough to fit in budget alongside `S_ret`. With `top_k=6` and a typical SkillBank of 12–20 general skills + 32–80 task-specific skills, the total in-context skill count stays below ~20 even after evolution.
- **Code ref**: [src/execution/skill_retrieval.py](../../src/execution/skill_retrieval.py)
- **Source**: §3.2 "Skill Organization" + Eq. 5; released `SkillsOnlyMemory.retrieve` always returns `S_g` regardless of mode.

## H03: Anchor RL KL penalty to the cold-start SFT model, not the base model
- **Rationale**: KL anchoring to the SFT model preserves the *learned skill-utilization behavior* during RL while still allowing task improvement. Anchoring to the unmodified base model would push the policy back to a state that does not know how to use the skills, undermining the whole pipeline.
- **Sensitivity**: high (inferred from the paper text "The KL penalty anchored to π_ref = π_θ_sft ensures that RL optimization preserves the learned skill utilization capabilities while improving task performance"). Quantitative comparison to the alternative anchor is not reported.
- **Bounds**: Requires a successful cold-start SFT phase before RL — bypassing it costs ≈25 absolute success points (Table 3, "w/o Cold-Start SFT").
- **Code ref**: [src/execution/grpo_skill_loss.py](../../src/execution/grpo_skill_loss.py)
- **Source**: §3.3 "Recursive Skill Evolution" prose immediately following Eq. 9.

## H04: Trigger evolution per-category, not globally
- **Rationale**: Catastrophic forgetting risk if the bank is rewritten globally; per-category triggering on `Acc(C) < δ` ensures growth is targeted at the categories that are still failing. Categories already at high success rate don't trigger.
- **Sensitivity**: medium — paper does not ablate the per-category vs global formulation, but the design choice is explicit in §3.3 ("To ensure targeted growth, the evolution is triggered only for categories where Acc(C) < δ").
- **Bounds**: δ = 0.4 in released configs (Table 4). At higher thresholds the bank would grow unboundedly; at lower thresholds evolution would rarely fire.
- **Code ref**: [src/execution/recursive_evolution.py](../../src/execution/recursive_evolution.py)
- **Source**: §3.3 "Recursive Skill Evolution".

## H05: Bound new skills per evolution to 3
- **Rationale**: Limits noisy or duplicate skills from a single LLM call and prevents bank-size explosion. The paper reports a 55→100 growth over 150 steps (Figure 3) — a slow, monitored expansion enabled by this cap.
- **Sensitivity**: medium — observed library growth is consistent with `≤3 × evolution_count`. Higher caps would risk noise; lower caps would reduce responsiveness.
- **Bounds**: `max_new_skills = 3` in released config (`run_alfworld_skills.sh`, `run_webshop_skills.sh`); also enforced inside `SkillUpdater.analyze_failures(reassigned[:self.max_new_skills_per_update])`.
- **Code ref**: [src/execution/recursive_evolution.py](../../src/execution/recursive_evolution.py)
- **Source**: Appendix B.1 Table 4 "Max new skills per evolution: 3"; released code.

## H06: Diversity-aware stratified sampling for failure analysis
- **Rationale**: A naive top-loss selection would over-sample one failure mode, leaving others undiscovered. Grouping by category, prioritizing severity (negative-reward magnitude), and round-robin selection preserves categorical entropy and forces the teacher to address breadth as well as depth.
- **Sensitivity**: low–medium — paper notes the design but does not ablate it.
- **Bounds**: Sample budget per fire: 10 trajectories when SR < 0.4, 5 when SR > 0.4 (Table 4). The sampler is implemented inside the validation-epoch hook (described in §3.3, not a standalone function in the released `skill_updater.py`, which receives the pre-sampled failures).
- **Code ref**: [src/execution/recursive_evolution.py](../../src/execution/recursive_evolution.py)
- **Source**: §3.3 "Recursive Skill Evolution" — "diversity-aware stratified sampling strategy: trajectories are grouped by category, prioritized by the severity of failure (negative rewards), and selected via round-robin sampling to maintain categorical entropy."

## H07: Always include dynamic skills in retrieval; fill the budget with static skills only as remainder
- **Rationale**: A naive `[:top_k]` slice on the general-skill list would silently drop newly-evolved `dyn_NNN` skills once the bank exceeds `top_k`. Always including dynamics first ensures fresh failure-derived guidance is surfaced.
- **Sensitivity**: medium — without this rule, evolution work is wasted at retrieval time, eroding C06 and C07. The paper does not ablate this rule directly; it is documented as a fix in the released code.
- **Bounds**: With `top_k = 6` and up to 8 dynamic skills produced over training (~150 steps × 1 fire/5 steps × 3 skills cap, mostly task-specific), the dynamic-only branch can in principle fill the budget; in practice the dynamic count for general skills stays small (12 → 20 over training, Figure 3).
- **Code ref**: [src/execution/skill_retrieval.py](../../src/execution/skill_retrieval.py)
- **Source**: Released code at `agent_system/memory/skills_only_memory.py:362-366` (template-mode branch of `retrieve()`).
