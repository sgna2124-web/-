
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import shutil
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

BATCH = 'V31_BASELINE_AUDIT_FEE_004'
AUDIT_FEE_PCT_PER_SIDE = 0.04
AUDIT_ROUND_TRIP_FEE_PCT = 0.08
AUDIT_BASELINE_ONLY = True
AUDIT_TP03_ON_BASELINE = False
AUDIT_CANDLE_LIMIT = "NO_LIMIT_MAX_BARS_0"

POS_FRAC = 0.01
COST_PCT = 0.04
WARMUP = 140
MIN_BARS = 260
SEED = 821
MIN_EXPECTED_TP = 0.0
REC_DTYPE = np.dtype([("ts", "<i8"), ("pnl", "<f4")])

# CORE_SUMMARY 기준선. 첫 4개는 반드시 기준선 복제본으로 먼저 실행한다.
BASELINES = {
    "long_main": {
        "name": "6V2_L01_doubleflush_core",
        "side": "long",
        "trades": 592,
        "max_return_pct": 23.919060,
        "max_drawdown_pct": 1.751183,
        "official_cd_value": 121.7490287208,
    },
    "long_max": {
        "name": "8V4_V51_V002_core_rare22_c1",
        "side": "long",
        "trades": 2276,
        "max_return_pct": 44.266371,
        "max_drawdown_pct": 6.758722,
        "official_cd_value": 134.5158668232,
    },
    "short_main": {
        "name": "short_beh_dd_brake",
        "side": "short",
        "trades": 28017,
        "max_return_pct": 311.812150,
        "max_drawdown_pct": 4.758886,
        "official_cd_value": 392.2144692142,
    },
    "short_max": {
        "name": "short_only_reference_1x",
        "side": "short",
        "trades": 36505,
        "max_return_pct": 394.614496,
        "max_drawdown_pct": 7.779240,
        "official_cd_value": 456.1374488160,
    },
}

EMBEDDED_BASELINE_SOURCE = {
    "long_main": {"source": "CORE_SUMMARY 8V12 base_safe6v2_profile", "strategy": "6V2_L01_doubleflush_core"},
    "long_max": {"source": "CORE_SUMMARY 8V12 base_rawv51_profile", "strategy": "8V4_V51_V002_core_rare22_c1"},
    "short_main": {
        "source": "v52 short_only_behavioral_guards JSON embedded",
        "strategy": "short_beh_dd_brake",
        "quality": {"short_dev": 0.033, "short_rsi_min": 77},
        "risk": {"atr_stop_mult": 1.8975, "rr_mult": 6.0, "timeout_bars": 200},
        "trade_control": {"dd_brake_trigger_pct": 0.03, "dd_brake_freeze_steps": 5},
    },
    "short_max": {
        "source": "v42 rr60 t200 short_only JSON embedded",
        "strategy": "short_only_reference_1x",
        "quality": {"short_dev": 0.032, "short_rsi_min": 76},
        "risk": {"atr_stop_mult": 1.8975, "rr_mult": 6.0, "timeout_bars": 200},
    },
}

TOL_TRADES_ABS = 5
TOL_TRADES_PCT = 0.005
TOL_MAX_RETURN_ABS = 0.50
TOL_MDD_ABS = 0.25
MAX_PARENT_TRADE_RATIO = 1.10
MIN_PARENT_TRADE_RATIO = 0.20


@dataclass(frozen=True)
class Spec:
    name: str
    axis: str
    parent: str
    side: str
    kind: str
    tag: str

    stop_atr: float
    rr: float
    hold: int
    cooldown: int

    atrp_min: float
    atrp_max: float
    range20_max: float
    vol_min: float
    body_min: float

    # long parent fields
    ret3_floor: float
    ret5_floor: float
    ret10_floor: float
    ret20_floor: float
    close_pos_min: float
    wick_min: float
    upper_wick_max: float
    reclaim_buffer: float
    low_buffer: float
    require_green: bool
    require_reclaim: bool
    require_rare22: bool
    require_lowanchor: bool
    require_strict: bool
    require_shocklow: bool
    ema_guard: str

    # short parent fields
    dev_short: float
    rsi_short_min: float
    close_pos_short_max: float
    wick_short_min: float
    ret3_ceil: float
    ret5_ceil: float
    ret10_ceil: float
    ret20_ceil: float
    require_upper_sweep: bool
    require_ema_reject: bool

    # post-entry controls
    be_r: float
    trail_r: float
    trail_atr: float
    fail_bars: int
    fail_pnl: float

    # post-loss / symbol-DD / shock controls
    post_loss_after: int
    post_loss_bars: int
    sym_dd_pct: float
    sym_dd_bars: int
    shock_lb: int
    shock_ret5: float
    shock_range: float
    shock_close_pos: float

    # mandatory TP expectation gate
    min_expected_tp: float = MIN_EXPECTED_TP


def official_cd(max_return_pct: float, mdd: float) -> float:
    if mdd >= 100.0:
        return 0.0
    return 100.0 * (1.0 - abs(mdd) / 100.0) * (1.0 + max_return_pct / 100.0)


def equity_stats(pnls: Iterable[float]) -> Tuple[float, float, float, float]:
    eq = peak = max_eq = 1.0
    mdd = 0.0
    for p in pnls:
        eq *= max(0.0, 1.0 + POS_FRAC * float(p) / 100.0)
        peak = max(peak, eq)
        max_eq = max(max_eq, eq)
        if peak > 0:
            mdd = max(mdd, abs(eq / peak - 1.0) * 100.0)
        if eq <= 1e-12:
            return -100.0, max(0.0, (max_eq - 1.0) * 100.0), 100.0, 0.0
    final_ret = (eq - 1.0) * 100.0
    max_ret = (max_eq - 1.0) * 100.0
    return final_ret, max_ret, mdd, official_cd(max_ret, mdd)


def norm(s: str) -> str:
    return str(s).upper().replace("/", "").replace("_", "").replace("-", "").replace(" ", "")


def infer_symbol(path: Path) -> str:
    s = path.stem.upper().replace("_5M", "").replace("-5M", "").replace("PERP", "")
    if s.endswith("USDT"):
        return s[:-4] + "/USDT"
    if s.endswith("USD"):
        return s[:-3] + "/USD"
    return s


