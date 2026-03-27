from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "test8" / "2026-03-24" / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from common_indicators import ema, rsi, atr, candle_features  # noqa: E402

BASE_CONFIG_PATH = ROOT / "experiments" / "base_config_json_only_timeout18_split_entry.json"
SINGLE_CHANGES_PATH = ROOT / "experiments" / "combinations_json_only_timeout18_split_entry.json"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def deep_merge(base: dict, overrides: dict) -> dict:
    merged = copy.deepcopy(base)
    for k, v in overrides.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = copy.deepcopy(v)
    return merged


def build_experiments(base_config: dict, experiment_group: dict) -> list[dict]:
    experiments = []
    for exp in experiment_group.get("experiments", []):
        if not exp.get("enabled", False):
            continue
        effective_config = deep_merge(base_config, exp.get("overrides", {}))
        experiments.append(
            {
                "name": exp["name"],
                "description": exp.get("description", ""),
                "effective_config": effective_config,
            }
        )
    return experiments


def load_symbol_df(path: Path) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        first_line = f.readline().strip()
    if first_line.startswith("version https://git-lfs.github.com/spec/"):
        raise ValueError(
            f"{path.name} 는 실제 CSV가 아니라 Git LFS 포인터 파일입니다. repo-assets workflow에서는 DATA_DIR 경로의 실제 csv를 읽어야 합니다."
        )

    alias_map = {
        "date": ["date", "datetime", "timestamp", "time", "open_time", "opentime", "candle_date_time_utc", "candle_date_time_kst"],
        "open": ["open", "open_price", "opening_price", "시가"],
        "high": ["high", "high_price", "고가"],
        "low": ["low", "low_price", "저가"],
        "close": ["close", "close_price", "closing_price", "trade_price", "종가"],
        "volume": ["volume", "vol", "base_volume", "candle_acc_trade_volume", "acc_trade_volume", "거래량"],
    }

    raw = pd.read_csv(path)
    raw.columns = [str(c).strip().replace("\ufeff", "").lower() for c in raw.columns]
    rename_map = {}
    for target, aliases in alias_map.items():
        found = None
        for alias in aliases:
            alias = alias.lower()
            if alias in raw.columns:
                found = alias
                break
        if found is None:
            raise ValueError(f"{path.name} 컬럼 매핑 실패. 현재 컬럼: {list(raw.columns)}")
        rename_map[found] = target

    df = raw.rename(columns=rename_map)[["date", "open", "high", "low", "close", "volume"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "open", "high", "low", "close", "volume"])
    df = df.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    return df


def trade_return_cfg(entry: float, exit_price: float, side: int, fee_per_side: float) -> float:
    gross = (exit_price / entry - 1.0) if side == 1 else (entry / exit_price - 1.0)
    return gross - (2.0 * fee_per_side)


def evaluate_trades_cfg(trades: list[tuple[int, int, float, float]], base_position_fraction: float) -> dict:
    trades = sorted(trades, key=lambda x: x[0])
    eq = 1.0
    peak = 1.0
    peak_asset = 1.0
    mdd = 0.0
    wins = 0
    gp = 0.0
    gl = 0.0
    for _, _, r, frac in trades:
        eq *= (1.0 + base_position_fraction * frac * r)
        peak_asset = max(peak_asset, eq)
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1.0)
        weighted_r = frac * r
        if weighted_r > 0:
            wins += 1
            gp += weighted_r
        else:
            gl += -weighted_r
    if trades:
        ent = np.array([x[0] for x in trades], dtype=np.int64)
        exi = np.array([x[1] for x in trades], dtype=np.int64)
        times = np.concatenate([ent, exi])
        delta = np.concatenate([np.ones_like(ent), -np.ones_like(exi)])
        order = np.lexsort((1 - delta, times))
        cur = 0
        mx = 0
        for d in delta[order]:
            cur += int(d)
            mx = max(mx, cur)
    else:
        mx = 0
    return {
        "trades": len(trades),
        "final_asset": float(eq),
        "final_return": float(eq - 1.0),
        "peak_asset": float(peak_asset),
        "peak_growth": float(peak_asset - 1.0),
        "win_rate": float(wins / len(trades)) if trades else 0.0,
        "pf": float(gp / gl) if gl > 0 else float("inf"),
        "mdd": float(mdd),
        "max_conc": int(mx),
    }


