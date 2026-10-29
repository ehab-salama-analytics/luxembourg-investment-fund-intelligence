# Luxembourg Investment Fund Intelligence
Executive statistical report · 29 October 2026

Validated run: `20261028T234800_179012`. 51 checks passed; 0 failed. Local supplied source vintage only.

## Executive findings

- ECB Luxembourg total fund assets reached **EUR 9.462 trillion** in **2026-Q2** (9,462,105.000 EUR million). End-period stock; source: file 01, `IVF.Q.LU.N.T0.T00.A.1.Z5.0000.Z01.E`.
- Quarterly asset growth was **9.26%**: (9,462,105.000 / 8,660,034.000 − 1) × 100. Annual growth was **25.76%**: (9,462,105.000 / 7,523,777.000 − 1) × 100. Same ECB population and source; asset growth is not an investment return.
- Luxembourg represented **38.68%** of euro-area fund assets at 2026-Q2: LU T00 stock / U2 T00 stock × 100. U2 is the changing-composition aggregate; no country-plus-aggregate sum.
- At 2026-Q2, ECB Luxembourg shares outstanding were **EUR 8,490.652 billion**; gross issues **617.992 billion** and redemptions **585.909 billion**. Net issuance = issues − redemptions = **32.083 billion**. Source: file 02, LU L30 data types 1/2/3. Quarterly flows; stocks at quarter-end.
- Net issuance rate was **0.41%**: 32,083.000 / previous-quarter shares 7,796,504.000 × 100, in EUR millions. Flow intensity, not performance.
- Reported transactions were **EUR 78.508 billion** (file 02, LU L30/4); issuance-minus-transactions difference **EUR -46,424.678000 million**. Shares-stock change less transactions was **EUR 615.640 billion**; this residual can include valuation, exchange-rate and reclassification effects and is not a pure market return.
- From 2018-Q1 to 2026-Q2, Luxembourg assets changed from 4.243 to 9.462 EUR trillion: (9,462,105.000/4,242,824.000 − 1) × 100 = 123.01%. Same non-MMF ECB reporting sector; source file 01.
- Largest Luxembourg quarterly decline in supplied history: **-9.61% in 2020-Q1**; largest increase **9.37% in 2025-Q4**. Each equals current T00 stock/prior consecutive stock − 1; full calculation operands are in mart_ecb_quarterly.

## Latest European comparison

2026-Q2; ECB investment funds excluding money-market and pension funds. Stocks in EUR billion; growth and statistical shares in percent. File 01, area-specific T00/1 series.

| Reporting area | Assets, EUR bn | QoQ % | YoY % | Share of euro area % |
|---|---:|---:|---:|---:|
| Germany | 3,413.383 | 6.21 | 10.00 | 13.96 |
| France | 2,261.167 | 6.12 | 12.93 | 9.24 |
| Ireland | 6,212.841 | 11.63 | 30.41 | 25.40 |
| Luxembourg | 9,462.105 | 9.26 | 25.76 | 38.68 |
| Euro area (changing composition) | 24,459.491 | 8.84 | 21.41 | 100.00 |

## CSSF Luxembourg context — separate population

At **2026-08**, the supplied CSSF workbook reports **2,961 UCIs** and **EUR 6,790.699 billion** net assets (Evolution générale, B62/G62). Monthly net issuance was **EUR 45.881 billion** = 493.631 issues − 447.750 redemptions (C62:E62). The EUR 104.125 billion monthly net-asset increase comprises EUR 45.881 billion net issuance plus EUR 58.244 billion reported financial-market variation (F62:H62).

The workbook contains 57 observed months, not an invented history. Its detailed table supports legal-status and legal-form comparisons. Redemption figures include UCIs liquidated during the month. CSSF net assets are not ECB total assets; there is no cross-source join or reconciliation claim.

## Review indicators and limitations

Across all 170 area-quarter observations, the maximum absolute difference between derived net issuance and reported transactions is EUR 95,240.858677 million. Differences are retained, not forced to zero.
Monitoring flags show consecutive asset declines and changes in net-issuance sign. These are descriptive review prompts, not regulatory risk ratings. No individual-fund performance, customer benefit or causal driver can be established from these aggregates.
Only one source vintage is available. Future manually supplied revisions require schema/definition review and an explicit source-contract update. Missing comparisons remain blank. Euro-area composition can change. Report visual acceptance is recorded separately from pipeline validation.

## Interpretation references

- ECB investment fund statistics: https://www.ecb.europa.eu/stats/financial_corporations/investment_funds/html/index.en.html
- ECB explanatory notes: https://www.ecb.europa.eu/stats/pdf/money/aggregates/ecb.investmentfundstatexplnotes201901.en.pdf
- CSSF statistics catalogue: https://www.cssf.lu/en/statistics/
These references were used for interpretation only. All numerical findings use the three supplied local files.

## Reconciliation interpretation

The ECB investment-fund statistics manual, paragraphs 135–137, includes income-related components net of management charges in financial transactions. Therefore reported transactions need not equal gross issues less redemptions. The supplied files cannot fully attribute the observed difference, which remains disclosed rather than forced to zero. Reference: https://www.ecb.europa.eu/pub/pdf/other/manualinvestmentfundstatistics201712.en.pdf

The four-page Power BI report passed ten scoped Desktop acceptance checks on 29 October 2026. Six fault-injection tests also passed. These are separate from the 51 independent data checks.
