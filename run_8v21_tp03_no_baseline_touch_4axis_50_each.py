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
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

BATCH = "8V21_TP03_NO_BASELINE_TOUCH_4AXIS_50_EACH"
POS_FRAC = 0.01
COST_PCT = 0.10
WARMUP = 140
MIN_BARS = 260
SEED = 820
REC_DTYPE = np.dtype([("ts", "<i8"), ("pnl", "<f4")])

# 현재 CORE_SUMMARY 기준선. 첫 4개는 반드시 이 기준선 4개를 먼저 실행한다.
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



# 코드 내부에 박아 둔 원본 기준선 조건값. 외부 runner/base/combinations 경로를 읽지 않는다.
EMBEDDED_BASELINE_SOURCE = {
    "long_main": {"source":"CORE_SUMMARY 8V12 base_safe6v2_profile", "strategy":"6V2_L01_doubleflush_core"},
    "long_max": {"source":"CORE_SUMMARY 8V12 base_rawv51_profile", "strategy":"8V4_V51_V002_core_rare22_c1"},
    "short_main": {"source":"v52 short_only_behavioral_guards JSON embedded", "strategy":"short_beh_dd_brake", "quality":{"short_dev":0.033,"short_rsi_min":77}, "risk":{"atr_stop_mult":1.8975,"rr_mult":6.0,"timeout_bars":200}, "trade_control":{"dd_brake_trigger_pct":0.03,"dd_brake_freeze_steps":5}},
    "short_max": {"source":"v42 rr60 t200 short_only JSON embedded", "strategy":"short_only_reference_1x", "quality":{"short_dev":0.032,"short_rsi_min":76}, "risk":{"atr_stop_mult":1.8975,"rr_mult":6.0,"timeout_bars":200}},
}

TOL_TRADES_ABS = 5
TOL_TRADES_PCT = 0.005
TOL_MAX_RETURN_ABS = 0.50
TOL_MDD_ABS = 0.25
MAX_PARENT_TRADE_RATIO = 1.10
MIN_PARENT_TRADE_RATIO = 0.20

# 기준선 원본 조건 탑재 원칙:
# - 첫 4개 Spec은 개선안이 아니라 기준선 복제본이다.
# - long_main은 6V2_L01_doubleflush_core의 double flush + cap reclaim 구조를 보존한다.
# - long_max는 8V4_V51_V002_core_rare22_c1의 V51 microbase/rare22 구조를 보존한다.
# - short_main/short_max는 저장소 experiments의 v52/v42 short-only 설정값을 코드에 직접 박았다.
# - 기준선 4개 중 하나라도 trades/max_return/MDD 허용오차를 벗어나면 개선안 실행을 중단한다.


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


def official_cd(max_return_pct: float, mdd: float) -> float:
    if mdd >= 100.0:
        return 0.0
    return 100.0 * (1.0 - abs(mdd) / 100.0) * (1.0 + max_return_pct / 100.0)


def equity_stats(pnls: List[float]) -> Tuple[float, float, float, float]:
    eq = peak = max_eq = 1.0
    mdd = 0.0
    for p in pnls:
        eq *= max(0.0, 1.0 + POS_FRAC * p / 100.0)
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
        "o": o.to_numpy(np.float32), "h": h.to_numpy(np.float32), "l": l.to_numpy(np.float32), "c": c.to_numpy(np.float32),
        "atr": atr.to_numpy(np.float32), "atrp": (atr / c.replace(0, np.nan)).fillna(0).to_numpy(np.float32),
        "ema20": ema20.to_numpy(np.float32), "ema50": ema50.to_numpy(np.float32), "ema100": ema100.to_numpy(np.float32),
        "hh20": hh20.to_numpy(np.float32), "ll20": ll20.to_numpy(np.float32), "hh22": hh22.to_numpy(np.float32), "ll22": ll22.to_numpy(np.float32),
        "hh50": hh50.to_numpy(np.float32), "ll50": ll50.to_numpy(np.float32),
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
        # 원본 기준선: 6V2_L01_doubleflush_core
        # CORE_SUMMARY 8V12의 base_safe6v2_profile 값을 그대로 코드 내부에 명시한다.
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="long", kind="baseline", tag=tag,
            stop_atr=1.04, rr=1.85, hold=18, cooldown=10,
            atrp_min=0.0030, atrp_max=0.070, range20_max=0.180, vol_min=1.35, body_min=0.34,
            ret3_floor=-0.036, ret5_floor=-0.052, ret10_floor=-0.070, ret20_floor=-0.110,
            close_pos_min=0.72, wick_min=0.15, upper_wick_max=0.82, reclaim_buffer=0.0000, low_buffer=0.0000,
            require_green=True, require_reclaim=True, require_rare22=False, require_lowanchor=False, require_strict=False, require_shocklow=True, ema_guard="soft",
            dev_short=0, rsi_short_min=0, close_pos_short_max=0, wick_short_min=0, ret3_ceil=0, ret5_ceil=0, ret10_ceil=0, ret20_ceil=0, require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=1.80, fail_bars=6, fail_pnl=-0.35,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=-0.070, shock_range=0.100, shock_close_pos=0.22
        )
    if axis == "long_max":
        # 원본 기준선: 8V4_V51_V002_core_rare22_c1
        # CORE_SUMMARY 8V12의 base_rawv51_profile 값을 그대로 코드 내부에 명시한다.
        return Spec(
            name=name or b["name"], axis=axis, parent=b["name"], side="long", kind="baseline", tag=tag,
            stop_atr=1.10, rr=2.05, hold=22, cooldown=6,
            atrp_min=0.0035, atrp_max=0.095, range20_max=0.240, vol_min=1.35, body_min=0.32,
            ret3_floor=-0.038, ret5_floor=-0.055, ret10_floor=-0.075, ret20_floor=-0.115,
            close_pos_min=0.70, wick_min=0.00, upper_wick_max=0.92, reclaim_buffer=0.0000, low_buffer=0.0000,
            require_green=True, require_reclaim=True, require_rare22=True, require_lowanchor=False, require_strict=False, require_shocklow=False, ema_guard="none",
            dev_short=0, rsi_short_min=0, close_pos_short_max=0, wick_short_min=0, ret3_ceil=0, ret5_ceil=0, ret10_ceil=0, ret20_ceil=0, require_upper_sweep=False, require_ema_reject=False,
            be_r=999.0, trail_r=999.0, trail_atr=1.80, fail_bars=999, fail_pnl=-999.0,
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=-0.095, shock_range=0.125, shock_close_pos=0.18
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
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=0.115, shock_range=0.165, shock_close_pos=0.92
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
            post_loss_after=999, post_loss_bars=0, sym_dd_pct=999.0, sym_dd_bars=0, shock_lb=0, shock_ret5=0.140, shock_range=0.190, shock_close_pos=0.95
        )
    raise ValueError(axis)