def find_limit_fill(side: int, start_idx: int, end_idx: int, limit_price: float, o: np.ndarray, h: np.ndarray, l: np.ndarray) -> tuple[int, float] | None:
    for j in range(start_idx, min(end_idx + 1, len(o))):
        if side == 1:
            if o[j] <= limit_price:
                return j, float(o[j])
            if l[j] <= limit_price <= h[j]:
                return j, float(limit_price)
        else:
            if o[j] >= limit_price:
                return j, float(o[j])
            if l[j] <= limit_price <= h[j]:
                return j, float(limit_price)
    return None


def run_symbol(df: pd.DataFrame, config: dict) -> list[tuple[int, int, float, float, str]]:
    signal_cfg = config["signal"]
    risk_cfg = config["risk"]
    trade_control_cfg = config["trade_control"]
    exec_cfg = config["execution"]
    entry_refine_cfg = config.get("entry_refine", {})
    fee_per_side = float(config["fee_per_side"])

    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    t = pd.to_datetime(df["date"]).astype("int64").to_numpy()

    ema_period = int(signal_cfg["ema_period"])
    rsi_period = int(signal_cfg["rsi_period"])
    atr_period = int(signal_cfg["atr_period"])

    ema_v = ema(c, ema_period)
    rsi_v = rsi(c, rsi_period)
    atr_v = atr(h, l, c, atr_period)
    feat = candle_features(o, h, l, c)

    min_expected_tp = float(risk_cfg["min_expected_tp"])
    atr_stop_mult = float(risk_cfg["atr_stop_mult"])
    rr_mult = float(risk_cfg["rr_mult"])
    timeout_bars = int(risk_cfg["timeout_bars"])
    cooldown_bars = int(trade_control_cfg["cooldown_bars_same_symbol_same_side"])

    allow_long = bool(exec_cfg["allow_long"])
    allow_short = bool(exec_cfg["allow_short"])

    long_dev = float(signal_cfg["long_dev"])
    short_dev = float(signal_cfg["short_dev"])
    long_rsi_max = float(signal_cfg["long_rsi_max"])
    short_rsi_min = float(signal_cfg["short_rsi_min"])
    long_wick_mult = float(signal_cfg["long_wick_mult"])
    short_wick_mult = float(signal_cfg["short_wick_mult"])

    mode = str(entry_refine_cfg.get("mode", "none"))
    first_fraction = float(entry_refine_cfg.get("first_fraction") or 1.0)
    second_fraction = float(entry_refine_cfg.get("second_fraction") or 0.0)
    second_mode = entry_refine_cfg.get("second_mode")
    retrace_atr_mult = entry_refine_cfg.get("retrace_atr_mult")
    wick_retrace_frac = entry_refine_cfg.get("wick_retrace_frac")
    second_fill_window_bars = int(entry_refine_cfg.get("second_fill_window_bars") or 1)

    trades: list[tuple[int, int, float, float, str]] = []
    open_legs: list[dict] = []
    last_exit_idx = {1: -10_000_000, -1: -10_000_000}
    start_idx = max(ema_period, rsi_period, atr_period, 30)

    for i in range(start_idx, len(c) - 1):
        if open_legs:
            remaining = []
            for leg in open_legs:
                side = leg["side"]
                exit_p = None
                if side == 1:
                    if l[i] <= leg["sp"]:
                        exit_p = leg["sp"]
                    elif h[i] >= leg["tp"]:
                        exit_p = leg["tp"]
                    elif i - leg["ei"] >= timeout_bars:
                        exit_p = c[i]
                else:
                    if h[i] >= leg["sp"]:
                        exit_p = leg["sp"]
                    elif l[i] <= leg["tp"]:
                        exit_p = leg["tp"]
                    elif i - leg["ei"] >= timeout_bars:
                        exit_p = c[i]
                if exit_p is not None:
                    ret = trade_return_cfg(leg["ep"], float(exit_p), side, fee_per_side)
                    trades.append((int(t[leg["ei"]]), int(t[i]), float(ret), float(leg["frac"]), "long" if side == 1 else "short"))
                    last_exit_idx[side] = i
                else:
                    remaining.append(leg)
            open_legs = remaining
            if open_legs:
                continue

        long_cooldown_ok = (i - last_exit_idx[1]) > cooldown_bars
        short_cooldown_ok = (i - last_exit_idx[-1]) > cooldown_bars

        long_sig = (
            allow_long
            and long_cooldown_ok
            and ((c[i] / ema_v[i]) - 1.0) <= -long_dev
            and rsi_v[i] < long_rsi_max
            and feat["lower_wick"][i] >= long_wick_mult * feat["body"][i]
        )
        short_sig = (
            allow_short
            and short_cooldown_ok
            and ((c[i] / ema_v[i]) - 1.0) >= short_dev
            and rsi_v[i] > short_rsi_min
            and feat["upper_wick"][i] >= short_wick_mult * feat["body"][i]
        )

        if not (long_sig or short_sig):
            continue

        side = 1 if long_sig else -1
        signal_high = h[i]
        signal_low = l[i]
        signal_close = c[i]
        signal_atr = atr_v[i]

        candidate_legs = []

        if first_fraction > 0:
            entry_idx = i + 1
            entry = float(o[entry_idx])
            if side == 1:
                stop = min(signal_low, entry - signal_atr * atr_stop_mult)
                ema_target = ema_v[i]
                r_target = entry + rr_mult * (entry - stop)
                target = min(ema_target, r_target) if ema_target > entry else r_target
                if entry > stop and (target - entry) / entry >= min_expected_tp:
                    candidate_legs.append({"side": side, "ei": entry_idx, "ep": entry, "sp": float(stop), "tp": float(target), "frac": first_fraction})
            else:
                stop = max(signal_high, entry + signal_atr * atr_stop_mult)
                ema_target = ema_v[i]
                r_target = entry - rr_mult * (stop - entry)
                target = max(ema_target, r_target) if ema_target < entry else r_target
                if stop > entry and (entry - target) / entry >= min_expected_tp:
                    candidate_legs.append({"side": side, "ei": entry_idx, "ep": entry, "sp": float(stop), "tp": float(target), "frac": first_fraction})

        if mode == "split_entry" and second_fraction > 0 and second_mode is not None:
            fill = None
            if side == 1:
                if second_mode == "atr_pullback":
                    limit_price = float(signal_close - float(retrace_atr_mult) * signal_atr)
                else:
                    wick = max(min(o[i], c[i]) - l[i], 0.0)
                    limit_price = float(signal_close - float(wick_retrace_frac) * wick)
                fill = find_limit_fill(1, i + 1, i + second_fill_window_bars, limit_price, o, h, l)
            else:
                if second_mode == "atr_pullback":
                    limit_price = float(signal_close + float(retrace_atr_mult) * signal_atr)
                else:
                    wick = max(h[i] - max(o[i], c[i]), 0.0)
                    limit_price = float(signal_close + float(wick_retrace_frac) * wick)
                fill = find_limit_fill(-1, i + 1, i + second_fill_window_bars, limit_price, o, h, l)

            if fill is not None:
                entry_idx, entry = fill
                if side == 1:
                    stop = min(signal_low, entry - signal_atr * atr_stop_mult)
                    ema_target = ema_v[i]
                    r_target = entry + rr_mult * (entry - stop)
                    target = min(ema_target, r_target) if ema_target > entry else r_target
                    if entry > stop and (target - entry) / entry >= min_expected_tp:
                        candidate_legs.append({"side": side, "ei": int(entry_idx), "ep": float(entry), "sp": float(stop), "tp": float(target), "frac": second_fraction})
                else:
                    stop = max(signal_high, entry + signal_atr * atr_stop_mult)
                    ema_target = ema_v[i]
                    r_target = entry - rr_mult * (stop - entry)
                    target = max(ema_target, r_target) if ema_target < entry else r_target
                    if stop > entry and (entry - target) / entry >= min_expected_tp:
                        candidate_legs.append({"side": side, "ei": int(entry_idx), "ep": float(entry), "sp": float(stop), "tp": float(target), "frac": second_fraction})

        if candidate_legs:
            open_legs = candidate_legs

    last_i = len(c) - 1
    for leg in open_legs:
        ret = trade_return_cfg(leg["ep"], float(c[last_i]), leg["side"], fee_per_side)
        trades.append((int(t[leg["ei"]]), int(t[last_i]), float(ret), float(leg["frac"]), "long" if leg["side"] == 1 else "short"))

    return trades


