# Related Work

The paper organizes citations into three threads in Section 5: LLM Agents, Memory
Mechanisms in Agents, and Evolution of Agentic Skills and Reinforcement Learning.
Below, works with a clear technical delta carry full RW blocks; remaining works that
appear in the References list (background, infrastructure, datasets, baselines) are
captured more briefly so the paper's full citation footprint is preserved.

## RW01: Yao et al., 2022b — ReAct
- **DOI**: ICLR 2022b (no arXiv ID in references list)
- **Type**: baseline, imports
- **Delta**:
  - What changed: ReAct interleaves chain-of-thought reasoning with environment actions; SkillRL builds on ReAct-style action format but augments the prompt with retrieved skills + lessons-from-failure rather than just CoT.
  - Why: ReAct provides the "Think → Act" template that SkillRL's prompts (Appendix A.1, A.2) inherit; SkillRL adds a structured `## Retrieved Relevant Experience` block above the reasoning.
- **Claims affected**: C01 (ReAct is a baseline in Table 1)
- **Adopted elements**: ReAct prompting style with `<think>`/`<action>` tags.

## RW02: Shinn et al., 2023 — Reflexion
- **DOI**: NeurIPS 2023 (no arXiv ID in references)
- **Type**: baseline, refutes
- **Delta**:
  - What changed: Reflexion uses verbal self-reflection on past failures stored in-context; SkillRL distills failures into structured `s⁻` records with the four-component schema and persists them in a hierarchical bank instead of episodic in-context reflection.
  - Why: SkillRL argues that abstraction (not just self-reflection) is the load-bearing operation for transfer.
- **Claims affected**: C01, C03
- **Adopted elements**: The idea of leveraging failure information.

## RW03: Wang et al. (Voyager), TMLR — Voyager
- **DOI**: Wang, G. et al. (TMLR; no arXiv ID in references)
- **Type**: extends
- **Delta**:
  - What changed: Voyager builds an open-ended skill library for an embodied agent in Minecraft via in-context learning; SkillRL extends this idea with (a) hierarchical separation general/task-specific, (b) RL-coupled co-evolution, (c) cold-start SFT for skill utilization.
  - Why: Voyager's library is static during use; SkillRL makes it a co-evolving component.
- **Claims affected**: C04, C06, C07
- **Adopted elements**: The notion of a persistent skill library with retrievable, reusable strategies.

## RW04: Chhikara et al., 2025 — Mem0
- **DOI**: arXiv:2504.19413
- **Type**: baseline, refutes
- **Delta**:
  - What changed: Mem0 builds production-ready long-term memory by storing/retrieving raw experience; SkillRL specifically argues that storing raw trajectories is noise-heavy and shows abstraction beats Mem0+GRPO by 35.2 absolute on ALFWorld.
  - Why: Direct refutation target — "raw trajectories are often token-heavy and contain significant redundancy and noise."
- **Claims affected**: C01, C03, C05
- **Adopted elements**: Memory-augmented RL framework comparison setup.

## RW05: Zhao et al., 2024 — ExpeL
- **DOI**: AAAI 2024 (no arXiv ID in references)
- **Type**: baseline, extends
- **Delta**:
  - What changed: ExpeL extracts insights from successful trajectories without parameter updates; SkillRL distills both successes *and* failures, and updates parameters via SFT + RL.
  - Why: ExpeL's prompt-only paradigm cannot adapt the policy itself.
- **Claims affected**: C01
- **Adopted elements**: The pattern of using a strong LLM to extract insights from trajectories.

## RW06: Fang et al., 2025 — MemP
- **DOI**: arXiv:2508.06433
- **Type**: baseline
- **Delta**:
  - What changed: MemP explores agent procedural memory via prompt-only retrieval; SkillRL replaces ad-hoc procedural memory with a hierarchical, RL-coevolving skill library.
  - Why: Distinct memory abstraction with parameter updates.
- **Claims affected**: C01
- **Adopted elements**: Categorical organization of procedural memory.

## RW07: Liu et al., 2026 — SimpleMem
- **DOI**: arXiv:2601.02553
- **Type**: baseline, refutes
- **Delta**:
  - What changed: SimpleMem provides an efficient lifelong memory with per-trajectory storage; SimpleMem+GRPO is the strongest non-skill memory-augmented RL baseline at 62.5% ALFWorld but still trails SkillRL by 27.4 absolute points.
  - Why: SimpleMem demonstrates the ceiling of trajectory-based memory + RL; SkillRL exceeds it by abstracting away from trajectories.
