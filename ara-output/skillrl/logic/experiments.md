# Experiments

## E01: Main results on ALFWorld and WebShop
- **Verifies**: C01, C08
- **Setup**:
  - Model: Qwen2.5-7B-Instruct as base agent; OpenAI o3 (Azure) as teacher `M_T` for skill distillation and SFT data generation
  - Hardware: Cluster of 8 NVIDIA H100 80GB GPUs (Appendix B.2). Wall-clock per experiment ≈30 hours, broken down as trajectory collection 3 h, skill distillation 0.5 h, cold-start SFT 2 h, RL training 24 h.
  - Dataset: ALFWorld text-game split (Shridhar et al.) — six task categories Pick, Look, Clean, Heat, Cool, Pick2; WebShop (Yao et al., 2022a) e-commerce environment
  - System: GRPO with skill augmentation; SFT data 7,500 (ALFWorld) / 2,400 (WebShop); top-K=6 retrieval; δ=0.4; max new skills per evolution=3; max prompt 6,000 tokens (WebShop) / 4,096 (ALFWorld script); max response 1,024 tokens; epoch=150
- **Procedure**:
  1. Use the base model to generate raw memory data (prompt template at `memory_data/prompt/prompt.txt` per README)
  2. Run experience-based skill distillation (Eqs. 2 + 3) with `M_T` producing the initial SkillBank JSON
  3. Cold-start SFT the base model on `M_T`-generated skill-augmented reasoning traces (Eq. 6)
  4. Run RL (Algorithm 1) with skill retrieval, GRPO updates, and recursive evolution at every validation epoch
  5. Report ALFWorld per-subtask and overall success and WebShop Score / Succ. on the validation split
- **Metrics**: ALFWorld success rate (%) per subtask + "All" (mean over subtasks); WebShop Score (avg) and Succ. (%)
- **Expected outcome**:
  - SkillRL ranks first on ALFWorld "All" and on both WebShop columns vs all listed baselines
  - SkillRL exceeds GRPO by a clear margin on ALFWorld attributable to skill augmentation
  - SkillRL with Qwen2.5-7B exceeds GPT-4o and Gemini-2.5-Pro on ALFWorld
  - In complex subtasks (Cool, Pick2) SkillRL exceeds GRPO by a larger margin than on simple subtasks
- **Baselines**: Closed-source LLMs (GPT-4o, Gemini-2.5-Pro); base Qwen2.5-7B-Instruct; prompt/memory methods (ReAct, Reflexion, Mem0, ExpeL, MemP, SimpleMem); RL methods (RLOO, GRPO); memory-augmented RL (MemRL, EvolveR, Mem0+GRPO, SimpleMem+GRPO)
- **Dependencies**: none

## E02: Search-augmented QA evaluation
- **Verifies**: C02
- **Setup**:
  - Model: Qwen2.5-7B-Instruct + SkillRL pipeline
  - Hardware: Same H100 cluster (assumed identical infrastructure; not separately broken out)
  - Dataset: Train on NQ + HotpotQA (in-domain); evaluate also on TriviaQA, PopQA, 2Wiki, MuSiQue, Bamboogle (out-of-domain)
  - System: SkillRL with the search-task skill JSON (`memory_data/search/claude_style_skills_search.json`)
- **Procedure**:
  1. Train SkillRL on NQ + HotpotQA following the same Algorithm-1 pipeline
  2. Evaluate the resulting policy on all seven QA datasets without further fine-tuning
  3. Report per-dataset accuracy and the seven-dataset average
- **Metrics**: Per-dataset accuracy (%); seven-dataset average (%)
- **Expected outcome**:
  - SkillRL average exceeds Search-R1 and EvolveR averages
  - SkillRL achieves the largest absolute gain on Bamboogle relative to EvolveR
  - SkillRL maintains competitive performance on OOD datasets (TriviaQA, 2Wiki) demonstrating that distilled search strategies are task-agnostic
- **Baselines**: Qwen2.5 (zero-shot), CoT, RAG, Search-o1, R1-Instruct, Search-R1, ZeroSearch, StepSearch, EvolveR
- **Dependencies**: E01 (shares pipeline configuration)