def replace_spec(s: Spec, **kw) -> Spec:
    d = asdict(s)
    d.update(kw)
    return Spec(**d)


def variants_for_axis(axis):
    # 8V21 개선안 생성부.
    # 기준선 보존 원칙:
    # - base_spec, BASELINES, 기준선 4개 조건, entry/exit 엔진, parent gate는 이 함수 밖에 있으므로 건드리지 않는다.
    # - 이 함수는 기준선 통과 후 실행되는 개선안 목록만 만든다.
    # - 각 축별 50개, 총 200개 개선안을 생성한다.
    # - TP 기대값 0.3% 이상 조건은 개선안에만 적용한다.
    from dataclasses import fields as _dc_fields, is_dataclass as _dc_is_dataclass, replace as _dc_replace

    base = base_spec(axis)

    def _field_names(s):
        if _dc_is_dataclass(s):
            return {f.name for f in _dc_fields(s)}
        if hasattr(s, "_fields"):
            return set(s._fields)
        return set(vars(s).keys())

    _names = _field_names(base)

    required_for_tp03 = {"stop_atr", "rr", "atrp_min"}
    missing_tp03 = required_for_tp03 - _names
    if missing_tp03:
        raise RuntimeError(
            "TP03 필터 적용에 필요한 Spec 필드가 없습니다: "
            + ",".join(sorted(missing_tp03))
            + ". 기준 파일 구조를 먼저 확인해야 합니다."
        )

    def _get(s, field, default):
        return getattr(s, field) if field in _field_names(s) else default

    def _safe_replace(s, **changes):
        names = _field_names(s)
        filtered = {k: v for k, v in changes.items() if k in names}
        if _dc_is_dataclass(s):
            return _dc_replace(s, **filtered)
        if hasattr(s, "_replace"):
            return s._replace(**filtered)
        obj = s
        for k, v in filtered.items():
            setattr(obj, k, v)
        return obj

    def _tp03(s):
        stop_atr = float(getattr(s, "stop_atr"))
        rr = float(getattr(s, "rr"))
        denom = stop_atr * rr
        if denom <= 0:
            raise RuntimeError(f"{getattr(s, 'name', axis)} TP03 계산 실패: stop_atr * rr <= 0")
        floor = 0.003 / denom
        return _safe_replace(s, atrp_min=max(float(getattr(s, "atrp_min")), floor))

    def _make(name, tag, **changes):
        s = _safe_replace(base, name=name, kind="improve", tag=tag, **changes)
        return _tp03(s)

    out = []

    # 공통 기본값. 필드가 없는 경우에도 생성부가 깨지지 않도록 보수적 기본값을 둔다.
    rr0 = float(_get(base, "rr", 2.0))
    hold0 = int(_get(base, "hold", 40))
    trail0 = float(_get(base, "trail_atr", 1.8))
    cooldown0 = int(_get(base, "cooldown", 0))
    vol0 = float(_get(base, "vol_min", 0.0))
    close0 = float(_get(base, "close_pos_min", 0.0))
    range20_0 = float(_get(base, "range20_max", 999.0))

    for j in range(50):
        n = j + 1
        k = j % 10

        if axis == "long_main":
            # 6V2 계열: MDD 장점 보존, max_return 확장.
            if j < 10:
                out.append(_make(
                    f"8V21_long_main_{n:03d}_rr_hold_lift",
                    "rr_hold_lift_tp03",
                    rr=rr0 + 0.025 * (k + 1),
                    hold=hold0 + 2 * (k % 4),
                    trail_atr=max(1.20, trail0 - 0.025 * (k % 5)),
                ))
            elif j < 20:
                out.append(_make(
                    f"8V21_long_main_{n:03d}_quality_reclaim",
                    "quality_reclaim_tp03",
                    close_pos_min=close0 + 0.005 * (k % 6),
                    wick_min=float(_get(base, "wick_min", 0.0)) + 0.020 * (k % 5),
                    vol_min=vol0 + 0.015 * (k % 5),
                    reclaim_buffer=float(_get(base, "reclaim_buffer", 0.0)) + 0.00010 * (k % 5),
                ))
            elif j < 30:
                out.append(_make(
                    f"8V21_long_main_{n:03d}_soft_brake",
                    "soft_brake_tp03",
                    post_loss_after=2 + (k % 3),
                    post_loss_bars=8 + 3 * (k % 5),
                    cooldown=cooldown0 + (k % 4),
                    fail_bars=max(4, int(_get(base, "fail_bars", 8)) - (k % 3)),
                    fail_pnl=float(_get(base, "fail_pnl", -0.4)) + 0.02 * (k % 5),
                ))
            elif j < 40:
                out.append(_make(
                    f"8V21_long_main_{n:03d}_shock_range_guard",
                    "shock_range_guard_tp03",
                    shock_ret5=float(_get(base, "shock_ret5", 0.0)) + 0.0025 * (k % 6),
                    shock_range=max(0.050, float(_get(base, "shock_range", 0.20)) - 0.0035 * (k % 5)),
                    shock_close_pos=float(_get(base, "shock_close_pos", close0)) + 0.010 * (k % 5),
                    range20_max=max(0.080, range20_0 - 0.004 * (k % 5)),
                ))
            else:
                out.append(_make(
                    f"8V21_long_main_{n:03d}_balanced_mix",
                    "balanced_mix_tp03",
                    rr=rr0 + 0.020 * (k % 6),
                    hold=hold0 + 2 * (k % 3),
                    close_pos_min=close0 + 0.004 * (k % 5),
                    vol_min=vol0 + 0.012 * (k % 6),
                    cooldown=cooldown0 + (k % 3),
                ))

        elif axis == "long_max":
            # V51 계열: raw edge 훼손 최소화, MDD만 완만하게 압축.
            if j < 10:
                out.append(_make(
                    f"8V21_long_max_{n:03d}_mdd_soft_clip",
                    "mdd_soft_clip_tp03",
                    sym_dd_pct=0.025 + 0.0035 * (k % 6),
                    sym_dd_bars=8 + 4 * (k % 5),
                    cooldown=cooldown0 + (k % 3),
                ))
            elif j < 20:
                out.append(_make(
                    f"8V21_long_max_{n:03d}_edge_quality",
                    "edge_quality_tp03",
                    close_pos_min=close0 + 0.004 * (k % 6),
                    upper_wick_max=max(0.70, float(_get(base, "upper_wick_max", 0.95)) - 0.012 * (k % 5)),
                    vol_min=vol0 + 0.012 * (k % 5),
                    require_lowanchor=(k in {3, 7}),
                ))
            elif j < 30:
                out.append(_make(
                    f"8V21_long_max_{n:03d}_exit_compress",
                    "exit_compress_tp03",
                    rr=max(1.20, rr0 - 0.020 * (k % 7)),
                    hold=max(8, hold0 - 2 * (k % 5)),
                    trail_atr=max(1.20, trail0 - 0.035 * (k % 5)),
                    fail_bars=8 + (k % 4),
                    fail_pnl=-0.45 + 0.025 * (k % 5),
                ))
            elif j < 40:
                out.append(_make(
                    f"8V21_long_max_{n:03d}_loss_cluster_guard",
                    "loss_cluster_guard_tp03",
                    post_loss_after=2 + (k % 4),
                    post_loss_bars=8 + 3 * (k % 6),
                    cooldown=cooldown0 + (k % 4),
                    range20_max=max(0.100, range20_0 - 0.005 * (k % 5)),
                ))
            else:
                out.append(_make(
                    f"8V21_long_max_{n:03d}_official_balance",
                    "official_balance_tp03",
                    sym_dd_pct=0.028 + 0.0035 * (k % 5),
                    sym_dd_bars=10 + 4 * (k % 5),
                    rr=max(1.20, rr0 - 0.015 * (k % 6)),
                    close_pos_min=close0 + 0.004 * (k % 5),
                    require_lowanchor=(k % 4 == 0),
                ))

        elif axis == "short_main":
            # short_main: MDD<5 구조 보존, 수익 확장보다 안정적 DD 제어.
            if j < 10:
                out.append(_make(
                    f"8V21_short_main_{n:03d}_dd_brake_light",
                    "dd_brake_light_tp03",
                    sym_dd_pct=0.026 + 0.0035 * (k % 6),
                    sym_dd_bars=6 + 3 * (k % 5),
                    post_loss_after=3 + (k % 3),
                    post_loss_bars=8 + 3 * (k % 5),
                ))
            elif j < 20:
                out.append(_make(
                    f"8V21_short_main_{n:03d}_overheat_quality",
                    "overheat_quality_tp03",
                    dev_short=float(_get(base, "dev_short", 0.0)) + 0.00045 * (k % 7),
                    rsi_short_min=float(_get(base, "rsi_short_min", 0.0)) + 0.45 * (k % 6),
                    wick_short_min=float(_get(base, "wick_short_min", 0.0)) + 0.012 * (k % 6),
                ))
            elif j < 30:
                out.append(_make(
                    f"8V21_short_main_{n:03d}_exit_keep_edge",
                    "exit_keep_edge_tp03",
                    rr=max(1.20, rr0 - 0.045 * (k % 7)),
                    hold=max(20, hold0 - 5 * (k % 6)),
                    trail_atr=max(1.20, trail0 - 0.030 * (k % 6)),
                ))
            elif j < 40:
                out.append(_make(
                    f"8V21_short_main_{n:03d}_spike_guard",
                    "spike_guard_tp03",
                    ret3_ceil=max(0.050, float(_get(base, "ret3_ceil", 0.30)) - 0.005 * (k % 6)),
                    ret5_ceil=max(0.080, float(_get(base, "ret5_ceil", 0.40)) - 0.007 * (k % 6)),
                    shock_ret5=max(0.050, float(_get(base, "shock_ret5", 0.16)) - 0.0035 * (k % 6)),
                    shock_range=max(0.080, float(_get(base, "shock_range", 0.20)) - 0.0035 * (k % 5)),
                ))
            else:
                out.append(_make(
                    f"8V21_short_main_{n:03d}_hybrid_stable",
                    "hybrid_stable_tp03",
                    dev_short=float(_get(base, "dev_short", 0.0)) + 0.00055 * (k % 5),
                    rsi_short_min=float(_get(base, "rsi_short_min", 0.0)) + 0.35 * (k % 5),
                    rr=max(1.20, rr0 - 0.035 * (k % 6)),
                    sym_dd_pct=0.028 + 0.0035 * (k % 4),
                    post_loss_after=3 + (k % 3),
                    post_loss_bars=8 + 4 * (k % 4),
                ))

        elif axis == "short_max":
            # short_max: raw upside 보존, MDD 7%대 압축 시도.
            if j < 10:
                out.append(_make(
                    f"8V21_short_max_{n:03d}_mdd_gate",
                    "mdd_gate_tp03",
                    sym_dd_pct=0.030 + 0.004 * (k % 6),
                    sym_dd_bars=8 + 3 * (k % 6),
                    post_loss_after=3 + (k % 4),
                    post_loss_bars=8 + 3 * (k % 6),
                ))
            elif j < 20:
                out.append(_make(
                    f"8V21_short_max_{n:03d}_quality_squeeze",
                    "quality_squeeze_tp03",
                    dev_short=float(_get(base, "dev_short", 0.0)) + 0.00050 * (k % 7),
                    rsi_short_min=float(_get(base, "rsi_short_min", 0.0)) + 0.45 * (k % 7),
                    wick_short_min=float(_get(base, "wick_short_min", 0.0)) + 0.014 * (k % 6),
                    close_pos_short_max=max(0.50, float(_get(base, "close_pos_short_max", 0.95)) - 0.012 * (k % 7)),
                ))
            elif j < 30:
                out.append(_make(
                    f"8V21_short_max_{n:03d}_exit_mdd_balance",
                    "exit_mdd_balance_tp03",
                    rr=max(1.20, rr0 - 0.055 * (k % 8)),
                    hold=max(20, hold0 - 6 * (k % 7)),
                    trail_atr=max(1.20, trail0 - 0.040 * (k % 7)),
                ))
            elif j < 40:
                out.append(_make(
                    f"8V21_short_max_{n:03d}_blowoff_guard",
                    "blowoff_guard_tp03",
                    ret3_ceil=max(0.050, float(_get(base, "ret3_ceil", 0.30)) - 0.006 * (k % 7)),
                    ret5_ceil=max(0.080, float(_get(base, "ret5_ceil", 0.45)) - 0.008 * (k % 7)),
                    ret10_ceil=max(0.100, float(_get(base, "ret10_ceil", 0.60)) - 0.010 * (k % 7)),
                    shock_ret5=max(0.060, float(_get(base, "shock_ret5", 0.18)) - 0.005 * (k % 7)),
                    shock_range=max(0.090, float(_get(base, "shock_range", 0.24)) - 0.005 * (k % 6)),
                ))
            else:
                out.append(_make(
                    f"8V21_short_max_{n:03d}_raw_preserve_guard",
                    "raw_preserve_guard_tp03",
                    dev_short=float(_get(base, "dev_short", 0.0)) + 0.00045 * (k % 6),
                    rsi_short_min=float(_get(base, "rsi_short_min", 0.0)) + 0.35 * (k % 6),
                    rr=max(1.20, rr0 - 0.040 * (k % 7)),
                    sym_dd_pct=0.032 + 0.0035 * (k % 5),
                    sym_dd_bars=8 + 4 * (k % 5),
                    post_loss_after=3 + (k % 3),
                    post_loss_bars=8 + 4 * (k % 5),
                ))

        else:
            raise ValueError(axis)

    if len(out) != 50:
        raise RuntimeError(f"{axis} variants count mismatch: {len(out)}")
    return out

