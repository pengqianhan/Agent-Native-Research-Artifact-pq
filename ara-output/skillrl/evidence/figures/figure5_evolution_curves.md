# Figure 5: Effect of skill evolution on convergence

- **Source**: Figure 5, Section 4.3 (page 8)
- **Caption**: "Success rate on ALFWorld validation set. The recursive skill evolution significantly accelerates convergence and enhances the overall performance ceiling."
- **Axes**: X = Training Steps (0–~120), Y = Success Rate (0.0–1.0)
- **Extraction type**: raw_figure (line chart; key crossings from §4.3 prose)

| Configuration | Step at which Success ≥0.8 | Asymptotic plateau (≈) |
|---------------|----------------------------|------------------------|
| w/ Skills Evolution (red dashed)  | ~60 | ~0.85–0.90 |
| w/o Skills Evolution (blue solid) | ~90 (lower peak) | ~0.75 |

§4.3 "Evolution Dynamics" states verbatim: "SKILLRL achieves a success rate of over 80%
within 60 training steps, whereas the baseline requires approximately 90 steps to reach
a lower peak."
