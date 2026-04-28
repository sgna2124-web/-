from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import csv
import json
import math
import os
import random
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# ============================================================
# 8V12 LONG/SHORT MAIN/MAX 400 LOCAL BACKTEST ENGINE
# ------------------------------------------------------------
# 목적
# - 저장소 내 long_main_v1, long_max_v1, short_main_v1, short_max_v1 기준선 각각 100개 개선안 생성.
# - 총 400개: long_main 100 + long_max 100 + short_main 100 + short_max 100.
# - 단순 파라미터 근방 조정이 아니라, 각 기준선의 장단점을 반영한 신규 조건축을 혼합한다.
# - 포지션/거래수 개수 제한은 두지 않는다. 단, 전략 자체의 cooldown / fail-exit / trail은 리스크 제어로 유지한다.
#
# 중요 규칙
# - 공식 승격 조건: max_drawdown_pct < 5.0
# - 개선 후보: 1) MDD 5% 미만 중 cd_value 1위, 2) MDD 무관 cd_value 1위
# - cd_value: 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
# - max_return_pct를 사용하며 final_return_pct를 사용하지 않는다.
# ============================================================


BATCH_LABEL = "8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP"
TIMEFRAME_LABEL = "5m"
SIDE = "mixed"

ROUND_TRIP_COST_BPS = 10.0
POSITION_FRACTION = 0.01
MIN_BARS = 250
WARMUP_BARS = 140
SAVE_EVERY = 25
RANDOM_SEED = 811

# 현재 저장소 기준선 alias.
# long_main_v1: 롱 공식 기준선 = MDD 5% 미만 중 cd_value 1위
REFERENCE_LONG_MAIN = {
    "alias": "long_main_v1",
    "strategy_name": "6V2_L01_doubleflush_core",
    "side": "long",
    "max_return_pct": 23.9191,
    "max_drawdown_pct": 1.7512,
    "cd_value": 121.7490287208,
}
# long_max_v1: 롱 raw 개선 후보 = MDD 무관 cd_value 1위
REFERENCE_LONG_MAX = {
    "alias": "long_max_v1",
    "strategy_name": "8V4_V51_V002_core_rare22_c1",
    "side": "long",
    "max_return_pct": 44.2664,
    "max_drawdown_pct": 6.7587,
    "cd_value": 134.5158668232,
}
# short_main_v1: 숏 공식 기준선 = MDD 5% 미만 중 cd_value 1위
REFERENCE_SHORT_MAIN = {
    "alias": "short_main_v1",
    "strategy_name": "short_beh_dd_brake",
    "side": "short",
    "max_return_pct": 311.8122,
    "max_drawdown_pct": 4.7589,
    "cd_value": 392.2144692142,
}
# short_max_v1: 숏 raw 개선 후보 = MDD 무관 cd_value 1위
REFERENCE_SHORT_MAX = {
    "alias": "short_max_v1",
    "strategy_name": "short_only_reference_1x",
    "side": "short",
    "max_return_pct": 394.6145,
    "max_drawdown_pct": 7.7792,
    "cd_value": 456.1374488160,
}

REFERENCE_SAFE6V2_CD_VALUE = REFERENCE_LONG_MAIN["cd_value"]
ALL_REFERENCES = [REFERENCE_LONG_MAIN, REFERENCE_LONG_MAX, REFERENCE_SHORT_MAIN, REFERENCE_SHORT_MAX]

# -----------------------------
# Dataclasses
# -----------------------------
@dataclass(frozen=True)
class StrategySpec:
    name: str
    parent: str
    family: str
    group: str
    side: str
    description: str

    atr_stop: float
    rr_target: float
    max_hold_bars: int
    cooldown_bars: int

    ret3_drop: float
    ret5_drop: float
    ret10_drop: float
    close_pos_min: float
    body_atr_min: float
    vol_ratio_min: float
    atrp_min: float
    atrp_max: float
    range20_min: float
    range20_max: float

    require_green: bool
    require_reclaim: bool
    require_rare22: bool
    require_shocklow: bool
    strict_gate: bool
    lowanchor_gate: bool
    spring_gate: bool
    refire40_gate: bool
    microguard_gate: bool

    low_break_buffer: float
    reclaim_buffer: float
    lower_wick_body_min: float
    upper_wick_range_max: float
    ema_guard: str

    breakeven_after_r: float
    trail_after_r: float
    trail_atr_mult: float
    fail_exit_bars: int
    fail_exit_pnl_pct: float
    fail_exit_close_pos_max: float

    # 8V7 added logic fields. These are not simple parameter tweaks:
    # they control conditional entry release/brake, post-loss brake, and adaptive exits.
    safe_branch_mode: str
    entry_brake_mode: str
    chop_guard_mode: str
    exit_mode: str
    loss_brake_after: int
    loss_brake_bars: int
    loss_brake_pnl_pct: float
    symbol_dd_brake_pct: float
    symbol_dd_brake_bars: int
    recent_shock_lookback: int
    recent_shock_ret: float
    recent_shock_range_pct: float
    recent_shock_close_pos_max: float


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
    old_ratio_cd_value: float = 0.0


@dataclass
class StrategyAggregate:
    spec: StrategySpec
    trades: List[Tuple[int, float]] = field(default_factory=list)
    per_symbol_summary: List[SymbolSummary] = field(default_factory=list)
    total_trades: int = 0
    total_wins: int = 0
    total_losses: int = 0
    processed_symbols: int = 0


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
    lower_wick_body: np.ndarray
    upper_wick_range: np.ndarray
    candle_range: np.ndarray
    close_pos: np.ndarray

    range20: np.ndarray
    range50: np.ndarray
    range20_pct: np.ndarray
    range50_pct: np.ndarray

    ret1: np.ndarray
    ret3: np.ndarray
    ret5: np.ndarray
    ret10: np.ndarray
    ret20: np.ndarray

    trend_up: np.ndarray
    trend_down: np.ndarray


# This global is used by worker processes.
STRATEGIES: List[StrategySpec] = []


# -----------------------------
# Logging / JSON helpers
# -----------------------------
def log(msg: str) -> None:
    print(msg, flush=True)


def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
        if math.isfinite(v):
            return v
    except Exception:
        pass
    return default


def json_dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------
# Path discovery
# -----------------------------
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
    if "/USDT" not in stem and stem.endswith("USDT"):
        stem = stem[:-4] + "/USDT"
    elif "/BUSD" not in stem and stem.endswith("BUSD"):
        stem = stem[:-4] + "/BUSD"
    elif "/USD" not in stem and stem.endswith("USD"):
        stem = stem[:-3] + "/USD"
    return stem.replace("__", "_")


def find_repo_root(start: Optional[Path] = None) -> Path:
    base = (start or Path.cwd()).resolve()
    candidates: List[Path] = [base] + list(base.parents)
    script_dir = Path(__file__).resolve().parent
    candidates += [script_dir] + list(script_dir.parents)

    seen = set()
    uniq: List[Path] = []
    for c in candidates:
        s = str(c)
        if s not in seen:
            uniq.append(c)
            seen.add(s)

    for root in uniq:
        has_symbol_cost = (root / "symbol_cost").exists()
        has_data = (root / "코인" / "Data" / "time").exists() or (root / "Data" / "time").exists()
        if has_symbol_cost and has_data:
            return root

    for root in uniq:
        if (root / "symbol_cost").exists():
            return root

    for root in uniq:
        if (root / "코인" / "Data" / "time").exists() or (root / "Data" / "time").exists():
            return root

    return Path.cwd().resolve()


