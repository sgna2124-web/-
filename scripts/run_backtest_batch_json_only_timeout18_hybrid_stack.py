from __future__ import annotations
import copy,json,os
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'experiments'/'base_config_json_only_timeout18_hybrid_stack.json'
COMB=ROOT/'experiments'/'combinations_json_only_timeout18_hybrid_stack.json'

def lj(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def dm(a,b):
    x=copy.deepcopy(a)
    for k,v in b.items(): x[k]=dm(x[k],v) if isinstance(v,dict) and isinstance(x.get(k),dict) else copy.deepcopy(v)
    return x

def exps(base,group):
    return [{'name':e['name'],'effective_config':dm(base,e.get('overrides',{}))} for e in group.get('experiments',[]) if e.get('enabled',False)]

def ema(a,p): return pd.Series(a).ewm(span=p,adjust=False).mean().to_numpy(float)
def rsi(a,p):
    s=pd.Series(a,dtype=float); d=s.diff(); up=d.clip(lower=0); dn=-d.clip(upper=0)
    ru=up.ewm(alpha=1/p,adjust=False).mean(); rd=dn.ewm(alpha=1/p,adjust=False).mean(); rs=ru/rd.replace(0,np.nan)
    return (100-(100/(1+rs))).fillna(50).to_numpy(float)
def atr(h,l,c,p):
    pc=np.roll(c,1); pc[0]=c[0]; tr=np.maximum(h-l,np.maximum(np.abs(h-pc),np.abs(l-pc)))
    return pd.Series(tr).ewm(alpha=1/p,adjust=False).mean().to_numpy(float)
def feats(o,h,l,c):
    body=np.abs(c-o); return {'body':body,'upper_wick':h-np.maximum(o,c),'lower_wick':np.minimum(o,c)-l}

def load_df(path):
    first=Path(path).read_text(encoding='utf-8',errors='ignore').splitlines()[0].strip()
    if first.startswith('version https://git-lfs.github.com/spec/'): raise ValueError('LFS pointer')
    raw=pd.read_csv(path); raw.columns=[str(c).strip().replace('\ufeff','').lower() for c in raw.columns]
    mp={}
    alias={'date':['date','datetime','timestamp','time','open_time','opentime','candle_date_time_utc','candle_date_time_kst'],'open':['open','open_price','opening_price','시가'],'high':['high','high_price','고가'],'low':['low','low_price','저가'],'close':['close','close_price','closing_price','trade_price','종가'],'volume':['volume','vol','base_volume','candle_acc_trade_volume','acc_trade_volume','거래량']}
    for t,ks in alias.items():
        for k in ks:
            if k.lower() in raw.columns: mp[k.lower()]=t; break
    df=raw.rename(columns=mp)[['date','open','high','low','close','volume']].copy(); df['date']=pd.to_datetime(df['date'],errors='coerce')
    for c in ['open','high','low','close','volume']: df[c]=pd.to_numeric(df[c],errors='coerce')
    return df.dropna().sort_values('date').drop_duplicates('date').reset_index(drop=True)

def tret(entry,exitp,side,fee): return ((exitp/entry-1.0) if side==1 else (entry/exitp-1.0))-(2*fee)

def evalt(trades,pf):
    trades=sorted(trades,key=lambda x:x[0]); eq=peak=peak_asset=1.0; mdd=0.0; wins=0; gp=gl=0.0
    for _,_,r in trades:
        eq*=1+pf*r; peak_asset=max(peak_asset,eq); peak=max(peak,eq); mdd=min(mdd,eq/peak-1.0)
        if r>0: wins+=1; gp+=r
        else: gl+=-r
    if trades:
        ent=np.array([x[0] for x in trades],dtype=np.int64); exi=np.array([x[1] for x in trades],dtype=np.int64)
        times=np.concatenate([ent,exi]); delta=np.concatenate([np.ones_like(ent),-np.ones_like(exi)]); order=np.lexsort((1-delta,times)); cur=mx=0
        for d in delta[order]: cur+=int(d); mx=max(mx,cur)
    else: mx=0
    return {'trades':len(trades),'final_asset':float(eq),'final_return':float(eq-1.0),'peak_asset':float(peak_asset),'peak_growth':float(peak_asset-1.0),'win_rate':float(wins/len(trades)) if trades else 0.0,'pf':float(gp/gl) if gl>0 else float('inf'),'mdd':float(mdd),'max_conc':int(mx)}

def run_symbol(df,cfg):
    s,q,r,e,t,x=cfg['signal'],cfg.get('quality',{}),cfg['risk'],cfg.get('exit_refine',{}),cfg['trade_control'],cfg['execution']; fee=float(cfg['fee_per_side'])
    o,h,l,c=df['open'].to_numpy(float),df['high'].to_numpy(float),df['low'].to_numpy(float),df['close'].to_numpy(float); ts=pd.to_datetime(df['date']).astype('int64').to_numpy()
    ema_v,rsi_v,atr_v=ema(c,int(s['ema_period'])),rsi(c,int(s['rsi_period'])),atr(h,l,c,int(s['atr_period'])); f=feats(o,h,l,c)
    ld=float(q.get('long_dev') if q.get('long_dev') is not None else s['long_dev']); lr=float(q.get('long_rsi_max') if q.get('long_rsi_max') is not None else s['long_rsi_max']); lw=float(q.get('long_wick_mult') if q.get('long_wick_mult') is not None else s['long_wick_mult'])
    sd=float(q.get('short_dev') if q.get('short_dev') is not None else s['short_dev']); sr=float(q.get('short_rsi_min') if q.get('short_rsi_min') is not None else s['short_rsi_min']); sw=float(q.get('short_wick_mult') if q.get('short_wick_mult') is not None else s['short_wick_mult'])
    asm=float(r['atr_stop_mult']); rrm=float(r['rr_mult']); met=float(r['min_expected_tp']); timeout=int(r['timeout_bars']); ff_b=e.get('fail_fast_bars'); ff_r=e.get('fail_fast_min_progress_r'); cd=int(t['cooldown_bars_same_symbol_same_side'])
    trades=[]; inpos=False; last={1:-10_000_000,-1:-10_000_000}; start=max(int(s['ema_period']),int(s['rsi_period']),int(s['atr_period']),30); mfe=0.0; riskv=0.0
    for i in range(start,len(c)-1):
        if not inpos:
            ls=bool(x['allow_long']) and (i-last[1]>cd) and ((c[i]/ema_v[i])-1.0)<=-ld and rsi_v[i]<lr and f['lower_wick'][i]>=lw*f['body'][i]
            ss=bool(x['allow_short']) and (i-last[-1]>cd) and ((c[i]/ema_v[i])-1.0)>=sd and rsi_v[i]>sr and f['upper_wick'][i]>=sw*f['body'][i]
            if ls:
                entry=o[i+1]; stop=min(l[i],entry-atr_v[i]*asm); ema_t=ema_v[i]; rr_t=entry+rrm*(entry-stop); target=min(ema_t,rr_t) if ema_t>entry else rr_t
                if entry>stop and (target-entry)/entry>=met: inpos=True; side=1; ei=i+1; ep=float(entry); sp=float(stop); tp=float(target); mfe=0.0; riskv=max(ep-sp,1e-12)
            elif ss:
                entry=o[i+1]; stop=max(h[i],entry+atr_v[i]*asm); ema_t=ema_v[i]; rr_t=entry-rrm*(stop-entry); target=max(ema_t,rr_t) if ema_t<entry else rr_t
                if stop>entry and (entry-target)/entry>=met: inpos=True; side=-1; ei=i+1; ep=float(entry); sp=float(stop); tp=float(target); mfe=0.0; riskv=max(sp-ep,1e-12)
        else:
            prev=max(ei,i-1)
            if side==1:
                mfe=max(mfe,(h[prev]-ep)/riskv)
                exit_p=sp if l[i]<=sp else tp if h[i]>=tp else c[i] if (ff_b is not None and (i-ei)>=int(ff_b) and mfe<float(ff_r or 0.0) and c[i]<ep) or (i-ei)>=timeout else None
            else:
                mfe=max(mfe,(ep-l[prev])/riskv)
                exit_p=sp if h[i]>=sp else tp if l[i]<=tp else c[i] if (ff_b is not None and (i-ei)>=int(ff_b) and mfe<float(ff_r or 0.0) and c[i]>ep) or (i-ei)>=timeout else None
            if exit_p is not None:
                trades.append((int(ts[ei]),int(ts[i]),float(tret(ep,float(exit_p),side,fee)),'long' if side==1 else 'short')); last[side]=i; inpos=False
    return trades

def run_one(exp):
    cfg=exp['effective_config']; name=exp['name']; data_dir=Path(os.environ.get('DATA_DIR',str(ROOT/cfg['data_dir']))); out_dir=ROOT/cfg['results_dir']/name; out_dir.mkdir(parents=True,exist_ok=True)
    all_t=[]; rows=[]; by=[]
    for p in sorted(data_dir.glob('*.csv')):
        df=load_df(p)
        if len(df)<int(cfg['min_bars']): continue
        st=run_symbol(df,cfg); all_t.extend((a,b,c) for a,b,c,_ in st)
        wins=sum(1 for _,_,r,_ in st if r>0); losses=sum(1 for _,_,r,_ in st if r<=0); gp=sum(r for _,_,r,_ in st if r>0); gl=-sum(r for _,_,r,_ in st if r<=0)
        by.append({'symbol':p.stem,'bars':len(df),'trades':len(st),'wins':wins,'losses':losses,'win_rate':(wins/len(st)) if st else 0.0,'pf':(gp/gl) if gl>0 else None,'sum_r':sum(r for _,_,r,_ in st)})
        for a,b,c,side in st: rows.append({'symbol':p.stem,'entry_ts':a,'exit_ts':b,'ret':c,'side':side})
    s=evalt(all_t,float(cfg['position_fraction'])); s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'symbols':len(by),'effective_config':cfg})
    pd.DataFrame(rows).to_csv(out_dir/'trades.csv',index=False); pd.DataFrame(by).to_csv(out_dir/'by_symbol.csv',index=False); Path(out_dir/'summary.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(s,ensure_ascii=False,indent=2)); return s

if __name__=='__main__':
    base,group=lj(BASE),lj(COMB); out=[]
    for exp in exps(base,group):
        print(f"running experiment: {exp['name']}"); s=run_one(exp); out.append({'experiment':exp['name'],'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc']})
    d=ROOT/'results_json_only_timeout18_hybrid_stack'; d.mkdir(parents=True,exist_ok=True); pd.DataFrame(out).to_csv(d/'single_changes_quick_summary.csv',index=False)
