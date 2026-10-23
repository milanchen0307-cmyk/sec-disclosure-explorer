"""Build a bounded filing/price explorer from the original headerless database exports."""
from pathlib import Path
import argparse,json,csv
import numpy as np,pandas as pd
def event_window(prices,date,before=5,after=10):
    p=prices.sort_values('date').drop_duplicates('date');idx=p['date'].searchsorted(pd.Timestamp(date))
    if idx==0 or idx>=len(p):return None
    # Do not treat an unrelated far-future quote as the event date.
    if (p.iloc[idx]['date']-pd.Timestamp(date)).days>7:return None
    base=float(p.iloc[idx-1]['adj_close'])
    if not np.isfinite(base) or base<=0:return None
    sub=p.iloc[max(0,idx-before):min(len(p),idx+after+1)]
    return [dict(day=int(i-idx),date=r.date.strftime('%Y-%m-%d'),return_pct=float((r.adj_close/base-1)*100)) for i,r in sub.iterrows()]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--max-filings',type=int,default=600);args=ap.parse_args();src=Path(args.source)
    company=pd.read_csv(src/'company.csv',header=None,names=['company_id','cik','ticker','name','sic','industry'],dtype={'cik':str})
    prices=pd.read_csv(src/'daily_price.csv',header=None,names=['company_id','date','open','high','low','close','adj_close','volume'],parse_dates=['date'])
    lookup=company.set_index('company_id').to_dict('index');pricegroups={i:g.sort_values('date').reset_index(drop=True) for i,g in prices.groupby('company_id')}
    csv.field_size_limit(100_000_000);events=[];seen=set();scanned=0
    with (src/'sec_filings.csv').open(encoding='utf-8',newline='') as fh:
        for row in csv.reader(fh):
            scanned+=1
            if scanned>args.max_filings:break
            if len(row)<12:continue
            try:cid=int(row[3])
            except ValueError:continue
            if cid not in pricegroups or cid not in lookup:continue
            if row[1] in seen:continue
            c=lookup[cid];window=event_window(pricegroups[cid],row[5])
            if not window:continue
            seen.add(row[1]);events.append(dict(ticker=c['ticker'],company=c['name'],form=row[6],filing_date=row[5],accession=row[1],url=row[9],document_url=row[10],window=window))
            if len(events)>=75:break
    root=Path(__file__).resolve().parents[1];out=root/'reports';out.mkdir(exist_ok=True)
    result=dict(events=events,scanned=scanned,companies=len({e['ticker'] for e in events}),method='Adjusted-close cumulative return, normalized to the trading day before the filing date. Day 0 is the first trading date on/after filing. Filing time is not available; after-hours filings may react on the following session.',limitations='Bounded convenience sample from historical exports, not a representative market study. These are raw price reactions, NOT benchmark-adjusted abnormal returns or causal effects. Other news and stale data can confound interpretation. No filing full text is republished.')
    (out/'events.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    print('Exported',len(events),'events across',result['companies'],'companies')
if __name__=='__main__':main()
