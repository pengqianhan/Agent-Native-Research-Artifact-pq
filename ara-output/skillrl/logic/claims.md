# Claims

## C01: SkillRL outperforms all published baselines on ALFWorld and WebShop with a Qwen2.5-7B agent
- **Statement**: With Qwen2.5-7B-Instruct as the base model, SkillRL achieves the best "All" success rate on ALFWorld (89.9%) and the best Score and Success on WebShop (85.2 / 72.7) compared to closed-source LLMs (GPT-4o, Gemini-2.5-Pro), prompt-/memory-based methods (ReAct, Reflexion, Mem0, ExpeL, MemP, SimpleMem), RL-based methods (RLOO, GRPO), and memory-augmented RL methods (MemRL, EvolveR, Mem0+GRPO, SimpleMem+GRPO).
- **Status**: supported
- **Falsification criteria**: A reproduction with the released hyperparameters and skill bank should rank SkillRL strictly above every listed baseline on the ALFWorld "All" column and on both WebShop columns. If any baseline matches or exceeds SkillRL on those validation metrics, the claim is refuted.
- **Proof**: [E01]
- **Evidence basis**: Table 1 — ALFWorld "All" 89.9 (SkillRL) vs second-best GRPO 77.6 (+12.3); WebShop Score 85.2 vs second-best RLOO 80.3; WebShop Succ. 72.7 vs second-best RLOO 65.7.
- **Interpretation**: The combination of distilled skills + hierarchical retrieval + recursive evolution + GRPO is jointly responsible for the SOTA gap; the paper attributes the +12.3 ALFWorld absolute gain over plain GRPO directly to skill augmentation (§4.2).
- **Dependencies**: none
- **Tags**: main-result, ALFWorld, WebShop, GRPO, benchmark

## C02: SkillRL achieves SOTA on seven search-augmented QA benchmarks
- **Statement**: SkillRL trained on NQ + HotpotQA achieves an average score of 47.1% across seven QA datasets (NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue, Bamboogle), beating Search-R1 (38.5%) and EvolveR (43.1%); the largest delta is +19.4 absolute on Bamboogle (73.8 vs EvolveR 54.4).
- **Status**: supported
- **Falsification criteria**: A reproduction with NQ+HotpotQA training should produce a 7-dataset average that ranks above Search-R1 and EvolveR on the same evaluation protocol; if EvolveR or any newer baseline matches/exceeds SkillRL average, the claim is refuted.
- **Proof**: [E02]
- **Evidence basis**: Table 2 — SkillRL Avg 47.1; NQ 45.9, TriviaQA 63.3, PopQA 45.9, HotpotQA 43.2, 2Wiki 40.3, MuSiQue 20.2, Bamboogle 73.8.
- **Interpretation**: Skill abstraction transfers to multi-hop and out-of-domain QA — TriviaQA, PopQA, 2Wiki, MuSiQue and Bamboogle were OOD, suggesting distilled search strategies are task-agnostic.
- **Dependencies**: C01
- **Tags**: main-result, search-QA, multi-hop, OOD

## C03: Removing the skill library entirely (raw-trajectory replacement) is the most damaging single ablation
- **Statement**: Replacing the skill library with raw trajectory snippets reduces ALFWorld success from 89.9% to 61.7% and WebShop success from 72.7 to 50.2 — the largest single-component drop among all ablations reported in Table 3.
- **Status**: supported
- **Falsification criteria**: An ablation rerun should show "w/o Skill Library (Raw Trajectories)" producing a larger absolute gap than every other ablation row (w/o Hierarchical Structure, w/o Cold-Start SFT, w/o Dynamic Evolution); if a different ablation row produces a larger drop, the claim is refuted.
- **Proof**: [E03]
- **Evidence basis**: Table 3 — w/o Skill Library: 61.7 / 50.2 vs full SkillRL 89.9 / 72.7 (ALFWorld -28.2, WebShop -22.5); next-largest drop is w/o Cold-Start SFT (-24.7 / -26.2).
- **Interpretation**: Abstraction (not retrieval) is the load-bearing operation; raw experience contains too much noise to substitute for distilled skills.
- **Dependencies**: C01
- **Tags**: ablation, abstraction, ALFWorld, WebShop

## C04: Each of the four SkillRL components contributes positively on the validation tasks
- **Statement**: Removing any one of (a) hierarchical structure, (b) the skill library, (c) cold-start SFT, or (d) dynamic evolution, individually reduces both ALFWorld and WebShop validation success vs the full SkillRL configuration.
- **Status**: supported
- **Falsification criteria**: For an ablation matching Table 3's protocol, each ablation row should be strictly worse than the SkillRL row on both ALFWorld "All" and WebShop "Succ."; if any single ablation matches or exceeds SkillRL on either, the claim is refuted.
- **Proof**: [E03]
- **Evidence basis**: Table 3 — every ablation row is below 89.9 / 72.7: w/o Hierarchical 76.8 / 61.4; w/o Skill Library 61.7 / 50.2; w/o Cold-Start SFT 65.2 / 46.5; w/o Dynamic Evolution 84.4 / 70.3.
- **Interpretation**: All four design decisions are individually necessary for the reported peak performance; the paper specifically calls out the +5.5 contribution of dynamic evolution and the ~25% drop from raw trajectories.
- **Dependencies**: C01, C03
- **Tags**: ablation, component-analysis