- **Claims affected**: C01, C03
- **Adopted elements**: Hybrid prompt-memory + RL comparison paradigm.

## RW08: Wu et al., 2025 — EvolveR
- **DOI**: arXiv:2510.16079
- **Type**: baseline, extends
- **Delta**:
  - What changed: EvolveR is a self-evolving LLM-agent framework with experience-driven lifecycle that jointly updates policy and memory; SkillRL improves over EvolveR by replacing rough trajectory storage with structured skill abstraction (and beats it by 19.4 absolute on Bamboogle, Table 2).
  - Why: EvolveR is the closest co-evolution baseline; SkillRL claims abstraction is the differentiator.
- **Claims affected**: C01, C02, C04
- **Adopted elements**: The general framing of "policy + memory co-evolution."

## RW09: Zhang et al., 2026 — MemRL
- **DOI**: arXiv:2601.03192
- **Type**: baseline, refutes
- **Delta**:
  - What changed: MemRL uses RL to update the memory bank while keeping the policy frozen; SkillRL updates *both* and shows that frozen-policy memory updates yield only 21.4% on ALFWorld vs SkillRL's 89.9%.
  - Why: Direct head-to-head on memory-augmented RL paradigms.
- **Claims affected**: C01
- **Adopted elements**: RL-driven memory-update procedure (used differently here for skills).

## RW10: Shao et al., 2024 — DeepSeekMath / GRPO
- **DOI**: arXiv:2402.03300
- **Type**: imports
- **Delta**:
  - What changed: GRPO is an RL method that avoids training a critic by using intra-group relative rewards; SkillRL adopts GRPO unchanged as the optimizer (Eq. 1) and only modifies the conditioning context to include skills (Eq. 9).
  - Why: GRPO's critic-free formulation is well-suited to LLM-agent RL where reward is sparse and binary.
- **Claims affected**: C01, C04, C06
- **Adopted elements**: The full GRPO objective (Eq. 1), group-normalized advantages (Eq. 8), KL-regularized PPO-clip variant.

## RW11: Schulman et al., 2017 — PPO
- **DOI**: arXiv:1707.06347
- **Type**: imports
- **Delta**:
  - What changed: SkillRL adopts the PPO clip mechanism inside its GRPO objective unchanged.
  - Why: PPO clipping bounds policy updates per step.
- **Claims affected**: C01
- **Adopted elements**: Clip(·, 1−ε, 1+ε) pattern.

## RW12: Ahmadian et al., 2024 — RLOO
- **DOI**: ACL 2024 (no arXiv ID in references list)
- **Type**: baseline
- **Delta**:
  - What changed: RLOO is a REINFORCE-style baseline included in Table 1; SkillRL exceeds RLOO on ALFWorld by 14.4 absolute and on WebShop by 7.0 absolute.
  - Why: Provides a non-GRPO RL reference for the policy-optimizer dimension.
- **Claims affected**: C01
- **Adopted elements**: None directly; used only as benchmark.

## RW13: Anthropic, 2024 — Claude / Agent Skills
- **DOI**: https://www.anthropic.com/news/claude-3-family
- **Type**: imports
- **Delta**:
  - What changed: SkillRL borrows the framing of "skills" as compact, reusable strategies — described as Anthropic's "agent skills" design pattern — and operationalizes it with structured fields (title, principle, when_to_apply).
  - Why: Provides the conceptual vocabulary for "skills" as a first-class design unit.
- **Claims affected**: none directly (conceptual)
- **Adopted elements**: Three-field skill schema (title / principle / when_to_apply) is referred to as "Claude-style" skills throughout the released code.

## RW14: Bai et al., 2023 — Qwen Technical Report
- **DOI**: arXiv:2309.16609
- **Type**: imports
- **Delta**:
  - What changed: SkillRL uses Qwen2.5-7B-Instruct as the base agent.
  - Why: Strong open-source instruction-tuned model with manageable size for academic GPU budgets.
- **Claims affected**: C01, C02, C08
- **Adopted elements**: Qwen2.5-7B-Instruct checkpoint as base model.

