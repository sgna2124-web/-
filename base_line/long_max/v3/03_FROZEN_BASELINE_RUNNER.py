# -*- coding: utf-8 -*-
"""
LONG_MAIN v7 / LONG_MAX v3 frozen baseline runner

목적:
- 공식 기준선 전략을 이 파일 안에 직접 고정한다.
- 외부 기준선 코드 파일, base_line 파일, 깃허브 경로를 읽지 않는다.
- 처음 보는 사람이 이 파일 하나로 기준선 재현 여부를 확인할 수 있게 한다.

공식 전략:
8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110

고정 조건:
- parent entry: orig_V09_extreme_vol18
- child entry: child::orig_V09_extreme_vol18::tp03
- atr_stop: 1.10
- rr_target: 2.90
- max_hold_bars: 21
- cooldown_bars: 31
- position_fraction: 0.01
- round_trip_cost_bps: 8.0

공식 기대 결과:
- trades: 57114
- wins: 20911
- losses: 36203
- win_rate_pct: 36.6127394334
- final_return_pct: 240.7307747654
- max_return_pct: 241.3427142366
- max_drawdown_pct: 1.3408670828
- official_cd_value: 336.7657621418
- max_conc: 435
- errors: 0

실행 예:
python 03_FROZEN_BASELINE_RUNNER.py
python 03_FROZEN_BASELINE_RUNNER.py --workers 1
python 03_FROZEN_BASELINE_RUNNER.py --data-root ./코인/Data/time --workers 2
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


RUN_LABEL = "LONG_MAIN_V7_LONG_MAX_V3_FROZEN_BASELINE"
STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110"
PARENT_NAME = "8V4_V09_V054_extreme_vol18"
PARENT_ENTRY_KEY = "orig_V09_extreme_vol18"
ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
SIDE = "long"
MIN_BARS = 250
WARMUP_BARS = 120
RUIN_THRESHOLD = 1e-12
DEFAULT_POSITION_FRACTION = 0.01
DEFAULT_ROUND_TRIP_COST_BPS = 8.0

EXPECTED = {
    "strategy": STRATEGY_NAME,
    "trades": 57114,
    "wins": 20911,
    "losses": 36203,
    "win_rate_pct": 36.6127394334,
    "final_return_pct": 240.7307747654,
    "max_return_pct": 241.3427142366,
    "max_drawdown_pct": 1.3408670828,
    "official_cd_value": 336.7657621418,
    "max_conc": 435,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


@dataclass(frozen=True)
class StrategySpec:
    name: str = STRATEGY_NAME
    side: str = SIDE
    description: str = "OFFICIAL FROZEN BASELINE: V09 extreme vol18 parent + TP03 + rr 2.90 + atr_stop 1.10"
    entry_key: str = ENTRY_KEY
    atr_stop: float = 1.10
    rr_target: float = 2.90
    max_hold_bars: int = 21
    cooldown_bars: int = 31
    use_tp03_gate: bool = True


@dataclass
class TradeRecord:
    symbol: str
    strategy: str
    entry_ts: int
    exit_ts: int
    pnl_pct: float
    hold_bars: int
    entry_price: float
    exit_price: float
    exit_reason: str


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
    vol_ratio: np.ndarray
    body_atr: np.ndarray
    close_pos: np.ndarray
    lower_wick_body_ratio: np.ndarray
    ll20: np.ndarray
    range_mid20: np.ndarray
    ret3: np.ndarray
    ret5: np.ndarray
    quiet_ratio: np.ndarray


def log(msg: str) -> None:
    print(msg, flush=True)


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
    if isinstance(obj, Path):
        return str(obj)
    return obj


def normalize_symbol_text(x: str) -> str:
    s = str(x).strip().upper()
    for ch in ["-", "_", "/", ":", " ", "."]:
        s = s.replace(ch, "")
    return s


def infer_symbol_from_path(path: Path) -> str:
    stem = path.stem.upper().replace("-", "_")
    parts = stem.split("_")
    if len(parts) >= 2 and parts[-1] in {"1M", "3M", "5M", "15M", "30M", "1H", "2H", "4H", "1D"}:
        stem = "_".join(parts[:-1])
    stem = stem.replace("_PERP", "").replace("PERP", "")
    if "/USDT" not in stem and "USDT" in stem:
        stem = stem.replace("USDT", "/USDT")
    elif "/BUSD" not in stem and "BUSD" in stem:
        stem = stem.replace("BUSD", "/BUSD")
    elif "/USD" not in stem and stem.endswith("USD"):
        stem = stem[:-3] + "/USD"
    while "__" in stem:
        stem = stem.replace("__", "_")
    return stem


def unique_paths(paths: Iterable[Path]) -> List[Path]:
    out: List[Path] = []
    seen = set()
    for p in paths:
        try:
            rp = p.resolve()
        except Exception:
            rp = p.absolute()
        key = str(rp).lower()
        if key not in seen:
            out.append(rp)
            seen.add(key)
    return out


def candidate_base_dirs() -> List[Path]:
    script_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()
    bases: List[Path] = []
    for base in [cwd, script_dir]:
        bases.append(base)
        bases.extend(list(base.parents))
    return unique_paths(bases)


def find_data_root(explicit: Optional[str]) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"--data-root 경로가 없습니다: {p}")
        return p
    candidates: List[Path] = []
    for base in candidate_base_dirs():
        candidates.extend([base / "Data" / "time", base / "코인" / "Data" / "time", base / "data" / "time", base / "coin" / "Data" / "time"])
    for p in unique_paths(candidates):
        if p.exists() and any(p.rglob("*.csv")):
            return p
    cwd = Path.cwd().resolve()
    for p in cwd.rglob("time"):
        try:
            if p.is_dir() and p.parent.name.lower() == "data" and any(p.rglob("*.csv")):
                return p.resolve()
        except Exception:
            continue
    raise FileNotFoundError("OHLCV 데이터 폴더를 찾지 못했다. 필요하면 --data-root 로 지정해라.")


def find_symbol_cost_path(explicit: Optional[str]) -> Optional[Path]:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"--symbol-cost 경로가 없습니다: {p}")
        return p
    candidates: List[Path] = []
    for base in candidate_base_dirs():
        candidates.extend([base / "symbol_cost", base / "코인" / "symbol_cost", base / "symbol_cost.csv", base / "코인" / "symbol_cost.csv", base / "symbols.csv", base / "코인" / "symbols.csv"])
    for p in unique_paths(candidates):
        if p.exists():
            return p
    return None


def build_data_file_map(data_root: Path) -> Dict[str, Path]:
    mapping: Dict[str, Path] = {}
    for p in sorted(data_root.rglob("*.csv")):
        for key in {normalize_symbol_text(p.stem), normalize_symbol_text(infer_symbol_from_path(p))}:
            mapping.setdefault(key, p)
    if not mapping:
        raise FileNotFoundError(f"CSV 데이터 파일을 찾지 못했습니다: {data_root}")
    return mapping


def read_symbol_file(path: Path) -> List[str]:
    symbols: List[str] = []
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("symbols", list(data.values()))
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    symbols.append(item)
                elif isinstance(item, dict):
                    s = item.get("symbol") or item.get("ticker") or item.get("name")
                    if s:
                        symbols.append(str(s))
    elif path.suffix.lower() in {".csv", ".txt"}:
        try:
            df = pd.read_csv(path)
            cols = [c for c in df.columns if str(c).lower() in {"symbol", "ticker", "name", "market"}]
            symbols = df[cols[0]].dropna().astype(str).tolist() if cols else df.iloc[:, 0].dropna().astype(str).tolist()
        except Exception:
            symbols = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return symbols


def load_symbols(symbol_cost_path: Optional[Path], data_file_map: Dict[str, Path]) -> List[str]:
    symbols: List[str] = []
    if symbol_cost_path is not None:
        if symbol_cost_path.is_file():
            symbols = read_symbol_file(symbol_cost_path)
        elif symbol_cost_path.is_dir():
            files: List[Path] = []
            for pat in ["*.csv", "*.json", "*.txt"]:
                files.extend(sorted(symbol_cost_path.rglob(pat)))
            if files:
                symbols = read_symbol_file(files[0])
    if symbols:
        resolved = []
        for s in symbols:
            p = data_file_map.get(normalize_symbol_text(s))
            if p is not None:
                resolved.append(infer_symbol_from_path(p))
        if resolved:
            return sorted(set(resolved))
    return sorted({infer_symbol_from_path(p) for p in data_file_map.values()})


def resolve_symbol_path(symbol: str, data_file_map: Dict[str, Path]) -> Optional[Path]:
    return data_file_map.get(normalize_symbol_text(symbol))


def rma(s: pd.Series, length: int) -> pd.Series:
    return s.ewm(alpha=1.0 / max(1, length), adjust=False).mean()


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return rma(tr, length).bfill().fillna(0.0)


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    diff = series.diff().fillna(0.0)
    up = diff.clip(lower=0.0)
    down = (-diff).clip(lower=0.0)
    avg_up = rma(up, length)
    avg_down = rma(down, length)
    rs = avg_up / avg_down.replace(0, np.nan)
    return (100.0 - (100.0 / (1.0 + rs))).fillna(50.0)


def standardize_ohlcv_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = {str(c).lower().strip(): c for c in df.columns}
    rename_map: Dict[Any, str] = {}
    for low_name, target in [("timestamp", "timestamp"), ("open_time", "timestamp"), ("opentime", "timestamp"), ("time", "timestamp"), ("date", "timestamp"), ("datetime", "timestamp"), ("open", "open"), ("high", "high"), ("low", "low"), ("close", "close"), ("volume", "volume"), ("vol", "volume")]:
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
    return df.dropna().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)


def compute_features(df: pd.DataFrame) -> FeaturePack:
    c, h, l, o, v = df["close"], df["high"], df["low"], df["open"], df["volume"]
    atr14 = atr(df, 14)
    atrp = (atr14 / c.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    rsi14 = rsi(c, 14)
    vol_ma20 = v.rolling(20, min_periods=1).mean()
    vol_ratio = (v / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    body = (c - o).abs()
    lower_wick = pd.concat([o, c], axis=1).min(axis=1) - l
    body_atr = (body / atr14.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    bar_range = (h - l).replace(0, np.nan)
    close_pos = ((c - l) / bar_range).replace([np.inf, -np.inf], np.nan).fillna(0.5)
    lower_wick_body_ratio = (lower_wick / body.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    ll20 = l.rolling(20, min_periods=1).min()
    hh20 = h.rolling(20, min_periods=1).max()
    range_mid20 = ll20 + (hh20 - ll20) * 0.5
    tr = pd.concat([(h - l).abs(), (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    quiet_ratio = (tr.ewm(span=6, adjust=False).mean() / tr.ewm(span=24, adjust=False).mean().replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    return FeaturePack(
        timestamp=df["timestamp"].astype("int64").to_numpy(), open=o.to_numpy(float), high=h.to_numpy(float), low=l.to_numpy(float), close=c.to_numpy(float), volume=v.to_numpy(float),
        atr14=atr14.to_numpy(float), atrp=atrp.to_numpy(float), rsi14=rsi14.to_numpy(float), vol_ratio=vol_ratio.to_numpy(float), body_atr=body_atr.to_numpy(float), close_pos=close_pos.to_numpy(float), lower_wick_body_ratio=lower_wick_body_ratio.to_numpy(float), ll20=ll20.to_numpy(float), range_mid20=range_mid20.to_numpy(float), ret3=c.pct_change(3).fillna(0.0).to_numpy(float), ret5=c.pct_change(5).fillna(0.0).to_numpy(float), quiet_ratio=quiet_ratio.to_numpy(float)
    )


def load_feature_pack(csv_path: Path, max_bars: int) -> FeaturePack:
    df = standardize_ohlcv_columns(pd.read_csv(csv_path))
    if max_bars and max_bars > 0 and len(df) > max_bars:
        df = df.tail(max_bars).reset_index(drop=True)
    return compute_features(df)


def raw_l01_signal_at(f: FeaturePack, i: int) -> bool:
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    bull_reclaim = f.low[i] < ll20_prev and f.close[i] > ll20_prev and f.close[i] > f.open[i] and f.close_pos[i] > 0.70
    return (f.ret3[i] < -0.04 or f.ret5[i] < -0.06) and bull_reclaim and f.vol_ratio[i] > 1.40 and f.body_atr[i] > 0.35 and f.atrp[i] > 0.003


def raw_shock_down_at(f: FeaturePack, i: int) -> bool:
    return (f.ret3[i] <= -0.035 or f.ret5[i] <= -0.050) and f.vol_ratio[i] >= 1.10 and f.body_atr[i] >= 0.25


def raw_extreme_reclaim_at(f: FeaturePack, i: int) -> bool:
    return raw_l01_signal_at(f, i) and f.close_pos[i] >= 0.80 and f.lower_wick_body_ratio[i] >= 1.50 and f.vol_ratio[i] >= 1.60


def raw_shock_reversal_balance_at(f: FeaturePack, i: int) -> bool:
    if i < 22:
        return False
    return (f.ret3[i] <= -0.025 or f.ret5[i] <= -0.040) and f.close[i] > f.open[i] and f.close_pos[i] >= 0.70 and f.vol_ratio[i] >= 0.90 and f.body_atr[i] >= 0.16 and f.rsi14[i] <= 48.0 and f.quiet_ratio[i] <= 1.45


def compute_frozen_entry_mask(f: FeaturePack, spec: StrategySpec) -> np.ndarray:
    n = len(f.close)
    shock_down = np.zeros(n, dtype=bool)
    l01 = np.zeros(n, dtype=bool)
    shock_balance = np.zeros(n, dtype=bool)
    extreme = np.zeros(n, dtype=bool)
    for i in range(max(21, WARMUP_BARS), n - 1):
        shock_down[i] = raw_shock_down_at(f, i)
        l01[i] = raw_l01_signal_at(f, i)
        shock_balance[i] = raw_shock_reversal_balance_at(f, i)
        extreme[i] = raw_extreme_reclaim_at(f, i)
    family_v09 = shock_down | l01 | shock_balance
    anchor_extreme = extreme | (f.rsi14 <= 34.0)
    guard_vol18 = f.vol_ratio >= 1.18
    parent = family_v09 & anchor_extreme & guard_vol18
    target_pct = (float(spec.atr_stop) * f.atr14 * float(spec.rr_target) / np.maximum(f.close, 1e-12)) * 100.0
    entry = parent & (target_pct >= 0.30)
    entry[:WARMUP_BARS] = False
    entry[-1:] = False
    return entry


def max_drawdown_pct_from_equity(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    peaks = np.maximum.accumulate(equity_curve)
    dd = (equity_curve / np.where(peaks == 0, 1.0, peaks) - 1.0) * 100.0
    return min(100.0, float(abs(np.min(dd))) if dd.size else 0.0)


def max_return_pct_from_equity(equity_curve: np.ndarray) -> float:
    return float((np.max(equity_curve) - 1.0) * 100.0) if equity_curve.size else 0.0


def cd_value_from_return_and_mdd(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - max_drawdown_pct / 100.0) * (1.0 + max_return_pct / 100.0)


def equity_curve_from_trade_pnls(trade_pnls_pct: List[float], position_fraction: float) -> Tuple[np.ndarray, bool]:
    if not trade_pnls_pct:
        return np.array([1.0], dtype=float), False
    eq = [1.0]
    cur = 1.0
    ruined = False
    for pnl_pct in trade_pnls_pct:
        cur *= 1.0 + position_fraction * (pnl_pct / 100.0)
        eq.append(cur)
        if cur <= RUIN_THRESHOLD:
            ruined = True
            break
    return np.asarray(eq, dtype=float), ruined


def summarize_trade_pnls(trade_pnls_pct: List[float], position_fraction: float) -> Tuple[float, float, float, float, bool]:
    eq, ruined = equity_curve_from_trade_pnls(trade_pnls_pct, position_fraction)
    final_return_pct = float((eq[-1] - 1.0) * 100.0) if eq.size else 0.0
    max_return_pct = max_return_pct_from_equity(eq)
    max_dd_pct = max_drawdown_pct_from_equity(eq)
    return final_return_pct, max_return_pct, max_dd_pct, cd_value_from_return_and_mdd(max_return_pct, max_dd_pct), ruined


def simulate_strategy_on_symbol(symbol: str, f: FeaturePack, spec: StrategySpec, entry_mask: np.ndarray, round_trip_cost_bps: float) -> List[TradeRecord]:
    trades: List[TradeRecord] = []
    n = len(f.close)
    if n < MIN_BARS:
        return trades
    signal_indices = np.flatnonzero(entry_mask)
    next_allowed_signal_i = WARMUP_BARS
    cost_pct = round_trip_cost_bps * 0.01
    for signal_i in signal_indices:
        if signal_i < next_allowed_signal_i:
            continue
        entry_i = int(signal_i + 1)
        if entry_i >= n:
            break
        entry_price = float(f.open[entry_i])
        atr_val = float(f.atr14[signal_i])
        if not math.isfinite(entry_price) or not math.isfinite(atr_val) or entry_price <= 0 or atr_val <= 0:
            continue
        stop_dist = spec.atr_stop * atr_val
        stop_price = entry_price - stop_dist
        target_price = entry_price + stop_dist * spec.rr_target
        if stop_dist <= 0 or stop_price <= 0:
            continue
        last_i = min(n - 1, entry_i + spec.max_hold_bars)
        exit_i = last_i
        exit_price = float(f.close[last_i])
        exit_reason = "time"
        for j in range(entry_i, last_i + 1):
            hit_stop = float(f.low[j]) <= stop_price
            hit_target = float(f.high[j]) >= target_price
            if hit_stop and hit_target:
                exit_i, exit_price, exit_reason = j, stop_price, "stop_first_same_bar"
                break
            if hit_stop:
                exit_i, exit_price, exit_reason = j, stop_price, "stop"
                break
            if hit_target:
                exit_i, exit_price, exit_reason = j, target_price, "target"
                break
        gross_pct = (exit_price / entry_price - 1.0) * 100.0
        pnl_pct = gross_pct - cost_pct
        trades.append(TradeRecord(symbol, spec.name, int(f.timestamp[entry_i]), int(f.timestamp[exit_i]), float(pnl_pct), int(exit_i - entry_i + 1), float(entry_price), float(exit_price), exit_reason))
        next_allowed_signal_i = int(exit_i + spec.cooldown_bars)
    return trades


def run_symbol_worker(payload: Tuple[str, str, int, float, float, Dict[str, Any], bool]) -> Dict[str, Any]:
    symbol, csv_path_str, max_bars, round_trip_cost_bps, position_fraction, spec_dict, save_full = payload
    spec = StrategySpec(**spec_dict)
    try:
        f = load_feature_pack(Path(csv_path_str), max_bars=max_bars)
        if len(f.close) < MIN_BARS:
            return {"symbol": symbol, "ok": False, "error": f"too few bars: {len(f.close)}", "trades": []}
        mask = compute_frozen_entry_mask(f, spec)
        trades = simulate_strategy_on_symbol(symbol, f, spec, mask, round_trip_cost_bps)
        if save_full:
            rows = [asdict(t) for t in trades]
        else:
            rows = [{"symbol": t.symbol, "strategy": t.strategy, "entry_ts": t.entry_ts, "exit_ts": t.exit_ts, "pnl_pct": t.pnl_pct} for t in trades]
        return {"symbol": symbol, "ok": True, "error": "", "trades": rows}
    except Exception as exc:
        return {"symbol": symbol, "ok": False, "error": repr(exc), "trades": []}


def compute_max_concurrency(trades: List[Dict[str, Any]]) -> int:
    events: List[Tuple[int, int]] = []
    for t in trades:
        try:
            events.append((int(t["entry_ts"]), 1))
            events.append((int(t["exit_ts"]), -1))
        except Exception:
            continue
    events.sort(key=lambda x: (x[0], x[1]))
    cur = 0
    mx = 0
    for _, delta in events:
        cur += delta
        mx = max(mx, cur)
    return int(mx)


def aggregate_results(trades: List[Dict[str, Any]], spec: StrategySpec, position_fraction: float, round_trip_cost_bps: float, symbol_files_count: int, errors_count: int) -> pd.DataFrame:
    pnls = [float(t["pnl_pct"]) for t in trades]
    wins = int(sum(1 for x in pnls if x > 0))
    losses = int(len(pnls) - wins)
    final_return_pct, max_return_pct, max_dd_pct, cd_value, ruined = summarize_trade_pnls(pnls, position_fraction)
    row = {
        "run_label": RUN_LABEL,
        "fee_tag": f"fee_{int(round(round_trip_cost_bps)):03d}_rt_bps",
        "round_trip_cost_bps": round_trip_cost_bps,
        "position_fraction": position_fraction,
        "axis": "long_main_v7_and_long_max_v3",
        "strategy": spec.name,
        "side": spec.side,
        "entry_key": spec.entry_key,
        "description": spec.description,
        "atr_stop": spec.atr_stop,
        "rr_target": spec.rr_target,
        "max_hold_bars": spec.max_hold_bars,
        "cooldown_bars": spec.cooldown_bars,
        "use_tp03_gate": spec.use_tp03_gate,
        "trades": len(pnls),
        "wins": wins,
        "losses": losses,
        "win_rate_pct": (wins / len(pnls) * 100.0) if pnls else 0.0,
        "final_return_pct": final_return_pct,
        "max_return_pct": max_return_pct,
        "max_drawdown_pct": max_dd_pct,
        "official_cd_value": cd_value,
        "cd_value": cd_value,
        "max_conc": compute_max_concurrency(trades),
        "symbol_files": symbol_files_count,
        "errors": errors_count,
        "ruined": bool(ruined),
    }
    return pd.DataFrame([row])


def compare_expected(row: Dict[str, Any]) -> Dict[str, Any]:
    diffs = {}
    for key in ["trades", "wins", "losses", "win_rate_pct", "final_return_pct", "max_return_pct", "max_drawdown_pct", "official_cd_value", "max_conc", "errors"]:
        actual = float(row.get(key, 0.0))
        expected = float(EXPECTED[key])
        diffs[key] = {"actual": actual, "expected": expected, "delta": actual - expected}
    ok = (
        int(row.get("trades", -1)) == EXPECTED["trades"]
        and int(row.get("wins", -1)) == EXPECTED["wins"]
        and int(row.get("losses", -1)) == EXPECTED["losses"]
        and int(row.get("max_conc", -1)) == EXPECTED["max_conc"]
        and int(row.get("errors", -1)) == EXPECTED["errors"]
        and abs(float(row.get("official_cd_value", 0.0)) - EXPECTED["official_cd_value"]) <= 0.001
        and abs(float(row.get("max_return_pct", 0.0)) - EXPECTED["max_return_pct"]) <= 0.001
        and abs(float(row.get("max_drawdown_pct", 0.0)) - EXPECTED["max_drawdown_pct"]) <= 0.001
    )
    return {"pass_frozen_reproduction_gate": bool(ok), "diffs": diffs}


def write_report(out_dir: Path, row: Dict[str, Any], compare: Dict[str, Any]) -> None:
    lines = []
    lines.append(RUN_LABEL)
    lines.append("")
    lines.append(f"strategy: {STRATEGY_NAME}")
    lines.append(f"parent_strategy: {PARENT_NAME}")
    lines.append(f"entry_key: {ENTRY_KEY}")
    lines.append(f"pass_frozen_reproduction_gate: {compare['pass_frozen_reproduction_gate']}")
    lines.append("")
    lines.append("actual_result:")
    for key in ["trades", "wins", "losses", "win_rate_pct", "final_return_pct", "max_return_pct", "max_drawdown_pct", "official_cd_value", "max_conc", "symbol_files", "errors", "ruined"]:
        lines.append(f"- {key}: {row.get(key)}")
    lines.append("")
    lines.append("expected_result:")
    for key, value in EXPECTED.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("diff_vs_expected:")
    for key, value in compare["diffs"].items():
        lines.append(f"- {key}: actual={value['actual']}, expected={value['expected']}, delta={value['delta']}")
    lines.append("")
    lines.append("reproduction_rule:")
    lines.append("- trades, wins, losses가 다르면 재현 실패다.")
    lines.append("- cd_value는 max_return_pct와 max_drawdown_pct로 계산한다.")
    lines.append("- long_main 기준은 MDD 5% 미만 내 cd_value 최대다.")
    lines.append("- long_max 기준은 MDD 제한 없이 cd_value 최대다.")
    (out_dir / "frozen_baseline_reproduction_report.txt").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Frozen runner for long_main v7 / long_max v3 official baseline")
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--symbol-cost", default=None)
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--workers", type=int, default=min(2, max(1, os.cpu_count() or 1)))
    parser.add_argument("--max-symbols", type=int, default=0)
    parser.add_argument("--max-bars", type=int, default=0)
    parser.add_argument("--round-trip-cost-bps", type=float, default=DEFAULT_ROUND_TRIP_COST_BPS)
    parser.add_argument("--position-fraction", type=float, default=DEFAULT_POSITION_FRACTION)
    parser.add_argument("--save-trade-rows", action="store_true")
    parser.add_argument("--save-full-trades", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    t0 = time.time()
    data_root = find_data_root(args.data_root)
    symbol_cost_path = find_symbol_cost_path(args.symbol_cost)
    data_file_map = build_data_file_map(data_root)
    symbols = load_symbols(symbol_cost_path, data_file_map)
    symbols = sorted(set(s for s in symbols if resolve_symbol_path(s, data_file_map) is not None))
    if args.max_symbols and args.max_symbols > 0:
        symbols = symbols[: args.max_symbols]
    if not symbols:
        raise RuntimeError("백테스트할 심볼을 찾지 못했다.")
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else Path.cwd().resolve() / "local_result" / "long_max" / RUN_LABEL
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = StrategySpec()
    payloads = []
    for sym in symbols:
        p = resolve_symbol_path(sym, data_file_map)
        if p is not None:
            payloads.append((sym, str(p), int(args.max_bars), float(args.round_trip_cost_bps), float(args.position_fraction), asdict(spec), bool(args.save_full_trades)))
    log(f"[RUN] {RUN_LABEL}")
    log(f"[STRATEGY] {STRATEGY_NAME}")
    log(f"[ENTRY] {ENTRY_KEY}")
    log(f"[EXPECTED_CD] {EXPECTED['official_cd_value']}")
    log(f"[PATH] cwd={Path.cwd().resolve()}")
    log(f"[PATH] data_root={data_root}")
    log(f"[PATH] symbol_cost={symbol_cost_path}")
    log(f"[PATH] out_dir={out_dir}")
    log(f"[CONFIG] symbols={len(payloads)} workers={args.workers} max_bars={args.max_bars} fee_rt_bps={args.round_trip_cost_bps}")
    results: Dict[str, Dict[str, Any]] = {}
    errors: List[Dict[str, str]] = []
    workers = max(1, int(args.workers))
    if workers == 1:
        for idx, payload in enumerate(payloads, 1):
            r = run_symbol_worker(payload)
            results[payload[0]] = r
            if not r.get("ok"):
                errors.append({"symbol": payload[0], "error": r.get("error", "")})
            if idx % 25 == 0 or idx == len(payloads):
                trade_rows = sum(len(v.get("trades", [])) for v in results.values())
                log(f"[PROGRESS] processed={idx}/{len(payloads)} errors={len(errors)} trade_rows={trade_rows} elapsed={time.time() - t0:.1f}s")
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            future_map = {ex.submit(run_symbol_worker, payload): payload[0] for payload in payloads}
            done = 0
            for fut in as_completed(future_map):
                sym = future_map[fut]
                try:
                    r = fut.result()
                except Exception as exc:
                    r = {"symbol": sym, "ok": False, "error": repr(exc), "trades": []}
                results[sym] = r
                if not r.get("ok"):
                    errors.append({"symbol": sym, "error": r.get("error", "")})
                done += 1
                if done % 25 == 0 or done == len(payloads):
                    trade_rows = sum(len(v.get("trades", [])) for v in results.values())
                    log(f"[PROGRESS] processed={done}/{len(payloads)} errors={len(errors)} trade_rows={trade_rows} elapsed={time.time() - t0:.1f}s")
    all_trades: List[Dict[str, Any]] = []
    for sym in symbols:
        all_trades.extend(results.get(sym, {}).get("trades", []))
    agg_df = aggregate_results(all_trades, spec, float(args.position_fraction), float(args.round_trip_cost_bps), len(payloads), len(errors))
    row = agg_df.iloc[0].to_dict()
    compare = compare_expected(row)
    agg_df.to_csv(out_dir / "frozen_baseline_aggregate_results.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(all_trades).to_csv(out_dir / ("frozen_baseline_trades_full.csv" if args.save_full_trades else "frozen_baseline_trades_compact.csv"), index=False, encoding="utf-8-sig") if args.save_trade_rows else None
    (out_dir / "frozen_baseline_errors.json").write_text(json.dumps(to_serializable(errors), ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "frozen_baseline_strategy.json").write_text(json.dumps(to_serializable(asdict(spec)), ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(out_dir, row, compare)
    meta = {"run_label": RUN_LABEL, "strategy": STRATEGY_NAME, "parent_strategy": PARENT_NAME, "entry_key": ENTRY_KEY, "expected": EXPECTED, "actual": row, "compare": compare, "strategy_spec": asdict(spec), "data_root": str(data_root), "symbol_cost_path": str(symbol_cost_path) if symbol_cost_path else None, "out_dir": str(out_dir), "symbols": len(payloads), "workers": workers, "elapsed_sec": time.time() - t0}
    (out_dir / "run_meta.json").write_text(json.dumps(to_serializable(meta), ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"[RESULT] cd_value={float(row.get('official_cd_value', 0.0)):.10f} trades={int(row.get('trades', 0))} mdd={float(row.get('max_drawdown_pct', 0.0)):.10f}")
    log(f"[REPORT] pass_frozen_reproduction_gate={compare['pass_frozen_reproduction_gate']}")
    log(f"[OUT] {out_dir}")


if __name__ == "__main__":
    main()
