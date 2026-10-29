"""Build editable Power BI project definitions using validated local CSVs."""
from pathlib import Path
import json, copy, uuid
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/power_bi'; NAME='Luxembourg_Fund_Intelligence'
REPORT=OUT/(NAME+'.Report'); MODEL=OUT/(NAME+'.SemanticModel')
def put(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False) if not isinstance(o,str) else o,encoding='utf-8')
def lit(x): return {'expr':{'Literal':{'Value':x}}}
def color(x): return {'solid':{'color':lit("'"+x+"'")}}
def field(table,name,kind='Measure'): return {kind:{'Expression':{'SourceRef':{'Entity':table}},'Property':name}}
def projection(table,name,kind='Measure',label=None):
    p={'field':field(table,name,kind),'queryRef':table+'.'+name,'nativeQueryRef':label or name,'displayName':label or name}
    if kind=='Column': p['active']=True
    return p
def base(template,name,x,y,w,h):
    d=json.loads((ROOT/'src/report_templates'/f'{template}.json').read_text(encoding='utf-8'))
    d['name']=name; d['position']={'x':x,'y':y,'width':w,'height':h,'z':y*10+x,'tabOrder':y*10+x}
    return d
def text(name,value,x,y,w,h,size=15,bg='#F3F6FA',fg='#17365D'):
    d=base('text',name,x,y,w,h)
    d['visual']['objects']['general'][0]['properties']['paragraphs']=[{'textRuns':[{'value':line,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'pt','color':fg,'fontWeight':'bold' if size>20 else 'normal'}}]} for line in value.split('\n')]
    d['visual']['visualContainerObjects']['background'][0]['properties']['color']=color(bg)
    return d
def card(name,table,measure,label,x,y,w=376):
    d=base('card',name,x,y,w,112); d['visual']['query']['queryState']={'Data':{'projections':[projection(table,measure+' display' if measure!='Latest quarter' else measure,label=label)]}}
    return d
def chart(name,table,category,measures,title,x,y,w,h,kind='lineChart'):
    d=base('chart',name,x,y,w,h); v=d['visual'];v['visualType']=kind
    v['query']['queryState']={'Category':{'projections':[projection(table,category,'Column')]},'Y':{'projections':[projection(table,m,label={'LU issues history':'Gross issues','LU redemptions history':'Redemptions'}.get(m,m)) for m in measures]}}
    v['query']['sortDefinition']={'sort':[{'field':field(table,category,'Column'),'direction':'Ascending'}],'isDefaultSort':True}
    v['visualContainerObjects']['title'][0]['properties']['text']=lit("'"+title+"'")
    v['visualContainerObjects']['subTitle']=[{'properties':{'show':lit('false')}}]
    if len(measures)>1: v['objects'].pop('dataPoint',None)
    v['objects']['labels'][0]['properties']['show']=lit('true' if kind=='clusteredBarChart' else 'false')
    v['objects']['legend'][0]['properties']['show']=lit('true' if len(measures)>1 else 'false')
    return d
def slicer(name,table,col,title,x,y,w):
    d=base('slicer',name,x,y,w,80);d['visual']['query']['queryState']={'Values':{'projections':[projection(table,col,'Column')]}}
    d['visual']['visualContainerObjects']['title'][0]['properties']['text']=lit("'"+title+"'")
    return d