def resolve_data_root(repo_root: Path, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    candidates = [
        repo_root / "코인" / "Data" / "time",
        repo_root / "Data" / "time",
        repo_root / "time",
        Path.cwd() / "코인" / "Data" / "time",
        Path.cwd() / "Data" / "time",
    ]
    for c in candidates:
        if c.exists():
            return c.resolve()
    return candidates[0].resolve()


def resolve_symbol_cost(repo_root: Path, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    return (repo_root / "symbol_cost").resolve()


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
        suffix = symbol_cost_path.suffix.lower()
        if suffix == ".json":
            data = json.loads(symbol_cost_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        symbols.append(item)
                    elif isinstance(item, dict):
                        s = item.get("symbol") or item.get("ticker") or item.get("name")
                        if s:
                            symbols.append(str(s))
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        s = v.get("symbol") or k
                        symbols.append(str(s))
                    else:
                        symbols.append(str(k))
        elif suffix in {".csv", ".txt"}:
            try:
                df = pd.read_csv(symbol_cost_path, low_memory=False)
                candidate_cols = [c for c in df.columns if str(c).lower() in {"symbol", "ticker", "name"}]
                if candidate_cols:
                    symbols = df[candidate_cols[0]].dropna().astype(str).tolist()
                else:
                    symbols = df.iloc[:, 0].dropna().astype(str).tolist()
            except Exception:
                text = symbol_cost_path.read_text(encoding="utf-8", errors="ignore")
                symbols = [line.strip() for line in text.splitlines() if line.strip()]

    elif symbol_cost_path.is_dir():
        preferred: List[Path] = []
        for pat in ["*.csv", "*.json", "*.txt"]:
            preferred.extend(sorted(symbol_cost_path.rglob(pat)))
        if preferred:
            return load_symbols(preferred[0], data_file_map)

    if symbols:
        resolved: List[str] = []
        for s in symbols:
            key = normalize_symbol_text(s)
            p = data_file_map.get(key)
            if p is not None:
                resolved.append(infer_symbol_from_path(p))
        if resolved:
            return sorted(set(resolved))

    return sorted({infer_symbol_from_path(p) for p in data_file_map.values()})


def resolve_symbol_path(symbol: str, data_file_map: Dict[str, Path]) -> Optional[Path]:
    return data_file_map.get(normalize_symbol_text(symbol))


# -----------------------------
# OHLCV loading / indicators
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
            parsed = pd.to_datetime(ts, errors="coerce", utc=False)
            if parsed.notna().mean() > 0.8:
                ts_num = parsed.astype("int64") // 10**9
                ts_num = ts_num.where(parsed.notna(), np.arange(len(df), dtype=np.int64))
                df["timestamp"] = ts_num
            else:
                df["timestamp"] = pd.to_numeric(ts, errors="coerce").ffill().fillna(0).astype("int64")

    usecols = ["timestamp", "open", "high", "low", "close", "volume"]
    df = df[usecols].copy()
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float32")
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce").ffill().fillna(0).astype("int64")
    df = df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    return df


def load_df(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df = standardize_ohlcv_columns(df)
    if len(df) < MIN_BARS:
        raise ValueError(f"bars 부족: {path.name} ({len(df)})")
    return df


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


def pct_change_np(close: pd.Series, n: int) -> pd.Series:
    return close.pct_change(n).replace([np.inf, -np.inf], np.nan).fillna(0.0)


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
    atrp = (atr14 / close.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")

    hh20 = high.rolling(20, min_periods=1).max().astype("float32")
    ll20 = low.rolling(20, min_periods=1).min().astype("float32")
    hh50 = high.rolling(50, min_periods=1).max().astype("float32")
    ll50 = low.rolling(50, min_periods=1).min().astype("float32")

    vol_ma20 = volume.rolling(20, min_periods=1).mean().astype("float32")
    vol_ratio = (volume / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")

    body = (close - open_).abs().astype("float32")
    upper_wick = (high - np.maximum(open_, close)).clip(lower=0).astype("float32")
    lower_wick = (np.minimum(open_, close) - low).clip(lower=0).astype("float32")
    candle_range = (high - low).replace(0, np.nan).astype("float32")
    lower_wick_body = (lower_wick / body.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")
    upper_wick_range = (upper_wick / candle_range).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")

    body_atr = (body / atr14.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")
    close_pos = ((close - low) / candle_range).replace([np.inf, -np.inf], np.nan).fillna(0.5).astype("float32")

    range20 = (hh20 - ll20).astype("float32")
    range50 = (hh50 - ll50).astype("float32")
    range20_pct = (range20 / close.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")
    range50_pct = (range50 / close.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float32")

    ret1 = pct_change_np(close, 1).astype("float32")
    ret3 = pct_change_np(close, 3).astype("float32")
    ret5 = pct_change_np(close, 5).astype("float32")
    ret10 = pct_change_np(close, 10).astype("float32")
    ret20 = pct_change_np(close, 20).astype("float32")

    trend_up = ((ema20 > ema50) & (ema50 > ema100)).to_numpy(dtype=np.bool_)
    trend_down = ((ema20 < ema50) & (ema50 < ema100)).to_numpy(dtype=np.bool_)

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
        lower_wick_body=lower_wick_body.to_numpy(dtype=np.float32),
        upper_wick_range=upper_wick_range.to_numpy(dtype=np.float32),
        candle_range=candle_range.fillna(0.0).to_numpy(dtype=np.float32),
        close_pos=close_pos.to_numpy(dtype=np.float32),
        range20=range20.to_numpy(dtype=np.float32),
        range50=range50.to_numpy(dtype=np.float32),
        range20_pct=range20_pct.to_numpy(dtype=np.float32),
        range50_pct=range50_pct.to_numpy(dtype=np.float32),
        ret1=ret1.to_numpy(dtype=np.float32),
        ret3=ret3.to_numpy(dtype=np.float32),
        ret5=ret5.to_numpy(dtype=np.float32),
        ret10=ret10.to_numpy(dtype=np.float32),
        ret20=ret20.to_numpy(dtype=np.float32),
        trend_up=trend_up,
        trend_down=trend_down,
    )


# -----------------------------
# Metric functions
# -----------------------------
def equity_curve_from_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[np.ndarray, bool]:
    if not trade_pnls_pct:
        return np.array([1.0], dtype=np.float64), False

    eq = [1.0]
    cur = 1.0
    ruined = False
    for pnl_pct in trade_pnls_pct:
        step = 1.0 + POSITION_FRACTION * (float(pnl_pct) / 100.0)
        if step <= 0.0:
            cur = 0.0
            eq.append(cur)
            ruined = True
            break
        cur *= step
        if cur <= 1e-12:
            cur = 0.0
            eq.append(cur)
            ruined = True
            break
        eq.append(cur)
    return np.asarray(eq, dtype=np.float64), ruined


def max_drawdown_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    peaks = np.maximum.accumulate(equity_curve)
    dd = (equity_curve / np.where(peaks == 0, 1.0, peaks) - 1.0) * 100.0
    return float(abs(np.min(dd))) if dd.size else 0.0


def max_return_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    return float((np.max(equity_curve) - 1.0) * 100.0)


def ratio_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    if max_drawdown_pct <= 0.0:
        return float(max_return_pct) if max_return_pct > 0 else 0.0
    return float(max_return_pct / max_drawdown_pct)


def user_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    if max_drawdown_pct >= 100.0:
        return 0.0
    return float((100.0 * (1.0 - abs(max_drawdown_pct) / 100.0)) * (1.0 + max_return_pct / 100.0))


def summarize_trade_pnls(trade_pnls_pct: List[float]) -> Tuple[float, float, float, float, float, bool]:
    eq, ruined = equity_curve_from_trade_pnls(trade_pnls_pct)
    max_return_pct = max_return_pct_from_equity(eq)
    final_return_pct = float((eq[-1] - 1.0) * 100.0)
    max_dd_pct = max_drawdown_pct_from_equity(eq)

    if ruined or max_dd_pct >= 99.9999:
        final_return_pct = -100.0
        max_dd_pct = 100.0
        max_return_pct = max(0.0, max_return_pct)
        cd = 0.0
        legacy_cd = 0.0
        ruined = True
    else:
        cd = user_cd_value(max_return_pct, max_dd_pct)
        legacy_cd = ratio_cd_value(max_return_pct, max_dd_pct)

    return (
        float(final_return_pct),
        float(max_return_pct),
        float(max_dd_pct),
        float(cd),
        float(legacy_cd),
        bool(ruined),
    )


# -----------------------------
# Strategy generation
# -----------------------------
def make_spec(
    idx: int,
    parent_label: str,
    parent_code: str,
    family: str,
    group: str,
    require_rare22: bool,
    require_shocklow: bool,
    profile: Dict[str, Any],
    side: str,
) -> StrategySpec:
    # naming rule: long_main_v(기준선버전)_(개선안번호)_(전략명) 형태를 직접 반영한다.
    # parent_code examples: long_main_v1, long_max_v1, short_main_v1, short_max_v1
    code = f"{parent_code}_{idx}_{group}_{profile['tag']}"
    cd = int(profile.get("cooldown_bars", 10))
    refire40 = bool(profile.get("refire40_gate", False))
    if refire40:
        cd = max(cd, 40)

    return StrategySpec(
        name=code,
        parent=parent_label,
        family=family,
        group=group,
        side=side,
        description=(
            f"8V12 long/short main/max no-trade-cap improvement from {parent_label}; side={side}; group={group}; "
            f"tag={profile['tag']}; focus={profile.get('focus', '')}"
        ),
        atr_stop=float(profile.get("atr_stop", 1.12)),
        rr_target=float(profile.get("rr_target", 2.0)),
        max_hold_bars=int(profile.get("max_hold_bars", 18)),
        cooldown_bars=cd,
        ret3_drop=float(profile.get("ret3_drop", -0.038)),
        ret5_drop=float(profile.get("ret5_drop", -0.055)),
        ret10_drop=float(profile.get("ret10_drop", -0.075)),
        close_pos_min=float(profile.get("close_pos_min", 0.72)),
        body_atr_min=float(profile.get("body_atr_min", 0.36)),
        vol_ratio_min=float(profile.get("vol_ratio_min", 1.45)),
        atrp_min=float(profile.get("atrp_min", 0.0035)),
        atrp_max=float(profile.get("atrp_max", 0.060)),
        range20_min=float(profile.get("range20_min", 0.010)),
        range20_max=float(profile.get("range20_max", 0.240)),
        require_green=bool(profile.get("require_green", True)),
        require_reclaim=bool(profile.get("require_reclaim", True)),
        require_rare22=bool(require_rare22 or profile.get("require_rare22", False)),
        require_shocklow=bool(require_shocklow or profile.get("require_shocklow", False)),
        strict_gate=bool(profile.get("strict_gate", False)),
        lowanchor_gate=bool(profile.get("lowanchor_gate", False)),
        spring_gate=bool(profile.get("spring_gate", False)),
        refire40_gate=refire40,
        microguard_gate=bool(profile.get("microguard_gate", False)),
        low_break_buffer=float(profile.get("low_break_buffer", 0.0000)),
        reclaim_buffer=float(profile.get("reclaim_buffer", 0.0000)),
        lower_wick_body_min=float(profile.get("lower_wick_body_min", 0.0)),
        upper_wick_range_max=float(profile.get("upper_wick_range_max", 0.92)),
        ema_guard=str(profile.get("ema_guard", "none")),
        breakeven_after_r=float(profile.get("breakeven_after_r", 999.0)),
        trail_after_r=float(profile.get("trail_after_r", 999.0)),
        trail_atr_mult=float(profile.get("trail_atr_mult", 1.8)),
        fail_exit_bars=int(profile.get("fail_exit_bars", 999)),
        fail_exit_pnl_pct=float(profile.get("fail_exit_pnl_pct", -999.0)),
        fail_exit_close_pos_max=float(profile.get("fail_exit_close_pos_max", 0.35)),
        safe_branch_mode=str(profile.get("safe_branch_mode", "none")),
        entry_brake_mode=str(profile.get("entry_brake_mode", "none")),
        chop_guard_mode=str(profile.get("chop_guard_mode", "none")),
        exit_mode=str(profile.get("exit_mode", "none")),
        loss_brake_after=int(profile.get("loss_brake_after", 0)),
        loss_brake_bars=int(profile.get("loss_brake_bars", 0)),
        loss_brake_pnl_pct=float(profile.get("loss_brake_pnl_pct", -0.55)),
        symbol_dd_brake_pct=float(profile.get("symbol_dd_brake_pct", 0.0)),
        symbol_dd_brake_bars=int(profile.get("symbol_dd_brake_bars", 0)),
        recent_shock_lookback=int(profile.get("recent_shock_lookback", 0)),
        recent_shock_ret=float(profile.get("recent_shock_ret", -0.045)),
        recent_shock_range_pct=float(profile.get("recent_shock_range_pct", 0.045)),
        recent_shock_close_pos_max=float(profile.get("recent_shock_close_pos_max", 0.32)),
    )


def base_safe6v2_profile() -> Dict[str, Any]:
    return {
        "tag": "base",
        "focus": "official MDD<5 cd_value leader: 6V2_L01_doubleflush_core",
        "atr_stop": 1.04,
        "rr_target": 1.85,
        "max_hold_bars": 18,
        "cooldown_bars": 10,
        "ret3_drop": -0.036,
        "ret5_drop": -0.052,
        "ret10_drop": -0.070,
        "close_pos_min": 0.72,
        "body_atr_min": 0.34,
        "vol_ratio_min": 1.35,
        "atrp_min": 0.0030,
        "atrp_max": 0.070,
        "range20_min": 0.012,
        "range20_max": 0.180,
        "require_green": True,
        "require_reclaim": True,
        "require_rare22": False,
        "require_shocklow": True,
        "microguard_gate": True,
        "lower_wick_body_min": 0.15,
        "upper_wick_range_max": 0.82,
        "ema_guard": "avoid_trend_down",
        "fail_exit_bars": 6,
        "fail_exit_pnl_pct": -0.35,
        "fail_exit_close_pos_max": 0.42,
        "safe_branch_mode": "trend_repair_only",
        "entry_brake_mode": "none",
        "chop_guard_mode": "avoid_deep_down_no_reclaim",
        "exit_mode": "none",
    }


def base_rawv51_profile() -> Dict[str, Any]:
    return {
        "tag": "base",
        "focus": "unrestricted cd_value leader: 8V4_V51_V002_core_rare22_c1",
        "atr_stop": 1.10,
        "rr_target": 2.05,
        "max_hold_bars": 22,
        "cooldown_bars": 6,
        "ret3_drop": -0.038,
        "ret5_drop": -0.055,
        "ret10_drop": -0.075,
        "close_pos_min": 0.70,
        "body_atr_min": 0.32,
        "vol_ratio_min": 1.35,
        "atrp_min": 0.0035,
        "atrp_max": 0.095,
        "range20_min": 0.010,
        "range20_max": 0.240,
        "require_green": True,
        "require_reclaim": True,
        "require_rare22": True,
        "require_shocklow": False,
        "microguard_gate": False,
        "lower_wick_body_min": 0.00,
        "upper_wick_range_max": 0.92,
        "ema_guard": "none",
        "safe_branch_mode": "none",
        "entry_brake_mode": "none",
        "chop_guard_mode": "none",
        "exit_mode": "none",
    }


def with_overrides(base: Dict[str, Any], tag: str, focus: str, **kw: Any) -> Dict[str, Any]:
    p = dict(base)
    p.update(kw)
    p["tag"] = tag
    p["focus"] = focus
    return p


def cy(seq: List[Any], k: int) -> Any:
    return seq[k % len(seq)]



def safe6v2_profile(group_id: int, k: int) -> Tuple[str, Dict[str, Any]]:
    """
    8V9-A: 현재 공식 long 기준선(6V2_L01_doubleflush_core) 100개 개선.
    8V8에서 이미 시도한 density-release / loss-cluster / graft / exit-first를 반복하지 않고,
    거래수 제한 없이 다음 새 조건축만 사용한다.
    - dryup -> reaccel: 직전 수축 이후 현재 회수 강도
    - absorption-floor: 저점 이탈 후 아래꼬리 흡수
    - shelf-repair: EMA20/EMA50 선반 회복
    - followthrough-exit: 진입 후 2~4봉 안에 반응이 없으면 절단
    """
    b = base_safe6v2_profile()
    group_names = [
        "safe_dryup_reaccel",
        "safe_absorption_floor",
        "safe_shelf_repair",
        "safe_followthrough_exit",
    ]
    group = group_names[group_id]
    j = group_id * 25 + k + 1

    if group_id == 0:
        # 공식 기준선의 강점인 안정성은 유지하되, 직전 수축 후 재가속되는 구간을 추가로 선별한다.
        common = dict(
            atr_stop=cy([0.90, 0.96, 1.02, 1.08, 1.16], k),
            rr_target=cy([1.62, 1.74, 1.86, 2.02, 2.18], k // 2),
            max_hold_bars=cy([14, 16, 18, 21, 24], k // 3),
            cooldown_bars=cy([0, 2, 4, 6, 8], k // 4),
            ret3_drop=cy([-0.030, -0.035, -0.040, -0.046, -0.052], k),
            ret5_drop=cy([-0.044, -0.050, -0.057, -0.064, -0.072], k // 2),
            ret10_drop=cy([-0.060, -0.070, -0.082, -0.094, -0.108], k // 3),
            close_pos_min=cy([0.72, 0.75, 0.78, 0.81, 0.84], k),
            body_atr_min=cy([0.26, 0.32, 0.38, 0.45, 0.52], k // 2),
            vol_ratio_min=cy([1.20, 1.32, 1.45, 1.58, 1.72], k // 3),
            atrp_max=cy([0.058, 0.064, 0.070, 0.078, 0.086], k // 4),
            lower_wick_body_min=cy([0.05, 0.12, 0.20, 0.32, 0.45], k // 2),
            upper_wick_range_max=cy([0.58, 0.66, 0.74, 0.82], k // 4),
            ema_guard=cy(["none", "avoid_trend_down", "reclaim_ema20"], k // 5),
            safe_branch_mode=cy(["vol_dryup_reaccel", "compression_then_reclaim", "shelf_or_sweep", "reversal_followthrough"], k),
            entry_brake_mode=cy(["prev_red_climax_no_reclaim", "two_bar_slide_no_absorb", "bounce_failure", "none"], k // 4),
            chop_guard_mode=cy(["avoid_thin_reclaim", "avoid_vshape_chase", "avoid_low_quality_melt", "none"], k // 5),
            exit_mode=cy(["followthrough_or_cut", "runner_if_strong", "quick_repair", "none"], k // 3),
            fail_exit_bars=cy([3, 4, 5, 6], k // 2),
            fail_exit_pnl_pct=cy([-0.10, -0.18, -0.26, -0.36], k // 3),
            fail_exit_close_pos_max=cy([0.36, 0.42, 0.50, 0.58], k // 4),
            microguard_gate=(k % 5 in [1, 4]),
        )
        focus = "official leader dryup-to-reaccel without trade-count cap"
    elif group_id == 1:
        # 급락 직후 무조건 회피가 아니라, 아래꼬리 흡수와 저점 회수 품질이 있는 경우만 살린다.
        common = dict(
            atr_stop=cy([0.82, 0.88, 0.96, 1.04, 1.14], k),
            rr_target=cy([1.48, 1.60, 1.74, 1.92, 2.08], k // 2),
            max_hold_bars=cy([10, 12, 15, 18, 22], k // 3),
            cooldown_bars=cy([0, 2, 5, 8, 12], k // 4),
            ret3_drop=cy([-0.034, -0.041, -0.048, -0.056, -0.064], k),
            ret5_drop=cy([-0.050, -0.058, -0.067, -0.077, -0.090], k // 2),
            ret10_drop=cy([-0.070, -0.084, -0.098, -0.114, -0.132], k // 3),
            close_pos_min=cy([0.74, 0.78, 0.82, 0.86], k),
            body_atr_min=cy([0.22, 0.30, 0.38, 0.48, 0.60], k // 2),
            vol_ratio_min=cy([1.25, 1.42, 1.60, 1.82, 2.05], k // 3),
            atrp_max=cy([0.052, 0.060, 0.070, 0.082, 0.096], k // 4),
            lower_wick_body_min=cy([0.20, 0.35, 0.55, 0.80, 1.10], k),
            upper_wick_range_max=cy([0.52, 0.62, 0.72, 0.82], k // 5),
            ema_guard=cy(["none", "avoid_trend_down"], k // 4),
            safe_branch_mode=cy(["double_sweep_absorption", "multi_low_reclaim", "capitulation_absorb_only", "strict_lowanchor_and_dryup"], k),
            entry_brake_mode=cy(["lower_low_no_body", "prev_red_climax_no_reclaim", "two_bar_slide_no_absorb", "none"], k // 3),
            chop_guard_mode=cy(["avoid_liquidity_void", "avoid_low_quality_melt", "avoid_thin_reclaim", "none"], k // 4),
            exit_mode=cy(["shock_tight_then_trail", "followthrough_or_cut", "loss_cluster_quarantine", "none"], k // 3),
            fail_exit_bars=cy([2, 3, 4, 5], k // 2),
            fail_exit_pnl_pct=cy([-0.08, -0.16, -0.25, -0.34], k // 3),
            fail_exit_close_pos_max=cy([0.34, 0.40, 0.48, 0.56], k // 4),
            microguard_gate=(k % 4 == 0),
        )
        focus = "official leader absorption-floor for MDD compression without starving trades"
    elif group_id == 2:
        # 추세 하락 전체 차단 대신, EMA20/50 회복 선반이 있는 구간만 선택한다.
        common = dict(
            atr_stop=cy([0.92, 1.00, 1.08, 1.18, 1.30], k),
            rr_target=cy([1.70, 1.88, 2.05, 2.28, 2.52], k // 2),
            max_hold_bars=cy([16, 19, 22, 26, 30], k // 3),
            cooldown_bars=cy([0, 3, 6, 9], k // 4),
            ret3_drop=cy([-0.026, -0.032, -0.039, -0.047, -0.056], k),
            ret5_drop=cy([-0.040, -0.048, -0.058, -0.070, -0.084], k // 2),
            ret10_drop=cy([-0.058, -0.070, -0.086, -0.104, -0.124], k // 3),
            close_pos_min=cy([0.70, 0.74, 0.78, 0.82], k),
            body_atr_min=cy([0.24, 0.32, 0.42, 0.54], k // 2),
            vol_ratio_min=cy([1.18, 1.30, 1.44, 1.60, 1.78], k // 3),
            atrp_max=cy([0.060, 0.070, 0.082, 0.096, 0.110], k // 4),
            lower_wick_body_min=cy([0.00, 0.10, 0.20, 0.35, 0.55], k),
            ema_guard=cy(["reclaim_ema20", "reclaim_ema50", "none"], k // 5),
            safe_branch_mode=cy(["ema_shelf_repair", "shelf_or_sweep", "compression_then_reclaim", "reversal_followthrough"], k),
            entry_brake_mode=cy(["ema20_reject_recent", "bounce_failure", "two_bar_slide_no_absorb", "none"], k // 4),
            chop_guard_mode=cy(["avoid_upper_supply", "avoid_thin_reclaim", "avoid_low_quality_melt", "none"], k // 5),
            exit_mode=cy(["shelf_runner", "runner_if_strong", "followthrough_or_cut", "none"], k // 3),
            breakeven_after_r=cy([0.80, 1.00, 1.20, 999.0], k // 2),
            trail_after_r=cy([1.20, 1.50, 1.80, 999.0], k // 3),
            trail_atr_mult=cy([0.90, 1.10, 1.35, 1.70], k // 4),
            fail_exit_bars=cy([4, 5, 6, 8], k // 2),
            fail_exit_pnl_pct=cy([-0.12, -0.22, -0.34, -0.48], k // 3),
        )
        focus = "official leader EMA shelf repair and runner preservation"
    else:
        # 진입 필터보다 사후 반응 판정 중심. 거래수는 제한하지 않고 품질 낮은 진입만 빠르게 자른다.
        common = dict(
            atr_stop=cy([0.78, 0.86, 0.96, 1.08, 1.22], k),
            rr_target=cy([1.40, 1.56, 1.76, 2.04, 2.36], k // 2),
            max_hold_bars=cy([8, 11, 14, 18, 24], k // 3),
            cooldown_bars=cy([0, 1, 3, 5, 8], k // 4),
            ret3_drop=cy([-0.028, -0.036, -0.044, -0.054, -0.066], k),
            ret5_drop=cy([-0.042, -0.052, -0.064, -0.078, -0.096], k // 2),
            ret10_drop=cy([-0.060, -0.076, -0.094, -0.114, -0.138], k // 3),
            close_pos_min=cy([0.72, 0.76, 0.80, 0.84], k),
            body_atr_min=cy([0.22, 0.30, 0.40, 0.52], k // 2),
            vol_ratio_min=cy([1.15, 1.30, 1.48, 1.70, 1.95], k // 3),
            atrp_max=cy([0.052, 0.064, 0.078, 0.094], k // 4),
            lower_wick_body_min=cy([0.00, 0.15, 0.35, 0.65], k),
            safe_branch_mode=cy(["reversal_followthrough", "vol_dryup_reaccel", "double_sweep_absorption", "ema_shelf_repair"], k),
            entry_brake_mode=cy(["bounce_failure", "ema20_reject_recent", "lower_low_no_body", "none"], k // 4),
            chop_guard_mode=cy(["avoid_vshape_chase", "avoid_upper_supply", "avoid_liquidity_void", "none"], k // 5),
            exit_mode=cy(["green_fail_cut", "volfade_cut", "followthrough_or_cut", "quick_repair"], k // 3),
            breakeven_after_r=cy([0.70, 0.90, 1.10, 999.0], k // 2),
            trail_after_r=cy([1.00, 1.35, 1.70, 999.0], k // 3),
            trail_atr_mult=cy([0.80, 1.00, 1.25, 1.55], k // 4),
            fail_exit_bars=cy([2, 3, 4, 5], k // 2),
            fail_exit_pnl_pct=cy([-0.06, -0.14, -0.24, -0.36], k // 3),
            loss_brake_after=cy([0, 1, 2, 3], k // 4),
            loss_brake_bars=cy([0, 4, 8, 12], k // 5),
        )
        focus = "official leader reaction-based exits with no trade-count cap"

    return group, with_overrides(b, tag=f"s{j:03d}", focus=focus, **common)


def rawv51_profile(group_id: int, k: int) -> Tuple[str, Dict[str, Any]]:
    """
    8V9-B: 현재 MDD 무관 cd_value 1위(8V4_V51_V002_core_rare22_c1) 100개 개선.
    V51 장점인 rare22/저점 회수/수익 확장성은 유지하되, 직전 시도와 겹치지 않도록
    dryup, absorption, shelf, followthrough 조건축으로 MDD를 압축한다.
    """
    b = base_rawv51_profile()
    group_names = [
        "raw_dryup_reaccel",
        "raw_absorption_mdd_cut",
        "raw_shelf_conversion",
        "raw_followthrough_runner",
    ]
    group = group_names[group_id]
    j = group_id * 25 + k + 1

    if group_id == 0:
        common = dict(
            atr_stop=cy([0.94, 1.02, 1.10, 1.20, 1.32], k),
            rr_target=cy([1.86, 2.05, 2.26, 2.50, 2.78], k // 2),
            max_hold_bars=cy([16, 20, 24, 28, 34], k // 3),
            cooldown_bars=cy([0, 2, 4, 6], k // 4),
            ret3_drop=cy([-0.032, -0.038, -0.046, -0.055, -0.066], k),
            ret5_drop=cy([-0.048, -0.056, -0.066, -0.080, -0.096], k // 2),
            ret10_drop=cy([-0.068, -0.082, -0.100, -0.122, -0.148], k // 3),
            close_pos_min=cy([0.70, 0.74, 0.78, 0.82], k),
            body_atr_min=cy([0.24, 0.32, 0.42, 0.54], k // 2),
            vol_ratio_min=cy([1.22, 1.38, 1.56, 1.78, 2.05], k // 3),
            atrp_max=cy([0.070, 0.084, 0.100, 0.118], k // 4),
            lower_wick_body_min=cy([0.00, 0.12, 0.28, 0.50, 0.85], k),
            upper_wick_range_max=cy([0.62, 0.72, 0.82, 0.92], k // 5),
            ema_guard=cy(["none", "reclaim_ema20", "avoid_trend_down"], k // 5),
            safe_branch_mode=cy(["vol_dryup_reaccel", "compression_then_reclaim", "strict_lowanchor_and_dryup", "reversal_followthrough"], k),
            entry_brake_mode=cy(["prev_red_climax_no_reclaim", "two_bar_slide_no_absorb", "lower_low_no_body", "none"], k // 4),
            chop_guard_mode=cy(["avoid_thin_reclaim", "avoid_liquidity_void", "avoid_vshape_chase", "none"], k // 5),
            exit_mode=cy(["runner_if_strong", "followthrough_or_cut", "shock_tight_then_trail", "none"], k // 3),
            fail_exit_bars=cy([3, 4, 5, 6], k // 2),
            fail_exit_pnl_pct=cy([-0.10, -0.20, -0.32, -0.48], k // 3),
        )
        focus = "raw V51 dryup-to-reaccel MDD compression"
    elif group_id == 1:
        common = dict(
            atr_stop=cy([0.82, 0.90, 1.00, 1.12, 1.26], k),
            rr_target=cy([1.55, 1.72, 1.92, 2.18, 2.50], k // 2),
            max_hold_bars=cy([10, 13, 16, 20, 26], k // 3),
            cooldown_bars=cy([0, 2, 5, 8], k // 4),
            ret3_drop=cy([-0.038, -0.046, -0.056, -0.068, -0.082], k),
            ret5_drop=cy([-0.055, -0.066, -0.080, -0.096, -0.116], k // 2),
            ret10_drop=cy([-0.080, -0.100, -0.122, -0.148, -0.178], k // 3),
            close_pos_min=cy([0.76, 0.80, 0.84, 0.88], k),
            body_atr_min=cy([0.22, 0.32, 0.44, 0.58], k // 2),
            vol_ratio_min=cy([1.32, 1.55, 1.82, 2.12], k // 3),
            atrp_max=cy([0.060, 0.074, 0.090, 0.108], k // 4),
            lower_wick_body_min=cy([0.30, 0.55, 0.85, 1.20], k),
            upper_wick_range_max=cy([0.50, 0.60, 0.72, 0.84], k // 5),
            ema_guard=cy(["none", "avoid_trend_down"], k // 4),
            safe_branch_mode=cy(["capitulation_absorb_only", "double_sweep_absorption", "multi_low_reclaim", "quality_not_quantity"], k),
            entry_brake_mode=cy(["lower_low_no_body", "prev_red_climax_no_reclaim", "two_bar_slide_no_absorb", "bounce_failure"], k // 3),
            chop_guard_mode=cy(["avoid_liquidity_void", "avoid_low_quality_melt", "avoid_upper_supply", "none"], k // 4),
            exit_mode=cy(["shock_tight_then_trail", "quick_repair", "followthrough_or_cut", "loss_cluster_quarantine"], k // 3),
            fail_exit_bars=cy([2, 3, 4, 5], k // 2),
            fail_exit_pnl_pct=cy([-0.08, -0.16, -0.26, -0.40], k // 3),
            force_shocklow=(k % 3 != 1),
        )
        focus = "raw V51 absorption floor to cut MDD spikes"
    elif group_id == 2:
        common = dict(
            atr_stop=cy([0.96, 1.06, 1.18, 1.32, 1.48], k),
            rr_target=cy([1.90, 2.14, 2.42, 2.74, 3.10], k // 2),
            max_hold_bars=cy([18, 22, 27, 33, 40], k // 3),
            cooldown_bars=cy([0, 3, 6, 9], k // 4),
            ret3_drop=cy([-0.028, -0.035, -0.044, -0.055], k),
            ret5_drop=cy([-0.042, -0.052, -0.066, -0.082], k // 2),
            ret10_drop=cy([-0.062, -0.078, -0.098, -0.122, -0.150], k // 3),
            close_pos_min=cy([0.68, 0.72, 0.76, 0.80], k),
            body_atr_min=cy([0.20, 0.30, 0.42, 0.56], k // 2),
            vol_ratio_min=cy([1.14, 1.28, 1.46, 1.68], k // 3),
            atrp_max=cy([0.076, 0.092, 0.110, 0.130], k // 4),
            lower_wick_body_min=cy([0.00, 0.10, 0.25, 0.45], k),
            ema_guard=cy(["reclaim_ema20", "reclaim_ema50", "none"], k // 5),
            safe_branch_mode=cy(["ema_shelf_repair", "shelf_or_sweep", "compression_then_reclaim", "reversal_followthrough"], k),
            entry_brake_mode=cy(["ema20_reject_recent", "bounce_failure", "prev_red_climax_no_reclaim", "none"], k // 4),
            chop_guard_mode=cy(["avoid_upper_supply", "avoid_thin_reclaim", "avoid_vshape_chase", "none"], k // 5),
            exit_mode=cy(["shelf_runner", "runner_if_strong", "volfade_cut", "none"], k // 3),
            breakeven_after_r=cy([0.90, 1.15, 1.40, 999.0], k // 2),
            trail_after_r=cy([1.35, 1.70, 2.05, 999.0], k // 3),
            trail_atr_mult=cy([0.95, 1.20, 1.55, 2.00], k // 4),
            fail_exit_bars=cy([4, 5, 7, 9], k // 2),
            fail_exit_pnl_pct=cy([-0.12, -0.24, -0.38, -0.56], k // 3),
        )
        focus = "raw V51 EMA shelf conversion for official promotion"
    else:
        common = dict(
            atr_stop=cy([0.86, 0.96, 1.08, 1.24, 1.42], k),
            rr_target=cy([1.62, 1.84, 2.12, 2.50, 2.95], k // 2),
            max_hold_bars=cy([9, 12, 16, 22, 30], k // 3),
            cooldown_bars=cy([0, 1, 3, 6], k // 4),
            ret3_drop=cy([-0.030, -0.040, -0.052, -0.066], k),
            ret5_drop=cy([-0.046, -0.060, -0.078, -0.100], k // 2),
            ret10_drop=cy([-0.066, -0.086, -0.112, -0.146], k // 3),
            close_pos_min=cy([0.72, 0.76, 0.80, 0.86], k),
            body_atr_min=cy([0.20, 0.30, 0.42, 0.58], k // 2),
            vol_ratio_min=cy([1.18, 1.36, 1.60, 1.90], k // 3),
            atrp_max=cy([0.066, 0.082, 0.100, 0.120], k // 4),
            lower_wick_body_min=cy([0.00, 0.15, 0.35, 0.70], k),
            safe_branch_mode=cy(["reversal_followthrough", "vol_dryup_reaccel", "capitulation_absorb_only", "ema_shelf_repair"], k),
            entry_brake_mode=cy(["bounce_failure", "ema20_reject_recent", "lower_low_no_body", "none"], k // 4),
            chop_guard_mode=cy(["avoid_liquidity_void", "avoid_upper_supply", "avoid_low_quality_melt", "none"], k // 5),
            exit_mode=cy(["green_fail_cut", "volfade_cut", "followthrough_or_cut", "runner_if_strong"], k // 3),
            breakeven_after_r=cy([0.75, 1.00, 1.30, 999.0], k // 2),
            trail_after_r=cy([1.10, 1.45, 1.85, 999.0], k // 3),
            trail_atr_mult=cy([0.85, 1.10, 1.45, 1.85], k // 4),
            fail_exit_bars=cy([2, 3, 4, 6], k // 2),
            fail_exit_pnl_pct=cy([-0.06, -0.16, -0.28, -0.46], k // 3),
        )
        focus = "raw V51 followthrough runner/fast-cut balance"

    return group, with_overrides(b, tag=f"r{j:03d}", focus=focus, **common)




def base_short_main_profile() -> Dict[str, Any]:
    """short_main_v1 계열: MDD 5% 미만 공식 기준선의 장점(손실 제어)을 유지하면서 하락 추세 재가속/상단 거부만 새로 선별한다."""
    return {
        "tag": "base",
        "focus": "short main official baseline improvement",
        "atr_stop": 1.05,
        "rr_target": 2.20,
        "max_hold_bars": 22,
        "cooldown_bars": 3,
        "ret3_drop": 0.032,
        "ret5_drop": 0.050,
        "ret10_drop": 0.074,
        "close_pos_min": 0.68,
        "body_atr_min": 0.28,
        "vol_ratio_min": 1.18,
        "atrp_min": 0.004,
        "atrp_max": 0.090,
        "range20_min": 0.012,
        "range20_max": 0.230,
        "require_green": True,       # short에서는 red candle requirement로 해석된다.
        "require_reclaim": True,     # short에서는 upper sweep rejection으로 해석된다.
        "require_rare22": False,
        "require_shocklow": False,
        "low_break_buffer": 0.0000,
        "reclaim_buffer": 0.0000,
        "lower_wick_body_min": 0.28, # short에서는 upper wick/rejection strength로 해석된다.
        "upper_wick_range_max": 0.88,
        "ema_guard": "avoid_trend_down",
        "breakeven_after_r": 1.10,
        "trail_after_r": 1.80,
        "trail_atr_mult": 1.40,
        "fail_exit_bars": 5,
        "fail_exit_pnl_pct": -0.18,
        "fail_exit_close_pos_max": 0.35,
        "safe_branch_mode": "short_upper_sweep_reject",
        "entry_brake_mode": "none",
        "chop_guard_mode": "none",
        "exit_mode": "short_failfast_then_trail",
        "loss_brake_after": 2,
        "loss_brake_bars": 10,
        "loss_brake_pnl_pct": -0.45,
        "symbol_dd_brake_pct": 2.2,
        "symbol_dd_brake_bars": 18,
        "recent_shock_lookback": 3,
        "recent_shock_ret": 0.045,
        "recent_shock_range_pct": 0.045,
        "recent_shock_close_pos_max": 0.68,
    }


def base_short_max_profile() -> Dict[str, Any]:
    """short_max_v1 계열: raw cd_value 1위의 높은 수익성을 살리되, 상단 숏 추격 실패와 V자 반등 손실을 새 조건으로 제어한다."""
    p = base_short_main_profile()
    p.update({
        "focus": "short max raw cd baseline improvement",
        "atr_stop": 1.28,
        "rr_target": 3.20,
        "max_hold_bars": 36,
        "cooldown_bars": 1,
        "ret3_drop": 0.025,
        "ret5_drop": 0.040,
        "ret10_drop": 0.060,
        "close_pos_min": 0.60,
        "body_atr_min": 0.18,
        "vol_ratio_min": 1.00,
        "atrp_max": 0.135,
        "range20_max": 0.330,
        "lower_wick_body_min": 0.16,
        "upper_wick_range_max": 0.94,
        "safe_branch_mode": "short_breakdown_reaccel",
        "exit_mode": "short_runner_if_strong",
        "loss_brake_after": 0,
        "loss_brake_bars": 0,
        "symbol_dd_brake_pct": 0.0,
        "symbol_dd_brake_bars": 0,
    })
    return p


def tune_profile_for_8v12(kind: str, idx: int, base: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """8V12: 8V11에서 이미 쓴 liquidity/squeeze/ema50/volume-climax 계열을 반복하지 않고,
    구조 전환, 변동성 수축-확장, 실패 돌파/실패 이탈, MA 기울기 대용치, DD 완화형 exit을 새 축으로만 구성한다.
    단순 파라미터 조정 배치가 아니라 조건 해석축 자체를 교체한다.
    """
    p = dict(base)
    # allow safe arithmetic before make_spec applies final StrategySpec defaults
    p.setdefault("reclaim_buffer", 0.0)
    p.setdefault("low_break_buffer", 0.0)
    p.setdefault("trail_after_r", 999.0)
    p.setdefault("trail_atr_mult", 1.8)
    p.setdefault("fail_exit_pnl_pct", -0.35 if not kind.startswith("short") else -0.45)
    p.setdefault("cooldown_bars", 10)
    p.setdefault("recent_shock_lookback", 0)
    k = idx % 20
    lane = idx // 20

    def cy(vals: List[Any], offset: int = 0) -> Any:
        return vals[(k + offset) % len(vals)]

    if kind == "long_main":
        groups = [
            "lm12_regime_flip_repair",
            "lm12_vol_contract_expand",
            "lm12_ema20_slope_proxy",
            "lm12_failed_breakdown_inside",
            "lm12_dd_sanitizer",
        ]
        group = groups[lane]
        p.update({
            "tag": f"lm12_{lane}_{k:02d}",
            "safe_branch_mode": ["long_regime_flip_repair", "long_vol_contract_expand", "long_ema20_slope_proxy", "long_failed_breakdown_inside", "long_dd_sanitized_reclaim"][lane],
            "entry_brake_mode": cy(["overhead_compression_recent", "bear_body_cluster", "thin_green_reversal", "ema100_below_pressure", "no_reclaim_after_gap"], lane),
            "chop_guard_mode": cy(["avoid_midrange_no_edge", "avoid_ema100_ceiling", "avoid_ret20_overheat", "avoid_low_volume_wide", "avoid_one_bar_spike"], lane),
            "exit_mode": cy(["mfe_lock_fast", "time_decay_runner", "atr_band_trail", "two_stage_take", "dd_sensitive_fast"], lane),
            "microguard_gate": True,
            "lowanchor_gate": cy([True, True, False, True, False], lane),
            "strict_gate": cy([True, False, True, True, False], lane),
            "require_rare22": cy([False, False, True, False], lane),
            "require_shocklow": cy([False, True, False, False, True], lane),
            "loss_brake_after": cy([1, 2, 2, 1], lane),
            "loss_brake_bars": cy([8, 12, 16, 20], lane),
            "symbol_dd_brake_pct": cy([1.20, 1.45, 1.70, 2.00], lane),
            "symbol_dd_brake_bars": cy([12, 18, 24, 30], lane),
            "recent_shock_lookback": cy([2, 3, 4, 5], lane),
        })
        if lane == 0:
            p.update({"close_pos_min": max(p["close_pos_min"], 0.76), "vol_ratio_min": max(p["vol_ratio_min"], 1.10), "rr_target": max(p["rr_target"], 2.05), "max_hold_bars": min(max(p["max_hold_bars"], 16), 26)})
        elif lane == 1:
            p.update({"range20_max": min(p["range20_max"], 0.145), "atrp_max": min(p["atrp_max"], 0.072), "vol_ratio_min": max(p["vol_ratio_min"], 1.18), "body_atr_min": max(p["body_atr_min"], 0.24)})
        elif lane == 2:
            p.update({"ema_guard": cy(["reclaim_ema20", "avoid_trend_down", "reclaim_ema50"], lane), "ret3_drop": min(p["ret3_drop"], -0.018), "close_pos_min": max(p["close_pos_min"], 0.72)})
        elif lane == 3:
            p.update({"lower_wick_body_min": max(p["lower_wick_body_min"], 0.28), "reclaim_buffer": max(p["reclaim_buffer"], 0.0005), "body_atr_min": max(p["body_atr_min"], 0.20)})
        else:
            p.update({"atr_stop": min(p["atr_stop"], 1.06), "rr_target": min(max(p["rr_target"], 1.80), 2.35), "max_hold_bars": min(p["max_hold_bars"], 18), "cooldown_bars": max(p["cooldown_bars"], 4)})
        return group, p

    if kind == "long_max":
        groups = [
            "lx12_range_expansion_runner",
            "lx12_pullback_continuation",
            "lx12_second_leg_absorption",
            "lx12_ema_band_reentry",
            "lx12_asymmetric_trail",
        ]
        group = groups[lane]
        p.update({
            "tag": f"lx12_{lane}_{k:02d}",
            "safe_branch_mode": ["long_range_expansion_runner", "long_pullback_continuation", "long_second_leg_absorption", "long_ema_band_reentry", "long_asymmetric_runner_reclaim"][lane],
            "entry_brake_mode": cy(["overhead_compression_recent", "no_reclaim_after_gap", "bear_body_cluster", "ema100_below_pressure", "thin_green_reversal"], lane),
            "chop_guard_mode": cy(["avoid_one_bar_spike", "avoid_midrange_no_edge", "avoid_ret20_overheat", "avoid_low_volume_wide", "avoid_ema100_ceiling"], lane),
            "exit_mode": cy(["atr_band_trail", "time_decay_runner", "two_stage_take", "mfe_lock_fast", "runner_reversal_cut"], lane),
            "microguard_gate": cy([True, False, True, True, False], lane),
            "lowanchor_gate": cy([False, True, False, True, False], lane),
            "strict_gate": cy([False, True, False, False, True], lane),
            "force_rare22": cy([True, True, False, True], lane),
            "force_shocklow": cy([False, False, True, False], lane),
            "loss_brake_after": cy([0, 1, 2, 0, 1], lane),
            "loss_brake_bars": cy([0, 8, 14, 0, 10], lane),
            "symbol_dd_brake_pct": cy([0.0, 2.20, 2.80, 0.0, 3.20], lane),
            "symbol_dd_brake_bars": cy([0, 18, 26, 0, 32], lane),
        })
        if lane == 0:
            p.update({"range20_min": max(p["range20_min"], 0.030), "range20_max": min(max(p["range20_max"], 0.180), 0.260), "rr_target": max(p["rr_target"], 2.65), "max_hold_bars": max(p["max_hold_bars"], 28)})
        elif lane == 1:
            p.update({"ret5_drop": min(p["ret5_drop"], -0.030), "close_pos_min": max(p["close_pos_min"], 0.70), "vol_ratio_min": max(p["vol_ratio_min"], 1.02)})
        elif lane == 2:
            p.update({"lower_wick_body_min": max(p["lower_wick_body_min"], 0.24), "vol_ratio_min": max(p["vol_ratio_min"], 1.20), "rr_target": max(p["rr_target"], 2.35)})
        elif lane == 3:
            p.update({"ema_guard": cy(["reclaim_ema20", "reclaim_ema50", "avoid_trend_down"], lane), "atrp_max": min(max(p["atrp_max"], 0.082), 0.115), "range20_max": min(max(p["range20_max"], 0.160), 0.245)})
        else:
            p.update({"atr_stop": min(max(p["atr_stop"], 1.08), 1.42), "trail_after_r": cy([1.20, 1.35, 1.50, 1.65], lane), "trail_atr_mult": cy([1.10, 1.25, 1.40, 1.55], lane), "max_hold_bars": max(p["max_hold_bars"], 30)})
        return group, p

    if kind == "short_main":
        groups = [
            "sm12_regime_flip_reject",
            "sm12_vol_contract_breakdown",
            "sm12_ema20_slope_proxy",
            "sm12_failed_breakout_inside",
            "sm12_dd_sanitizer",
        ]
        group = groups[lane]
        p.update({
            "tag": f"sm12_{lane}_{k:02d}",
            "safe_branch_mode": ["short_regime_flip_reject", "short_vol_contract_breakdown", "short_ema20_slope_proxy", "short_failed_breakout_inside", "short_dd_sanitized_reject"][lane],
            "entry_brake_mode": cy(["underfoot_support_recent", "bull_body_cluster", "thin_red_reversal", "ema100_above_pressure", "no_reject_after_gap"], lane),
            "chop_guard_mode": cy(["short_avoid_midrange_no_edge", "short_avoid_ema100_floor", "short_avoid_ret20_oversold", "short_avoid_low_volume_wide", "short_avoid_one_bar_spike"], lane),
            "exit_mode": cy(["short_mfe_lock_fast", "short_time_decay_runner", "short_atr_band_trail", "short_two_stage_take", "short_dd_sensitive_fast"], lane),
            "microguard_gate": True,
            "lowanchor_gate": cy([True, True, False, True, False], lane),
            "strict_gate": cy([True, False, True, True, False], lane),
            "loss_brake_after": cy([1, 2, 2, 1], lane),
            "loss_brake_bars": cy([8, 12, 16, 20], lane),
            "symbol_dd_brake_pct": cy([1.50, 1.80, 2.10, 2.40], lane),
            "symbol_dd_brake_bars": cy([12, 18, 24, 30], lane),
            "recent_shock_lookback": cy([2, 3, 4, 5], lane),
        })
        if lane == 0:
            p.update({"close_pos_min": max(p["close_pos_min"], 0.72), "vol_ratio_min": max(p["vol_ratio_min"], 1.12), "rr_target": max(p["rr_target"], 2.15), "max_hold_bars": min(max(p["max_hold_bars"], 18), 28)})
        elif lane == 1:
            p.update({"range20_max": min(p["range20_max"], 0.170), "atrp_max": min(p["atrp_max"], 0.078), "vol_ratio_min": max(p["vol_ratio_min"], 1.20), "body_atr_min": max(p["body_atr_min"], 0.24)})
        elif lane == 2:
            p.update({"ema_guard": cy(["reclaim_ema20", "avoid_trend_down", "reclaim_ema50"], lane), "ret3_drop": max(p["ret3_drop"], 0.028), "close_pos_min": max(p["close_pos_min"], 0.68)})
        elif lane == 3:
            p.update({"lower_wick_body_min": max(p["lower_wick_body_min"], 0.28), "reclaim_buffer": max(p["reclaim_buffer"], 0.0005), "body_atr_min": max(p["body_atr_min"], 0.20)})
        else:
            p.update({"atr_stop": min(p["atr_stop"], 1.10), "rr_target": min(max(p["rr_target"], 1.95), 2.45), "max_hold_bars": min(p["max_hold_bars"], 20), "cooldown_bars": max(p["cooldown_bars"], 4)})
        return group, p

    # short_max
    groups = [
        "sx12_range_expansion_runner",
        "sx12_pullback_continuation",
        "sx12_second_leg_reject",
        "sx12_ema_band_reentry",
        "sx12_asymmetric_trail",
    ]
    group = groups[lane]
    p.update({
        "tag": f"sx12_{lane}_{k:02d}",
        "safe_branch_mode": ["short_range_expansion_runner", "short_pullback_continuation", "short_second_leg_reject", "short_ema_band_reentry", "short_asymmetric_runner_reject"][lane],
        "entry_brake_mode": cy(["underfoot_support_recent", "no_reject_after_gap", "bull_body_cluster", "ema100_above_pressure", "thin_red_reversal"], lane),
        "chop_guard_mode": cy(["short_avoid_one_bar_spike", "short_avoid_midrange_no_edge", "short_avoid_ret20_oversold", "short_avoid_low_volume_wide", "short_avoid_ema100_floor"], lane),
        "exit_mode": cy(["short_atr_band_trail", "short_time_decay_runner", "short_two_stage_take", "short_mfe_lock_fast", "short_runner_reversal_cut"], lane),
        "microguard_gate": cy([True, False, True, True, False], lane),
        "lowanchor_gate": cy([False, True, False, True, False], lane),
        "strict_gate": cy([False, True, False, False, True], lane),
        "loss_brake_after": cy([0, 1, 2, 0, 1], lane),
        "loss_brake_bars": cy([0, 8, 14, 0, 10], lane),
        "symbol_dd_brake_pct": cy([0.0, 2.80, 3.40, 0.0, 4.00], lane),
        "symbol_dd_brake_bars": cy([0, 18, 26, 0, 32], lane),
    })
    if lane == 0:
        p.update({"range20_min": max(p["range20_min"], 0.032), "range20_max": min(max(p["range20_max"], 0.200), 0.300), "rr_target": max(p["rr_target"], 3.25), "max_hold_bars": max(p["max_hold_bars"], 34)})
    elif lane == 1:
        p.update({"ret5_drop": max(p["ret5_drop"], 0.044), "close_pos_min": max(p["close_pos_min"], 0.62), "vol_ratio_min": max(p["vol_ratio_min"], 1.02)})
    elif lane == 2:
        p.update({"lower_wick_body_min": max(p["lower_wick_body_min"], 0.22), "vol_ratio_min": max(p["vol_ratio_min"], 1.18), "rr_target": max(p["rr_target"], 2.90)})
    elif lane == 3:
        p.update({"ema_guard": cy(["reclaim_ema20", "reclaim_ema50", "avoid_trend_down"], lane), "atrp_max": min(max(p["atrp_max"], 0.098), 0.145), "range20_max": min(max(p["range20_max"], 0.210), 0.320)})
    else:
        p.update({"atr_stop": min(max(p["atr_stop"], 1.12), 1.60), "trail_after_r": cy([1.25, 1.45, 1.65, 1.85], lane), "trail_atr_mult": cy([1.10, 1.28, 1.46, 1.64], lane), "max_hold_bars": max(p["max_hold_bars"], 38)})
    return group, p


def build_strategies() -> List[StrategySpec]:
    out: List[StrategySpec] = []

    for i in range(100):
        _, base = safe6v2_profile(i // 25, i % 25)
        group, profile = tune_profile_for_8v12("long_main", i, base)
        out.append(make_spec(i + 1, REFERENCE_LONG_MAIN["strategy_name"], "long_main_v1", "long_main_v1_improvements", group, bool(profile.get("require_rare22", False)), bool(profile.get("require_shocklow", False)), profile, "long"))

    for i in range(100):
        _, base = rawv51_profile(i // 25, i % 25)
        group, profile = tune_profile_for_8v12("long_max", i, base)
        out.append(make_spec(i + 1, REFERENCE_LONG_MAX["strategy_name"], "long_max_v1", "long_max_v1_improvements", group, bool(profile.get("force_rare22", True)), bool(profile.get("force_shocklow", False)), profile, "long"))

    for i in range(100):
        base = base_short_main_profile()
        group, profile = tune_profile_for_8v12("short_main", i, base)
        out.append(make_spec(i + 1, REFERENCE_SHORT_MAIN["strategy_name"], "short_main_v1", "short_main_v1_improvements", group, bool(profile.get("require_rare22", False)), bool(profile.get("require_shocklow", False)), profile, "short"))

    for i in range(100):
        base = base_short_max_profile()
        group, profile = tune_profile_for_8v12("short_max", i, base)
        out.append(make_spec(i + 1, REFERENCE_SHORT_MAX["strategy_name"], "short_max_v1", "short_max_v1_improvements", group, bool(profile.get("require_rare22", False)), bool(profile.get("require_shocklow", False)), profile, "short"))

    assert len(out) == 400, f"전략 수 오류: {len(out)}"
    assert len({s.name for s in out}) == len(out), "전략명 중복"
    return out

def shift1(a: np.ndarray, fill: float = np.nan) -> np.ndarray:
    out = np.empty_like(a)
    out[0] = fill
    out[1:] = a[:-1]
    return out


def rolling_any_prev(flag: np.ndarray, lookback: int) -> np.ndarray:
    """True if the condition happened in one of the previous lookback bars.
    Current bar is intentionally excluded so this acts as a short cool-off filter.
    """
    flag = np.asarray(flag, dtype=np.bool_)
    out = np.zeros(flag.size, dtype=np.bool_)
    if lookback <= 0 or flag.size == 0:
        return out
    lb = min(int(lookback), max(0, flag.size - 1))
    for k in range(1, lb + 1):
        out[k:] |= flag[:-k]
    return out



def short_entry_mask(spec: StrategySpec, f: FeaturePack) -> np.ndarray:
    n = f.close.size
    prev_hh20 = shift1(f.hh20, np.nan)
    prev_hh50 = shift1(f.hh50, np.nan)
    prev_ll20 = shift1(f.ll20, np.nan)
    prev_close = shift1(f.close, np.nan)
    prev_open = shift1(f.open, np.nan)
    prev_high = shift1(f.high, np.nan)
    prev_close_pos = shift1(f.close_pos, np.nan)
    prev_vol_ratio = shift1(f.vol_ratio, np.nan)
    range_pct_now = f.candle_range / np.where(f.close == 0, np.nan, f.close)
    prev_range_pct = shift1(range_pct_now, np.nan)

    # short에서는 ret thresholds를 양수 rally 기준으로 사용한다.
    rally = (f.ret3 >= spec.ret3_drop) | (f.ret5 >= spec.ret5_drop) | (f.ret10 >= spec.ret10_drop)

    if spec.require_reclaim:
        reject = (
            (f.high >= prev_hh20 * (1.0 + spec.low_break_buffer))
            & (f.close <= prev_hh20 * (1.0 - spec.reclaim_buffer))
        )
    else:
        reject = np.ones(n, dtype=bool)

    red = f.close < f.open
    if spec.require_green:
        base_candle = red
    else:
        base_candle = np.ones(n, dtype=bool)

    atr_ok = (f.atrp >= spec.atrp_min) & (f.atrp <= spec.atrp_max)
    range_ok = (f.range20_pct >= spec.range20_min) & (f.range20_pct <= spec.range20_max)
    vol_ok = f.vol_ratio >= spec.vol_ratio_min
    body_ok = f.body_atr >= spec.body_atr_min
    closepos_short = 1.0 - f.close_pos
    closepos_ok = closepos_short >= spec.close_pos_min
    wick_ok = (f.upper_wick_range >= spec.lower_wick_body_min) & (f.lower_wick_body <= max(0.05, spec.upper_wick_range_max * 2.25))

    strict_core = rally & reject & base_candle & atr_ok & range_ok & vol_ok & body_ok & closepos_ok & wick_ok
    shockhigh_core = strict_core & (f.high >= prev_hh20 * (1.0 + spec.low_break_buffer * 0.50))
    rare22_core = strict_core & ((f.ret20 >= 0.080) | (f.ret10 >= spec.ret10_drop * 1.10) | (f.high >= prev_hh50 * 0.996))
    highanchor_core = strict_core & ((f.high >= prev_hh50 * 0.992) | ((f.ret20 >= 0.070) & (closepos_short >= spec.close_pos_min + 0.04)))
    spring_core = strict_core & ((f.high > prev_hh20 * (1.0 + spec.low_break_buffer * 1.25)) & (f.close <= prev_hh20 * (1.0 - spec.reclaim_buffer * 0.60)) & (f.upper_wick_range >= max(0.20, spec.lower_wick_body_min)))

    mask = strict_core.copy()
    if spec.require_shocklow:
        mask &= shockhigh_core
    if spec.require_rare22:
        mask &= rare22_core
    if spec.strict_gate:
        mask &= strict_core
    if spec.lowanchor_gate:
        mask &= highanchor_core
    if spec.spring_gate:
        mask &= spring_core

    # mirrored ema guards.
    if spec.ema_guard == "avoid_trend_down":
        mask &= (~f.trend_up) | (closepos_short >= 0.84) | (f.close <= f.ema20)
    elif spec.ema_guard == "reclaim_ema20":
        mask &= (f.close <= f.ema20) | ((f.high >= f.ema20) & (closepos_short >= 0.82))
    elif spec.ema_guard == "reclaim_ema50":
        mask &= (f.close <= f.ema50) | ((f.high >= f.ema50) & (f.close <= f.ema20) & (closepos_short >= 0.78))

    prior_dryup = (
        (prev_vol_ratio <= 0.95)
        | ((prev_range_pct <= np.maximum(0.018, range_pct_now * 0.70)) & (prev_vol_ratio <= 1.15))
        | (rolling_any_prev(f.vol_ratio <= 0.90, 5) & (f.vol_ratio >= spec.vol_ratio_min + 0.15))
    )
    breakdown = (f.close < prev_close) & (closepos_short >= max(0.68, spec.close_pos_min - 0.02)) & (f.vol_ratio >= spec.vol_ratio_min) & (f.body_atr >= max(0.16, spec.body_atr_min * 0.70))
    upper_sweep_reject = (((f.high >= prev_hh20 * (1.0 + spec.low_break_buffer * 0.65)) | (prev_high >= prev_hh20 * (1.0 + spec.low_break_buffer * 0.80))) & (f.close <= prev_hh20 * (1.0 + spec.reclaim_buffer * 0.35)) & (f.upper_wick_range >= max(0.24, spec.lower_wick_body_min)) & (closepos_short >= max(0.66, spec.close_pos_min - 0.04)))
    ema_resistance = (((f.high >= f.ema20 * 0.994) & (f.close <= f.ema20) & (closepos_short >= max(0.66, spec.close_pos_min - 0.05))) | ((f.high >= f.ema50 * 0.992) & (f.close <= f.ema20) & (closepos_short >= 0.74)))
    compressed = (f.range20_pct <= np.minimum(spec.range20_max * 0.72, 0.115)) & (f.atrp <= np.minimum(spec.atrp_max * 0.82, 0.100)) & (f.vol_ratio >= spec.vol_ratio_min) & (closepos_short >= max(0.66, spec.close_pos_min))
    failed_breakout = (f.high >= prev_hh20 * 0.998) & (f.close < prev_close) & (f.upper_wick_range >= max(0.30, spec.lower_wick_body_min))
    parabolic_exhaust = (f.ret20 >= max(0.09, spec.ret10_drop * 1.05)) & (f.upper_wick_range >= max(0.32, spec.lower_wick_body_min)) & (closepos_short >= max(0.60, spec.close_pos_min - 0.10))
    supply_shelf = (f.high >= f.ema20 * 0.996) & (f.close <= f.ema20) & (f.ret3 >= 0.0) & (f.vol_ratio >= max(0.90, spec.vol_ratio_min * 0.85))
    quality = (closepos_short >= max(0.76, spec.close_pos_min)) & (f.vol_ratio >= spec.vol_ratio_min + 0.12) & (f.body_atr >= max(0.22, spec.body_atr_min)) & (f.lower_wick_body <= max(0.55, spec.upper_wick_range_max))

    if spec.safe_branch_mode == "short_upper_sweep_reject":
        mask &= upper_sweep_reject & (quality | rare22_core | highanchor_core)
    elif spec.safe_branch_mode == "short_breakdown_retest":
        mask &= breakdown & (f.close <= prev_hh20) & (upper_sweep_reject | ema_resistance | quality)
    elif spec.safe_branch_mode == "short_ema20_resistance":
        mask &= ema_resistance & ((~f.trend_up) | (closepos_short >= 0.78) | (f.vol_ratio >= spec.vol_ratio_min + 0.20))
    elif spec.safe_branch_mode == "short_volume_climax_reject":
        mask &= upper_sweep_reject & (f.vol_ratio >= spec.vol_ratio_min + 0.20) & (f.upper_wick_range >= max(0.35, spec.lower_wick_body_min))
    elif spec.safe_branch_mode == "short_failed_breakout":
        mask &= failed_breakout & (upper_sweep_reject | quality)
    elif spec.safe_branch_mode == "short_parabolic_exhaust_reject":
        mask &= parabolic_exhaust & (upper_sweep_reject | failed_breakout | quality)
    elif spec.safe_branch_mode == "short_breakdown_reaccel":
        mask &= prior_dryup & breakdown
    elif spec.safe_branch_mode == "short_supply_shelf_reject":
        mask &= supply_shelf & (upper_sweep_reject | breakdown)
    elif spec.safe_branch_mode == "short_squeeze_breakdown":
        mask &= compressed & breakdown


    # 8V12 신규 short 조건축: 구조 전환/수축-확장/실패 돌파/EMA 밴드 재진입 중심. 8V11 조건명과 중복하지 않는다.
    ema20_slope_proxy = (f.ema20 <= shift1(f.ema20, np.nan)) | (f.close <= f.ema20 * 0.995)
    ema50_dist_short = (f.ema50 - f.close) / np.where(f.close == 0, np.nan, f.close)
    prev_contract = prev_range_pct <= np.maximum(0.014, f.range20_pct * 0.42)
    regime_flip_reject = (f.ret20 >= -0.030) & (f.close <= f.ema20) & ema20_slope_proxy & (closepos_short >= max(0.66, spec.close_pos_min - 0.04)) & (f.vol_ratio >= max(0.96, spec.vol_ratio_min * 0.82))
    vol_contract_breakdown = prev_contract & (f.close < prev_close) & (closepos_short >= max(0.70, spec.close_pos_min)) & (f.body_atr >= max(0.24, spec.body_atr_min)) & (f.vol_ratio >= spec.vol_ratio_min)
    ema20_slope_reject = ema20_slope_proxy & (f.high >= f.ema20 * 0.996) & (f.close <= f.ema20) & (closepos_short >= max(0.68, spec.close_pos_min - 0.04))
    failed_breakout_inside = (prev_high >= prev_hh20 * 0.998) & (f.close < prev_close) & (f.close <= prev_hh20 * 1.002) & (f.upper_wick_range >= max(0.24, spec.lower_wick_body_min))
    dd_sanitized_reject = (upper_sweep_reject | ema20_slope_reject | failed_breakout_inside) & (f.vol_ratio >= max(1.04, spec.vol_ratio_min * 0.86)) & (f.range20_pct <= min(spec.range20_max, 0.200))
    range_expansion_runner_s = (f.range20_pct >= max(spec.range20_min, 0.035)) & (f.close < prev_close) & (closepos_short >= max(0.64, spec.close_pos_min - 0.04)) & (f.vol_ratio >= max(1.00, spec.vol_ratio_min * 0.84))
    pullback_continuation_s = (f.ret20 <= 0.055) & (f.ret3 >= min(spec.ret3_drop * 0.45, 0.020)) & (f.close <= f.ema20) & (f.close < prev_close) & (closepos_short >= max(0.62, spec.close_pos_min - 0.06))
    second_leg_reject_s = rolling_any_prev(upper_sweep_reject | failed_breakout, 6) & (f.close < prev_close) & (closepos_short >= max(0.62, spec.close_pos_min - 0.08))
    ema_band_reentry_s = ((f.high >= f.ema20 * 0.995) | (f.high >= f.ema50 * 0.990)) & (f.close <= f.ema20) & (ema50_dist_short >= -0.045) & (closepos_short >= max(0.60, spec.close_pos_min - 0.08))
    asymmetric_runner_reject_s = (upper_sweep_reject | ema20_slope_reject | range_expansion_runner_s) & (f.upper_wick_range >= 0.18) & (f.vol_ratio >= max(0.94, spec.vol_ratio_min * 0.78))

    if spec.safe_branch_mode == "short_regime_flip_reject":
        mask &= regime_flip_reject & (quality | ema20_slope_reject | upper_sweep_reject)
    elif spec.safe_branch_mode == "short_vol_contract_breakdown":
        mask &= vol_contract_breakdown & (ema20_slope_reject | breakdown | quality)
    elif spec.safe_branch_mode == "short_ema20_slope_proxy":
        mask &= ema20_slope_reject & ((~f.trend_up) | (f.vol_ratio >= spec.vol_ratio_min + 0.12) | failed_breakout_inside)
    elif spec.safe_branch_mode == "short_failed_breakout_inside":
        mask &= failed_breakout_inside & (upper_sweep_reject | quality | ema20_slope_reject)
    elif spec.safe_branch_mode == "short_dd_sanitized_reject":
        mask &= dd_sanitized_reject
    elif spec.safe_branch_mode == "short_range_expansion_runner":
        mask &= range_expansion_runner_s & (breakdown | ema20_slope_reject | quality)
    elif spec.safe_branch_mode == "short_pullback_continuation":
        mask &= pullback_continuation_s & (ema20_slope_reject | breakdown | failed_breakout_inside)
    elif spec.safe_branch_mode == "short_second_leg_reject":
        mask &= second_leg_reject_s & (quality | breakdown | ema20_slope_reject)
    elif spec.safe_branch_mode == "short_ema_band_reentry":
        mask &= ema_band_reentry_s & (quality | failed_breakout_inside | breakdown)
    elif spec.safe_branch_mode == "short_asymmetric_runner_reject":
        mask &= asymmetric_runner_reject_s

    bull_shock = (f.ret1 >= spec.recent_shock_ret) & (range_pct_now >= spec.recent_shock_range_pct) & (f.close_pos >= spec.recent_shock_close_pos_max)
    green_volshock = (f.close > f.open) & (f.vol_ratio >= max(1.70, spec.vol_ratio_min + 0.20)) & (range_pct_now >= max(0.024, spec.recent_shock_range_pct * 0.75)) & (f.close_pos >= max(0.56, spec.recent_shock_close_pos_max - 0.10))
    support_bounce = (f.low <= prev_ll20 * 1.004) & (f.close_pos >= 0.55) & (f.vol_ratio >= max(1.10, spec.vol_ratio_min * 0.80))
    ema20_support = (f.low <= f.ema20) & (f.close > f.ema20) & (f.lower_wick_body >= 0.42) & (f.close_pos >= 0.52)
    two_bar_squeeze = (f.close > f.open) & (prev_close > prev_open) & (f.close_pos >= 0.52) & (prev_close_pos >= 0.52)

    lb = max(1, spec.recent_shock_lookback)
    if spec.entry_brake_mode == "short_recent_bull_shock":
        mask &= ~rolling_any_prev(bull_shock, lb)
    elif spec.entry_brake_mode == "short_green_volshock":
        mask &= ~rolling_any_prev(green_volshock, max(2, lb))
    elif spec.entry_brake_mode == "short_support_bounce":
        mask &= ~rolling_any_prev(support_bounce, max(2, lb))
    elif spec.entry_brake_mode == "short_ema20_support_recent":
        mask &= ~rolling_any_prev(ema20_support, max(2, lb))
    elif spec.entry_brake_mode == "short_two_bar_squeeze":
        mask &= ~(two_bar_squeeze & ~(upper_sweep_reject | quality))

    elif spec.entry_brake_mode == "underfoot_support_recent":
        mask &= ~rolling_any_prev(support_bounce | ema20_support, max(2, lb))
    elif spec.entry_brake_mode == "bull_body_cluster":
        mask &= ~rolling_any_prev((f.close > f.open) & (f.body_atr >= 0.28) & (f.close_pos >= 0.56), max(2, lb))
    elif spec.entry_brake_mode == "thin_red_reversal":
        mask &= ~((f.body_atr < max(0.16, spec.body_atr_min * 0.60)) & (closepos_short < 0.64))
    elif spec.entry_brake_mode == "ema100_above_pressure":
        mask &= ~((f.close > f.ema100) & (f.low >= f.ema20 * 0.992) & (closepos_short < 0.74))
    elif spec.entry_brake_mode == "no_reject_after_gap":
        mask &= ~((f.high > prev_hh20 * 1.006) & (f.close > prev_close) & (closepos_short < 0.70))

    if spec.microguard_gate:
        mask &= ~((f.lower_wick_body > 0.85) & (closepos_short < 0.60))
        mask &= ~((f.range20_pct > 0.230) & (f.atrp > 0.085) & (closepos_short < 0.70))

    if spec.chop_guard_mode == "short_avoid_dead_chop":
        mask &= ~((f.range20_pct < 0.026) & (f.vol_ratio < 1.15) & (np.abs(f.ret5) < 0.018))
    elif spec.chop_guard_mode == "short_avoid_lower_support":
        mask &= ~((f.close <= prev_ll20 * 1.035) & (f.lower_wick_body >= 0.35) & (closepos_short < 0.70))
    elif spec.chop_guard_mode == "short_avoid_downtrend_late_chase":
        mask &= ~((f.trend_down) & (f.close < f.ema50) & (f.ret20 < -0.12) & (closepos_short < 0.82))
    elif spec.chop_guard_mode == "short_avoid_liquidity_void":
        mask &= ~((f.range20_pct > min(0.240, spec.range20_max * 0.95)) & (f.atrp > min(0.090, spec.atrp_max * 0.88)) & (closepos_short < 0.78))
    elif spec.chop_guard_mode == "short_avoid_vshape_bounce":
        mask &= ~((f.ret3 < -0.030) | ((f.close <= prev_ll20 * 1.025) & (f.lower_wick_body >= 0.35)))

    elif spec.chop_guard_mode == "short_avoid_midrange_no_edge":
        mask &= ~((f.close < prev_hh20) & (f.close > prev_ll20) & (np.abs(f.ret5) < 0.014) & (f.vol_ratio < 1.20))
    elif spec.chop_guard_mode == "short_avoid_ema100_floor":
        mask &= ~((f.close <= f.ema100 * 1.004) & (f.close >= f.ema100 * 0.982) & (closepos_short < 0.72))
    elif spec.chop_guard_mode == "short_avoid_ret20_oversold":
        mask &= ~((f.ret20 < -0.120) & (f.lower_wick_body >= 0.24) & (closepos_short < 0.84))
    elif spec.chop_guard_mode == "short_avoid_low_volume_wide":
        mask &= ~((f.range20_pct > 0.145) & (f.vol_ratio < max(1.05, spec.vol_ratio_min * 0.76)) & (closepos_short < 0.76))
    elif spec.chop_guard_mode == "short_avoid_one_bar_spike":
        mask &= ~((range_pct_now > np.maximum(0.050, f.range20_pct * 0.75)) & (f.body_atr < 0.18) & (closepos_short < 0.72))

    mask[:WARMUP_BARS] = False
    mask &= np.isfinite(f.close) & np.isfinite(prev_hh20) & np.isfinite(f.atr14)
    return mask

def entry_mask(spec: StrategySpec, f: FeaturePack) -> np.ndarray:
    if str(spec.side).lower() == "short":
        return short_entry_mask(spec, f)

    n = f.close.size
    prev_ll20 = shift1(f.ll20, np.nan)
    prev_ll50 = shift1(f.ll50, np.nan)
    prev_hh20 = shift1(f.hh20, np.nan)
    prev_close = shift1(f.close, np.nan)
    prev_open = shift1(f.open, np.nan)
    prev_low = shift1(f.low, np.nan)
    prev_close_pos = shift1(f.close_pos, np.nan)
    prev_vol_ratio = shift1(f.vol_ratio, np.nan)
    prev_range_pct = shift1(f.candle_range / np.where(f.close == 0, np.nan, f.close), np.nan)

    range_pct_now = f.candle_range / np.where(f.close == 0, np.nan, f.close)
    eps = 1e-12

    pullback = (
        (f.ret3 <= spec.ret3_drop)
        | (f.ret5 <= spec.ret5_drop)
        | (f.ret10 <= spec.ret10_drop)
    )

    if spec.require_reclaim:
        reclaim = (
            (f.low <= prev_ll20 * (1.0 - spec.low_break_buffer))
            & (f.close >= prev_ll20 * (1.0 + spec.reclaim_buffer))
        )
    else:
        reclaim = np.ones(n, dtype=bool)

    green = f.close > f.open
    if spec.require_green:
        base_candle = green
    else:
        base_candle = np.ones(n, dtype=bool)

    atr_ok = (f.atrp >= spec.atrp_min) & (f.atrp <= spec.atrp_max)
    range_ok = (f.range20_pct >= spec.range20_min) & (f.range20_pct <= spec.range20_max)
    vol_ok = f.vol_ratio >= spec.vol_ratio_min
    body_ok = f.body_atr >= spec.body_atr_min
    closepos_ok = f.close_pos >= spec.close_pos_min
    wick_ok = (f.lower_wick_body >= spec.lower_wick_body_min) & (f.upper_wick_range <= spec.upper_wick_range_max)

    strict_core = (
        pullback
        & reclaim
        & base_candle
        & atr_ok
        & range_ok
        & vol_ok
        & body_ok
        & closepos_ok
        & wick_ok
    )
    shocklow_core = strict_core & (f.low <= prev_ll20 * (1.0 - spec.low_break_buffer * 0.50))
    rare22_core = (
        strict_core
        & (
            (f.ret20 <= -0.080)
            | (f.ret10 <= spec.ret10_drop * 1.10)
            | (f.low <= prev_ll50 * 1.004)
        )
    )
    lowanchor_core = strict_core & (
        (f.low <= prev_ll50 * 1.008)
        | ((f.ret20 <= -0.070) & (f.close_pos >= spec.close_pos_min + 0.04))
    )
    spring_core = strict_core & (
        (f.low < prev_ll20 * (1.0 - spec.low_break_buffer * 1.25))
        & (f.close >= prev_ll20 * (1.0 + spec.reclaim_buffer * 0.60))
        & (f.lower_wick_body >= max(0.15, spec.lower_wick_body_min))
    )

    mask = strict_core.copy()
    if spec.require_shocklow:
        mask &= shocklow_core
    if spec.require_rare22:
        mask &= rare22_core
    if spec.strict_gate:
        mask &= strict_core
    if spec.lowanchor_gate:
        mask &= lowanchor_core
    if spec.spring_gate:
        mask &= spring_core

    if spec.ema_guard == "avoid_trend_down":
        mask &= (~f.trend_down) | (f.close_pos >= 0.84) | (f.close >= f.ema20)
    elif spec.ema_guard == "reclaim_ema20":
        mask &= (f.close >= f.ema20) | ((f.low <= f.ema20) & (f.close_pos >= 0.82))
    elif spec.ema_guard == "reclaim_ema50":
        mask &= (f.close >= f.ema50) | ((f.low <= f.ema50) & (f.close >= f.ema20) & (f.close_pos >= 0.78))

    hot_risk = (f.atrp > min(spec.atrp_max * 0.92, 0.080)) | (f.range20_pct > min(spec.range20_max * 0.92, 0.185))

    # 기존 축 유지: strict / lowanchor는 safe branch 핵심 축이다.
    if spec.safe_branch_mode == "strict_when_hot":
        mask &= (~hot_risk) | strict_core
    elif spec.safe_branch_mode == "shocklow_when_hot":
        mask &= (~hot_risk) | shocklow_core
    elif spec.safe_branch_mode == "strict_or_lowanchor_when_hot":
        mask &= (~hot_risk) | strict_core | lowanchor_core
    elif spec.safe_branch_mode == "rare_proxy_when_loose":
        rare_proxy = (
            (f.ret20 <= -0.065)
            | ((f.vol_ratio >= spec.vol_ratio_min + 0.35) & (f.ret5 <= spec.ret5_drop * 0.92))
            | (f.low <= prev_ll50 * 1.006)
        )
        mask &= rare_proxy
    elif spec.safe_branch_mode == "trend_repair_only":
        repaired = (~f.trend_down) | (f.close_pos >= 0.82) | (f.vol_ratio >= spec.vol_ratio_min + 0.35) | (f.close >= f.ema20)
        mask &= repaired

    # 8V9 새 조건축.
    prior_dryup = (
        (prev_vol_ratio <= 0.95)
        | ((prev_range_pct <= np.maximum(0.018, range_pct_now * 0.70)) & (prev_vol_ratio <= 1.15))
        | (rolling_any_prev(f.vol_ratio <= 0.90, 5) & (f.vol_ratio >= spec.vol_ratio_min + 0.15))
    )
    reaccel = (
        (f.close > prev_close)
        & (f.close_pos >= max(0.70, spec.close_pos_min - 0.02))
        & (f.vol_ratio >= spec.vol_ratio_min)
        & (f.body_atr >= max(0.18, spec.body_atr_min * 0.75))
    )
    sweep_absorb = (
        ((f.low <= prev_ll20 * (1.0 - spec.low_break_buffer * 0.65)) | (prev_low <= prev_ll20 * (1.0 - spec.low_break_buffer * 0.80)))
        & (f.close >= prev_ll20 * (1.0 - spec.reclaim_buffer * 0.35))
        & (f.lower_wick_body >= max(0.18, spec.lower_wick_body_min))
        & (f.close_pos >= max(0.70, spec.close_pos_min - 0.03))
    )
    ema_shelf = (
        ((f.low <= f.ema20 * 1.006) & (f.close >= f.ema20) & (f.close_pos >= max(0.68, spec.close_pos_min - 0.05)))
        | ((f.low <= f.ema50 * 1.008) & (f.close >= f.ema20) & (f.close_pos >= 0.76))
    )
    compressed = (
        (f.range20_pct <= np.minimum(spec.range20_max * 0.72, 0.105))
        & (f.atrp <= np.minimum(spec.atrp_max * 0.82, 0.085))
        & (f.vol_ratio >= spec.vol_ratio_min)
        & (f.close_pos >= max(0.72, spec.close_pos_min))
    )
    followthrough = (
        (f.close > prev_close)
        & (f.close_pos >= max(0.74, spec.close_pos_min))
        & (f.ret1 >= -0.012)
        & (f.upper_wick_range <= min(spec.upper_wick_range_max, 0.82))
    )
    quality = (
        (f.close_pos >= max(0.80, spec.close_pos_min))
        & (f.vol_ratio >= spec.vol_ratio_min + 0.20)
        & (f.body_atr >= max(0.28, spec.body_atr_min))
        & (f.upper_wick_range <= min(0.78, spec.upper_wick_range_max))
    )

    if spec.safe_branch_mode == "vol_dryup_reaccel":
        mask &= prior_dryup & reaccel
    elif spec.safe_branch_mode == "double_sweep_absorption":
        mask &= sweep_absorb & ((f.low <= prev_ll20) | (prev_low <= prev_ll20))
    elif spec.safe_branch_mode == "ema_shelf_repair":
        mask &= ema_shelf & ((~f.trend_down) | (f.close_pos >= 0.82) | (f.vol_ratio >= spec.vol_ratio_min + 0.25))
    elif spec.safe_branch_mode == "capitulation_absorb_only":
        mask &= sweep_absorb & ((f.ret5 <= spec.ret5_drop * 0.92) | (f.ret10 <= spec.ret10_drop * 0.90)) & (f.lower_wick_body >= 0.30)
    elif spec.safe_branch_mode == "multi_low_reclaim":
        mask &= ((f.low <= prev_ll50 * 1.006) | (f.low <= prev_ll20 * (1.0 - spec.low_break_buffer))) & sweep_absorb
    elif spec.safe_branch_mode == "strict_lowanchor_and_dryup":
        mask &= lowanchor_core & (prior_dryup | (f.vol_ratio >= spec.vol_ratio_min + 0.35))
    elif spec.safe_branch_mode == "reversal_followthrough":
        mask &= followthrough & ((f.ret3 <= spec.ret3_drop * 0.80) | (f.ret5 <= spec.ret5_drop * 0.80))
    elif spec.safe_branch_mode == "shelf_or_sweep":
        mask &= (ema_shelf | sweep_absorb) & quality
    elif spec.safe_branch_mode == "compression_then_reclaim":
        mask &= compressed & (reclaim | ema_shelf | sweep_absorb)
    elif spec.safe_branch_mode == "quality_not_quantity":
        mask &= quality & (sweep_absorb | lowanchor_core | rare22_core)

    # 8V12 신규 long 조건축: 기존 V51/safe branch와 중복되지 않도록 liquidity retest, ATR cooldown repair,
    # EMA50 bounce, volume climax absorption, squeeze/reclaim, breakout pullback을 별도 해석한다.
    atr_cooling = (f.atrp <= shift1(f.atrp, np.nan)) | (f.atrp <= np.minimum(spec.atrp_max * 0.70, 0.075))
    ema20_dist = (f.close - f.ema20) / np.where(f.close == 0, np.nan, f.close)
    sweep_retest = sweep_absorb & (prev_close <= prev_ll20 * 1.012) & (f.close > prev_close) & (f.upper_wick_range <= min(0.74, spec.upper_wick_range_max))
    atr_cool_repair = strict_core & atr_cooling & (f.ret1 >= -0.006) & ((f.close >= f.ema20) | (f.close_pos >= 0.84))
    ema50_bounce = ((f.low <= f.ema50 * 1.012) & (f.close >= f.ema20) & (f.close_pos >= max(0.74, spec.close_pos_min - 0.04)) & (f.vol_ratio >= max(1.0, spec.vol_ratio_min * 0.85)))
    volume_climax_absorb = (sweep_absorb & (f.vol_ratio >= spec.vol_ratio_min + 0.30) & (f.lower_wick_body >= max(0.35, spec.lower_wick_body_min)))
    inside_break_reversal = (prev_range_pct <= np.maximum(0.016, range_pct_now * 0.72)) & (f.close > prev_close) & (f.close_pos >= max(0.76, spec.close_pos_min)) & (f.vol_ratio >= spec.vol_ratio_min)
    squeeze_reclaim = compressed & ((f.close >= f.ema20) | reclaim | sweep_absorb) & (np.abs(ema20_dist) <= 0.055)
    breakout_pullback_reclaim = (f.ret20 >= -0.035) & (f.ret3 <= spec.ret3_drop * 0.65) & (f.close >= f.ema20) & (f.close_pos >= max(0.70, spec.close_pos_min - 0.06))

    if spec.safe_branch_mode == "long_liquidity_sweep_retest":
        mask &= sweep_retest & (quality | rare22_core | lowanchor_core)
    elif spec.safe_branch_mode == "long_atr_cooldown_repair":
        mask &= atr_cool_repair & (prior_dryup | sweep_absorb | ema_shelf)
    elif spec.safe_branch_mode == "long_ema50_bounce_volume":
        mask &= ema50_bounce & (quality | followthrough | sweep_absorb)
    elif spec.safe_branch_mode == "long_volume_climax_absorb":
        mask &= volume_climax_absorb
    elif spec.safe_branch_mode == "long_inside_break_reversal":
        mask &= inside_break_reversal & (sweep_absorb | reclaim | ema_shelf)
    elif spec.safe_branch_mode == "long_squeeze_reclaim":
        mask &= squeeze_reclaim & (quality | followthrough)
    elif spec.safe_branch_mode == "long_breakout_pullback_reclaim":
        mask &= breakout_pullback_reclaim & (quality | followthrough | ema_shelf)


    # 8V12 신규 long 조건축: 구조 전환/수축-확장/실패 이탈/EMA 밴드 재진입 중심. 8V11 조건명과 중복하지 않는다.
    ema20_slope_proxy = (f.ema20 >= shift1(f.ema20, np.nan)) | (f.close >= f.ema20 * 1.005)
    ema50_dist_long = (f.close - f.ema50) / np.where(f.close == 0, np.nan, f.close)
    prev_contract = prev_range_pct <= np.maximum(0.014, f.range20_pct * 0.42)
    regime_flip_repair = (f.ret20 <= 0.035) & (f.close >= f.ema20) & ema20_slope_proxy & (f.close_pos >= max(0.70, spec.close_pos_min - 0.04)) & (f.vol_ratio >= max(0.96, spec.vol_ratio_min * 0.82))
    vol_contract_expand = prev_contract & (f.close > prev_close) & (f.close_pos >= max(0.74, spec.close_pos_min)) & (f.body_atr >= max(0.24, spec.body_atr_min)) & (f.vol_ratio >= spec.vol_ratio_min)
    ema20_slope_reclaim = ema20_slope_proxy & (f.low <= f.ema20 * 1.004) & (f.close >= f.ema20) & (f.close_pos >= max(0.70, spec.close_pos_min - 0.04))
    failed_breakdown_inside = (prev_low <= prev_ll20 * 1.002) & (f.close > prev_close) & (f.close >= prev_ll20 * 0.998) & (f.lower_wick_body >= max(0.24, spec.lower_wick_body_min))
    dd_sanitized_reclaim = (sweep_absorb | ema20_slope_reclaim | failed_breakdown_inside) & (f.vol_ratio >= max(1.04, spec.vol_ratio_min * 0.86)) & (f.range20_pct <= min(spec.range20_max, 0.185))
    lower_low_weak = (
        (f.low <= prev_ll20 * (1.0 - spec.low_break_buffer * 0.80))
        & (f.close_pos <= max(0.58, spec.close_pos_min - 0.10))
        & (f.body_atr <= max(0.20, spec.body_atr_min * 0.70))
    )
    range_expansion_runner_l = (f.range20_pct >= max(spec.range20_min, 0.032)) & (f.close > prev_close) & (f.close_pos >= max(0.68, spec.close_pos_min - 0.04)) & (f.vol_ratio >= max(1.00, spec.vol_ratio_min * 0.84))
    pullback_continuation_l = (f.ret20 >= -0.055) & (f.ret3 <= max(spec.ret3_drop * 0.45, -0.020)) & (f.close >= f.ema20) & (f.close > prev_close) & (f.close_pos >= max(0.66, spec.close_pos_min - 0.06))
    second_leg_absorb_l = rolling_any_prev(sweep_absorb | lower_low_weak, 6) & (f.close > prev_close) & (f.close_pos >= max(0.66, spec.close_pos_min - 0.08))
    ema_band_reentry_l = ((f.low <= f.ema20 * 1.005) | (f.low <= f.ema50 * 1.010)) & (f.close >= f.ema20) & (ema50_dist_long >= -0.045) & (f.close_pos >= max(0.64, spec.close_pos_min - 0.08))
    asymmetric_runner_reclaim_l = (sweep_absorb | ema20_slope_reclaim | range_expansion_runner_l) & (f.lower_wick_body >= 0.18) & (f.vol_ratio >= max(0.94, spec.vol_ratio_min * 0.78))

    if spec.safe_branch_mode == "long_regime_flip_repair":
        mask &= regime_flip_repair & (quality | ema20_slope_reclaim | sweep_absorb)
    elif spec.safe_branch_mode == "long_vol_contract_expand":
        mask &= vol_contract_expand & (ema20_slope_reclaim | reaccel | quality)
    elif spec.safe_branch_mode == "long_ema20_slope_proxy":
        mask &= ema20_slope_reclaim & ((~f.trend_down) | (f.vol_ratio >= spec.vol_ratio_min + 0.12) | failed_breakdown_inside)
    elif spec.safe_branch_mode == "long_failed_breakdown_inside":
        mask &= failed_breakdown_inside & (sweep_absorb | quality | ema20_slope_reclaim)
    elif spec.safe_branch_mode == "long_dd_sanitized_reclaim":
        mask &= dd_sanitized_reclaim
    elif spec.safe_branch_mode == "long_range_expansion_runner":
        mask &= range_expansion_runner_l & (reaccel | ema20_slope_reclaim | quality)
    elif spec.safe_branch_mode == "long_pullback_continuation":
        mask &= pullback_continuation_l & (ema20_slope_reclaim | reaccel | failed_breakdown_inside)
    elif spec.safe_branch_mode == "long_second_leg_absorption":
        mask &= second_leg_absorb_l & (quality | reaccel | ema20_slope_reclaim)
    elif spec.safe_branch_mode == "long_ema_band_reentry":
        mask &= ema_band_reentry_l & (quality | failed_breakdown_inside | reaccel)
    elif spec.safe_branch_mode == "long_asymmetric_runner_reclaim":
        mask &= asymmetric_runner_reclaim_l

    # Short-lived entry brakes. These avoid the immediate aftermath of adverse shocks,
    # not the whole strategy regime.
    adverse_shock = (
        (f.ret1 <= spec.recent_shock_ret)
        & (range_pct_now >= spec.recent_shock_range_pct)
        & (f.close_pos <= spec.recent_shock_close_pos_max)
    )
    red_volshock = (
        (f.close < f.open)
        & (f.vol_ratio >= max(1.80, spec.vol_ratio_min + 0.25))
        & (range_pct_now >= max(0.026, spec.recent_shock_range_pct * 0.80))
        & (f.close_pos <= min(0.46, spec.recent_shock_close_pos_max + 0.10))
    )
    wick_reject = (
        (f.upper_wick_range >= 0.55)
        & (f.close_pos <= 0.55)
        & (f.vol_ratio >= max(1.25, spec.vol_ratio_min * 0.85))
    )
    prev_red_climax = (
        (prev_close < prev_open)
        & (prev_vol_ratio >= max(1.60, spec.vol_ratio_min + 0.10))
        & (prev_close_pos <= 0.36)
        & (prev_range_pct >= max(0.020, spec.recent_shock_range_pct * 0.65))
    )
    bounce_fail = (
        (prev_close > prev_open)
        & (prev_close_pos <= 0.48)
        & (f.close <= prev_close)
        & (f.close_pos <= 0.62)
    )
    ema20_reject = (
        (f.high >= f.ema20)
        & (f.close < f.ema20)
        & (f.upper_wick_range >= 0.42)
        & (f.close_pos <= 0.62)
    )
    two_bar_slide = (
        (f.close < f.open)
        & (prev_close < prev_open)
        & (f.close_pos <= 0.48)
        & (prev_close_pos <= 0.48)
    )

    lb = max(1, spec.recent_shock_lookback)
    if spec.entry_brake_mode == "recent_adverse_shock":
        mask &= ~rolling_any_prev(adverse_shock, lb)
    elif spec.entry_brake_mode == "recent_red_volshock":
        mask &= ~rolling_any_prev(red_volshock, max(2, lb))
    elif spec.entry_brake_mode == "wick_reject_recent":
        mask &= ~rolling_any_prev(wick_reject, max(2, lb))
    elif spec.entry_brake_mode == "prev_red_climax_no_reclaim":
        mask &= ~(rolling_any_prev(prev_red_climax, max(2, lb)) & ~(sweep_absorb | quality))
    elif spec.entry_brake_mode == "lower_low_no_body":
        mask &= ~lower_low_weak
    elif spec.entry_brake_mode == "bounce_failure":
        mask &= ~rolling_any_prev(bounce_fail, max(2, lb))
    elif spec.entry_brake_mode == "ema20_reject_recent":
        mask &= ~rolling_any_prev(ema20_reject, max(2, lb))
    elif spec.entry_brake_mode == "two_bar_slide_no_absorb":
        mask &= ~(two_bar_slide & ~(sweep_absorb | quality))

    elif spec.entry_brake_mode == "overhead_compression_recent":
        mask &= ~((f.close >= prev_hh20 * 0.970) & (f.range20_pct < 0.055) & (f.vol_ratio < max(1.18, spec.vol_ratio_min)))
    elif spec.entry_brake_mode == "bear_body_cluster":
        mask &= ~rolling_any_prev((f.close < f.open) & (f.body_atr >= 0.28) & (f.close_pos <= 0.44), max(2, lb))
    elif spec.entry_brake_mode == "thin_green_reversal":
        mask &= ~((f.body_atr < max(0.16, spec.body_atr_min * 0.60)) & (f.close_pos < 0.68))
    elif spec.entry_brake_mode == "ema100_below_pressure":
        mask &= ~((f.close < f.ema100) & (f.high <= f.ema20 * 1.008) & (f.close_pos < 0.78))
    elif spec.entry_brake_mode == "no_reclaim_after_gap":
        mask &= ~((f.low < prev_ll20 * 0.994) & (f.close < prev_close) & (f.close_pos < 0.70))

    if spec.microguard_gate:
        mask &= ~((f.upper_wick_range > 0.58) & (f.close_pos < 0.62))
        mask &= ~((f.range20_pct > 0.200) & (f.atrp > 0.070) & (f.close_pos < 0.72))

    if spec.chop_guard_mode == "avoid_dead_chop":
        mask &= ~((f.range20_pct < 0.026) & (f.vol_ratio < 1.20) & (np.abs(f.ret5) < 0.018))
    elif spec.chop_guard_mode == "avoid_top_quiet":
        mask &= ~((f.close >= prev_hh20 * 0.965) & (f.vol_ratio < 1.25) & (f.range20_pct < 0.045))
    elif spec.chop_guard_mode == "avoid_deep_down_no_reclaim":
        mask &= ~((f.trend_down) & (f.close < f.ema50) & (f.close_pos < 0.75) & (f.ret20 < -0.10))
    elif spec.chop_guard_mode == "avoid_range_blowoff":
        mask &= ~((f.range20_pct > 0.200) & (f.atrp > 0.065) & (f.close_pos < 0.78))
    elif spec.chop_guard_mode == "avoid_vshape_chase":
        mask &= ~((f.ret3 > 0.030) | ((f.close >= prev_hh20 * 0.975) & (f.upper_wick_range >= 0.38)))
    elif spec.chop_guard_mode == "avoid_low_quality_melt":
        mask &= ~((f.trend_down) & (f.close < f.ema50) & (f.ret20 < -0.14) & (f.lower_wick_body < 0.25))
    elif spec.chop_guard_mode == "avoid_thin_reclaim":
        mask &= ~((f.vol_ratio < max(1.05, spec.vol_ratio_min * 0.82)) & (f.body_atr < max(0.20, spec.body_atr_min * 0.65)))
    elif spec.chop_guard_mode == "avoid_upper_supply":
        mask &= ~((f.close >= prev_hh20 * 0.960) & (f.upper_wick_range >= 0.42) & (f.close_pos < 0.78))
    elif spec.chop_guard_mode == "avoid_liquidity_void":
        mask &= ~((f.range20_pct > min(0.220, spec.range20_max * 0.95)) & (f.atrp > min(0.080, spec.atrp_max * 0.88)) & (f.close_pos < 0.82))

    elif spec.chop_guard_mode == "avoid_midrange_no_edge":
        mask &= ~((f.close < prev_hh20) & (f.close > prev_ll20) & (np.abs(f.ret5) < 0.014) & (f.vol_ratio < 1.20))
    elif spec.chop_guard_mode == "avoid_ema100_ceiling":
        mask &= ~((f.close >= f.ema100 * 0.996) & (f.close <= f.ema100 * 1.018) & (f.close_pos < 0.76))
    elif spec.chop_guard_mode == "avoid_ret20_overheat":
        mask &= ~((f.ret20 > 0.115) & (f.upper_wick_range >= 0.24) & (f.close_pos < 0.84))
    elif spec.chop_guard_mode == "avoid_low_volume_wide":
        mask &= ~((f.range20_pct > 0.135) & (f.vol_ratio < max(1.05, spec.vol_ratio_min * 0.76)) & (f.close_pos < 0.78))
    elif spec.chop_guard_mode == "avoid_one_bar_spike":
        mask &= ~((range_pct_now > np.maximum(0.048, f.range20_pct * 0.75)) & (f.body_atr < 0.18) & (f.close_pos < 0.74))

    mask[:WARMUP_BARS] = False
    mask &= np.isfinite(f.close) & np.isfinite(prev_ll20) & np.isfinite(f.atr14)
    return mask


def simulate_strategy_on_symbol(symbol: str, f: FeaturePack, spec: StrategySpec) -> Tuple[SymbolSummary, List[Tuple[int, float]]]:
    n = f.close.size
    if n < max(MIN_BARS, WARMUP_BARS + 5):
        return SymbolSummary(symbol=symbol), []

    mask = entry_mask(spec, f)
    entry_indices = np.flatnonzero(mask)
    if entry_indices.size == 0:
        return SymbolSummary(symbol=symbol), []

    is_short = str(spec.side).lower() == "short"
    trades: List[Tuple[int, float]] = []
    wins = 0
    losses = 0
    next_allowed = WARMUP_BARS
    loss_streak = 0
    symbol_equity = 1.0
    symbol_equity_peak = 1.0

    for i_raw in entry_indices:
        i = int(i_raw)
        if i < next_allowed:
            continue
        if i >= n - 2:
            break

        entry_price = float(f.close[i])
        if entry_price <= 0.0:
            continue

        atr_i = max(1e-12, float(f.atr14[i]))
        local_atr_stop = float(spec.atr_stop)
        local_rr_target = float(spec.rr_target)
        local_max_hold = int(spec.max_hold_bars)
        atrp_i = float(f.atrp[i]) if math.isfinite(float(f.atrp[i])) else 0.0
        dir_close_pos = float(1.0 - f.close_pos[i]) if is_short else float(f.close_pos[i])

        # Adaptive exits: same framework, mirrored for short where needed.
        if spec.exit_mode == "hot_tighten" and atrp_i >= 0.055:
            local_atr_stop = max(0.72, local_atr_stop * 0.88)
            local_rr_target = min(local_rr_target, 1.65)
            local_max_hold = min(local_max_hold, 14)
        elif spec.exit_mode == "hot_wide_fast" and atrp_i >= 0.055:
            local_atr_stop = min(1.45, local_atr_stop * 1.08)
            local_rr_target = min(local_rr_target, 1.55)
            local_max_hold = min(local_max_hold, 12)
        elif spec.exit_mode == "cold_extend" and atrp_i <= 0.030:
            local_rr_target = max(local_rr_target, 2.05)
            local_max_hold = max(local_max_hold, 22)
        elif spec.exit_mode == "late_fail_fast":
            local_max_hold = min(local_max_hold, 16)
        elif spec.exit_mode == "loss_cluster_fast_target" and loss_streak > 0:
            local_rr_target = min(local_rr_target, 1.45)
            local_max_hold = min(local_max_hold, 12)
        elif spec.exit_mode == "followthrough_or_cut":
            local_max_hold = min(local_max_hold, 18)
            local_rr_target = min(local_rr_target, 2.15)
        elif spec.exit_mode == "runner_if_strong":
            if dir_close_pos >= 0.84 and float(f.vol_ratio[i]) >= spec.vol_ratio_min + 0.25 and atrp_i <= min(0.075, spec.atrp_max):
                local_rr_target = max(local_rr_target, 2.35)
                local_max_hold = max(local_max_hold, 24)
                local_atr_stop = min(1.55, local_atr_stop * 1.05)
            else:
                local_max_hold = min(local_max_hold, 16)
        elif spec.exit_mode == "quick_repair":
            local_atr_stop = max(0.70, local_atr_stop * 0.88)
            local_rr_target = min(local_rr_target, 1.70)
            local_max_hold = min(local_max_hold, 13)
        elif spec.exit_mode == "shock_tight_then_trail":
            if atrp_i >= 0.060:
                local_atr_stop = max(0.68, local_atr_stop * 0.82)
                local_rr_target = min(local_rr_target, 1.65)
                local_max_hold = min(local_max_hold, 14)
            else:
                local_rr_target = max(local_rr_target, 2.05)
        elif spec.exit_mode == "shelf_runner":
            if float(f.close[i]) >= float(f.ema20[i]) or dir_close_pos >= 0.82:
                local_rr_target = max(local_rr_target, 2.20)
                local_max_hold = max(local_max_hold, 24)
            else:
                local_max_hold = min(local_max_hold, 15)
        elif spec.exit_mode == "loss_cluster_quarantine" and loss_streak > 0:
            local_atr_stop = max(0.70, local_atr_stop * 0.86)
            local_rr_target = min(local_rr_target, 1.55)
            local_max_hold = min(local_max_hold, 12)
        elif spec.exit_mode == "short_failfast_then_trail":
            local_atr_stop = max(0.72, local_atr_stop * 0.90)
            local_rr_target = min(max(local_rr_target, 1.65), 3.20)
            local_max_hold = min(local_max_hold, 26)
        elif spec.exit_mode == "short_runner_if_strong":
            if dir_close_pos >= 0.82 and float(f.vol_ratio[i]) >= spec.vol_ratio_min + 0.15 and atrp_i <= min(0.105, spec.atrp_max):
                local_rr_target = max(local_rr_target, 2.75)
                local_max_hold = max(local_max_hold, 34)
                local_atr_stop = min(1.75, local_atr_stop * 1.06)
            else:
                local_max_hold = min(local_max_hold, 20)
        elif spec.exit_mode == "short_support_take_profit":
            local_rr_target = min(local_rr_target, 2.25)
            local_max_hold = min(local_max_hold, 18)
        elif spec.exit_mode == "short_shelf_runner":
            if float(f.close[i]) <= float(f.ema20[i]) or dir_close_pos >= 0.80:
                local_rr_target = max(local_rr_target, 2.60)
                local_max_hold = max(local_max_hold, 32)
            else:
                local_max_hold = min(local_max_hold, 18)

        elif spec.exit_mode == "mfe_lock_fast":
            local_atr_stop = max(0.68, local_atr_stop * 0.86)
            local_rr_target = min(max(local_rr_target, 1.65), 2.55)
            local_max_hold = min(local_max_hold, 18)
        elif spec.exit_mode == "time_decay_runner":
            if dir_close_pos >= 0.82 and float(f.vol_ratio[i]) >= max(1.05, spec.vol_ratio_min * 0.90):
                local_rr_target = max(local_rr_target, 2.45)
                local_max_hold = max(local_max_hold, 30)
            else:
                local_rr_target = min(local_rr_target, 1.95)
                local_max_hold = min(local_max_hold, 15)
        elif spec.exit_mode == "atr_band_trail":
            local_atr_stop = min(1.55, max(0.82, local_atr_stop * 1.02))
            local_rr_target = max(local_rr_target, 2.25)
            local_max_hold = max(local_max_hold, 24)
        elif spec.exit_mode == "two_stage_take":
            local_rr_target = min(max(local_rr_target, 1.95), 2.75)
            local_max_hold = min(max(local_max_hold, 20), 32)
        elif spec.exit_mode == "dd_sensitive_fast":
            local_atr_stop = max(0.66, local_atr_stop * 0.82)
            local_rr_target = min(local_rr_target, 1.85)
            local_max_hold = min(local_max_hold, 14)
        elif spec.exit_mode == "runner_reversal_cut":
            if dir_close_pos >= 0.80:
                local_rr_target = max(local_rr_target, 2.85)
                local_max_hold = max(local_max_hold, 34)
            else:
                local_max_hold = min(local_max_hold, 18)
        elif spec.exit_mode == "short_mfe_lock_fast":
            local_atr_stop = max(0.70, local_atr_stop * 0.86)
            local_rr_target = min(max(local_rr_target, 1.75), 2.70)
            local_max_hold = min(local_max_hold, 20)
        elif spec.exit_mode == "short_time_decay_runner":
            if dir_close_pos >= 0.80 and float(f.vol_ratio[i]) >= max(1.05, spec.vol_ratio_min * 0.90):
                local_rr_target = max(local_rr_target, 2.80)
                local_max_hold = max(local_max_hold, 34)
            else:
                local_rr_target = min(local_rr_target, 2.10)
                local_max_hold = min(local_max_hold, 18)
        elif spec.exit_mode == "short_atr_band_trail":
            local_atr_stop = min(1.70, max(0.86, local_atr_stop * 1.03))
            local_rr_target = max(local_rr_target, 2.65)
            local_max_hold = max(local_max_hold, 30)
        elif spec.exit_mode == "short_two_stage_take":
            local_rr_target = min(max(local_rr_target, 2.15), 3.15)
            local_max_hold = min(max(local_max_hold, 24), 38)
        elif spec.exit_mode == "short_dd_sensitive_fast":
            local_atr_stop = max(0.72, local_atr_stop * 0.84)
            local_rr_target = min(local_rr_target, 2.05)
            local_max_hold = min(local_max_hold, 16)
        elif spec.exit_mode == "short_runner_reversal_cut":
            if dir_close_pos >= 0.78:
                local_rr_target = max(local_rr_target, 3.15)
                local_max_hold = max(local_max_hold, 40)
            else:
                local_max_hold = min(local_max_hold, 20)

        risk = max(1e-12, local_atr_stop * atr_i)
        if is_short:
            stop_price = entry_price + risk
            target_price = entry_price - risk * local_rr_target
        else:
            stop_price = entry_price - risk
            target_price = entry_price + risk * local_rr_target
        if stop_price <= 0.0 or target_price <= 0.0:
            continue

        active_stop = stop_price
        exit_price = float(f.close[min(n - 1, i + local_max_hold)])
        exit_ts = int(f.timestamp[min(n - 1, i + local_max_hold)])
        exit_idx = min(n - 1, i + local_max_hold)

        for j in range(i + 1, min(n, i + local_max_hold + 1)):
            high_j = float(f.high[j])
            low_j = float(f.low[j])
            close_j = float(f.close[j])
            ts_j = int(f.timestamp[j])

            # Breakeven / trail update before hit decision.
            if spec.breakeven_after_r < 900:
                if is_short:
                    if low_j <= entry_price - risk * spec.breakeven_after_r:
                        active_stop = min(active_stop, entry_price)
                else:
                    if high_j >= entry_price + risk * spec.breakeven_after_r:
                        active_stop = max(active_stop, entry_price)

            if spec.trail_after_r < 900:
                if is_short:
                    if low_j <= entry_price - risk * spec.trail_after_r:
                        trail_stop = low_j + max(1e-12, float(f.atr14[j])) * spec.trail_atr_mult
                        active_stop = min(active_stop, trail_stop)
                else:
                    if high_j >= entry_price + risk * spec.trail_after_r:
                        trail_stop = high_j - max(1e-12, float(f.atr14[j])) * spec.trail_atr_mult
                        active_stop = max(active_stop, trail_stop)

            if is_short:
                hit_stop = high_j >= active_stop
                hit_target = low_j <= target_price
            else:
                hit_stop = low_j <= active_stop
                hit_target = high_j >= target_price

            if hit_stop and hit_target:
                # 보수적 체결: 같은 봉에서 양쪽 터치 시 stop 우선
                exit_price = active_stop
                exit_ts = ts_j
                exit_idx = j
                break
            if hit_stop:
                exit_price = active_stop
                exit_ts = ts_j
                exit_idx = j
                break
            if hit_target:
                exit_price = target_price
                exit_ts = ts_j
                exit_idx = j
                break

            hold = j - i
            if is_short:
                unrealized_pct = (entry_price - close_j) / entry_price * 100.0
                dir_close_pos_j = float(1.0 - f.close_pos[j])
            else:
                unrealized_pct = (close_j - entry_price) / entry_price * 100.0
                dir_close_pos_j = float(f.close_pos[j])

            if spec.fail_exit_bars < 900 and hold >= spec.fail_exit_bars:
                if unrealized_pct <= spec.fail_exit_pnl_pct and dir_close_pos_j <= spec.fail_exit_close_pos_max:
                    exit_price = close_j
                    exit_ts = ts_j
                    exit_idx = j
                    break

            if not is_short:
                if spec.exit_mode == "followthrough_or_cut" and hold >= 3:
                    if unrealized_pct <= max(spec.fail_exit_pnl_pct, -0.12) and float(f.close_pos[j]) <= max(0.46, spec.fail_exit_close_pos_max):
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "volfade_cut" and hold >= 4:
                    if unrealized_pct < 0.10 and float(f.vol_ratio[j]) <= 0.88 and float(f.close_pos[j]) <= 0.56:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "green_fail_cut" and hold >= 2:
                    if close_j < float(f.open[j]) and close_j <= entry_price and float(f.close_pos[j]) <= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break

                elif spec.exit_mode == "mfe_lock_fast" and hold >= 3:
                    if unrealized_pct <= 0.0 and float(f.close_pos[j]) <= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "time_decay_runner" and hold >= 7:
                    if unrealized_pct < 0.18 and float(f.vol_ratio[j]) < 0.95:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "two_stage_take" and hold >= 5:
                    if unrealized_pct > 0.0 and float(f.upper_wick_range[j]) >= 0.60 and float(f.close_pos[j]) < 0.58:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "dd_sensitive_fast" and hold >= 2:
                    if unrealized_pct <= max(spec.fail_exit_pnl_pct, -0.10) and float(f.close_pos[j]) <= 0.56:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "runner_reversal_cut" and hold >= 4:
                    if close_j < float(f.ema20[j]) and float(f.close_pos[j]) <= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
            else:
                if spec.exit_mode == "short_support_take_profit" and hold >= 3:
                    if unrealized_pct > 0.0 and (float(f.low[j]) <= float(f.ll20[j]) * 1.006 or float(f.lower_wick_body[j]) >= 0.60):
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_volfade_cut" and hold >= 4:
                    if unrealized_pct < 0.10 and float(f.vol_ratio[j]) <= 0.88 and float(1.0 - f.close_pos[j]) <= 0.56:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_green_fail_cut" and hold >= 2:
                    if close_j > float(f.open[j]) and close_j >= entry_price and float(f.close_pos[j]) >= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break

                elif spec.exit_mode == "short_mfe_lock_fast" and hold >= 3:
                    if unrealized_pct <= 0.0 and float(1.0 - f.close_pos[j]) <= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_time_decay_runner" and hold >= 7:
                    if unrealized_pct < 0.18 and float(f.vol_ratio[j]) < 0.95:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_two_stage_take" and hold >= 5:
                    if unrealized_pct > 0.0 and float(f.lower_wick_body[j]) >= 0.60 and float(1.0 - f.close_pos[j]) < 0.58:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_dd_sensitive_fast" and hold >= 2:
                    if unrealized_pct <= max(spec.fail_exit_pnl_pct, -0.10) and float(1.0 - f.close_pos[j]) <= 0.56:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break
                elif spec.exit_mode == "short_runner_reversal_cut" and hold >= 4:
                    if close_j > float(f.ema20[j]) and float(1.0 - f.close_pos[j]) <= 0.50:
                        exit_price = close_j
                        exit_ts = ts_j
                        exit_idx = j
                        break

        if is_short:
            gross_pct = (entry_price - exit_price) / entry_price * 100.0
        else:
            gross_pct = (exit_price - entry_price) / entry_price * 100.0
        net_pct = gross_pct - (ROUND_TRIP_COST_BPS / 100.0)
        trades.append((exit_ts, float(net_pct)))
        if net_pct > 0:
            wins += 1
            loss_streak = 0
        else:
            losses += 1
            if net_pct <= spec.loss_brake_pnl_pct:
                loss_streak += 1
            else:
                loss_streak = max(0, loss_streak)

        step = 1.0 + POSITION_FRACTION * (float(net_pct) / 100.0)
        if step > 0.0:
            symbol_equity *= step
            symbol_equity_peak = max(symbol_equity_peak, symbol_equity)
        symbol_dd_pct = 0.0
        if symbol_equity_peak > 0:
            symbol_dd_pct = abs((symbol_equity / symbol_equity_peak - 1.0) * 100.0)

        adaptive_cd = 0
        if spec.loss_brake_after > 0 and loss_streak >= spec.loss_brake_after:
            adaptive_cd = max(adaptive_cd, max(0, spec.loss_brake_bars))
            loss_streak = 0
        if spec.symbol_dd_brake_pct > 0.0 and symbol_dd_pct >= spec.symbol_dd_brake_pct:
            adaptive_cd = max(adaptive_cd, max(0, spec.symbol_dd_brake_bars))
            symbol_equity_peak = max(symbol_equity, 1e-12)

        next_allowed = exit_idx + max(0, spec.cooldown_bars, adaptive_cd)

    trade_pnls = [pnl for _, pnl in trades]
    final_ret, max_ret, max_dd, cd, legacy_cd, _ruined = summarize_trade_pnls(trade_pnls)
    total = len(trades)
    summary = SymbolSummary(
        symbol=symbol,
        trades=total,
        wins=wins,
        losses=losses,
        win_rate_pct=(wins / total * 100.0) if total else 0.0,
        final_return_pct=final_ret,
        max_return_pct=max_ret,
        max_drawdown_pct=max_dd,
        cd_value=cd,
        old_ratio_cd_value=legacy_cd,
    )
    return summary, trades


# -----------------------------
# Worker / aggregation
# -----------------------------
def spec_from_dict(d: Dict[str, Any]) -> StrategySpec:
    # asdict(StrategySpec)로 전달된 payload를 그대로 복원한다.
    # 이전 버전의 StrategyParams 참조는 이 파일 구조와 맞지 않아 Windows multiprocess에서 즉시 실패했다.
    allowed = {field.name for field in StrategySpec.__dataclass_fields__.values()}
    clean = {k: v for k, v in d.items() if k in allowed}
    return StrategySpec(**clean)


def worker_init(strategy_dicts: List[Dict[str, Any]]) -> None:
    global STRATEGIES
    STRATEGIES = [spec_from_dict(d) for d in strategy_dicts]


def ensure_worker_strategies() -> None:
    global STRATEGIES
    if not STRATEGIES:
        # Windows spawn 방식에서는 부모 프로세스에서 설정한 전역 STRATEGIES가 자식에게 전달되지 않을 수 있다.
        # 이 경우 최소한 전체 300개 전략을 복원해 빈 결과가 나오지 않도록 방어한다.
        STRATEGIES = build_strategies()


def process_symbol_job(job: Tuple[str, str]) -> Dict[str, Any]:
    ensure_worker_strategies()
    symbol, path_str = job
    path = Path(path_str)
    t0 = time.perf_counter()
    df = load_df(path)
    t1 = time.perf_counter()
    f = prepare_features(df)
    t2 = time.perf_counter()

    out: Dict[str, Any] = {
        "symbol": symbol,
        "path": str(path),
        "bars": int(len(df)),
        "timing": {
            "load_sec": round(t1 - t0, 4),
            "feature_sec": round(t2 - t1, 4),
            "backtest_sec": 0.0,
        },
        "strategies": {},
        "error": None,
    }

    bt_total = 0.0
    for spec in STRATEGIES:
        s0 = time.perf_counter()
        summary, trades = simulate_strategy_on_symbol(symbol, f, spec)
        s1 = time.perf_counter()
        bt_total += s1 - s0
        out["strategies"][spec.name] = {
            "summary": asdict(summary),
            "trades": trades,
        }

    out["timing"]["backtest_sec"] = round(bt_total, 4)
    return out


def init_aggregates() -> Dict[str, StrategyAggregate]:
    return {spec.name: StrategyAggregate(spec=spec) for spec in STRATEGIES}


def merge_result(aggs: Dict[str, StrategyAggregate], item: Dict[str, Any]) -> None:
    for spec in STRATEGIES:
        data = item["strategies"][spec.name]
        summary = SymbolSummary(**data["summary"])
        trades = [(int(ts), float(pnl)) for ts, pnl in data["trades"]]
        agg = aggs[spec.name]
        agg.per_symbol_summary.append(summary)
        agg.trades.extend(trades)
        agg.total_trades += summary.trades
        agg.total_wins += summary.wins
        agg.total_losses += summary.losses
        agg.processed_symbols += 1


def strategy_summary(agg: StrategyAggregate) -> Dict[str, Any]:
    ordered = sorted(agg.trades, key=lambda x: x[0])
    pnl_list = [pnl for _, pnl in ordered]
    final_ret, max_ret, max_dd, cd, legacy_cd, ruined = summarize_trade_pnls(pnl_list)
    win_rate = (agg.total_wins / agg.total_trades * 100.0) if agg.total_trades else 0.0
    official_pass = (not ruined) and (agg.total_trades > 0) and (max_dd < 5.0) and (max_ret > 0.0)

    if ruined:
        verdict = "ruin"
    elif agg.total_trades <= 0:
        verdict = "no_trade"
    elif max_dd >= 5.0:
        verdict = "mdd_fail"
    elif max_ret <= 0:
        verdict = "return_fail"
    else:
        verdict = "official_mdd_pass"

    d = asdict(agg.spec)
    return {
        "batch_label": BATCH_LABEL,
        "strategy_name": agg.spec.name,
        "parent": agg.spec.parent,
        "family": agg.spec.family,
        "group": agg.spec.group,
        "side": agg.spec.side,
        "description": agg.spec.description,
        "timeframe": TIMEFRAME_LABEL,
        "processed_symbols": agg.processed_symbols,
        "trades": agg.total_trades,
        "wins": agg.total_wins,
        "losses": agg.total_losses,
        "win_rate_pct": round(win_rate, 6),
        "final_return_pct": round(final_ret, 6),
        "max_return_pct": round(max_ret, 6),
        "max_drawdown_pct": round(max_dd, 6),
        "cd_value": round(cd, 9),
        "cd_formula": "100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)",
        "old_ratio_cd_value": round(legacy_cd, 6),
        "reference_safe6v2_cd_value": REFERENCE_SAFE6V2_CD_VALUE,
        "official_pass_mdd_lt_5": official_pass,
        "ruined": ruined,
        "verdict": verdict,
        "params": d,
    }


def write_outputs(result_root: Path, aggs: Dict[str, StrategyAggregate], failed_symbols: List[Dict[str, str]], timing: Dict[str, float]) -> None:
    result_root.mkdir(parents=True, exist_ok=True)
    summaries = [strategy_summary(agg) for agg in aggs.values()]

    def sort_key_any(x: Dict[str, Any]) -> Tuple[float, float, int]:
        return (float(x["cd_value"]), -float(x["max_drawdown_pct"]), int(x["trades"]))

    def best_any(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return max(rows, key=sort_key_any) if rows else None

    def best_mdd5(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        rows2 = [x for x in rows if x["official_pass_mdd_lt_5"]]
        return best_any(rows2)

    summaries.sort(
        key=lambda x: (
            1 if x["official_pass_mdd_lt_5"] else 0,
            x["cd_value"],
            x["max_return_pct"],
            -x["max_drawdown_pct"],
        ),
        reverse=True,
    )

    long_rows = [x for x in summaries if x["side"] == "long"]
    short_rows = [x for x in summaries if x["side"] == "short"]

    top_any_cd_value = sorted(summaries, key=lambda x: (-float(x["cd_value"]), float(x["max_drawdown_pct"]), -int(x["trades"])))[:20]
    top_mdd5_cd_value = sorted([x for x in summaries if x["official_pass_mdd_lt_5"]], key=lambda x: (-float(x["cd_value"]), float(x["max_drawdown_pct"]), -int(x["trades"])))[:20]

    leaders = {
        "long_main_candidate_mdd5": best_mdd5(long_rows),
        "long_max_candidate_any": best_any(long_rows),
        "short_main_candidate_mdd5": best_mdd5(short_rows),
        "short_max_candidate_any": best_any(short_rows),
    }

    def compare(row: Optional[Dict[str, Any]], ref: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if row is None:
            return None
        return {
            "candidate_strategy": row["strategy_name"],
            "reference_alias": ref["alias"],
            "reference_strategy": ref["strategy_name"],
            "candidate_side": row["side"],
            "candidate_cd_value": row["cd_value"],
            "reference_cd_value": ref["cd_value"],
            "delta_cd_value": float(row["cd_value"]) - float(ref["cd_value"]),
            "beat_reference": float(row["cd_value"]) > float(ref["cd_value"]),
            "candidate_mdd": row["max_drawdown_pct"],
            "reference_mdd": ref["max_drawdown_pct"],
            "candidate_max_return": row["max_return_pct"],
            "reference_max_return": ref["max_return_pct"],
            "candidate_trades": row["trades"],
        }

    reference_comparison = {
        "long_main_v1": compare(leaders["long_main_candidate_mdd5"], REFERENCE_LONG_MAIN),
        "long_max_v1": compare(leaders["long_max_candidate_any"], REFERENCE_LONG_MAX),
        "short_main_v1": compare(leaders["short_main_candidate_mdd5"], REFERENCE_SHORT_MAIN),
        "short_max_v1": compare(leaders["short_max_candidate_any"], REFERENCE_SHORT_MAX),
    }

    json_dump(result_root / "master_summary.json", {
        "batch_label": BATCH_LABEL,
        "cd_value_formula": "100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)",
        "official_promotion": "max_drawdown_pct < 5.0",
        "reference_comparison": reference_comparison,
        "leaders": leaders,
        "top_any_cd_value": top_any_cd_value,
        "top_mdd5_cd_value": top_mdd5_cd_value,
        "summaries": summaries,
        "failed_symbols": failed_symbols,
        "timing": timing,
    })

    registry_rows: List[Dict[str, Any]] = []
    for s in summaries:
        row = {k: v for k, v in s.items() if k != "params"}
        registry_rows.append(row)

    if registry_rows:
        fieldnames = list(registry_rows[0].keys())
        with (result_root / f"{BATCH_LABEL}_registry.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(registry_rows)
    else:
        with (result_root / f"{BATCH_LABEL}_registry.csv").open("w", encoding="utf-8-sig", newline="") as f:
            f.write("empty\n")

    json_dump(result_root / "failed_symbols.json", failed_symbols)
    json_dump(result_root / "timing.json", timing)
    json_dump(result_root / "strategies.json", [asdict(spec) for spec in STRATEGIES])

    for s in summaries:
        agg = aggs[s["strategy_name"]]
        sroot = result_root / s["strategy_name"]
        sroot.mkdir(parents=True, exist_ok=True)
        json_dump(sroot / "summary.json", s)
        json_dump(sroot / "registry.json", {
            "batch_label": BATCH_LABEL,
            "strategy_name": s["strategy_name"],
            "side": s["side"],
            "description": s["description"],
            "timeframe": TIMEFRAME_LABEL,
            "summary_file": "summary.json",
            "per_symbol_file": "per_symbol_summary.json",
            "summary": {k: v for k, v in s.items() if k != "params"},
        })
        per_symbol = [asdict(x) for x in agg.per_symbol_summary]
        per_symbol.sort(key=lambda x: (x["cd_value"], x["max_return_pct"]), reverse=True)
        json_dump(sroot / "per_symbol_summary.json", per_symbol)

    def fmt_row(row: Optional[Dict[str, Any]]) -> str:
        if row is None:
            return "None"
        return (
            f"{row['strategy_name']} | side={row['side']} | cd={row['cd_value']:.6f} | "
            f"mdd={row['max_drawdown_pct']:.4f} | max={row['max_return_pct']:.4f} | "
            f"trades={row['trades']} | verdict={row['verdict']}"
        )

    lines: List[str] = []
    lines.append(f"batch={BATCH_LABEL}")
    lines.append("cd_value_formula=100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)")
    lines.append("official_promotion=max_drawdown_pct < 5.0")
    lines.append(f"strategies={len(STRATEGIES)}")
    lines.append(f"failed_symbols={len(failed_symbols)}")
    lines.append("")
    lines.append("REFERENCE BASELINES")
    for ref in ALL_REFERENCES:
        lines.append(f"{ref['alias']}={ref['strategy_name']} | side={ref['side']} | cd={ref['cd_value']:.6f} | mdd={ref['max_drawdown_pct']:.4f} | max={ref['max_return_pct']:.4f}")
    lines.append("")
    lines.append("BASELINE CHANGE CHECK")
    for alias, comp in reference_comparison.items():
        if comp is None:
            lines.append(f"{alias}: no candidate")
        else:
            lines.append(
                f"{alias}: candidate={comp['candidate_strategy']} | delta_cd={comp['delta_cd_value']:.6f} | "
                f"beat={comp['beat_reference']} | cand_cd={comp['candidate_cd_value']:.6f} | ref_cd={comp['reference_cd_value']:.6f} | "
                f"cand_mdd={comp['candidate_mdd']:.4f} | cand_max={comp['candidate_max_return']:.4f} | trades={comp['candidate_trades']}"
            )
    lines.append("")
    lines.append("LEADERS")
    lines.append(f"long_mdd5_cd_1={fmt_row(leaders['long_main_candidate_mdd5'])}")
    lines.append(f"long_any_cd_1={fmt_row(leaders['long_max_candidate_any'])}")
    lines.append(f"short_mdd5_cd_1={fmt_row(leaders['short_main_candidate_mdd5'])}")
    lines.append(f"short_any_cd_1={fmt_row(leaders['short_max_candidate_any'])}")
    lines.append("")
    lines.append("TOP 40 BY OFFICIAL-FIRST SORT")
    for i, s in enumerate(summaries[:40], start=1):
        lines.append(
            f"{i:02d}. {s['strategy_name']} | parent={s['parent']} | family={s['family']} | group={s['group']} | side={s['side']} | "
            f"verdict={s['verdict']} | trades={s['trades']} | win={s['win_rate_pct']:.4f} | "
            f"final={s['final_return_pct']:.4f} | max={s['max_return_pct']:.4f} | "
            f"mdd={s['max_drawdown_pct']:.4f} | cd={s['cd_value']:.6f} | old_ratio_cd={s['old_ratio_cd_value']:.4f}"
        )
    (result_root / "master_summary.txt").write_text("\n".join(lines), encoding="utf-8")


def partial_write(result_root: Path, aggs: Dict[str, StrategyAggregate], failed_symbols: List[Dict[str, str]], timing: Dict[str, float]) -> None:
    try:
        write_outputs(result_root, aggs, failed_symbols, timing)
    except Exception as e:
        log(f"[WARN] partial save failed: {e}")


# -----------------------------
# Main runner
# -----------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="8V12 long/short main/max 400 fresh no-trade-cap local backtest")
    parser.add_argument("--repo-root", default=None, help="Repository/local project root. Default: auto-discover from cwd/script")
    parser.add_argument("--data-root", default=None, help="OHLCV CSV root. Default: auto-discover")
    parser.add_argument("--symbol-cost", default=None, help="symbol_cost file/dir. Default: auto-discover")
    parser.add_argument("--result-root", default=None, help="Output root. Default: <repo>/local_results/<batch>")
    parser.add_argument("--workers", type=int, default=1, help="Process workers. Default 1 for Windows-safe deterministic execution")
    parser.add_argument("--max-symbols", type=int, default=0, help="Debug: limit symbols. 0 means all")
    parser.add_argument("--strategy-limit", type=int, default=0, help="Debug: limit strategies. 0 means all 400")
    parser.add_argument("--dry-run", action="store_true", help="Only print discovered paths and strategy count")
    return parser.parse_args()


def run_batch(args: argparse.Namespace) -> None:
    global STRATEGIES

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else find_repo_root()
    data_root = resolve_data_root(repo_root, args.data_root)
    symbol_cost = resolve_symbol_cost(repo_root, args.symbol_cost)
    result_root = Path(args.result_root).expanduser().resolve() if args.result_root else (repo_root / "local_results" / BATCH_LABEL)
    result_root.mkdir(parents=True, exist_ok=True)

    STRATEGIES = build_strategies()
    if args.strategy_limit and args.strategy_limit > 0:
        STRATEGIES = STRATEGIES[:args.strategy_limit]

    data_map = build_data_file_map(data_root)
    symbols = load_symbols(symbol_cost, data_map)
    jobs: List[Tuple[str, str]] = []
    for symbol in symbols:
        p = resolve_symbol_path(symbol, data_map)
        if p is not None:
            jobs.append((symbol, str(p)))

    jobs = sorted(set(jobs), key=lambda x: x[0])
    if args.max_symbols and args.max_symbols > 0:
        jobs = jobs[:args.max_symbols]

    log("=" * 72)
    log(f"BATCH_LABEL: {BATCH_LABEL}")
    log(f"repo_root   : {repo_root}")
    log(f"data_root   : {data_root}")
    log(f"symbol_cost : {symbol_cost}")
    log(f"result_root : {result_root}")
    log(f"symbols     : {len(jobs)}")
    log(f"strategies  : {len(STRATEGIES)}")
    log(f"workers     : {args.workers}")
    log("cd_value    : 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)")
    log("official    : max_drawdown_pct < 5.0")
    log("branches    : 100 long_main_v1 + 100 long_max_v1 + 100 short_main_v1 + 100 short_max_v1")
    log("=" * 72)

    if args.dry_run:
        log("dry-run finished.")
        return

    if not jobs:
        raise RuntimeError("테스트할 심볼이 없습니다. data_root와 symbol_cost를 확인하십시오.")

    aggs = init_aggregates()
    failed_symbols: List[Dict[str, str]] = []
    timing = {
        "load_sec": 0.0,
        "feature_sec": 0.0,
        "backtest_sec": 0.0,
        "wall_sec": 0.0,
    }

    start = time.perf_counter()
    done = 0

    if args.workers <= 1:
        for job in jobs:
            try:
                item = process_symbol_job(job)
                merge_result(aggs, item)
                timing["load_sec"] += float(item["timing"]["load_sec"])
                timing["feature_sec"] += float(item["timing"]["feature_sec"])
                timing["backtest_sec"] += float(item["timing"]["backtest_sec"])
            except Exception as e:
                err = {"symbol": job[0], "path": job[1], "error": repr(e), "traceback": traceback.format_exc()}
                failed_symbols.append(err)
                if len(failed_symbols) <= 5:
                    log(f"[FAIL] {job[0]} | {repr(e)}")
            done += 1
            if done % SAVE_EVERY == 0 or done == len(jobs):
                timing["wall_sec"] = round(time.perf_counter() - start, 4)
                partial_write(result_root, aggs, failed_symbols, timing)
                log(f"[{done}/{len(jobs)}] saved | failed={len(failed_symbols)} | elapsed={timing['wall_sec']}s")
    else:
        strategy_payload = [asdict(spec) for spec in STRATEGIES]
        with ProcessPoolExecutor(max_workers=args.workers, initializer=worker_init, initargs=(strategy_payload,)) as ex:
            futs = {ex.submit(process_symbol_job, job): job for job in jobs}
            for fut in as_completed(futs):
                job = futs[fut]
                try:
                    item = fut.result()
                    merge_result(aggs, item)
                    timing["load_sec"] += float(item["timing"]["load_sec"])
                    timing["feature_sec"] += float(item["timing"]["feature_sec"])
                    timing["backtest_sec"] += float(item["timing"]["backtest_sec"])
                except Exception as e:
                    failed_symbols.append({"symbol": job[0], "path": job[1], "error": repr(e)})
                done += 1
                if done % SAVE_EVERY == 0 or done == len(jobs):
                    timing["wall_sec"] = round(time.perf_counter() - start, 4)
                    partial_write(result_root, aggs, failed_symbols, timing)
                    log(f"[{done}/{len(jobs)}] saved | failed={len(failed_symbols)} | elapsed={timing['wall_sec']}s")

    timing["wall_sec"] = round(time.perf_counter() - start, 4)
    write_outputs(result_root, aggs, failed_symbols, timing)

    # 백테스트 종료 즉시 갱신된 기준선만 콘솔에 출력한다. 갱신이 없으면 none만 출력한다.
    summary_json = result_root / "master_summary.json"
    if summary_json.exists():
        try:
            data = json.loads(summary_json.read_text(encoding="utf-8"))
            comps = data.get("reference_comparison", {})
            updated = []
            for alias, comp in comps.items():
                if comp and comp.get("beat_reference"):
                    updated.append((alias, comp))
            log("=" * 72)
            log("UPDATED_BASELINES_ONLY")
            if not updated:
                log("none")
            else:
                for alias, comp in updated:
                    log(
                        f"{alias} -> {comp['candidate_strategy']} | "
                        f"cd={float(comp['candidate_cd_value']):.6f} | "
                        f"delta={float(comp['delta_cd_value']):.6f} | "
                        f"mdd={float(comp['candidate_mdd']):.4f} | "
                        f"max={float(comp['candidate_max_return']):.4f} | "
                        f"trades={comp['candidate_trades']}"
                    )
            log("=" * 72)
        except Exception as e:
            log(f"[WARN] updated baseline print failed: {e}")

    log(f"FINISHED: {result_root}")
    log(f"Open: {result_root / 'master_summary.txt'}")
    log(f"CSV : {result_root / (BATCH_LABEL + '_registry.csv')}")


if __name__ == "__main__":
    try:
        run_batch(parse_args())
    except KeyboardInterrupt:
        log("Interrupted by user.")
        raise