def run_single_experiment(experiment: dict) -> dict:
    exp_name = experiment["name"]
    cfg = experiment["effective_config"]
    data_dir = Path(os.environ.get("DATA_DIR", str(ROOT / cfg["data_dir"])))
    result_dir = ROOT / cfg["results_dir"] / exp_name
    result_dir.mkdir(parents=True, exist_ok=True)

    min_bars = int(cfg["min_bars"])
    position_fraction = float(cfg["position_fraction"])
    all_trades: list[tuple[int, int, float, float]] = []
    trade_rows = []
    symbol_rows = []

    top_n = cfg["trade_control"].get("top_n_per_timestamp")
    if top_n is not None:
        raise NotImplementedError("top_n_per_timestamp는 현재 구조에서 지원하지 않습니다.")

    for csv_path in sorted(data_dir.glob("*.csv")):
        print(f"loading: {csv_path.name}")
        df = load_symbol_df(csv_path)
        if len(df) < min_bars:
            continue
        symbol_trades = run_symbol(df, cfg)
        all_trades.extend((en, ex, ret, frac) for en, ex, ret, frac, _ in symbol_trades)

        wins = sum(1 for _, _, r, frac, _ in symbol_trades if frac * r > 0)
        losses = sum(1 for _, _, r, frac, _ in symbol_trades if frac * r <= 0)
        gp = sum(frac * r for _, _, r, frac, _ in symbol_trades if frac * r > 0)
        gl = -sum(frac * r for _, _, r, frac, _ in symbol_trades if frac * r <= 0)
        symbol_rows.append(
            {
                "symbol": csv_path.stem,
                "bars": len(df),
                "trades": len(symbol_trades),
                "wins": wins,
                "losses": losses,
                "win_rate": (wins / len(symbol_trades)) if symbol_trades else 0.0,
                "pf": (gp / gl) if gl > 0 else None,
                "sum_r": sum(frac * r for _, _, r, frac, _ in symbol_trades),
            }
        )
        for en, ex, ret, frac, side in symbol_trades:
            trade_rows.append({"symbol": csv_path.stem, "entry_ts": en, "exit_ts": ex, "ret": ret, "fraction": frac, "side": side})

    summary = evaluate_trades_cfg(all_trades, position_fraction)
    summary["strategy"] = f"{cfg['strategy_name']}_{exp_name}"
    summary["experiment_name"] = exp_name
    summary["initial_asset"] = float(cfg["initial_asset"])
    summary["position_fraction"] = float(cfg["position_fraction"])
    summary["fee_per_side"] = float(cfg["fee_per_side"])
    summary["symbols"] = len(symbol_rows)
    summary["effective_config"] = cfg

    trades_df = pd.DataFrame(trade_rows)
    if not trades_df.empty:
        trades_df = trades_df.sort_values(["entry_ts", "symbol"])
    by_symbol_df = pd.DataFrame(symbol_rows)
    if not by_symbol_df.empty:
        by_symbol_df = by_symbol_df.sort_values(["trades", "sum_r"], ascending=[False, False])
    trades_df.to_csv(result_dir / "trades.csv", index=False)
    by_symbol_df.to_csv(result_dir / "by_symbol.csv", index=False)
    with open(result_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main() -> None:
    base_config = load_json(BASE_CONFIG_PATH)
    experiment_group = load_json(SINGLE_CHANGES_PATH)
    experiments = build_experiments(base_config, experiment_group)
    all_rows = []
    for experiment in experiments:
        print(f"running experiment: {experiment['name']}")
        summary = run_single_experiment(experiment)
        all_rows.append(
            {
                "experiment": experiment['name'],
                "trades": summary['trades'],
                "final_asset": summary['final_asset'],
                "final_return": summary['final_return'],
                "peak_asset": summary['peak_asset'],
                "peak_growth": summary['peak_growth'],
                "win_rate": summary['win_rate'],
                "pf": summary['pf'],
                "mdd": summary['mdd'],
                "max_conc": summary['max_conc'],
            }
        )
    if all_rows:
        out_path = ROOT / "results_json_only_timeout18_split_entry" / "single_changes_quick_summary.csv"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(all_rows).to_csv(out_path, index=False)
        print(f"saved quick summary to {out_path}")


if __name__ == '__main__':
    main()