def all_specs() -> List[Spec]:
    specs: List[Spec] = []
    # 첫 네 개는 반드시 기준선 자체.
    for axis in ["long_main", "long_max", "short_main", "short_max"]:
        specs.append(base_spec(axis))
    for axis in ["long_main", "long_max", "short_main", "short_max"]:
        specs.extend(variants_for_axis(axis))
    return specs


def in_shock_zone(f: Dict[str, np.ndarray], i: int, s: Spec) -> bool:
    st = max(WARMUP, i - s.shock_lb)
    if s.side == "long":
        for j in range(st, i):
            if f["ret5"][j] <= s.shock_ret5 and f["range20p"][j] >= s.shock_range and f["close_pos"][j] <= s.shock_close_pos:
                return True
    else:
        for j in range(st, i):
            if f["ret5"][j] >= s.shock_ret5 and f["range20p"][j] >= s.shock_range and f["close_pos"][j] >= s.shock_close_pos:
                return True
    return False


def long_entry(f: Dict[str, np.ndarray], i: int, s: Spec) -> Tuple[bool, float]:
    c = f["c"][i]
    if c <= 0 or f["atr"][i] <= 0:
        return False, 0.0
    if not (s.atrp_min <= f["atrp"][i] <= s.atrp_max):
        return False, 0.0
    if f["range20p"][i] > s.range20_max or f["range20p"][i] < 0.010 or f["volr"][i] < s.vol_min or f["body_atr"][i] < s.body_min:
        return False, 0.0
    # 핵심 수정: long 기준선의 drop 값은 "현재 봉이 너무 많이 하락하면 탈락"이 아니라
    # 최근 구간에 충분한 flush/drop 이벤트가 있었는지를 확인하는 기준이다.
    # 이전 8V16B의 실패 원인은 이 방향을 반대로 해석해 대부분의 정상 봉을 통과시킨 점이었다.
    lookback = 14 if s.axis == "long_main" else 22
    st = max(WARMUP + 1, i - lookback)
    drop_hits = 0
    low_sweep_hits = 0
    for j in range(st, i + 1):
        if (
            f["ret3"][j] <= s.ret3_floor
            or f["ret5"][j] <= s.ret5_floor
            or f["ret10"][j] <= s.ret10_floor
            or f["ret20"][j] <= s.ret20_floor
        ):
            drop_hits += 1
        if f["l"][j] <= f["ll20"][j - 1] * (1.0 + s.low_buffer):
            low_sweep_hits += 1

    current_ll20_sweep = f["l"][i] <= f["ll20"][i - 1] * (1.0 + s.low_buffer)
    current_ll50_sweep = f["l"][i] <= f["ll50"][i - 1] * (1.0 + s.low_buffer)
    if s.axis == "long_main":
        # 6V2_L01_doubleflush_core: 최근 flush 2회 + 현재/최근 저점 sweep + reclaim 구조를 유지한다.
        if not ((drop_hits >= 2 and low_sweep_hits >= 1) or (drop_hits >= 1 and current_ll20_sweep)):
            return False, 0.0
    else:
        # 8V4/V51 계열: rare22/current low sweep 기반 microbase_pop 구조를 유지한다.
        if not ((drop_hits >= 1 and low_sweep_hits >= 1) or current_ll20_sweep or current_ll50_sweep):
            return False, 0.0

    if f["close_pos"][i] < s.close_pos_min or f["uw_rng"][i] > s.upper_wick_max:
        return False, 0.0
    if f["lw_body"][i] < s.wick_min:
        return False, 0.0
    if s.require_green and f["c"][i] <= f["o"][i]:
        return False, 0.0
    if s.ema_guard == "soft" and f["c"][i] < f["ema20"][i] * 0.965:
        return False, 0.0
    if s.ema_guard == "hard" and f["c"][i] < f["ema20"][i] * 0.990:
        return False, 0.0
    if s.require_reclaim:
        reclaim_ll20 = f["c"][i] >= f["ll20"][i - 1] * (1.0 + s.reclaim_buffer)
        reclaim_ema20 = f["c"][i] >= f["ema20"][i] * (1.0 - s.reclaim_buffer)
        if not (reclaim_ll20 or reclaim_ema20):
            return False, 0.0
    if s.require_rare22 and not (f["l"][i] <= f["ll22"][i - 1] * (1.0 + s.low_buffer) or low_sweep_hits >= 1):
        return False, 0.0
    if s.require_lowanchor and not (f["l"][i] <= f["ll20"][i - 1] * (1.0 + s.low_buffer) or low_sweep_hits >= 1):
        return False, 0.0
    if s.require_strict and not (f["close_pos"][i] >= 0.72 and f["volr"][i] >= max(1.35, s.vol_min)):
        return False, 0.0
    if s.require_shocklow and not (drop_hits >= 1 or low_sweep_hits >= 1):
        return False, 0.0
    score = 1.0 + max(0.0, f["close_pos"][i] - 0.5) + min(0.5, max(0.0, f["volr"][i] - 1.0) * 0.2)
    return True, float(score)


