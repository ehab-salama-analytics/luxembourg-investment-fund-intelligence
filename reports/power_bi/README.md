# Power BI report and acceptance

**Accepted for local MVP demonstration on 29 October 2026.** Open `Luxembourg_Fund_Intelligence.pbip` with its adjacent `.Report` and `.SemanticModel` folders. The local model has been refreshed and saved in Power BI Desktop. No Power BI Service deployment or scheduled distribution is claimed.

## Pages

1. Executive fund industry overview: Luxembourg assets, growth, euro-area share and history.
2. Fund shares and capital flows: shares stock, issues, redemptions, derived net issuance, reported transactions and flow intensity.
3. European benchmarking: the five source reporting areas at the latest selected quarter, with the euro-area aggregate explicitly identified.
4. Luxembourg fund industry structure: August 2026 CSSF headline values and legal-status/form breakdowns.

Quarter slicers apply to the page's charts. Cards use the latest selected quarter; with All selected, they show 2026 Q2. Clearing a selection restores the full history. Growth comparisons unavailable in the source history display a dash. CSSF structural charts cross-highlight each other; its headline cards deliberately show the full CSSF population, as stated on the page. No relationship joins CSSF to ECB.

Monetary headline cards show EUR billions explicitly. Chart axes may abbreviate thousands as K; with EUR-billion charts, 1K means EUR 1,000 billion. The analytical extracts and executive report preserve full precision. Stocks are never summed across quarters; ambiguous ECB metric contexts return blank. U2 is never added to its constituent countries.

## Executed Desktop acceptance

| Check | Observed outcome |
|---|---|
| Native project load and local refresh | PASS; three reporting tables loaded |
| Four-page navigation and rendering | PASS; all pages inspected, no remaining visual errors |
| Overview latest-quarter reconciliation | PASS; 9,462.1 EUR bn, 9.26% QoQ, 25.76% YoY, 38.68% share |
| 2018 Q1 filter and missing comparisons | PASS; 4,242.8 EUR bn, both growth cards blank, share 34.27% |
| Clearing the quarter filter | PASS; full history and latest-quarter cards restored |
| Flow-page reconciliation | PASS; shares 8,490.7, issues 618.0, redemptions 585.9, net issuance 32.1, transactions 78.5 EUR bn; rate 0.41% |
| Benchmark annual growth | PASS; U2 21.41%, FR 12.93%, DE 10.00%, IE 30.41%, LU 25.76% |
| CSSF headline and structural values | PASS; 2,961 UCIs, 6,790.7 EUR bn net assets; legal forms 36 / 1,063 / 135 / 1,727 |
| CSSF FIS cross-highlight | PASS; other UCI/FIS 36, FCP 217, SICAR 0, SICAV 760; full-population cards remain unchanged |
| Clearing CSSF selection | PASS; complete structural totals restored |

**10 scoped acceptance checks passed; 0 failed.** Earlier duplicate measure names, missing report theme configuration and a reserved-table-name DAX error were corrected before acceptance. These checks are distinct from 51 independent data-validation checks and six fault-injection tests. They do not establish exhaustive testing of every filter combination, accessibility, mobile layouts or Service behaviour.

Genuine unaltered Desktop captures are in `../../assets/screenshots/`: four report pages and two focused acceptance tests. They are actual report screenshots, not mockups.

## Refresh and portability

The DataFolder expression points to the selected local validated run. Rebuild with `python src/build_power_bi.py` after a successful new pipeline run, or deliberately update DataFolder to the new run's analytical directory and refresh. The builder regenerates report definitions; preserve manual report customisations before rerunning it. Public copies replace DataFolder with `SET_VALIDATED_ANALYTICAL_FOLDER_BEFORE_REFRESH` and exclude caches. Generate the required extracts locally before opening/refreshing a public copy.
