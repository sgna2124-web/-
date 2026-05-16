# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse,json,math,time
from pathlib import Path
from typing import Any,Dict,List,Optional,Tuple
import numpy as np
import pandas as pd

NAME='8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18'
ENTRY_KEY='child::orig_V09_extreme_vol18::tp03'
ATR_STOP=1.12; RR_TARGET=4.70; MAX_HOLD=18; COOLDOWN=31
WARMUP=120; MIN_BARS=250; TRAIN_END='2026-01-01 00:00:00'; POS=0.01; FEE_BPS=8.0
EXPECTED=dict(strategy=NAME,trades=56697,wins=20962,losses=35735,win_rate_pct=36.97197382577562,final_return_pct=405.1480528315248,max_return_pct=405.8734002703171,max_drawdown_pct=1.228290350505734,official_cd_value=499.6598061090216,cd_value=499.6598061090216,max_conc=444,symbol_files=597,errors=0,ruined=False)

def norm(x):
    s=str(x).strip().upper()
    for ch in ['-','_','/',':',' ','.']: s=s.replace(ch,'')
    return s

def infer_symbol(p:Path):
    s=p.stem.upper().replace('-','_'); parts=s.split('_')
    if len(parts)>=2 and parts[-1] in {'1M','3M','5M','15M','30M','1H','2H','4H','1D'}: s='_'.join(parts[:-1])
    s=s.replace('_PERP','').replace('PERP','')
    if '/USDT' not in s and 'USDT' in s: s=s.replace('USDT','/USDT')
    elif '/BUSD' not in s and 'BUSD' in s: s=s.replace('BUSD','/BUSD')
    elif '/USD' not in s and s.endswith('USD'): s=s[:-3]+'/USD'
    return s

def bases():
    out=[]; seen=set()
    for b in [Path.cwd().resolve(),Path(__file__).resolve().parent]:
        for p in [b,*b.parents]:
            k=str(p).lower()
            if k not in seen: seen.add(k); out.append(p)
    return out

def find_data_root(x=None):
    if x:
        p=Path(x).expanduser().resolve()
        if not p.exists(): raise FileNotFoundError(p)
        return p
    cand=[]
    for b in bases(): cand += [b/'Data'/'time',b/'코인'/'Data'/'time',b/'data'/'time',b/'coin'/'Data'/'time']
    for p in cand:
        if p.exists() and any(p.rglob('*.csv')): return p
    raise FileNotFoundError('Data/time 폴더를 찾지 못했다. --data-root 로 지정')

def find_symbol_cost(x=None):
    if x:
        p=Path(x).expanduser().resolve()
        if not p.exists(): raise FileNotFoundError(p)
        return p
    for b in bases():
        for p in [b/'symbol_cost',b/'코인'/'symbol_cost',b/'symbol_cost.csv',b/'코인'/'symbol_cost.csv',b/'symbols.csv']:
            if p.exists(): return p
    return None

def build_map(root):
    m={}
    for p in sorted(root.rglob('*.csv')):
        m.setdefault(norm(p.stem),p); m.setdefault(norm(infer_symbol(p)),p)
    if not m: raise FileNotFoundError(root)
    return m

def read_symbols(path,m):
    sy=[]
    if path:
        files=[path] if path.is_file() else sum([sorted(path.rglob(g)) for g in ['*.csv','*.json','*.txt']],[])
        if files:
            f=files[0]
            if f.suffix.lower()=='.json':
                d=json.loads(f.read_text(encoding='utf-8')); d=d.get('symbols',list(d.values())) if isinstance(d,dict) else d
                sy=[str(x.get('symbol') or x.get('ticker') or x.get('name')) if isinstance(x,dict) else str(x) for x in d if x]
            else:
                try:
                    df=pd.read_csv(f); cols=[c for c in df.columns if str(c).lower() in {'symbol','ticker','name','market'}]
                    sy=(df[cols[0]] if cols else df.iloc[:,0]).dropna().astype(str).tolist()
                except Exception: sy=[z.strip() for z in f.read_text(encoding='utf-8').splitlines() if z.strip()]
    got=[]
    for s in sy:
        p=m.get(norm(s))
        if p: got.append(infer_symbol(p))
    return sorted(set(got)) if got else sorted({infer_symbol(p) for p in m.values()})

