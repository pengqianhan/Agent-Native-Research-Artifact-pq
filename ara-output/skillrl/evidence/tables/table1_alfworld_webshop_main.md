# Table 1: Performance on ALFWorld and WebShop

- **Source**: Table 1, Section 4.2 (page 6)
- **Caption**: "Performance on ALFWorld and WebShop. For ALFWorld, we report the average success rate (%) for each subtask as well as the overall result. For WebShop, we report both the average score and the average success rate (%). * denotes the results replicated from (Feng et al., 2025). The best results and second best results are highlighted in red and blue, respectively."
- **Extraction type**: raw_table

| Method | ALFWorld Pick | ALFWorld Look | ALFWorld Clean | ALFWorld Heat | ALFWorld Cool | ALFWorld Pick2 | ALFWorld All | WebShop Score | WebShop Succ. |
|--------|---------------|---------------|----------------|---------------|---------------|----------------|---------------|----------------|----------------|
| **Closed-source LLMs** |  |  |  |  |  |  |  |  |  |
| GPT-4o | 75.3 | 60.8 | 31.2 | 56.7 | 21.6 | 49.8 | 48.0 | 31.8 | 23.7 |
| Gemini-2.5-Pro | 92.8 | 63.3 | 62.1 | 69.0 | 26.6 | 58.7 | 60.3 | 42.5 | 35.9 |
| **Qwen2.5-7B-Instruct** |  |  |  |  |  |  |  |  |  |
| Qwen2.5 | 33.4 | 21.6 | 19.3 | 6.90 | 2.80 | 3.20 | 14.8 | 26.4 | 7.80 |
| **Prompt-based Agentic or Memory-based Methods** |  |  |  |  |  |  |  |  |  |
| ReAct* | 48.5 | 35.4 | 34.3 | 13.2 | 18.2 | 17.6 | 31.2 | 46.2 | 19.5 |
| Reflexion* | 62.0 | 41.6 | 44.9 | 30.9 | 36.3 | 23.8 | 42.7 | 58.1 | 28.8 |
| Mem0 | 54.0 | 55.0 | 26.9 | 36.4 | 20.8 | 7.69 | 33.6 | 23.9 | 2.00 |
| ExpeL | 21.0 | 67.0 | 55.0 | 52.0 | 71.0 | 6.00 | 46.3 | 30.9 | 11.2 |
| MemP | 54.3 | 38.5 | 48.1 | 56.2 | 32.0 | 16.7 | 41.4 | 25.3 | 6.40 |
| SimpleMem | 64.5 | 33.3 | 20.0 | 12.5 | 33.3 | 3.84 | 29.7 | 33.2 | 8.59 |
| **RL-based Methods** |  |  |  |  |  |  |  |  |  |
| RLOO* | 87.6 | 78.2 | 87.3 | 81.3 | 71.9 | 48.9 | 75.5 | 80.3 | 65.7 |
| GRPO* | 90.8 | 66.1 | 89.3 | 74.7 | 72.5 | 64.7 | 77.6 | 79.3 | 66.1 |
| **Memory-Augmented RL-based Methods** |  |  |  |  |  |  |  |  |  |
| MemRL | 62.8 | 38.5 | 22.2 | 12.5 | 8.00 | 0.00 | 21.4 | 29.5 | 9.20 |
| EvolveR | 64.9 | 33.3 | 46.3 | 13.3 | 33.3 | 43.8 | 43.8 | 42.5 | 17.6 |
| Mem0+GRPO | 78.1 | 54.8 | 56.1 | 31.0 | 65.0 | 26.9 | 54.7 | 58.1 | 37.5 |
| SimpleMem+GRPO | 89.5 | 36.3 | 60.0 | 50.0 | 64.9 | 26.3 | 62.5 | 67.8 | 46.9 |
| **SkillRL** | 97.9 | 71.4 | 90.0 | 90.0 | 95.5 | 87.5 | 89.9 | 85.2 | 72.7 |
