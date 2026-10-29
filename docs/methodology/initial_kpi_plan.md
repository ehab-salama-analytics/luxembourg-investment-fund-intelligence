# KPI plan and approved methodology

Source verification supports all 12 requested KPI families. There is no fund-strategy breakdown in the ECB extracts; use total-sector statistics only. CSSF structural measures come from actual legal-status/form cells.

| KPI | Rule | Availability and safeguards |
|---|---|---|
| Total assets | T00/1 end-quarter stock | All five areas, 34 quarters |
| Quarterly growth | (stock / exact preceding-quarter stock − 1) × 100 | 33 comparisons per area; positive denominator |
| Annual growth | (stock / same quarter last year − 1) × 100 | 30 comparisons per area; positive denominator |
| Shares outstanding | L30/1 stock | Separate from total assets |
| Gross issues | L30/2 flow | Source-reported, EUR millions |
| Redemptions | L30/3 flow | Source-reported positive redemption amount |
| Net issuance | issues − redemptions | Do not rename as reported transactions |
| Issuance rate | net issuance / exact prior-quarter shares × 100 | Flow intensity, never investment performance |
| European comparison | Compatible measures, quarter and units | DE, FR, IE, LU, U2; no total across all five |
| Luxembourg statistical share | LU T00 / U2 T00 × 100 | U2 changes composition; not company market share |
| CSSF context | Source monthly history and structural cells | Separate population, EUR billions and counts |
| Monitoring | decline; two consecutive declines; net-issuance sign reversal | Descriptive flags, no regulatory thresholds |

## Stocks, flows and the observed reconciliation difference

The supplied collection attributes are E for stocks and transactions, S for gross issues/redemptions. The source DATA_TYPE and complete title govern stock/flow classification: type 4 remains a financial flow despite COLLECTION=E. All supplied series have FREQ=Q and TIME_FORMAT=P3M. Preserve these attributes without silently reinterpreting periods.

At 2026 Q2 Luxembourg net issuance is EUR 32,083 million, compared with reported transactions of EUR 78,507.678 million: difference −46,424.678 million. Across all source observations the maximum absolute difference is EUR 95,240.858677 million. This is a methodological reconciliation item, not a failed arithmetic test.

The [ECB investment-fund statistics manual](https://www.ecb.europa.eu/pub/pdf/other/manualinvestmentfundstatistics201712.en.pdf), paragraphs 135–137, explains that transactions in fund shares include subscriptions less redemptions and income-related components net of management charges. The files do not contain the components needed to attribute each difference fully. Do not describe the residual as a measured reinvested-income amount or force equality.

Shares-stock change minus reported transactions is a descriptive nontransaction residual. It can contain valuation, currency and classification effects. Total-asset change is also retained but is not reconciled to a shares-liability flow as though they were the same balance-sheet item.

## Population and scaling

The [ECB overview](https://www.ecb.europa.eu/stats/financial_corporations/investment_funds/html/index.en.html) excludes money-market and pension funds. The CSSF workbook contains supervised UCI categories including Part I, Part II, FIS and SICAR. No cross-source join asserts matching coverage. CSSF history is monthly; structural detail is August 2026 only. Redemption footnotes include liquidated UCIs.

ECB EUR/10^6 values are retained unchanged. Presentation in EUR billion divides by 1,000; EUR trillion divides by 1,000,000. CSSF monetary values are already EUR billion; counts remain counts. CSSF H is an absolute monthly change, not a percentage. Structural totals are reconciliation controls, not additive fact rows.

## Missing observations, revisions and controls

No ECB numerical blanks, duplicate observations or internal quarter gaps exist in this vintage. The first growth comparisons remain missing; CSSF first-month market variation and change remain missing. No interpolation or forward fill. A changed hash stops the build until the operator reviews the vintage and explicitly updates the source contract. Previous run folders remain intact. Source status flags and metadata are preserved; changed series dimensions fail the ingestion contract.

The Power BI layer uses SELECTEDVALUE for ECB metrics and explicit latest-selected-quarter card measures. It does not sum stocks over dates or sum countries with U2. Empty/ambiguous metric contexts return blank. Structural sums use only additive CSSF leaf cells. Pipeline validation does not substitute for Power BI visual and interaction acceptance.
