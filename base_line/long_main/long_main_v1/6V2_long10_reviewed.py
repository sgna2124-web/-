from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed


BASELINE_CD_VALUE = {
    "long": 108.8106,
}

TIMEFRAME_LABEL = "5m"
BATCH_LABEL = "6V2_LONG10_REVIEWED"
ROUND_TRIP_COST_BPS = 10.0
MIN_BARS = 250
WARMUP_BARS = 120
DEFAULT_WORKERS = max(1, (os.cpu_count() or 2) - 1)
POSITION_FRACTION = 0.01
RUIN_THRESHOLD = 1e-12


SCRIPT_DIR = Path(__file__).resolve().parent
CWD = Path.cwd()


def find_repo_root() -> Path:
    candidates: List[Path] = []
    for base in [CWD, SCRIPT_DIR]:
        candidates.append(base)
        candidates.extend(list(base.parents))

    uniq: List[Path] = []
    seen = set()
    for p in candidates:
        s = str(p)
        if s not in seen:
            uniq.append(p)
            seen.add(s)

    for root in uniq:
        has_symbol_cost = (root / "symbol_cost").exists()
        has_data_dir = (root / "코인" / "Data" / "time").exists() or (root / "Data" / "time").exists()
        if has_symbol_cost and has_data_dir:
            return root

    for root in uniq:
        if (root / "symbol_cost").exists():
            return root

    return CWD


REPO_ROOT = find_repo_root()
if (REPO_ROOT / "코인" / "Data" / "time").exists():
    DATA_ROOT = REPO_ROOT / "코인" / "Data" / "time"
else:
    DATA_ROOT = REPO_ROOT / "Data" / "time"

SYMBOL_COST_PATH = REPO_ROOT / "symbol_cost"
RESULT_ROOT = REPO_ROOT / "local_results" / BATCH_LABEL
RESULT_ROOT.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class StrategySpec:
    name: str
    side: str
    description: str
    atr_stop: float
    rr_target: float
    max_hold_bars: int
    cooldown_bars: int


STRATEGIES: List[StrategySpec] = [
    StrategySpec("6V2_L01_doubleflush_core", "long", "cap reclaim + double flush core", 1.05, 2.50, 18, 18),
    StrategySpec("6V2_L02_doubleflush_trendfloor", "long", "double flush + trend floor", 1.05, 2.40, 16, 18),
    StrategySpec("6V2_L03_doubleflush_quiet", "long", "double flush + quiet regime", 1.00, 2.40, 16, 20),
    StrategySpec("6V2_L04_doubleflush_extremeclose", "long", "double flush + extreme close quality", 1.00, 2.60, 18, 20),
    StrategySpec("6V2_L05_doubleflush_secondpush", "long", "double flush + delayed second push", 1.00, 2.60, 16, 22),
    StrategySpec("6V2_L06_doubleflush_absorbbreak", "long", "double flush + absorb base break", 0.95, 2.60, 20, 22),
    StrategySpec("6V2_L07_absorb_reclaim_core", "long", "post shock absorb + reclaim break", 0.95, 2.40, 20, 24),
    StrategySpec("6V2_L08_quiet_reclaim_secondpush", "long", "quiet reclaim + second push", 1.00, 2.30, 16, 22),
    StrategySpec("6V2_L09_retest_hold_break", "long", "retest hold after reclaim", 1.00, 2.40, 18, 20),
    StrategySpec("6V2_L10_contraction_flush_break", "long", "double flush + contraction break", 0.95, 2.70, 20, 24),
]


@dataclass
class TradeRecord:
    entry_ts: int
    exit_ts: int
    pnl_pct: float
    hold_bars: int
    entry_price: float
    exit_price: float
    exit_reason: str


@dataclass
class SymbolSummary:
    symbol: str
    trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate_pct: float = 0.0
    final_return_pct: float = 0.0
    max_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    cd_value: float = 0.0


def log(msg: str) -> None:
    print(msg, flush=True)


def normalize_symbol_text(x: str) -> str:
    s = str(x).strip().upper()
    for ch in ["-", "_", "/", ":", " "]:
        s = s.replace(ch, "")
    return s


def infer_symbol_from_path(path: Path) -> str:
    stem = path.stem.upper().replace("-", "_")
    parts = stem.split("_")
    if len(parts) >= 2 and parts[-1] in {"1M", "3M", "5M", "15M", "30M", "1H", "4H", "1D"}:
        stem = "_".join(parts[:-1])
    stem = stem.replace("_PERP", "").replace("PERP", "")
    if "/USDT" not in stem and "USDT" in stem:
        stem = stem.replace("USDT", "/USDT")
    if "/BUSD" not in stem and "BUSD" in stem:
        stem = stem.replace("BUSD", "/BUSD")
    if "/USD" not in stem and stem.endswith("USD"):
        stem = stem.replace("USD", "/USD")
    while "__" in stem:
        stem = stem.replace("__", "_")
    return stem


