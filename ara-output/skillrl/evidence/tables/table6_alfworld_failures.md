# Table 6: Common Agent Failures and Mitigation Strategies for ALFWorld

- **Source**: Table 6, Appendix C (page 15)
- **Caption**: "Common Agent Failures and Mitigation Strategies for ALFWorld."
- **Extraction type**: raw_table

| ID | Failure Description | Root Cause (Why it happens) | Mitigation (How to avoid) |
|----|--------------------|------------------------------|---------------------------|
| err_001 | Redundant Revisit | Lacks explicit memory of explored areas; strategy degenerates into local loops. | Maintain an exploration map; prioritize unvisited candidates. |
| err_006 | Skipping State Changes | Conflates object presence with goal satisfaction; omits cleanliness/temp checks. | Integrate state precondition checks into the planner before placement. |
