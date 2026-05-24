from __future__ import annotations
import argparse,json,math,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd

CFG=dict(strategy='smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540',axis='short_main',baseline_version='short_main/v13',initial_asset=100.0,position_fraction=0.01,fee_per_side=0.0004,min_bars=120,ema_period=20,rsi_period=14,atr_period=14,short_dev=0.032,short_rsi_min=77.0,use_rsi_gate=False,short_wick_mult=1.3,score_min_short=2.35,score_dev_weight=1.3,score_rsi_weight=0.8,score_wick_weight=0.7,score_dev_cap=2.0,score_rsi_cap=2.0,score_wick_cap=2.5,wick_atr_floor_mult=0.2,atr_stop_mult=2.15,rr_mult=5.4,min_expected_tp=0.003,timeout_bars=200,time_reduce_bars=4,time_reduce_to_risk_frac=0.05,fail_fast_bars=10,fail_fast_min_progress_r=0.1,atr_pct_min=0.0,atr_pct_max=999.0,body_pct_max=999.0,close_position_min=-999.0,upper_body_ratio_max=float('inf'),dd_brake_trigger_pct=0.03,dd_brake_freeze_steps=5,dd_brake_mode='edge_current')
EXPECTED=dict(trades=63863,max_return_pct=4220.190005886,max_drawdown_pct=4.260534220480682,official_cd_value=4136.12683229544,active_leftover=0,pending_leftover=0,load_errors=0)
OLD=dict(strategy='smv10_dev1_01_v10_stop210_rr550',trades=64128,max_return_pct=3942.1044355472736,max_drawdown_pct=4.38893845928694,official_cd_value=3864.6989594109964,profit_factor=1.7555392280496656)

def ema(a,p): return pd.Series(a,dtype=float).ewm(span=int(p),adjust=False).mean().to_numpy(float)
def rsi(a,p):
    s=pd.Series(a,dtype=float); d=s.diff(); up=d.clip(lower=0); dn=-d.clip(upper=0)
    rs=up.ewm(alpha=1/int(p),adjust=False).mean()/dn.ewm(alpha=1/int(p),adjust=False).mean().replace(0,np.nan)
    return (100-100/(1+rs)).to_numpy(float)
def atr(h,l,c,p):
    pc=np.roll(c,1); pc[0]=c[0]
    tr=np.maximum(h-l,np.maximum(np.abs(h-pc),np.abs(l-pc)))
    return pd.Series(tr,dtype=float).ewm(alpha=1/int(p),adjust=False).mean().to_numpy(float)
def norm(df):
    df=df.copy(); df.columns=[str(c).strip().replace('\ufeff','').lower() for c in df.columns]
    aliases=dict(date=['date','datetime','timestamp','time','open_time','opentime','candle_date_time_utc','candle_date_time_kst'],open=['open','open_price','opening_price','시가'],high=['high','high_price','고가'],low=['low','low_price','저가'],close=['close','close_price','closing_price','trade_price','종가'],volume=['volume','vol','base_volume','candle_acc_trade_volume','acc_trade_volume','거래량'])
    ren={}
    for target,names in aliases.items():
        hit=next((x for x in names if x in df.columns),None)
        if hit is None: raise ValueError('missing column '+target)
        ren[hit]=target
    out=df.rename(columns=ren)[['date','open','high','low','close','volume']].copy(); out['date']=pd.to_datetime(out['date'],errors='coerce')
    for c in ['open','high','low','close','volume']: out[c]=pd.to_numeric(out[c],errors='coerce')
    return out.dropna().sort_values('date').drop_duplicates('date').reset_index(drop=True)
def load_csv(path,end):
    if path.read_text(encoding='utf-8',errors='ignore')[:80].startswith('version https://git-lfs.github.com/spec/'): raise ValueError('LFS pointer')
    d=norm(pd.read_csv(path,low_memory=False)); d=d[d.date<=end].reset_index(drop=True)
    if len(d)<CFG['min_bars']: raise ValueError('too few bars '+str(len(d)))
    o=d.open.to_numpy(float); h=d.high.to_numpy(float); l=d.low.to_numpy(float); c=d.close.to_numpy(float); v=d.volume.to_numpy(float); ts=pd.to_datetime(d.date).astype('int64').to_numpy()
    return dict(symbol=path.stem,ts=ts,open=o,high=h,low=l,close=c,volume=v,ema20=ema(c,CFG['ema_period']),rsi14=rsi(c,CFG['rsi_period']),atr14=atr(h,l,c,CFG['atr_period']),body=np.abs(c-o),upper_wick=h-np.maximum(o,c),candle_range=np.maximum(h-l,1e-12))