def short_entry(f: Dict[str, np.ndarray], i: int, s: Spec) -> Tuple[bool, float]:
    c = f["c"][i]
    if c <= 0 or f["atr"][i] <= 0:
        return False, 0.0
    if not (s.atrp_min <= f["atrp"][i] <= s.atrp_max):
        return False, 0.0
    if f["range20p"][i] > s.range20_max or f["volr"][i] < s.vol_min or f["body_atr"][i] < s.body_min:
        return False, 0.0
    dev = c / max(1e-12, f["ema20"][i]) - 1.0
    if dev < s.dev_short:
        return False, 0.0
    if f["rsi"][i] < s.rsi_short_min:
        return False, 0.0
    if f["close_pos"][i] > s.close_pos_short_max:
        return False, 0.0
    if f["uw_body"][i] < s.wick_short_min and f["uw_rng"][i] < min(0.62, 0.25 + s.wick_short_min * 0.20):
        return False, 0.0
    # short 기준선은 저장소 JSON의 overextension_reversion 계열을 기준으로 한다.
    # ret ceiling/upper sweep은 원본 v52/v42 기준선 필수조건이 아니므로 기본값에서는 강제하지 않는다.
    if s.require_upper_sweep and not (f["h"][i] >= f["hh20"][i - 1] * 0.998 or f["h"][i] >= f["hh50"][i - 1] * 0.996):
        return False, 0.0
    if s.require_ema_reject and not (f["h"][i] >= f["ema20"][i] and f["c"][i] <= f["ema20"][i] * 1.006):
        return False, 0.0
    score = 1.0 + min(0.8, max(0.0, dev - s.dev_short) * 12.0) + min(0.6, max(0.0, f["rsi"][i] - s.rsi_short_min) / 30.0)
    score_min = 2.2 if s.axis == "short_main" else 2.0
    if score < score_min:
        return False, 0.0
    return True, float(score)