## RW15: OpenAI, 2025a — o3
- **DOI**: https://openai.com/index/introducing-o3-and-o4-mini/
- **Type**: imports
- **Delta**:
  - What changed: SkillRL uses OpenAI o3 (Azure) as the teacher model `M_T` for both skill distillation and SFT data generation.
  - Why: Strong-reasoning frontier model needed for trajectory→skill abstraction quality.
- **Claims affected**: C01, C04
- **Adopted elements**: o3 inference API (Azure).

## RW16: Guo et al., 2025 — DeepSeek-R1
- **DOI**: arXiv:2501.12948
- **Type**: imports
- **Delta**:
  - What changed: Cited as motivation for the cold-start SFT phase — "Simply providing skills to an unchanged model yields limited benefit" (Guo et al., 2025).
  - Why: Provides the empirical case that RL on top of a non-aligned base model is unstable.
- **Claims affected**: C04
- **Adopted elements**: The cold-start initialization pattern (SFT before RL).

## RW17: Shridhar et al. — ALFWorld
- **DOI**: ICLR (Shridhar, Yuan, Côté, Bisk, Trischler, Hausknecht; no arXiv ID in references list)
- **Type**: baseline (environment)
- **Delta**:
  - What changed: SkillRL evaluates on the ALFWorld text-game environment built on the ALFRED embodied AI benchmark.
  - Why: Provides a sparse-reward, multi-step household task benchmark.
- **Claims affected**: C01, C03, C04, C06, C07, C08
- **Adopted elements**: Environment + 6-task taxonomy (Pick / Look / Clean / Heat / Cool / Pick2).

## Background and infrastructure citations (no separate technical delta)

These citations appear in the References list and inform the paper's intellectual
context without being differentiated against:

- **Yao et al., 2022a — WebShop**: e-commerce environment used for evaluation (Tab. 1, page 5).
- **Kwiatkowski et al., 2019 — Natural Questions**, **Joshi et al., 2017 — TriviaQA**, **Mallen et al., 2023 — PopQA**, **Yang et al., 2018 — HotpotQA**, **Ho et al., 2020 — 2WikiMultiHopQA**, **Trivedi et al., 2022 — MuSiQue**, **Press et al., 2023 — Bamboogle**: search-augmented QA datasets evaluated in Table 2.
- **Li et al., 2025 — Search-o1**, **Jin et al., 2025 — Search-R1**, **Sun et al., 2025 — ZeroSearch**, **Zheng et al., 2025 — StepSearch**: search-augmented baselines in Table 2.
- **Comanici et al., 2025 — Gemini 2.5**: closed-source baseline in Table 1.
- **OpenAI, 2024 — GPT-4o system card**, **OpenAI, 2025c — Computer Using Agent**, **OpenAI, 2025b — Deep Research system card**, **Google, 2024**, **Google, 2025**: cited as illustrative LLM-agent products.
- **Ouyang et al., 2022 — InstructGPT / SFT**: cited as the basis for the cold-start SFT stage.
- **Hu et al., 2025 — "Memory in the Age of AI Agents"**: motivating survey for memory architectures.
- **Wang, Y., 2025 — From Static Parameters to Updatable Memory** (PhD thesis); **Wang & Chen, 2025 — Mirix**; **Wang et al., 2025 — Mem-α**; **Wang et al., 2024 — Agent Workflow Memory**; **Tang et al., 2025 — Agent KB**; **Zhang et al., 2025a — G-memory**; **Zhang et al., 2025b — MemEvolve**; **Ouyang et al., 2025 — ReasoningBank**; **Wei et al., 2025 — Evo-Memory**: the broad self-evolving memory literature in §5 paragraph "Memory Mechanisms in Agents".
- **Wei et al., 2026 — Agentic Reasoning** (arXiv:2601.12538); **Yao et al., 2022b — ReAct**; **Wu et al., 2024 — AutoGen**; **Li et al., 2023 — CAMEL**; **Liu et al., 2025 — Agent0-VL**; **Xia et al., 2025 — Agent0**; **Gao et al., 2025 — Self-evolving Agents Survey**; **Feng et al., 2025 — GiGPO** (the verl-agent codebase the released training scripts build on); **Team et al., 2025 — Tongyi DeepResearch**: §5 paragraph "Evolution of Agentic Skills and Reinforcement Learning".
- **Parisi et al., 2019 — Continual Lifelong Learning Review**: cited as the framing for "skills as continual learning."
- **Anthropic, 2024 — Claude 3 family release**; **Dong et al., 2024 — In-Context Learning Survey**: background framing.