## C05: Skill distillation reduces average prompt length compared to raw memory at higher accuracy
- **Statement**: At inference SkillRL maintains an average prompt length below ~1,300 tokens while the matched raw-memory baseline (Qwen2.5-7B with Raw Memory) averages around ~1,450 tokens — about 10.3% reduction in context length — while simultaneously achieving higher task success.
- **Status**: supported
- **Falsification criteria**: A side-by-side measurement of average prompt token count should show SkillRL strictly less than the raw-memory baseline across the same inference window; if SkillRL prompts are equal or longer, the claim is refuted.
- **Proof**: [E04]
- **Evidence basis**: Figure 4 caption + axes (Prompt Length tokens 1,200–1,500 over 100 steps); §4.3 "Context Efficiency" — "averaging ~1,450 tokens" (raw) vs "<1,300 tokens" (SkillRL), "approximately 10.3% reduction"; §3.1 also notes "10–20× token compression" between τ and the distilled skill artifact at the per-trajectory level.
- **Interpretation**: Abstraction does not just *organize* memory more tightly — it preserves the actionable signal at a much smaller token cost than raw text retrieval.
- **Dependencies**: C01
- **Tags**: efficiency, context-length

## C06: Recursive skill evolution accelerates RL convergence
- **Statement**: With recursive skill evolution enabled, the SkillRL agent reaches >80% ALFWorld validation success in ~60 training steps; with skill evolution disabled the agent needs ~90 steps to reach a lower peak.
- **Status**: supported
- **Falsification criteria**: Two RL runs with identical hyperparameters that differ only in the dynamic-evolution flag should show the evolution-on run reaching ≥80% sooner *and* with a higher asymptotic peak than the evolution-off run; if no such ordering holds, the claim is refuted.
- **Proof**: [E05]
- **Evidence basis**: Figure 5 — "w/ Skills Evolution" red curve reaches >0.8 success around step 60; "w/o Skills Evolution" blue curve reaches its lower peak around step 90; §4.3 "Evolution Dynamics" states "SkillRL achieves a success rate of over 80% within 60 training steps, whereas the baseline requires approximately 90 steps to reach a lower peak."
- **Interpretation**: Periodic addition of failure-derived skills supplies timely strategic guidance and raises the asymptotic ceiling, in addition to giving the same final performance faster. The evidence is from validation success curves; we do not extend this to claims about training-loss optimization quality.
- **Dependencies**: C01, C04
- **Tags**: convergence, evolution, validation-curve

## C07: Skill library size grows from 55 to ~100 skills over 150 training steps
- **Statement**: The skill library used during ALFWorld training contains 55 skills at step 0 (12 general + 43 task-specific) and grows to ~100 skills at step 150 (≈20 general + ≈80 task-specific), with growth driven predominantly by task-specific skills.
- **Status**: supported
- **Falsification criteria**: A reproduction should produce skill counts whose initial total is 55 and whose final total is ≈100 (within ±5), with the per-category split matching the directional claim that task-specific count grows faster than general count; otherwise the claim is refuted.
- **Proof**: [E06]
- **Evidence basis**: Figure 3 — initial bar at step 0 totals 55 skills; final bar at step 150 totals 100; §4.3 "Skill Library Growth" — "The initial skill library contains 55 skills (12 general, 43 task-specific). Through dynamic evolution, this grows to 100 skills by the end of training (Step 150). The growth is predominantly driven by task-specific skills (increasing from 43 to 80), while general skills show a steadier increase (from 12 to 20)."
- **Interpretation**: Failure-driven evolution naturally biases toward task-specific patterns, suggesting that broad strategies stabilize early while task-particular failures continue to be discovered.
- **Dependencies**: C01, C04, C06
- **Tags**: evolution, library-growth

## C08: SkillRL with Qwen2.5-7B beats GPT-4o and Gemini-2.5-Pro on ALFWorld
- **Statement**: SkillRL with Qwen2.5-7B-Instruct attains 89.9% on ALFWorld, exceeding GPT-4o (48.0%) by 41.9 absolute points and Gemini-2.5-Pro (60.3%) by 29.6 absolute points.
- **Status**: supported
- **Falsification criteria**: An evaluation that re-runs GPT-4o, Gemini-2.5-Pro, and the released SkillRL ALFWorld checkpoint under the same task split should preserve the ranking SkillRL > Gemini-2.5-Pro > GPT-4o on All success rate; otherwise the claim is refuted.
- **Proof**: [E01]
- **Evidence basis**: Table 1 — Closed-source: GPT-4o 48.0, Gemini-2.5-Pro 60.3; SkillRL 89.9.
- **Interpretation**: Effective skill learning can compensate for model scale on agentic tasks within this benchmark; we do not generalize this to all agent settings or to GPT-4o-class models that have themselves been trained for agentic tasks.
- **Dependencies**: C01
- **Tags**: closed-source-comparison, scale, ALFWorld