def rma(s,n): return s.ewm(alpha=1/max(1,n),adjust=False).mean()
def atr(df,n=14):
    h,l,c=df.high,df.low,df.close; pc=c.shift(1)
    tr=pd.concat([(h-l).abs(),(h-pc).abs(),(l-pc).abs()],axis=1).max(axis=1)
    return rma(tr,n).bfill().fillna(0)
def rsi(c,n=14):
    d=c.diff().fillna(0); up=d.clip(lower=0); dn=(-d).clip(lower=0); rs=rma(up,n)/rma(dn,n).replace(0,np.nan)
    return (100-100/(1+rs)).fillna(50)

def load_csv(p,max_bars,train_end):
    df=pd.read_csv(p); cols={str(c).lower().strip():c for c in df.columns}; mp={}
    for a,b in [('timestamp','timestamp'),('open_time','timestamp'),('opentime','timestamp'),('time','timestamp'),('date','timestamp'),('datetime','timestamp'),('open','open'),('high','high'),('low','low'),('close','close'),('volume','volume'),('vol','volume')]:
        if a in cols: mp[cols[a]]=b
    df=df.rename(columns=mp)[['timestamp','open','high','low','close','volume']].copy()
    if not np.issubdtype(df.timestamp.dtype,np.number):
        ts=pd.to_datetime(df.timestamp,utc=True,errors='coerce'); df.timestamp=(ts.astype('int64')//10**9).astype(float)
    for c in df.columns: df[c]=pd.to_numeric(df[c],errors='coerce')
    df=df.dropna().sort_values('timestamp').drop_duplicates('timestamp').reset_index(drop=True)
    ts=pd.Timestamp(train_end); ts=ts.tz_localize('UTC') if ts.tzinfo is None else ts.tz_convert('UTC'); cut=float(int(ts.timestamp())); med=float(df.timestamp.median())
    if med>1e17: cut*=1_000_000_000
    elif med>1e14: cut*=1_000_000
    elif med>1e11: cut*=1_000
    df=df[df.timestamp<cut].reset_index(drop=True)
    if max_bars and len(df)>max_bars: df=df.tail(max_bars).reset_index(drop=True)
    return df

def features(df):
    c,h,l,o,v=df.close,df.high,df.low,df.open,df.volume; a=atr(df,14); rs=rsi(c,14)
    vr=(v/v.rolling(20,min_periods=1).mean().replace(0,np.nan)).replace([np.inf,-np.inf],np.nan).fillna(0)
    body=(c-o).abs(); cp=((c-l)/(h-l).replace(0,np.nan)).replace([np.inf,-np.inf],np.nan).fillna(.5)
    lw=(pd.concat([o,c],axis=1).min(axis=1)-l); lwbr=(lw/body.replace(0,np.nan)).replace([np.inf,-np.inf],np.nan).fillna(0)
    tr=pd.concat([(h-l).abs(),(h-c.shift(1)).abs(),(l-c.shift(1)).abs()],axis=1).max(axis=1)
    return dict(ts=df.timestamp.astype('int64').to_numpy(),o=o.to_numpy(float),h=h.to_numpy(float),l=l.to_numpy(float),c=c.to_numpy(float),atr=a.to_numpy(float),rsi=rs.to_numpy(float),vr=vr.to_numpy(float),body_atr=(body/a.replace(0,np.nan)).replace([np.inf,-np.inf],np.nan).fillna(0).to_numpy(float),cp=cp.to_numpy(float),lwbr=lwbr.to_numpy(float),ll20=l.rolling(20,min_periods=1).min().to_numpy(float),ret3=c.pct_change(3).fillna(0).to_numpy(float),ret5=c.pct_change(5).fillna(0).to_numpy(float),quiet=(tr.ewm(span=6,adjust=False).mean()/tr.ewm(span=24,adjust=False).mean().replace(0,np.nan)).replace([np.inf,-np.inf],np.nan).fillna(1).to_numpy(float))

def entry_mask(f):
    n=len(f['c']); shock=np.zeros(n,bool); l01=np.zeros(n,bool); extreme=np.zeros(n,bool); balance=np.zeros(n,bool)
    for i in range(max(21,WARMUP),n-1):
        l20=f['ll20'][i-1]
        raw=((f['ret3'][i]<-0.04 or f['ret5'][i]<-0.06) and f['l'][i]<l20 and f['c'][i]>l20 and f['c'][i]>f['o'][i] and f['cp'][i]>.70 and f['vr'][i]>1.40 and f['body_atr'][i]>.35)
        shock[i]=((f['ret3'][i]<=-0.035 or f['ret5'][i]<=-0.050) and f['vr'][i]>=1.10 and f['body_atr'][i]>=0.25)
        l01[i]=raw
        extreme[i]=raw and f['cp'][i]>=.80 and f['lwbr'][i]>=1.50 and f['vr'][i]>=1.60
        balance[i]=((f['ret3'][i]<=-0.025 or f['ret5'][i]<=-0.040) and f['c'][i]>f['o'][i] and f['cp'][i]>=.70 and f['vr'][i]>=.90 and f['body_atr'][i]>=.16 and f['rsi'][i]<=48 and f['quiet'][i]<=1.45)
    parent=(shock|l01|balance) & (extreme|(f['rsi']<=34)) & (f['vr']>=1.18)
    target_pct=(ATR_STOP*f['atr']*RR_TARGET/np.maximum(f['c'],1e-12))*100
    m=parent & (target_pct>=.30); m[:WARMUP]=False; m[-1:]=False
    return m

def run_symbol(sym,path,args):
    df=load_csv(path,args.max_bars,args.train_end_exclusive)
    if len(df)<MIN_BARS: return [],repr(f'too few bars: {len(df)}')
    f=features(df); m=entry_mask(f); trades=[]; next_i=WARMUP; cost=args.round_trip_cost_bps*.01
    for sig in np.flatnonzero(m):
        if sig<next_i: continue
        ei=int(sig+1)
        if ei>=len(f['c']): break
        ep=float(f['o'][ei]); av=float(f['atr'][sig])
        if not math.isfinite(ep) or not math.isfinite(av) or ep<=0 or av<=0: continue
        stop=ep-ATR_STOP*av; target=ep+ATR_STOP*av*RR_TARGET
        if stop<=0: continue
        last=min(len(f['c'])-1,ei+MAX_HOLD); xi=last; xp=float(f['c'][last]); reason='time'
        for j in range(ei,last+1):
            hs=float(f['l'][j])<=stop; ht=float(f['h'][j])>=target
            if hs and ht: xi=j; xp=stop; reason='stop_first_same_bar'; break
            if hs: xi=j; xp=stop; reason='stop'; break
            if ht: xi=j; xp=target; reason='target'; break
        pnl=(xp/ep-1)*100-cost
        trades.append(dict(symbol=sym,strategy=NAME,entry_ts=int(f['ts'][ei]),exit_ts=int(f['ts'][xi]),pnl_pct=float(pnl),hold_bars=int(xi-ei+1),entry_price=ep,exit_price=float(xp),exit_reason=reason))
        next_i=int(xi+COOLDOWN)
    return trades,''

def summarize(pnls,pos):
    cur=1.0; eq=[cur]; ruined=False
    for p in pnls:
        cur*=1+pos*(p/100); eq.append(cur)
        if cur<=1e-12: ruined=True; break
    a=np.asarray(eq); peaks=np.maximum.accumulate(a); dd=float(abs(np.min((a/np.where(peaks==0,1,peaks)-1)*100)))
    mx=float((a.max()-1)*100); fin=float((a[-1]-1)*100); cd=100*(1-dd/100)*(1+mx/100)
    return fin,mx,min(100,dd),cd,ruined

def max_conc(tr):
    ev=[]
    for t in tr: ev += [(int(t['entry_ts']),1),(int(t['exit_ts']),-1)]
    ev.sort(key=lambda x:(x[0],x[1])); cur=mx=0
    for _,d in ev: cur+=d; mx=max(mx,cur)
    return mx

def main(axis_default='long_max'):
    ap=argparse.ArgumentParser(); ap.add_argument('--axis',default=axis_default,choices=['long_max','long_main']); ap.add_argument('--data-root'); ap.add_argument('--symbol-cost'); ap.add_argument('--out-dir'); ap.add_argument('--max-symbols',type=int,default=0); ap.add_argument('--max-bars',type=int,default=0); ap.add_argument('--round-trip-cost-bps',type=float,default=FEE_BPS); ap.add_argument('--position-fraction',type=float,default=POS); ap.add_argument('--train-end-exclusive',default=TRAIN_END); ap.add_argument('--save-trade-rows',action='store_true')
    args=ap.parse_args(); version='V9' if args.axis=='long_max' else 'V13'; t0=time.time(); root=find_data_root(args.data_root); fmap=build_map(root); syms=[s for s in read_symbols(find_symbol_cost(args.symbol_cost),fmap) if norm(s) in fmap]
    if args.max_symbols: syms=syms[:args.max_symbols]
    out=Path(args.out_dir).expanduser().resolve() if args.out_dir else Path.cwd().resolve()/'local_results'/args.axis/f'{args.axis.upper()}_FROZEN_BASELINE_2025_{version}'; out.mkdir(parents=True,exist_ok=True)
    print(f'[RUN] {out}\n[BASELINE] {NAME}\n[CONFIG] symbols={len(syms)} train_end={args.train_end_exclusive} fee={args.round_trip_cost_bps} pos={args.position_fraction}',flush=True)
    trades=[]; errors=[]
    for i,s in enumerate(syms,1):
        tr,err=run_symbol(s,fmap[norm(s)],args); trades+=tr
        if err: errors.append(dict(symbol=s,error=err))
        if i%25==0 or i==len(syms): print(f'[PROGRESS] processed={i}/{len(syms)} errors={len(errors)} trade_rows={len(trades)} elapsed={time.time()-t0:.1f}s',flush=True)
    pnls=[float(t['pnl_pct']) for t in trades]; wins=sum(x>0 for x in pnls); losses=len(pnls)-wins; fin,mx,dd,cd,ruined=summarize(pnls,args.position_fraction)
    row=dict(axis=args.axis,strategy=NAME,entry_key=ENTRY_KEY,atr_stop=ATR_STOP,rr_target=RR_TARGET,max_hold_bars=MAX_HOLD,cooldown_bars=COOLDOWN,trades=len(pnls),wins=int(wins),losses=int(losses),win_rate_pct=(wins/len(pnls)*100 if pnls else 0),final_return_pct=fin,max_return_pct=mx,max_drawdown_pct=dd,official_cd_value=cd,cd_value=cd,max_conc=max_conc(trades),symbol_files=len(syms),errors=len(errors),ruined=bool(ruined),result_scope='2025년까지의 데이터 기준')
    pd.DataFrame([row]).to_csv(out/'frozen_baseline_aggregate_results.csv',index=False,encoding='utf-8-sig')
    if args.save_trade_rows: pd.DataFrame(trades).to_csv(out/'frozen_baseline_trades.csv',index=False,encoding='utf-8-sig')
    (out/'frozen_baseline_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
    diffs={}; ok=True
    for k,e in EXPECTED.items():
        a=row.get(k); good=(a==e if isinstance(e,(bool,int,str)) else abs(float(a)-float(e))<=1e-3); ok=ok and good; diffs[k]=dict(actual=a,expected=e,ok=bool(good))
    report=dict(baseline_reproduction_ok=bool(ok),actual=row,expected=EXPECTED,diffs=diffs)
    (out/'frozen_reproduction_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'frozen_reproduction_report.txt').write_text('\n'.join([f'baseline_reproduction_ok: {ok}',f'axis: {args.axis}',f'strategy: {NAME}',f'entry_key: {ENTRY_KEY}',f'official_cd_value: {cd}',f'trades: {len(pnls)}',f'max_conc: {row["max_conc"]}',f'errors: {len(errors)}']),encoding='utf-8')
    print(f'[RESULT] baseline_reproduction_ok={ok} cd_value={cd:.12f} trades={len(pnls)} errors={len(errors)}',flush=True)
