# AUTO-GENERATED PATCHED RUNNER V3
# target=8V4_V51_V002_core_rare22_c1
# batch_label=RESTORE_EXACT_8V4_V51_V002_FEE008_V4
# repo_root=C:\Users\user\Desktop\LCD\파이썬\코인
# data_root=C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
# symbol_cost_path=C:\Users\user\Desktop\LCD\파이썬\symbol_cost
# sequential=True

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

# ---- injected stable sequential executor for Windows/local restore ----
class _ImmediateFuture:
    def __init__(self, fn, *args, **kwargs):
        self._result = None
        self._exc = None
        try:
            self._result = fn(*args, **kwargs)
        except BaseException as exc:
            self._exc = exc

    def result(self):
        if self._exc is not None:
            raise self._exc
        return self._result


class ProcessPoolExecutor:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def submit(self, fn, *args, **kwargs):
        return _ImmediateFuture(fn, *args, **kwargs)


def as_completed(futures):
    return list(futures)
# ----------------------------------------------------------------------

BASELINE_CD_VALUE = {
    "long": 121.5300,
}
TIMEFRAME_LABEL = "5m"
BATCH_LABEL = 'RESTORE_EXACT_8V4_V51_V002_FEE008_V4'
ROUND_TRIP_COST_BPS = 8.0
MIN_BARS = 250
WARMUP_BARS = 120
DEFAULT_WORKERS = 1
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

# ---- injected fixed paths ----
REPO_ROOT = Path('C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인')
DATA_ROOT = Path('C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인\\Data\\time')
SYMBOL_COST_PATH = Path('C:\\Users\\user\\Desktop\\LCD\\파이썬\\symbol_cost')
RESULT_ROOT = REPO_ROOT / "local_results" / 'RESTORE_EXACT_8V4_V51_V002_FEE008_V4'
RESULT_ROOT.mkdir(parents=True, exist_ok=True)
print(f"[PATHS] REPO_ROOT={REPO_ROOT}", flush=True)
print(f"[PATHS] DATA_ROOT={DATA_ROOT}", flush=True)
print(f"[PATHS] SYMBOL_COST_PATH={SYMBOL_COST_PATH} exists={SYMBOL_COST_PATH.exists()}", flush=True)
print(f"[PATHS] RESULT_ROOT={RESULT_ROOT}", flush=True)
# ------------------------------

@dataclass(frozen=True)
class StrategySpec:
    name: str
    side: str
    description: str
    atr_stop: float
    rr_target: float
    max_hold_bars: int
    cooldown_bars: int

