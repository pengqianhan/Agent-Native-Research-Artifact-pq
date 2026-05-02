---
title: "SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning"
authors:
  - Peng Xia
  - Jianwen Chen
  - Hanyang Wang
  - Jiaqi Liu
  - Kaide Zeng
  - Yu Wang
  - Siwei Han
  - Yiyang Zhou
  - Xujiang Zhao
  - Haifeng Chen
  - Zeyu Zheng
  - Cihang Xie
  - Huaxiu Yao
year: 2026
venue: "arXiv preprint (Preprint, 10 February 2026)"
doi: "arXiv:2602.08234"
ara_version: "1.0"
domain: "LLM agents / reinforcement learning / agent memory"
keywords:
  - LLM agents
  - skill distillation
  - reinforcement learning
  - GRPO
  - hierarchical skill library
  - memory-augmented agents
  - ALFWorld
  - WebShop
  - search-augmented QA
  - self-evolving agents
claims_summary:
  - "SkillRL — a framework that distills successful + failed trajectories into a hierarchical, recursively-evolving skill library coupled to GRPO — achieves state-of-the-art success rates on ALFWorld, WebShop, and seven search-augmented QA benchmarks for a Qwen2.5-7B agent."
  - "Hierarchical separation into general skills + task-specific skills, recursive evolution at validation epochs, and cold-start SFT on skill-augmented traces are each ablation-required components."
  - "Abstracting raw trajectories into compact skills both improves task performance and reduces prompt length compared to raw memory-augmented baselines."
abstract: "Large Language Model (LLM) agents have shown stunning results in complex tasks, yet they often operate in isolation, failing to learn from past experiences. Existing memory-based methods primarily store raw trajectories, which are often redundant and noise-heavy. This prevents agents from extracting high-level, reusable behavioral patterns that are essential for generalization. In this paper, we propose SKILLRL, a framework that bridges the gap between raw experience and policy improvement through automatic skill discovery and recursive evolution. Our approach introduces an experience-based distillation mechanism to build a hierarchical skill library SKILLBANK, an adaptive retrieval strategy for general and task-specific heuristics, and a recursive evolution mechanism that allows the skill library to co-evolve with the agent's policy during reinforcement learning. These innovations significantly reduce the token footprint while enhancing reasoning utility. Experimental results on ALFWorld, WebShop and seven search-augmented tasks demonstrate that SKILLRL achieves state-of-the-art performance, outperforming strong baselines over 15.3% and maintaining robustness as task complexity increases. Code is available at https://github.com/aiming-lab/SkillRL."
---

# SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning

## Overview

SkillRL is an LLM-agent training framework that bridges the gap between raw interaction
experience and policy improvement through three coupled components: (1) an
experience-based skill distillation step that uses a teacher model `M_T` (Azure OpenAI
o3) to convert successful trajectories into reusable strategic patterns and failed
trajectories into concise lessons-from-failure; (2) a hierarchical skill library
SKILLBANK partitioned into general skills and task-specific skills, retrieved via
keyword-template or Qwen3-Embedding-0.6B semantic similarity at inference time; (3) a
recursive skill-evolution loop that, after every validation epoch with
`Acc(C) < δ` (δ = 0.4), prompts `M_T` with failed validation trajectories and the
current SKILLBANK to mint up to 3 new skills per round. Policy optimization uses GRPO
over the skill-augmented context, anchored by KL to a reference policy `π_ref` that is
the cold-start SFT model. With Qwen2.5-7B-Instruct as the base agent, SkillRL reaches
SOTA on ALFWorld (89.9% success), WebShop (85.2 score / 72.7 success rate), and seven
search-augmented QA tasks (47.1% average), beating GRPO, RLOO and memory-augmented RL
baselines while keeping average prompt length below 1,300 tokens.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight on raw-trajectory memory limitations |
| [claims.md](logic/claims.md) | 8 falsifiable claims (C01–C08) covering main results, ablations, efficiency |
| [concepts.md](logic/concepts.md) | 9 formal concept definitions (SkillBank, general/task-specific skill, etc.) |
| [experiments.md](logic/experiments.md) | 6 experiment plans (E01–E06): main results, ablations, evolution dynamics |
| [solution/architecture.md](logic/solution/architecture.md) | Pipeline component graph |
| [solution/algorithm.md](logic/solution/algorithm.md) | Mathematical formulation + Algorithm 1 pseudocode |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions and limitations |
| [solution/heuristics.md](logic/solution/heuristics.md) | 7 implementation heuristics (H01–H07) |
| [related_work.md](logic/related_work.md) | Typed dependency graph (RW01–RW17) plus background citations |
| [appendix_skill_catalog.md](logic/appendix_skill_catalog.md) | Verbatim skill / mistake taxonomy from Appendix C and D |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [configs/training.md](src/configs/training.md) | Cold-start SFT and RL hyperparameters | C01, C02, C04 |
| [configs/model.md](src/configs/model.md) | Base / teacher / embedding model choices | C01, C02 |
| [execution/skill_distillation.py](src/execution/skill_distillation.py) | Teacher-driven distillation of τ⁺/τ⁻ into skills | C01, C03 |
| [execution/skill_retrieval.py](src/execution/skill_retrieval.py) | Template + embedding skill retrieval (top-K) | C01, C04, C05 |
| [execution/recursive_evolution.py](src/execution/recursive_evolution.py) | Validation-failure-driven SKILLBANK update | C01, C04 |
| [execution/grpo_skill_loss.py](src/execution/grpo_skill_loss.py) | Skill-augmented GRPO objective | C01, C02 |
| [environment.md](src/environment.md) | Hardware, dependencies, seeds |  |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 16-node research DAG with explicit + inferred nodes |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of 6 tables + 4 figures |
