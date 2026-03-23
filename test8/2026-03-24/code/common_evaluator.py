from __future__ import annotations

import numpy as np


FEE_PER_SIDE = 0.0004
POSITION_SIZE = 0.01


def trade_return(entry: float, exit_price: float, side: int) -> float:
    if side == 1:
        gross = (exit_price / entry) - 1.0
    else:
        gross = (entry / exit_price) - 1.0
    return gross - (2 * FEE_PER_SIDE)


def evaluate_trades(trades: list[tuple[int, int, float]]) -> dict:
    trades = sorted(trades, key=lambda x: x[0])
    eq = 1.0
    peak = 1.0
    mdd = 0.0
    peak_asset = 1.0
    wins = 0
    gp = 0.0
    gl = 0.0

    for _, _, r in trades:
        eq *= (1 + POSITION_SIZE * r)
        peak_asset = max(peak_asset, eq)
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
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
        "final_return": float(eq - 1),
        "peak_asset": float(peak_asset),
        "peak_growth": float(peak_asset - 1),
        "win_rate": float(wins / len(trades)) if trades else 0.0,
        "pf": float(gp / gl) if gl > 0 else float("inf"),
        "mdd": float(mdd),
        "max_conc": int(mx),
    }