## E03: Component ablation on ALFWorld and WebShop
- **Verifies**: C03, C04
- **Setup**: Same as E01; vary one component at a time
  - "w/o Hierarchical Structure": remove `S_k`, keep only `S_g`
  - "w/o Skill Library": replace skill bank with raw trajectory snippets
  - "w/o Cold-Start SFT": skip the SFT stage (Eq. 6), start RL directly from base model
  - "w/o Dynamic Evolution": fix the SkillBank at its post-distillation state, disable evolution
- **Procedure**:
  1. For each ablation variant, run the full E01 pipeline with the named component disabled
  2. Hold all hyperparameters constant
  3. Report ALFWorld "All" success and WebShop "Succ." vs the full SkillRL number
- **Metrics**: ALFWorld success (%); WebShop success rate (%)
- **Expected outcome**:
  - Every ablation row is strictly worse than full SkillRL
  - "w/o Skill Library (Raw Trajectories)" produces the largest single drop
  - "w/o Cold-Start SFT" is the second-largest drop
  - "w/o Hierarchical Structure" produces a moderate drop
  - "w/o Dynamic Evolution" produces the smallest but still positive drop
- **Baselines**: Full SkillRL configuration
- **Dependencies**: E01

## E04: Context efficiency vs raw memory
- **Verifies**: C05
- **Setup**:
  - Model: Qwen2.5-7B (Raw Memory) baseline vs Qwen2.5-7B (Skills) configuration
  - Hardware: Same H100 cluster
  - Dataset: ALFWorld validation rollouts at successive training steps
  - System: Compare prompt token length step-by-step
- **Procedure**:
  1. Run inference with both configurations across the same training-step window
  2. Record prompt length (tokens) per step
  3. Plot and compare averages
- **Metrics**: Prompt length (tokens); average prompt length over the measurement window
- **Expected outcome**:
  - SkillRL average prompt length is consistently lower than the raw-memory baseline
  - Prompt-length variability for SkillRL is lower than that of raw memory
  - Performance is not lost despite shorter prompts (cross-reference E01/E03)
- **Baselines**: Qwen2.5-7B with raw-memory retrieval
- **Dependencies**: E01

## E05: Effect of skill evolution on convergence
- **Verifies**: C06
- **Setup**:
  - Model: Same SkillRL configuration as E01
  - Hardware: H100 cluster
  - Dataset: ALFWorld validation set at 10-step intervals
  - System: Two configurations differing only in the dynamic-evolution flag
- **Procedure**:
  1. Train SkillRL with `enable_dynamic_update=True` (validation interval 5 steps; threshold δ=0.4)
  2. Train SkillRL with `enable_dynamic_update=False`
  3. Plot validation success vs training step for both
- **Metrics**: Validation success rate (%) vs training step
- **Expected outcome**:
  - Evolution-enabled run reaches the high-success regime earlier in training than evolution-disabled
  - Evolution-enabled run also has a higher asymptotic peak (does not just converge faster to the same point)
- **Baselines**: SkillRL "w/o Dynamic Evolution" variant from E03
- **Dependencies**: E01, E03

## E06: Skill library growth over training
- **Verifies**: C07
- **Setup**:
  - Model: SkillRL ALFWorld run from E01 with dynamic evolution enabled
  - Hardware: H100 cluster
  - Dataset: ALFWorld training schedule (epoch=150)
  - System: Track skill counts at validation checkpoints
- **Procedure**:
  1. Snapshot the SkillBank at every 20-step interval throughout the 150-step run
  2. Count general skills, task-specific skills (per category), and totals
  3. Plot stacked bar chart of counts vs training step
- **Metrics**: Number of skills (general, per task category, total)
- **Expected outcome**:
  - Initial total = 55 (12 general + 43 task-specific)
  - Final total ≈ 100 at step 150
  - Task-specific count grows faster than general count
  - Growth is balanced across task categories rather than dominated by a single category
- **Baselines**: Static skill library (zero growth) — implicitly compared with the "w/o Dynamic Evolution" line of E03
- **Dependencies**: E01, E05
