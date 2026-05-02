# Derived subset — ALFWorld complex sub-tasks (Cool, Pick2)

- **Source**: Derived from Table 1 in the SkillRL paper (page 6)
- **Caption**: "Sub-task gain SkillRL vs GRPO on the most complex ALFWorld categories that the paper highlights in §4.2 ('In complex subtasks like Cool and Pick2, SKILLRL outperforms GRPO by 23.0% and 22.8% respectively')."
- **Extraction type**: derived_subset
- **Derived from**: `table1_alfworld_webshop_main.md`

| Sub-task | GRPO* | SkillRL | Δ (absolute) |
|----------|-------|---------|---------------|
| Cool     | 72.5  | 95.5    | +23.0 |
| Pick2    | 64.7  | 87.5    | +22.8 |

The paper specifically calls out these two categories as evidence that "structured skill
priors effectively accelerate and enhance policy learning in sparse-reward environments"
(§4.2 point 2).
