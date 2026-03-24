from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "test8" / "2026-03-24" / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from common_evaluator import evaluate_trades, trade_return  # noqa: E402
from common_indicators import ema, rsi, atr, candle_features  # noqa: E402

FEE_PER_SIDE = 0.0004
POSITION_SIZE = 0.01
MIN_EXPECTED_TP = 0.003
DATA_DIR = ROOT / "5m_data"
RESULT_DIR = ROOT / "results" / "latest"


def load_symbol_df(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, usecols=["date", "open", "high", "low", "close", "volume"])
    df = df.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    return df


def run_symbol(df: pd.DataFrame) -> list[tuple[int, int, float, str]]:
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    t = pd.to_datetime(df["date"]).astype("int64").to_numpy()

    ema20 = ema(c, 20)
    rs = rsi(c, 14)
    at = atr(h, l, c, 14)
    feat = candle_features(o, h, l, c)

    trades: list[tuple[int, int, float, str]] = []
    inpos = False

    for i in range(30, len(c) - 1):
        if not inpos:
            long_sig = (
                ((c[i] / ema20[i]) - 1.0) <= -0.025
                and rs[i] < 28
                and feat["lower_wick"][i] > feat["body"][i]
            )
            short_sig = (
                ((c[i] / ema20[i]) - 1.0) >= 0.025
                and rs[i] > 72
                and feat["upper_wick"][i] > feat["body"][i]
            )

            if long_sig:
                entry = o[i + 1]
                stop = min(l[i], entry - at[i] * 1.5)
                ema_target = ema20[i]
                r_target = entry + 2.2 * (entry - stop)
                target = min(ema_target, r_target) if ema_target > entry else r_target
                if entry > stop and (target - entry) / entry >= MIN_EXPECTED_TP:
                    inpos = True
                    side = 1
                    ei = i + 1
                    ep = float(entry)
                    sp = float(stop)
                    tp = float(target)
            elif short_sig:
                entry = o[i + 1]
                stop = max(h[i], entry + at[i] * 1.5)
                ema_target = ema20[i]
                r_target = entry - 2.2 * (stop - entry)
                target = max(ema_target, r_target) if ema_target < entry else r_target
                if stop > entry and (entry - target) / entry >= MIN_EXPECTED_TP:
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
                elif i - ei >= 36:
                    exit_p = c[i]
            else:
                if h[i] >= sp:
                    exit_p = sp
                elif l[i] <= tp:
                    exit_p = tp
                elif i - ei >= 36:
                    exit_p = c[i]

            if exit_p is not None:
                trades.append((int(t[ei]), int(t[i]), float(trade_return(ep, float(exit_p), side)), "long" if side == 1 else "short"))
                inpos = False

    return trades


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    all_trades: list[tuple[int, int, float]] = []
    trade_rows = []
    symbol_rows = []

    for csv_path in sorted(DATA_DIR.glob("*.csv")):
        df = load_symbol_df(csv_path)
        if len(df) < 120:
            continue
        symbol_trades = run_symbol(df)
        all_trades.extend((en, ex, ret) for en, ex, ret, _ in symbol_trades)

        wins = sum(1 for _, _, r, _ in symbol_trades if r > 0)
        losses = sum(1 for _, _, r, _ in symbol_trades if r <= 0)
        gp = sum(r for _, _, r, _ in symbol_trades if r > 0)
        gl = -sum(r for _, _, r, _ in symbol_trades if r <= 0)
        symbol_rows.append(
            {
                "symbol": csv_path.stem,
                "bars": len(df),
                "trades": len(symbol_trades),
                "wins": wins,
                "losses": losses,
                "win_rate": (wins / len(symbol_trades)) if symbol_trades else 0.0,
                "pf": (gp / gl) if gl > 0 else None,
                "sum_r": sum(r for _, _, r, _ in symbol_trades),
            }
        )

        for en, ex, ret, side in symbol_trades:
            trade_rows.append(
                {
                    "symbol": csv_path.stem,
                    "entry_ts": en,
                    "exit_ts": ex,
                    "ret": ret,
                    "side": side,
                }
            )

    summary = evaluate_trades(all_trades)
    summary["strategy"] = "overextension_reversion_v1_repo_batch"
    summary["initial_asset"] = 100.0
    summary["position_fraction"] = POSITION_SIZE
    summary["fee_per_side"] = FEE_PER_SIDE
    summary["symbols"] = len(symbol_rows)

    pd.DataFrame(trade_rows).sort_values(["entry_ts", "symbol"]).to_csv(RESULT_DIR / "trades.csv", index=False)
    pd.DataFrame(symbol_rows).sort_values(["trades", "sum_r"], ascending=[False, False]).to_csv(RESULT_DIR / "by_symbol.csv", index=False)
    with open(RESULT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
