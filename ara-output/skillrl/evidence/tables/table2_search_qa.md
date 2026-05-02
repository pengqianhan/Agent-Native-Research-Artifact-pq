# Table 2: Performance on search-augmented QA tasks

- **Source**: Table 2, Section 4.2 (page 7)
- **Caption**: "Performance on search-augmented QA tasks. SkillRL is trained on NQ and HotpotQA. † and * indicate in-domain and out-of-domain datasets, respectively. * denotes the results replicated from (Sun et al., 2025)."
- **Extraction type**: raw_table

Single-Hop QA: NQ (in-domain), TriviaQA (OOD), PopQA (OOD).
Multi-Hop QA: HotpotQA (in-domain), 2Wiki (OOD), MuSiQue (OOD), Bamboogle (OOD).

| Method | NQ† | TriviaQA* | PopQA* | HotpotQA† | 2Wiki* | MuSiQue* | Bamboogle* | Avg |
|--------|-----|-----------|--------|-----------|--------|----------|------------|------|
| Qwen2.5* | 11.6 | 35.6 | 1.20 | 16.4 | 22.2 | 4.80 | 14.4 | 15.2 |
| CoT* | 12.8 | 35.6 | 3.80 | 16.2 | 22.6 | 6.60 | 24.0 | 17.4 |
| RAG* | 27.4 | 58.2 | 17.8 | 25.8 | 23.2 | 9.40 | 16.8 | 25.5 |
| Search-o1* | 19.4 | 40.6 | 11.4 | 17.0 | 27.0 | 8.60 | 30.4 | 22.1 |
| R1-Instruct | 21.0 | 44.9 | 17.1 | 20.8 | 27.5 | 6.00 | 19.2 | 22.4 |
| Search-R1 | 39.3 | 61.0 | 39.7 | 37.0 | 41.4 | 14.6 | 36.8 | 38.5 |
| ZeroSearch | 43.6 | 61.8 | 51.5 | 34.6 | 35.2 | 18.4 | 27.8 | 39.1 |
| StepSearch | - | - | - | 38.6 | 36.4 | 22.6 | 40.0 | - |
| EvolveR | 43.5 | 63.4 | 44.6 | 38.2 | 42.0 | 15.6 | 54.4 | 43.1 |
| **SkillRL** | 45.9 | 63.3 | 45.9 | 43.2 | 40.3 | 20.2 | 73.8 | 47.1 |
