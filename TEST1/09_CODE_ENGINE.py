import numpy as np
import pandas as pd

FEE_RATE = 0.0004
WINDOW = 1500
H_CANDIDATES = (12, 24, 48)
RR_DEFAULT = 3.1
MIN_SL_PCT = 0.3
BINS = 3
ALPHA = 10.0
P_MIN = 0.58
N_MIN = 40
MAE_Q = 0.8
SL_CAP_PCT = 1.2


def _rank01(x: np.ndarray) -> np.ndarray:
    s = pd.Series(x)
    out = s.rank(pct=True).to_numpy()
    return np.nan_to_num(out, nan=0.5)


def compute_feature_ranks(df_window: pd.DataFrame):
    c = df_window['close'].to_numpy(dtype=float)
    o = df_window['open'].to_numpy(dtype=float)
    h = df_window['high'].to_numpy(dtype=float)
    l = df_window['low'].to_numpy(dtype=float)
    prev_c = np.roll(c, 1)
    prev_c[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))
    atr = pd.Series(tr).rolling(14, min_periods=14).mean().to_numpy()
    atr_pct = (atr / c) * 100.0
    ret12 = pd.Series(c).pct_change(12).to_numpy() * 100.0
    rng = h - l
    rng_safe = np.where(rng == 0, np.nan, rng)
    upper = (h - np.maximum(o, c)) / rng_safe
    lower = (np.minimum(o, c) - l) / rng_safe
    wick_skew = upper - lower
    atr_rank = _rank01(atr_pct)
    mom_rank = _rank01(ret12)
    wick_rank = _rank01(wick_skew)
    return atr_rank, mom_rank, wick_rank


def bin3(a, b, c, bins=BINS):
    ia = int(min(bins - 1, max(0, np.floor(a * bins))))
    ib = int(min(bins - 1, max(0, np.floor(b * bins))))
    ic = int(min(bins - 1, max(0, np.floor(c * bins))))
    return (ia, ib, ic)


def make_triple_barrier_label(df: pd.DataFrame, idx: int, side: str, sl_pct: float, rr: float, H: int):
    entry = float(df.at[idx, 'close'])
    if not np.isfinite(entry) or entry <= 0:
        return None
    if side == 'long':
        sl = entry * (1.0 - sl_pct / 100.0)
        tp = entry * (1.0 + (sl_pct * rr) / 100.0)
    else:
        sl = entry * (1.0 + sl_pct / 100.0)
        tp = entry * (1.0 - (sl_pct * rr) / 100.0)
    end = min(len(df) - 1, idx + H)
    for j in range(idx + 1, end + 1):
        hi = float(df.at[j, 'high'])
        lo = float(df.at[j, 'low'])
        if side == 'long':
            hit_sl = lo <= sl
            hit_tp = hi >= tp
        else:
            hit_sl = hi >= sl
            hit_tp = lo <= tp
        if hit_sl and hit_tp:
            return 0
        if hit_sl:
            return 0
        if hit_tp:
            return 1
    close_end = float(df.at[end, 'close'])
    if side == 'long':
        return 1 if close_end > entry else 0
    return 1 if close_end < entry else 0


def compute_mae_pct(df: pd.DataFrame, idx: int, side: str, H: int):
    entry = float(df.at[idx, 'close'])
    if not np.isfinite(entry) or entry <= 0:
        return None
    end = min(len(df) - 1, idx + H)
    worst = 0.0
    if side == 'long':
        for j in range(idx + 1, end + 1):
            lo = float(df.at[j, 'low'])
            worst = max(worst, (entry - lo) / entry * 100.0)
    else:
        for j in range(idx + 1, end + 1):
            hi = float(df.at[j, 'high'])
            worst = max(worst, (hi - entry) / entry * 100.0)
    return worst


class RollingProbEngine:
    def __init__(self, bins=BINS, alpha=ALPHA, min_sl_pct=MIN_SL_PCT):
        self.bins = bins
        self.alpha = float(alpha)
        self.min_sl_pct = float(min_sl_pct)
        self.tbl = {}

    def update(self, key, is_win, mae_pct):
        if key not in self.tbl:
            self.tbl[key] = [0, 0, []]
        self.tbl[key][1] += 1
        if is_win:
            self.tbl[key][0] += 1
        if mae_pct is not None and np.isfinite(mae_pct):
            self.tbl[key][2].append(float(mae_pct))

    def count(self, key):
        if key not in self.tbl:
            return 0
        return int(self.tbl[key][1])

    def prob(self, key):
        if key not in self.tbl:
            return 0.5
        w, n, _ = self.tbl[key]
        a = self.alpha
        return (w + a) / (n + 2 * a)

    def adaptive_sl(self, key, q=MAE_Q, sl_cap_pct=SL_CAP_PCT):
        if key not in self.tbl:
            return self.min_sl_pct
        maes = self.tbl[key][2]
        if len(maes) < 5:
            return self.min_sl_pct
        arr = np.array(maes, dtype=float)
        arr = arr[np.isfinite(arr)]
        if len(arr) < 5:
            return self.min_sl_pct
        sl = float(np.quantile(arr, q))
        if not np.isfinite(sl):
            sl = self.min_sl_pct
        sl = max(self.min_sl_pct, sl)
        if sl_cap_pct is not None and sl_cap_pct > 0:
            sl = min(sl, float(sl_cap_pct))
        return sl


def build_engine_from_window(df_window: pd.DataFrame, side: str, rr: float, H: int):
    eng = RollingProbEngine()
    atr_rank, mom_rank, wick_rank = compute_feature_ranks(df_window)
    start = 60
    end = len(df_window) - H - 1
    if end <= start:
        return eng
    for k in range(start, end):
        key = bin3(atr_rank[k], mom_rank[k], wick_rank[k], bins=BINS)
        y = make_triple_barrier_label(df_window, k, side, sl_pct=MIN_SL_PCT, rr=rr, H=H)
        mae = compute_mae_pct(df_window, k, side, H)
        eng.update(key, is_win=(y == 1), mae_pct=mae)
    return eng


def decide_entry_best(df_window: pd.DataFrame, side: str, rr: float = RR_DEFAULT):
    atr_rank, mom_rank, wick_rank = compute_feature_ranks(df_window)
    i = len(df_window) - 1
    key_now = bin3(atr_rank[i], mom_rank[i], wick_rank[i], bins=BINS)
    best = {'enter': False, 'EV_pct': -1e9, 'H': None, 'P': 0.0, 'N': 0, 'SL_pct': None, 'TP_pct': None}
    fee_roundtrip_pct = (FEE_RATE * 2) * 100.0
    for H in H_CANDIDATES:
        eng = build_engine_from_window(df_window, side, rr, H)
        n = eng.count(key_now)
        if n < N_MIN:
            continue
        P = eng.prob(key_now)
        if P < P_MIN:
            continue
        sl_pct = eng.adaptive_sl(key_now, q=MAE_Q, sl_cap_pct=SL_CAP_PCT)
        tp_pct = sl_pct * rr
        ev = P * tp_pct - (1.0 - P) * sl_pct - fee_roundtrip_pct
        if ev > best['EV_pct']:
            best.update({'EV_pct': ev, 'H': H, 'P': P, 'N': n, 'SL_pct': sl_pct, 'TP_pct': tp_pct})
    best['enter'] = best['EV_pct'] > 0.0 and best['H'] is not None and best['SL_pct'] is not None
    return best
