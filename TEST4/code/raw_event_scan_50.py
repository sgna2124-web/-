import pandas as pd, numpy as np, glob, os
from collections import defaultdict

H = 12
FILES = sorted(glob.glob('/mnt/data/*_5m.csv'))

short_expansion_defs = {
    'E1': {'lookback':12,'range_thr':2.5,'close_loc_thr':0.70,'body_thr':None,'vol_thr':None},
    'E2': {'lookback':24,'range_thr':2.5,'close_loc_thr':0.70,'body_thr':None,'vol_thr':None},
    'E3': {'lookback':12,'range_thr':3.5,'close_loc_thr':0.85,'body_thr':None,'vol_thr':None},
    'E4': {'lookback':24,'range_thr':3.5,'close_loc_thr':0.85,'body_thr':None,'vol_thr':None},
    'E5': {'lookback':12,'range_thr':2.5,'close_loc_thr':0.70,'body_thr':2.5,'vol_thr':2.0},
}
long_expansion_defs = {
    'E1': {'lookback':12,'range_thr':2.5,'close_loc_thr':0.30,'body_thr':None,'vol_thr':None},
    'E2': {'lookback':24,'range_thr':2.5,'close_loc_thr':0.30,'body_thr':None,'vol_thr':None},
    'E3': {'lookback':12,'range_thr':3.5,'close_loc_thr':0.15,'body_thr':None,'vol_thr':None},
    'E4': {'lookback':24,'range_thr':3.5,'close_loc_thr':0.15,'body_thr':None,'vol_thr':None},
    'E5': {'lookback':12,'range_thr':2.5,'close_loc_thr':0.30,'body_thr':2.5,'vol_thr':2.0},
}
failure_defs = {
    'F1': {'k':3,'rule':'mid'},
    'F2': {'k':5,'rule':'mid'},
    'F3': {'k':3,'rule':'open'},
    'F4': {'k':5,'rule':'rangeback'},
    'F5': {'k':5,'rule':'quarter'},
}

