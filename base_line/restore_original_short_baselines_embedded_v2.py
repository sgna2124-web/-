from __future__ import annotations

"""
숏 기준선 2개 독립 복원 코드
- 외부 runner import 없음
- 외부 json config 참조 없음
- 다른 scripts 경로 참조 없음
- OHLCV CSV 데이터 폴더만 자동 탐색 또는 --data-dir로 지정

실행:
python base_line/restore_original_short_baselines_embedded_v2.py
python base_line/restore_original_short_baselines_embedded_v2.py --data-dir "C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인\\Data\\time"
"""

import argparse, copy, json, math, os, traceback
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

REFERENCE = {
    "short_only_reference_1x": {
        "axis": "short_max",
        "reference_trades": 36505,
        "reference_max_return_pct": 394.614496,
        "reference_max_drawdown_pct": 7.779240,
        "reference_official_cd_value": 456.137449,
    },
    "short_beh_dd_brake": {
        "axis": "short_main",
        "reference_trades": 28017,
        "reference_max_return_pct": 311.812150,
        "reference_max_drawdown_pct": 4.758886,
        "reference_official_cd_value": 392.214469,
    },
}

BASE_CONFIG: Dict[str, Any] = {
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "fee_per_side": 0.0004,
    "min_bars": 120,
    "signal": {
        "ema_period": 20,
        "rsi_period": 14,
        "atr_period": 14,
        "long_dev": 0.028,
        "short_dev": 0.032,
        "long_rsi_max": 25,
        "short_rsi_min": 76,
        "long_wick_mult": 1.2,
        "short_wick_mult": 1.3,
    },
    "quality": {"short_dev": None, "short_rsi_min": None, "short_wick_mult": None},
    "risk": {
        "atr_stop_mult": 1.8975,
        "rr_mult": 6.0,
        "min_expected_tp": 0.003,
        "timeout_bars": 200,
        "fail_fast_bars": 10,
        "fail_fast_min_progress_r": 0.1,
        "time_reduce_bars": 10,
        "time_reduce_to_risk_frac": 0.05,
    },
    "trade_control": {
        "score_min_short": 2.0,
        "score_dev_weight": 1.0,
        "score_rsi_weight": 0.8,
        "score_wick_weight": 0.7,
        "score_dev_cap": 2.0,
        "score_rsi_cap": 2.0,
        "score_wick_cap": 2.5,
        "wick_atr_floor_mult": 0.2,
        "dd_brake_trigger_pct": None,
        "dd_brake_freeze_steps": 0,
    },
}

STRATEGIES = {
    "short_only_reference_1x": {"overrides": {}, "behavioral": False},
    "short_beh_dd_brake": {
        "overrides": {
            "quality": {"short_dev": 0.033, "short_rsi_min": 77},
            "trade_control": {"score_min_short": 2.2, "dd_brake_trigger_pct": 0.03, "dd_brake_freeze_steps": 5},
        },
        "behavioral": True,
    },
}


def deep_merge(a, b):
    x = copy.deepcopy(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(x.get(k), dict):
            x[k] = deep_merge(x[k], v)
        else:
            x[k] = copy.deepcopy(v)
    return x


def ema(a, p):
    return pd.Series(a).ewm(span=p, adjust=False).mean().to_numpy(float)


def rsi(a, p):
    s = pd.Series(a, dtype=float)
    d = s.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    ru = up.ewm(alpha=1 / p, adjust=False).mean()
    rd = dn.ewm(alpha=1 / p, adjust=False).mean()
    rs = ru / rd.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).fillna(50).to_numpy(float)


def atr(h, l, c, p):
    pc = np.roll(c, 1)
    pc[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).ewm(alpha=1 / p, adjust=False).mean().to_numpy(float)


