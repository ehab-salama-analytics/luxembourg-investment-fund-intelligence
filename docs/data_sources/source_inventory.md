# Source inventory

Inspected locally on 28 October 2026. Files remain unchanged; no raw data acquired. Hashes identify this supplied vintage, not remote provenance certification.

## 01_ECB_IVF_Total_Assets_2018_Onward.csv
- Size: 88,493 bytes
- SHA-256: `1fae4cd0d8c72296fcc4ec5dfcd388ff534e6b1ae2cb4f39f57b757b9ccc9cd3`
- 170 observations × 37 fields; 5 series
- Coverage: 2018-Q1–2026-Q2; areas DE, FR, IE, LU, U2; quarterly
- Duplicate KEY/TIME_PERIOD: 0; missing OBS_VALUE: 0; statuses: {'A': 170}
- Units: EUR, UNIT_MULT=6 (EUR millions); no metadata/footer records encountered.
- No internal quarter gaps in the supplied series. Blank metadata counts and full series descriptions: source_inventory.json.

## 02_ECB_IVF_Fund_Shares_and_Flows_2018_Onward.csv
- Size: 351,396 bytes
- SHA-256: `911f464565850d66bf1f9c37075ac43b834a53b4560cf8db77c95fe057e9dfb3`
- 680 observations × 37 fields; 20 series
- Coverage: 2018-Q1–2026-Q2; areas DE, FR, IE, LU, U2; quarterly
- Duplicate KEY/TIME_PERIOD: 0; missing OBS_VALUE: 0; statuses: {'A': 680}
- Units: EUR, UNIT_MULT=6 (EUR millions); no metadata/footer records encountered.
- No internal quarter gaps in the supplied series. Blank metadata counts and full series descriptions: source_inventory.json.

## 03_CSSF_Basic_Statistical_Data_UCIs_August_2026.xlsx
- Size: 26,443 bytes
- SHA-256: `a05da3f6c74cbc5f9f2a4cbd5e8d045713517e8e9e66a78246e821169845aded`
- Genuine readable XLSX, two sheets; report date 2026-08-01 (August reference month).
- Evolution générale: A5:H5 headers, A6:H62 observations, 57 months from 2021-12 to 2026-08; A63 redemption footnote. Declared used range A1:H80 includes formatting-only trailing rows.
- Stat. détaillée: A1:H42 used range; counts A7:F12, assets A17:F22, umbrella structure A27:F28, flows A33:F36, distributions A41:F42.
- First history row has no market variation or monthly change; retain these two blanks. No duplicate months.
- Reader warnings concern print-area and header/footer formatting; all observation cells are readable.
- Redemption footnote: includes UCIs liquidated during the reference month.

## Statistical boundaries
ECB: investment funds excluding MMFs and pension funds. CSSF: workbook UCI population including displayed Part I, Part II, FIS and SICAR categories; do not assert equality with the ECB perimeter. U2 denotes changing euro-area composition. No historical revision vintage is available; changes to future supplied hashes require review.