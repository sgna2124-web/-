from __future__ import annotations

import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from common_indicators import ema, rsi, atr, candle_features
from common_evaluator import evaluate_trades, trade_return


FEE_PER_SIDE = 0.0004
POSITION_SIZE = 0.01
MIN_EXPECTED_TP = 0.003
ZIP_PATH = Path("CGPT_5m.zip")


def load_symbol_df(zf: zipfile.ZipFile, name: str) -> pd.DataFrame:
    df = pd.read_csv(zf.open(name), usecols=["date", "open", "high", "low", "close", "volume"])
    df = df.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    return df


def run_symbol(df: pd.DataFrame) -> list[tuple[int, int, float]]:
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    t = pd.to_datetime(df["date"]).astype("int64").to_numpy()

    ema20 = ema(c, 20)
    rs = rsi(c, 14)
    at = atr(h, l, c, 14)
    feat = candle_features(o, h, l, c)

    trades: list[tuple[int, int, float]] = []
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
                trades.append((int(t[ei]), int(t[i]), float(trade_return(ep, float(exit_p), side))))
                inpos = False

    return trades


def run_all(zip_path: Path = ZIP_PATH) -> dict:
    all_trades: list[tuple[int, int, float]] = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            df = load_symbol_df(zf, name)
            if len(df) < 120:
                continue
            all_trades.extend(run_symbol(df))
    out = evaluate_trades(all_trades)
    out["strategy"] = "overextension_reversion_v1"
    return out


if __name__ == "__main__":
    result = run_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))
