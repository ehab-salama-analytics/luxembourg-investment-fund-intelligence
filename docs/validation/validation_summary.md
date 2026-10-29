# Independent validation

Run 20261028T234800_179012

51 passed; 0 failed.

- PASS: 01_ECB_IVF_Total_Assets_2018_Onward.csv hash
- PASS: 01_ECB_IVF_Total_Assets_2018_Onward.csv observation count
- PASS: 02_ECB_IVF_Fund_Shares_and_Flows_2018_Onward.csv hash
- PASS: 02_ECB_IVF_Fund_Shares_and_Flows_2018_Onward.csv observation count
- PASS: 03_CSSF_Basic_Statistical_Data_UCIs_August_2026.xlsx hash
- PASS: Raw/staging/fact cardinality
- PASS: Unique full series-period grain
- PASS: Unique KPI area-period grain
- PASS: All physical metadata preserved
- PASS: Numeric values reconcile
- PASS: Units and scaling retained
- PASS: Quarter parsing
- PASS: Five reporting areas only
- PASS: Geography labels
- PASS: Stock/flow classification
- PASS: No CSSF observations mixed into ECB
- PASS: Independent full-source KPI assets
- PASS: Independent full-source KPI shares
- PASS: Independent full-source KPI gross_issues
- PASS: Independent full-source KPI redemptions
- PASS: Independent full-source KPI transactions
- PASS: Independent full-source KPI qoq_growth_pct
- PASS: Independent full-source KPI yoy_growth_pct
- PASS: Independent full-source KPI net_issuance
- PASS: Independent full-source KPI net_issuance_rate_pct
- PASS: Independent full-source KPI share_of_euro_area_pct
- PASS: Independent full-source KPI issuance_transaction_difference
- PASS: Independent full-source KPI shares_nontransaction_residual
- PASS: Independent full-source KPI asset_change
- PASS: First quarter growth unavailable
- PASS: First four quarters annual growth unavailable
- PASS: Euro area denominator is source aggregate
- PASS: Missing-quarter lookup fixture
- PASS: Missing numeric observations preserved
- PASS: CSSF history cardinality
- PASS: CSSF month grain
- PASS: CSSF raw numeric reconciliation
- PASS: CSSF issuance arithmetic
- PASS: CSSF stock movement
- PASS: CSSF movement components
- PASS: CSSF initial missing changes preserved
- PASS: CSSF structural leaf grain
- PASS: CSSF totals excluded from leaf fact
- PASS: CSSF structural raw reconciliation
- PASS: CSSF structural counts tie to history
- PASS: CSSF structural net assets tie to history
- PASS: CSSF row/column count margins
- PASS: CSSF row/column asset margins
- PASS: CSSF umbrella count identity
- PASS: CSSF compartment/unit identity
- PASS: CSSF lossless nonblank cell count

Full execution evidence: data/runs/20261028T234800_179012/validation.json. Raw CSV expectations use Python csv and Decimal; workbook checks read source cells independently. Power BI interactions are a separate acceptance activity.