def repo_root() -> Path:
    here = Path.cwd().resolve()
    candidates = [here] + list(here.parents) + [Path(__file__).resolve().parent] + list(Path(__file__).resolve().parent.parents)
    seen = set()
    for p in candidates:
        sp = str(p)
        if sp in seen:
            continue
        seen.add(sp)
        if (p / "symbol_cost").exists() or (p / "코인" / "Data" / "time").exists() or (p / "Data" / "time").exists():
            return p
    return here


def data_root(root: Path, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    for p in [root / "코인" / "Data" / "time", root / "Data" / "time", root / "time"]:
        if p.exists():
            return p.resolve()
    return (root / "코인" / "Data" / "time").resolve()


def file_map(root: Path) -> Dict[str, Path]:
    if not root.exists():
        raise FileNotFoundError(f"data root not found: {root}")
    mp: Dict[str, Path] = {}
    for p in root.rglob("*.csv"):
        mp.setdefault(norm(p.stem), p)
        mp.setdefault(norm(infer_symbol(p)), p)
    if not mp:
        raise FileNotFoundError(f"csv not found under: {root}")
    return mp


def load_symbols(symbol_cost: Path, mp: Dict[str, Path]) -> List[str]:
    symbols: List[str] = []
    if symbol_cost.is_file():
        if symbol_cost.suffix.lower() == ".json":
            obj = json.loads(symbol_cost.read_text(encoding="utf-8"))
            if isinstance(obj, dict):
                symbols = [str(k) for k in obj.keys()]
            elif isinstance(obj, list):
                symbols = [str(x.get("symbol", x)) if isinstance(x, dict) else str(x) for x in obj]
        else:
            try:
                df = pd.read_csv(symbol_cost, low_memory=False)
                col = "symbol" if "symbol" in df.columns else df.columns[0]
                symbols = df[col].dropna().astype(str).tolist()
            except Exception:
                symbols = [x.strip() for x in symbol_cost.read_text(encoding="utf-8", errors="ignore").splitlines() if x.strip()]
    out = []
    for s in symbols:
        if norm(s) in mp:
            out.append(infer_symbol(mp[norm(s)]))
    return sorted(set(out)) if out else sorted({infer_symbol(p) for p in mp.values()})


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    ren = {}
    for c in df.columns:
        lc = str(c).strip().lower()
        if lc in {"time", "timestamp", "date", "datetime", "open_time", "ts"}:
            ren[c] = "timestamp"
        elif lc in {"open", "o"}:
            ren[c] = "open"
        elif lc in {"high", "h"}:
            ren[c] = "high"
        elif lc in {"low", "l"}:
            ren[c] = "low"
        elif lc in {"close", "c"}:
            ren[c] = "close"
        elif lc in {"volume", "vol", "v", "quote_volume"}:
            ren[c] = "volume"
    df = df.rename(columns=ren)
    need = ["open", "high", "low", "close", "volume"]
    miss = [c for c in need if c not in df.columns]
    if miss:
        raise ValueError(f"missing columns: {miss}")
    if "timestamp" not in df.columns:
        df["timestamp"] = np.arange(len(df), dtype=np.int64)
    for c in need:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce").ffill().fillna(0).astype("int64")
    return df[["timestamp"] + need].replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)


def rsi_np(close: pd.Series, n: int = 14) -> np.ndarray:
    delta = close.diff().fillna(0.0)
    gain = delta.clip(lower=0).ewm(alpha=1.0 / n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1.0 / n, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100.0 - 100.0 / (1.0 + rs)).fillna(50.0).to_numpy(dtype=np.float32)


