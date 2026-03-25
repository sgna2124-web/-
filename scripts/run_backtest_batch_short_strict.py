from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "test8" / "2026-03-24" / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from common_indicators import ema, rsi, atr, candle_features  # noqa: E402

BASE_CONFIG_PATH = ROOT / "experiments" / "base_config_short_strict.json"
SINGLE_CHANGES_PATH = ROOT / "experiments" / "single_changes_short_strict.json"


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
            f"{path.name} 는 실제 CSV가 아니라 Git LFS 포인터 파일입니다. "
            "GitHub Actions checkout 단계에서 LFS 파일을 pull 하도록 설정해야 합니다."
        )

    alias_map = {
        "date": [
            "date", "datetime", "timestamp", "time", "open_time", "opentime",
            "candle_date_time_utc", "candle_date_time_kst"
        ],
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
    if side == 1:
        gross = (exit_price / entry) - 1.0
    else:
        gross = (entry / exit_price) - 1.0
    return gross - (2.0 * fee_per_side)


def evaluate_trades_cfg(trades: list[tuple[int, int, float]], position_fraction: float) -> dict:
    trades = sorted(trades, key=lambda x: x[0])
    eq = 1.0
    peak = 1.0
    peak_asset = 1.0
    mdd = 0.0
    wins = 0
    gp = 0.0
    gl = 0.0

    for _, _, r in trades:
        eq *= (1.0 + position_fraction * r)
        peak_asset = max(peak_asset, eq)
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1.0)
        if r > 0:
            wins += 1
            gp += r
        else:
            gl += -r

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

def compute_prev_completed_htf_rsi(df: pd.DataFrame, htf_rule: str, rsi_period: int) -> pd.Series:
    htf_rule = str(htf_rule).strip().lower()

    htf = (
        df.set_index("date")["close"]
        .resample(htf_rule, label="left", closed="left")
        .last()
        .dropna()
        .reset_index()
    )
    htf_close = htf["close"].to_numpy(float)
    htf_rsi = rsi(htf_close, rsi_period)
    htf["htf_rsi_prev_completed"] = pd.Series(htf_rsi).shift(1)

    merged = pd.merge_asof(
        df[["date"]].sort_values("date"),
        htf[["date", "htf_rsi_prev_completed"]].sort_values("date"),
        on="date",
        direction="backward",
    )
    return merged["htf_rsi_prev_completed"]


def run_symbol(df: pd.DataFrame, config: dict) -> list[tuple[int, int, float, str]]:
    signal_cfg = config["signal"]
    risk_cfg = config["risk"]
    trade_control_cfg = config["trade_control"]
    filters_cfg = config.get("filters", {})
    exec_cfg = config["execution"]
    fee_per_side = float(config["fee_per_side"])

    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    v = df["volume"].to_numpy(float)
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

    volume_cfg = filters_cfg.get("volume_filter", {})
    volume_enabled = bool(volume_cfg.get("enabled", False))
    volume_lookback = int(volume_cfg.get("lookback", 20))
    volume_multiple = float(volume_cfg.get("min_multiple", 1.5))
    vol_ma = pd.Series(v).rolling(volume_lookback).mean().to_numpy(float)

    htf_cfg = filters_cfg.get("htf_filter", {})
    htf_enabled = bool(htf_cfg.get("enabled", False))
    if htf_enabled:
        if not bool(htf_cfg.get("use_prev_completed_only", True)):
            raise ValueError("HTF filter must use previous completed bar only.")
        htf_rule = htf_cfg.get("timeframe", "1h")
        htf_long_rsi_max = float(htf_cfg.get("long_rsi_max", 35))
        htf_short_rsi_min = float(htf_cfg.get("short_rsi_min", 65))
        htf_prev_rsi = compute_prev_completed_htf_rsi(df, htf_rule, rsi_period).to_numpy(float)
    else:
        htf_long_rsi_max = np.nan
        htf_short_rsi_min = np.nan
        htf_prev_rsi = np.full(len(df), np.nan)

    trades: list[tuple[int, int, float, str]] = []
    inpos = False
    last_exit_idx = {1: -10_000_000, -1: -10_000_000}
    start_idx = max(ema_period, rsi_period, atr_period, volume_lookback, 30)

    for i in range(start_idx, len(c) - 1):
        volume_ok = True
        if volume_enabled:
            volume_ok = pd.notna(vol_ma[i]) and vol_ma[i] > 0 and v[i] >= volume_multiple * vol_ma[i]

        htf_long_ok = True
        htf_short_ok = True
        if htf_enabled:
            # 중요: 5분봉 17:30에서는 현재 진행 중인 17:00 1시간봉을 쓰면 안 됨.
            # resample 후 shift(1)한 직전 완성 1시간봉 RSI만 사용한다.
            htf_long_ok = pd.notna(htf_prev_rsi[i]) and htf_prev_rsi[i] <= htf_long_rsi_max
            htf_short_ok = pd.notna(htf_prev_rsi[i]) and htf_prev_rsi[i] >= htf_short_rsi_min

        if not inpos:
            long_cooldown_ok = (i - last_exit_idx[1]) > cooldown_bars
            short_cooldown_ok = (i - last_exit_idx[-1]) > cooldown_bars

            long_sig = (
                allow_long
                and long_cooldown_ok
                and volume_ok
                and htf_long_ok
                and ((c[i] / ema_v[i]) - 1.0) <= -long_dev
                and rsi_v[i] < long_rsi_max
                and feat["lower_wick"][i] >= long_wick_mult * feat["body"][i]
            )

            short_sig = (
                allow_short
                and short_cooldown_ok
                and volume_ok
                and htf_short_ok
                and ((c[i] / ema_v[i]) - 1.0) >= short_dev
                and rsi_v[i] > short_rsi_min
                and feat["upper_wick"][i] >= short_wick_mult * feat["body"][i]
            )

            if long_sig:
                entry = o[i + 1]
                stop = min(l[i], entry - atr_v[i] * atr_stop_mult)
                ema_target = ema_v[i]
                r_target = entry + rr_mult * (entry - stop)
                target = min(ema_target, r_target) if ema_target > entry else r_target
                if entry > stop and (target - entry) / entry >= min_expected_tp:
                    inpos = True
                    side = 1
                    ei = i + 1
                    ep = float(entry)
                    sp = float(stop)
                    tp = float(target)
            elif short_sig:
                entry = o[i + 1]
                stop = max(h[i], entry + atr_v[i] * atr_stop_mult)
                ema_target = ema_v[i]
                r_target = entry - rr_mult * (stop - entry)
                target = max(ema_target, r_target) if ema_target < entry else r_target
                if stop > entry and (entry - target) / entry >= min_expected_tp:
                    inpos = True
                    side = -1
                    ei = i + 1
                    ep = float(entry)
                    sp = float(stop)
                    tp = float(target)
        else:
            exit_p = None
            if side == 1:
                if l[i] <= sp:
                    exit_p = sp
                elif h[i] >= tp:
                    exit_p = tp
                elif i - ei >= timeout_bars:
                    exit_p = c[i]
            else:
                if h[i] >= sp:
                    exit_p = sp
                elif l[i] <= tp:
                    exit_p = tp
                elif i - ei >= timeout_bars:
                    exit_p = c[i]

            if exit_p is not None:
                ret = trade_return_cfg(ep, float(exit_p), side, fee_per_side)
                trades.append((int(t[ei]), int(t[i]), float(ret), "long" if side == 1 else "short"))
                last_exit_idx[side] = i
                inpos = False

    return trades


