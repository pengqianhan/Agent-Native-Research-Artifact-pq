# Figure 4: Comparison of prompt length (tokens) between raw memory retrieval and skill abstraction

- **Source**: Figure 4, Section 4.3 (page 8)
- **Caption**: "Comparison of prompt length (tokens) between raw memory retrieval and distilled skill abstraction. SKILLRL consistently reduces context overhead while maintaining reasoning utility."
- **Axes**: X = Step (0–110), Y = Prompt Length (Tokens) in 1,200–1,500 range
- **Extraction type**: raw_figure (line chart; numeric averages from §4.3 prose)

Section 4.3 "Context Efficiency" states the comparison numerically:

| Configuration | Average prompt length (tokens) |
|---------------|--------------------------------|
| Qwen2.5-7B (Raw Memory) | ≈1,450 |
| Qwen2.5-7B (Skills) | <1,300 |

Visible structure of the curves (qualitative):

| Step (≈) | Raw Memory line (≈ tokens) | Skills line (≈ tokens) |
|----------|----------------------------|------------------------|
| 0   | 1,500 | 1,250 |
| 20  | 1,470 | 1,275 |
| 40  | 1,440 | 1,290 |
| 60  | 1,470 | 1,300 |
| 80  | 1,450 | 1,290 |
| 100 | 1,450 | 1,290 |

The Skills line is consistently below the Raw Memory line. The paper reports
"approximately 10.3% reduction in context length" relative to the raw memory baseline.
