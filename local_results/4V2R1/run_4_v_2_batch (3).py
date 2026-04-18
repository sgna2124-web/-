from __future__ import annotations

import json
import math
import os
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import pandas as pd


# ============================================================
# 4V2 FAST LOCAL BACKTEST ENGINE
# ------------------------------------------------------------
# 핵심 목표
# 1) 종목 1회 로드
# 2) 공통 지표 1회 계산
# 3) 여러 전략을 같은 종목에서 연속 평가
# 4) 종목 단위 병렬 처리
# 5) summary/per_symbol_summary/registry만 저장
# 6) fillna(method='bfill') FutureWarning 제거
# ============================================================


# -----------------------------
# Baseline comparison
# -----------------------------
BASELINE_CD_VALUE = {
    "long": 108.8106,
    "short": 391.9606,
}


# -----------------------------
# Runtime config
# -----------------------------
TIMEFRAME_LABEL = "5m"
BATCH_LABEL = "4V2R1"
ROUND_TRIP_COST_BPS = 10.0
MIN_BARS = 250
WARMUP_BARS = 120
DEFAULT_WORKERS = max(1, (os.cpu_count() or 2) - 1)
SAVE_EVERY = 20


# -----------------------------
# Path discovery
# -----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
CWD = Path.cwd()


def find_repo_root() -> Path:
    candidates: List[Path] = []
    for base in [CWD, SCRIPT_DIR]:
        candidates.append(base)
        candidates.extend(list(base.parents))

    seen = set()
    uniq_candidates: List[Path] = []
    for c in candidates:
        s = str(c)
        if s not in seen:
            uniq_candidates.append(c)
            seen.add(s)

    for root in uniq_candidates:
        has_symbol_cost = (root / "symbol_cost").exists()
        has_data_dir = (root / "코인" / "Data" / "time").exists() or (root / "Data" / "time").exists()
        if has_symbol_cost and has_data_dir:
            return root

    for root in uniq_candidates:
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


# -----------------------------
# Strategy specs
# -----------------------------
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
    StrategySpec(
        "4V2_L01_capitulation_reclaim",
        "long",
        "4V2 L01 재검증: 1% 진입 기준 원형 급락 회수 전략",
        1.10,
        2.20,
        18,
        8,
    ),
]


# -----------------------------
# Result dataclasses
# -----------------------------
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


@dataclass
class StrategyAggregate:
    name: str
    side: str
    description: str
    trades: List[Tuple[int, float]] = field(default_factory=list)
    per_symbol_summary: List[SymbolSummary] = field(default_factory=list)
    total_trades: int = 0
    total_wins: int = 0
    total_losses: int = 0
    processed_symbols: int = 0


# -----------------------------
# Utility
# -----------------------------

def log(msg: str) -> None:
    print(msg, flush=True)


def normalize_symbol_text(x: str) -> str:
    s = str(x).strip().upper()
    s = s.replace("-", "")
    s = s.replace("_", "")
    s = s.replace("/", "")
    s = s.replace(":", "")
    s = s.replace(" ", "")
    return s


def infer_symbol_from_path(path: Path) -> str:
    stem = path.stem.upper()
    stem = stem.replace("-", "_")
    parts = stem.split("_")
    if len(parts) >= 2 and parts[-1] in {"1M", "3M", "5M", "15M", "30M", "1H", "4H", "1D"}:
        stem = "_".join(parts[:-1])
    stem = stem.replace("_PERP", "")
    stem = stem.replace("PERP", "")
    stem = stem.replace("USDT", "/USDT") if "/USDT" not in stem and "USDT" in stem else stem
    stem = stem.replace("BUSD", "/BUSD") if "/BUSD" not in stem and "BUSD" in stem else stem
    stem = stem.replace("USD", "/USD") if "/USD" not in stem and stem.endswith("USD") else stem
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
    key = normalize_symbol_text(symbol)
    return data_file_map.get(key)


# -----------------------------
# Indicator helpers
# -----------------------------

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
    dd_value = float(abs(np.min(dd))) if dd.size else 0.0
    return min(100.0, dd_value)


def max_return_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    return float((np.max(equity_curve) - 1.0) * 100.0)