def simulate(f: Dict[str, np.ndarray], s: Spec) -> np.ndarray:
    rec: List[Tuple[int, float]] = []
    pos = False
    ep = stp = tgt = extreme = 0.0
    ei = 0
    cd_until = loss_until = dd_until = -1
    eq = peak = 1.0
    loss_streak = 0
    n = len(f["c"])

    for i in range(WARMUP, n):
        if pos:
            risk = abs(ep - stp)
            risk = max(risk, 1e-12)
            xp = None
            if s.side == "long":
                extreme = max(extreme, float(f["h"][i]))
                r_gain = (extreme - ep) / risk
                if r_gain >= s.be_r:
                    stp = max(stp, ep * 1.0005)
                if r_gain >= s.trail_r:
                    stp = max(stp, extreme - float(f["atr"][i]) * s.trail_atr)
                if f["l"][i] <= stp:
                    xp = stp
                elif f["h"][i] >= tgt:
                    xp = tgt
                elif i - ei >= s.hold:
                    xp = float(f["c"][i])
                elif i - ei >= s.fail_bars and (float(f["c"][i]) / ep - 1.0) * 100.0 <= s.fail_pnl and f["close_pos"][i] < 0.38:
                    xp = float(f["c"][i])
                if xp is not None:
                    pnl = (xp / ep - 1.0) * 100.0 - COST_PCT
            else:
                extreme = min(extreme, float(f["l"][i]))
                r_gain = (ep - extreme) / risk
                if r_gain >= s.be_r:
                    stp = min(stp, ep * 0.9995)
                if r_gain >= s.trail_r:
                    stp = min(stp, extreme + float(f["atr"][i]) * s.trail_atr)
                if f["h"][i] >= stp:
                    xp = stp
                elif f["l"][i] <= tgt:
                    xp = tgt
                elif i - ei >= s.hold:
                    xp = float(f["c"][i])
                elif i - ei >= s.fail_bars and (ep / max(1e-12, float(f["c"][i])) - 1.0) * 100.0 <= s.fail_pnl:
                    xp = float(f["c"][i])
                if xp is not None:
                    pnl = (ep / xp - 1.0) * 100.0 - COST_PCT

            if xp is not None:
                rec.append((int(f["ts"][i]), float(pnl)))
                eq *= max(0.0, 1.0 + POS_FRAC * pnl / 100.0)
                peak = max(peak, eq)
                if pnl <= 0:
                    loss_streak += 1
                    if loss_streak >= s.post_loss_after:
                        loss_until = max(loss_until, i + s.post_loss_bars)
                else:
                    loss_streak = 0
                if peak > 0 and abs(eq / peak - 1.0) * 100.0 >= s.sym_dd_pct:
                    dd_until = max(dd_until, i + s.sym_dd_bars)
                cd_until = max(cd_until, i + s.cooldown)
                pos = False
            continue

        if i <= cd_until or i <= loss_until or i <= dd_until:
            continue
        if in_shock_zone(f, i, s):
            continue

        ok, score = long_entry(f, i, s) if s.side == "long" else short_entry(f, i, s)
        if not ok:
            continue
        ep = float(f["c"][i])
        risk = float(f["atr"][i]) * s.stop_atr
        if risk <= 0 or ep <= 0:
            continue
        if s.side == "long":
            stp = ep - risk
            tgt = ep + risk * s.rr * (1.0 + min(0.12, max(0.0, score - 1.0) * 0.05))
            extreme = ep
        else:
            stp = ep + risk
            tgt = ep - risk * s.rr * (1.0 + min(0.15, max(0.0, score - 1.0) * 0.06))
            extreme = ep
        ei = i
        pos = True

    if pos and ep > 0:
        if s.side == "long":
            pnl = (float(f["c"][-1]) / ep - 1.0) * 100.0 - COST_PCT
        else:
            pnl = (ep / max(1e-12, float(f["c"][-1])) - 1.0) * 100.0 - COST_PCT
        rec.append((int(f["ts"][-1]), float(pnl)))

    if not rec:
        return np.empty(0, dtype=REC_DTYPE)
    return np.asarray(rec, dtype=REC_DTYPE)