def load_features(path: Path, max_bars: Optional[int]) -> Dict[str, np.ndarray]:
    df = standardize(pd.read_csv(path, low_memory=False))
    if max_bars and len(df) > max_bars:
        df = df.tail(max_bars).reset_index(drop=True)
    if len(df) < MIN_BARS:
        raise ValueError(f"not enough bars: {len(df)}")
    o, h, l, c, v = [df[x].astype("float64") for x in ["open", "high", "low", "close", "volume"]]
    pc = c.shift(1)
    tr = pd.concat([(h - l).abs(), (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / 14, adjust=False).mean().bfill().fillna(0)
    ema20 = c.ewm(span=20, adjust=False).mean()
    ema50 = c.ewm(span=50, adjust=False).mean()
    ema100 = c.ewm(span=100, adjust=False).mean()
    hh20 = h.rolling(20, min_periods=1).max()
    ll20 = l.rolling(20, min_periods=1).min()
    hh22 = h.rolling(22, min_periods=1).max()
    ll22 = l.rolling(22, min_periods=1).min()
    hh50 = h.rolling(50, min_periods=1).max()
    ll50 = l.rolling(50, min_periods=1).min()
    rng = (h - l).replace(0, np.nan)
    body = (c - o).abs()
    lw = (np.minimum(o, c) - l).clip(lower=0)
    uw = (h - np.maximum(o, c)).clip(lower=0)
    return {
        "ts": df["timestamp"].to_numpy(np.int64),
        "o": o.to_numpy(np.float32),
        "h": h.to_numpy(np.float32),
        "l": l.to_numpy(np.float32),
        "c": c.to_numpy(np.float32),
        "atr": atr.to_numpy(np.float32),
        "atrp": (atr / c.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "ema20": ema20.to_numpy(np.float32),
        "ema50": ema50.to_numpy(np.float32),
        "ema100": ema100.to_numpy(np.float32),
        "hh20": hh20.to_numpy(np.float32),
        "ll20": ll20.to_numpy(np.float32),
        "hh22": hh22.to_numpy(np.float32),
        "ll22": ll22.to_numpy(np.float32),
        "hh50": hh50.to_numpy(np.float32),
        "ll50": ll50.to_numpy(np.float32),
        "range20p": ((hh20 - ll20) / c.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "range50p": ((hh50 - ll50) / c.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "volr": (v / v.rolling(20, min_periods=1).mean().replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "body_atr": (body / atr.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "close_pos": ((c - l) / rng).fillna(0.5).to_numpy(np.float32),
        "lw_body": (lw / body.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "uw_body": (uw / body.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "uw_rng": (uw / rng).fillna(0).to_numpy(np.float32),
        "ret1": c.pct_change(1).fillna(0).to_numpy(np.float32),
        "ret3": c.pct_change(3).fillna(0).to_numpy(np.float32),
        "ret5": c.pct_change(5).fillna(0).to_numpy(np.float32),
        "ret10": c.pct_change(10).fillna(0).to_numpy(np.float32),
        "ret20": c.pct_change(20).fillna(0).to_numpy(np.float32),
        "rsi": rsi_np(c),
    }


def base_spec(axis: str, name: Optional[str] = None, tag: str = "baseline") -> Spec:
    b = BASELINES[axis]
    if axis == "long_main":
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="long", kind="baseline", tag=tag,
            stop_atr=1.04, rr=1.85, hold=18, cooldown=10,
            atrp_min=0.0030, atrp_max=0.070, range20_max=0.180, vol_min=1.35, body_min=0.34,
            ret3_floor=-0.036, ret5_floor=-0.052, ret10_floor=-0.070, ret20_floor=-0.110,
            close_pos_min=0.72, wick_min=0.15, upper_wick_max=0.82, reclaim_buffer=0.0000, low_buffer=0.0000,
            require_green=True, require_reclaim=True, require_rare22=False, require_lowanchor=False, require_strict=False, require_shocklow=True, ema_guard="soft",
            dev_short=0, rsi_short_min=0, close_pos_short_max=0, wick_short_min=0, ret3_ceil=0, ret5_ceil=0, ret10_ceil=0, ret20_ceil=0, require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=1.80, fail_bars=6, fail_pnl=-0.35,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=-0.070, shock_range=0.100, shock_close_pos=0.22,
        )
    if axis == "long_max":
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="long", kind="baseline", tag=tag,
            stop_atr=1.10, rr=2.05, hold=22, cooldown=6,
            atrp_min=0.0035, atrp_max=0.095, range20_max=0.240, vol_min=1.35, body_min=0.32,
            ret3_floor=-0.038, ret5_floor=-0.055, ret10_floor=-0.075, ret20_floor=-0.115,
            close_pos_min=0.70, wick_min=0.00, upper_wick_max=0.92, reclaim_buffer=0.0000, low_buffer=0.0000,
            require_green=True, require_reclaim=True, require_rare22=True, require_lowanchor=False, require_strict=False, require_shocklow=False, ema_guard="none",
            dev_short=0, rsi_short_min=0, close_pos_short_max=0, wick_short_min=0, ret3_ceil=0, ret5_ceil=0, ret10_ceil=0, ret20_ceil=0, require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=1.80, fail_bars=999, fail_pnl=-999.0,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=-0.095, shock_range=0.125, shock_close_pos=0.18,
        )
    if axis == "short_main":
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="short", kind="baseline", tag=tag,
            stop_atr=1.8975, rr=6.00, hold=200, cooldown=0,
            atrp_min=0.0018, atrp_max=0.110, range20_max=0.500, vol_min=0.0, body_min=0.0,
            ret3_floor=0, ret5_floor=0, ret10_floor=0, ret20_floor=0, close_pos_min=0, wick_min=0, upper_wick_max=0, reclaim_buffer=0, low_buffer=0,
            require_green=False, require_reclaim=False, require_rare22=False, require_lowanchor=False, require_strict=False, require_shocklow=False, ema_guard="none",
            dev_short=0.033, rsi_short_min=77.0, close_pos_short_max=1.00, wick_short_min=1.30,
            ret3_ceil=0.250, ret5_ceil=0.360, ret10_ceil=0.520, ret20_ceil=0.760,
            require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=2.10, fail_bars=10, fail_pnl=-999.0,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=0.115, shock_range=0.165, shock_close_pos=0.92,
        )
    if axis == "short_max":
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="short", kind="baseline", tag=tag,
            stop_atr=1.8975, rr=6.00, hold=200, cooldown=0,
            atrp_min=0.0018, atrp_max=0.110, range20_max=0.500, vol_min=0.0, body_min=0.0,
            ret3_floor=0, ret5_floor=0, ret10_floor=0, ret20_floor=0, close_pos_min=0, wick_min=0, upper_wick_max=0, reclaim_buffer=0, low_buffer=0,
            require_green=False, require_reclaim=False, require_rare22=False, require_lowanchor=False, require_strict=False, require_shocklow=False, ema_guard="none",
            dev_short=0.032, rsi_short_min=76.0, close_pos_short_max=1.00, wick_short_min=1.30,
            ret3_ceil=0.250, ret5_ceil=0.360, ret10_ceil=0.520, ret20_ceil=0.760,
            require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=2.40, fail_bars=10, fail_pnl=-999.0,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=0.140, shock_range=0.190, shock_close_pos=0.95,
        )
    raise ValueError(axis)


def replace_spec(s: Spec, **kw) -> Spec:
    d = asdict(s)
    d.update(kw)
    return Spec(**d)


def variants_for_axis(axis: str) -> List[Spec]:
    base = base_spec(axis)
    out: List[Spec] = []
    for j in range(50):
        n = j + 1
        if axis == "long_main":
            if j < 10:
                # 6V2의 낮은 MDD는 유지하고 TP 폭과 홀드만 완만히 확장
                k = j
                out.append(replace_spec(
                    base, name=f"8V21_long_main_{n:03d}_tp03_rr_lift", kind="improve", tag="tp03_rr_lift",
                    rr=1.88 + 0.035 * (k % 10), hold=18 + 2 * (k % 4), cooldown=10 + (k % 3),
                    close_pos_min=0.72 + 0.005 * (k % 3), min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 20:
                # 거래 수를 과도하게 죽이지 않는 품질 필터
                k = j - 10
                out.append(replace_spec(
                    base, name=f"8V21_long_main_{n:03d}_tp03_quality_expand", kind="improve", tag="tp03_quality_expand",
                    vol_min=1.28 + 0.04 * (k % 5), body_min=0.30 + 0.025 * (k % 4),
                    wick_min=0.10 + 0.035 * (k % 5), upper_wick_max=0.76 + 0.03 * (k % 4),
                    rr=1.92 + 0.03 * (k % 3), min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 30:
                # 손실 후 과매매 구간 정지
                k = j - 20
                out.append(replace_spec(
                    base, name=f"8V21_long_main_{n:03d}_tp03_postloss_pause", kind="improve", tag="tp03_postloss_pause",
                    post_loss_after=2 + (k % 3), post_loss_bars=8 + 4 * (k % 6),
                    cooldown=10 + 2 * (k % 4), fail_bars=5 + (k % 4), fail_pnl=-0.28 - 0.03 * (k % 3),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 40:
                # 쇼크성 하락 직후의 나쁜 반등 제거
                k = j - 30
                out.append(replace_spec(
                    base, name=f"8V21_long_main_{n:03d}_tp03_shock_filter", kind="improve", tag="tp03_shock_filter",
                    shock_lb=5 + (k % 4), shock_ret5=-0.058 - 0.004 * (k % 5),
                    shock_range=0.085 + 0.006 * (k % 4), shock_close_pos=0.20 + 0.025 * (k % 4),
                    rr=1.86 + 0.04 * (k % 4), min_expected_tp=MIN_EXPECTED_TP,
                ))
            else:
                # 공식 cd_value용 복합형
                k = j - 40
                out.append(replace_spec(
                    base, name=f"8V21_long_main_{n:03d}_tp03_cd_mix", kind="improve", tag="tp03_cd_mix",
                    rr=1.90 + 0.04 * (k % 5), hold=18 + 2 * (k % 5),
                    close_pos_min=0.72 + 0.01 * (k % 4), wick_min=0.12 + 0.03 * (k % 4),
                    post_loss_after=3, post_loss_bars=10 + 3 * (k % 5), min_expected_tp=MIN_EXPECTED_TP,
                ))
        elif axis == "long_max":
            if j < 10:
                # V51 raw edge 보존 + 심볼 단위 DD 브레이크
                k = j
                out.append(replace_spec(
                    base, name=f"8V21_long_max_{n:03d}_tp03_mdd_clip", kind="improve", tag="tp03_mdd_clip",
                    sym_dd_pct=1.8 + 0.25 * (k % 5), sym_dd_bars=8 + 4 * (k % 4),
                    cooldown=6 + 2 * (k % 3), min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 20:
                # rare22 훼손을 최소화한 진입 품질 조정
                k = j - 10
                out.append(replace_spec(
                    base, name=f"8V21_long_max_{n:03d}_tp03_rare22_quality", kind="improve", tag="tp03_rare22_quality",
                    close_pos_min=0.70 + 0.012 * (k % 5), upper_wick_max=0.88 - 0.015 * (k % 4),
                    body_min=0.30 + 0.025 * (k % 4), require_lowanchor=(k % 3 == 0),
                    require_strict=(k % 4 == 0), min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 30:
                # V51의 MDD를 줄이기 위한 exit 압축
                k = j - 20
                out.append(replace_spec(
                    base, name=f"8V21_long_max_{n:03d}_tp03_exit_compress", kind="improve", tag="tp03_exit_compress",
                    rr=1.84 + 0.05 * (k % 6), hold=14 + 2 * (k % 6),
                    fail_bars=5 + (k % 5), fail_pnl=-0.35 - 0.04 * (k % 4),
                    trail_r=0.95 + 0.10 * (k % 4), trail_atr=1.25 + 0.10 * (k % 4),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 40:
                # 손실 군집 회피
                k = j - 30
                out.append(replace_spec(
                    base, name=f"8V21_long_max_{n:03d}_tp03_density_cool", kind="improve", tag="tp03_density_cool",
                    cooldown=8 + 3 * (k % 6), post_loss_after=2 + (k % 3), post_loss_bars=8 + 4 * (k % 6),
                    sym_dd_pct=2.2 + 0.20 * (k % 4), sym_dd_bars=8 + 3 * (k % 4),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            else:
                # 공식 cd_value 복합형: raw upside와 MDD<5 사이 절충
                k = j - 40
                out.append(replace_spec(
                    base, name=f"8V21_long_max_{n:03d}_tp03_official_mix", kind="improve", tag="tp03_official_mix",
                    rr=1.86 + 0.05 * (k % 5), hold=16 + 2 * (k % 5),
                    close_pos_min=0.70 + 0.01 * (k % 4), require_lowanchor=(k % 2 == 0),
                    post_loss_after=3, post_loss_bars=10 + 4 * (k % 4),
                    sym_dd_pct=2.0 + 0.25 * (k % 4), sym_dd_bars=8 + 4 * (k % 3),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
        elif axis == "short_main":
            if j < 10:
                # 이미 MDD<5인 기준선의 DD 브레이크 미세 조정
                k = j
                out.append(replace_spec(
                    base, name=f"8V21_short_main_{n:03d}_tp03_dd_brake", kind="improve", tag="tp03_dd_brake",
                    sym_dd_pct=2.3 + 0.25 * (k % 5), sym_dd_bars=8 + 3 * (k % 4),
                    cooldown=k % 4, min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 20:
                # 고점 과열 품질 강화
                k = j - 10
                out.append(replace_spec(
                    base, name=f"8V21_short_main_{n:03d}_tp03_score_edge", kind="improve", tag="tp03_score_edge",
                    dev_short=0.033 + 0.0015 * (k % 6), rsi_short_min=77.0 + 0.75 * (k % 6),
                    wick_short_min=1.20 + 0.05 * (k % 5), require_upper_sweep=(k % 3 == 0),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 30:
                # 연속 손실 일시정지
                k = j - 20
                out.append(replace_spec(
                    base, name=f"8V21_short_main_{n:03d}_tp03_loss_pause", kind="improve", tag="tp03_loss_pause",
                    post_loss_after=2 + (k % 4), post_loss_bars=8 + 4 * (k % 6),
                    cooldown=k % 5, min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 40:
                # 너무 긴 200바 홀드로 생기는 꼬리위험 압축
                k = j - 30
                out.append(replace_spec(
                    base, name=f"8V21_short_main_{n:03d}_tp03_exit_compact", kind="improve", tag="tp03_exit_compact",
                    rr=5.15 + 0.15 * (k % 6), hold=128 + 8 * (k % 8),
                    trail_r=1.15 + 0.12 * (k % 5), trail_atr=1.55 + 0.12 * (k % 5),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            else:
                # short_main 공식 방어 복합형
                k = j - 40
                out.append(replace_spec(
                    base, name=f"8V21_short_main_{n:03d}_tp03_hybrid_guard", kind="improve", tag="tp03_hybrid_guard",
                    dev_short=0.034 + 0.0015 * (k % 4), rsi_short_min=77.0 + 0.8 * (k % 5),
                    rr=5.30 + 0.15 * (k % 5), hold=140 + 8 * (k % 6),
                    sym_dd_pct=2.4 + 0.25 * (k % 4), post_loss_after=3, post_loss_bars=10 + 4 * (k % 5),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
        elif axis == "short_max":
            if j < 10:
                # short_max의 핵심 raw upside 보존 + 심볼 DD 제한
                k = j
                out.append(replace_spec(
                    base, name=f"8V21_short_max_{n:03d}_tp03_mdd_clip", kind="improve", tag="tp03_mdd_clip",
                    sym_dd_pct=2.4 + 0.30 * (k % 6), sym_dd_bars=8 + 4 * (k % 4),
                    cooldown=k % 4, min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 20:
                # 고점 과열 신뢰도 강화
                k = j - 10
                out.append(replace_spec(
                    base, name=f"8V21_short_max_{n:03d}_tp03_quality_peak", kind="improve", tag="tp03_quality_peak",
                    dev_short=0.032 + 0.0015 * (k % 7), rsi_short_min=76.0 + 0.8 * (k % 7),
                    wick_short_min=1.20 + 0.05 * (k % 6), require_upper_sweep=(k % 2 == 0),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 30:
                # 긴 홀드의 꼬리위험 압축
                k = j - 20
                out.append(replace_spec(
                    base, name=f"8V21_short_max_{n:03d}_tp03_exit_compress", kind="improve", tag="tp03_exit_compress",
                    rr=5.10 + 0.18 * (k % 6), hold=120 + 10 * (k % 8),
                    trail_r=1.10 + 0.12 * (k % 5), trail_atr=1.50 + 0.14 * (k % 5),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            elif j < 40:
                # 손실 군집 및 급등장 회피
                k = j - 30
                out.append(replace_spec(
                    base, name=f"8V21_short_max_{n:03d}_tp03_squeeze_guard", kind="improve", tag="tp03_squeeze_guard",
                    post_loss_after=2 + (k % 4), post_loss_bars=8 + 5 * (k % 5),
                    shock_lb=5 + (k % 4), shock_ret5=0.095 + 0.010 * (k % 5),
                    shock_range=0.145 + 0.012 * (k % 4), shock_close_pos=0.86 + 0.02 * (k % 4),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
            else:
                # 공식 cd_value 복합형
                k = j - 40
                out.append(replace_spec(
                    base, name=f"8V21_short_max_{n:03d}_tp03_official_mix", kind="improve", tag="tp03_official_mix",
                    dev_short=0.033 + 0.0015 * (k % 5), rsi_short_min=76.5 + 0.75 * (k % 5),
                    rr=5.20 + 0.18 * (k % 5), hold=130 + 10 * (k % 6),
                    sym_dd_pct=2.5 + 0.25 * (k % 5), sym_dd_bars=8 + 4 * (k % 4),
                    post_loss_after=3, post_loss_bars=10 + 4 * (k % 5),
                    min_expected_tp=MIN_EXPECTED_TP,
                ))
        else:
            raise ValueError(axis)
    if len(out) != 50:
        raise AssertionError(f"{axis} variants count mismatch: {len(out)}")
    return out


def baseline_specs() -> List[Spec]:
    return [base_spec(axis) for axis in ["long_main", "long_max", "short_main", "short_max"]]


def improvement_specs() -> List[Spec]:
    specs: List[Spec] = []
    for axis in ["long_main", "long_max", "short_main", "short_max"]:
        specs.extend(variants_for_axis(axis))
    if len(specs) != 200:
        raise AssertionError(f"improvement count mismatch: {len(specs)}")
    return specs


def all_specs() -> List[Spec]:
    return baseline_specs() + improvement_specs()


def _common_filters(f: Dict[str, np.ndarray], i: int, s: Spec) -> bool:
    atrp = float(f["atrp"][i])
    if not (s.atrp_min <= atrp <= s.atrp_max):
        return False
    if float(f["range20p"][i]) > s.range20_max:
        return False
    if float(f["volr"][i]) < s.vol_min:
        return False
    if float(f["body_atr"][i]) < s.body_min:
        return False
    expected_tp = s.stop_atr * s.rr * atrp
    if expected_tp < s.min_expected_tp:
        return False
    return True


def _long_signal(f: Dict[str, np.ndarray], i: int, s: Spec) -> bool:
    if not _common_filters(f, i, s):
        return False
    o, h, l, c = f["o"], f["h"], f["l"], f["c"]
    if s.require_green and not (c[i] > o[i]):
        return False
    if float(f["ret3"][i]) < s.ret3_floor or float(f["ret5"][i]) < s.ret5_floor:
        return False
    if float(f["ret10"][i]) < s.ret10_floor or float(f["ret20"][i]) < s.ret20_floor:
        return False
    if float(f["close_pos"][i]) < s.close_pos_min:
        return False
    if float(f["lw_body"][i]) < s.wick_min:
        return False
    if float(f["uw_body"][i]) > s.upper_wick_max:
        return False
    if s.require_reclaim:
        reclaim_level = float(f["ll20"][i]) * (1.0 + s.reclaim_buffer)
        if not (c[i] >= reclaim_level):
            return False
    if s.require_rare22:
        if not (l[i] <= float(f["ll22"][i]) * (1.0 + max(s.low_buffer, 0.0005))):
            return False
    if s.require_lowanchor:
        if not (l[i] <= float(f["ll50"][i]) * 1.012):
            return False
    if s.require_strict:
        if not (float(f["close_pos"][i]) >= max(s.close_pos_min, 0.74) and float(f["body_atr"][i]) >= max(s.body_min, 0.34)):
            return False
    if s.require_shocklow:
        flush = (l[i] <= float(f["ll20"][i]) * 1.006) or (float(f["ret5"][i]) <= -0.018)
        if not flush:
            return False
    if s.ema_guard == "soft":
        if not (c[i] >= float(f["ema20"][i]) * 0.965 or c[i] >= float(f["ema50"][i]) * 0.940):
            return False
    elif s.ema_guard == "hard":
        if not (c[i] >= float(f["ema20"][i]) * 0.985):
            return False
    if s.shock_lb > 0:
        shock = (float(f["ret5"][i]) <= s.shock_ret5 and float(f["range20p"][i]) >= s.shock_range and float(f["close_pos"][i]) <= s.shock_close_pos)
        if shock:
            return False
    return True


def _short_signal(f: Dict[str, np.ndarray], i: int, s: Spec) -> bool:
    if not _common_filters(f, i, s):
        return False
    h, c = f["h"], f["c"]
    ema50 = max(float(f["ema50"][i]), 1e-12)
    dev = float(h[i] / ema50 - 1.0)
    if dev < s.dev_short:
        return False
    if float(f["rsi"][i]) < s.rsi_short_min:
        return False
    if float(f["close_pos"][i]) > s.close_pos_short_max:
        return False
    if float(f["uw_body"][i]) < s.wick_short_min:
        return False
    if float(f["ret3"][i]) > s.ret3_ceil or float(f["ret5"][i]) > s.ret5_ceil:
        return False
    if float(f["ret10"][i]) > s.ret10_ceil or float(f["ret20"][i]) > s.ret20_ceil:
        return False
    if s.require_upper_sweep:
        if not (h[i] >= float(f["hh20"][i]) * 0.997):
            return False
    if s.require_ema_reject:
        if not (c[i] <= float(f["ema20"][i]) * 1.020):
            return False
    if s.shock_lb > 0:
        shock = (float(f["ret5"][i]) >= s.shock_ret5 and float(f["range20p"][i]) >= s.shock_range and float(f["close_pos"][i]) >= s.shock_close_pos)
        if shock:
            return False
    return True


def _exit_trade(f: Dict[str, np.ndarray], i: int, s: Spec) -> Tuple[int, float]:
    o, h, l, c, atr = f["o"], f["h"], f["l"], f["c"], f["atr"]
    n = len(c)
    entry = float(c[i])
    a = max(float(atr[i]), entry * 1e-6)
    risk = s.stop_atr * a
    max_j = min(n - 1, i + max(1, int(s.hold)))
    exit_j = max_j
    exit_price = float(c[max_j])
    best_r = 0.0
    stop = entry - risk if s.side == "long" else entry + risk
    tp = entry + s.rr * risk if s.side == "long" else entry - s.rr * risk
    be_active = False
    trail_active = False

    for j in range(i + 1, max_j + 1):
        if s.side == "long":
            runup_r = (float(h[j]) - entry) / risk
            best_r = max(best_r, runup_r)
            if s.be_r < 900 and best_r >= s.be_r:
                be_active = True
            if s.trail_r < 900 and best_r >= s.trail_r:
                trail_active = True
            dyn_stop = stop
            if be_active:
                dyn_stop = max(dyn_stop, entry)
            if trail_active:
                dyn_stop = max(dyn_stop, float(h[j]) - s.trail_atr * a)
            if float(l[j]) <= dyn_stop:
                exit_j, exit_price = j, dyn_stop
                break
            if float(h[j]) >= tp:
                exit_j, exit_price = j, tp
                break
            if s.fail_bars < 900 and (j - i) >= s.fail_bars:
                now_pnl = (float(c[j]) / entry - 1.0) * 100.0 - COST_PCT
                if now_pnl <= s.fail_pnl:
                    exit_j, exit_price = j, float(c[j])
                    break
        else:
            runup_r = (entry - float(l[j])) / risk
            best_r = max(best_r, runup_r)
            if s.be_r < 900 and best_r >= s.be_r:
                be_active = True
            if s.trail_r < 900 and best_r >= s.trail_r:
                trail_active = True
            dyn_stop = stop
            if be_active:
                dyn_stop = min(dyn_stop, entry)
            if trail_active:
                dyn_stop = min(dyn_stop, float(l[j]) + s.trail_atr * a)
            if float(h[j]) >= dyn_stop:
                exit_j, exit_price = j, dyn_stop
                break
            if float(l[j]) <= tp:
                exit_j, exit_price = j, tp
                break
            if s.fail_bars < 900 and (j - i) >= s.fail_bars:
                now_pnl = (entry / max(float(c[j]), 1e-12) - 1.0) * 100.0 - COST_PCT
                if now_pnl <= s.fail_pnl:
                    exit_j, exit_price = j, float(c[j])
                    break

    if s.side == "long":
        pnl = (exit_price / entry - 1.0) * 100.0 - COST_PCT
    else:
        pnl = (entry / max(exit_price, 1e-12) - 1.0) * 100.0 - COST_PCT
    return exit_j, pnl


def simulate_symbol(path: Path, symbol: str, specs: List[Spec], max_bars: Optional[int]) -> Tuple[str, Dict[int, np.ndarray], Optional[str]]:
    try:
        f = load_features(path, max_bars)
        n = len(f["c"])
        per_spec: Dict[int, List[Tuple[int, float]]] = {k: [] for k in range(len(specs))}
        for k, s in enumerate(specs):
            i = WARMUP
            next_allowed = WARMUP
            loss_streak = 0
            pause_until = -1
            sym_eq = sym_peak = 1.0
            dd_pause_until = -1
            while i < n - 2:
                if i < next_allowed or i < pause_until or i < dd_pause_until:
                    i += 1
                    continue
                ok = _long_signal(f, i, s) if s.side == "long" else _short_signal(f, i, s)
                if not ok:
                    i += 1
                    continue
                exit_i, pnl = _exit_trade(f, i, s)
                per_spec[k].append((int(f["ts"][exit_i]), float(pnl)))

                sym_eq *= max(0.0, 1.0 + POS_FRAC * pnl / 100.0)
                sym_peak = max(sym_peak, sym_eq)
                sym_dd = abs(sym_eq / sym_peak - 1.0) * 100.0 if sym_peak > 0 else 100.0

                if pnl < 0:
                    loss_streak += 1
                else:
                    loss_streak = 0

                if s.post_loss_after < 900 and loss_streak >= s.post_loss_after:
                    pause_until = exit_i + max(1, s.post_loss_bars)
                    loss_streak = 0

                if s.sym_dd_pct < 900 and sym_dd >= s.sym_dd_pct:
                    dd_pause_until = exit_i + max(1, s.sym_dd_bars)
                    sym_eq = sym_peak = 1.0

                next_allowed = exit_i + max(0, s.cooldown)
                i = max(exit_i + 1, i + 1)

        out: Dict[int, np.ndarray] = {}
        for k, rows in per_spec.items():
            if rows:
                arr = np.array(rows, dtype=REC_DTYPE)
            else:
                arr = np.empty(0, dtype=REC_DTYPE)
            out[k] = arr
        return symbol, out, None
    except Exception as e:
        return symbol, {}, repr(e) + "\n" + traceback.format_exc()


def aggregate_results(specs: List[Spec], spec_records: Dict[int, List[np.ndarray]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for i, spec in enumerate(specs):
        chunks = [x for x in spec_records.get(i, []) if x is not None and len(x) > 0]
        if chunks:
            arr = np.concatenate(chunks)
            arr.sort(order="ts")
            pnls = arr["pnl"].astype(np.float64)
        else:
            arr = np.empty(0, dtype=REC_DTYPE)
            pnls = np.array([], dtype=np.float64)
        final_ret, max_ret, mdd, cd = equity_stats(pnls)
        wins = int(np.sum(pnls > 0)) if len(pnls) else 0
        trades = int(len(pnls))
        row = {
            "name": spec.name,
            "axis": spec.axis,
            "parent": spec.parent,
            "side": spec.side,
            "kind": spec.kind,
            "tag": spec.tag,
            "trades": trades,
            "wins": wins,
            "win_rate": (wins / trades) if trades else 0.0,
            "avg_pnl": float(np.mean(pnls)) if trades else 0.0,
            "median_pnl": float(np.median(pnls)) if trades else 0.0,
            "final_return_pct": final_ret,
            "max_return_pct": max_ret,
            "max_drawdown_pct": mdd,
            "official_cd_value": cd,
            "min_expected_tp": spec.min_expected_tp,
            "stop_atr": spec.stop_atr,
            "rr": spec.rr,
            "hold": spec.hold,
            "cooldown": spec.cooldown,
            "atrp_min": spec.atrp_min,
            "atrp_max": spec.atrp_max,
            "range20_max": spec.range20_max,
            "vol_min": spec.vol_min,
            "body_min": spec.body_min,
            "close_pos_min": spec.close_pos_min,
            "wick_min": spec.wick_min,
            "dev_short": spec.dev_short,
            "rsi_short_min": spec.rsi_short_min,
            "sym_dd_pct": spec.sym_dd_pct,
            "sym_dd_bars": spec.sym_dd_bars,
            "post_loss_after": spec.post_loss_after,
            "post_loss_bars": spec.post_loss_bars,
            "be_r": spec.be_r,
            "trail_r": spec.trail_r,
            "trail_atr": spec.trail_atr,
            "fail_bars": spec.fail_bars,
            "fail_pnl": spec.fail_pnl,
        }
        rows.append(row)
    rows.sort(key=lambda r: (float(r["official_cd_value"]), -float(r["max_drawdown_pct"]), int(r["trades"])), reverse=True)
    return rows


def check_baseline_gate(baseline_rows: List[Dict[str, object]], mode: str) -> Tuple[bool, List[str]]:
    messages: List[str] = []
    row_by_axis = {str(r["axis"]): r for r in baseline_rows}
    ok_all = True
    for axis, ref in BASELINES.items():
        r = row_by_axis.get(axis)
        if not r:
            ok_all = False
            messages.append(f"[GATE_FAIL] {axis}: missing result")
            continue
        trades = int(r["trades"])
        max_ret = float(r["max_return_pct"])
        mdd = float(r["max_drawdown_pct"])
        trade_tol = max(TOL_TRADES_ABS, int(ref["trades"] * TOL_TRADES_PCT))
        axis_ok = True
        if abs(trades - int(ref["trades"])) > trade_tol:
            axis_ok = False
        if abs(max_ret - float(ref["max_return_pct"])) > TOL_MAX_RETURN_ABS:
            axis_ok = False
        if abs(mdd - float(ref["max_drawdown_pct"])) > TOL_MDD_ABS:
            axis_ok = False
        status = "PASS" if axis_ok else "FAIL"
        if not axis_ok:
            ok_all = False
        messages.append(
            f"[GATE_{status}] {axis} {ref['name']} | "
            f"trades {trades} vs {ref['trades']} | "
            f"max_ret {max_ret:.6f} vs {ref['max_return_pct']:.6f} | "
            f"mdd {mdd:.6f} vs {ref['max_drawdown_pct']:.6f}"
        )
    if mode == "off":
        return True, messages
    return ok_all, messages


def check_parent_trade_ratio(all_rows: List[Dict[str, object]]) -> List[str]:
    messages: List[str] = []
    parent_trades: Dict[str, int] = {}
    for r in all_rows:
        if r["kind"] == "baseline":
            parent_trades[str(r["axis"])] = int(r["trades"])
    for r in all_rows:
        if r["kind"] != "improve":
            continue
        axis = str(r["axis"])
        pt = parent_trades.get(axis, 0)
        if pt <= 0:
            continue
        ratio = int(r["trades"]) / pt
        if ratio > MAX_PARENT_TRADE_RATIO or ratio < MIN_PARENT_TRADE_RATIO:
            messages.append(f"[RATIO_WARN] {r['name']} axis={axis} trades={r['trades']} parent={pt} ratio={ratio:.3f}")
    return messages


def write_summary(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_trades(path: Path, specs: List[Spec], records: Dict[int, List[np.ndarray]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows_written = 0
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["strategy", "axis", "side", "kind", "tag", "ts", "pnl"])
        for i, s in enumerate(specs):
            chunks = [x for x in records.get(i, []) if x is not None and len(x) > 0]
            if not chunks:
                continue
            arr = np.concatenate(chunks)
            arr.sort(order="ts")
            for rec in arr:
                w.writerow([s.name, s.axis, s.side, s.kind, s.tag, int(rec["ts"]), float(rec["pnl"])])
                rows_written += 1
    return rows_written


def run_phase(
    phase_name: str,
    specs: List[Spec],
    symbols: List[str],
    fmap: Dict[str, Path],
    max_bars: Optional[int],
    workers: int,
    progress_every: int,
) -> Tuple[List[Dict[str, object]], Dict[int, List[np.ndarray]], List[Tuple[str, str]]]:
    spec_records: Dict[int, List[np.ndarray]] = {i: [] for i in range(len(specs))}
    errors: List[Tuple[str, str]] = []
    started = time.time()
    processed = 0
    trade_rows = 0

    def submit_items(ex):
        futs = {}
        for sym in symbols:
            key = norm(sym)
            path = fmap.get(key)
            if path is None:
                errors.append((sym, "symbol file not found"))
                continue
            fut = ex.submit(simulate_symbol, path, sym, specs, max_bars)
            futs[fut] = sym
        return futs

    if workers <= 1:
        for sym in symbols:
            key = norm(sym)
            path = fmap.get(key)
            if path is None:
                errors.append((sym, "symbol file not found"))
                continue
            _, out, err = simulate_symbol(path, sym, specs, max_bars)
            if err:
                errors.append((sym, err))
            else:
                for k, arr in out.items():
                    spec_records[k].append(arr)
                    trade_rows += len(arr)
            processed += 1
            if processed % progress_every == 0:
                print(f"[PROGRESS:{phase_name}] processed={processed}/{len(symbols)} errors={len(errors)} trade_rows={trade_rows} elapsed={time.time()-started:.1f}s", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = submit_items(ex)
            for fut in as_completed(futs):
                sym = futs[fut]
                try:
                    _, out, err = fut.result()
                except Exception as e:
                    out, err = {}, repr(e) + "\n" + traceback.format_exc()
                if err:
                    errors.append((sym, err))
                else:
                    for k, arr in out.items():
                        spec_records[k].append(arr)
                        trade_rows += len(arr)
                processed += 1
                if processed % progress_every == 0:
                    print(f"[PROGRESS:{phase_name}] processed={processed}/{len(futs)} errors={len(errors)} trade_rows={trade_rows} elapsed={time.time()-started:.1f}s", flush=True)

    rows = aggregate_results(specs, spec_records)
    return rows, spec_records, errors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="8V21 TP0.3% parent-preserve 4-axis 50-each backtest runner")
    p.add_argument("--data-root", default=None, help="OHLCV csv root. default: auto-detect")
    p.add_argument("--symbol-cost", default="symbol_cost", help="symbol list file/path. default: symbol_cost")
    p.add_argument("--outdir", default=None, help="output dir. default: backtest_results/<BATCH>")
    p.add_argument("--max-bars", type=int, default=0, help="recent bars per symbol. default: 1500")
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    p.add_argument("--progress-every", type=int, default=25)
    p.add_argument("--gate-mode", choices=["abort", "warn", "off"], default="abort", help="baseline gate handling")
    p.add_argument("--save-trades", action="store_true", help="write trades csv files")
    p.add_argument("--phase", choices=["all", "baseline", "improve"], default="all")
    p.add_argument("--sample-symbols", type=int, default=0, help="debug only: random sample symbols")
    return p.parse_args()


def main() -> None:
    random.seed(SEED)
    args = parse_args()
    root = repo_root()
    droot = data_root(root, args.data_root)
    fmap = file_map(droot)
    scost = Path(args.symbol_cost)
    if not scost.is_absolute():
        scost = root / scost
    symbols = load_symbols(scost, fmap)
    if args.sample_symbols and args.sample_symbols > 0:
        random.shuffle(symbols)
        symbols = sorted(symbols[: args.sample_symbols])

    outdir = Path(args.outdir) if args.outdir else root / "backtest_results" / BATCH
    if outdir.exists() and args.phase == "all":
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    meta = {
        "batch": BATCH,
        "seed": SEED,
        "min_expected_tp": MIN_EXPECTED_TP,
        "baseline_source": EMBEDDED_BASELINE_SOURCE,
        "baselines": BASELINES,
        "pos_frac": POS_FRAC,
        "cost_pct": COST_PCT,
        "warmup": WARMUP,
        "min_bars": MIN_BARS,
        "max_bars": args.max_bars,
        "data_root": str(droot),
        "symbol_cost": str(scost),
        "symbols": len(symbols),
        "workers": args.workers,
        "gate_mode": args.gate_mode,
        "axis_plan": {"long_main": 50, "long_max": 50, "short_main": 50, "short_max": 50},
    }
    (outdir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[START] batch={BATCH} symbols={len(symbols)} workers={args.workers} max_bars={args.max_bars}", flush=True)
    print(f"[DATA] root={droot}", flush=True)
    print(f"[RULE] mandatory expected TP gate: stop_atr * rr * atrp >= {MIN_EXPECTED_TP}", flush=True)

    all_rows: List[Dict[str, object]] = []
    all_records: Dict[int, List[np.ndarray]] = {}
    all_errors: List[Tuple[str, str]] = []

    if args.phase in {"all", "baseline"}:
        bspecs = baseline_specs()
        b_rows, b_records, b_errors = run_phase("baseline", bspecs, symbols, fmap, args.max_bars, args.workers, args.progress_every)
        write_summary(outdir / "baseline_summary.csv", b_rows)
        if args.save_trades:
            b_trade_rows = write_trades(outdir / "baseline_trades.csv", bspecs, b_records)
            print(f"[WRITE] baseline_trades={b_trade_rows}", flush=True)
        ok_gate, gate_msgs = check_baseline_gate(b_rows, args.gate_mode)
        (outdir / "baseline_gate.txt").write_text("\n".join(gate_msgs) + "\n", encoding="utf-8")
        for m in gate_msgs:
            print(m, flush=True)
        all_rows.extend(b_rows)
        all_records.update({i: v for i, v in b_records.items()})
        all_errors.extend(b_errors)
        if args.gate_mode == "abort" and not ok_gate:
            write_summary(outdir / "summary.csv", all_rows)
            if all_errors:
                (outdir / "errors.txt").write_text("\n\n".join([f"[{s}]\n{e}" for s, e in all_errors]), encoding="utf-8")
            print("[ABORT] baseline gate failed. Improvements were not executed.", flush=True)
            return

    if args.phase in {"all", "improve"}:
        ispecs = improvement_specs()
        i_rows, i_records, i_errors = run_phase("improve", ispecs, symbols, fmap, args.max_bars, args.workers, args.progress_every)
        write_summary(outdir / "improvement_summary.csv", i_rows)
        if args.save_trades:
            i_trade_rows = write_trades(outdir / "improvement_trades.csv", ispecs, i_records)
            print(f"[WRITE] improvement_trades={i_trade_rows}", flush=True)
        # shift improvement record keys after baseline if phase all
        if args.phase == "all":
            offset = 4
            for k, v in i_records.items():
                all_records[offset + k] = v
        else:
            all_records = i_records
        all_rows.extend(i_rows)
        all_errors.extend(i_errors)

    all_rows_sorted = sorted(
        all_rows,
        key=lambda r: (float(r["official_cd_value"]), -float(r["max_drawdown_pct"]), int(r["trades"])),
        reverse=True,
    )
    write_summary(outdir / "summary.csv", all_rows_sorted)

    if all_errors:
        (outdir / "errors.txt").write_text("\n\n".join([f"[{s}]\n{e}" for s, e in all_errors]), encoding="utf-8")

    ratio_msgs = check_parent_trade_ratio(all_rows)
    if ratio_msgs:
        (outdir / "parent_trade_ratio_warnings.txt").write_text("\n".join(ratio_msgs) + "\n", encoding="utf-8")
        for m in ratio_msgs[:20]:
            print(m, flush=True)
        if len(ratio_msgs) > 20:
            print(f"[RATIO_WARN] ... {len(ratio_msgs)-20} more", flush=True)

    top = all_rows_sorted[:10]
    print("[TOP10]", flush=True)
    for r in top:
        print(
            f"{r['name']} | axis={r['axis']} kind={r['kind']} trades={r['trades']} "
            f"max_ret={float(r['max_return_pct']):.6f} mdd={float(r['max_drawdown_pct']):.6f} "
            f"cd={float(r['official_cd_value']):.6f}",
            flush=True,
        )
    print(f"[DONE] outdir={outdir}", flush=True)


if __name__ == "__main__":
    main()
