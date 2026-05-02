# Figure 3: Skill Library Evolution

- **Source**: Figure 3, Section 4.3 (page 7)
- **Caption**: "Evolution of skill library size during RL training. Dynamic skill evolution adds skills at validation checkpoints."
- **Axes**: X = Training Steps (0–150), Y = Number of Skills (0–120)
- **Extraction type**: raw_figure (stacked bar; counts read from the bar tops on page 7)

The figure is a stacked bar chart with categories: Total Skills (envelope), General, Cool, Cod, Pick, Pick2, Look, Heat, Clean, Mistakes (legend per the figure caption — note "Cod" appears in the published label and is presumed to denote one of the ALFWorld task subsets but is not separately defined in the body). Total bar tops:

| Training Step | Total Skills (≈) |
|---------------|------------------|
| 0   | 55  |
| 20  | 60  |
| 40  | 71  |
| 60  | 77  |
| 80  | 83  |
| 100 | 88  |
| 120 | 94  |
| 140 | 100 |

Per-category totals reported in §4.3 prose (page 7):
- Initial: 12 general + 43 task-specific = 55 skills.
- Final (step 150): ≈20 general + ≈80 task-specific = 100 skills.
- Growth is balanced across task categories per the prose; quantitative per-category breakdowns at each step are not separately tabulated in the paper.
