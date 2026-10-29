# Luxembourg Investment Fund Intelligence & Automated Reporting

QuantRisk Analytics portfolio project #3 — ANALYSE → AUTOMATE → TRAIN.

## Objective
Turn manually supplied ECB investment-fund statistics and CSSF UCI statistics into traceable industry analysis, European benchmarks and repeatable reporting. Intended users include fund administrators, ManCos, AIFMs, asset managers and FundTech teams. This is an aggregate-data portfolio demonstration and a proposed consultancy offering, not a client deployment or individual-fund performance model.

## Approved scope
Preserve the three supplied raw files. Build local Python staging, Parquet facts, explicitly defined KPIs, independent validation, an executive report and a four-page Power BI report. Document source evidence, limitations and reproduction. Prepare public source code and portfolio materials; external publication requires the user's approval of the repository identity and publication plan.

## Boundaries
No source downloads, fabricated observations, silent interpolation, mixing CSSF and ECB populations, claims of investment returns, customer savings or regulatory approval. Do not modify Projects #1 or #2. Euro-area totals must never be added to constituent countries. Failed source or validation checks prevent release of new analytical outputs.

## Initial evidence — 28 October 2026
All three supplied files are readable. ECB assets: 170 observations; shares/flows: 680 observations; both have 37 columns and cover 2018 Q1–2026 Q2 across DE, FR, IE, LU and U2. CSSF has two worksheets, 57 monthly observations (December 2021–August 2026) and August 2026 structural tables. Source verification details are in docs/data_sources/.

## Acceptance
A: actual source inventory and schema; B: reconciled analytical foundation; C: verified KPIs; D: sourced findings; E: functional Power BI report with visual/interaction acceptance; F: successful repeatable local workflow; G: commercial case study, presentation, genuine screenshots and reviewed publication package. Incomplete acceptance must remain visible in project status.