def load_df(path: Path):
    first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
    if first.startswith("version https://git-lfs.github.com/spec/"):
        raise ValueError(f"LFS pointer: {path}")
    raw = pd.read_csv(path, low_memory=False)
    raw.columns = [str(c).strip().replace("\ufeff", "").lower() for c in raw.columns]
    alias = {
        "date": ["date", "datetime", "timestamp", "time", "open_time", "opentime", "candle_date_time_utc", "candle_date_time_kst"],
        "open": ["open", "open_price", "opening_price", "시가"],
        "high": ["high", "high_price", "고가"],
        "low": ["low", "low_price", "저가"],
        "close": ["close", "close_price", "closing_price", "trade_price", "종가"],
        "volume": ["volume", "vol", "base_volume", "candle_acc_trade_volume", "acc_trade_volume", "거래량"],
    }
    mp = {}
    for target, keys in alias.items():
        for k in keys:
            if k in raw.columns:
                mp[k] = target
                break
    df = raw.rename(columns=mp)[["date", "open", "high", "low", "close", "volume"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna().sort_values("date").drop_duplicates("date").reset_index(drop=True)


def score_short(close_i, ema_i, rsi_i, wick_i, body_i, atr_i, dev_thr, rsi_thr, tc):
    raw_dev = max(0.0, close_i / ema_i - 1.0)
    raw_rsi = max(0.0, rsi_i - rsi_thr)
    dev_score = max(0.0, min(raw_dev / max(dev_thr, 1e-12), float(tc["score_dev_cap"])))
    rsi_score = max(0.0, min(raw_rsi / 10.0, float(tc["score_rsi_cap"])))
    denom = max(abs(body_i), atr_i * float(tc["wick_atr_floor_mult"]), 1e-12)
    wick_score = max(0.0, min(math.log1p(max(0.0, wick_i / denom)), float(tc["score_wick_cap"])))
    return float(tc["score_dev_weight"] * dev_score + tc["score_rsi_weight"] * rsi_score + tc["score_wick_weight"] * wick_score)


def trade_return(entry, exitp, fee):
    return entry / exitp - 1.0 - 2 * fee


def gen_trades(symbol, df, cfg):
    s, q, r, tc = cfg["signal"], cfg["quality"], cfg["risk"], cfg["trade_control"]
    fee = float(cfg["fee_per_side"])
    o = df["open"].to_numpy(float); h = df["high"].to_numpy(float); l = df["low"].to_numpy(float); c = df["close"].to_numpy(float)
    ts = pd.to_datetime(df["date"]).astype("int64").to_numpy()
    ema_v = ema(c, int(s["ema_period"])); rsi_v = rsi(c, int(s["rsi_period"])); atr_v = atr(h, l, c, int(s["atr_period"]))
    body = np.abs(c - o); upper = h - np.maximum(o, c)
    sd = float(q["short_dev"] if q.get("short_dev") is not None else s["short_dev"])
    sr = float(q["short_rsi_min"] if q.get("short_rsi_min") is not None else s["short_rsi_min"])
    sw = float(q["short_wick_mult"] if q.get("short_wick_mult") is not None else s["short_wick_mult"])
    asm = float(r["atr_stop_mult"]); rrm = float(r["rr_mult"]); met = float(r["min_expected_tp"])
    timeout = int(r["timeout_bars"]); trb = int(r["time_reduce_bars"]); trf = float(r["time_reduce_to_risk_frac"])
    ff_b = int(r["fail_fast_bars"]); ff_r = float(r["fail_fast_min_progress_r"])
    trades = []; inpos = False; start = max(int(s["ema_period"]), int(s["rsi_period"]), int(s["atr_period"]), 30)
    for i in range(start, len(c) - 1):
        if not inpos:
            sig = (c[i] / ema_v[i] - 1.0) >= sd and rsi_v[i] > sr and upper[i] >= sw * body[i]
            if sig:
                entry = float(o[i + 1])
                stop = float(entry + atr_v[i] * asm)
                target = float(entry - rrm * (stop - entry))
                if stop > entry and (entry - target) / entry >= met:
                    inpos = True; ei = i + 1; ep = entry; sp = stop; tp = target
                    riskv = max(abs(ep - sp), 1e-12); mfe = 0.0
                    sc = score_short(c[i], ema_v[i], rsi_v[i], upper[i], body[i], atr_v[i], sd, sr, tc)
        else:
            prev = max(ei, i - 1)
            mfe = max(mfe, (ep - l[prev]) / riskv)
            if i - ei >= trb and mfe > 0:
                sp = min(sp, ep + riskv * trf)
            exit_p = None
            if h[i] >= sp:
                exit_p = sp
            elif l[i] <= tp:
                exit_p = tp
            elif (i - ei >= ff_b and mfe < ff_r and c[i] > ep) or i - ei >= timeout:
                exit_p = float(c[i])
            if exit_p is not None:
                trades.append({"symbol": symbol, "entry_ts": int(ts[ei]), "exit_ts": int(ts[i]), "return": trade_return(ep, float(exit_p), fee), "score": sc, "side": -1, "same_bar": bool(int(ts[ei]) == int(ts[i]))})
                inpos = False
    return trades


def eval_plain(trades, initial, frac, score_min_short):
    by_e, by_x = {}, {}
    for i, tr in enumerate(trades):
        by_e.setdefault(tr["entry_ts"], []).append(i); by_x.setdefault(tr["exit_ts"], []).append(i)
    equity = peak = peak_asset = float(initial); mdd = gp = gl = 0.0; wins = 0; active = {}; executed = set(); max_conc = max_sym = 0
    for ts in sorted(set(by_e) | set(by_x)):
        for idx in [i for i in by_x.get(ts, []) if trades[i]["entry_ts"] < ts]:
            pos = active.pop(idx, None)
            if pos:
                pnl = pos["notional"] * trades[idx]["return"]; equity += pnl; peak = max(peak, equity); peak_asset = max(peak_asset, equity); mdd = min(mdd, equity / peak - 1.0)
                if pnl > 0: wins += 1; gp += pnl
                else: gl += -pnl
        selected = [i for i in by_e.get(ts, []) if trades[i]["score"] >= score_min_short]
        selected = sorted(selected, key=lambda i: trades[i]["score"], reverse=True)
        for idx in selected:
            active[idx] = {"notional": equity * frac, "symbol": trades[idx]["symbol"]}; executed.add(idx)
        max_conc = max(max_conc, len(active)); max_sym = max(max_sym, len({p["symbol"] for p in active.values()}))
    return finish(equity, peak_asset, mdd, gp, gl, wins, executed, active, trades, max_conc, max_sym, initial)


def eval_behavioral(trades, initial, frac, tc):
    by_e, by_x = {}, {}
    for i, tr in enumerate(trades):
        by_e.setdefault(tr["entry_ts"], []).append(i); by_x.setdefault(tr["exit_ts"], []).append(i)
    equity = peak = peak_asset = float(initial); mdd = gp = gl = 0.0; wins = 0; active = {}; executed = set(); max_conc = max_sym = 0
    dd_freeze_left = 0; prev_dd_below = False; score_min_short = float(tc["score_min_short"])
    for ts in sorted(set(by_e) | set(by_x)):
        for idx in [i for i in by_x.get(ts, []) if trades[i]["entry_ts"] < ts]:
            pos = active.pop(idx, None)
            if pos:
                pnl = pos["notional"] * trades[idx]["return"]; equity += pnl; peak = max(peak, equity); peak_asset = max(peak_asset, equity); mdd = min(mdd, equity / peak - 1.0)
                if pnl > 0: wins += 1; gp += pnl
                else: gl += -pnl
        dd_trig = tc.get("dd_brake_trigger_pct")
        dd_below = dd_trig is not None and equity / peak - 1.0 <= -float(dd_trig)
        if dd_below and not prev_dd_below:
            dd_freeze_left = max(dd_freeze_left, int(tc.get("dd_brake_freeze_steps", 0) or 0))
        prev_dd_below = bool(dd_below)
        selected = [i for i in by_e.get(ts, []) if trades[i]["score"] >= score_min_short]
        if dd_freeze_left > 0:
            dd_freeze_left -= 1; selected = []
        for idx in selected:
            active[idx] = {"notional": equity * frac, "symbol": trades[idx]["symbol"]}; executed.add(idx)
        max_conc = max(max_conc, len(active)); max_sym = max(max_sym, len({p["symbol"] for p in active.values()}))
    return finish(equity, peak_asset, mdd, gp, gl, wins, executed, active, trades, max_conc, max_sym, initial)


def finish(equity, peak_asset, mdd, gp, gl, wins, executed, active, trades, max_conc, max_sym, initial):
    n = len(executed)
    return {"trades": n, "final_asset": equity, "final_return": equity / initial - 1.0, "peak_asset": peak_asset, "peak_growth": peak_asset / initial - 1.0, "win_rate": wins / n if n else 0.0, "pf": gp / gl if gl > 0 else float("inf"), "mdd": mdd, "max_conc": max_conc, "max_conc_unique_symbols": max_sym, "same_bar_trades": sum(1 for tr in trades if tr.get("same_bar")), "active_leftover": len(active)}


def official_cd(max_return_pct, mdd_pct):
    return 100 * (1 - abs(mdd_pct) / 100) * (1 + max_return_pct / 100)


def has_csv(p):
    return p.exists() and p.is_dir() and any(x.suffix.lower() == ".csv" for x in p.glob("*.csv"))


def resolve_data_dir(arg):
    if arg:
        p = Path(arg).expanduser().resolve()
        if not has_csv(p): raise FileNotFoundError(f"CSV 데이터 폴더가 아님: {p}")
        return p
    cwd = Path.cwd().resolve()
    candidates = [
        cwd / "코인" / "Data" / "time",
        cwd.parent / "Data" / "time",
        cwd.parent / "코인" / "Data" / "time",
        cwd.parent.parent / "코인" / "Data" / "time",
        Path(r"C:\Users\user\Desktop\LCD\파이썬\코인\Data\time"),
        cwd / "5m_data",
        cwd / "data",
    ]
    for p in candidates:
        if has_csv(p): return p
    raise FileNotFoundError("데이터 루트 자동 탐색 실패:\n" + "\n".join(str(p) for p in candidates))


def run_one(name, data_dir, out_dir, save_trades=False):
    meta = STRATEGIES[name]; cfg = deep_merge(BASE_CONFIG, meta["overrides"]); trades = []; errors = []
    for p in sorted(data_dir.glob("*.csv")):
        try:
            df = load_df(p)
            if len(df) >= int(cfg["min_bars"]): trades.extend(gen_trades(p.stem, df, cfg))
        except Exception as e:
            errors.append({"file": str(p), "error": repr(e)})
    if meta["behavioral"]:
        s = eval_behavioral(trades, cfg["initial_asset"], cfg["position_fraction"], cfg["trade_control"])
    else:
        s = eval_plain(trades, cfg["initial_asset"], cfg["position_fraction"], float(cfg["trade_control"]["score_min_short"]))
    max_ret = s["peak_growth"] * 100; mdd = abs(s["mdd"]) * 100
    rep = {"strategy": name, "axis": REFERENCE[name]["axis"], "trades": s["trades"], "reference_trades": REFERENCE[name]["reference_trades"], "trade_diff": s["trades"] - REFERENCE[name]["reference_trades"], "final_return_pct": s["final_return"] * 100, "max_return_pct": max_ret, "reference_max_return_pct": REFERENCE[name]["reference_max_return_pct"], "max_drawdown_pct": mdd, "reference_max_drawdown_pct": REFERENCE[name]["reference_max_drawdown_pct"], "official_cd_value": official_cd(max_ret, mdd), "reference_official_cd_value": REFERENCE[name]["reference_official_cd_value"], "win_rate": s["win_rate"], "pf": s["pf"], "max_conc": s["max_conc"], "same_bar_trades": s["same_bar_trades"], "errors": len(errors)}
    d = out_dir / name; d.mkdir(parents=True, exist_ok=True)
    (d / "summary.json").write_text(json.dumps({**s, "effective_config": cfg, "reference_compare": rep, "errors": errors}, ensure_ascii=False, indent=2), encoding="utf-8")
    if save_trades: pd.DataFrame(trades).to_csv(d / "trades.csv", index=False, encoding="utf-8-sig")
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--out-dir", default="RESTORE_ORIGINAL_SHORT_BASELINES_EMBEDDED")
    ap.add_argument("--strategy", choices=["short_only_reference_1x", "short_beh_dd_brake", "all"], default="all")
    ap.add_argument("--save-trades", action="store_true")
    args = ap.parse_args()
    data_dir = resolve_data_dir(args.data_dir); out_dir = Path(args.out_dir).expanduser().resolve(); out_dir.mkdir(parents=True, exist_ok=True)
    targets = ["short_only_reference_1x", "short_beh_dd_brake"] if args.strategy == "all" else [args.strategy]
    print(f"[LAUNCH_CWD] {Path.cwd().resolve()}"); print(f"[DATA_ROOT] {data_dir}"); print(f"[RESULTS_DIR] {out_dir}"); print(f"[CSV_FILES] {len(list(data_dir.glob('*.csv')))}")
    rows = []
    for t in targets:
        try:
            r = run_one(t, data_dir, out_dir, args.save_trades); rows.append(r); print(json.dumps(r, ensure_ascii=False, indent=2))
        except Exception as e:
            rows.append({"strategy": t, "error": repr(e), "traceback": traceback.format_exc()})
    pd.DataFrame(rows).to_csv(out_dir / "restore_short_baselines_registry.csv", index=False, encoding="utf-8-sig")
    (out_dir / "restore_short_baselines_registry.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
