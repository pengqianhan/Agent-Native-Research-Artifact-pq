# Model and Architecture Configuration

## Base agent (π_θ)

### model_name
- **Value**: `Qwen/Qwen2.5-7B-Instruct`
- **Rationale**: Strong open-source instruction-tuned LLM; balances reasoning capability with affordable compute on the 8 × H100 cluster (Appendix B.2). The released SFT/RL checkpoints are derived from this base.
- **Search range**: Not specified — paper does not test other base sizes.
- **Sensitivity**: Not specified.
- **Source**: §4.1 "We use Qwen2.5-7B-Instruct (Bai et al., 2023) as our base model".

### use_remove_padding
- **Value**: `True`
- **Rationale**: Standard verl optimization for variable-length sequences during forward passes.
- **Source**: `actor_rollout_ref.model.use_remove_padding=True` in released scripts.

### enable_gradient_checkpointing
- **Value**: `True`
- **Rationale**: Trades compute for memory to fit Qwen2.5-7B + skill-augmented context on each H100.
- **Source**: `actor_rollout_ref.model.enable_gradient_checkpointing=True`.

### fsdp_param_offload / fsdp_optimizer_offload
- **Value**: Both `True`
- **Rationale**: Offload to host memory to make the H100 budget feasible alongside vLLM rollout workers.
- **Source**: Released scripts.

## Teacher model (M_T)

### teacher_model
- **Value**: `OpenAI o3` (Azure OpenAI deployment)
- **Rationale**: Strong-reasoning frontier model required for trajectory→skill abstraction quality and validation-failure analysis.
- **Source**: §4.1 "OpenAI o3 (OpenAI, 2025a) as the teacher model"; released `skill_generation/alfworld.py:46-53`, `skill_updater.py:39 self.model = "o3"`.

### teacher_max_completion_tokens (initial distillation)
- **Value**: `4,096`
- **Rationale**: Long enough for 8-15 skills with full title/principle/when_to_apply fields.
- **Source**: `skill_generation/alfworld.py:46 OpenAIClient(max_new_tokens=4096, model="o3")`.

### teacher_max_completion_tokens (recursive evolution)
- **Value**: `2,048`
- **Rationale**: Bounded budget for 1–3 new skills per fire.
- **Source**: `skill_updater.py:22 max_completion_tokens: int = 2048`.

### azure_api_version
- **Value**: `2025-01-01-preview` (default)
- **Source**: `skill_updater.py:26`.

## Embedding model (used in embedding-mode skill retrieval)

### embedding_model
- **Value**: `Qwen/Qwen3-Embedding-0.6B`
- **Rationale**: Compact embedding model with strong cross-domain semantic similarity; cosine-similarity ranking over pre-computed skill embeddings is fast at inference (<1ms per task).
- **Source**: README "Embedding Mode"; `SkillsOnlyMemory.__init__` default
  `embedding_model_path = "Qwen/Qwen3-Embedding-0.6B"`.

### normalize_embeddings
- **Value**: `True`
- **Rationale**: Cosine similarity is computed as a normalized dot product after the encoder pre-normalises both query and skill embeddings.
- **Source**: `SkillsOnlyMemory._compute_skill_embeddings`.

## vLLM rollout backend

### rollout_engine
- **Value**: `vllm`
- **Rationale**: Default high-throughput inference backend used during RL rollouts; chunked prefill + flash attention enabled.
- **Source**: `actor_rollout_ref.rollout.name=$ENGINE` (default `vllm`); `VLLM_ATTENTION_BACKEND=FLASH_ATTN` exported in scripts.

### tensor_model_parallel_size
- **Value**: ALFWorld script `4`; WebShop script `4` (note `n_gpus_per_node=8` in WebShop with TP=4 → 2 inference replicas).
- **Source**: Released scripts.

### gpu_memory_utilization
- **Value**: ALFWorld `0.5`; WebShop `0.7`
- **Rationale**: Reserve GPU memory for FSDP sharded actor weights and reference model.
- **Source**: Released scripts.

### val_sampling
- **Value**: `temperature=0.4`, `do_sample=True`
- **Rationale**: Mild stochasticity for validation rollouts; matches the temperature used during training inference.
- **Source**: Released scripts `actor_rollout_ref.rollout.val_kwargs.temperature=0.4`, `do_sample=True`.

## SkillBank schema

Skill bank JSON with three top-level keys (README "Skill Bank Format"; verified directly
in `memory_data/{alfworld,webshop,search}/claude_style_skills*.json`):

```json
{
  "general_skills": [
    {"skill_id": "gen_001", "title": "...", "principle": "...", "when_to_apply": "..."}
  ],
  "task_specific_skills": {
    "<category_key>": [{"skill_id": "...", "title": "...", "principle": "...", "when_to_apply": "..."}]
  },
  "common_mistakes": [
    {"mistake_id": "err_001", "description": "...", "why_it_happens": "...", "how_to_avoid": "..."}
  ]
}
```

Released JSON sizes (post-distillation, pre-evolution):

| Environment | general | task-specific (categories)             | common_mistakes | total |
|-------------|---------|----------------------------------------|-----------------|-------|
| ALFWorld    | 12      | 32 across 6 (pick_and_place / look_at_obj_in_light / clean / heat / cool / examine) | 11 | 55 |
| WebShop     | 15      | 39 across 7 (apparel / footwear / home_decor / electronics / accessories / beauty_health / other) | 12 | 66 |
| Search      | 10      | 0 (none)                              | 11 | 21 |

After the 150-step ALFWorld run with dynamic evolution enabled, the bank totals ≈100
skills (Figure 3, page 7).