def scan():
    stats = defaultdict(lambda: {'n':0,'sum_edge':0.0,'sum_mfe':0.0,'sum_mae':0.0,'wins':0,'tp1':0,'sl1':0,'sum_stop':0.0,'sum_abs':0.0})
    for f in FILES:
        sym = os.path.basename(f).replace('_5m.csv','')
        df = pd.read_csv(f)
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date','open','high','low','close','volume']].dropna().reset_index(drop=True)
        o,h,l,c,v = [df[x].to_numpy() for x in ['open','high','low','close','volume']]
        rng = np.maximum(h-l, 1e-12)
        body = np.abs(c-o)
        close_loc = (c-l)/rng
        prev_high_12 = pd.Series(h).shift(1).rolling(12).max().to_numpy()
        prev_low_12  = pd.Series(l).shift(1).rolling(12).min().to_numpy()
        prev_high_24 = pd.Series(h).shift(1).rolling(24).max().to_numpy()
        prev_low_24  = pd.Series(l).shift(1).rolling(24).min().to_numpy()
        rng_ma20  = pd.Series(rng).shift(1).rolling(20).mean().to_numpy()
        body_ma20 = pd.Series(body).shift(1).rolling(20).mean().replace(0,np.nan).to_numpy()
        vol_ma20  = pd.Series(v).shift(1).rolling(20).mean().replace(0,np.nan).to_numpy()
        rr20 = rng / rng_ma20
        br20 = body / body_ma20
        vr20 = v / vol_ma20

        def pack(k):
            return {
                'fut_max': pd.Series(h).shift(-1)[::-1].rolling(k, min_periods=k).max()[::-1].to_numpy(),
                'fut_min': pd.Series(l).shift(-1)[::-1].rolling(k, min_periods=k).min()[::-1].to_numpy(),
                'closek' : pd.Series(c).shift(-k).to_numpy(),
                'entry'  : pd.Series(o).shift(-(k+1)).to_numpy(),
                'fwdmax' : pd.Series(h).shift(-(k+1))[::-1].rolling(H, min_periods=H).max()[::-1].to_numpy(),
                'fwdmin' : pd.Series(l).shift(-(k+1))[::-1].rolling(H, min_periods=H).min()[::-1].to_numpy(),
                'closeH' : pd.Series(c).shift(-(k+H)).to_numpy(),
            }
        data_by_k = {3: pack(3), 5: pack(5)}

        for side, exp_defs in [('SHORT', short_expansion_defs), ('LONG', long_expansion_defs)]:
            for ei, e in exp_defs.items():
                lb = e['lookback']
                prev_high = prev_high_12 if lb==12 else prev_high_24
                prev_low  = prev_low_12 if lb==12 else prev_low_24
                if side == 'SHORT':
                    expansion = (c>o) & (rr20>=e['range_thr']) & (close_loc>=e['close_loc_thr']) & (h>prev_high)
                else:
                    expansion = (c<o) & (rr20>=e['range_thr']) & (close_loc<=e['close_loc_thr']) & (l<prev_low)
                if e['body_thr'] is not None:
                    expansion &= br20>=e['body_thr']
                if e['vol_thr'] is not None:
                    expansion &= vr20>=e['vol_thr']

                for fi, fd in failure_defs.items():
                    k = fd['k']
                    dd = data_by_k[k]
                    if side == 'SHORT':
                        no_follow = dd['fut_max'] <= h
                        if fd['rule']=='mid': fail = dd['closek'] < ((o+c)/2)
                        elif fd['rule']=='open': fail = dd['closek'] < o
                        elif fd['rule']=='rangeback': fail = dd['closek'] < prev_high
                        elif fd['rule']=='quarter': fail = dd['closek'] < (l + 0.25*rng)
                        entry = dd['entry']; stop = h; stop_dist = stop-entry
                        valid = expansion & no_follow & fail & np.isfinite(entry) & np.isfinite(dd['closeH']) & np.isfinite(dd['fwdmax']) & np.isfinite(dd['fwdmin']) & (stop_dist>0)
                        edge = ((dd['closeH']-entry)*-1.0)/stop_dist
                        mfe  = (entry-dd['fwdmin'])/stop_dist
                        mae  = (dd['fwdmax']-entry)/stop_dist
                    else:
                        no_follow = dd['fut_min'] >= l
                        if fd['rule']=='mid': fail = dd['closek'] > ((o+c)/2)
                        elif fd['rule']=='open': fail = dd['closek'] > o
                        elif fd['rule']=='rangeback': fail = dd['closek'] > prev_low
                        elif fd['rule']=='quarter': fail = dd['closek'] > (h - 0.25*rng)
                        entry = dd['entry']; stop = l; stop_dist = entry-stop
                        valid = expansion & no_follow & fail & np.isfinite(entry) & np.isfinite(dd['closeH']) & np.isfinite(dd['fwdmax']) & np.isfinite(dd['fwdmin']) & (stop_dist>0)
                        edge = ((dd['closeH']-entry)*1.0)/stop_dist
                        mfe  = (dd['fwdmax']-entry)/stop_dist
                        mae  = (entry-dd['fwdmin'])/stop_dist

                    name = f'{ei}_{fi}_{side}'
                    if valid.any():
                        st = stats[name]
                        st['n'] += int(valid.sum())
                        st['sum_edge'] += float(np.nansum(edge[valid]))
                        st['sum_mfe'] += float(np.nansum(mfe[valid]))
                        st['sum_mae'] += float(np.nansum(mae[valid]))
                        st['wins'] += int(np.sum(edge[valid] > 0))
                        st['tp1'] += int(np.sum(mfe[valid] >= 1))
                        st['sl1'] += int(np.sum(mae[valid] >= 1))
                        st['sum_stop'] += float(np.nansum(stop_dist[valid] / entry[valid]))
                        st['sum_abs'] += float(np.nansum(np.abs(dd['closeH'][valid]-entry[valid]) / entry[valid]))

    rows=[]
    for name, st in stats.items():
        n=st['n']
        rows.append({
            'event':name,
            'n':n,
            'edge_R12':st['sum_edge']/n,
            'mfe_R12':st['sum_mfe']/n,
            'mae_R12':st['sum_mae']/n,
            'mfe_minus_mae':(st['sum_mfe']-st['sum_mae'])/n,
            'win_rate_h12':st['wins']/n,
            'tp1_rate':st['tp1']/n,
            'sl1_rate':st['sl1']/n,
            'avg_stop_pct':st['sum_stop']/n,
            'avg_abs_ret_pct_h12':st['sum_abs']/n,
        })
    out = pd.DataFrame(rows).sort_values(['edge_R12','mfe_minus_mae','n'], ascending=[False,False,False]).reset_index(drop=True)
    out.to_csv('/mnt/data/raw_event_scan_50_results.csv', index=False)
    return out

if __name__ == '__main__':
    print(scan().head(20).to_string(index=False))
