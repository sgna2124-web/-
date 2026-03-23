import io
import os
import heapq
import warnings
import openpyxl
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

SYMBOLS = ["BTC","ETH","BCH","LTC","LINK","ETC","BOB","SENT","IRYS","RLS"]

def load_disguised_excel(path, start_date="2021-01-01"):
    start = pd.Timestamp(start_date)
    with open(path, "rb") as fh:
        bio = io.BytesIO(fh.read())
    wb = openpyxl.load_workbook(bio, read_only=True, data_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    next(rows)
    out = []
    for row in rows:
        dt = row[1]
        if dt is None or dt < start:
            continue
        out.append((dt, float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])))
    wb.close()
    df = pd.DataFrame(out, columns=["date","open","high","low","close","volume"])
    return df

def prepare_symbol(df):
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    dt = df["date"].to_numpy()
    rng = h - l
    med20 = pd.Series(rng).rolling(20).median().shift(1).to_numpy()
    prev5h = pd.Series(h).rolling(5).max().shift(1).to_numpy()
    prev5l = pd.Series(l).rolling(5).min().shift(1).to_numpy()
    return dt, o, h, l, c, rng, med20, prev5h, prev5l

def extract_trades(prep, symbol, event_mult=2.0, rr=1.5, max_hold=120, min_tp_pct=0.003):
    dt, o, h, l, c, rng, med20, prev5h, prev5l = prep
    n = len(c)
    trades = []
    i = 21

    while i < n - 1:
        made_trade = False
        event_range = rng[i]
        event_mid = (o[i] + c[i]) / 2.0

        if not np.isnan(med20[i]) and event_range >= event_mult * med20[i]:
            if h[i] > prev5h[i]:
                j = i + 1
                if h[j] <= h[i] and c[j] < event_mid and c[j] < o[j]:
                    entry = c[j]
                    sl = h[i]
                    risk = sl - entry
                    if risk > 0:
                        tp = entry - rr * risk
                        if (entry - tp) / entry >= min_tp_pct:
                            end = min(n - 1, j + max_hold)
                            exit_idx = end
                            exit_price = c[end]
                            reason = "TIME"
                            for k in range(j + 1, end + 1):
                                sl_hit = h[k] >= sl
                                tp_hit = l[k] <= tp
                                if sl_hit or tp_hit:
                                    if sl_hit:
                                        exit_idx = k
                                        exit_price = sl
                                        reason = "SL"
                                    else:
                                        exit_idx = k
                                        exit_price = tp
                                        reason = "TP"
                                    break
                            trades.append({
                                "entry_time": dt[j],
                                "exit_time": dt[exit_idx],
                                "symbol": symbol,
                                "side": "SHORT",
                                "entry": entry,
                                "exit": exit_price,
                                "ret_pct": (entry - exit_price) / entry,
                                "reason": reason,
                            })
                            i = exit_idx + 1
                            made_trade = True

            if not made_trade and l[i] < prev5l[i]:
                j = i + 1
                if l[j] >= l[i] and c[j] > event_mid and c[j] > o[j]:
                    entry = c[j]
                    sl = l[i]
                    risk = entry - sl
                    if risk > 0:
                        tp = entry + rr * risk
                        if (tp - entry) / entry >= min_tp_pct:
                            end = min(n - 1, j + max_hold)
                            exit_idx = end
                            exit_price = c[end]
                            reason = "TIME"
                            for k in range(j + 1, end + 1):
                                sl_hit = l[k] <= sl
                                tp_hit = h[k] >= tp
                                if sl_hit or tp_hit:
                                    if sl_hit:
                                        exit_idx = k
                                        exit_price = sl
                                        reason = "SL"
                                    else:
                                        exit_idx = k
                                        exit_price = tp
                                        reason = "TP"
                                    break
                            trades.append({
                                "entry_time": dt[j],
                                "exit_time": dt[exit_idx],
                                "symbol": symbol,
                                "side": "LONG",
                                "entry": entry,
                                "exit": exit_price,
                                "ret_pct": (exit_price - entry) / entry,
                                "reason": reason,
                            })
                            i = exit_idx + 1
                            made_trade = True

        if not made_trade:
            i += 1

    return pd.DataFrame(trades)

