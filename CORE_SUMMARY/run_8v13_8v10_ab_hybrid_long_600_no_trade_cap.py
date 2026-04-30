from __future__ import annotations

import argparse, csv, json, math, os, random, time, traceback
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import pandas as pd

BATCH = '8V13_8V10_AB_HYBRID_LONG_600_NO_TRADE_CAP'
POS_FRAC = 0.01
COST_PCT = 0.10
WARMUP = 160
MIN_BARS = 250
LONG_MAIN_CD = 121.7490287208
LONG_MAX_CD = 134.5158668232

@dataclass(frozen=True)
class Spec:
    name: str
    parent: str
    group: str
    entry: str
    stop_atr: float
    rr: float
    hold: int
    cooldown: int
    atrp_max: float
    vol_min: float
    body_min: float
    close_pos_min: float
    trend: bool
    reclaim: bool
    low_anchor: bool
    second_leg: bool
    wick_min: float
    be_r: float
    trail_r: float
    trail_atr: float
    shock_ret5: float
    shock_range: float
    post_loss_bars: int
    sym_dd_pct: float

def cd_value(max_return: float, mdd: float) -> float:
    return 0.0 if mdd >= 100 else 100 * (1 - abs(mdd) / 100) * (1 + max_return / 100)

def equity_stats(pnls: List[float]) -> Tuple[float, float, float, float]:
    eq = peak = mx = 1.0; mdd = 0.0
    for p in pnls:
        eq *= max(0.0, 1 + POS_FRAC * p / 100)
        peak = max(peak, eq); mx = max(mx, eq)
        if peak > 0: mdd = max(mdd, abs(eq / peak - 1) * 100)
        if eq <= 1e-12: return -100.0, max(0, (mx - 1) * 100), 100.0, 0.0
    final_ret = (eq - 1) * 100; max_ret = (mx - 1) * 100
    return final_ret, max_ret, mdd, cd_value(max_ret, mdd)

def norm(x: str) -> str:
    return str(x).upper().replace('/', '').replace('_', '').replace('-', '').replace(' ', '')

def infer_symbol(p: Path) -> str:
    s = p.stem.upper().replace('_5M', '').replace('-5M', '').replace('PERP', '')
    if s.endswith('USDT'): return s[:-4] + '/USDT'
    if s.endswith('USD'): return s[:-3] + '/USD'
    return s

def find_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here] + list(here.parents):
        if (p/'symbol_cost').exists() or (p/'코인'/'Data'/'time').exists() or (p/'Data'/'time').exists(): return p
    return here

def build_file_map(data_root: Path) -> Dict[str, Path]:
    if not data_root.exists(): raise FileNotFoundError(f'data root not found: {data_root}')
    mp = {}
    for p in data_root.rglob('*.csv'):
        mp.setdefault(norm(p.stem), p); mp.setdefault(norm(infer_symbol(p)), p)
    if not mp: raise FileNotFoundError(f'csv files not found: {data_root}')
    return mp

def load_symbols(symbol_cost: Path, mp: Dict[str, Path]) -> List[str]:
    syms = []
    if symbol_cost.is_file():
        try:
            df = pd.read_csv(symbol_cost); col = 'symbol' if 'symbol' in df.columns else df.columns[0]
            syms = df[col].dropna().astype(str).tolist()
        except Exception:
            try:
                obj = json.loads(symbol_cost.read_text(encoding='utf-8'))
                syms = list(obj.keys()) if isinstance(obj, dict) else [str(x.get('symbol', x)) if isinstance(x, dict) else str(x) for x in obj]
            except Exception:
                syms = [x.strip() for x in symbol_cost.read_text(encoding='utf-8', errors='ignore').splitlines() if x.strip()]
    out = [infer_symbol(mp[norm(s)]) for s in syms if norm(s) in mp]
    return sorted(set(out)) if out else sorted({infer_symbol(p) for p in mp.values()})