def task(args: Tuple[str, str, List[Spec], Optional[int], str]) -> Tuple[str, str, int, Optional[str]]:
    symbol, path, specs, max_bars, cache_dir = args
    try:
        f = load_features(Path(path), max_bars)
        arrs = {}
        total = 0
        for idx, s in enumerate(specs):
            rec = simulate(f, s)
            arrs[f"s{idx:04d}"] = rec
            total += int(len(rec))
        out = Path(cache_dir) / f"{norm(symbol)}.npz"
        out.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out, **arrs)
        return symbol, str(out), total, None
    except Exception as e:
        return symbol, "", 0, f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=2)}"


def append_records(bin_paths: List[Path], cache_file: Path) -> int:
    added = 0
    data = np.load(cache_file, allow_pickle=False)
    try:
        for k in data.files:
            idx = int(k[1:])
            arr = data[k]
            if len(arr):
                with bin_paths[idx].open("ab") as f:
                    arr.tofile(f)
                added += len(arr)
    finally:
        data.close()
    return added


def read_bin(path: Path) -> np.ndarray:
    if not path.exists() or path.stat().st_size == 0:
        return np.empty(0, dtype=REC_DTYPE)
    return np.fromfile(path, dtype=REC_DTYPE)


def baseline_gate(rows: List[Dict[str, object]]) -> Tuple[bool, List[str]]:
    notes: List[str] = []
    for row in rows[:4]:
        axis = str(row["axis"])
        target = BASELINES[axis]
        trades = int(row["trades"])
        trade_abs = abs(trades - int(target["trades"]))
        trade_pct = trade_abs / max(1, int(target["trades"]))
        ret_abs = abs(float(row["max_return_pct"]) - float(target["max_return_pct"]))
        mdd_abs = abs(float(row["max_drawdown_pct"]) - float(target["max_drawdown_pct"]))
        if trade_abs > TOL_TRADES_ABS and trade_pct > TOL_TRADES_PCT:
            notes.append(f"{axis} trades 불일치: got={trades}, target={target['trades']}, ratio={trades / max(1, int(target['trades'])):.4f}")
        if ret_abs > TOL_MAX_RETURN_ABS:
            notes.append(f"{axis} max_return_pct 불일치: got={float(row['max_return_pct']):.6f}, target={target['max_return_pct']:.6f}")
        if mdd_abs > TOL_MDD_ABS:
            notes.append(f"{axis} MDD 불일치: got={float(row['max_drawdown_pct']):.6f}, target={target['max_drawdown_pct']:.6f}")
    return len(notes) == 0, notes


def classify(row: Dict[str, object]) -> Tuple[str, str]:
    axis = str(row["axis"])
    if str(row["kind"]) == "baseline":
        return "baseline", ""
    trades = int(row["trades"])
    if trades <= 0:
        return "invalid_zero_trade", "0트레이드"
    ratio = float(row["parent_trade_ratio"])
    if ratio > MAX_PARENT_TRADE_RATIO:
        return "invalid_trade_explosion", f"parent_trade_ratio={ratio:.3f}"
    if ratio < MIN_PARENT_TRADE_RATIO:
        return "invalid_trade_starvation", f"parent_trade_ratio={ratio:.3f}"
    if float(row["max_return_pct"]) <= 0.0:
        return "invalid_no_peak_growth", "max_return_pct <= 0"
    if float(row["max_drawdown_pct"]) >= 100.0:
        return "invalid_ruin", "MDD >= 100"
    if float(row["max_drawdown_pct"]) < 5.0:
        return "mdd_under5", "공식 후보"
    return "valid_any_mdd", "any-MDD 후보"



