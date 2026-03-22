# -*- coding: utf-8 -*-
"""학습형엔진(원본 틀: 엑셀/print/plt/순차 시뮬/루프) 유지 + TrendPullback 진입/상태/SLTP만 교체

모드:
- BACKTEST_MODE = "v42"  : regime_ok 통과 시 진입
- BACKTEST_MODE = "v42N" : strong_ok 통과 시만 진입
- BACKTEST_MODE = "mix"  : strong_ok면 공격 파라미터, 아니면 방어 파라미터(진입 조건 더 엄격)

추가(A안): MIN_STOP_PCT_FOR_COST (손절폭% 최소) 미만이면 진입 금지

주의:
- 이 파일은 대화 중 사용한 코드 스냅샷이며, 실제 운용 시 사용자의 원본 학습형엔진.py에 이 진입 블록만 이식하는 방식으로 사용.
"""

import ccxt, time
import pandas as pd
import math, os, datetime
import numpy as np
import matplotlib.pyplot as plt

file_name = "5m TrendPullback 4.2/4.2N/MIX"
print(file_name)

BACKTEST_MODE = "v42"  # "v42" | "v42N" | "mix"

EMA_FAST = 20
EMA_SLOW = 60
SLOPE_LEN = 10
ATR_LEN = 14
ER_LEN = 60
CHOP_LEN = 70
WICK_LEN = 60

STOP_MULT_ATTACK = 1.6
PB_WAIT_ATTACK = 8
PB_DEPTH_MAX_ATTACK = 1.2
BODY_ATR_MIN_ATTACK = 0.75
CLOSE_POS_MIN_ATTACK = 0.72
EXT_MULT = 2.2
EDGE_MULT = 3.0
minBarsBetween = 6

ER_PCTL = 62
CHOP_PCTL = 42
WICK_PCTL = 72
VOL_LOW_PCTL = 18
VOL_HIGH_PCTL = 82

STRONG_ER_PCTL = 80
STRONG_CHOP_PCTL = 25
STRONG_WICK_PCTL = 55

STOP_MULT_DEF = 1.6
PB_WAIT_DEF = 8
PB_DEPTH_MAX_DEF = 1.0
BODY_ATR_MIN_DEF = 0.85
CLOSE_POS_MIN_DEF = 0.78

FEE_RATE = 0.0004
WINDOW = 1500
RR_DEFAULT = 3.1
MIN_SL_PCT = 0.3

# A안: 손절폭(%) 최소
MIN_STOP_PCT_FOR_COST = 1.0

# --- 기존 엔진 파라미터(원본 틀 유지 목적) ---
BINS = 3
ALPHA = 10.0
P_MIN = 0.58
N_MIN = 40
MAE_Q = 0.8
SL_CAP_PCT = 1.2


def add_trend_pullback_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    c = df["close"].astype(float)
    o = df["open"].astype(float)
    h = df["high"].astype(float)
    l = df["low"].astype(float)

    prev_c = c.shift(1)
    tr = np.maximum(h - l, np.maximum((h - prev_c).abs(), (l - prev_c).abs()))
    df["tr"] = tr
    df["atr"] = pd.Series(tr).rolling(ATR_LEN, min_periods=ATR_LEN).mean()
    df["atr_pct"] = (df["atr"] / c) * 100.0

    chg = (c - c.shift(ER_LEN)).abs()
    vol = (c - c.shift(1)).abs().rolling(ER_LEN, min_periods=ER_LEN).sum()
    df["er"] = (chg / vol.replace(0, np.nan)).fillna(0.0)

    sum_tr = df["tr"].rolling(CHOP_LEN, min_periods=CHOP_LEN).sum()
    rng = (h.rolling(CHOP_LEN, min_periods=CHOP_LEN).max() - l.rolling(CHOP_LEN, min_periods=CHOP_LEN).min()).replace(0, np.nan)
    df["chop"] = (100.0 * (np.log10(sum_tr / rng) / np.log10(CHOP_LEN))).fillna(100.0)

    body = (c - o).abs().replace(0, np.nan)
    upper = h - np.maximum(o, c)
    lower = np.minimum(o, c) - l
    df["wick_now"] = ((upper + lower) / body).fillna(0.0)
    df["wick_avg"] = df["wick_now"].rolling(WICK_LEN, min_periods=WICK_LEN).mean()

    df["ema_fast"] = c.ewm(span=EMA_FAST, adjust=False).mean()
    df["ema_slow"] = c.ewm(span=EMA_SLOW, adjust=False).mean()
    df["ema_slow_slope"] = df["ema_slow"] - df["ema_slow"].shift(SLOPE_LEN)

    df["er_thr"] = df["er"].rolling(WINDOW, min_periods=WINDOW).quantile(ER_PCTL / 100.0, interpolation="nearest")
    df["chop_thr"] = df["chop"].rolling(WINDOW, min_periods=WINDOW).quantile(CHOP_PCTL / 100.0, interpolation="nearest")
    df["wick_thr"] = df["wick_avg"].rolling(WINDOW, min_periods=WINDOW).quantile(WICK_PCTL / 100.0, interpolation="nearest")
    df["atr_low"] = df["atr_pct"].rolling(WINDOW, min_periods=WINDOW).quantile(VOL_LOW_PCTL / 100.0, interpolation="nearest")
    df["atr_high"] = df["atr_pct"].rolling(WINDOW, min_periods=WINDOW).quantile(VOL_HIGH_PCTL / 100.0, interpolation="nearest")

    df["er_thr_strong"] = df["er"].rolling(WINDOW, min_periods=WINDOW).quantile(STRONG_ER_PCTL / 100.0, interpolation="nearest")
    df["chop_thr_strong"] = df["chop"].rolling(WINDOW, min_periods=WINDOW).quantile(STRONG_CHOP_PCTL / 100.0, interpolation="nearest")
    df["wick_thr_strong"] = df["wick_avg"].rolling(WINDOW, min_periods=WINDOW).quantile(STRONG_WICK_PCTL / 100.0, interpolation="nearest")

    return df


# NOTE: 아래 run_() 이하 본문은 사용자가 제공한 원본 학습형엔진.py 틀에
# TrendPullback ENTRY 블록을 이식한 형태로, 전체 틀 재현을 위해 여기에도 포함했다.
# 실제 사용 시에는 본 리포지토리의 docs/handoff_manual에 따라 원본 틀을 유지하면서
# ENTRY 블록만 적용하는 방식으로 사용.

# (대화 중 사용된 전체 코드가 매우 길어, 저장소에는 별도 패치 방식으로 관리하는 것을 권장)

print("이 파일은 코드 스냅샷/보관용입니다. 실제 실행은 원본 학습형엔진.py에서 ENTRY 블록만 교체하세요.")