def calc_score(s,i):
    close=s['close'][i]; e=s['ema20'][i]; rr=s['rsi14'][i]; at=s['atr14'][i]; body=s['body'][i]; up=s['upper_wick'][i]
    ds=max(0,min(max(0,close/max(e,1e-12)-1)/CFG['short_dev'],CFG['score_dev_cap']))
    rs=max(0,min(max(0,rr-CFG['short_rsi_min'])/10,CFG['score_rsi_cap']))
    ws=max(0,min(math.log1p(max(0,up/max(abs(body),at*CFG['wick_atr_floor_mult'],1e-12))),CFG['score_wick_cap']))
    return CFG['score_dev_weight']*ds+CFG['score_rsi_weight']*rs+CFG['score_wick_weight']*ws
def make_pending(si,s,i):
    j=i+1
    if j>=len(s['ts']): return None
    vals=[s['close'][i],s['ema20'][i],s['rsi14'][i],s['atr14'][i],s['open'][j]]
    if not all(np.isfinite(float(x)) for x in vals): return None
    close=s['close'][i]; e=s['ema20'][i]; rr=s['rsi14'][i]; at=s['atr14'][i]; body=s['body'][i]; up=s['upper_wick'][i]
    if e<=0 or at<=0: return None
    rng=s['candle_range'][i]; candle_pos=(close-s['low'][i])/max(rng,1e-12); atr_pct=at/max(close,1e-12); body_pct=body/max(close,1e-12); up_body_ratio=up/max(abs(body),1e-12)
    if atr_pct<CFG['atr_pct_min'] or atr_pct>CFG['atr_pct_max'] or body_pct>CFG['body_pct_max'] or candle_pos<CFG['close_position_min']: return None
    if np.isfinite(float(CFG['upper_body_ratio_max'])) and up_body_ratio>CFG['upper_body_ratio_max']: return None
    sc=calc_score(s,i)
    ok=(close/max(e,1e-12)-1>=CFG['short_dev']) and (up>=CFG['short_wick_mult']*body) and (sc>=CFG['score_min_short'])
    if CFG['use_rsi_gate']: ok=ok and rr>CFG['short_rsi_min']
    if not ok: return None
    entry=float(s['open'][j]); risk=at*CFG['atr_stop_mult']; stop=entry+risk; target=entry-CFG['rr_mult']*risk; etp=(entry-target)/max(entry,1e-12)
    if entry<=0 or etp<CFG['min_expected_tp']: return None
    return dict(si=si,symbol=s['symbol'],sig=i,ei=j,ets=int(s['ts'][j]),entry=entry,risk=float(risk),stop=float(stop),target=float(target),score=float(sc),mfe=0.0,notional=0.0)
