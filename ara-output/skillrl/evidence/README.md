# Evidence Index

Numerical evidence files for the SkillRL ARA. All values are transcribed verbatim from
the source PDF; see each file's `Source` field for the exact section/figure.

## Tables

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1_alfworld_webshop_main.md](tables/table1_alfworld_webshop_main.md) | Table 1 (page 6) | C01, C03, C04, C08 | Main results: ALFWorld per-subtask + All, WebShop Score + Succ. across 17 baselines + SkillRL |
| [tables/table2_search_qa.md](tables/table2_search_qa.md) | Table 2 (page 7) | C02 | Search-augmented QA — 7 datasets × 11 methods |
| [tables/table3_ablations.md](tables/table3_ablations.md) | Table 3 (page 7) | C03, C04 | Component ablation results |
| [tables/table4_hyperparameters.md](tables/table4_hyperparameters.md) | Table 4 (page 14, Appendix B.1) | (used by `src/configs/training.md`) | All training and evolution hyperparameters |
| [tables/table5_alfworld_skill_examples.md](tables/table5_alfworld_skill_examples.md) | Table 5 (page 15, Appendix C) | (catalog) | Sample distilled ALFWorld general skills |
| [tables/table6_alfworld_failures.md](tables/table6_alfworld_failures.md) | Table 6 (page 15, Appendix C) | (catalog) | Common ALFWorld agent failures and mitigations |
| [tables/table7_webshop_skill_examples.md](tables/table7_webshop_skill_examples.md) | Table 7 (page 16, Appendix C) | (catalog) | Sample distilled WebShop general skills |
| [tables/table8_webshop_failures.md](tables/table8_webshop_failures.md) | Table 8 (page 16, Appendix C) | (catalog) | Common WebShop failures and mitigations |
| [tables/derived_alfworld_complex_subtasks.md](tables/derived_alfworld_complex_subtasks.md) | Derived from Table 1 | C01 | Cool / Pick2 sub-task gain SkillRL vs GRPO |

## Figures

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1b_training_curves.md](figures/figure1b_training_curves.md) | Figure 1(b) (page 1) | C01, C06 | ALFWorld validation success rate vs training steps for SkillRL / GRPO+Memory / Vanilla GRPO |
| [figures/figure3_skill_library_growth.md](figures/figure3_skill_library_growth.md) | Figure 3 (page 7) | C07 | Skill library size vs training step (stacked by category) |
| [figures/figure4_prompt_length.md](figures/figure4_prompt_length.md) | Figure 4 (page 8) | C05 | Prompt length (tokens) vs step — Raw Memory vs Skills |
| [figures/figure5_evolution_curves.md](figures/figure5_evolution_curves.md) | Figure 5 (page 8) | C06 | ALFWorld success vs training step with / without skill evolution |
