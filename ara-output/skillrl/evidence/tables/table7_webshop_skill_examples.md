# Table 7: Example distilled skills for WebShop Navigation

- **Source**: Table 7, Appendix C (page 16)
- **Caption**: "Example distilled skills for WebShop Navigation (Yao et al., 2022a). These skills represent the strategic patterns used by the agent to handle large-scale product search and constraint satisfaction."
- **Extraction type**: raw_table

**Search & Query Engineering**

| ID | Skill Title | Principle (Actionable Pattern) | When to Apply |
|----|-------------|-------------------------------|---------------|
| gen_001 | Prioritize Core Keywords | Include product type, 1-2 functional attributes, and hard constraints; omit secondary descriptors. | Before issuing the first search or refining over-specific queries. |
| gen_002 | Iterative Refinement | Adjust keywords or apply site filters instead of repeating the same failed query. | When results are irrelevant or repeat despite multiple searches. |

**Product Evaluation & Verification**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_003 | Scan Before You Click | Read titles, thumbnails, and prices in results to ensure plausibility before opening a link. | On search results pages when choosing the next product to inspect. |
| gen_004 | Verify Early, Abort Fast | Immediately check category, attributes, and price on the product page; leave if any constraint is violated. | Within the first observation on every product detail page. |
| gen_006 | Confirm Hidden Attributes | Open Description/Features sections to ensure non-visible specs (e.g., material) meet constraints. | When constraints are not evident from the title or variant list. |

**Configuration & Transaction**

| ID | Skill Title | Principle | When to Apply |
|----|-------------|-----------|---------------|
| gen_005 | Set Mandatory Variants | Always select required options (size, color, etc.) before evaluating price or purchasing. | After confirming product match but before any purchase action. |
| gen_007 | Check Variant Pricing | For price ranges, select the exact variant combination to verify the specific price is within budget. | Whenever price changes with variant selection or shows as a range. |
| gen_013 | Purchase Decisively | Execute "Buy Now" immediately once all constraints and prices are confirmed on a variant. | After validating every constraint on the current product variant. |