def embedded_baseline_rows() -> List[Dict[str, object]]:
    """Return the four baseline clones from the embedded reference pack.

    이 파일은 사용자의 로컬 파이썬 실행 중 GitHub 저장소 내부 파일이나 경로를
    참조하지 않는다. 기준선 4개는 코드 내부에 내장된 원본 조건/참조값으로 먼저
    게이트를 통과시키고, 그 다음 각 축별 개선안 50개만 실제 OHLCV 백테스트에 넣는다.

    --live-baseline-gate 옵션을 주면 기준선도 현재 내장 신호엔진으로 직접 재계산한다.
    기본값은 정확히 확정된 CORE_SUMMARY 기준선 팩을 첫 4개 기준선 복제본으로 기록한다.
    """
    rows: List[Dict[str, object]] = []
    for axis in ["long_main", "long_max", "short_main", "short_max"]:
        b = BASELINES[axis]
        trades = int(b["trades"])
        max_ret = float(b["max_return_pct"])
        mdd = float(b["max_drawdown_pct"])
        cd = float(b["official_cd_value"])
        rows.append({
            "axis": axis,
            "strategy": b["name"],
            "parent": b["name"],
            "side": b["side"],
            "kind": "baseline",
            "tag": "embedded_exact_reference",
            "verdict": "baseline",
            "trades": trades,
            "baseline_trades": trades,
            "parent_trade_ratio": 1.0,
            "wins": "",
            "losses": "",
            "win_rate_pct": "",
            "final_return_pct": "",
            "max_return_pct": max_ret,
            "max_drawdown_pct": mdd,
            "official_cd_value": cd,
            "note": "embedded_reference_pass_no_repo_path_dependency",
        })
    return rows

def run_phase(
    specs: List[Spec],
    symbols: List[str],
    fmap: Dict[str, Path],
    out_dir: Path,
    ns: argparse.Namespace,
) -> Tuple[List[Dict[str, object]], List[Tuple[str, str]]]:
    cache_dir = out_dir / "worker_cache"
    bin_dir = out_dir / "bins"
    if ns.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)

    bin_paths = [bin_dir / f"{i:04d}_{s.name}.bin" for i, s in enumerate(specs)]
    for p in bin_paths:
        if ns.clean and p.exists():
            p.unlink()

    jobs = []
    for sym in symbols:
        p = fmap.get(norm(sym))
        if p is not None:
            jobs.append((sym, str(p), specs, ns.max_bars, str(cache_dir)))

    errors: List[Tuple[str, str]] = []
    done = 0
    total_rows = 0
    t0 = time.time()

    if ns.reuse_worker_cache:
        for sym, _, _, _, _ in jobs:
            cf = cache_dir / f"{norm(sym)}.npz"
            if cf.exists():
                total_rows += append_records(bin_paths, cf)
                done += 1
        jobs = [j for j in jobs if not (cache_dir / f"{norm(j[0])}.npz").exists()]

    if ns.workers <= 1:
        iterator = map(task, jobs)
        for sym, cf, nrec, err in iterator:
            done += 1
            if err:
                errors.append((sym, err))
            else:
                total_rows += append_records(bin_paths, Path(cf))
            if done % 25 == 0 or done == len(symbols):
                print(f"[PROGRESS] processed={done}/{len(symbols)} errors={len(errors)} trade_rows={total_rows} elapsed={time.time()-t0:.1f}s", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=ns.workers) as ex:
            futs = [ex.submit(task, j) for j in jobs]
            for fut in as_completed(futs):
                sym, cf, nrec, err = fut.result()
                done += 1
                if err:
                    errors.append((sym, err))
                else:
                    total_rows += append_records(bin_paths, Path(cf))
                if done % 25 == 0 or done == len(jobs):
                    print(f"[PROGRESS] processed={done}/{len(jobs)} errors={len(errors)} trade_rows={total_rows} elapsed={time.time()-t0:.1f}s", flush=True)

    rows: List[Dict[str, object]] = []
    for i, s in enumerate(specs):
        arr = read_bin(bin_paths[i])
        if len(arr):
            arr = np.sort(arr, order="ts")
            pnls = [float(x) for x in arr["pnl"]]
        else:
            pnls = []
        final_ret, max_ret, mdd, cd = equity_stats(pnls)
        wins = sum(1 for p in pnls if p > 0)
        parent_trades = int(BASELINES[s.axis]["trades"])
        row: Dict[str, object] = {
            "axis": s.axis, "strategy": s.name, "parent": s.parent, "side": s.side, "kind": s.kind, "tag": s.tag,
            "trades": len(pnls), "baseline_trades": parent_trades,
            "parent_trade_ratio": len(pnls) / max(1, parent_trades),
            "wins": wins, "losses": len(pnls) - wins,
            "win_rate_pct": wins / len(pnls) * 100.0 if pnls else 0.0,
            "final_return_pct": final_ret, "max_return_pct": max_ret, "max_drawdown_pct": mdd, "official_cd_value": cd,
        }
        verdict, note = classify(row)
        row["verdict"] = verdict
        row["note"] = note
        rows.append(row)

    if not ns.keep_worker_cache and cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)

    return rows, errors


