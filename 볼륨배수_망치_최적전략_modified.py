"""추세"""
import os
import math
import time
import datetime
from collections import deque

import ccxt
import ta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_name = "5m 볼륨배수_망치 3"
print(file_name)

DEBUG_MODE = True
DEBUG_SYMBOL = "CGPT/USDT"
DEBUG_SHOW_ROWS = 30
DEBUG_SAVE_SIGNAL_TABLE = False


def rma(series, length):
    return series.ewm(alpha=1 / length, adjust=False).mean()


def calc_rsi(series, length=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = rma(gain, length)
    avg_loss = rma(loss, length)
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)


def calc_adx(df, length=14):
    up_move = df["high"].diff()
    down_move = -df["low"].diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    plus_dm = pd.Series(plus_dm, index=df.index, dtype=float)
    minus_dm = pd.Series(minus_dm, index=df.index, dtype=float)

    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift(1)).abs()
    tr3 = (df["low"] - df["close"].shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = rma(tr, length)
    plus = 100 * rma(plus_dm, length) / atr.replace(0, np.nan)
    minus = 100 * rma(minus_dm, length) / atr.replace(0, np.nan)
    dx = 100 * (plus - minus).abs() / (plus + minus).replace(0, np.nan)
    return rma(dx, length).fillna(0)


def calc_atr(df, length=14):
    tr1 = df["high"] - df["low"]
    tr2 = (df["high"] - df["close"].shift(1)).abs()
    tr3 = (df["low"] - df["close"].shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return rma(tr, length).fillna(0)


def calc_heikin_ashi(df):
    ha_close = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha_open = pd.Series(index=df.index, dtype=float)

    if len(df) > 0:
        ha_open.iloc[0] = (df["open"].iloc[0] + df["close"].iloc[0]) / 2
        for i in range(1, len(df)):
            ha_open.iloc[i] = (ha_open.iloc[i - 1] + ha_close.iloc[i - 1]) / 2

    return ha_open, ha_close


def build_closed_1h_filter_from_5m(df):
    temp = df[["datetime", "open", "high", "low", "close", "volume"]].copy()
    temp["hour_bucket"] = temp["datetime"].dt.floor("1h")

    df_1h = temp.groupby("hour_bucket", as_index=False).agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum")
    )

    df_1h = df_1h.sort_values("hour_bucket").reset_index(drop=True)

    df_1h["ema20_1h"] = df_1h["close"].ewm(span=20, adjust=False).mean()
    df_1h["ema50_1h"] = df_1h["close"].ewm(span=50, adjust=False).mean()
    df_1h["ema20_slope_1h"] = df_1h["ema20_1h"].diff()
    df_1h["ema20_slope_prev_1h"] = df_1h["ema20_slope_1h"].shift(1)

    df_1h["mid_filter_1h_raw"] = (
        (df_1h["ema20_1h"] > df_1h["ema50_1h"]) &
        (df_1h["ema20_slope_1h"] < df_1h["ema20_slope_prev_1h"])
    )

    df_1h["mid_filter_1h_closed"] = df_1h["mid_filter_1h_raw"].shift(1, fill_value=False)

    filter_map = dict(zip(df_1h["hour_bucket"], df_1h["mid_filter_1h_closed"]))
    ema20_map = dict(zip(df_1h["hour_bucket"], df_1h["ema20_1h"].shift(1)))
    ema50_map = dict(zip(df_1h["hour_bucket"], df_1h["ema50_1h"].shift(1)))
    slope_map = dict(zip(df_1h["hour_bucket"], df_1h["ema20_slope_1h"].shift(1)))
    slope_prev_map = dict(zip(df_1h["hour_bucket"], df_1h["ema20_slope_prev_1h"].shift(1)))

    df["hour_bucket"] = df["datetime"].dt.floor("1h")
    df["mid_filter_1h"] = df["hour_bucket"].map(filter_map).fillna(False)
    df["ema20_1h_closed"] = df["hour_bucket"].map(ema20_map)
    df["ema50_1h_closed"] = df["hour_bucket"].map(ema50_map)
    df["ema20_slope_1h_closed"] = df["hour_bucket"].map(slope_map)
    df["ema20_slope_prev_1h_closed"] = df["hour_bucket"].map(slope_prev_map)

    return df, df_1h


def print_debug_summary(symbol, df, skip_length):
    check_df = df.iloc[skip_length + 1:].copy()

    cols = [
        "date", "rsi_high", "short_cross", "wick_cond", "close_cond",
        "recent_uptrend", "trend_exhausted", "high_update_ok",
        "mid_filter_1h", "short_setup", "ha_strong_bear"
    ]
    for c in cols:
        if c not in check_df.columns:
            check_df[c] = np.nan

    print("=" * 80)
    print(f"[DEBUG] {symbol}")
    print(f"전체봉수: {len(df)} / 체크시작후 봉수: {len(check_df)}")
    print(f"short_cross: {int(check_df['short_cross'].sum())}")
    print(f"wick_cond: {int(check_df['wick_cond'].sum())}")
    print(f"close_cond: {int(check_df['close_cond'].sum())}")
    print(f"recent_uptrend: {int(check_df['recent_uptrend'].sum())}")
    print(f"trend_exhausted: {int(check_df['trend_exhausted'].sum())}")
    print(f"high_update_ok: {int(check_df['high_update_ok'].sum())}")
    print(f"mid_filter_1h: {int(check_df['mid_filter_1h'].sum())}")
    print(f"short_setup: {int(check_df['short_setup'].sum())}")
    print(f"ha_strong_bear: {int(check_df['ha_strong_bear'].sum())}")

    signal_rows = check_df.loc[check_df["short_setup"] == True, [
        "date", "close", "high", "rsi_close", "short_dev_pct", "upper_wick", "body", "close_pos",
        "recent_uptrend", "trend_exhausted", "high_update_ok", "mid_filter_1h",
        "ema20_1h_closed", "ema50_1h_closed", "ema20_slope_1h_closed", "ema20_slope_prev_1h_closed",
        "ha_strong_bear"
    ]].head(DEBUG_SHOW_ROWS)

    if len(signal_rows) > 0:
        print("-" * 80)
        print("[DEBUG] short_setup 통과 샘플")
        print(signal_rows.to_string(index=False))
    else:
        print("-" * 80)
        print("[DEBUG] short_setup 통과 샘플 없음")

    if DEBUG_SAVE_SIGNAL_TABLE:
        out_path = f"코인\\Data\\cir\\DEBUG_{symbol.replace('/','_')}_signals.xlsx"
        check_df.to_excel(out_path, index=False)
        print(f"[DEBUG] 신호 테이블 저장: {out_path}")

    print("=" * 80)


def run_(prange, hl_period, skip_length, for_check, for_check_nu):
    coin_df = pd.read_csv("symbol_cost")
    coin_df = coin_df.sort_index(ascending=False)
    coin_df = coin_df.loc[coin_df.symbol == 'CGPT/USDT']

    trade_record = 1

    ap_list = []
    aw_list = []
    al_list = []
    mc_list = []

    date_list = []
    side_list = []
    stat_list = []
    profit_list = []
    profit3_list = []
    fee_list = []
    count_list = []
    in_price_list = []
    av_price_list = []
    symbol_list = []
    symbol2_list = []
    pp_list = []
    danger_list = []

    max_symbol = ""
    max_profit = 0
    min_symbol = ""
    min_profit = 0

    aleady_simul = 0
    df_sm = pd.DataFrame()
    df_sm2 = pd.DataFrame()

    for ss in coin_df.symbol:
        if os.path.exists(f"코인\\Data\\cir\\거래결과{file_name}.xlsx") and aleady_simul == 1 and len(coin_df) > 1:
            df_sm = pd.read_excel(f"코인\\Data\\cir\\거래결과{file_name}.xlsx")
            aleady_simul = 1
            break
        else:
            aleady_simul = 0

        if ss in ["BTCST/USDT", "USDC/USDT", "GAIB/USDT", "XEM/USDT", "VOXEL/USDT", "BAKE/USDT", "UNFI/USDT"]:
            continue

        count_list2 = []
        win_list = []

        seed = 100.0
        seed2 = 100.0

        ss_ = ss.replace("/USDT", "")
        time_1 = "5m"
        path = f"코인\\Data\\time\\{ss_}_{time_1}.csv"
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)
        if len(df) == 0:
            continue

        df["datetime"] = pd.to_datetime(df["date"])
        df = df.sort_values("datetime").drop_duplicates(subset=["datetime"]).reset_index(drop=True)

        if len(df) <= skip_length + 5:
            continue

        short_count = 0

        pending_short = 0
        pending_short_bar = -1
        pending_short_atr = np.nan

        short_seed = 0.0
        short_avr_price = np.nan
        short_more = np.nan
        short_end = np.nan
        short_entry_bar = -1
        short_original_risk = np.nan
        short_best_mfe_r = 0.0
        short_time_reduced = 0

        df["rsi_high"] = calc_rsi(df["high"], 14)
        df["rsi_close"] = calc_rsi(df["close"], 14)
        df["adx"] = calc_adx(df, 14)
        df["atr"] = calc_atr(df, 14)
        df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
        df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
        df["ema_spread_pct"] = (df["ema20"] - df["ema50"]).abs() / df["close"].replace(0, np.nan)

        df["body"] = (df["open"] - df["close"]).abs()
        df["range"] = df["high"] - df["low"]
        df["upper_wick"] = df["high"] - df[["open", "close"]].max(axis=1)
        df["lower_wick"] = df[["open", "close"]].min(axis=1) - df["low"]
        df["close_pos"] = np.where(df["range"] == 0, 0.5, (df["close"] - df["low"]) / df["range"])

        df["recent_uptrend"] = df["close"] > df["close"].shift(8)
        df["adx_falling"] = df["adx"] < df["adx"].shift(3)
        df["trend_exhausted"] = (df["adx"] < 25) & df["adx_falling"] & (df["ema_spread_pct"] < 0.025)

        prev_high_8 = df["high"].shift(1).rolling(8).max()
        df["high_update_ok"] = (df["high"] <= prev_high_8) | prev_high_8.isna()

        ha_open, ha_close = calc_heikin_ashi(df)
        df["ha_open"] = ha_open
        df["ha_close"] = ha_close
        df["ha_bear"] = df["ha_close"] < df["ha_open"]
        df["ha_strong_bear"] = df["ha_bear"] & df["ha_bear"].shift(1, fill_value=False) & (df["ha_close"] < df["ha_close"].shift(1))

        df, df_1h = build_closed_1h_filter_from_5m(df)

        df["short_dev_pct"] = (df["close"] / df["ema20"] - 1).replace([np.inf, -np.inf], np.nan).fillna(0)
        df["short_dev_cond"] = df["short_dev_pct"] >= 0.032
        df["short_rsi_cond"] = df["rsi_close"] > 76
        df["wick_cond"] = (df["upper_wick"] >= df["body"] * 1.3) & (df["upper_wick"] > 0)
        df["short_cross"] = df["short_dev_cond"]
        df["close_cond"] = df["short_rsi_cond"]

        df["short_setup"] = (
            df["short_dev_cond"] &
            df["short_rsi_cond"] &
            df["wick_cond"]
        )

        if DEBUG_MODE and ss == DEBUG_SYMBOL:
            print_debug_summary(ss, df, skip_length)

        for i in range(skip_length + 1, len(df)):
            pre_open = df["open"].iloc[i]
            pre_close = df["close"].iloc[i]
            pre_high = df["high"].iloc[i]
            pre_low = df["low"].iloc[i]

            if short_count == 0 and pending_short == 1 and i == pending_short_bar + 1:
                if pd.notna(pending_short_atr) and pending_short_atr > 0 and pd.notna(pre_open) and pre_open > 0:
                    entry_price = pre_open
                    stop_price = entry_price + pending_short_atr * 1.8975
                    risk_r = stop_price - entry_price

                    if risk_r > 0:
                        target_price = entry_price - risk_r * 6.0

                        short_count = 1
                        short_seed = seed * 1.0
                        fee = short_seed * 0.0004
                        seed -= fee

                        short_avr_price = entry_price
                        short_more = stop_price
                        short_end = target_price
                        short_entry_bar = i
                        short_original_risk = risk_r
                        short_best_mfe_r = 0.0
                        short_time_reduced = 0

                        danger_value = abs(entry_price - short_more) / entry_price if entry_price != 0 else 0

                        date_list.append(df["date"].iloc[i])
                        count_list.append(short_count)
                        count_list2.append(short_count)
                        win_list.append("o")
                        side_list.append("Short")
                        stat_list.append("오픈")
                        profit_list.append(0)
                        profit3_list.append(0)
                        fee_list.append(fee)
                        in_price_list.append(entry_price)
                        av_price_list.append(entry_price)
                        symbol_list.append(ss)
                        danger_list.append(danger_value)

                pending_short = 0
                pending_short_bar = -1
                pending_short_atr = np.nan

            if short_count >= 1:
                current_mfe_r = 0.0
                if short_original_risk > 0:
                    current_mfe_r = max((short_avr_price - pre_low) / short_original_risk, 0.0)
                    short_best_mfe_r = max(short_best_mfe_r, current_mfe_r)

                stop_hit = pre_high >= short_more
                tp_hit = pre_low <= short_end

                if stop_hit:
                    exit_price = short_more
                    profit = (short_avr_price - exit_price) / short_avr_price * 100
                    profit3 = short_seed * profit / 100
                    fee = (short_seed + profit3) * 0.0004
                    seed += profit3 - fee
                    short_count = 0

                    date_list.append(df["date"].iloc[i])
                    count_list.append(short_count)
                    count_list2.append(short_count)
                    win_list.append("l")
                    side_list.append("Short")
                    stat_list.append("손절")
                    profit_list.append(profit)
                    profit3_list.append(profit3)
                    fee_list.append(fee)
                    in_price_list.append(exit_price)
                    av_price_list.append(short_avr_price)
                    symbol_list.append(ss)
                    danger_list.append(short_seed)

                    short_avr_price = np.nan
                    short_more = np.nan
                    short_end = np.nan
                    short_entry_bar = -1
                    short_original_risk = np.nan
                    short_best_mfe_r = 0.0
                    short_time_reduced = 0

                elif tp_hit:
                    exit_price = short_end
                    profit = (short_avr_price - exit_price) / short_avr_price * 100
                    profit3 = short_seed * profit / 100
                    fee = (short_seed + profit3) * 0.0004
                    seed += profit3 - fee
                    short_count = 0

                    date_list.append(df["date"].iloc[i])
                    count_list.append(short_count)
                    count_list2.append(short_count)
                    win_list.append("w")
                    side_list.append("Short")
                    stat_list.append("정리")
                    profit_list.append(profit)
                    profit3_list.append(profit3)
                    fee_list.append(fee)
                    in_price_list.append(exit_price)
                    av_price_list.append(short_avr_price)
                    symbol_list.append(ss)
                    danger_list.append(short_seed)

                    short_avr_price = np.nan
                    short_more = np.nan
                    short_end = np.nan
                    short_entry_bar = -1
                    short_original_risk = np.nan
                    short_best_mfe_r = 0.0
                    short_time_reduced = 0

                else:
                    bars_since_entry = i - short_entry_bar

                    if bars_since_entry >= 10 and short_time_reduced == 0 and short_best_mfe_r > 0 and short_original_risk > 0:
                        reduced_stop = short_avr_price + short_original_risk * 0.05
                        short_more = min(short_more, reduced_stop)
                        short_time_reduced = 1

                    if bars_since_entry >= 10 and short_best_mfe_r < 0.10 and pre_close > short_avr_price:
                        exit_price = pre_close
                        profit = (short_avr_price - exit_price) / short_avr_price * 100
                        profit3 = short_seed * profit / 100
                        fee = (short_seed + profit3) * 0.0004
                        seed += profit3 - fee
                        short_count = 0

                        date_list.append(df["date"].iloc[i])
                        count_list.append(short_count)
                        count_list2.append(short_count)
                        win_list.append("l" if profit <= 0 else "w")
                        side_list.append("Short")
                        stat_list.append("손절" if profit <= 0 else "정리")
                        profit_list.append(profit)
                        profit3_list.append(profit3)
                        fee_list.append(fee)
                        in_price_list.append(exit_price)
                        av_price_list.append(short_avr_price)
                        symbol_list.append(ss)
                        danger_list.append(short_seed)

                        short_avr_price = np.nan
                        short_more = np.nan
                        short_end = np.nan
                        short_entry_bar = -1
                        short_original_risk = np.nan
                        short_best_mfe_r = 0.0
                        short_time_reduced = 0

                    elif bars_since_entry >= 200:
                        exit_price = pre_close
                        profit = (short_avr_price - exit_price) / short_avr_price * 100
                        profit3 = short_seed * profit / 100
                        fee = (short_seed + profit3) * 0.0004
                        seed += profit3 - fee
                        short_count = 0

                        date_list.append(df["date"].iloc[i])
                        count_list.append(short_count)
                        count_list2.append(short_count)
                        win_list.append("l" if profit <= 0 else "w")
                        side_list.append("Short")
                        stat_list.append("손절" if profit <= 0 else "정리")
                        profit_list.append(profit)
                        profit3_list.append(profit3)
                        fee_list.append(fee)
                        in_price_list.append(exit_price)
                        av_price_list.append(short_avr_price)
                        symbol_list.append(ss)
                        danger_list.append(short_seed)

                        short_avr_price = np.nan
                        short_more = np.nan
                        short_end = np.nan
                        short_entry_bar = -1
                        short_original_risk = np.nan
                        short_best_mfe_r = 0.0
                        short_time_reduced = 0

            if short_count == 0 and pending_short == 0 and i < len(df) - 1 and bool(df["short_setup"].iloc[i]):
                pending_short = 1
                pending_short_bar = i
                pending_short_atr = df["atr"].iloc[i]

        last_profit = 0
        if len(win_list) > 0:
            w = win_list.count("w")
            l = win_list.count("l")
            aw_list.append(w)
            al_list.append(l)
            max_count = max(count_list2) if len(count_list2) > 0 else 0
            last_profit = round(seed - seed2, 2)
            ap_list.append(last_profit)

            if max_profit < last_profit:
                max_symbol = ss
                max_profit = last_profit
            if min_profit > last_profit:
                min_symbol = ss
                min_profit = last_profit
            if max_count >= 10:
                mc_list.append(max_count)

        symbol2_list.append(ss)
        pp_list.append(last_profit)

    if aleady_simul == 0:
        tr_data = {
            "Symbol": symbol_list,
            "Date": date_list,
            "count_": count_list,
            "side": side_list,
            "stat": stat_list,
            "price": in_price_list,
            "av_price": av_price_list,
            "자산비중": danger_list,
            "수익": profit3_list,
            "수수료": fee_list,
            "수익률": profit_list
        }
        tr_data2 = {"Symbol": symbol2_list, "자산": pp_list}

        df_sm = pd.DataFrame(tr_data)
        df_sm2 = pd.DataFrame(tr_data2)

        if len(df_sm) > 0:
            df_sm = df_sm.sort_values("Date").reset_index(drop=True)
            print(f"기간 {df_sm.Date.iloc[0]} ~ {df_sm.Date.iloc[-1]}")
        else:
            print("거래없음")

        df_sm2 = df_sm2.sort_values("자산").reset_index(drop=True)

        win_rating = 0
        if sum(aw_list) + sum(al_list) > 0:
            win_rating = round(sum(aw_list) / (sum(aw_list) + sum(al_list)) * 100, 2)

        print("총 승률 : ", win_rating, "%")
        print("총 승 : ", sum(aw_list))
        print("총 패 : ", sum(al_list))
        print("총 오픈기록 : ", len([x for x in stat_list if x == "오픈"]))
        print("최대 수익 종목 : {} {}".format(max_symbol, max_profit))
        print("최대 손실 종목 : {} {}".format(min_symbol, min_profit))

        try:
            if for_check <= for_check_nu:
                if len(coin_df) == 1 and len(df_sm) > 0:
                    only_symbol = coin_df.symbol.iloc[0].replace("/USDT", "")
                    df_sm.to_excel(f"코인\\Data\\cir\\{file_name}_{only_symbol}.xlsx", sheet_name="sheet1", index=False)
                else:
                    df_sm2.to_excel(f"코인\\Data\\cir\\결과_{file_name}.xlsx", sheet_name="sheet1", index=False)
                if trade_record == 1 and len(coin_df) > 1 and len(df_sm) > 0:
                    df_sm.to_excel(f"코인\\Data\\cir\\거래결과{file_name}.xlsx", sheet_name="sheet1", index=False)
        except Exception as e:
            print("결과저장에러", e)
    else:
        win_rating = 0
        if len(df_sm) > 0 and "stat" in df_sm.columns:
            wins = (df_sm["stat"] == "정리").sum()
            losses = (df_sm["stat"] == "손절").sum()
            if wins + losses > 0:
                win_rating = round(wins / (wins + losses) * 100, 2)

    base_money = 100
    money = 100
    fee_rate = 0.0004
    symbol_list_live = []
    asset_list_live = []
    count_list_live = []
    side_list_live = []
    devide = 300
    in_money = money / 300
    max_ = 100
    mdd = 0
    lev = 10
    max_position = 0
    yday = 100

    d_list = []
    p_list = []
    mdd_list = []
    now_mdd_list = []
    pnl_list = []
    in_money_list = []
    len_dev_list = []
    have_list = []

    if len(df_sm) > 0:
        df_sm = df_sm.sort_values("Date").reset_index(drop=True)

        for i in range(len(df_sm)):
            if i == 0 or df_sm.Date.iloc[i] != df_sm.Date.iloc[i - 1]:
                dev = df_sm[(df_sm["Date"] == df_sm.Date.iloc[i]) & (df_sm["count_"] == 1)]
                len_dev = len(dev)
                devide = len_dev if len_dev > 300 else 300
                in_money = money / 300

            if df_sm.count_.iloc[i] == 1:
                asset = money / devide * lev
                symbol_list_live.append(df_sm.Symbol.iloc[i])
                asset_list_live.append(asset)
                side_list_live.append(df_sm.side.iloc[i])
                count_list_live.append(df_sm.count_.iloc[i])
                money -= asset * fee_rate

            elif df_sm.count_.iloc[i] > 1:
                check1 = 0
                for ii in range(len(symbol_list_live)):
                    if symbol_list_live[ii] == df_sm.Symbol.iloc[i] and side_list_live[ii] == df_sm.side.iloc[i]:
                        money -= asset_list_live[ii] * (df_sm.count_.iloc[i] - count_list_live[ii]) * fee_rate
                        count_list_live[ii] = df_sm.count_.iloc[i]
                        check1 = 1
                        break
                if check1 == 0:
                    continue

            else:
                for ii in range(len(symbol_list_live)):
                    if symbol_list_live[ii] == df_sm.Symbol.iloc[i] and side_list_live[ii] == df_sm.side.iloc[i]:
                        profit = asset_list_live[ii] * count_list_live[ii] * df_sm.수익률.iloc[i] / 100
                        money += profit - profit * fee_rate
                        del symbol_list_live[ii]
                        del side_list_live[ii]
                        del asset_list_live[ii]
                        del count_list_live[ii]
                        break

            max_position = max(max_position, len(symbol_list_live))
            max_ = max(max_, money)
            mdd = min(mdd, money / max_ - 1)

            if i == 0 or df_sm.Date.iloc[i] != df_sm.Date.iloc[i - 1]:
                d_list.append(df_sm.Date.iloc[i])
                p_list.append(round(money, 2))
                mdd_list.append(round(mdd * 100, 2))
                now_mdd_list.append(round((money / max_ - 1) * 100, 2))
                pnl_list.append(round((money - yday) / yday * 100, 2))
                in_money_list.append(in_money)
                len_dev_list.append(len_dev)
                have_list.append(len(symbol_list_live))
                yday = money

    print("최종 순차 수익 : {}".format(round(money, 2)))
    print("MDD : {}%".format(round(mdd * 100, 2)))
    print("최대 수익 : {}".format(round(max_, 2)))
    print("최대 포지션 보유수 : {}".format(max_position))

    if for_check <= for_check_nu and len(d_list) > 0:
        tr_data3 = {
            "날짜": d_list,
            "자산": p_list,
            "일일변동": pnl_list,
            "현재낙폭": now_mdd_list,
            "최대낙폭": mdd_list,
            "진입자산": in_money_list,
            "진입수": len_dev_list,
            "포지션수": have_list
        }
        df_sm3 = pd.DataFrame(tr_data3)
        if len(coin_df) > 1:
            df_sm3.to_excel(f"코인\\Data\\cir\\순차결과_{file_name}.xlsx", sheet_name="sheet1", index=False)

        plt.figure(1)
        plt.plot(d_list, p_list, "b-")
        plt.show()

    return win_rating, round(money, 2), round(mdd * 100, 2), round(max_, 2)


