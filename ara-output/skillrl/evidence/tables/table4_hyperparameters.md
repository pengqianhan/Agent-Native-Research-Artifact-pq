# Table 4: Hyperparameters for SkillRL

- **Source**: Table 4, Appendix B.1 (page 14)
- **Caption**: "Hyperparameters for SKILLRL."
- **Extraction type**: raw_table

| Hyperparameter | Value |
|----------------|-------|
| **Cold-Start SFT** |  |
| Learning rate | 1 × 10⁻⁴ |
| Batch size | 16 |
| Epochs | 3 |
| SFT examples | 7,500 (AlfWorld) / 2,400 (WebShop) |
| **RL Training** |  |
| Learning rate | 1 × 10⁻⁶ |
| Batch size | 64 |
| KL loss Coef | 0.01 |
| Invalid Action Penalty Coef | 0.1 |
| Max Prompt Length | 6,000 |
| Max Response Length | 1,024 |
| Epoch | 150 |
| **Skill Retrieval** |  |
| Top-K retrieval | 6 |
| Validation interval | 5 Steps |
| Update Threshold δ | 0.4 |
| Max failures analyzed | 10 (SR < 0.4) / 5 (SR > 0.4) |
| Max new skills per evolution | 3 |
