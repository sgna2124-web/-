from __future__ import annotations
import importlib.util
import json
from collections import deque
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'v76_short_base.json'
COMB = ROOT / 'experiments' / 'v76_short_combinations.json'
V56 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes.py'

spec = importlib.util.spec_from_file_location('v56mod', str(V56))
v56mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v56mod)


def bars_diff(a, b):
    return int((pd.Timestamp(a) - pd.Timestamp(b)).total_seconds() // 300)


def evaluate_router(trades, initial_asset, position_fraction, tc, router):
    if not trades:
        return {'trades':0,'final_asset':float(initial_asset),'final_return':0.0,'peak_asset':float(initial_asset),'peak_growth':0.0,'win_rate':0.0,'pf':0.0,'mdd':0.0,'max_conc':0,'max_conc_unique_symbols':0,'same_bar_trades':0,'active_leftover':0}
    by_entry={}; by_exit={}; signal_history={}
    for idx,tr in enumerate(trades):
        by_entry.setdefault(tr['entry_ts'], []).append(idx)
        by_exit.setdefault(tr['exit_ts'], []).append(idx)
        signal_history.setdefault(tr['symbol'], []).append(pd.Timestamp(tr['entry_ts']))
    for sym in signal_history: signal_history[sym].sort()
    timestamps=sorted(set(by_entry.keys())|set(by_exit.keys()))
    equity=float(initial_asset); peak=equity; peak_asset=equity; mdd=0.0; active={}; max_conc=0; max_conc_symbols=0; gp=0.0; gl=0.0; wins=0; executed=set(); same_bar_trades=sum(1 for tr in trades if tr.get('same_bar'))
    score_min_short = v56mod.safe_threshold(tc.get('score_min')) if tc.get('score_min_short') is None else float(tc.get('score_min_short'))
    max_active_cap = tc.get('max_active_cap'); max_per_symbol = tc.get('max_per_symbol')
    loss_streak_trigger_losses = tc.get('loss_streak_trigger_losses'); loss_streak_window = tc.get('loss_streak_window'); loss_streak_freeze_steps=int(tc.get('loss_streak_freeze_steps',0) or 0)
    dd_brake_trigger_pct = tc.get('dd_brake_trigger_pct'); dd_brake_freeze_steps=int(tc.get('dd_brake_freeze_steps',0) or 0)
    reentry_gap_after_close_bars = tc.get('reentry_gap_after_close_bars'); entry_gap_same_symbol_bars = tc.get('entry_gap_same_symbol_bars'); skip_dense_ts_threshold = tc.get('skip_dense_ts_threshold')
    recent_closed=deque(maxlen=int(loss_streak_window or 1)); loss_freeze_left=0; dd_freeze_left=0; prev_dd_below=False; last_entry_ts_by_symbol={}; last_exit_ts_by_symbol={}
    asia_hours={int(x) for x in router.get('asia_hours_utc', [])}; us_hours={int(x) for x in router.get('us_hours_utc', [])}
    def count_prior(sym, ts, window_bars):
        cur=pd.Timestamp(ts); cnt=0
        for old in signal_history.get(sym, []):
            if old >= cur: break
            if bars_diff(cur, old) <= int(window_bars): cnt += 1
        return cnt
    for ts in timestamps:
        exit_idxs=by_exit.get(ts, []); normal_exit=[i for i in exit_idxs if trades[i]['entry_ts'] < ts]; same_bar_exit=[i for i in exit_idxs if trades[i]['entry_ts'] == ts]
        def close_idx(idx):
            nonlocal equity, peak, peak_asset, mdd, gp, gl, wins
            pos=active.pop(idx, None)
            if pos is None: return
            tr=trades[idx]; pnl=pos['notional']*tr['return']; equity += pnl; peak=max(peak,equity); peak_asset=max(peak_asset,equity); mdd=min(mdd,equity/peak-1.0)
            if pnl>0: wins += 1; gp += pnl; recent_closed.append(1)
            else: gl += -pnl; recent_closed.append(0)
            last_exit_ts_by_symbol[tr['symbol']] = pd.Timestamp(tr['exit_ts'])
        for idx in normal_exit: close_idx(idx)
        if loss_streak_trigger_losses is not None and loss_streak_window is not None and len(recent_closed)==int(loss_streak_window):
            if sum(1 for x in recent_closed if x==0) >= int(loss_streak_trigger_losses): loss_freeze_left=max(loss_freeze_left, loss_streak_freeze_steps); recent_closed.clear()
        current_dd=equity/peak-1.0; dd_below=(dd_brake_trigger_pct is not None) and (current_dd <= -float(dd_brake_trigger_pct))
        if dd_below and not prev_dd_below: dd_freeze_left=max(dd_freeze_left, dd_brake_freeze_steps)
        prev_dd_below=bool(dd_below)
        entry_idxs=by_entry.get(ts, [])
        if not entry_idxs: continue
        candidates=[]
        for idx in entry_idxs:
            tr=trades[idx]; score=tr.get('score',0.0)
            if tr.get('side') != -1 or score < score_min_short: continue
            sym=tr['symbol']; t=pd.Timestamp(tr['entry_ts']); hr=int(t.hour); prior24=count_prior(sym,t,24); prior48=count_prior(sym,t,48)
            route=None
            if hr in asia_hours and prior48 >= int(router.get('asia_prior_required', 99)): route='asia'
            elif hr in us_hours and prior24 >= int(router.get('us_prior_required', 99)): route='us'
            elif router.get('allow_allhours_fallback') and prior48 >= int(router.get('fallback_prior_required', 99)):
                route='fallback'
            elif router.get('quiet_bars') is not None and count_prior(sym,t,int(router['quiet_bars']))==0:
                route='quiet'
            if route is None: continue
            effective_max_per_symbol = None if (router.get('broad_when_prior2') and prior48 >= 2) else max_per_symbol
            effective_reentry_gap = None if (router.get('drop_reentry_when_prior2') and prior48 >= 2) else reentry_gap_after_close_bars
            if entry_gap_same_symbol_bars is not None and sym in last_entry_ts_by_symbol and bars_diff(t, last_entry_ts_by_symbol[sym]) < int(entry_gap_same_symbol_bars):
                continue
            if effective_reentry_gap is not None and sym in last_exit_ts_by_symbol and bars_diff(t, last_exit_ts_by_symbol[sym]) < int(effective_reentry_gap):
                continue
            candidates.append((idx, route, effective_max_per_symbol))
        if skip_dense_ts_threshold is not None and len(candidates) > int(skip_dense_ts_threshold): candidates=[]
        if loss_freeze_left > 0: loss_freeze_left -= 1; candidates=[]
        if dd_freeze_left > 0: dd_freeze_left -= 1; candidates=[]
        ranked=sorted(candidates, key=lambda x: ({'asia':0,'us':1,'fallback':2,'quiet':3}.get(x[1],9), -trades[x[0]].get('score',0.0)))
        final=[]; symbol_counts={}
        for p in active.values(): symbol_counts[p['symbol']] = symbol_counts.get(p['symbol'],0) + 1
        for idx, route, eff_max_per_symbol in ranked:
            if max_active_cap is not None and len(active)+len(final) >= int(max_active_cap): break
            sym=trades[idx]['symbol']; current_sym=symbol_counts.get(sym,0)+sum(1 for j,_,_ in final if trades[j]['symbol']==sym)
            if eff_max_per_symbol is not None and current_sym >= int(eff_max_per_symbol): continue
            final.append((idx, route, eff_max_per_symbol))
        selected_set={idx for idx,_,_ in final}
        for idx, _, _ in final:
            tr=trades[idx]; active[idx]={'notional': equity*float(position_fraction), 'entry_ts': tr['entry_ts'], 'symbol': tr['symbol'], 'side': tr['side']}; executed.add(idx); last_entry_ts_by_symbol[tr['symbol']] = pd.Timestamp(tr['entry_ts'])
        max_conc=max(max_conc, len(active)); max_conc_symbols=max(max_conc_symbols, len({p['symbol'] for p in active.values()}))
        for idx in same_bar_exit:
            if idx in selected_set: close_idx(idx)
    final_asset=equity; final_return=final_asset/float(initial_asset)-1.0; peak_growth=peak_asset/float(initial_asset)-1.0; pf=(gp/gl) if gl>0 else float('inf')
    return {'trades':len(executed),'final_asset':float(final_asset),'final_return':float(final_return),'peak_asset':float(peak_asset),'peak_growth':float(peak_growth),'win_rate':float(wins/len(executed)) if executed else 0.0,'pf':float(pf),'mdd':float(mdd),'max_conc':int(max_conc),'max_conc_unique_symbols':int(max_conc_symbols),'same_bar_trades':int(same_bar_trades),'active_leftover':int(len(active))}

if __name__ == '__main__':
    base=v56mod.v27mod.load_json(BASE); group=v56mod.v27mod.load_json(COMB); out=[]
    for exp in v56mod.v27mod.build_experiments(base, group):
        cfg=exp['effective_config']; name=exp['name']; data_dir=Path(v56mod.v27mod.os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir']))); out_dir=ROOT / cfg['results_dir'] / name; out_dir.mkdir(parents=True, exist_ok=True); all_trades=[]
        for p in sorted(data_dir.glob('*.csv')):
            df=v56mod.v27mod.load_df(p)
            if len(df) < int(cfg['min_bars']): continue
            all_trades.extend(v56mod.v27mod.generate_symbol_trades(p.stem, df, cfg))
        s=evaluate_router(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), cfg.get('trade_control', {}), cfg.get('router', {}))
        s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'effective_config':cfg,'engine_mode':'adaptive_short_router'})
        (out_dir/'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8'); print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment':name,'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc'],'max_conc_unique_symbols':s['max_conc_unique_symbols'],'same_bar_trades':s['same_bar_trades'],'active_leftover':s['active_leftover']})
    d=ROOT / base['results_dir']; d.mkdir(parents=True, exist_ok=True); v56mod.v27mod.pd.DataFrame(out).to_csv(d/'lane_summary.csv', index=False)
