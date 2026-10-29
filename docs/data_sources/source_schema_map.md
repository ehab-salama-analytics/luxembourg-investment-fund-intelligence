# Physical source schema

## 01_ECB_IVF_Total_Assets_2018_Onward.csv

| Physical column | Blank records |
|---|---:|
| KEY | 0 |
| FREQ | 0 |
| REF_AREA | 0 |
| ADJUSTMENT | 0 |
| IVF_REP_SECTOR | 0 |
| IVF_ITEM | 0 |
| MATURITY_ORIG | 0 |
| DATA_TYPE | 0 |
| COUNT_AREA | 0 |
| BS_COUNT_SECTOR | 0 |
| CURRENCY_TRANS | 0 |
| BS_SUFFIX | 0 |
| TIME_PERIOD | 0 |
| OBS_VALUE | 0 |
| OBS_STATUS | 0 |
| OBS_CONF | 0 |
| OBS_PRE_BREAK | 170 |
| OBS_COM | 170 |
| TIME_FORMAT | 0 |
| COLLECTION | 0 |
| COMPILING_ORG | 170 |
| DISS_ORG | 170 |
| DOM_SER_IDS | 170 |
| PUBL_MU | 170 |
| PUBL_PUBLIC | 170 |
| UNIT_INDEX_BASE | 170 |
| UNIT_PRICE_BASE | 170 |
| AGG_EQUN | 170 |
| COMPILATION | 170 |
| COVERAGE | 170 |
| DECIMALS | 0 |
| SOURCE_AGENCY | 170 |
| SOURCE_DETAIL | 170 |
| TITLE | 0 |
| TITLE_COMPL | 0 |
| UNIT | 0 |
| UNIT_MULT | 0 |
## 02_ECB_IVF_Fund_Shares_and_Flows_2018_Onward.csv

| Physical column | Blank records |
|---|---:|
| KEY | 0 |
| FREQ | 0 |
| REF_AREA | 0 |
| ADJUSTMENT | 0 |
| IVF_REP_SECTOR | 0 |
| IVF_ITEM | 0 |
| MATURITY_ORIG | 0 |
| DATA_TYPE | 0 |
| COUNT_AREA | 0 |
| BS_COUNT_SECTOR | 0 |
| CURRENCY_TRANS | 0 |
| BS_SUFFIX | 0 |
| TIME_PERIOD | 0 |
| OBS_VALUE | 0 |
| OBS_STATUS | 0 |
| OBS_CONF | 0 |
| OBS_PRE_BREAK | 680 |
| OBS_COM | 680 |
| TIME_FORMAT | 0 |
| COLLECTION | 0 |
| COMPILING_ORG | 680 |
| DISS_ORG | 680 |
| DOM_SER_IDS | 680 |
| PUBL_MU | 680 |
| PUBL_PUBLIC | 680 |
| UNIT_INDEX_BASE | 680 |
| UNIT_PRICE_BASE | 680 |
| AGG_EQUN | 680 |
| COMPILATION | 680 |
| COVERAGE | 680 |
| DECIMALS | 0 |
| SOURCE_AGENCY | 680 |
| SOURCE_DETAIL | 680 |
| TITLE | 0 |
| TITLE_COMPL | 0 |
| UNIT | 0 |
| UNIT_MULT | 0 |
## CSSF workbook

History A=month, B=UCI count, C=gross issues, D=redemptions, E=net issuance, F=financial-market variation, G=net assets, H=absolute monthly change. Monetary values are EUR billions; B is a count. H is not a percentage.

Detailed tables retain legal status (Part I, Part II, FIS, SICAR) and legal form (FCP, SICAV, Other UCI/FIS, SICAR). Totals are controls, excluded from the additive leaf fact. The 32-cell structural fact is 4 statuses × 4 forms × 2 measures. Umbrella counts, compartments and distributions remain available in lossless cell staging.

## Grain and semantics
ECB grain: KEY + TIME_PERIOD. KEY retains all source dimensions. T00/1=assets stock; L30/1=shares stock; L30/2=gross issues flow; L30/3=redemptions flow; L30/4=transactions flow. All series use N/T0/A/Z5/0000/Z01/E dimensions. No supported fund-strategy breakdown exists, so no invented fund-category dimension.

Source TITLE and TITLE_COMPL are preserved verbatim with all 37 physical fields. OBS_STATUS=A for all 850 observations; OBS_CONF=F. Blank OBS_PRE_BREAK, OBS_COM and other optional metadata are not missing numerical observations.