def page(name,title,visuals,subtitle):
    p=REPORT/'definition/pages'/name
    put(p/'page.json',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json','name':name,'displayName':title,'displayOption':'FitToPage','width':1600,'height':900,'objects':{'background':[{'properties':{'color':color('#F3F6FA'),'transparency':lit('0D')}}]}})
    visuals=[text('header','QUANTRISK  /  INVESTMENT FUNDS\n'+title,24,16,1552,92,23,'#17365D','#FFFFFF'),text('subtitle',subtitle,24,116,1552,44,14)]+visuals
    for v in visuals: put(p/'visuals'/v['name']/'visual.json',v)
def table(name,filename,cols,measures):
    lines=[f'table {name}',f'\tlineageTag: {uuid.uuid4()}','']
    measures = measures + [(m+' display', f'IF(ISBLANK([{m}]), BLANK(), FORMAT([{m}], "{fmt}"))', 'General') for m,expr,fmt in measures if m.startswith('LU ') and 'history' not in m or name=='CSSF']
    for m,expr,fmt in measures:
        expr = expr.replace("Structure[", "'Structure'[")
        lines += [f"\tmeasure '{m}' = {expr}",f'\t\tformatString: {fmt}', '']
    for c,t in cols:
        lines += [f'\tcolumn {c}',f'\t\tdataType: {t}','\t\tsummarizeBy: none',f'\t\tsourceColumn: {c}','']
    types=', '.join('{"'+c+'", '+('type text' if t=='string' else 'type number')+'}' for c,t in cols)
    lines += [f'\tpartition {name} = m','\t\tmode: import','\t\tsource =','\t\t\tlet',f'\t\t\t    Source = Csv.Document(File.Contents(DataFolder & "\\{filename}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),','\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',f'\t\t\t    Typed = Table.TransformColumnTypes(Headers, {{{types}}}, "en-US")','\t\t\tin Typed','']
    put(MODEL/'definition/tables'/f'{name}.tmdl','\n'.join(lines))
def main():
    pointer=json.loads((ROOT/'data/latest_validated.json').read_text()); data=(ROOT/pointer['relative_path']/'analytical').resolve()
    put(OUT/(NAME+'.pbip'),{'version':'1.0','artifacts':[{'report':{'path':NAME+'.Report'}}],'settings':{'enableAutoRecovery':True}})
    put(REPORT/'definition.pbir',{'version':'4.0','datasetReference':{'byPath':{'path':'../'+NAME+'.SemanticModel'}}})
    put(REPORT/'definition/version.json',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
    put(REPORT/'definition/report.json',json.loads((ROOT/'src/report_templates/report.json').read_text(encoding='utf-8')))
    import shutil
    shutil.copytree(ROOT/'src/report_templates/SharedResources',REPORT/'StaticResources/SharedResources',dirs_exist_ok=True)
    put(REPORT/'definition/pages/pages.json',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':['overview','flows','benchmark','structure'],'activePageName':'overview'})
    put(MODEL/'definition.pbism',{'version':'4.2','settings':{}})
    put(MODEL/'definition/database.tmdl','database\n\tcompatibilityLevel: 1606\n')
    put(MODEL/'definition/model.tmdl','model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\nannotation __PBI_TimeIntelligenceEnabled = 0\n\nref table ECB\nref table CSSF\nref table Structure\n')
    put(MODEL/'definition/expressions.tmdl',f'expression DataFolder = "{data}"\n\tkind: m\n')
    numeric=['assets','shares','gross_issues','redemptions','net_issuance','transactions','qoq_growth_pct','yoy_growth_pct','share_of_euro_area_pct','net_issuance_rate_pct','issuance_transaction_difference']
    measures=[]
    # SELECTEDVALUE prevents accidental sums across countries or quarters. Cards explicitly use latest selected period.
    for col,label,div,fmt in [('assets','Assets EUR bn',1000,'#,0.0'),('shares','Shares EUR bn',1000,'#,0.0'),('gross_issues','Issues EUR bn',1000,'#,0.0'),('redemptions','Redemptions EUR bn',1000,'#,0.0'),('net_issuance','Net issuance EUR bn',1000,'#,0.0'),('transactions','Transactions EUR bn',1000,'#,0.0'),('qoq_growth_pct','QoQ growth',100,'0.00%'),('yoy_growth_pct','YoY growth',100,'0.00%'),('share_of_euro_area_pct','Euro area share',100,'0.00%'),('net_issuance_rate_pct','Issuance rate',100,'0.00%')]:
        measures.append((label,f'DIVIDE(SELECTEDVALUE(ECB[{col}]), {div})',fmt))
        measures.append(('LU '+label,f'VAR p = MAX(ECB[TIME_PERIOD]) RETURN CALCULATE([{label}], ECB[REF_AREA] = "LU", ECB[TIME_PERIOD] = p)',fmt))
    measures += [('Latest quarter','MAX(ECB[TIME_PERIOD])','General'),('LU asset history','CALCULATE([Assets EUR bn], ECB[REF_AREA] = "LU")','#,0.0'),('LU net history','CALCULATE([Net issuance EUR bn], ECB[REF_AREA] = "LU")','#,0.0'),('LU issues history','CALCULATE([Issues EUR bn], ECB[REF_AREA] = "LU")','#,0.0'),('LU redemptions history','CALCULATE([Redemptions EUR bn], ECB[REF_AREA] = "LU")','#,0.0')]
    for metric in ['Assets EUR bn','YoY growth','Euro area share']:
        measures.append(('Latest '+metric,f'VAR p = MAX(ECB[TIME_PERIOD]) RETURN CALCULATE([{metric}], ECB[TIME_PERIOD] = p)','#,0.0' if metric=='Assets EUR bn' else '0.00%'))
    table('ECB','mart_ecb_quarterly.csv',[(x,'string') for x in ['REF_AREA','TIME_PERIOD','area']]+[(x,'double') for x in numeric],measures)
    table('CSSF','fact_cssf_monthly.csv',[('month','string')]+[(x,'double') for x in ['uci_count','net_assets','net_issuance']], [('UCI count','VAR p = MAX(CSSF[month]) RETURN CALCULATE(SELECTEDVALUE(CSSF[uci_count]), CSSF[month] = p)','#,0'),('Net assets EUR bn','VAR p = MAX(CSSF[month]) RETURN CALCULATE(SELECTEDVALUE(CSSF[net_assets]), CSSF[month] = p)','#,0.0'),('Net inflow EUR bn','VAR p = MAX(CSSF[month]) RETURN CALCULATE(SELECTEDVALUE(CSSF[net_issuance]), CSSF[month] = p)','#,0.0')])
    table('Structure','fact_cssf_structure.csv',[(x,'string') for x in ['month','legal_status','legal_form','measure']]+[('value','double')],[('Structure assets EUR bn','CALCULATE(SUM(Structure[value]), Structure[measure] = "net_assets")','#,0.0'),('Structure UCI count','CALCULATE(SUM(Structure[value]), Structure[measure] = "uci_count")','#,0')])
    page('overview','Executive fund industry overview',[
       slicer('period','ECB','TIME_PERIOD','Quarter selection (cards use latest selected)',24,166,500),card('periodcard','ECB','Latest quarter','Latest selected quarter',1200,166,376),
       *[card('k'+str(i),'ECB',m,l,24+i*392,267) for i,(m,l) in enumerate([('LU Assets EUR bn','Luxembourg assets | EUR bn'),('LU QoQ growth','Quarterly asset growth'),('LU YoY growth','Annual asset growth'),('LU Euro area share','Share of euro-area assets')])],
       chart('history','ECB','TIME_PERIOD',['LU asset history'],'Luxembourg fund assets | EUR billion',24,395,1000,365),
       text('findings','READING THE OVERVIEW\nQuarter-end assets describe industry size.\nGrowth also reflects valuation and other changes.\nEuro-area share uses the reported U2 aggregate.\nAsset growth is not an investment return.',1040,395,536,365,18,'#FFFFFF'),
       text('footer','Source: supplied ECB IVF files | Non-MMF investment funds | 2018 Q1–2026 Q2 | Missing comparisons display blank',24,795,1552,68,14)],'Luxembourg • ECB investment-fund population • validated local source vintage')
    page('flows','Fund shares and capital flows',[
       slicer('period','ECB','TIME_PERIOD','Quarter selection (cards use latest selected)',24,166,500),card('periodcard','ECB','Latest quarter','Latest selected quarter',1200,166,376),
       *[card('k'+str(i),'ECB',m,l,24+i*392,267) for i,(m,l) in enumerate([('LU Shares EUR bn','Shares outstanding | EUR bn'),('LU Issues EUR bn','Gross issues | EUR bn'),('LU Redemptions EUR bn','Redemptions | EUR bn'),('LU Net issuance EUR bn','Net issuance | EUR bn')])],
       chart('gross','ECB','TIME_PERIOD',['LU issues history','LU redemptions history'],'Issues and redemptions | EUR billion',24,395,760,285),
       chart('net','ECB','TIME_PERIOD',['LU net history'],'Net issuance; sign changes show reversals | EUR bn',800,395,776,285,'clusteredColumnChart'),
       card('tx','ECB','LU Transactions EUR bn','Reported transactions | EUR bn',24,700),card('rate','ECB','LU Issuance rate','Net issuance / prior shares',416,700),
       text('note','Transactions include income-related components and can differ from net issuance.\nThe difference is retained for review. Flows are not investment performance.',824,700,752,140,16)],'Luxembourg • quarterly flows and quarter-end stocks • amounts in EUR billion')
    page('benchmark','European benchmarking',[
       slicer('period','ECB','TIME_PERIOD','Quarter selection (latest selected)',24,166,500),card('periodcard','ECB','Latest quarter','Comparison quarter',1200,166,376),
       chart('assets','ECB','area',['Latest Assets EUR bn'],'Latest selected assets | EUR billion',24,280,760,440,'clusteredBarChart'),
       chart('growth','ECB','area',['Latest YoY growth'],'Latest selected annual asset growth',800,280,776,440,'clusteredBarChart'),
       text('note','U2 is the euro-area aggregate with changing composition. Never add it to the four countries.\nCommon definitions, currency and quarter support comparison; growth is not investment performance.',24,760,1552,100,18)],'Luxembourg • Ireland • Germany • France • euro area shown separately as a benchmark')
    page('structure','Luxembourg fund industry structure',[
       *[card('k'+str(i),'CSSF',m,l,24+i*520,180,504) for i,(m,l) in enumerate([('UCI count','Supervised UCIs | count'),('Net assets EUR bn','Net assets | EUR bn'),('Net inflow EUR bn','August net issuance | EUR bn')])],
       chart('status','Structure','legal_status',['Structure assets EUR bn'],'Net assets by legal status | EUR billion',24,330,760,380,'clusteredBarChart'),
       chart('forms','Structure','legal_form',['Structure UCI count'],'UCI count by legal form',800,330,776,380,'clusteredBarChart'),
       text('note','Separate CSSF population: Part I, Part II, FIS and SICAR categories supplied in the workbook.\nNet assets are not ECB total assets. Structural charts may cross-filter each other; headline cards show the complete CSSF population.',24,750,1552,110,17)],'CSSF supervised UCI statistics • August 2026 • source workbook legal-status and legal-form breakdowns')
    print(OUT/(NAME+'.pbip'))
if __name__=='__main__':main()