def load_features(path: Path, max_bars: Optional[int]) -> Dict[str, np.ndarray]:
    df = pd.read_csv(path, low_memory=False)
    ren = {}
    for c in df.columns:
        lc = str(c).lower().strip()
        if lc in ['time','timestamp','date','datetime','open_time']: ren[c] = 'ts'
        elif lc in ['open','o']: ren[c] = 'o'
        elif lc in ['high','h']: ren[c] = 'h'
        elif lc in ['low','l']: ren[c] = 'l'
        elif lc in ['close','c']: ren[c] = 'c'
        elif lc in ['volume','vol','v','quote_volume']: ren[c] = 'v'
    df = df.rename(columns=ren)
    if 'ts' not in df: df['ts'] = np.arange(len(df))
    for c in ['o','h','l','c','v']: df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df[['ts','o','h','l','c','v']].replace([np.inf,-np.inf], np.nan).dropna().reset_index(drop=True)
    if max_bars and len(df) > max_bars: df = df.tail(max_bars).reset_index(drop=True)
    if len(df) < MIN_BARS: raise ValueError(f'not enough bars: {len(df)}')
    o,h,l,c,v = [df[x].astype(float) for x in ['o','h','l','c','v']]
    tr = pd.concat([(h-l).abs(), (h-c.shift(1)).abs(), (l-c.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/14, adjust=False).mean().bfill().fillna(0)
    ema20 = c.ewm(span=20, adjust=False).mean(); ema50 = c.ewm(span=50, adjust=False).mean()
    hh20 = h.rolling(20, min_periods=1).max(); ll20 = l.rolling(20, min_periods=1).min()
    rng = (h-l).replace(0, np.nan); body = (c-o).abs()
    return {'ts':pd.to_numeric(df.ts, errors='coerce').ffill().fillna(0).astype('int64').to_numpy(),'o':o.to_numpy(),'h':h.to_numpy(),'l':l.to_numpy(),'c':c.to_numpy(),'atr':atr.to_numpy(),'atrp':(atr/c.replace(0,np.nan)).fillna(0).to_numpy(),'ema20':ema20.to_numpy(),'ema50':ema50.to_numpy(),'hh20':hh20.to_numpy(),'ll20':ll20.to_numpy(),'range20p':((hh20-ll20)/c.replace(0,np.nan)).fillna(0).to_numpy(),'volr':(v/v.rolling(20,min_periods=1).mean().replace(0,np.nan)).fillna(0).to_numpy(),'body_atr':(body/atr.replace(0,np.nan)).fillna(0).to_numpy(),'close_pos':((c-l)/rng).fillna(0.5).to_numpy(),'lw_body':((np.minimum(o,c)-l).clip(lower=0)/body.replace(0,np.nan)).fillna(0).to_numpy(),'uw_rng':((h-np.maximum(o,c)).clip(lower=0)/rng).fillna(0).to_numpy(),'ret3':c.pct_change(3).fillna(0).to_numpy(),'ret5':c.pct_change(5).fillna(0).to_numpy(),'ret10':c.pct_change(10).fillna(0).to_numpy(),'ret20':c.pct_change(20).fillna(0).to_numpy()}

def make_specs(limit: Optional[int]) -> List[Spec]:
    out=[]
    for k in range(600):
        block,j=k//150,k%150
        if block==0: parent,group,entry='long_max_v1_8v10B','b102_dd_compress','trend_runner'
        elif block==1: parent,group,entry='long_main_v1_8v10A','b176_return_lift','rescue_mix'
        elif block==2: parent,group,entry='long_hybrid_v1_8v10AB','ab_absorb_mix','hybrid_ab'
        else: parent,group,entry='long_safe_v1_v51','safe_branch_repair','rescue_mix'
        out.append(Spec(f'8V13_{parent}_{j+1:03d}_{group}',parent,group,entry,1.05+(j%7)*0.04,1.98+((j//7)%8)*0.09,16+((j//24)%6)*3,10+(j%8)*2,0.046+((j//5)%7)*0.004,1.04+((j//5)%7)*0.055,0.18+((j//8)%6)*0.035,0.60+((j//9)%6)*0.03,(j%4!=1) if block==0 else (j%5==0),(j%3!=0) if block==0 else (j%3==1),(j%6 in [1,4]) if block in [1,3] else (j%10 in [2,7]),block==2 and j%15==0,0.22+(j%8)*0.10 if block==0 else 0.38+(j%8)*0.10,0.82+(j%5)*0.09,1.12+((j//5)%7)*0.11,1.24+((j//9)%8)*0.09,-0.036-((j//7)%5)*0.006,0.068+((j//15)%6)*0.009,10+((j//6)%7)*4,0.16+((j//11)%7)*0.022))
    out.sort(key=lambda s:s.name)
    return out[:limit] if limit else out

def entry_ok(f: Dict[str,np.ndarray], i:int, s:Spec) -> Tuple[bool,float]:
    if f['c'][i]<=0 or f['atrp'][i]>s.atrp_max or f['volr'][i]<s.vol_min or f['body_atr'][i]<s.body_min or f['close_pos'][i]<s.close_pos_min or f['uw_rng'][i]>0.78: return False,0
    if s.trend and f['ema20'][i] < f['ema50'][i]*0.995: return False,0
    if s.reclaim and f['c'][i] < f['ema20'][i]*0.997: return False,0
    if s.low_anchor and f['l'][i] > f['ll20'][i-1]*1.003: return False,0
    rescue=(f['ret5'][i]<=-0.010 or f['ret10'][i]<=-0.018) and f['lw_body'][i]>=s.wick_min*0.75
    runner=f['c'][i]>f['ema20'][i] and f['ema20'][i]>=f['ema50'][i]*0.995
    second=f['ret10'][i]<-0.012 and f['ret3'][i]>-0.008 and f['lw_body'][i]>=s.wick_min
    release=f['c'][i]>=f['hh20'][i-1]*0.995 and f['volr'][i]>=max(1.10,s.vol_min)
    if s.second_leg and not second: return False,0
    if s.entry=='trend_runner': score=(1 if runner else 0)+(0.35 if release else 0)+(0.15 if second else 0)
    elif s.entry=='rescue_mix': score=(1 if rescue else 0)+(0.35 if release else 0)+(0.35 if second else 0)
    else: score=(0.75 if rescue else 0)+(0.75 if runner else 0)+(0.35 if release else 0)+(0.35 if second else 0)
    return score>=0.60,score

def simulate(f: Dict[str,np.ndarray], s: Spec) -> List[Tuple[int,float]]:
    pnls=[]; pos=False; ep=stp=tgt=hi=0.0; ei=0; cd_until=loss_until=dd_until=-1; eq=peak=1.0; losses=0
    for i in range(WARMUP,len(f['c'])):
        if pos:
            hi=max(hi,f['h'][i]); risk=max(1e-12,ep-stp); r=(hi-ep)/risk
            if r>=s.be_r: stp=max(stp,ep*1.0005)
            if r>=s.trail_r: stp=max(stp,hi-f['atr'][i]*s.trail_atr)
            xp=None
            if f['l'][i]<=stp: xp=stp
            elif f['h'][i]>=tgt: xp=tgt
            elif i-ei>=s.hold: xp=f['c'][i]
            if xp is not None:
                p=(xp/ep-1)*100-COST_PCT; pnls.append((int(f['ts'][i]),float(p)))
                eq*=max(0,1+POS_FRAC*p/100); peak=max(peak,eq)
                losses=losses+1 if p<=0 else 0
                if losses>=2: loss_until=max(loss_until,i+s.post_loss_bars)
                if peak>0 and abs(eq/peak-1)*100>=s.sym_dd_pct: dd_until=max(dd_until,i+24)
                cd_until=max(cd_until,i+s.cooldown); pos=False
            continue
        if i<=cd_until or i<=loss_until or i<=dd_until: continue
        if f['ret5'][i]<=s.shock_ret5 and f['range20p'][i]>=s.shock_range and f['close_pos'][i]<0.34: continue
        ok,score=entry_ok(f,i,s)
        if not ok or f['atr'][i]<=0: continue
        ep=f['c'][i]; risk=f['atr'][i]*s.stop_atr; stp=ep-risk; tgt=ep+risk*s.rr*(1+min(0.18,max(0,score-1)*0.07)); hi=ep; ei=i; pos=True
    if pos and ep>0: pnls.append((int(f['ts'][-1]),float((f['c'][-1]/ep-1)*100-COST_PCT)))
    return pnls

def task(args):
    sym,path,specs,max_bars=args
    try:
        f=load_features(Path(path),max_bars); return sym,{s.name:simulate(f,s) for s in specs},None
    except Exception as e:
        return sym,{},f'{type(e).__name__}: {e}\n{traceback.format_exc(limit=2)}'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-root'); ap.add_argument('--symbol-cost'); ap.add_argument('--output-root',default='local_results'); ap.add_argument('--workers',type=int,default=max(1,min(4,(os.cpu_count() or 2)-1))); ap.add_argument('--max-symbols',type=int); ap.add_argument('--max-bars',type=int); ap.add_argument('--limit-strategies',type=int)
    ns=ap.parse_args(); random.seed(813); np.random.seed(813); t0=time.time(); root=find_root(); dr=Path(ns.data_root).resolve() if ns.data_root else (root/'코인'/'Data'/'time' if (root/'코인'/'Data'/'time').exists() else root/'Data'/'time').resolve(); sc=Path(ns.symbol_cost).resolve() if ns.symbol_cost else (root/'symbol_cost').resolve()
    mp=build_file_map(dr); syms=load_symbols(sc,mp); syms=syms[:ns.max_symbols] if ns.max_symbols else syms; ss=make_specs(ns.limit_strategies); out=Path(ns.output_root).resolve()/BATCH; out.mkdir(parents=True,exist_ok=True); (out/'strategies.json').write_text(json.dumps([asdict(s) for s in ss],ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'[BATCH] {BATCH}'); print(f'[DATA] {dr}'); print(f'[SYMBOLS] {len(syms)} [STRATEGIES] {len(ss)}')
    agg={s.name:[] for s in ss}; errs=[]; jobs=[(sym,str(mp[norm(sym)]),ss,ns.max_bars) for sym in syms if norm(sym) in mp]
    if ns.workers<=1: iterator=map(task,jobs)
    else:
        ex=ProcessPoolExecutor(max_workers=ns.workers); iterator=as_completed([ex.submit(task,j) for j in jobs])
    done=0
    for item in iterator:
        sym,res,err=item.result() if ns.workers>1 else item; done+=1
        if err: errs.append((sym,err))
        else:
            for k,v in res.items(): agg[k].extend(v)
        if done%25==0 or done==len(jobs): print(f'[PROGRESS] processed={done}/{len(jobs)} errors={len(errs)} elapsed={time.time()-t0:.1f}s',flush=True)
    if ns.workers>1: ex.shutdown()
    rows=[]; spec_map={s.name:s for s in ss}
    for s in ss:
        tr=sorted(agg[s.name],key=lambda x:x[0]); pn=[p for _,p in tr]; final,maxret,mdd,cd=equity_stats(pn); wins=sum(1 for p in pn if p>0)
        rows.append({'strategy':s.name,'parent':s.parent,'group':s.group,'entry':s.entry,'trades':len(pn),'wins':wins,'losses':len(pn)-wins,'win_rate_pct':wins/len(pn)*100 if pn else 0,'final_return_pct':final,'max_return_pct':maxret,'max_drawdown_pct':mdd,'official_cd_value':cd,**asdict(s)})
    rows.sort(key=lambda r:r['official_cd_value'],reverse=True)
    csvp=out/f'{BATCH}_registry.csv'
    with csvp.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    best5=next((r for r in rows if r['trades']>0 and r['max_drawdown_pct']<5),None); besta=next((r for r in rows if r['trades']>0),None)
    lines=[BATCH,'','candidate A MDD<5',json.dumps(best5,ensure_ascii=False,default=str) if best5 else 'none','','candidate B any-MDD',json.dumps(besta,ensure_ascii=False,default=str) if besta else 'none','',f'LONG_MAIN_CD={LONG_MAIN_CD}',f'LONG_MAX_CD={LONG_MAX_CD}','','top20']
    for i,r in enumerate(rows[:20],1): lines.append(f"{i}. {r['strategy']} | trades={r['trades']} | max_return={r['max_return_pct']:.6f} | mdd={r['max_drawdown_pct']:.6f} | cd={r['official_cd_value']:.6f}")
    (out/'master_summary.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8'); (out/'failed_symbols.json').write_text(json.dumps(errs,ensure_ascii=False,indent=2),encoding='utf-8')
    print('[BASELINE UPDATE]' if best5 and best5['official_cd_value']>LONG_MAIN_CD else '[NO BASELINE UPDATE]')
    if best5: print(f"[BEST MDD<5] {best5['strategy']} cd={best5['official_cd_value']:.6f} mdd={best5['max_drawdown_pct']:.6f} max_return={best5['max_return_pct']:.6f} trades={best5['trades']}")
    if besta: print(f"[BEST ANY] {besta['strategy']} cd={besta['official_cd_value']:.6f} mdd={besta['max_drawdown_pct']:.6f} max_return={besta['max_return_pct']:.6f} trades={besta['trades']}")
    print(f'[DONE] {csvp}')

if __name__ == '__main__':
    main()