FAMILY_SEEDS = {
    "V51": {"label": "microbase_pop", "desc": "l09 v51 microbase pop"},
    "V27": {"label": "failed_break_pivot", "desc": "l09 v27 failed break pivot"},
    "V09": {"label": "cluster_pressure", "desc": "l09 v09 cluster pressure"},
    "V28": {"label": "refire_block", "desc": "l09 v28 refire block"},
}
ANCHOR_TAGS = [
    ("core", "core"),
    ("strict", "strict"),
    ("lowanchor", "lowanchor"),
    ("shocklow", "shocklow"),
    ("prevhigh", "prevhigh"),
    ("extreme", "extreme"),
    ("spring", "spring"),
    ("ema_mid", "ema_mid"),
    ("hammer_outside", "hammer_outside"),
    ("quality_hold", "quality_hold"),
]
GUARD_TAGS = [
    ("base", "base"),
    ("rare22_c1", "rare22_c1"),
    ("rare28_first", "rare28_first"),
    ("vol18", "vol18"),
    ("vol16_quiet", "vol16_quiet"),
    ("noshock14", "noshock14"),
    ("refire40", "refire40"),
    ("softscore", "softscore"),
    ("microguard", "microguard"),
    ("shortgap", "shortgap"),
]
def family_risk_profile(seed: str, a_idx: int, g_idx: int) -> Tuple[float, float, int, int]:
    seed_base = {
        "V51": (0.92, 2.50, 18, 24),
        "V27": (0.97, 2.60, 20, 26),
        "V09": (0.95, 2.55, 20, 28),
        "V28": (0.94, 2.50, 18, 26),
    }[seed]
    atr, rr, hold, cool = seed_base
    atr += (a_idx % 3) * 0.03
    rr += (g_idx % 4) * 0.05
    hold += (a_idx // 3)
    cool += g_idx
    return float(round(atr, 2)), float(round(rr, 2)), int(hold), int(cool)
def build_family_variants() -> Dict[str, List[Tuple[str, float, float, int, int, str]]]:
    out: Dict[str, List[Tuple[str, float, float, int, int, str]]] = {}
    for seed, meta in FAMILY_SEEDS.items():
        rows: List[Tuple[str, float, float, int, int, str]] = []
        for a_idx, (a_code, a_desc) in enumerate(ANCHOR_TAGS, start=1):
            for g_idx, (g_code, g_desc) in enumerate(GUARD_TAGS, start=1):
                variant_no = (a_idx - 1) * len(GUARD_TAGS) + g_idx
                name = f"8V4_{seed}_V{variant_no:03d}_{a_code}_{g_code}"
                atr, rr, hold, cool = family_risk_profile(seed, a_idx - 1, g_idx - 1)
                desc = f"{meta['desc']} + {a_desc} + {g_desc}"
                rows.append((name, atr, rr, hold, cool, desc))
        out[seed] = rows
    return out
FAMILY_VARIANTS = build_family_variants()

STRATEGY_META: Dict[str, Tuple[str, int]] = {}
STRATEGIES: List[StrategySpec] = []
for family, items in FAMILY_VARIANTS.items():
    for idx, (name, atr_stop, rr, max_hold, cooldown_bars, desc) in enumerate(items, start=1):
        STRATEGY_META[name] = (family, idx)
        STRATEGIES.append(
            StrategySpec(name, "long", desc, atr_stop, rr, max_hold, cooldown_bars)
        )
FAMILY_INDEXED_NAMES: Dict[str, List[str]] = {
    family: [name for name, *_rest in items] for family, items in FAMILY_VARIANTS.items()
}
STRATEGIES: List[StrategySpec] = []
for family, items in FAMILY_VARIANTS.items():
    for idx, (name, atr_stop, rr, max_hold, cooldown_bars, desc) in enumerate(items, start=1):
        STRATEGY_META[name] = (family, idx)
        STRATEGIES.append(
            StrategySpec(name, "long", desc, atr_stop, rr, max_hold, cooldown_bars)
        )

# ---- injected target strategy filter ----
_TARGET_STRATEGY_NAME = '8V4_V51_V002_core_rare22_c1'
STRATEGIES = [s for s in STRATEGIES if getattr(s, "name", None) == _TARGET_STRATEGY_NAME]
if len(STRATEGIES) != 1:
    raise RuntimeError(f"target strategy filter failed: {_TARGET_STRATEGY_NAME} / remaining={[getattr(s, 'name', None) for s in STRATEGIES]}")
print(f"[TARGET_ONLY] {STRATEGIES[0].name} | {STRATEGIES[0].description} | atr_stop={STRATEGIES[0].atr_stop} | rr={STRATEGIES[0].rr_target} | hold={STRATEGIES[0].max_hold_bars} | cooldown={STRATEGIES[0].cooldown_bars}", flush=True)
# ---------------------------------------

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
    spring_undercut: np.ndarray
    hammer_flush: np.ndarray
    beartrap_midflip: np.ndarray
    engulf_panic: np.ndarray
    outside_flush_reversal: np.ndarray
    deep_ema20_retake: np.ndarray
    climax_wick_reclaim: np.ndarray
    rangefloor_pop: np.ndarray
    beartrap_close_drive: np.ndarray
    shock_reversal_balance: np.ndarray
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
def raw_spring_undercut_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll10_prev = f.ll10[i - 1]
    return (
        (f.ret3[i] <= -0.022 or f.ret5[i] <= -0.035)
        and f.low[i] < ll10_prev
        and f.close[i] > ll10_prev
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.68
        and f.lower_wick_body_ratio[i] >= 1.00
        and f.vol_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.18
    )
def raw_hammer_flush_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    return (
        (f.ret3[i] <= -0.025 or f.ret5[i] <= -0.040)
        and f.low[i] <= ll20_prev * 1.003
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.78
        and f.lower_wick_body_ratio[i] >= 1.80
        and f.vol_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.16
    )
def raw_beartrap_midflip_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    prev_mid = f.range_mid20[i - 1]
    return (
        f.ret10[i] <= -0.030
        and f.low[i] < ll20_prev
        and f.close[i] > prev_mid
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.72
        and f.body_atr[i] >= 0.22
        and f.vol_ratio[i] >= 1.00
    )
def raw_engulf_panic_at(f: FeaturePack, i: int) -> bool:
    if i < 22:
        return False
    prev_bear = f.close[i - 1] < f.open[i - 1]
    prev_body = abs(f.close[i - 1] - f.open[i - 1]) / max(1e-9, f.atr14[i])
    return (
        f.ret5[i] <= -0.035
        and prev_bear
        and prev_body >= 0.20
        and f.close[i] > f.open[i]
        and f.open[i] <= f.close[i - 1] * 1.003
        and f.close[i] >= f.open[i - 1] * 0.998
        and f.close_pos[i] >= 0.70
        and f.vol_ratio[i] >= 1.05
        and f.body_atr[i] >= 0.24
    )
def raw_outside_flush_reversal_at(f: FeaturePack, i: int) -> bool:
    if i < 22:
        return False
    return (
        f.ret3[i] <= -0.020
        and f.low[i] < f.low[i - 1]
        and f.high[i] > f.high[i - 1]
        and f.close[i] > f.high[i - 1] * 0.998
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.75
        and f.vol_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.20
    )
def raw_deep_ema20_retake_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    return (
        f.ret10[i] <= -0.030
        and f.low[i] <= f.ema20[i] * 0.985
        and f.close[i] > f.ema20[i]
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.72
        and f.vol_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.18
    )
def raw_climax_wick_reclaim_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll10_prev = f.ll10[i - 1]
    return (
        (f.ret1[i] <= -0.015 or f.ret3[i] <= -0.030)
        and f.low[i] <= ll10_prev * 1.003
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.80
        and f.lower_wick_body_ratio[i] >= 1.50
        and f.vol_ratio[i] >= 1.40
        and f.body_atr[i] >= 0.18
    )
def raw_rangefloor_pop_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    return (
        f.ret20[i] <= -0.020
        and f.low[i] <= ll20_prev * 1.002
        and f.close[i] > f.range_mid20[i]
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.70
        and f.vol_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.22
    )
def raw_beartrap_close_drive_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    return (
        f.ret5[i] <= -0.030
        and f.low[i] < ll20_prev
        and f.close[i] > ll20_prev
        and f.close[i] > f.close[i - 1]
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.82
        and f.vol_ratio[i] >= 1.15
        and f.body_atr[i] >= 0.28
    )
def raw_shock_reversal_balance_at(raw: RawSignals, f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    idxs = recent_true_indices(raw.shock_down, i - 6, i)
    if not idxs:
        return False
    ref_low = min(f.low[j] for j in idxs)
    return (
        f.low[i] <= ref_low * 1.006
        and f.close[i] > ref_low
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.72
        and f.vol_ratio[i] >= 0.95
        and f.body_atr[i] >= 0.20
    )
def build_raw_signals(f: FeaturePack) -> RawSignals:
    n = len(f.close)
    l01_cap_reclaim = np.zeros(n, dtype=bool)
    shock_down = np.zeros(n, dtype=bool)
    extreme_reclaim = np.zeros(n, dtype=bool)
    spring_undercut = np.zeros(n, dtype=bool)
    hammer_flush = np.zeros(n, dtype=bool)
    beartrap_midflip = np.zeros(n, dtype=bool)
    engulf_panic = np.zeros(n, dtype=bool)
    outside_flush_reversal = np.zeros(n, dtype=bool)
    deep_ema20_retake = np.zeros(n, dtype=bool)
    climax_wick_reclaim = np.zeros(n, dtype=bool)
    rangefloor_pop = np.zeros(n, dtype=bool)
    beartrap_close_drive = np.zeros(n, dtype=bool)
    shock_reversal_balance = np.zeros(n, dtype=bool)
    start = max(WARMUP_BARS, 21)
    for i in range(start, n):
        l01_cap_reclaim[i] = raw_l01_signal_at(f, i)
        shock_down[i] = raw_shock_down_at(f, i)
        extreme_reclaim[i] = raw_extreme_reclaim_at(f, i)
        spring_undercut[i] = raw_spring_undercut_at(f, i)
        hammer_flush[i] = raw_hammer_flush_at(f, i)
        beartrap_midflip[i] = raw_beartrap_midflip_at(f, i)
        engulf_panic[i] = raw_engulf_panic_at(f, i)
        outside_flush_reversal[i] = raw_outside_flush_reversal_at(f, i)
        deep_ema20_retake[i] = raw_deep_ema20_retake_at(f, i)
        climax_wick_reclaim[i] = raw_climax_wick_reclaim_at(f, i)
        rangefloor_pop[i] = raw_rangefloor_pop_at(f, i)
        beartrap_close_drive[i] = raw_beartrap_close_drive_at(f, i)
        shock_reversal_balance[i] = raw_shock_reversal_balance_at(
            RawSignals(
                l01_cap_reclaim=l01_cap_reclaim,
                shock_down=shock_down,
                extreme_reclaim=extreme_reclaim,
                spring_undercut=spring_undercut,
                hammer_flush=hammer_flush,
                beartrap_midflip=beartrap_midflip,
                engulf_panic=engulf_panic,
                outside_flush_reversal=outside_flush_reversal,
                deep_ema20_retake=deep_ema20_retake,
                climax_wick_reclaim=climax_wick_reclaim,
                rangefloor_pop=rangefloor_pop,
                beartrap_close_drive=beartrap_close_drive,
                shock_reversal_balance=shock_reversal_balance,
            ),
            f,
            i,
        )
    return RawSignals(
        l01_cap_reclaim=l01_cap_reclaim,
        shock_down=shock_down,
        extreme_reclaim=extreme_reclaim,
        spring_undercut=spring_undercut,
        hammer_flush=hammer_flush,
        beartrap_midflip=beartrap_midflip,
        engulf_panic=engulf_panic,
        outside_flush_reversal=outside_flush_reversal,
        deep_ema20_retake=deep_ema20_retake,
        climax_wick_reclaim=climax_wick_reclaim,
        rangefloor_pop=rangefloor_pop,
        beartrap_close_drive=beartrap_close_drive,
        shock_reversal_balance=shock_reversal_balance,
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
def low_vs_low20_now(f: FeaturePack, i: int) -> float:
    base = f.ll20[i] if f.ll20[i] > 0 else f.low[i]
    if base == 0:
        return 0.0
    return float(f.low[i] / base - 1.0)
def no_recent_signal(arr: np.ndarray, i: int, bars: int) -> bool:
    return len(recent_true_indices(arr, i - bars, i)) == 0
def recent_shock_age(raw: RawSignals, i: int, lookback: int = 12) -> Optional[int]:
    idxs = recent_true_indices(raw.shock_down, i - lookback, i)
    if not idxs:
        return None
    return i - idxs[-1]
def volatility_soft_point(f: FeaturePack, i: int, lookback: int = 20) -> int:
    if i < lookback:
        return 0
    recent = f.atrp[i - lookback:i]
    if recent.size == 0:
        return 0
    recent_max = float(np.max(recent))
    recent_med = float(np.median(recent))
    ok = f.atrp[i] <= recent_max * 0.99 and f.atrp[i] >= recent_med * 0.70
    return int(ok)
def oversold_soft_point(f: FeaturePack, i: int) -> int:
    return int(-0.22 <= f.ret20[i] <= -0.01 and f.close_to_ema50[i] >= -0.16)
def recovery_soft_point(f: FeaturePack, i: int) -> int:
    return int(f.close[i] > f.ema20[i] or (f.close[i] > f.open[i] and f.close_pos[i] >= 0.70))
def trendfloor_soft_point(f: FeaturePack, i: int) -> int:
    return int(f.close_to_ema50[i] >= -0.10 and f.ema50_slope8[i] >= -0.015 and f.ret20[i] >= -0.20)
def shockfresh_soft_point(raw: RawSignals, i: int) -> int:
    age = recent_shock_age(raw, i, lookback=10)
    return int(age is not None and 0 <= age <= 6)
def reclaim_soft_point(f: FeaturePack, i: int) -> int:
    return int(f.close_pos[i] >= 0.72 and f.lower_wick_body_ratio[i] >= 0.90)
def volume_soft_point(f: FeaturePack, i: int) -> int:
    return int(f.vol_ratio[i] >= 1.00 and f.body_atr[i] >= 0.18)
def location_soft_point(f: FeaturePack, i: int) -> int:
    return int(low_vs_low20_now(f, i) <= 0.025 and f.close_to_ema50[i] >= -0.18)
def reversal_context_score(raw: RawSignals, f: FeaturePack, i: int) -> int:
    return (
        volatility_soft_point(f, i)
        + oversold_soft_point(f, i)
        + recovery_soft_point(f, i)
        + trendfloor_soft_point(f, i)
        + shockfresh_soft_point(raw, i)
        + reclaim_soft_point(f, i)
        + volume_soft_point(f, i)
        + location_soft_point(f, i)
    )
def recent_count(arr: np.ndarray, i: int, bars: int, include_current: bool = False) -> int:
    end = i + 1 if include_current else i
    return len(recent_true_indices(arr, i - bars, end))
def shock_age_leq(raw: RawSignals, i: int, max_age: int, lookback: int = 10) -> bool:
    age = recent_shock_age(raw, i, lookback=lookback)
    return age is not None and 0 <= age <= max_age
def shock_age_between(raw: RawSignals, i: int, min_age: int, max_age: int, lookback: int = 10) -> bool:
    age = recent_shock_age(raw, i, lookback=lookback)
    return age is not None and min_age <= age <= max_age
def first_shock_only(raw: RawSignals, i: int, lookback: int = 8) -> bool:
    return recent_count(raw.shock_down, i, lookback, include_current=False) <= 1
def strict_reclaim_ok(f: FeaturePack, i: int) -> bool:
    return (
        f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.80
        and f.lower_wick_body_ratio[i] >= 1.00
        and f.body_atr[i] >= 0.20
    )
def drive_reclaim_ok(f: FeaturePack, i: int) -> bool:
    return (
        f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.84
        and f.body_atr[i] >= 0.25
        and f.vol_ratio[i] >= 1.10
    )
def low_anchor_ok(f: FeaturePack, i: int, max_gap: float = 0.015) -> bool:
    return low_vs_low20_now(f, i) <= max_gap
def ema20_retake_ok(f: FeaturePack, i: int) -> bool:
    return f.close[i] > f.ema20[i]
def midflip_ok(f: FeaturePack, i: int) -> bool:
    return f.close[i] > f.range_mid20[i]
def deep_discount_ok(f: FeaturePack, i: int) -> bool:
    return -0.16 <= f.close_to_ema50[i] <= -0.04
def moderate_discount_ok(f: FeaturePack, i: int) -> bool:
    return f.close_to_ema50[i] >= -0.10
def vol_not_manic(f: FeaturePack, i: int, max_vol: float = 2.40) -> bool:
    return f.vol_ratio[i] <= max_vol
def shock_low_retake_ok(raw: RawSignals, f: FeaturePack, i: int, lookback: int = 8, min_markup: float = 0.002) -> bool:
    ref_low = recent_signal_low(raw.shock_down, f.low, i, lookback)
    if ref_low is None:
        return False
    return f.close[i] > ref_low * (1.0 + min_markup)
def prev_high_reclaim_ok(f: FeaturePack, i: int) -> bool:
    if i < 1:
        return False
    return f.close[i] > f.high[i - 1] * 0.998
def no_family_cluster(arr: np.ndarray, i: int, bars: int) -> bool:
    return recent_count(arr, i, bars, include_current=False) == 0

def family_seed_core(seed: str, f: FeaturePack, raw: RawSignals, i: int, score: int) -> bool:
    age_early = shock_age_leq(raw, i, 4)
    age_wide = shock_age_leq(raw, i, 6)
    drive = drive_reclaim_ok(f, i)
    low_anchor_wide = low_anchor_ok(f, i, 0.018)
    rare18 = no_family_cluster(raw.beartrap_close_drive, i, 18)
    rare22 = no_family_cluster(raw.beartrap_close_drive, i, 22)
    rare28 = no_family_cluster(raw.beartrap_close_drive, i, 28)
    c1 = recent_count(raw.beartrap_close_drive, i, 16, include_current=False) <= 1
    score4 = score >= 4
    if seed == "V51":
        return age_wide and raw.l01_cap_reclaim[i] and drive and score4 and rare22
    if seed == "V27":
        return drive and f.body_atr[i] >= 0.28 and score4 and rare18
    if seed == "V09":
        return recent_count(raw.beartrap_close_drive, i, 30, include_current=False) == 0 and age_wide and score4 and rare28
    if seed == "V28":
        return age_wide and c1 and drive and low_anchor_wide and score4
    return False

def family_anchor_guards(f: FeaturePack, raw: RawSignals, i: int, score: int) -> Tuple[List[bool], List[bool]]:
    age_mid = shock_age_between(raw, i, 2, 6)
    strict = strict_reclaim_ok(f, i)
    drive = drive_reclaim_ok(f, i)
    low_anchor = low_anchor_ok(f, i, 0.012)
    moderate = moderate_discount_ok(f, i)
    ema = ema20_retake_ok(f, i)
    mid = midflip_ok(f, i)
    prev = prev_high_reclaim_ok(f, i)
    shock_low = shock_low_retake_ok(raw, f, i, 8, 0.003)
    qh = f.close_pos[i] >= 0.82
    qb = f.close_pos[i] >= 0.78
    first = first_shock_only(raw, i, 8)
    rare22 = no_family_cluster(raw.beartrap_close_drive, i, 22)
    rare28 = no_family_cluster(raw.beartrap_close_drive, i, 28)
    vnm18 = vol_not_manic(f, i, 1.80)
    vnm16 = vol_not_manic(f, i, 1.60)
    c0 = recent_count(raw.beartrap_close_drive, i, 12, include_current=False) == 0
    c1 = recent_count(raw.beartrap_close_drive, i, 16, include_current=False) <= 1
    recent8 = recent_count(raw.beartrap_close_drive, i, 8, include_current=False) == 0
    score5 = score >= 5

    anchors = [
        True,
        strict,
        low_anchor,
        shock_low,
        prev,
        raw.extreme_reclaim[i],
        raw.spring_undercut[i],
        ema and mid and moderate,
        raw.hammer_flush[i] or raw.outside_flush_reversal[i],
        qh and strict and drive,
    ]
    guards = [
        True,
        rare22 and c1,
        rare28 and first,
        vnm18,
        vnm16 and f.quiet_ratio[i] <= 0.95,
        recent_count(raw.shock_down, i, 14, include_current=False) == 0,
        c0 and recent_count(raw.beartrap_close_drive, i, 40, include_current=False) == 0,
        score5 and recovery_soft_point(f, i) and location_soft_point(f, i),
        score >= 4 and f.body_atr[i] >= 0.22 and qb,
        recent8 and age_mid,
    ]
    return anchors, guards

def family_specific_gate(seed: str, a_idx: int, g_idx: int, f: FeaturePack, raw: RawSignals, i: int, score: int) -> bool:
    age_early = shock_age_leq(raw, i, 4)
    age_mid = shock_age_between(raw, i, 2, 6)
    age_wide = shock_age_leq(raw, i, 6)
    strict = strict_reclaim_ok(f, i)
    drive = drive_reclaim_ok(f, i)
    low_anchor = low_anchor_ok(f, i, 0.012)
    low_anchor_wide = low_anchor_ok(f, i, 0.018)
    moderate = moderate_discount_ok(f, i)
    deep = deep_discount_ok(f, i)
    ema = ema20_retake_ok(f, i)
    mid = midflip_ok(f, i)
    prev = prev_high_reclaim_ok(f, i)
    shock_low = shock_low_retake_ok(raw, f, i, 8, 0.003)
    score4 = score >= 4
    score5 = score >= 5
    c0 = recent_count(raw.beartrap_close_drive, i, 12, include_current=False) == 0
    c1 = recent_count(raw.beartrap_close_drive, i, 16, include_current=False) <= 1
    rare18 = no_family_cluster(raw.beartrap_close_drive, i, 18)
    rare22 = no_family_cluster(raw.beartrap_close_drive, i, 22)
    rare28 = no_family_cluster(raw.beartrap_close_drive, i, 28)
    qb = f.close_pos[i] >= 0.78
    qh = f.close_pos[i] >= 0.82

    if seed == "V51":
        extras = [
            age_wide,
            drive and rare22,
            strict and qb,
            low_anchor and drive,
            shock_low and strict,
            prev and drive,
            raw.extreme_reclaim[i] and score4,
            ema and moderate and score4,
            raw.hammer_flush[i] and drive,
            qh and c1 and score5,
        ]
    elif seed == "V27":
        extras = [
            f.body_atr[i] >= 0.28,
            drive and rare18,
            age_early and strict,
            low_anchor and shock_low,
            prev and qb,
            raw.spring_undercut[i] and drive,
            raw.extreme_reclaim[i] and score4,
            deep and strict,
            ema and mid and score4,
            qh and c0 and score5,
        ]
    elif seed == "V09":
        extras = [
            age_wide,
            c0 and rare28,
            first_shock_only(raw, i, 8),
            low_anchor_wide and drive,
            recent_count(raw.shock_down, i, 14, include_current=False) == 0,
            raw.l01_cap_reclaim[i] and drive,
            raw.extreme_reclaim[i] and strict,
            shock_low and prev,
            moderate and qb,
            score5 and recovery_soft_point(f, i),
        ]
    elif seed == "V28":
        extras = [
            age_wide and c1,
            drive and low_anchor_wide,
            strict and rare22,
            first_shock_only(raw, i, 10),
            shock_low and low_anchor,
            prev and drive,
            raw.spring_undercut[i] and score4,
            ema and strict and moderate,
            qh and c0,
            score5 and location_soft_point(f, i),
        ]
    else:
        return False
    return extras[a_idx % len(extras)] and extras[g_idx % len(extras)]

def seed_variant_signal(seed: str, variant: int, f: FeaturePack, raw: RawSignals, i: int, score: int) -> bool:
    if not raw.beartrap_close_drive[i]:
        return False
    core = family_seed_core(seed, f, raw, i, score)
    if not core:
        return False
    a_idx = (variant - 1) // len(GUARD_TAGS)
    g_idx = (variant - 1) % len(GUARD_TAGS)
    anchors, guards = family_anchor_guards(f, raw, i, score)
    return anchors[a_idx] and guards[g_idx] and family_specific_gate(seed, a_idx, g_idx, f, raw, i, score)

def build_strategy_masks(f: FeaturePack, raw: RawSignals) -> Dict[str, np.ndarray]:
    masks: Dict[str, np.ndarray] = {spec.name: np.zeros(len(f.close), dtype=bool) for spec in STRATEGIES}
    start = max(WARMUP_BARS, 21)
    family_names: Dict[str, List[str]] = {
        family: [name for name, *_ in items] for family, items in FAMILY_VARIANTS.items()
    }
    candidate_idxs = np.flatnonzero(raw.beartrap_close_drive[start:]) + start
    for i in candidate_idxs:
        score = reversal_context_score(raw, f, i)
        anchors, guards = family_anchor_guards(f, raw, i, score)
        # micro-optimization: skip families whose seed core is false
        family_core = {seed: family_seed_core(seed, f, raw, i, score) for seed in FAMILY_VARIANTS.keys()}
        for family, names in family_names.items():
            if not family_core[family]:
                continue
            for variant, name in enumerate(names, start=1):
                a_idx = (variant - 1) // len(GUARD_TAGS)
                g_idx = (variant - 1) % len(GUARD_TAGS)
                if anchors[a_idx] and guards[g_idx] and family_specific_gate(family, a_idx, g_idx, f, raw, i, score):
                    masks[name][i] = True
    return masks


def backtest_signal_mask(symbol: str, f: FeaturePack, spec: StrategySpec, signal_mask: np.ndarray) -> Tuple[SymbolSummary, List[Tuple[int, float]]]:
    n = len(f.close)
    if n < MIN_BARS or signal_mask.sum() == 0:
        return SymbolSummary(symbol=symbol), []
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
                trades.append(TradeRecord(entry_ts, ts, float(net_pct), hold_bars, float(entry_price), float(exit_price), exit_reason))
                in_pos = False
                cooldown = spec.cooldown_bars
                hold_bars = 0
                continue
        if not in_pos:
            if cooldown > 0:
                cooldown -= 1
                continue
            if signal_mask[i]:
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
def evaluate_all_strategies_for_symbol(symbol: str, csv_path: Path) -> Dict[str, Tuple[SymbolSummary, List[Tuple[int, float]]]]:
    try:
        f = load_feature_pack(csv_path)
        raw = build_raw_signals(f)
        masks = build_strategy_masks(f, raw)
        out: Dict[str, Tuple[SymbolSummary, List[Tuple[int, float]]]] = {}
        for spec in STRATEGIES:
            out[spec.name] = backtest_signal_mask(symbol, f, spec, masks[spec.name])
        return out
    except Exception:
        return {spec.name: (SymbolSummary(symbol=symbol), []) for spec in STRATEGIES}
def aggregate_strategy_result(spec: StrategySpec, per_symbol: List[SymbolSummary], trades: List[Tuple[int, float]]) -> Dict[str, Any]:
    all_trade_pnls = [pnl for _, pnl in sorted(trades, key=lambda x: x[0])]
    final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined = summarize_trade_pnls(all_trade_pnls)
    total_trades = sum(x.trades for x in per_symbol)
    total_wins = sum(x.wins for x in per_symbol)
    total_losses = sum(x.losses for x in per_symbol)
    win_rate_pct = (total_wins / total_trades * 100.0) if total_trades else 0.0
    baseline_cd = BASELINE_CD_VALUE[spec.side]
    if max_dd_pct > 5.0 and cd_value >= baseline_cd:
        verdict = "candidate_cd_win_mdd_fail"
    elif max_dd_pct > 5.0:
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
def merge_chunk_results(global_per_symbol: Dict[str, List[SymbolSummary]], global_trades: Dict[str, List[Tuple[int, float]]], chunk_result: Dict[str, Any]) -> None:
    for name, item in chunk_result.items():
        global_per_symbol[name].extend(item['per_symbol'])
        global_trades[name].extend(item['trades'])
def run_symbol_chunk(symbols_chunk: List[str], data_file_map: Dict[str, str]) -> Dict[str, Any]:
    per_symbol_map: Dict[str, List[SymbolSummary]] = {spec.name: [] for spec in STRATEGIES}
    trades_map: Dict[str, List[Tuple[int, float]]] = {spec.name: [] for spec in STRATEGIES}
    for symbol in symbols_chunk:
        csv_path_str = data_file_map.get(symbol)
        if not csv_path_str:
            continue
        csv_path = Path(csv_path_str)
        symbol_result = evaluate_all_strategies_for_symbol(symbol, csv_path)
        for name, (summary, trades) in symbol_result.items():
            per_symbol_map[name].append(summary)
            trades_map[name].extend(trades)
    return {name: {'per_symbol': per_symbol_map[name], 'trades': trades_map[name]} for name in per_symbol_map}
def chunk_list(items: List[str], n_chunks: int) -> List[List[str]]:
    n_chunks = max(1, n_chunks)
    chunk_size = max(1, int(np.ceil(len(items) / n_chunks)))
    return [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]
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
    workers = min(DEFAULT_WORKERS, max(1, os.cpu_count() or 2))
    chunks = chunk_list(resolved_symbols, workers * 2)
    global_per_symbol: Dict[str, List[SymbolSummary]] = {spec.name: [] for spec in STRATEGIES}
    global_trades: Dict[str, List[Tuple[int, float]]] = {spec.name: [] for spec in STRATEGIES}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(run_symbol_chunk, chunk, worker_file_map) for chunk in chunks if chunk]
        for fut in as_completed(futures):
            merge_chunk_results(global_per_symbol, global_trades, fut.result())
    summaries: List[Dict[str, Any]] = []
    spec_map = {spec.name: spec for spec in STRATEGIES}
    for spec in STRATEGIES:
        summary_dict = aggregate_strategy_result(spec, global_per_symbol[spec.name], global_trades[spec.name])
        print_strategy_summary_line(summary_dict)
        save_strategy_outputs(spec, summary_dict, global_per_symbol[spec.name])
        summaries.append(summary_dict)
    summaries = sorted(summaries, key=lambda x: (-x['cd_value'], -x['final_return_pct']))
    save_batch_registry(summaries)
    elapsed = time.time() - started
    log(f"done | strategies={len(summaries)} | elapsed_sec={elapsed:.2f}")
if __name__ == "__main__":
    main()