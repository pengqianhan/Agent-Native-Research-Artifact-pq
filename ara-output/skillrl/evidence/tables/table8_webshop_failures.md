# Table 8: Common Failures in Web-based Shopping Tasks

- **Source**: Table 8, Appendix C (page 16)
- **Caption**: "Common Failures in Web-based Shopping Tasks."
- **Extraction type**: raw_table

| ID | Failure Description | Root Cause | Mitigation Strategy |
|----|--------------------|-------------|---------------------|
| err_001 | Missing Constraints in Query | Omits size or price caps, leading to overwhelming or irrelevant result sets. | Assemble full requirement list first; ensure every hard constraint is in the query string. |
| err_004 | Price Shift Oversight | Fails to notice price changes after selecting a specific size or color variant. | Re-read the price element after every option change before proceeding to checkout. |
| err_005 | Premature Purchase | Clicks "Buy Now" without setting mandatory variants, leading to errors or wrong items. | Validate that every required dropdown/radio option is explicitly selected before buying. |
| err_009 | Ignoring Stock Status | Attempts to purchase out-of-stock items by ignoring disabled buttons or 'Out of Stock' messages. | Verify that the 'Add to Cart' button is enabled and no 'Out of Stock' message is present post-selection. |
| err_011 | Sponsored Link Distraction | Clicks loosely matched ads, diverting the workflow from organic, suitable products. | Implement ad-label detection; prioritize organic listings for higher constraint reliability. |