prange = 12

prange_list = []
rsi_list = []
win_list = []
last_list = []
mdd_list = []
max_list = []
skip_list = []

first_range = 1
second_range = 1
third_range = 1

for_check = first_range + second_range + third_range
for_check_nu = 3

for rf in range(first_range):
    hl_period = 6
    for _ in range(second_range):
        skip_length = 288
        for _ in range(third_range):
            print("-" * 50)
            print("prange {}, hl_period {}, skip {}".format(round(prange, 1), hl_period, skip_length))
            win_rate, last_, mdd, max_ = run_(prange, hl_period, skip_length, for_check, for_check_nu)

            prange_list.append(prange)
            rsi_list.append(hl_period)
            win_list.append(win_rate)
            last_list.append(last_)
            mdd_list.append(mdd)
            max_list.append(max_)
            skip_list.append(skip_length)
            skip_length += 1
        hl_period += 1
    prange += 1

if for_check > for_check_nu:
    tr_data = {
        "prange": prange_list,
        "hl": rsi_list,
        "최종수익": last_list,
        "MDD": mdd_list,
        "스킵길이": skip_list,
        "최대수익": max_list,
        "승률": win_list
    }
    df3 = pd.DataFrame(tr_data)
    df3.to_excel(f"코인\\Data\\cir\\{file_name}.xlsx", sheet_name="sheet1", index=False)

print(file_name)
