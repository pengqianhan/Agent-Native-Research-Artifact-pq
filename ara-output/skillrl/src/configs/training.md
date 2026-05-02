# Training Hyperparameters

All values come from Appendix B.1 Table 4 of the paper, plus the released training
scripts at `examples/grpo_trainer/run_alfworld_skills.sh` and `run_webshop_skills.sh`.
Where the paper and code disagree, the discrepancy is flagged.

## Cold-start SFT

### learning_rate (SFT)
- **Value**: `1e-4`
- **Rationale**: Standard SFT learning rate for instruction-tuned 7B-class models; balances rapid skill-utilization adaptation with stability.
- **Search range**: Not specified in paper.
- **Sensitivity**: Not specified.
- **Source**: Table 4, "Cold-Start SFT" block.

### batch_size (SFT)
- **Value**: `16`
- **Rationale**: Small enough to fit on the H100 cluster while supporting per-example skill-augmented prompts that can reach 4–6k tokens.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4.

### epochs (SFT)
- **Value**: `3`
- **Rationale**: Enough to instil the skill-utilization protocol without overfitting the small `D_SFT` corpus.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4.

### sft_examples
- **Value**: ALFWorld `7,500`; WebShop `2,400`
- **Rationale**: SFT data sized to the complexity of each environment; ALFWorld's larger taxonomy needs more demonstrations.
- **Search range**: Not specified.
- **Sensitivity**: Not specified, but the paper warns that bypassing this stage costs ~25 absolute success points (Table 3 "w/o Cold-Start SFT").
- **Source**: Table 4, "SFT examples" row.

## RL Training

### rl_learning_rate
- **Value**: `1e-6`
- **Rationale**: Conservative LR to keep RL updates close to the cold-start checkpoint; the KL anchor (β = 0.01) provides additional regularization.
- **Search range**: Not specified.
- **Sensitivity**: Standard for Qwen2.5-7B-class RLHF; values >1e-5 typically destabilize.
- **Source**: Table 4 RL Training block; also in §4.1 main text "learning rate 1×10⁻⁶".

### rl_batch_size
- **Value**: Table 4 says `64`; main text §4.1 says "batch size 16, group size 8, 4 gradient accumulation steps" (16 × 4 = 64 effective).
- **Rationale**: Effective batch 64 emerges from per-step batch 16 × group 8 × 4 grad accum. The released ALFWorld script sets `data.train_batch_size=16`, `actor_rollout_ref.actor.ppo_mini_batch_size=128`, `actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=4`, `env.rollout.n=8`.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4 + §4.1 main text + `examples/grpo_trainer/run_alfworld_skills.sh`.

### kl_loss_coef (β)
- **Value**: `0.01`
- **Rationale**: KL anchor to `π_ref = π_θ_sft` keeps the policy from forgetting skill-utilization while allowing task improvement.
- **Search range**: Not specified.
- **Sensitivity**: high (qualitative, per heuristics.md H03).
- **Source**: Table 4 "KL loss Coef"; also `actor_rollout_ref.actor.kl_loss_coef=0.01` in released scripts.

### invalid_action_penalty_coef
- **Value**: `0.1`
- **Rationale**: Discourage the agent from emitting syntactically invalid actions; complements the binary reward from the environment.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4 "Invalid Action Penalty Coef"; also `actor_rollout_ref.actor.invalid_action_penalty_coef=0.1` in released scripts.

### max_prompt_length
- **Value**: `6,000`
- **Rationale**: Bounded context for the skill-augmented prompt + observation + action history (Eq. 5 conditioning).
- **Search range**: Not specified.
- **Sensitivity**: medium — the paper measures average prompt length 1,200–1,500 tokens (Figure 4), so the bound is rarely binding.
- **Source**: Table 4. Released ALFWorld script sets `data.max_prompt_length=4096`; WebShop script sets `data.max_prompt_length=6000`.

### max_response_length
- **Value**: `1,024`
- **Rationale**: Bounded length for the LLM's `<think>...</think><action>...</action>` emission per step.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4. Released ALFWorld script sets `512`; WebShop sets `768`.

### epoch (RL)
- **Value**: `150`
- **Rationale**: Sufficient for the policy to plateau on validation success; library evolution operates throughout.
- **Search range**: Not specified.
- **Sensitivity**: medium — Figure 5 shows the with-evolution run plateaus around step 60–100.
- **Source**: Table 4 "Epoch: 150"; also `trainer.total_epochs=150` in released scripts.

### group_size (G)
- **Value**: `8`
- **Rationale**: Number of trajectories sampled per task for GRPO group-normalized advantage; larger groups give lower-variance advantage estimates but cost more rollouts.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: §4.1 "group size 8"; released scripts `env.rollout.n=8`.

## Skill Retrieval

### top_k (general skills, retrieval budget)
- **Value**: `6`
- **Rationale**: Number of general skills injected per episode; small enough to keep prompt under the budget, large enough to cover the multi-faceted strategic guidance the agent needs.
- **Search range**: Not specified.
- **Sensitivity**: Not specified, but the released code's H07 fix preserves dynamic skills inside this budget.
- **Source**: Table 4 "Top-K retrieval: 6"; §4.1 "K = 6"; released scripts.

### validation_interval
- **Value**: `5 Steps`
- **Rationale**: Frequency at which the trainer evaluates on the validation split and considers triggering skill evolution.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4 "Validation interval: 5 Steps"; released scripts `trainer.test_freq=5`.

### update_threshold (δ)
- **Value**: `0.4`
- **Rationale**: Per-category validation success rate below which evolution fires; chosen as a mid-range threshold so evolution targets struggling categories rather than already-saturated ones.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4 "Update Threshold δ: 0.4"; §4.1 "δ = 0.4 for the collection of failed trajectories"; released scripts `+env.skills_only_memory.update_threshold=0.4`.

### max_failures_analyzed
- **Value**: `10` (when SR < 0.4) / `5` (when SR > 0.4)
- **Rationale**: Adaptive sample budget — more failures analyzed when the agent is struggling, fewer when it is mostly succeeding.
- **Search range**: Not specified.
- **Sensitivity**: Not specified.
- **Source**: Table 4 "Max failures analyzed: 10 (SR < 0.4) / 5 (SR > 0.4)".

### max_new_skills_per_evolution
- **Value**: `3`
- **Rationale**: Hard cap on per-fire library growth; matches H05 in heuristics.md.
- **Search range**: Not specified.
- **Sensitivity**: medium per H05.
- **Source**: Table 4 "Max new skills per evolution: 3"; released scripts `+env.skills_only_memory.max_new_skills=3`; `SkillUpdater.max_new_skills_per_update`.

## Environment

### max_steps (per episode)
- **Value**: ALFWorld `50`; WebShop `15`
- **Rationale**: Episode length cap matched to typical task length per environment.
- **Source**: `env.max_steps=50` (ALFWorld script), `env.max_steps=15` (WebShop script).

### env.seed
- **Value**: `0`
- **Rationale**: Single-seed reproducibility; the paper does not report multi-seed variance.
- **Source**: Released scripts.

## Discrepancy notes

- **batch_size**: Table 4 says 64; §4.1 main text decomposes this as 16 × 4 grad-accum.
  Both values are consistent under the standard "effective batch = micro batch × grad
  accumulation × group" interpretation.
- **max_prompt_length / max_response_length**: Table 4 lists 6,000 / 1,024;
  released ALFWorld script uses 4,096 / 512 (smaller, tighter fit for shorter ALFWorld
  observations); released WebShop script uses 6,000 / 768. The Table 4 row is the
  WebShop-style upper bound.
