from __future__ import annotations

"""
FROZEN REPRODUCE RUNNER - short_max v7

이 파일은 공식 기준선 재현용 완전 실행 러너다.
strategy_code.py만 복사하지 말고, 처음 재현할 때는 이 파일을 실행한다.

실행 예:
python frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time"

결과 폴더:
현재 파일 위치/short_max_v7_frozen_reproduce_results
"""

import argparse
import json
import math
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


REF: Dict[str, Any] = {
    "strategy": "short_max_v7_devw120",
    "axis": "short_max",
    "trades": 43681,
    "final_return_pct": 1221.3299878755902,
    "max_return_pct": 1221.9746135454966,
    "max_drawdown_pct": 5.6636954922983485,
    "official_cd_value": 1247.1019969487918,
    "win_rate_pct": 13.827522263684438,
    "profit_factor": 1.5021526593629504,
    "max_conc": 295,
    "max_conc_unique_symbols": 295,
    "same_bar_trades": 3694,
    "active_leftover": 0,
    "generated_trades_before_score_filter": 43833,
    "errors": 0,
}

CFG: Dict[str, Any] = {
    "strategy_name": "short_max_v7_devw120",
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "fee_per_side": 0.0004,
    "min_bars": 120,
    "ema_period": 20,
    "rsi_period": 14,
    "atr_period": 14,
    "short_dev": 0.035,
    "short_rsi_min": 77.0,
    "use_rsi_gate": False,
    "short_wick_mult": 1.3,
    "score_min_short": 2.35,
    "score_dev_weight": 1.2,
    "score_rsi_weight": 0.8,
    "score_wick_weight": 0.7,
    "score_dev_cap": 2.0,
    "score_rsi_cap": 2.0,
    "score_wick_cap": 2.5,
    "wick_atr_floor_mult": 0.2,
    "atr_stop_mult": 1.8975,
    "rr_mult": 5.75,
    "min_expected_tp": 0.003,
    "timeout_bars": 200,
    "time_reduce_bars": 8,
    "time_reduce_to_risk_frac": 0.05,
    "fail_fast_bars": 10,
    "fail_fast_min_progress_r": 0.1,
    "dd_brake_trigger_pct": 0.03,
    "dd_brake_freeze_steps": 5,
    "dd_brake_mode": "edge_current",
}


def ema(a, p):
    return pd.Series(a, dtype=float).ewm(span=int(p), adjust=False).mean().to_numpy(float)


def rsi(a, p):
    s = pd.Series(a, dtype=float)
    d = s.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    ru = up.ewm(alpha=1 / int(p), adjust=False).mean()
    rd = dn.ewm(alpha=1 / int(p), adjust=False).mean()
    rs = ru / rd.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).to_numpy(float)


def atr(h, l, c, p):
    pc = np.roll(c, 1)
    pc[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr, dtype=float).ewm(alpha=1 / int(p), adjust=False).mean().to_numpy(float)