def run_single_experiment(experiment: dict) -> dict:
    exp_name = experiment["name"]
    cfg = experiment["effective_config"]
    data_dir = ROOT / cfg["data_dir"]
    result_dir = ROOT / cfg["results_dir"] / exp_name
    result_dir.mkdir(parents=True, exist_ok=True)

    min_bars = int(cfg["min_bars"])
    position_fraction = float(cfg["position_fraction"])
    all_trades: list[tuple[int, int, float]] = []
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
        all_trades.extend((en, ex, ret) for en, ex, ret, _ in symbol_trades)

        wins = sum(1 for _, _, r, _ in symbol_trades if r > 0)
        losses = sum(1 for _, _, r, _ in symbol_trades if r <= 0)
        gp = sum(r for _, _, r, _ in symbol_trades if r > 0)
        gl = -sum(r for _, _, r, _ in symbol_trades if r <= 0)
        symbol_rows.append({
            "symbol": csv_path.stem,
            "bars": len(df),
            "trades": len(symbol_trades),
            "wins": wins,
            "losses": losses,
            "win_rate": (wins / len(symbol_trades)) if symbol_trades else 0.0,
            "pf": (gp / gl) if gl > 0 else None,
            "sum_r": sum(r for _, _, r, _ in symbol_trades),
        })

        for en, ex, ret, side in symbol_trades:
            trade_rows.append({
                "symbol": csv_path.stem,
                "entry_ts": en,
                "exit_ts": ex,
                "ret": ret,
                "side": side,
            })

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
    single_changes = load_json(SINGLE_CHANGES_PATH)
    experiments = build_experiments(base_config, single_changes)
    print(f"loaded experiments: {[e['name'] for e in experiments]}")

    rows = []
    for experiment in experiments:
        print(f"running experiment: {experiment['name']}")
        summary = run_single_experiment(experiment)
        rows.append({
            "experiment": experiment["name"],
            "trades": summary["trades"],
            "final_asset": summary["final_asset"],
            "final_return": summary["final_return"],
            "peak_asset": summary["peak_asset"],
            "peak_growth": summary["peak_growth"],
            "win_rate": summary["win_rate"],
            "pf": summary["pf"],
            "mdd": summary["mdd"],
            "max_conc": summary["max_conc"],
        })

    if rows:
        out_path = ROOT / "results_short_strict" / "single_changes_quick_summary.csv"
        pd.DataFrame(rows).to_csv(out_path, index=False)
        print(f"saved quick summary to {out_path}")


if __name__ == "__main__":
    main()