def cd_value_from_return_and_mdd(final_return_pct: float, max_drawdown_pct: float) -> float:
    base_after_mdd = 100.0 * (1.0 - max_drawdown_pct / 100.0)
    return base_after_mdd * (1.0 + final_return_pct / 100.0)


POSITION_FRACTION = 0.01
RUIN_THRESHOLD = 1e-12


def equity_curve_from_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[np.ndarray, bool]:
    if not trade_pnls_pct:
        return np.array([1.0], dtype=np.float64), False
    eq = [1.0]
    cur = 1.0
    ruined = False
    for pnl_pct in trade_pnls_pct:
        step = 1.0 + POSITION_FRACTION * (pnl_pct / 100.0)
        if step <= 0.0:
            cur = 0.0
            eq.append(cur)
            ruined = True
            break
        cur *= step
        if cur <= RUIN_THRESHOLD:
            cur = 0.0
            eq.append(cur)
            ruined = True
            break
        eq.append(cur)
    return np.asarray(eq, dtype=np.float64), ruined


def summarize_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[float, float, float, float, bool]:
    eq, ruined = equity_curve_from_trade_pnls(trade_pnls_pct)
    max_return_pct = max_return_pct_from_equity(eq)
    final_return_pct = (eq[-1] - 1.0) * 100.0
    max_dd_pct = max_drawdown_pct_from_equity(eq)

    if ruined or max_dd_pct >= 99.9999:
        final_return_pct = -100.0
        max_dd_pct = 100.0
        cd_value = 0.0
        ruined = True
    else:
        cd_value = cd_value_from_return_and_mdd(final_return_pct, max_dd_pct)

    return float(final_return_pct), float(max_return_pct), float(max_dd_pct), float(cd_value), ruined


# -----------------------------
# Data preparation
# -----------------------------