def load_df(path: Path) -> pd.DataFrame:
    first = path.read_text(encoding="utf-8", errors="ignore")[:80]
    if first.startswith("version https://git-lfs.github.com/spec/"):
        raise ValueError(f"LFS pointer file: {path}")
    raw = pd.read_csv(path, low_memory=False)
    raw.columns = [str(c).strip().replace("\ufeff", "").lower() for c in raw.columns]
    aliases = {
        "date": ["date", "datetime", "timestamp", "time", "open_time", "opentime", "candle_date_time_utc", "candle_date_time_kst"],
        "open": ["open", "open_price", "opening_price", "시가"],
        "high": ["high", "high_price", "고가"],
        "low": ["low", "low_price", "저가"],
        "close": ["close", "close_price", "closing_price", "trade_price", "종가"],
        "volume": ["volume", "vol", "base_volume", "candle_acc_trade_volume", "acc_trade_volume", "거래량"],
    }
    mp = {}
    for target, keys in aliases.items():
        hit = next((k for k in keys if k in raw.columns), None)
        if hit is None:
            raise ValueError(f"missing required column group: {target}")
        mp[hit] = target
    df = raw.rename(columns=mp)[["date", "open", "high", "low", "close", "volume"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna().sort_values("date").drop_duplicates("date").reset_index(drop=True)


def score_short(close_i, ema_i, rsi_i, upper_i, body_i, atr_i, cfg):
    raw_dev = max(0.0, close_i / max(ema_i, 1e-12) - 1.0)
    raw_rsi = max(0.0, rsi_i - cfg["short_rsi_min"])
    dev_score = max(0.0, min(raw_dev / max(cfg["short_dev"], 1e-12), cfg["score_dev_cap"]))
    rsi_score = max(0.0, min(raw_rsi / 10.0, cfg["score_rsi_cap"]))
    floor = max(abs(body_i), atr_i * cfg["wick_atr_floor_mult"], 1e-12)
    wick_score = max(0.0, min(math.log1p(max(0.0, upper_i / floor)), cfg["score_wick_cap"]))
    return float(cfg["score_dev_weight"] * dev_score + cfg["score_rsi_weight"] * rsi_score + cfg["score_wick_weight"] * wick_score)


def trade_return(entry, exitp, fee):
    return entry / max(exitp, 1e-12) - 1.0 - 2.0 * fee


def gen_trades(symbol: str, df: pd.DataFrame, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    ts = pd.to_datetime(df["date"]).astype("int64").to_numpy()
    ema_v = ema(c, cfg["ema_period"])
    rsi_v = rsi(c, cfg["rsi_period"])
    atr_v = atr(h, l, c, cfg["atr_period"])
    body = np.abs(c - o)
    upper = h - np.maximum(o, c)
    trades: List[Dict[str, Any]] = []
    inpos = False
    start = max(int(cfg["ema_period"]), int(cfg["rsi_period"]), int(cfg["atr_period"]), 30)
    for i in range(start, len(c) - 1):
        if not inpos:
            sc = score_short(c[i], ema_v[i], rsi_v[i], upper[i], body[i], atr_v[i], cfg)
            dev_ok = (c[i] / max(ema_v[i], 1e-12) - 1.0) >= cfg["short_dev"]
            rsi_ok = (rsi_v[i] > cfg["short_rsi_min"]) if bool(cfg["use_rsi_gate"]) else True
            wick_ok = upper[i] >= cfg["short_wick_mult"] * body[i]
            score_ok = sc >= cfg["score_min_short"]
            if dev_ok and rsi_ok and wick_ok and score_ok:
                entry = float(o[i + 1])
                stop = float(entry + atr_v[i] * cfg["atr_stop_mult"])
                target = float(entry - cfg["rr_mult"] * (stop - entry))
                # 공식 재현 규칙: expected_tp만 필수 검증한다. target > 0 같은 임의 필터 금지.
                if (entry - target) / max(entry, 1e-12) >= cfg["min_expected_tp"]:
                    inpos = True
                    ei = i + 1
                    ep = entry
                    sp = stop
                    tp = target
                    risk = max(abs(ep - sp), 1e-12)
                    mfe = 0.0
                    score_at_entry = sc
        else:
            mfe = max(mfe, (ep - l[i]) / risk)
            if i - ei >= cfg["time_reduce_bars"] and mfe > 0:
                sp = min(sp, ep + risk * cfg["time_reduce_to_risk_frac"])
            exit_p = None
            reason = None
            if h[i] >= sp:
                exit_p = sp
                reason = "stop"
            elif l[i] <= tp:
                exit_p = tp
                reason = "target"
            elif (i - ei >= cfg["fail_fast_bars"] and mfe < cfg["fail_fast_min_progress_r"] and c[i] > ep) or i - ei >= cfg["timeout_bars"]:
                exit_p = float(c[i])
                reason = "fail_fast_or_timeout"
            if exit_p is not None:
                trades.append({
                    "symbol": symbol,
                    "entry_ts": int(ts[ei]),
                    "exit_ts": int(ts[i]),
                    "return": trade_return(ep, float(exit_p), cfg["fee_per_side"]),
                    "score": score_at_entry,
                    "side": -1,
                    "same_bar": bool(int(ts[ei]) == int(ts[i])),
                    "exit_reason": reason,
                })
                inpos = False
    return trades


def eval_portfolio(trades: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    by_e: Dict[int, List[int]] = {}
    by_x: Dict[int, List[int]] = {}
    for i, tr in enumerate(trades):
        by_e.setdefault(tr["entry_ts"], []).append(i)
        by_x.setdefault(tr["exit_ts"], []).append(i)
    initial = float(cfg["initial_asset"])
    frac = float(cfg["position_fraction"])
    equity = peak = peak_asset = initial
    mdd = gp = gl = 0.0
    wins = 0
    active: Dict[int, Dict[str, Any]] = {}
    executed = set()
    max_conc = max_sym = 0
    dd_freeze_left = 0
    prev_dd_below = False
    blocked = 0

    def close_idx(idx: int):
        nonlocal equity, peak, peak_asset, mdd, gp, gl, wins
        pos = active.pop(idx, None)
        if pos is None:
            return
        pnl = pos["notional"] * trades[idx]["return"]
        equity += pnl
        peak = max(peak, equity)
        peak_asset = max(peak_asset, equity)
        mdd = min(mdd, equity / peak - 1.0)
        if pnl > 0:
            wins += 1
            gp += pnl
        else:
            gl += -pnl

    for ts in sorted(set(by_e) | set(by_x)):
        for idx in [i for i in by_x.get(ts, []) if trades[i]["entry_ts"] < ts]:
            close_idx(idx)

        dd_now = equity / peak - 1.0
        dd_below = dd_now <= -float(cfg["dd_brake_trigger_pct"])
        if dd_below and not prev_dd_below:
            dd_freeze_left = max(dd_freeze_left, int(cfg["dd_brake_freeze_steps"]))
        prev_dd_below = bool(dd_below)

        selected = [i for i in by_e.get(ts, []) if trades[i]["score"] >= cfg["score_min_short"]]
        selected = sorted(selected, key=lambda i: trades[i]["score"], reverse=True)

        if dd_freeze_left > 0:
            blocked += len(selected)
            selected = []
            dd_freeze_left -= 1

        for idx in selected:
            active[idx] = {"notional": equity * frac, "symbol": trades[idx]["symbol"]}
            executed.add(idx)

        for idx in selected:
            if idx in active and trades[idx]["exit_ts"] == ts:
                close_idx(idx)

        max_conc = max(max_conc, len(active))
        max_sym = max(max_sym, len({p["symbol"] for p in active.values()}))

    n = len(executed)
    return {
        "trades": n,
        "final_asset": equity,
        "final_return_pct": (equity / initial - 1.0) * 100.0,
        "peak_asset": peak_asset,
        "max_return_pct": (peak_asset / initial - 1.0) * 100.0,
        "max_drawdown_pct": abs(mdd) * 100.0,
        "win_rate_pct": (wins / n * 100.0) if n else 0.0,
        "profit_factor": gp / gl if gl > 0 else float("inf"),
        "max_conc": max_conc,
        "max_conc_unique_symbols": max_sym,
        "same_bar_trades": sum(1 for tr in trades if tr.get("same_bar")),
        "active_leftover": len(active),
        "blocked_by_guard": blocked,
        "generated_trades_before_score_filter": len(trades),
        "dd_brake_mode": cfg["dd_brake_mode"],
    }


def official_cd(max_return_pct: float, mdd_pct: float) -> float:
    return 100.0 * (1.0 - abs(mdd_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def has_csv(p: Path) -> bool:
    return p.exists() and p.is_dir() and any(x.suffix.lower() == ".csv" for x in p.glob("*.csv"))


def resolve_data_dir(arg: Optional[str]) -> Path:
    if arg:
        p = Path(arg).expanduser().resolve()
        if not has_csv(p):
            raise FileNotFoundError(f"CSV 데이터 폴더가 아님: {p}")
        return p
    here = Path(__file__).resolve().parent
    candidates = [here / "Data" / "time", here / "data" / "time", here.parent / "Data" / "time", here.parent / "data" / "time", here / "코인" / "Data" / "time", here.parent / "코인" / "Data" / "time"]
    for p in candidates:
        if has_csv(p):
            return p.resolve()
    raise FileNotFoundError("데이터 폴더 자동 탐색 실패. --data-dir로 OHLCV CSV 폴더를 지정해라.")


def list_csv_files(data_dir: Path, recursive: bool, limit_files: Optional[int]) -> List[Path]:
    files = sorted(data_dir.rglob("*.csv") if recursive else data_dir.glob("*.csv"))
    if limit_files is not None:
        files = files[:int(limit_files)]
    if not files:
        raise FileNotFoundError(f"CSV 파일 없음: {data_dir}")
    return files


def baseline_gate(row: Dict[str, Any]) -> str:
    checks = [
        ("trades", abs(int(row["trades"]) - REF["trades"]), 0),
        ("max_return_pct", abs(float(row["max_return_pct"]) - REF["max_return_pct"]), 1e-6),
        ("max_drawdown_pct", abs(float(row["max_drawdown_pct"]) - REF["max_drawdown_pct"]), 1e-6),
        ("official_cd_value", abs(float(row["official_cd_value"]) - REF["official_cd_value"]), 1e-6),
        ("active_leftover", int(row["active_leftover"]), 0),
        ("errors", int(row["errors"]), 0),
    ]
    ok = True
    lines = ["BASELINE GATE - short_max v7 frozen_reproduce_runner"]
    for name, diff, tol in checks:
        passed = diff <= tol
        ok = ok and passed
        lines.append(f"{name}: value={row.get(name)} ref={REF.get(name)} diff={diff} tolerance={tol} pass={passed}")
    lines.append(f"gate_pass={ok}")
    if not ok:
        lines.append("FAIL: 후보 개발 금지. 기준선 재현부터 수정해야 한다.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--limit-files", type=int, default=None)
    ap.add_argument("--min-csv-files", type=int, default=100)
    ap.add_argument("--allow-small-data", action="store_true")
    ap.add_argument("--save-trades", action="store_true")
    ap.add_argument("--skip-baseline-gate", action="store_true")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    data_dir = resolve_data_dir(args.data_dir)
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else (script_dir / "short_max_v7_frozen_reproduce_results").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    files = list_csv_files(data_dir, args.recursive, args.limit_files)
    if len(files) < int(args.min_csv_files) and not args.allow_small_data:
        raise RuntimeError(f"CSV 파일 수가 너무 적다: {len(files)}개. 실제 OHLCV 폴더를 지정해라.")

    trades: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    print(f"FROZEN REPRODUCE short_max v7 | csv_files={len(files)} | data_dir={data_dir}")
    for n, path in enumerate(files, start=1):
        try:
            df = load_df(path)
            if len(df) >= int(CFG["min_bars"]):
                trades.extend(gen_trades(path.stem, df, CFG))
        except Exception as e:
            errors.append({"file": str(path), "error": repr(e), "traceback": traceback.format_exc(limit=1)})
        if n % 50 == 0:
            print(f"[PROGRESS] files={n}/{len(files)} generated_trades={len(trades)} errors={len(errors)}", flush=True)

    row = eval_portfolio(trades, CFG)
    row["strategy"] = CFG["strategy_name"]
    row["axis"] = REF["axis"]
    row["official_cd_value"] = official_cd(row["max_return_pct"], row["max_drawdown_pct"])
    row["errors"] = len(errors)
    row["fee_per_side"] = CFG["fee_per_side"]
    row["position_fraction"] = CFG["position_fraction"]
    row["score_dev_weight"] = CFG["score_dev_weight"]
    row["timeout_bars"] = CFG["timeout_bars"]

    meta = {
        "reference": REF,
        "config": CFG,
        "csv_files": len(files),
        "data_dir": str(data_dir),
        "runtime_external_path_reference": False,
        "source_of_truth": "base_line/short_max/v7/frozen_reproduce_runner.py",
        "critical_rules": ["current equity * 0.01 sizing", "fee_per_side 0.0004", "next-bar open", "RSI direct gate false", "score_min_short in entry mask", "expected_tp only, no target>0 filter", "same-bar immediate close", "dd_brake edge_current"],
    }
    (out_dir / "run_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame([row]).to_csv(out_dir / "summary_compact.csv", index=False, encoding="utf-8-sig")
    (out_dir / "summary.json").write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    gate_text = baseline_gate(row)
    (out_dir / "baseline_gate.txt").write_text(gate_text, encoding="utf-8")
    if errors:
        (out_dir / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.save_trades:
        pd.DataFrame(trades).to_csv(out_dir / "generated_trades.csv", index=False, encoding="utf-8-sig")
    print(gate_text)
    print(f"saved: {out_dir}")
    if "gate_pass=True" not in gate_text and not args.skip_baseline_gate:
        raise RuntimeError("baseline gate failed. short_max v7 기준선 재현 실패.")


if __name__ == "__main__":
    main()
