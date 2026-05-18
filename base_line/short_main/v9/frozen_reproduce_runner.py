from __future__ import annotations

import argparse
import json
import math
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

"""
short_main v9 frozen reproduction runner

목적
- 처음 보는 사람이 short_main v9 기준선을 그대로 재현할 수 있게 하는 단독 실행 파일이다.
- 외부 runner, 외부 json, GitHub 저장소 경로를 참조하지 않는다.
- OHLCV CSV 폴더만 지정하면 v9 공식 결과를 재현하도록 actual bar engine을 포함한다.

실행 예시
python base_line/short_main/v9/frozen_reproduce_runner.py --data-dir ./Data/time
python base_line/short_main/v9/frozen_reproduce_runner.py --data-dir ./Data/time --out-dir ./local_results/short_main/SHORT_MAIN_V9_REPRODUCE

공식 재현 목표
- trades: 36791
- wins: 5171
- losses: 31620
- max_return_pct: 1195.2759019740386
- max_drawdown_pct: 4.770262221769094
- official_cd_value: 1233.487844954492
- same_bar_trades: 3354
- active_leftover: 0
- pending_leftover: 0
- load_errors: 0
"""

TRAIN_END = pd.Timestamp("2025-12-31 23:59:59")
HOLDOUT_START = pd.Timestamp("2026-01-01 00:00:00")

CFG: Dict[str, Any] = dict(
    strategy="short_main_v9_wick120_dev03475_timeout215_actual_bar_engine",
    axis="short_main",
    baseline_version="short_main/v9",
    source_candidate="SM23_D02_wick120_dev03475_timeout215",
    parent_strategy="short_main_v8_wick125_actual_bar_engine",
    engine="actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231",
    data_scope="train_only_until_2025_12_31_end",
    initial_asset=100.0,
    position_fraction=0.01,
    fee_per_side=0.0004,
    min_bars=120,
    ema_period=20,
    rsi_period=14,
    atr_period=14,
    short_dev=0.03475,
    short_rsi_min=77.0,
    use_rsi_gate=False,
    short_wick_mult=1.20,
    score_min_short=2.35,
    score_dev_weight=1.0,
    score_rsi_weight=0.8,
    score_wick_weight=0.7,
    score_dev_cap=2.0,
    score_rsi_cap=2.0,
    score_wick_cap=2.5,
    wick_atr_floor_mult=0.2,
    atr_stop_mult=1.8975,
    rr_mult=5.75,
    min_expected_tp=0.003,
    timeout_bars=215,
    time_reduce_bars=8,
    time_reduce_to_risk_frac=0.05,
    fail_fast_bars=10,
    fail_fast_min_progress_r=0.1,
    dd_brake_trigger_pct=0.03,
    dd_brake_freeze_steps=5,
    dd_brake_mode="edge_current",
)

OFFICIAL_RESULT: Dict[str, Any] = dict(
    trades=36791,
    wins=5171,
    losses=31620,
    win_rate_pct=14.055067815498356,
    final_return_pct=1194.9206565723089,
    max_return_pct=1195.2759019740386,
    max_drawdown_pct=4.770262221769094,
    official_cd_value=1233.487844954492,
    profit_factor=1.5698636647889879,
    max_conc=287,
    same_bar_trades=3354,
    active_leftover=0,
    pending_leftover=0,
    load_errors=0,
)


def ema(a: np.ndarray, p: int) -> np.ndarray:
    return pd.Series(a, dtype=float).ewm(span=int(p), adjust=False).mean().to_numpy(float)


def rsi(a: np.ndarray, p: int) -> np.ndarray:
    s = pd.Series(a, dtype=float)
    d = s.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    avg_up = up.ewm(alpha=1 / int(p), adjust=False).mean()
    avg_dn = dn.ewm(alpha=1 / int(p), adjust=False).mean().replace(0, np.nan)
    rs = avg_up / avg_dn
    return (100 - 100 / (1 + rs)).to_numpy(float)


def atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, p: int) -> np.ndarray:
    pc = np.roll(c, 1)
    pc[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr, dtype=float).ewm(alpha=1 / int(p), adjust=False).mean().to_numpy(float)


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace("\ufeff", "").lower() for c in df.columns]
    aliases = dict(
        date=["date", "datetime", "timestamp", "time", "open_time", "opentime", "candle_date_time_utc", "candle_date_time_kst"],
        open=["open", "open_price", "opening_price", "시가"],
        high=["high", "high_price", "고가"],
        low=["low", "low_price", "저가"],
        close=["close", "close_price", "closing_price", "trade_price", "종가"],
        volume=["volume", "vol", "base_volume", "candle_acc_trade_volume", "acc_trade_volume", "거래량"],
    )
    rename_map: Dict[str, str] = {}
    for target, keys in aliases.items():
        hit = next((k for k in keys if k in df.columns), None)
        if hit is None:
            raise ValueError(f"missing column {target}")
        rename_map[hit] = target
    out = df.rename(columns=rename_map)[["date", "open", "high", "low", "close", "volume"]].copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    try:
        if out["date"].dt.tz is not None:
            out["date"] = out["date"].dt.tz_convert(None)
    except Exception:
        pass
    out = out[out["date"] <= TRAIN_END].copy()
    for col in ["open", "high", "low", "close", "volume"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out.dropna().sort_values("date").drop_duplicates("date").reset_index(drop=True)


def load_symbol(path: Path) -> Dict[str, Any]:
    head = path.read_text(encoding="utf-8", errors="ignore")[:80]
    if head.startswith("version https://git-lfs.github.com/spec/"):
        raise ValueError("LFS pointer")
    d = normalize_ohlcv(pd.read_csv(path, low_memory=False))
    if len(d) < int(CFG["min_bars"]):
        raise ValueError(f"too few bars {len(d)}")
    o = d.open.to_numpy(float)
    h = d.high.to_numpy(float)
    l = d.low.to_numpy(float)
    c = d.close.to_numpy(float)
    ts = pd.to_datetime(d.date).astype("int64").to_numpy()
    return dict(
        symbol=path.stem,
        ts=ts,
        open=o,
        high=h,
        low=l,
        close=c,
        volume=d.volume.to_numpy(float),
        ema20=ema(c, int(CFG["ema_period"])),
        rsi14=rsi(c, int(CFG["rsi_period"])),
        atr14=atr(h, l, c, int(CFG["atr_period"])),
        body=np.abs(c - o),
        upper_wick=h - np.maximum(o, c),
    )


def calc_score(s: Dict[str, Any], i: int) -> float:
    close = float(s["close"][i])
    e = float(s["ema20"][i])
    rr = float(s["rsi14"][i])
    at = float(s["atr14"][i])
    body = float(s["body"][i])
    up = float(s["upper_wick"][i])
    dev_raw = max(0.0, close / max(e, 1e-12) - 1.0)
    rsi_raw = max(0.0, rr - float(CFG["short_rsi_min"]))
    wick_ratio = max(0.0, up / max(abs(body), at * float(CFG["wick_atr_floor_mult"]), 1e-12))
    dev_score = min(dev_raw / float(CFG["short_dev"]), float(CFG["score_dev_cap"]))
    rsi_score = min(rsi_raw / 10.0, float(CFG["score_rsi_cap"]))
    wick_score = min(math.log1p(wick_ratio), float(CFG["score_wick_cap"]))
    return float(CFG["score_dev_weight"]) * dev_score + float(CFG["score_rsi_weight"]) * rsi_score + float(CFG["score_wick_weight"]) * wick_score


def make_pending(si: int, s: Dict[str, Any], i: int) -> Optional[Dict[str, Any]]:
    j = i + 1
    if j >= len(s["ts"]):
        return None
    vals = [s["close"][i], s["ema20"][i], s["rsi14"][i], s["atr14"][i], s["open"][j]]
    if not all(np.isfinite(float(x)) for x in vals):
        return None
    close = float(s["close"][i])
    e = float(s["ema20"][i])
    at = float(s["atr14"][i])
    body = float(s["body"][i])
    up = float(s["upper_wick"][i])
    if e <= 0 or at <= 0:
        return None
    score = calc_score(s, i)
    ok = close / max(e, 1e-12) - 1.0 >= float(CFG["short_dev"])
    ok = ok and up >= float(CFG["short_wick_mult"]) * body
    ok = ok and score >= float(CFG["score_min_short"])
    if bool(CFG["use_rsi_gate"]):
        ok = ok and float(s["rsi14"][i]) > float(CFG["short_rsi_min"])
    if not ok:
        return None
    entry = float(s["open"][j])
    risk = at * float(CFG["atr_stop_mult"])
    stop = entry + risk
    target = entry - float(CFG["rr_mult"]) * risk
    expected_tp = (entry - target) / max(entry, 1e-12)
    if entry <= 0 or expected_tp < float(CFG["min_expected_tp"]):
        return None
    return dict(si=si, symbol=s["symbol"], sig=i, ei=j, ets=int(s["ts"][j]), entry=entry, risk=float(risk), stop=float(stop), target=float(target), score=float(score))


def short_return(entry: float, exit_price: float) -> float:
    return entry / max(exit_price, 1e-12) - 1.0 - 2.0 * float(CFG["fee_per_side"])


def official_cd(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def run_engine(symbols: List[Dict[str, Any]], events: Dict[int, List[Tuple[int, int]]], timeline: List[int]) -> Dict[str, Any]:
    equity = float(CFG["initial_asset"])
    peak = equity
    peak_asset = equity
    mdd = 0.0
    gross_profit = 0.0
    gross_loss = 0.0
    wins = 0
    losses = 0
    active: Dict[int, Dict[str, Any]] = {}
    pending: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    trades: List[Dict[str, Any]] = []
    generated = 0
    executed = 0
    blocked = 0
    max_conc = 0
    max_conc_unique = 0
    freeze = 0
    prev_dd_below = False

    for ts in timeline:
        # 1. t open: t-1 close에서 생성된 pending entry만 진입한다.
        candidates = [p for p in pending.pop(ts, []) if p["si"] not in active]
        candidates.sort(key=lambda x: x["score"], reverse=True)
        if freeze > 0:
            blocked += len(candidates)
            candidates = []
            freeze -= 1
        equity_snapshot = equity
        for p in candidates:
            if p["si"] not in active:
                active[p["si"]] = dict(**p, notional=equity_snapshot * float(CFG["position_fraction"]), mfe=0.0)
                executed += 1
        max_conc = max(max_conc, len(active))
        max_conc_unique = max(max_conc_unique, len({p["symbol"] for p in active.values()}))

        # 2. t candle: high/low/close로 청산 평가한다.
        for si, i in events.get(ts, []):
            p = active.get(si)
            if p is None or i < int(p["ei"]):
                continue
            s = symbols[si]
            bars_held = i - int(p["ei"])
            p["mfe"] = max(float(p["mfe"]), (float(p["entry"]) - float(s["low"][i])) / max(float(p["risk"]), 1e-12))
            if bars_held >= int(CFG["time_reduce_bars"]) and float(p["mfe"]) > 0:
                p["stop"] = min(float(p["stop"]), float(p["entry"]) + float(p["risk"]) * float(CFG["time_reduce_to_risk_frac"]))
            exit_price = None
            why = None
            if float(s["high"][i]) >= float(p["stop"]):
                exit_price = float(p["stop"])
                why = "stop"
            elif float(s["low"][i]) <= float(p["target"]):
                exit_price = float(p["target"])
                why = "target"
            elif bars_held >= int(CFG["fail_fast_bars"]) and float(p["mfe"]) < float(CFG["fail_fast_min_progress_r"]) and float(s["close"][i]) > float(p["entry"]):
                exit_price = float(s["close"][i])
                why = "fail_fast"
            elif bars_held >= int(CFG["timeout_bars"]):
                exit_price = float(s["close"][i])
                why = "timeout"
            if exit_price is not None:
                r = short_return(float(p["entry"]), float(exit_price))
                pnl = float(p["notional"]) * r
                equity += pnl
                peak = max(peak, equity)
                peak_asset = max(peak_asset, equity)
                mdd = min(mdd, equity / max(peak, 1e-12) - 1.0)
                if pnl > 0:
                    wins += 1
                    gross_profit += pnl
                else:
                    losses += 1
                    gross_loss += -pnl
                trades.append(dict(same_bar=int(p["ets"]) == int(ts), exit_reason=why))
                del active[si]

        # 3. t candle 종료 후 DD brake edge 확정. 다음 timestamp부터 적용한다.
        dd = equity / max(peak, 1e-12) - 1.0
        below = dd <= -float(CFG["dd_brake_trigger_pct"])
        if below and not prev_dd_below:
            freeze = max(freeze, int(CFG["dd_brake_freeze_steps"]))
        prev_dd_below = bool(below)

        # 4. t close 신호 평가 -> t+1 open pending entry 생성.
        for si, i in events.get(ts, []):
            if si in active:
                continue
            p = make_pending(si, symbols[si], i)
            if p is not None:
                pending[p["ets"]].append(p)
                generated += 1

    # 5. train 구간 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.
    for si, p in list(active.items()):
        s = symbols[si]
        i = len(s["ts"]) - 1
        exit_price = float(s["close"][i])
        exit_ts = int(s["ts"][i])
        r = short_return(float(p["entry"]), exit_price)
        pnl = float(p["notional"]) * r
        equity += pnl
        peak = max(peak, equity)
        peak_asset = max(peak_asset, equity)
        mdd = min(mdd, equity / max(peak, 1e-12) - 1.0)
        if pnl > 0:
            wins += 1
            gross_profit += pnl
        else:
            losses += 1
            gross_loss += -pnl
        trades.append(dict(same_bar=int(p["ets"]) == exit_ts, exit_reason="forced_end"))
        del active[si]

    n = len(trades)
    max_return_pct = (peak_asset / float(CFG["initial_asset"]) - 1.0) * 100.0
    max_drawdown_pct = abs(mdd) * 100.0
    return dict(
        strategy=CFG["strategy"],
        baseline_version=CFG["baseline_version"],
        trades=n,
        wins=wins,
        losses=losses,
        win_rate_pct=wins / n * 100.0 if n else 0.0,
        final_asset=equity,
        final_return_pct=(equity / float(CFG["initial_asset"]) - 1.0) * 100.0,
        peak_asset=peak_asset,
        max_return_pct=max_return_pct,
        max_drawdown_pct=max_drawdown_pct,
        official_cd_value=official_cd(max_return_pct, max_drawdown_pct),
        profit_factor=gross_profit / gross_loss if gross_loss > 0 else float("inf"),
        max_conc=max_conc,
        max_conc_unique_symbols=max_conc_unique,
        same_bar_trades=sum(1 for r in trades if r.get("same_bar")),
        active_leftover=len(active),
        pending_leftover=sum(len(v) for v in pending.values()),
        blocked_by_guard=blocked,
        generated_entry_candidates=generated,
        executed_entries=executed,
        fee_per_side=CFG["fee_per_side"],
        position_fraction=CFG["position_fraction"],
        short_dev=CFG["short_dev"],
        short_wick_mult=CFG["short_wick_mult"],
        score_min_short=CFG["score_min_short"],
        rr_mult=CFG["rr_mult"],
        timeout_bars=CFG["timeout_bars"],
        dd_brake_trigger_pct=CFG["dd_brake_trigger_pct"],
        dd_brake_freeze_steps=CFG["dd_brake_freeze_steps"],
    )


def reproduction_gate(result: Dict[str, Any], load_errors: int) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    got = dict(result)
    got["load_errors"] = load_errors
    for k, expected in OFFICIAL_RESULT.items():
        actual = got.get(k)
        if isinstance(expected, float):
            if actual is None or abs(float(actual) - expected) > 1e-6:
                issues.append(f"{k}: got={actual} expected={expected}")
        else:
            if actual != expected:
                issues.append(f"{k}: got={actual} expected={expected}")
    return len(issues) == 0, issues


def has_csv(p: Path) -> bool:
    return p.exists() and p.is_dir() and any(x.suffix.lower() == ".csv" for x in p.glob("*.csv"))


def resolve_data_dir(arg: Optional[str]) -> Path:
    if arg:
        p = Path(arg).expanduser().resolve()
        if not has_csv(p):
            raise FileNotFoundError(f"CSV 데이터 폴더가 아님: {p}")
        return p
    here = Path(__file__).resolve().parent
    candidates = [
        here / "Data" / "time",
        here.parent / "Data" / "time",
        here.parent.parent / "Data" / "time",
        Path.cwd() / "Data" / "time",
        Path.cwd().parent / "Data" / "time",
    ]
    for p in candidates:
        if has_csv(p):
            return p.resolve()
    raise FileNotFoundError("CSV 데이터 폴더를 찾지 못했다. --data-dir로 OHLCV CSV 폴더를 지정해라.")


def main() -> None:
    ap = argparse.ArgumentParser(description="short_main v9 frozen reproduction runner")
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--out-dir", default="./local_results/short_main/SHORT_MAIN_V9_REPRODUCE")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--min-csv-files", type=int, default=100)
    ap.add_argument("--allow-small-data", action="store_true")
    ap.add_argument("--strict-gate", action="store_true")
    ap.add_argument("--progress-every", type=int, default=100)
    args = ap.parse_args()

    data_dir = resolve_data_dir(args.data_dir)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(data_dir.rglob("*.csv") if args.recursive else data_dir.glob("*.csv"))
    if len(files) < int(args.min_csv_files) and not args.allow_small_data:
        raise RuntimeError(f"CSV 파일 수가 너무 적다: {len(files)}개. 실제 OHLCV 폴더인지 확인해라.")

    symbols: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for n, path in enumerate(files, 1):
        try:
            symbols.append(load_symbol(path))
        except Exception as e:
            errors.append(dict(file=str(path), error=repr(e), traceback=traceback.format_exc(limit=1)))
        if args.progress_every and n % int(args.progress_every) == 0:
            print(f"[LOAD] files={n}/{len(files)} loaded_symbols={len(symbols)} load_errors={len(errors)}", flush=True)

    events: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for si, s in enumerate(symbols):
        for i, ts in enumerate(s["ts"]):
            events[int(ts)].append((si, i))
    timeline = sorted(events.keys())

    print("[START] short_main v9 frozen reproduction")
    print("[INFO] data_dir=", data_dir)
    print("[INFO] csv_files=", len(files), "loaded_symbols=", len(symbols), "load_errors=", len(errors), "timeline=", len(timeline))

    result = run_engine(symbols, events, timeline)
    gate_pass, gate_issues = reproduction_gate(result, len(errors))
    result["load_errors"] = len(errors)
    result["reproduction_gate_pass"] = gate_pass
    result["reproduction_issues"] = " | ".join(gate_issues)

    pd.DataFrame([result]).to_csv(out_dir / "short_main_v9_reproduction_summary.csv", index=False, encoding="utf-8-sig")
    (out_dir / "short_main_v9_reproduction_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "short_main_v9_reproduction_errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = dict(
        script="base_line/short_main/v9/frozen_reproduce_runner.py",
        official_result=OFFICIAL_RESULT,
        train_end=str(TRAIN_END),
        holdout_start=str(HOLDOUT_START),
        data_scope="2026 excluded before indicator calculation",
        engine_rules=[
            "t open uses pending entries from t-1 close",
            "t candle exits affect only after entry processing",
            "same timestamp reentry is disabled",
            "same-bar TP/SL is allowed",
            "DD brake applies from next timestamp",
            "active positions are force-closed at train final close",
        ],
        data_dir=str(data_dir),
        csv_files=len(files),
        loaded_symbols=len(symbols),
        load_errors=len(errors),
        reproduction_gate_pass=gate_pass,
        reproduction_issues=gate_issues,
    )
    (out_dir / "short_main_v9_reproduction_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    if gate_pass:
        print("[GATE PASS] short_main v9 official baseline reproduced")
    else:
        print("[GATE FAIL] short_main v9 official baseline mismatch")
        for issue in gate_issues:
            print(" -", issue)
        if args.strict_gate:
            raise RuntimeError("short_main v9 reproduction gate failed")
    print(pd.DataFrame([result]).to_string(index=False))
    print("[DONE]", out_dir / "short_main_v9_reproduction_summary.csv")


if __name__ == "__main__":
    main()
