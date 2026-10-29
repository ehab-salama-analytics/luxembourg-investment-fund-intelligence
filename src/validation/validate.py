"""Independent raw-to-output checks: csv/Decimal and direct workbook cells.
Does not import transformation helpers or derive expectations from KPI outputs.
"""
import csv, hashlib, json, math, re
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '.runtime'))
import pandas as pd
import openpyxl

def validate(root,run):
    checks=[]
    def check(name,ok,detail=''):
        checks.append({'check':name,'passed':bool(ok),'detail':str(detail)})
    def close(a,b,tol=0.000001):
        if b is None: return pd.isna(a)
        return not pd.isna(a) and math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=tol)
    manifest=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
    raw=[]
    for e in manifest:
        f=root/'data/raw'/e['file']
        check(e['file']+' hash',hashlib.sha256(f.read_bytes()).hexdigest()==e['sha256'])
        if f.suffix=='.csv':
            with f.open(encoding='utf-8-sig',newline='') as stream:
                rows=list(csv.DictReader(stream))
            check(e['file']+' observation count',len(rows)==e['rows'])
            raw.extend(rows)
    stage=pd.read_parquet(run/'staging/ecb_source.parquet')
    fact=pd.read_parquet(run/'analytical/fact_investment_fund_statistics.parquet')
    mart=pd.read_parquet(run/'analytical/mart_ecb_quarterly.parquet')
    check('Raw/staging/fact cardinality',len(raw)==len(stage)==len(fact))
    check('Unique full series-period grain',not fact.duplicated(['KEY','TIME_PERIOD']).any())
    check('Unique KPI area-period grain',not mart.duplicated(['REF_AREA','TIME_PERIOD']).any())
    check('All physical metadata preserved',all(all(str(stage.iloc[i][c])==v and str(fact.iloc[i][c])==v for c,v in row.items()) for i,row in enumerate(raw)))
    check('Numeric values reconcile',all(close(fact.iloc[i].observation_value,None if row['OBS_VALUE']=='' else Decimal(row['OBS_VALUE'])) for i,row in enumerate(raw)))
    check('Units and scaling retained',set(fact.UNIT)=={'EUR'} and set(fact.UNIT_MULT)=={'6'})
    check('Quarter parsing',all(str(d.date())==str(pd.Period(p,freq='Q').end_time.date()) for d,p in zip(fact.period_end,fact.TIME_PERIOD)))
    check('Five reporting areas only',set(fact.REF_AREA)=={'DE','FR','IE','LU','U2'})
    names={'DE':'Germany','FR':'France','IE':'Ireland','LU':'Luxembourg','U2':'Euro area (changing composition)'}
    check('Geography labels',all(names[a]==b for a,b in zip(fact.REF_AREA,fact.reporting_area)))
    check('Stock/flow classification',all(t==('stock' if c=='1' else 'flow') for c,t in zip(fact.DATA_TYPE,fact.measure_type)))
    check('No CSSF observations mixed into ECB',set(fact.source_authority)=={'ECB'} and not fact.source_file.str.endswith('.xlsx').any())
    values={(r['REF_AREA'],r['TIME_PERIOD'],r['IVF_ITEM'],r['DATA_TYPE']):None if r['OBS_VALUE']=='' else Decimal(r['OBS_VALUE']) for r in raw}
    def get(a,p,item,typ): return values.get((a,p,item,typ))
    def lag(p,n):
        y,q=map(int,re.fullmatch(r'(\d{4})-Q([1-4])',p).groups()); ix=y*4+q-1-n
        return f'{ix//4}-Q{ix%4+1}'
    def ratio(x,y,minus=False):
        return None if x is None or y is None or y<=0 else (x/y-(1 if minus else 0))*100
    def diff(a,b): return None if a is None or b is None else a-b
    metric_ok={n:True for n in ['assets','shares','gross_issues','redemptions','transactions','qoq_growth_pct','yoy_growth_pct','net_issuance','net_issuance_rate_pct','share_of_euro_area_pct','issuance_transaction_difference','shares_nontransaction_residual','asset_change']}
    for r in mart.to_dict('records'):
        a,p=r['REF_AREA'],r['TIME_PERIOD']; asset=get(a,p,'T00','1'); shares=get(a,p,'L30','1'); issue=get(a,p,'L30','2'); redeem=get(a,p,'L30','3'); tx=get(a,p,'L30','4'); net=diff(issue,redeem)
        expected={'assets':asset,'shares':shares,'gross_issues':issue,'redemptions':redeem,'transactions':tx,
          'qoq_growth_pct':ratio(asset,get(a,lag(p,1),'T00','1'),True),'yoy_growth_pct':ratio(asset,get(a,lag(p,4),'T00','1'),True),
          'net_issuance':net,'net_issuance_rate_pct':ratio(net,get(a,lag(p,1),'L30','1')),
          'share_of_euro_area_pct':ratio(asset,get('U2',p,'T00','1')),'issuance_transaction_difference':diff(net,tx),
          'shares_nontransaction_residual':diff(diff(shares,get(a,lag(p,1),'L30','1')),tx),'asset_change':diff(asset,get(a,lag(p,1),'T00','1'))}
        for n,v in expected.items(): metric_ok[n] &= close(r[n],v)
    for n,ok in metric_ok.items(): check('Independent full-source KPI '+n,ok)
    check('First quarter growth unavailable',mart[mart.TIME_PERIOD==mart.TIME_PERIOD.min()].qoq_growth_pct.isna().all())
    check('First four quarters annual growth unavailable',mart[mart.TIME_PERIOD.isin(sorted(mart.TIME_PERIOD.unique())[:4])].yoy_growth_pct.isna().all())
    check('Euro area denominator is source aggregate',all(close(x,100) for x in mart[mart.REF_AREA=='U2'].share_of_euro_area_pct))
    # Missing-quarter fixture verifies exact calendar-key expectations independently.
    check('Missing-quarter lookup fixture',lag('2024-Q1',1)=='2023-Q4' and ratio(Decimal(5),None) is None and ratio(Decimal(5),Decimal(0)) is None)
    check('Missing numeric observations preserved',int(fact.observation_value.isna().sum())==sum(r['OBS_VALUE']=='' for r in raw))
    w=openpyxl.load_workbook(root/'data/raw'/manifest[2]['file'],read_only=False,data_only=True)
    h=pd.read_parquet(run/'analytical/fact_cssf_monthly.parquet'); s=w.worksheets[0]; detail=w.worksheets[1]
    check('CSSF history cardinality',len(h)==sum(isinstance(row[0],__import__('datetime').datetime) for row in list(s.values)[5:] ))
    check('CSSF month grain',not h.month.duplicated().any())
    cols=['uci_count','gross_issues','redemptions','net_issuance','market_variation','net_assets','monthly_change']
    check('CSSF raw numeric reconciliation',all(close(row[col],s.cell(int(row['source_row']),j+2).value) for row in h.to_dict('records') for j,col in enumerate(cols)))
    check('CSSF issuance arithmetic',all(close(r.net_issuance,r.gross_issues-r.redemptions) for r in h.itertuples()))
    check('CSSF stock movement',all(close(h.iloc[i].monthly_change,h.iloc[i].net_assets-h.iloc[i-1].net_assets) for i in range(1,len(h))))
    check('CSSF movement components',all(close(r.monthly_change,r.net_issuance+r.market_variation) for r in h.iloc[1:].itertuples()))
    check('CSSF initial missing changes preserved',pd.isna(h.iloc[0].market_variation) and pd.isna(h.iloc[0].monthly_change))
    leaf=pd.read_parquet(run/'analytical/fact_cssf_structure.parquet')
    check('CSSF structural leaf grain',len(leaf)==32 and not leaf.duplicated(['month','legal_status','legal_form','measure']).any())
    check('CSSF totals excluded from leaf fact',not leaf.legal_status.eq('Total').any() and not leaf.legal_form.eq('Total').any())
    check('CSSF structural raw reconciliation',all(close(r.value,detail[r.source_cell].value) for r in leaf.itertuples()))
    check('CSSF structural counts tie to history',close(leaf[leaf.measure=='uci_count'].value.sum(),h.iloc[-1].uci_count))
    check('CSSF structural net assets tie to history',close(leaf[leaf.measure=='net_assets'].value.sum(),h.iloc[-1].net_assets))
    check('CSSF row/column count margins',all(close(sum(detail.cell(r,c).value for c in range(2,6)),detail.cell(r,6).value) for r in range(8,12)) and all(close(sum(detail.cell(r,c).value for r in range(8,12)),detail.cell(12,c).value) for c in range(2,6)))
    check('CSSF row/column asset margins',all(close(sum(detail.cell(r,c).value for c in range(2,6)),detail.cell(r,6).value) for r in range(18,22)) and all(close(sum(detail.cell(r,c).value for r in range(18,22)),detail.cell(22,c).value) for c in range(2,6)))
    check('CSSF umbrella count identity',detail['B28'].value+detail['C28'].value==detail['A28'].value)
    check('CSSF compartment/unit identity',detail['C28'].value+detail['D28'].value==detail['E28'].value)
    cells=pd.read_parquet(run/'staging/cssf_source_cells.parquet')
    check('CSSF lossless nonblank cell count',len(cells)==sum(c.value is not None for sheet in w for row in sheet for c in row))
    return {'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks}

if __name__=='__main__':
    from pathlib import Path
    import sys
    root=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(root/'.runtime'))
    pointer=json.loads((root/'data/latest_validated.json').read_text())
    result=validate(root,root/pointer['relative_path']); print(json.dumps(result,indent=2))
    sys.exit(bool(result['failed']))