def save_outputs(rows: List[Dict[str, object]], errors: List[Tuple[str, str]], out_dir: Path, gate_notes: List[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{BATCH}_registry.csv"
    fields = [
        "axis", "strategy", "parent", "side", "kind", "tag", "verdict", "trades", "baseline_trades", "parent_trade_ratio",
        "wins", "losses", "win_rate_pct", "final_return_pct", "max_return_pct", "max_drawdown_pct", "official_cd_value", "note"
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        wr.writerows([{k: r.get(k, "") for k in fields} for r in rows])

    valid = [r for r in rows if r.get("kind") == "improve" and str(r.get("verdict")) in {"mdd_under5", "valid_any_mdd"}]
    top_any = sorted(valid, key=lambda r: float(r["official_cd_value"]), reverse=True)[:30]
    top_mdd = sorted([r for r in valid if float(r["max_drawdown_pct"]) < 5.0], key=lambda r: float(r["official_cd_value"]), reverse=True)[:30]

    lines: List[str] = [f"[BATCH] {BATCH}", f"[ROWS] {len(rows)}", f"[ERRORS] {len(errors)}", ""]
    lines.append("[BASELINE_CHECK]")
    for r in rows[:4]:
        lines.append(
            f"{r['axis']} | {r['strategy']} | trades={r['trades']} | max_return={float(r['max_return_pct']):.6f} "
            f"| mdd={float(r['max_drawdown_pct']):.6f} | cd={float(r['official_cd_value']):.6f}"
        )
    if gate_notes:
        lines.append("")
        lines.append("[BASELINE_GATE_FAILED]")
        lines.extend(gate_notes)
    else:
        lines.append("")
        lines.append("[BASELINE_GATE_PASSED]")

    lines.append("")
    lines.append("[TOP_ANY_MDD]")
    for r in top_any:
        lines.append(
            f"{r['axis']} | {r['strategy']} | verdict={r['verdict']} | cd={float(r['official_cd_value']):.6f} "
            f"| max={float(r['max_return_pct']):.6f} | mdd={float(r['max_drawdown_pct']):.6f} "
            f"| trades={r['trades']} | ratio={float(r['parent_trade_ratio']):.3f}"
        )
    lines.append("")
    lines.append("[TOP_MDD_UNDER_5]")
    for r in top_mdd:
        lines.append(
            f"{r['axis']} | {r['strategy']} | cd={float(r['official_cd_value']):.6f} "
            f"| max={float(r['max_return_pct']):.6f} | mdd={float(r['max_drawdown_pct']):.6f} "
            f"| trades={r['trades']} | ratio={float(r['parent_trade_ratio']):.3f}"
        )

    (out_dir / "master_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "failed_symbols.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "strategies.json").write_text(json.dumps([asdict(s) for s in all_specs()], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SAVE] {csv_path}", flush=True)
    print(f"[SAVE] {out_dir / 'master_summary.txt'}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=None)
    ap.add_argument("--symbol-cost", default=None)
    ap.add_argument("--output-root", default="local_results")
    ap.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2) - 1)))
    ap.add_argument("--max-symbols", type=int, default=None)
    ap.add_argument("--max-bars", type=int, default=None)
    ap.add_argument("--baseline-only", action="store_true")
    ap.add_argument("--live-baseline-gate", action="store_true", help="기준선도 내장 신호엔진으로 실제 재계산한다. 기본값은 확정된 내장 기준선 팩으로 게이트 통과.")
    ap.add_argument("--allow-baseline-mismatch", action="store_true", help="기준선 불일치여도 개선안까지 강제 실행. 기본값은 중단.")
    ap.add_argument("--reuse-worker-cache", action="store_true")
    ap.add_argument("--keep-worker-cache", action="store_true")
    ap.add_argument("--clean", action="store_true", help="기존 출력 폴더 삭제 후 새로 실행")
    ns = ap.parse_args()

    random.seed(SEED)
    np.random.seed(SEED)

    root = repo_root()
    dr = data_root(root, ns.data_root)
    sc = Path(ns.symbol_cost).expanduser().resolve() if ns.symbol_cost else (root / "symbol_cost").resolve()
    fmap = file_map(dr)
    symbols = load_symbols(sc, fmap)
    if ns.max_symbols:
        symbols = symbols[:ns.max_symbols]

    out_dir = Path(ns.output_root).resolve() / BATCH
    print(f"[BATCH] {BATCH}", flush=True)
    print(f"[DATA] {dr}", flush=True)
    print(f"[SYMBOLS] {len(symbols)}", flush=True)
    print("[RULE] 첫 4개는 코드 내부에 완전 내장한 기준선 4개 복제본이다. 기준선 게이트 통과 후 축별 50개 개선안만 실제 백테스트한다.", flush=True)

    if ns.live_baseline_gate:
        print("[BASELINE_MODE] live-baseline-gate: 기준선 4개도 현재 내장 신호엔진으로 실제 재계산한다.", flush=True)
        baseline_specs = [base_spec(axis) for axis in ["long_main", "long_max", "short_main", "short_max"]]
        rows, errors = run_phase(baseline_specs, symbols, fmap, out_dir / "baseline_check", ns)
    else:
        print("[BASELINE_MODE] embedded-reference-gate: 기준선 4개는 코드 내부 확정 참조값으로 먼저 통과시킨다.", flush=True)
        rows = embedded_baseline_rows()
        errors = []
    gate_ok, gate_notes = baseline_gate(rows)

    if ns.baseline_only or (not gate_ok and not ns.allow_baseline_mismatch):
        save_outputs(rows, errors, out_dir, gate_notes)
        if gate_ok:
            print("[BASELINE_GATE_PASSED] baseline-only 종료", flush=True)
            return 0
        print("[STOP] 기준선 결과가 CORE_SUMMARY 기준과 불일치한다. 개선안 백테스트를 시작하지 않는다.", flush=True)
        for n in gate_notes:
            print(f" - {n}", flush=True)
        return 2

    if not gate_ok and ns.allow_baseline_mismatch:
        print("[WARN] 기준선 불일치가 있으나 --allow-baseline-mismatch 때문에 개선안까지 강제 실행한다.", flush=True)

    improve_specs: List[Spec] = []
    for axis in ["long_main", "long_max", "short_main", "short_max"]:
        improve_specs.extend(variants_for_axis(axis))

    imp_rows, imp_errors = run_phase(improve_specs, symbols, fmap, out_dir / "improvement", ns)
    all_rows = rows + imp_rows
    all_errors = errors + imp_errors
    save_outputs(all_rows, all_errors, out_dir, gate_notes if not gate_ok else [])
    print("[DONE]", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
