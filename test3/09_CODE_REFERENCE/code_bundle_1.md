# FILE: cross_sectional_isolated_reversion_v1.py
```python
"""원본 틀(엑셀 저장/print/plt/순차거래 시뮬/제외심볼) 유지 + 진입/손익절만 새 로직으로 교체

전략 개요
- OHLCV only
- 5분봉 멀티심볼
- 개별 종목 수익률을 자기 최근 변동성으로 표준화(z_self)
- 대표 시장 바스켓(메이저 코인들)의 같은 시점 z_self 분포와 비교(rel_z)
- 고립형 극단 이상치만 평균회귀 진입
- 청산은 SL/TP only

주의
- 기존 순차 시뮬 / 결과 저장 구조는 유지
- 기존 for문, 레버리지/자산분할 확인 용도 유지
- 완전한 전체시장 크로스섹션 엔진이 아니라, 계산량을 낮추기 위한 '메이저 바스켓 기반 시장표준화' 버전
"""
import ccxt, time
import pandas as pd
import math, os, datetime
import numpy as np
import matplotlib.pyplot as plt

file_name = "5m CrossSectional Isolated Reversion v1"
print(file_name)

# =========================
# 새 전략 파라미터
# =========================
TIMEFRAME = "5m"
WINDOW = 1500
FEE_RATE = 0.0004
MIN_SL_PCT = 0.3

# 개별 종목 자기표준화
RET_STD_LEN = 96          # 8시간
ATR_LEN = 14
VOL_MED_LEN = 96
RANGE_MED_LEN = 96
ZS_CLIP = 8.0

# 시장 바스켓(시장 표준화용)
MARKET_SYMBOLS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "TRX", "LINK", "LTC"
]
MARKET_MIN_COUNT = 5

# 고립형 이상치 평균회귀 조건
REL_Z_LONG_TH = -2.2
REL_Z_SHORT_TH = 2.2
RANGE_RATIO_MIN = 1.35
VOL_RATIO_MIN = 1.20
CLOSE_POS_LONG_MAX = 0.25
CLOSE_POS_SHORT_MIN = 0.75
WICK_IMB_LONG_MIN = 0.10
WICK_IMB_SHORT_MAX = -0.10
BREADTH_LOW = 0.20
BREADTH_HIGH = 0.80
CONSISTENCY_MAX = 1.1     # |z3|가 |z1| 대비 너무 크면 단발성 스파이크가 아닐 수 있음

# 손익절
STOP_ATR_MULT = 1.15
RR_DEFAULT = 1.25

# 원본 for문 호환용(남겨둠)
H_CANDIDATES = (12, 24, 48)
BINS = 3
ALPHA = 10.0
P_MIN = 0.58
N_MIN = 40
MAE_Q = 0.8
SL_CAP_PCT = 1.2

# 로더 캐시
_SYMBOL_CACHE = {}
_MARKET_CACHE = {}


def _safe_read_symbol(symbol_no_usdt: str, time_1: str = TIMEFRAME):
    path = '코인\\Data\\time\\{}_{}.xlsx'.format(symbol_no_usdt, time_1)
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_excel(path)
    except Exception:
        return None

    if "date" not in df.columns:
        return None
    need = {"open", "high", "low", "close", "volume"}
    if not need.issubset(set(df.columns)):
        return None

    use_cols = ["date", "open", "high", "low", "close", "volume"]
    df = df[use_cols].copy()
    df["datetime"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["datetime"]).copy()
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close", "volume"]).copy()
    df = df.sort_values("datetime").reset_index(drop=True)
    return df



def add_isolated_reversion_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    c = df["close"].astype(float)
    o = df["open"].astype(float)
    h = df["high"].astype(float)
    l = df["low"].astype(float)
    v = df["volume"].astype(float)

    prev_c = c.shift(1)
    tr = np.maximum(h - l, np.maximum((h - prev_c).abs(), (l - prev_c).abs()))
    atr = pd.Series(tr).rolling(ATR_LEN, min_periods=ATR_LEN).mean()
    rng = (h - l).replace(0, np.nan)

    ret1 = c.pct_change(1)
    ret3 = c.pct_change(3)
    ret12 = c.pct_change(12)

    ret_std = ret1.rolling(RET_STD_LEN, min_periods=RET_STD_LEN).std().replace(0, np.nan)
    z1 = (ret1 / ret_std).clip(-ZS_CLIP, ZS_CLIP)
    z3 = (ret3 / (ret_std * np.sqrt(3))).clip(-ZS_CLIP, ZS_CLIP)
    z12 = (ret12 / (ret_std * np.sqrt(12))).clip(-ZS_CLIP, ZS_CLIP)

    oc_max = pd.concat([o, c], axis=1).max(axis=1)
    oc_min = pd.concat([o, c], axis=1).min(axis=1)
    upper_wick = (h - oc_max).clip(lower=0)
    lower_wick = (oc_min - l).clip(lower=0)

    close_pos = ((c - l) / rng).clip(0, 1)
    wick_imb = ((lower_wick - upper_wick) / rng).replace([np.inf, -np.inf], np.nan)

    vol_med = v.rolling(VOL_MED_LEN, min_periods=VOL_MED_LEN).median().replace(0, np.nan)
    range_med = rng.rolling(RANGE_MED_LEN, min_periods=RANGE_MED_LEN).median().replace(0, np.nan)

    df["atr"] = atr
    df["z1"] = z1
    df["z3"] = z3
    df["z12"] = z12
    df["range"] = rng
    df["range_ratio"] = (rng / range_med).replace([np.inf, -np.inf], np.nan)
    df["vol_ratio"] = (v / vol_med).replace([np.inf, -np.inf], np.nan)
    df["close_pos"] = close_pos
    df["wick_imb"] = wick_imb
    df["atr_pct"] = (atr / c) * 100.0
    return df


# ... (bundle preserved; see local source for full implementation during development)
```

# FILE: event_scanner_ohlcv_v1.py
```python
# full source preserved in local development artifact; bundled here for project memory.
```

# FILE: event_scanner_ohlcv_v2.py
```python
# full source preserved in local development artifact; bundled here for project memory.
```

# FILE: failed_displacement_reclaim_v1.py
```python
# full source preserved in local development artifact; bundled here for project memory.
```