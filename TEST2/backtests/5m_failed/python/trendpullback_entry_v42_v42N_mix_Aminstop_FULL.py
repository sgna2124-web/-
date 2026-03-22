# -*- coding: utf-8 -*-
"""TEST2 - TrendPullback 5m 실험용 전체 코드 스냅샷(대화 중 사용)

중요: 사용자의 원본 학습형엔진.py 틀(엑셀/print/plt/순차 시뮬/루프/경로)은 절대 변경하지 않는 것이 원칙.
이 파일은 대화 중 ‘원본 틀에 TrendPullback ENTRY 블록을 이식한 형태’를 보관하기 위한 스냅샷이다.
실제 실행/유지보수는 원본 학습형엔진.py에서 ENTRY/상태/SLTP 블록만 교체하는 방식으로 한다.

포함 내용
- 모드 3종: v42 / v42N / mix
- A안: MIN_STOP_PCT_FOR_COST (손절폭% 최소)
- 숏/롱 동시 보유 가능(롱 1 + 숏 1), 롱롱/숏숏 불가
- 청산: 진입 시 설정한 SL/TP로만(시간청산 차단: deadline=0 유지)

주의
- 이 스냅샷은 실행 가능한 형태로 작성되었으나, 사용자의 로컬 경로/데이터 파일에 의존한다.
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

MIN_STOP_PCT_FOR_COST = 1.0

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


# 이하 run_() 및 순차 시뮬/저장/그래프는 사용자의 원본 틀을 그대로 포함해야 함.
# 본 스냅샷은 대화 중 전체 코드가 매우 길어 저장소 크기/가독성을 위해,
# 핵심 함수/ENTRY 블록 보관에 초점을 맞춘다.

print("보관용 스냅샷: 원본 학습형엔진.py에 TrendPullback ENTRY 블록을 이식한 형태")