def ret_short(e,x): return e/max(x,1e-12)-1-2*CFG['fee_per_side']
def cd(mr,md): return 100*(1-abs(md)/100)*(1+mr/100)
def run(S,events,timeline,end,hold):
    eq=peak=peak_asset=CFG['initial_asset']; mdd=gp=gl=0.0; wins=losses=trades=same_bar=0
    active={}; pend=defaultdict(list); generated=executed=blocked=maxc=maxcu=freeze=0; prev_below=False
    for ts in timeline:
        cand=[p for p in pend.pop(ts,[]) if p['si'] not in active]; cand.sort(key=lambda x:x['score'],reverse=True)
        if freeze>0: blocked+=len(cand); cand=[]; freeze-=1
        snap=eq
        for p in cand:
            if p['si'] not in active: p['notional']=snap*CFG['position_fraction']; active[p['si']]=p; executed+=1
        maxc=max(maxc,len(active)); maxcu=max(maxcu,len({p['symbol'] for p in active.values()}))
        for si,i in events.get(ts,[]):
            p=active.get(si)
            if p is None or i<p['ei']: continue
            s=S[si]; bh=i-p['ei']; p['mfe']=max(p['mfe'],(p['entry']-s['low'][i])/max(p['risk'],1e-12))
            if bh>=CFG['time_reduce_bars'] and p['mfe']>0: p['stop']=min(p['stop'],p['entry']+p['risk']*CFG['time_reduce_to_risk_frac'])
            x=None
            if s['high'][i]>=p['stop']: x=p['stop']
            elif s['low'][i]<=p['target']: x=p['target']
            elif bh>=CFG['fail_fast_bars'] and p['mfe']<CFG['fail_fast_min_progress_r'] and s['close'][i]>p['entry']: x=float(s['close'][i])
            elif bh>=CFG['timeout_bars']: x=float(s['close'][i])
            if x is not None:
                r=ret_short(p['entry'],float(x)); pnl=p['notional']*r; eq+=pnl; peak=max(peak,eq); peak_asset=max(peak_asset,eq); mdd=min(mdd,eq/max(peak,1e-12)-1)
                trades+=1; same_bar+=int(p['ets']==int(ts))
                if pnl>0: wins+=1; gp+=pnl
                else: losses+=1; gl+=-pnl
                del active[si]
        dd=eq/max(peak,1e-12)-1; below=dd<=-CFG['dd_brake_trigger_pct']
        if below and not prev_below: freeze=max(freeze,CFG['dd_brake_freeze_steps'])
        prev_below=bool(below)
        for si,i in events.get(ts,[]):
            if si in active: continue
            p=make_pending(si,S[si],i)
            if p is not None: pend[p['ets']].append(p); generated+=1
    for si,p in list(active.items()):
        s=S[si]; i=len(s['ts'])-1; x=float(s['close'][i]); xt=int(s['ts'][i]); r=ret_short(p['entry'],x); pnl=p['notional']*r; eq+=pnl; peak=max(peak,eq); peak_asset=max(peak_asset,eq); mdd=min(mdd,eq/max(peak,1e-12)-1)
        trades+=1; same_bar+=int(p['ets']==xt)
        if pnl>0: wins+=1; gp+=pnl
        else: losses+=1; gl+=-pnl
        del active[si]
    mr=(peak_asset/CFG['initial_asset']-1)*100; md=abs(mdd)*100
    res=dict(strategy=CFG['strategy'],axis=CFG['axis'],baseline_version=CFG['baseline_version'],engine='actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231',data_scope='train_only_until_2025_12_31_end',end_date=str(end),holdout_start=str(hold),trades=trades,wins=wins,losses=losses,win_rate_pct=wins/trades*100 if trades else 0,final_asset=eq,final_return_pct=(eq/CFG['initial_asset']-1)*100,peak_asset=peak_asset,max_return_pct=mr,max_drawdown_pct=md,official_cd_value=cd(mr,md),profit_factor=gp/gl if gl>0 else float('inf'),max_conc=maxc,max_conc_unique_symbols=maxcu,same_bar_trades=same_bar,active_leftover=len(active),pending_leftover=sum(len(v) for v in pend.values()),blocked_by_guard=blocked,generated_entry_candidates=generated,executed_entries=executed,fee_per_side=CFG['fee_per_side'],position_fraction=CFG['position_fraction'],score_dev_weight=CFG['score_dev_weight'],score_rsi_weight=CFG['score_rsi_weight'],score_wick_weight=CFG['score_wick_weight'],short_dev=CFG['short_dev'],short_wick_mult=CFG['short_wick_mult'],score_min_short=CFG['score_min_short'],atr_stop_mult=CFG['atr_stop_mult'],rr_mult=CFG['rr_mult'],min_expected_tp=CFG['min_expected_tp'],timeout_bars=CFG['timeout_bars'],time_reduce_bars=CFG['time_reduce_bars'],fail_fast_bars=CFG['fail_fast_bars'],atr_pct_min=CFG['atr_pct_min'],atr_pct_max=CFG['atr_pct_max'],close_position_min=CFG['close_position_min'],dd_brake_trigger_pct=CFG['dd_brake_trigger_pct'],dd_brake_freeze_steps=CFG['dd_brake_freeze_steps'],dd_brake_mode=CFG['dd_brake_mode'],previous_strategy=OLD['strategy'],previous_trades=OLD['trades'],previous_max_return_pct=OLD['max_return_pct'],previous_max_drawdown_pct=OLD['max_drawdown_pct'],previous_official_cd_value=OLD['official_cd_value'],previous_profit_factor=OLD['profit_factor'])
    res['delta_cd_vs_previous']=res['official_cd_value']-OLD['official_cd_value']; res['delta_mdd_vs_previous']=res['max_drawdown_pct']-OLD['max_drawdown_pct']; res['delta_trades_vs_previous']=res['trades']-OLD['trades']
    return res
def has_csv(p): return p.exists() and p.is_dir() and any(x.suffix.lower()=='.csv' for x in p.glob('*.csv'))
def resolve_data_dir(arg):
    if arg:
        p=Path(arg).expanduser().resolve()
        if not has_csv(p): raise FileNotFoundError('CSV 데이터 폴더가 아님: '+str(p))
        return p
    here=Path(__file__).resolve().parent
    for p in [here/'Data'/'time',here.parent/'Data'/'time',here.parent.parent/'Data'/'time',here/'코인'/'Data'/'time',here.parent/'코인'/'Data'/'time',here.parent.parent/'코인'/'Data'/'time']:
        if has_csv(p): return p.resolve()
    raise FileNotFoundError('CSV 데이터 폴더를 찾지 못했다. --data-dir로 OHLCV CSV 폴더를 지정해라.')