def standardize_ohlcv_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: Dict[str, str] = {}
    for c in df.columns:
        lc = str(c).strip().lower()
        if lc in {"time", "datetime", "date", "open_time", "timestamp", "ts"}:
            rename_map[c] = "timestamp"
        elif lc in {"open", "o"}:
            rename_map[c] = "open"
        elif lc in {"high", "h"}:
            rename_map[c] = "high"
        elif lc in {"low", "l"}:
            rename_map[c] = "low"
        elif lc in {"close", "c"}:
            rename_map[c] = "close"
        elif lc in {"volume", "vol", "v", "quote_volume"}:
            rename_map[c] = "volume"

    df = df.rename(columns=rename_map).copy()
    required = ["open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"필수 컬럼 누락: {missing}")

    if "timestamp" not in df.columns:
        df["timestamp"] = np.arange(len(df), dtype=np.int64)
    else:
        ts = df["timestamp"]
        if pd.api.types.is_datetime64_any_dtype(ts):
            df["timestamp"] = ts.astype("int64") // 10**9
        else:
            try:
                parsed = pd.to_datetime(ts, errors="coerce", utc=False)
                if parsed.notna().mean() > 0.8:
                    df["timestamp"] = parsed.astype("int64") // 10**9
                else:
                    df["timestamp"] = pd.to_numeric(ts, errors="coerce").fillna(method="ffill").fillna(0).astype("int64")
            except Exception:
                df["timestamp"] = np.arange(len(df), dtype=np.int64)

    usecols = ["timestamp", "open", "high", "low", "close", "volume"]
    df = df[usecols].copy()
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float32")
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce").fillna(0).astype("int64")
    df = df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    return df


def load_df(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        low_memory=False,
    )
    df = standardize_ohlcv_columns(df)
    if len(df) < MIN_BARS:
        raise ValueError(f"bars 부족: {path.name} ({len(df)})")
    return df


@dataclass
class FeaturePack:
    timestamp: np.ndarray
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray
    ema20: np.ndarray
    ema50: np.ndarray
    ema100: np.ndarray
    atr14: np.ndarray
    atrp: np.ndarray
    hh20: np.ndarray
    ll20: np.ndarray
    hh50: np.ndarray
    ll50: np.ndarray
    vol_ma20: np.ndarray
    vol_ratio: np.ndarray
    body: np.ndarray
    body_atr: np.ndarray
    upper_wick: np.ndarray
    lower_wick: np.ndarray
    close_pos: np.ndarray
    range20: np.ndarray
    range50: np.ndarray
    range20_pct: np.ndarray
    range50_pct: np.ndarray
    ret3: np.ndarray
    ret5: np.ndarray
    ret10: np.ndarray
    trend_up: np.ndarray
    trend_down: np.ndarray


def prepare_features(df: pd.DataFrame) -> FeaturePack:
    close = df["close"]
    high = df["high"]
    low = df["low"]
    open_ = df["open"]
    volume = df["volume"]

    ema20 = close.ewm(span=20, adjust=False).mean().astype("float32")
    ema50 = close.ewm(span=50, adjust=False).mean().astype("float32")
    ema100 = close.ewm(span=100, adjust=False).mean().astype("float32")
    atr14 = atr(df, 14).astype("float32")
    atrp = (atr14 / close.replace(0, np.nan)).fillna(0).astype("float32")

    hh20 = high.rolling(20, min_periods=1).max().astype("float32")
    ll20 = low.rolling(20, min_periods=1).min().astype("float32")
    hh50 = high.rolling(50, min_periods=1).max().astype("float32")
    ll50 = low.rolling(50, min_periods=1).min().astype("float32")

    vol_ma20 = volume.rolling(20, min_periods=1).mean().astype("float32")
    vol_ratio = (volume / vol_ma20.replace(0, np.nan)).fillna(0).astype("float32")

    body = (close - open_).abs().astype("float32")
    body_atr = (body / atr14.replace(0, np.nan)).fillna(0).astype("float32")
    upper_wick = (high - np.maximum(open_, close)).astype("float32")
    lower_wick = (np.minimum(open_, close) - low).astype("float32")

    spread = (high - low).replace(0, np.nan)
    close_pos = ((close - low) / spread).fillna(0.5).astype("float32")

    range20 = (hh20 - ll20).astype("float32")
    range50 = (hh50 - ll50).astype("float32")
    range20_pct = (range20 / close.replace(0, np.nan)).fillna(0).astype("float32")
    range50_pct = (range50 / close.replace(0, np.nan)).fillna(0).astype("float32")

    ret3 = close.pct_change(3).fillna(0).astype("float32")
    ret5 = close.pct_change(5).fillna(0).astype("float32")
    ret10 = close.pct_change(10).fillna(0).astype("float32")

    trend_up = ((ema20 > ema50) & (ema50 > ema100)).astype(np.bool_)
    trend_down = ((ema20 < ema50) & (ema50 < ema100)).astype(np.bool_)

    return FeaturePack(
        timestamp=df["timestamp"].to_numpy(dtype=np.int64),
        open=df["open"].to_numpy(dtype=np.float32),
        high=df["high"].to_numpy(dtype=np.float32),
        low=df["low"].to_numpy(dtype=np.float32),
        close=df["close"].to_numpy(dtype=np.float32),
        volume=df["volume"].to_numpy(dtype=np.float32),
        ema20=ema20.to_numpy(dtype=np.float32),
        ema50=ema50.to_numpy(dtype=np.float32),
        ema100=ema100.to_numpy(dtype=np.float32),
        atr14=atr14.to_numpy(dtype=np.float32),
        atrp=atrp.to_numpy(dtype=np.float32),
        hh20=hh20.to_numpy(dtype=np.float32),
        ll20=ll20.to_numpy(dtype=np.float32),
        hh50=hh50.to_numpy(dtype=np.float32),
        ll50=ll50.to_numpy(dtype=np.float32),
        vol_ma20=vol_ma20.to_numpy(dtype=np.float32),
        vol_ratio=vol_ratio.to_numpy(dtype=np.float32),
        body=body.to_numpy(dtype=np.float32),
        body_atr=body_atr.to_numpy(dtype=np.float32),
        upper_wick=upper_wick.to_numpy(dtype=np.float32),
        lower_wick=lower_wick.to_numpy(dtype=np.float32),
        close_pos=close_pos.to_numpy(dtype=np.float32),
        range20=range20.to_numpy(dtype=np.float32),
        range50=range50.to_numpy(dtype=np.float32),
        range20_pct=range20_pct.to_numpy(dtype=np.float32),
        range50_pct=range50_pct.to_numpy(dtype=np.float32),
        ret3=ret3.to_numpy(dtype=np.float32),
        ret5=ret5.to_numpy(dtype=np.float32),
        ret10=ret10.to_numpy(dtype=np.float32),
        trend_up=trend_up,
        trend_down=trend_down,
    )


# -----------------------------
# Strategy signal helpers
# -----------------------------

def recent_breakdown_bar(f: FeaturePack, i: int, lookback: int = 3) -> bool:
    start = max(1, i - lookback)
    for j in range(start, i):
        if f.close[j] < f.ll20[j - 1]:
            return True
    return False


def recent_breakout_bar(f: FeaturePack, i: int, lookback: int = 3) -> bool:
    start = max(1, i - lookback)
    for j in range(start, i):
        if f.close[j] > f.hh20[j - 1]:
            return True
    return False


def entry_signal(spec: StrategySpec, f: FeaturePack, i: int) -> bool:
    close = f.close
    open_ = f.open
    low = f.low
    vol_ratio = f.vol_ratio
    ll20 = f.ll20
    body_atr = f.body_atr
    ret3 = f.ret3
    ret5 = f.ret5
    close_pos = f.close_pos

    if f.atrp[i] <= 0.0035:
        return False

    if spec.name == "4V2_L01_capitulation_reclaim":
        flush = (ret3[i] < -0.04) or (ret5[i] < -0.06)
        reclaim = (low[i] < ll20[i - 1]) and (close[i] > ll20[i - 1]) and (close[i] > open_[i])
        strength = (close_pos[i] > 0.74) and (body_atr[i] > 0.42)
        vol_ok = vol_ratio[i] > 1.6
        return bool(flush and reclaim and strength and vol_ok)

    return False


# -----------------------------
# Backtest core
# -----------------------------

def backtest_symbol_strategy(symbol: str, f: FeaturePack, spec: StrategySpec) -> Tuple[SymbolSummary, List[Tuple[int, float]]]:
    n = len(f.close)
    if n < max(MIN_BARS, WARMUP_BARS + 5):
        return SymbolSummary(symbol=symbol), []

    in_pos = False
    entry_price = 0.0
    entry_ts = 0
    stop_price = 0.0
    target_price = 0.0
    hold_bars = 0
    cooldown = 0
    trades: List[TradeRecord] = []

    for i in range(max(WARMUP_BARS, 2), n):
        px_open = float(f.open[i])
        px_high = float(f.high[i])
        px_low = float(f.low[i])
        px_close = float(f.close[i])
        ts = int(f.timestamp[i])
        atr14 = max(1e-9, float(f.atr14[i]))

        if in_pos:
            hold_bars += 1
            exit_price: Optional[float] = None
            exit_reason = ""

            if spec.side == "long":
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
            else:
                hit_stop = px_high >= stop_price
                hit_target = px_low <= target_price
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
                if spec.side == "short":
                    gross_pct *= -1.0
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

            if entry_signal(spec, f, i):
                entry_price = px_close
                entry_ts = ts
                risk = spec.atr_stop * atr14
                if spec.side == "long":
                    stop_price = entry_price - risk
                    target_price = entry_price + (risk * spec.rr_target)
                else:
                    stop_price = entry_price + risk
                    target_price = entry_price - (risk * spec.rr_target)
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


# -----------------------------
# Worker
# -----------------------------

def process_symbol_job(job: Tuple[str, str]) -> Dict[str, Any]:
    symbol, path_str = job
    path = Path(path_str)
    t0 = time.perf_counter()

    df = load_df(path)
    t1 = time.perf_counter()
    features = prepare_features(df)
    t2 = time.perf_counter()

    out: Dict[str, Any] = {
        "symbol": symbol,
        "path": str(path),
        "bars": int(len(df)),
        "timing": {
            "load_sec": round(t1 - t0, 4),
            "feature_sec": round(t2 - t1, 4),
        },
        "strategies": {},
    }

    for spec in STRATEGIES:
        s0 = time.perf_counter()
        symbol_summary, trades = backtest_symbol_strategy(symbol, features, spec)
        s1 = time.perf_counter()
        out["strategies"][spec.name] = {
            "summary": asdict(symbol_summary),
            "trades": trades,
            "backtest_sec": round(s1 - s0, 4),
        }
    return out


# -----------------------------
# Aggregation
# -----------------------------

def init_aggregates() -> Dict[str, StrategyAggregate]:
    return {
        spec.name: StrategyAggregate(name=spec.name, side=spec.side, description=spec.description)
        for spec in STRATEGIES
    }


def aggregate_results(results: List[Dict[str, Any]]) -> Tuple[Dict[str, StrategyAggregate], Dict[str, float]]:
    aggs = init_aggregates()
    timing_total = {
        "load_sec": 0.0,
        "feature_sec": 0.0,
        "backtest_sec": 0.0,
    }

    for item in results:
        timing_total["load_sec"] += float(item["timing"]["load_sec"])
        timing_total["feature_sec"] += float(item["timing"]["feature_sec"])

        for spec in STRATEGIES:
            data = item["strategies"][spec.name]
            summary = data["summary"]
            trades = data["trades"]
            agg = aggs[spec.name]
            agg.per_symbol_summary.append(SymbolSummary(**summary))
            agg.trades.extend((int(ts), float(pnl)) for ts, pnl in trades)
            agg.total_trades += int(summary["trades"])
            agg.total_wins += int(summary["wins"])
            agg.total_losses += int(summary["losses"])
            agg.processed_symbols += 1
            timing_total["backtest_sec"] += float(data["backtest_sec"])

    return aggs, timing_total


def build_strategy_summary(agg: StrategyAggregate) -> Dict[str, Any]:
    ordered_trades = sorted(agg.trades, key=lambda x: x[0])
    pnl_list = [pnl for _, pnl in ordered_trades]
    final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined = summarize_trade_pnls(pnl_list)
    win_rate_pct = (agg.total_wins / agg.total_trades * 100.0) if agg.total_trades else 0.0
    baseline_cd = BASELINE_CD_VALUE[agg.side]
    delta_cd = cd_value - baseline_cd

    verdict = "candidate"
    if ruined:
        verdict = "ruin"
    elif cd_value <= 0.0:
        verdict = "reject"
    elif max_dd_pct >= 5.0:
        verdict = "mdd_fail"
    elif delta_cd <= 0.0:
        verdict = "below_baseline"

    return {
        "strategy_name": agg.name,
        "side": agg.side,
        "description": agg.description,
        "symbols_tested": agg.processed_symbols,
        "trades": agg.total_trades,
        "wins": agg.total_wins,
        "losses": agg.total_losses,
        "win_rate_pct": round(win_rate_pct, 4),
        "final_return_pct": round(final_return_pct, 4),
        "max_return_pct": round(max_return_pct, 4),
        "max_drawdown_pct": round(max_dd_pct, 4),
        "cd_value": round(cd_value, 4),
        "baseline_cd_value": baseline_cd,
        "delta_cd_value_vs_baseline": round(delta_cd, 4),
        "verdict": verdict,
    }


def write_strategy_outputs(agg: StrategyAggregate, summary: Dict[str, Any], strategy_root: Path) -> None:
    strategy_root.mkdir(parents=True, exist_ok=True)

    per_symbol_payload = [
        {
            "symbol": s.symbol,
            "trades": s.trades,
            "wins": s.wins,
            "losses": s.losses,
            "win_rate_pct": round(s.win_rate_pct, 4),
            "final_return_pct": round(s.final_return_pct, 4),
            "max_return_pct": round(s.max_return_pct, 4),
            "max_drawdown_pct": round(s.max_drawdown_pct, 4),
            "cd_value": round(s.cd_value, 4),
        }
        for s in sorted(agg.per_symbol_summary, key=lambda x: x.final_return_pct, reverse=True)
    ]

    (strategy_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (strategy_root / "per_symbol_summary.json").write_text(
        json.dumps(per_symbol_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        f"strategy={summary['strategy_name']}",
        f"side={summary['side']}",
        f"description={summary['description']}",
        f"symbols_tested={summary['symbols_tested']}",
        f"trades={summary['trades']}",
        f"win_rate_pct={summary['win_rate_pct']}",
        f"final_return_pct={summary['final_return_pct']}",
        f"max_return_pct={summary['max_return_pct']}",
        f"max_drawdown_pct={summary['max_drawdown_pct']}",
        f"cd_value={summary['cd_value']}",
        f"baseline_cd_value={summary['baseline_cd_value']}",
        f"delta_cd_value_vs_baseline={summary['delta_cd_value_vs_baseline']}",
        f"verdict={summary['verdict']}",
    ]
    (strategy_root / "master_summary.txt").write_text("".join(lines), encoding="utf-8")


def write_registry(registry_rows: List[Dict[str, Any]], result_root: Path) -> None:
    df = pd.DataFrame(registry_rows)
    order_cols = [
        "strategy_name",
        "side",
        "description",
        "symbols_tested",
        "trades",
        "wins",
        "losses",
        "win_rate_pct",
        "final_return_pct",
        "max_return_pct",
        "max_drawdown_pct",
        "cd_value",
        "baseline_cd_value",
        "delta_cd_value_vs_baseline",
        "verdict",
    ]
    cols = [c for c in order_cols if c in df.columns]
    df = df[cols].sort_values(["side", "cd_value"], ascending=[True, False]).reset_index(drop=True)
    df.to_csv(result_root / f"{BATCH_LABEL}_registry.csv", index=False, encoding="utf-8-sig")


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    t_global0 = time.perf_counter()

    log(f"REPO_ROOT = {REPO_ROOT}")
    log(f"DATA_ROOT = {DATA_ROOT}")
    log(f"SYMBOL_COST_PATH = {SYMBOL_COST_PATH}")
    log(f"RESULT_ROOT = {RESULT_ROOT}")

    data_file_map = build_data_file_map(DATA_ROOT)
    symbols = load_symbols(SYMBOL_COST_PATH, data_file_map)
    jobs: List[Tuple[str, str]] = []
    for symbol in symbols:
        p = resolve_symbol_path(symbol, data_file_map)
        if p is not None:
            jobs.append((symbol, str(p)))

    if not jobs:
        raise RuntimeError("백테스트 대상 종목이 없습니다.")

    log(f"symbols={len(jobs)} | workers={DEFAULT_WORKERS} | strategies={len(STRATEGIES)}")

    results: List[Dict[str, Any]] = []
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=DEFAULT_WORKERS) as ex:
        futures = [ex.submit(process_symbol_job, job) for job in jobs]
        done_count = 0
        for fut in as_completed(futures):
            results.append(fut.result())
            done_count += 1
            if done_count % SAVE_EVERY == 0 or done_count == len(futures):
                log(f"processed {done_count}/{len(futures)} symbols")
    t1 = time.perf_counter()

    aggs, timing_total = aggregate_results(results)
    registry_rows: List[Dict[str, Any]] = []

    for spec in STRATEGIES:
        agg = aggs[spec.name]
        summary = build_strategy_summary(agg)
        strategy_root = RESULT_ROOT / spec.name
        write_strategy_outputs(agg, summary, strategy_root)
        registry_rows.append(summary)
        log(
            f"{spec.name} | cd={summary['cd_value']:.4f} | "
            f"ret={summary['final_return_pct']:.4f} | "
            f"max_ret={summary['max_return_pct']:.4f} | "
            f"mdd={summary['max_drawdown_pct']:.4f} | "
            f"trades={summary['trades']} | verdict={summary['verdict']}"
        )

    write_registry(registry_rows, RESULT_ROOT)

    t_global1 = time.perf_counter()
    timing_report = {
        "symbols": len(jobs),
        "strategies": len(STRATEGIES),
        "workers": DEFAULT_WORKERS,
        "wall_clock_sec": round(t_global1 - t_global0, 4),
        "parallel_phase_sec": round(t1 - t0, 4),
        "sum_load_sec": round(timing_total["load_sec"], 4),
        "sum_feature_sec": round(timing_total["feature_sec"], 4),
        "sum_backtest_sec": round(timing_total["backtest_sec"], 4),
    }
    (RESULT_ROOT / "timing_report.json").write_text(
        json.dumps(timing_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    log("done")
    log(json.dumps(timing_report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
