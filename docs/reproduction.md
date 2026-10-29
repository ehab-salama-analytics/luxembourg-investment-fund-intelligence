# Local reproduction

1. Use Python 3.12+ and install requirements.txt in your own environment.
2. Place the three named manually downloaded files in data/raw. This project contains no acquisition code.
3. Run `python src/pipeline.py` from the project directory. The code resolves paths relative to itself.
4. Inspect the printed validation counts and data/latest_validated.json. Failed runs retain status.json and do not replace this pointer.
5. Run `python src/validation/validate.py` for an independent recheck of the selected validated run.
6. Run `python src/build_power_bi.py` to generate the editable report against that run's CSV extracts. Open reports/power_bi/Luxembourg_Fund_Intelligence.pbip in Power BI Desktop and refresh.

Each run has staging, analytical Parquet/CSV, a source manifest, validation evidence, status and an executive report. A dated executive copy is also saved in reports/executive. Never treat a partially written run as released: only latest_validated.json selects a successful release. Prior run folders are never overwritten.

The local execution environment uses the bundled Python runtime plus a project-local .runtime/pyarrow installation. This convenience folder is excluded from publication; ordinary reproduction uses requirements.txt.

## Manually supplied updates

Keep a backup of your prior source vintage before replacing raw files. A different source hash fails safely. Inspect the refreshed source_inventory.json, schema, complete titles, areas, frequency, units, statuses and coverage. Compare old/new observations by KEY and TIME_PERIOD to document revisions. Only after review, update approved_source_contract.json to the inspected manifest and rerun. The code rejects altered fixed dimensions and duplicate keys. CSSF schema changes require parser review; do not simply change the hash to bypass incompatible source content.

## Publication

Exclude data, runtimes, caches, private instructions and model data. Replace the local DataFolder expression with a neutral setup placeholder in a separate publication copy. Publish no raw data without a separate redistribution decision. GitHub creation/push requires the user's approval of the proposed identity and reviewed file list.