def gate(res,strict):
    bad=[]
    for k,e in EXPECTED.items():
        g=res.get(k)
        if isinstance(e,float):
            if g is None or abs(float(g)-e)>1e-6: bad.append(f'{k}: got={g} expected={e}')
        elif g!=e: bad.append(f'{k}: got={g} expected={e}')
    if bad:
        msg=CFG['baseline_version']+' frozen reproduction gate failed:\n'+'\n'.join(bad)
        if strict: raise RuntimeError(msg)
        print('[WARN]',msg)
    else: print('[GATE PASS]',CFG['baseline_version'],'공식 기준값 재현 완료')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-dir'); ap.add_argument('--out-dir'); ap.add_argument('--recursive',action='store_true'); ap.add_argument('--limit-files',type=int); ap.add_argument('--min-csv-files',type=int,default=100); ap.add_argument('--allow-small-data',action='store_true'); ap.add_argument('--no-strict-gate',action='store_true'); ap.add_argument('--end-date',default='2025-12-31 23:59:59'); ap.add_argument('--holdout-start',default='2026-01-01 00:00:00'); a=ap.parse_args()
    dd=resolve_data_dir(a.data_dir); out=Path(a.out_dir).expanduser().resolve() if a.out_dir else Path(__file__).resolve().parent/'short_main_v13_frozen_reproduce_results'; out.mkdir(parents=True,exist_ok=True)
    files=sorted(dd.rglob('*.csv') if a.recursive else dd.glob('*.csv'))
    if a.limit_files: files=files[:a.limit_files]
    if len(files)<a.min_csv_files and not a.allow_small_data: raise RuntimeError(f'CSV 파일 수가 너무 적다: {len(files)}개. 실제 OHLCV 폴더인지 확인해라.')
    end=pd.to_datetime(a.end_date); hold=pd.to_datetime(a.holdout_start)
    if end>=hold: raise ValueError('end-date는 holdout-start보다 빨라야 한다.')
    S=[]; errs=[]
    for n,p in enumerate(files,1):
        try: S.append(load_csv(p,end))
        except Exception as e: errs.append(dict(file=str(p),error=repr(e),traceback=traceback.format_exc(limit=1)))
        if n%50==0: print(f'[LOAD] files={n}/{len(files)} loaded_symbols={len(S)} load_errors={len(errs)}',flush=True)
    events=defaultdict(list)
    for si,s in enumerate(S):
        for i,ts in enumerate(s['ts']): events[int(ts)].append((si,i))
    timeline=sorted(events.keys())
    print(CFG['baseline_version'].upper(),'STANDALONE FROZEN REPRODUCE RUNNER')
    print('data_dir=',dd,'csv_files=',len(files),'loaded_symbols=',len(S),'timeline=',len(timeline),'out_dir=',out)
    res=run(S,events,timeline,end,hold); res['load_errors']=len(errs)
    try: gate(res,not a.no_strict_gate)
    except Exception as e:
        (out/'BASELINE_GATE_FAILED_DO_NOT_USE.txt').write_text(str(e),encoding='utf-8')
        pd.DataFrame([res]).to_csv(out/'summary_compact.csv',index=False,encoding='utf-8-sig')
        raise
    pd.DataFrame([res]).to_csv(out/'summary_compact.csv',index=False,encoding='utf-8-sig'); pd.DataFrame([res]).to_csv(out/'summary_full.csv',index=False,encoding='utf-8-sig')
    if errs: (out/'load_errors.json').write_text(json.dumps(errs,ensure_ascii=False,indent=2),encoding='utf-8')
    meta=dict(baseline_version=CFG['baseline_version'],source_file=Path(__file__).name,standalone=True,uses_external_runner=False,engine=res['engine'],data_scope=res['data_scope'],end_date=str(end),holdout_start=str(hold),engine_rules=['previous candle close signal -> current open entry','same timestamp exit cannot enable same timestamp entry','current candle exit affects next timestamp','same-bar TP/SL allowed','DD brake applies from next timestamp','2026 excluded before indicator calculation'],csv_files=len(files),loaded_symbols=len(S),load_errors=len(errs),data_dir=str(dd),runtime_external_path_reference=False,strategy=CFG,expected_gate=EXPECTED)
    (out/'run_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print('saved:',out/'summary_compact.csv')
if __name__=='__main__': main()