def simulate_portfolio(trades, initial_equity=10000.0, alloc_pct=0.01, fee_rate=0.0004):
    if trades.empty:
        return {
            "final_equity": initial_equity,
            "return_pct": 0.0,
            "peak_equity": initial_equity,
            "peak_pct": 0.0,
            "mdd_pct": 0.0,
            "win_rate": np.nan,
            "long_win_rate": np.nan,
            "short_win_rate": np.nan,
            "trades": 0,
            "max_positions": 0,
            "max_single_trade_pct": np.nan,
        }

    trades = trades.sort_values(["entry_time","exit_time"]).reset_index(drop=True)
    equity = initial_equity
    peak = initial_equity
    maxdd = 0.0
    wins = 0
    long_wins = 0
    short_wins = 0
    long_n = 0
    short_n = 0
    max_trade = -1e9
    max_positions = 0

    entries = trades.to_dict("records")
    open_positions = []
    idx = 0
    uid = 0

    while idx < len(entries) or open_positions:
        next_entry_time = entries[idx]["entry_time"] if idx < len(entries) else None
        next_exit_time = open_positions[0][0] if open_positions else None

        if next_exit_time is not None and (next_entry_time is None or next_exit_time <= next_entry_time):
            t = next_exit_time
            while open_positions and open_positions[0][0] <= t:
                _, _, pos = heapq.heappop(open_positions)
                net = pos["notional"] * pos["ret_pct"] - pos["notional"] * fee_rate * 2.0
                equity += net

                if net > 0:
                    wins += 1
                    if pos["side"] == "LONG":
                        long_wins += 1
                    else:
                        short_wins += 1

                if pos["side"] == "LONG":
                    long_n += 1
                else:
                    short_n += 1

                max_trade = max(max_trade, net / pos["notional"])
                peak = max(peak, equity)
                maxdd = min(maxdd, (equity - peak) / peak)
        else:
            t = next_entry_time
            while idx < len(entries) and entries[idx]["entry_time"] == t:
                row = entries[idx]
                heapq.heappush(
                    open_positions,
                    (
                        row["exit_time"],
                        uid,
                        {
                            "notional": equity * alloc_pct,
                            "ret_pct": row["ret_pct"],
                            "side": row["side"],
                        },
                    ),
                )
                uid += 1
                idx += 1
            max_positions = max(max_positions, len(open_positions))

    return {
        "final_equity": float(equity),
        "return_pct": float((equity / initial_equity - 1.0) * 100.0),
        "peak_equity": float(peak),
        "peak_pct": float((peak / initial_equity - 1.0) * 100.0),
        "mdd_pct": float(maxdd * 100.0),
        "win_rate": float(wins / len(trades) * 100.0),
        "long_win_rate": float(long_wins / long_n * 100.0) if long_n else np.nan,
        "short_win_rate": float(short_wins / short_n * 100.0) if short_n else np.nan,
        "trades": int(len(trades)),
        "max_positions": int(max_positions),
        "max_single_trade_pct": float(max_trade * 100.0) if max_trade > -1e8 else np.nan,
    }

def run_grid(data_dir="/mnt/data", rr_list=(1.0,1.5,2.0), event_mult_list=(1.5,2.0,2.5)):
    prepared = {}
    for sym in SYMBOLS:
        path = os.path.join(data_dir, f"{sym}_5m.csv")
        df = load_disguised_excel(path, start_date="2021-01-01")
        prepared[sym] = prepare_symbol(df)

    rows = []
    for event_mult in event_mult_list:
        for rr in rr_list:
            all_trades = []
            for sym in SYMBOLS:
                tr = extract_trades(prepared[sym], sym, event_mult=event_mult, rr=rr)
                if not tr.empty:
                    all_trades.append(tr)
            trades = pd.concat(all_trades, ignore_index=True) if all_trades else pd.DataFrame()
            summary = simulate_portfolio(trades)
            summary["event_mult"] = event_mult
            summary["rr"] = rr
            rows.append(summary)

    result = pd.DataFrame(rows).sort_values(["return_pct","peak_pct"], ascending=False).reset_index(drop=True)
    return result

if __name__ == "__main__":
    result = run_grid(
        data_dir="/mnt/data",
        rr_list=(1.0, 1.5, 2.0, 2.5),
        event_mult_list=(1.5, 2.0, 2.5, 3.0),
    )
    print(result.to_string(index=False))
