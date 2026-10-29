"""Generate dated findings only from the candidate validated run."""
from datetime import datetime
from zoneinfo import ZoneInfo

def executive(root,run,k,h,result):
    latest=k.TIME_PERIOD.max(); lu=k[(k.REF_AREA=='LU')&(k.TIME_PERIOD==latest)].iloc[0]
    history=k[k.REF_AREA=='LU'].sort_values('TIME_PERIOD'); first=history.iloc[0]; last=h.iloc[-1]
    worst=history.loc[history.qoq_growth_pct.idxmin()]; best=history.loc[history.qoq_growth_pct.idxmax()]
    out=['# Luxembourg Investment Fund Intelligence',f'Executive statistical report · {datetime.now(ZoneInfo("Europe/Paris")).date()}',
       '',f'Validated run: `{run.name}`. {result["passed"]} checks passed; {result["failed"]} failed. Local supplied source vintage only.','',
       '## Executive findings','',
       f'- ECB Luxembourg total fund assets reached **EUR {lu.assets/1e6:,.3f} trillion** in **{latest}** ({lu.assets:,.3f} EUR million). End-period stock; source: file 01, `IVF.Q.LU.N.T0.T00.A.1.Z5.0000.Z01.E`.',
       f'- Quarterly asset growth was **{lu.qoq_growth_pct:.2f}%**: ({lu.assets:,.3f} / {lu.previous_assets:,.3f} − 1) × 100. Annual growth was **{lu.yoy_growth_pct:.2f}%**: ({lu.assets:,.3f} / {lu.year_ago_assets:,.3f} − 1) × 100. Same ECB population and source; asset growth is not an investment return.',
       f'- Luxembourg represented **{lu.share_of_euro_area_pct:.2f}%** of euro-area fund assets at {latest}: LU T00 stock / U2 T00 stock × 100. U2 is the changing-composition aggregate; no country-plus-aggregate sum.',
       f'- At {latest}, ECB Luxembourg shares outstanding were **EUR {lu.shares/1000:,.3f} billion**; gross issues **{lu.gross_issues/1000:,.3f} billion** and redemptions **{lu.redemptions/1000:,.3f} billion**. Net issuance = issues − redemptions = **{lu.net_issuance/1000:,.3f} billion**. Source: file 02, LU L30 data types 1/2/3. Quarterly flows; stocks at quarter-end.',
       f'- Net issuance rate was **{lu.net_issuance_rate_pct:.2f}%**: {lu.net_issuance:,.3f} / previous-quarter shares {lu.previous_shares:,.3f} × 100, in EUR millions. Flow intensity, not performance.',
       f'- Reported transactions were **EUR {lu.transactions/1000:,.3f} billion** (file 02, LU L30/4); issuance-minus-transactions difference **EUR {lu.issuance_transaction_difference:,.6f} million**. Shares-stock change less transactions was **EUR {lu.shares_nontransaction_residual/1000:,.3f} billion**; this residual can include valuation, exchange-rate and reclassification effects and is not a pure market return.',
       f'- From {first.TIME_PERIOD} to {latest}, Luxembourg assets changed from {first.assets/1e6:.3f} to {lu.assets/1e6:.3f} EUR trillion: ({lu.assets:,.3f}/{first.assets:,.3f} − 1) × 100 = {(lu.assets/first.assets-1)*100:.2f}%. Same non-MMF ECB reporting sector; source file 01.',
       f'- Largest Luxembourg quarterly decline in supplied history: **{worst.qoq_growth_pct:.2f}% in {worst.TIME_PERIOD}**; largest increase **{best.qoq_growth_pct:.2f}% in {best.TIME_PERIOD}**. Each equals current T00 stock/prior consecutive stock − 1; full calculation operands are in mart_ecb_quarterly.',
       '', '## Latest European comparison', '', f'{latest}; ECB investment funds excluding money-market and pension funds. Stocks in EUR billion; growth and statistical shares in percent. File 01, area-specific T00/1 series.','',
       '| Reporting area | Assets, EUR bn | QoQ % | YoY % | Share of euro area % |','|---|---:|---:|---:|---:|']
    for r in k[k.TIME_PERIOD==latest].itertuples(): out.append(f'| {r.area} | {r.assets/1000:,.3f} | {r.qoq_growth_pct:.2f} | {r.yoy_growth_pct:.2f} | {r.share_of_euro_area_pct:.2f} |')
    out += ['', '## CSSF Luxembourg context — separate population','',
       f'At **{last.month}**, the supplied CSSF workbook reports **{int(last.uci_count):,} UCIs** and **EUR {last.net_assets:,.3f} billion** net assets (Evolution générale, B62/G62). Monthly net issuance was **EUR {last.net_issuance:,.3f} billion** = {last.gross_issues:,.3f} issues − {last.redemptions:,.3f} redemptions (C62:E62). The EUR {last.monthly_change:,.3f} billion monthly net-asset increase comprises EUR {last.net_issuance:,.3f} billion net issuance plus EUR {last.market_variation:,.3f} billion reported financial-market variation (F62:H62).',
       '', 'The workbook contains 57 observed months, not an invented history. Its detailed table supports legal-status and legal-form comparisons. Redemption figures include UCIs liquidated during the month. CSSF net assets are not ECB total assets; there is no cross-source join or reconciliation claim.',
       '', '## Review indicators and limitations','',
       f'Across all 170 area-quarter observations, the maximum absolute difference between derived net issuance and reported transactions is EUR {k.issuance_transaction_difference.abs().max():,.6f} million. Differences are retained, not forced to zero.',
       'Monitoring flags show consecutive asset declines and changes in net-issuance sign. These are descriptive review prompts, not regulatory risk ratings. No individual-fund performance, customer benefit or causal driver can be established from these aggregates.',
       'Only one source vintage is available. Future manually supplied revisions require schema/definition review and an explicit source-contract update. Missing comparisons remain blank. Euro-area composition can change. Report visual acceptance is recorded separately from pipeline validation.',
       '', '## Interpretation references','',
       '- ECB investment fund statistics: https://www.ecb.europa.eu/stats/financial_corporations/investment_funds/html/index.en.html',
       '- ECB explanatory notes: https://www.ecb.europa.eu/stats/pdf/money/aggregates/ecb.investmentfundstatexplnotes201901.en.pdf',
       '- CSSF statistics catalogue: https://www.cssf.lu/en/statistics/',
       'These references were used for interpretation only. All numerical findings use the three supplied local files.']
    text='\n'.join(out)
    (run/'executive_report.md').write_text(text,encoding='utf-8')
    dest=root/'reports/executive'; dest.mkdir(parents=True,exist_ok=True)
    (dest/f'executive_report_{run.name}.md').write_text(text,encoding='utf-8')
    vd=root/'docs/validation'; vd.mkdir(parents=True,exist_ok=True)
    (vd/'validation_summary.md').write_text('# Independent validation\n\nRun '+run.name+f'\n\n{result["passed"]} passed; {result["failed"]} failed.\n\n'+ '\n'.join(f'- {"PASS" if c["passed"] else "FAIL"}: {c["check"]}' for c in result['checks'])+'\n\nFull execution evidence: data/runs/'+run.name+'/validation.json. Raw CSV expectations use Python csv and Decimal; workbook checks read source cells independently. Power BI interactions are a separate acceptance activity.\n',encoding='utf-8')