def build_data_file_map(data_root: Path) -> Dict[str, Path]:
    if not data_root.exists():
        raise FileNotFoundError(f"데이터 폴더가 없습니다: {data_root}")

    mapping: Dict[str, Path] = {}
    for p in data_root.rglob("*.csv"):
        candidates = {
            normalize_symbol_text(p.stem),
            normalize_symbol_text(infer_symbol_from_path(p)),
        }
        for key in candidates:
            mapping.setdefault(key, p)

    if not mapping:
        raise FileNotFoundError(f"CSV 데이터 파일을 찾지 못했습니다: {data_root}")
    return mapping


def load_symbols(symbol_cost_path: Path, data_file_map: Dict[str, Path]) -> List[str]:
    symbols: List[str] = []

    if symbol_cost_path.is_file():
        if symbol_cost_path.suffix.lower() == ".json":
            data = json.loads(symbol_cost_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        symbols.append(item)
                    elif isinstance(item, dict):
                        s = item.get("symbol") or item.get("ticker") or item.get("name")
                        if s:
                            symbols.append(str(s))
        elif symbol_cost_path.suffix.lower() in {".csv", ".txt"}:
            try:
                df = pd.read_csv(symbol_cost_path)
                candidate_cols = [c for c in df.columns if str(c).lower() in {"symbol", "ticker", "name"}]
                if candidate_cols:
                    symbols = df[candidate_cols[0]].dropna().astype(str).tolist()
                else:
                    symbols = df.iloc[:, 0].dropna().astype(str).tolist()
            except Exception:
                text = symbol_cost_path.read_text(encoding="utf-8")
                symbols = [line.strip() for line in text.splitlines() if line.strip()]
    elif symbol_cost_path.is_dir():
        csvs = list(symbol_cost_path.rglob("*.csv"))
        jsons = list(symbol_cost_path.rglob("*.json"))
        txts = list(symbol_cost_path.rglob("*.txt"))
        preferred = csvs[:1] + jsons[:1] + txts[:1]
        if preferred:
            return load_symbols(preferred[0], data_file_map)

    if not symbols:
        inferred = sorted({infer_symbol_from_path(p) for p in data_file_map.values()})
        return inferred

    resolved: List[str] = []
    for s in symbols:
        key = normalize_symbol_text(s)
        if key in data_file_map:
            resolved.append(infer_symbol_from_path(data_file_map[key]))

    if resolved:
        return sorted(set(resolved))

    inferred = sorted({infer_symbol_from_path(p) for p in data_file_map.values()})
    return inferred


def resolve_symbol_path(symbol: str, data_file_map: Dict[str, Path]) -> Optional[Path]:
    return data_file_map.get(normalize_symbol_text(symbol))


def to_serializable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    if isinstance(obj, tuple):
        return [to_serializable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def rma(s: pd.Series, length: int) -> pd.Series:
    return s.ewm(alpha=1.0 / max(1, length), adjust=False).mean()


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return rma(tr, length).bfill().fillna(0.0)


def max_drawdown_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    peaks = np.maximum.accumulate(equity_curve)
    dd = (equity_curve / np.where(peaks == 0, 1.0, peaks) - 1.0) * 100.0
    return min(100.0, float(abs(np.min(dd))) if dd.size else 0.0)


def max_return_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    return float((np.max(equity_curve) - 1.0) * 100.0)


def cd_value_from_return_and_mdd(final_return_pct: float, max_drawdown_pct: float) -> float:
    base_after_mdd = 100.0 * (1.0 - max_drawdown_pct / 100.0)
    return base_after_mdd * (1.0 + final_return_pct / 100.0)


def equity_curve_from_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[np.ndarray, bool]:
    if not trade_pnls_pct:
        return np.array([1.0], dtype=np.float64), False

    eq = [1.0]
    cur = 1.0
    ruined = False

    for pnl_pct in trade_pnls_pct:
        step = 1.0 + (POSITION_FRACTION * (pnl_pct / 100.0))
        cur = cur * step
        eq.append(cur)
        if cur <= RUIN_THRESHOLD:
            ruined = True
            break

    return np.asarray(eq, dtype=np.float64), ruined


def summarize_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[float, float, float, float, bool]:
    eq, ruined = equity_curve_from_trade_pnls(trade_pnls_pct)
    final_return_pct = float((eq[-1] - 1.0) * 100.0) if eq.size else 0.0
    max_return_pct = max_return_pct_from_equity(eq)
    max_dd_pct = max_drawdown_pct_from_equity(eq)
    cd_value = cd_value_from_return_and_mdd(final_return_pct, max_dd_pct)
    return final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined


def standardize_ohlcv_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    cols = {str(c).lower(): c for c in df.columns}

    for low_name, target in [
        ("timestamp", "timestamp"),
        ("open_time", "timestamp"),
        ("time", "timestamp"),
        ("date", "timestamp"),
        ("datetime", "timestamp"),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("vol", "volume"),
    ]:
        if low_name in cols:
            rename_map[cols[low_name]] = target

    df = df.rename(columns=rename_map).copy()

    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"OHLCV 컬럼 누락: {missing}")

    df = df[required].copy()

    if not np.issubdtype(df["timestamp"].dtype, np.number):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        df["timestamp"] = (ts.astype("int64") // 10**9).astype("float64")

    for c in required:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna().copy()
    df = df.sort_values("timestamp").drop_duplicates("timestamp")
    df = df.reset_index(drop=True)
    return df


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    diff = series.diff().fillna(0.0)
    up = diff.clip(lower=0.0)
    down = (-diff).clip(lower=0.0)
    avg_up = rma(up, length)
    avg_down = rma(down, length)
    rs = avg_up / avg_down.replace(0, np.nan)
    out = 100.0 - (100.0 / (1.0 + rs))
    return out.fillna(50.0)


@dataclass
class FeaturePack:
    timestamp: np.ndarray
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray

    atr14: np.ndarray
    atrp: np.ndarray
    rsi14: np.ndarray

    ema20: np.ndarray
    ema50: np.ndarray
    ema100: np.ndarray

    vol_ratio: np.ndarray
    body_atr: np.ndarray
    close_pos: np.ndarray
    lower_wick_body_ratio: np.ndarray

    hh10: np.ndarray
    ll10: np.ndarray
    hh20: np.ndarray
    ll20: np.ndarray
    range_mid20: np.ndarray

    ret1: np.ndarray
    ret3: np.ndarray
    ret5: np.ndarray
    ret6: np.ndarray
    ret10: np.ndarray
    ret20: np.ndarray

    ema50_slope8: np.ndarray
    ema20_over_50: np.ndarray
    close_to_ema20: np.ndarray
    close_to_ema50: np.ndarray
    quiet_ratio: np.ndarray


def compute_features(df: pd.DataFrame) -> FeaturePack:
    c = df["close"]
    h = df["high"]
    l = df["low"]
    o = df["open"]
    v = df["volume"]

    atr14 = atr(df, 14)
    atrp = (atr14 / c.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    rsi14 = rsi(c, 14)

    ema20 = c.ewm(span=20, adjust=False).mean()
    ema50 = c.ewm(span=50, adjust=False).mean()
    ema100 = c.ewm(span=100, adjust=False).mean()

    vol_ma20 = v.rolling(20, min_periods=1).mean()
    vol_ratio = (v / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    body = (c - o).abs()
    lower_wick = pd.concat([o, c], axis=1).min(axis=1) - l
    body_atr = (body / atr14.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    bar_range = (h - l).replace(0, np.nan)
    close_pos = ((c - l) / bar_range).replace([np.inf, -np.inf], np.nan).fillna(0.5)
    lower_wick_body_ratio = (lower_wick / body.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    hh10 = h.rolling(10, min_periods=1).max()
    ll10 = l.rolling(10, min_periods=1).min()
    hh20 = h.rolling(20, min_periods=1).max()
    ll20 = l.rolling(20, min_periods=1).min()
    range_mid20 = ll20 + (hh20 - ll20) * 0.5

    ret1 = c.pct_change(1).fillna(0.0)
    ret3 = c.pct_change(3).fillna(0.0)
    ret5 = c.pct_change(5).fillna(0.0)
    ret6 = c.pct_change(6).fillna(0.0)
    ret10 = c.pct_change(10).fillna(0.0)
    ret20 = c.pct_change(20).fillna(0.0)

    ema50_slope8 = (ema50 / ema50.shift(8) - 1.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    ema20_over_50 = (ema20 / ema50 - 1.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    close_to_ema20 = (c / ema20 - 1.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    close_to_ema50 = (c / ema50 - 1.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    tr = pd.concat(
        [
            (h - l).abs(),
            (h - c.shift(1)).abs(),
            (l - c.shift(1)).abs(),
        ],
        axis=1,
    ).max(axis=1)
    tr_ema6 = tr.ewm(span=6, adjust=False).mean()
    tr_ema24 = tr.ewm(span=24, adjust=False).mean()
    quiet_ratio = (tr_ema6 / tr_ema24.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    return FeaturePack(
        timestamp=df["timestamp"].astype("int64").to_numpy(),
        open=o.to_numpy(dtype=np.float64),
        high=h.to_numpy(dtype=np.float64),
        low=l.to_numpy(dtype=np.float64),
        close=c.to_numpy(dtype=np.float64),
        volume=v.to_numpy(dtype=np.float64),
        atr14=atr14.to_numpy(dtype=np.float64),
        atrp=atrp.to_numpy(dtype=np.float64),
        rsi14=rsi14.to_numpy(dtype=np.float64),
        ema20=ema20.to_numpy(dtype=np.float64),
        ema50=ema50.to_numpy(dtype=np.float64),
        ema100=ema100.to_numpy(dtype=np.float64),
        vol_ratio=vol_ratio.to_numpy(dtype=np.float64),
        body_atr=body_atr.to_numpy(dtype=np.float64),
        close_pos=close_pos.to_numpy(dtype=np.float64),
        lower_wick_body_ratio=lower_wick_body_ratio.to_numpy(dtype=np.float64),
        hh10=hh10.to_numpy(dtype=np.float64),
        ll10=ll10.to_numpy(dtype=np.float64),
        hh20=hh20.to_numpy(dtype=np.float64),
        ll20=ll20.to_numpy(dtype=np.float64),
        range_mid20=range_mid20.to_numpy(dtype=np.float64),
        ret1=ret1.to_numpy(dtype=np.float64),
        ret3=ret3.to_numpy(dtype=np.float64),
        ret5=ret5.to_numpy(dtype=np.float64),
        ret6=ret6.to_numpy(dtype=np.float64),
        ret10=ret10.to_numpy(dtype=np.float64),
        ret20=ret20.to_numpy(dtype=np.float64),
        ema50_slope8=ema50_slope8.to_numpy(dtype=np.float64),
        ema20_over_50=ema20_over_50.to_numpy(dtype=np.float64),
        close_to_ema20=close_to_ema20.to_numpy(dtype=np.float64),
        close_to_ema50=close_to_ema50.to_numpy(dtype=np.float64),
        quiet_ratio=quiet_ratio.to_numpy(dtype=np.float64),
    )


def load_feature_pack(csv_path: Path) -> FeaturePack:
    df = pd.read_csv(csv_path)
    df = standardize_ohlcv_columns(df)
    return compute_features(df)


@dataclass
class RawSignals:
    l01_cap_reclaim: np.ndarray
    shock_down: np.ndarray
    extreme_reclaim: np.ndarray


def raw_l01_signal_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    bull_reclaim = (
        f.low[i] < ll20_prev
        and f.close[i] > ll20_prev
        and f.close[i] > f.open[i]
        and f.close_pos[i] > 0.70
    )
    return (
        (f.ret3[i] < -0.04 or f.ret5[i] < -0.06)
        and bull_reclaim
        and f.vol_ratio[i] > 1.40
        and f.body_atr[i] > 0.35
        and f.atrp[i] > 0.003
    )


def raw_shock_down_at(f: FeaturePack, i: int) -> bool:
    return (
        (f.ret3[i] <= -0.035 or f.ret5[i] <= -0.050)
        and f.vol_ratio[i] >= 1.10
        and f.body_atr[i] >= 0.25
    )


def raw_extreme_reclaim_at(f: FeaturePack, i: int) -> bool:
    return (
        raw_l01_signal_at(f, i)
        and f.close_pos[i] >= 0.80
        and f.lower_wick_body_ratio[i] >= 1.50
        and f.vol_ratio[i] >= 1.60
    )


def build_raw_signals(f: FeaturePack) -> RawSignals:
    n = len(f.close)
    l01_cap_reclaim = np.zeros(n, dtype=bool)
    shock_down = np.zeros(n, dtype=bool)
    extreme_reclaim = np.zeros(n, dtype=bool)
    start = max(WARMUP_BARS, 21)
    for i in range(start, n):
        l01_cap_reclaim[i] = raw_l01_signal_at(f, i)
        shock_down[i] = raw_shock_down_at(f, i)
        extreme_reclaim[i] = raw_extreme_reclaim_at(f, i)
    return RawSignals(
        l01_cap_reclaim=l01_cap_reclaim,
        shock_down=shock_down,
        extreme_reclaim=extreme_reclaim,
    )


def recent_true_indices(arr: np.ndarray, start_i: int, end_i: int) -> List[int]:
    start = max(0, start_i)
    end = max(start, end_i)
    return [j for j in range(start, end) if arr[j]]


def recent_signal_high(arr: np.ndarray, highs: np.ndarray, i: int, lookback: int) -> Optional[float]:
    idxs = recent_true_indices(arr, i - lookback, i)
    if not idxs:
        return None
    return float(max(highs[j] for j in idxs))


def recent_signal_low(arr: np.ndarray, lows: np.ndarray, i: int, lookback: int) -> Optional[float]:
    idxs = recent_true_indices(arr, i - lookback, i)
    if not idxs:
        return None
    return float(min(lows[j] for j in idxs))


def trend_floor_ok(f: FeaturePack, i: int, max_ema50_gap: float = -0.055, min_slope: float = -0.007, min_ret20: float = -0.14) -> bool:
    return (
        f.close_to_ema50[i] >= max_ema50_gap
        and f.ema50_slope8[i] >= min_slope
        and f.ret20[i] >= min_ret20
    )


def quiet_regime_ok(f: FeaturePack, i: int, max_quiet_ratio: float = 0.90, max_abs_ret6: float = 0.03) -> bool:
    return f.quiet_ratio[i] <= max_quiet_ratio and abs(f.ret6[i]) <= max_abs_ret6


def reclaim_quality_ok(f: FeaturePack, i: int, min_close_pos: float = 0.75, min_wick_ratio: float = 1.20) -> bool:
    return (
        f.close_pos[i] >= min_close_pos
        and f.lower_wick_body_ratio[i] >= min_wick_ratio
        and f.close[i] > f.open[i]
    )


def double_flush_ok(raw: RawSignals, f: FeaturePack, i: int, lookback: int = 10) -> bool:
    idxs = recent_true_indices(raw.shock_down, i - lookback, i - 1)
    if not idxs:
        return False
    ref_low = min(f.low[j] for j in idxs)
    return (
        f.low[i] <= ref_low * 1.003
        and reclaim_quality_ok(f, i, min_close_pos=0.75, min_wick_ratio=1.30)
    )


def delayed_secondpush_after_reclaim_ok(raw_arr: np.ndarray, f: FeaturePack, i: int, lookback: int = 2) -> bool:
    sig_high = recent_signal_high(raw_arr, f.high, i, lookback)
    if sig_high is None:
        return False
    return (
        f.close[i] > sig_high
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.60
        and f.body_atr[i] >= 0.20
    )


def postshock_absorb_break_ok(raw: RawSignals, f: FeaturePack, i: int) -> bool:
    idxs = recent_true_indices(raw.shock_down, i - 8, i - 1)
    if not idxs:
        return False
    shock_idx = idxs[-1]
    base_start = shock_idx + 1
    base_end = i - 1
    base_len = base_end - base_start + 1
    if base_len < 3 or base_len > 6:
        return False
    base_high = float(np.max(f.high[base_start:base_end + 1]))
    base_low = float(np.min(f.low[base_start:base_end + 1]))
    shock_range = max(1e-9, f.high[shock_idx] - f.low[shock_idx])
    return (
        base_low >= f.low[shock_idx] * 0.998
        and (base_high - base_low) <= shock_range * 0.55
        and f.close[i] > base_high
        and f.close[i] > f.open[i]
        and f.vol_ratio[i] >= 1.10
        and f.body_atr[i] >= 0.22
        and f.quiet_ratio[i] <= 0.95
    )


def absorb_after_reclaim_ok(raw: RawSignals, f: FeaturePack, i: int) -> bool:
    idxs = recent_true_indices(raw.l01_cap_reclaim, i - 6, i - 1)
    if not idxs:
        return False
    sig_idx = idxs[-1]
    base_start = sig_idx + 1
    base_end = i - 1
    base_len = base_end - base_start + 1
    if base_len < 2 or base_len > 5:
        return False
    base_high = float(np.max(f.high[base_start:base_end + 1]))
    base_low = float(np.min(f.low[base_start:base_end + 1]))
    sig_range = max(1e-9, f.high[sig_idx] - f.low[sig_idx])
    return (
        base_low >= f.low[sig_idx] * 0.998
        and (base_high - base_low) <= sig_range * 0.45
        and f.close[i] > base_high
        and f.close[i] > f.open[i]
        and f.vol_ratio[i] >= 1.05
        and f.quiet_ratio[i] <= 0.95
    )


def retest_hold_break_ok(raw: RawSignals, f: FeaturePack, i: int) -> bool:
    idxs = recent_true_indices(raw.l01_cap_reclaim, i - 4, i - 1)
    if not idxs:
        return False
    sig_idx = idxs[-1]
    sig_high = f.high[sig_idx]
    sig_low = f.low[sig_idx]
    recent_low = float(np.min(f.low[sig_idx + 1:i + 1])) if i > sig_idx + 1 else f.low[i]
    return (
        recent_low >= sig_low * 0.998
        and f.close[i] > sig_high
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.60
        and f.vol_ratio[i] >= 1.00
    )


def contraction_flush_break_ok(raw: RawSignals, f: FeaturePack, i: int) -> bool:
    if i < 4:
        return False
    if not double_flush_ok(raw, f, i, lookback=10):
        return False
    recent_high = float(np.max(f.high[i - 3:i]))
    recent_low = float(np.min(f.low[i - 3:i]))
    recent_range = recent_high - recent_low
    return (
        recent_range <= f.atr14[i] * 1.80
        and f.quiet_ratio[i] <= 0.90
        and f.close[i] > recent_high
        and f.close[i] > f.open[i]
        and f.vol_ratio[i] >= 1.05
    )


def entry_signal(spec: StrategySpec, f: FeaturePack, raw: RawSignals, i: int) -> bool:
    if i < max(WARMUP_BARS, 21):
        return False

    if spec.name == "6V2_L01_doubleflush_core":
        return raw.l01_cap_reclaim[i] and double_flush_ok(raw, f, i, lookback=10)

    if spec.name == "6V2_L02_doubleflush_trendfloor":
        return raw.l01_cap_reclaim[i] and double_flush_ok(raw, f, i, lookback=10) and trend_floor_ok(f, i)

    if spec.name == "6V2_L03_doubleflush_quiet":
        return (
            raw.l01_cap_reclaim[i]
            and double_flush_ok(raw, f, i, lookback=10)
            and quiet_regime_ok(f, i, max_quiet_ratio=0.90, max_abs_ret6=0.03)
        )

    if spec.name == "6V2_L04_doubleflush_extremeclose":
        return raw.extreme_reclaim[i] and double_flush_ok(raw, f, i, lookback=10)

    if spec.name == "6V2_L05_doubleflush_secondpush":
        ref_low = recent_signal_low(raw.shock_down, f.low, i, 10)
        return (
            delayed_secondpush_after_reclaim_ok(raw.l01_cap_reclaim, f, i, lookback=2)
            and ref_low is not None
            and f.low[i] >= ref_low * 0.998
            and trend_floor_ok(f, i, max_ema50_gap=-0.070, min_slope=-0.010, min_ret20=-0.18)
        )

    if spec.name == "6V2_L06_doubleflush_absorbbreak":
        return absorb_after_reclaim_ok(raw, f, i) and trend_floor_ok(f, i, max_ema50_gap=-0.070, min_slope=-0.010, min_ret20=-0.18)

    if spec.name == "6V2_L07_absorb_reclaim_core":
        return postshock_absorb_break_ok(raw, f, i) and f.close[i] > f.ema20[i]

    if spec.name == "6V2_L08_quiet_reclaim_secondpush":
        return (
            delayed_secondpush_after_reclaim_ok(raw.l01_cap_reclaim, f, i, lookback=2)
            and quiet_regime_ok(f, i, max_quiet_ratio=0.85, max_abs_ret6=0.025)
            and f.close[i] > f.ema20[i]
        )

    if spec.name == "6V2_L09_retest_hold_break":
        return retest_hold_break_ok(raw, f, i) and quiet_regime_ok(f, i, max_quiet_ratio=0.95, max_abs_ret6=0.04)

    if spec.name == "6V2_L10_contraction_flush_break":
        return contraction_flush_break_ok(raw, f, i)

    return False


def backtest_symbol_strategy(symbol: str, f: FeaturePack, spec: StrategySpec) -> Tuple[SymbolSummary, List[Tuple[int, float]]]:
    n = len(f.close)
    if n < MIN_BARS:
        return SymbolSummary(symbol=symbol), []

    raw = build_raw_signals(f)

    in_pos = False
    entry_price = 0.0
    entry_ts = 0
    stop_price = 0.0
    target_price = 0.0
    hold_bars = 0
    cooldown = 0

    trades: List[TradeRecord] = []

    for i in range(max(WARMUP_BARS, 21), n):
        px_high = float(f.high[i])
        px_low = float(f.low[i])
        px_close = float(f.close[i])
        ts = int(f.timestamp[i])
        atr14 = max(1e-9, float(f.atr14[i]))

        if in_pos:
            hold_bars += 1
            exit_price: Optional[float] = None
            exit_reason = ""

            hit_stop = px_low <= stop_price
            hit_target = px_high >= target_price

            if hit_stop and hit_target:
                exit_price = stop_price
                exit_reason = "both_hit_stop_first"
            elif hit_stop:
                exit_price = stop_price
                exit_reason = "stop"
            elif hit_target:
                exit_price = target_price
                exit_reason = "target"
            elif hold_bars >= spec.max_hold_bars:
                exit_price = px_close
                exit_reason = "time"

            if exit_price is not None:
                gross_pct = ((exit_price - entry_price) / max(1e-9, entry_price)) * 100.0
                net_pct = gross_pct - (ROUND_TRIP_COST_BPS / 100.0)
                trades.append(
                    TradeRecord(
                        entry_ts=entry_ts,
                        exit_ts=ts,
                        pnl_pct=float(net_pct),
                        hold_bars=hold_bars,
                        entry_price=float(entry_price),
                        exit_price=float(exit_price),
                        exit_reason=exit_reason,
                    )
                )
                in_pos = False
                cooldown = spec.cooldown_bars
                hold_bars = 0
                continue

        if not in_pos:
            if cooldown > 0:
                cooldown -= 1
                continue

            if entry_signal(spec, f, raw, i):
                entry_price = px_close
                entry_ts = ts
                risk_distance = spec.atr_stop * atr14
                stop_price = entry_price - risk_distance
                target_price = entry_price + (risk_distance * spec.rr_target)
                if stop_price <= 0 or target_price <= 0:
                    continue
                in_pos = True
                hold_bars = 0

    trade_pnls = [t.pnl_pct for t in trades]
    final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined = summarize_trade_pnls(trade_pnls)

    wins = sum(1 for t in trades if t.pnl_pct > 0)
    losses = sum(1 for t in trades if t.pnl_pct <= 0)
    win_rate_pct = (wins / len(trades) * 100.0) if trades else 0.0

    if ruined:
        max_dd_pct = 100.0

    summary = SymbolSummary(
        symbol=symbol,
        trades=len(trades),
        wins=wins,
        losses=losses,
        win_rate_pct=float(win_rate_pct),
        final_return_pct=float(final_return_pct),
        max_return_pct=float(max_return_pct),
        max_drawdown_pct=float(max_dd_pct),
        cd_value=float(cd_value),
    )
    compact_trades = [(t.exit_ts, t.pnl_pct) for t in trades]
    return summary, compact_trades


def evaluate_strategy_for_symbol(symbol: str, csv_path: Path, spec: StrategySpec) -> Tuple[SymbolSummary, List[Tuple[int, float]]]:
    try:
        f = load_feature_pack(csv_path)
        return backtest_symbol_strategy(symbol, f, spec)
    except Exception:
        return SymbolSummary(symbol=symbol), []


def aggregate_strategy_result(spec: StrategySpec, per_symbol: List[SymbolSummary], trades: List[Tuple[int, float]]) -> Dict[str, Any]:
    all_trade_pnls = [pnl for _, pnl in sorted(trades, key=lambda x: x[0])]
    final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined = summarize_trade_pnls(all_trade_pnls)

    total_trades = sum(x.trades for x in per_symbol)
    total_wins = sum(x.wins for x in per_symbol)
    total_losses = sum(x.losses for x in per_symbol)
    win_rate_pct = (total_wins / total_trades * 100.0) if total_trades else 0.0

    baseline_cd = BASELINE_CD_VALUE[spec.side]
    if max_dd_pct > 5.0:
        verdict = "mdd_fail"
    elif cd_value >= baseline_cd:
        verdict = "baseline_win"
    else:
        verdict = "baseline_fail"

    return {
        "batch_label": BATCH_LABEL,
        "strategy_name": spec.name,
        "side": spec.side,
        "description": spec.description,
        "timeframe": TIMEFRAME_LABEL,
        "processed_symbols": len(per_symbol),
        "trades": total_trades,
        "wins": total_wins,
        "losses": total_losses,
        "win_rate_pct": float(win_rate_pct),
        "final_return_pct": float(final_return_pct),
        "max_return_pct": float(max_return_pct),
        "max_drawdown_pct": float(max_dd_pct),
        "cd_value": float(cd_value),
        "baseline_cd_value": float(baseline_cd),
        "ruined": bool(ruined),
        "verdict": verdict,
    }


def print_strategy_summary_line(summary: Dict[str, Any]) -> None:
    log(
        f"{summary['strategy_name']} | side={summary['side']} | trades={summary['trades']} | "
        f"win_rate={summary['win_rate_pct']:.2f}% | final={summary['final_return_pct']:.4f}% | "
        f"max={summary['max_return_pct']:.4f}% | mdd={summary['max_drawdown_pct']:.4f}% | "
        f"cd={summary['cd_value']:.4f} | verdict={summary['verdict']}"
    )


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(to_serializable(obj), ensure_ascii=False, indent=2), encoding="utf-8")


def save_strategy_outputs(spec: StrategySpec, summary: Dict[str, Any], per_symbol: List[SymbolSummary]) -> None:
    out_dir = RESULT_ROOT / spec.name
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_path = out_dir / "summary.json"
    per_symbol_path = out_dir / "per_symbol_summary.json"
    registry_path = out_dir / "registry.json"

    per_symbol_dicts = [asdict(x) for x in sorted(per_symbol, key=lambda x: (x.cd_value, x.final_return_pct), reverse=True)]

    registry = {
        "batch_label": BATCH_LABEL,
        "strategy_name": spec.name,
        "side": spec.side,
        "description": spec.description,
        "timeframe": TIMEFRAME_LABEL,
        "summary_file": str(summary_path.name),
        "per_symbol_file": str(per_symbol_path.name),
        "summary": summary,
    }

    save_json(summary_path, summary)
    save_json(per_symbol_path, per_symbol_dicts)
    save_json(registry_path, registry)


def save_batch_registry(summaries: List[Dict[str, Any]]) -> None:
    reg_csv = RESULT_ROOT / f"{BATCH_LABEL}_registry.csv"
    reg_json = RESULT_ROOT / f"{BATCH_LABEL}_registry.json"
    master_summary = RESULT_ROOT / "master_summary.txt"

    df = pd.DataFrame(summaries).sort_values(["cd_value", "final_return_pct"], ascending=[False, False])
    df.to_csv(reg_csv, index=False, encoding="utf-8-sig")
    save_json(reg_json, df.to_dict(orient="records"))

    lines: List[str] = []
    lines.append(f"batch={BATCH_LABEL}")
    lines.append(f"timeframe={TIMEFRAME_LABEL}")
    lines.append("")
    for _, row in df.iterrows():
        lines.append(
            f"{row['strategy_name']} | verdict={row['verdict']} | final_return_pct={row['final_return_pct']:.4f} | "
            f"max_return_pct={row['max_return_pct']:.4f} | max_drawdown_pct={row['max_drawdown_pct']:.4f} | "
            f"cd_value={row['cd_value']:.4f} | trades={int(row['trades'])}"
        )
    master_summary.write_text("\n".join(lines), encoding="utf-8")


def run_strategy_single(spec: StrategySpec, symbols: List[str], data_file_map: Dict[str, str]) -> Tuple[StrategySpec, Dict[str, Any], List[SymbolSummary]]:
    per_symbol: List[SymbolSummary] = []
    compact_trades: List[Tuple[int, float]] = []

    for symbol in symbols:
        csv_path_str = data_file_map.get(symbol)
        if not csv_path_str:
            continue
        csv_path = Path(csv_path_str)
        summary, trades = evaluate_strategy_for_symbol(symbol, csv_path, spec)
        per_symbol.append(summary)
        compact_trades.extend(trades)

    summary_dict = aggregate_strategy_result(spec, per_symbol, compact_trades)
    return spec, summary_dict, per_symbol


def main() -> None:
    started = time.time()
    log(f"repo_root={REPO_ROOT}")
    log(f"data_root={DATA_ROOT}")
    log(f"result_root={RESULT_ROOT}")

    data_file_map_raw = build_data_file_map(DATA_ROOT)
    symbols = load_symbols(SYMBOL_COST_PATH, data_file_map_raw)
    if not symbols:
        raise RuntimeError("대상 심볼 목록이 비어 있습니다.")

    resolved_symbols: List[str] = []
    worker_file_map: Dict[str, str] = {}
    for s in symbols:
        p = resolve_symbol_path(s, data_file_map_raw)
        if p is None:
            continue
        canonical_symbol = infer_symbol_from_path(p)
        resolved_symbols.append(canonical_symbol)
        worker_file_map[canonical_symbol] = str(p)

    resolved_symbols = sorted(set(resolved_symbols))
    if not resolved_symbols:
        raise RuntimeError("실제 CSV 경로가 매칭되는 심볼이 없습니다.")

    log(f"symbols={len(resolved_symbols)} | strategies={len(STRATEGIES)}")

    summaries: List[Dict[str, Any]] = []
    workers = min(DEFAULT_WORKERS, max(1, len(STRATEGIES)))

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(run_strategy_single, spec, resolved_symbols, worker_file_map) for spec in STRATEGIES]
        for fut in as_completed(futures):
            spec, summary_dict, per_symbol = fut.result()
            print_strategy_summary_line(summary_dict)
            save_strategy_outputs(spec, summary_dict, per_symbol)
            summaries.append(summary_dict)

    summaries = sorted(summaries, key=lambda x: (-x["cd_value"], -x["final_return_pct"]))
    save_batch_registry(summaries)

    elapsed = time.time() - started
    log(f"done | strategies={len(summaries)} | elapsed_sec={elapsed:.2f}")


if __name__ == "__main__":
    main()
