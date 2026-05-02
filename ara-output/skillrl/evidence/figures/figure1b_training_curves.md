# Figure 1(b): ALFWorld validation success rate vs training steps

- **Source**: Figure 1(b), Section 1 / Abstract teaser (page 1)
- **Caption**: "Performance on ALFWorld validation set (Shridhar et al.). SKILLRL achieves faster convergence and superior success rates compared to vanilla GRPO and memory-augmented RL."
- **Axes**: X = Training Steps (0–150), Y = Success Rate (%)
- **Extraction type**: raw_figure (qualitative readings; the paper provides only the line chart, not a numerical table)

| Training Step | Vanilla GRPO (≈) | GRPO+Memory (≈) | SkillRL (≈) |
|---------------|------------------|------------------|--------------|
| 0   | ≈10  | ≈10  | ≈10  |
| 20  | ≈30  | ≈40  | ≈55  |
| 40  | ≈45  | ≈55  | ≈75  |
| 60  | ≈60  | ≈65  | ≈85  |
| 80  | ≈68  | ≈70  | ≈87  |
| 100 | ≈70  | ≈73  | ≈88  |
| 120 | ≈73  | ≈75  | ≈89  |
| 140 | ≈77  | ≈75  | ≈90  |

Notes from the figure:
- A starred annotation marks SkillRL's combination of "Higher Performance" and "Faster Convergence."
- The terminal SkillRL value (≈89.9%) matches Table 1.
