"""원본 틀 유지 + Failed Displacement Reclaim 진입로직 교체"""
import ccxt, time
import pandas as pd
import math, os, datetime
import numpy as np
import matplotlib.pyplot as plt

file_name = "5m FailedDisplacementReclaim v1"
print(file_name)

FDR_LOOKBACK_MULT = 8
FDR_HORIZON_MULT = 4
ZSCORE_WIN = 200
MIN_WARMUP = 260
RET1_Z_TH = 2.5
RET3_Z_TH = 3.0
RANGE_Z_TH = 2.0
CLOSE_LOC_LONG = 0.55
CLOSE_LOC_SHORT = 0.45
LOWER_WICK_MIN = 0.30
UPPER_WICK_MAX = 0.25
BODY_OVER_RANGE_MIN = 0.20

FEE_RATE = 0.0004
WINDOW = 1500
H_CANDIDATES = (12, 24, 48)
RR_DEFAULT = 3.1
MIN_SL_PCT = 0.3

BINS = 3
ALPHA = 10.0
P_MIN = 0.58
N_MIN = 40
MAE_Q = 0.8
SL_CAP_PCT = 1.2

# NOTE
# 이 파일은 프로젝트 후반에 기존 엔진 틀을 유지한 채
# Failed Displacement Reclaim 철학을 삽입하려던 참조 코드다.
# 핵심 철학:
# - 최근 수용 범위를 비정상적으로 강하게 이탈
# - 새 가격대 수용 실패 후 range 안으로 reclaim
# - 그 경우 반대 방향 역추세 진입
# - SL은 이벤트 고저점 기준으로 짧고 선명하게 설정
#
# 프로젝트 기록상, 철학 자체는 사용자 반응이 괜찮았지만
# 초기 20개 종목 테스트 성과는 손실과 낮은 승률로 실패 상태였다.
# 따라서 현재 시점에서는 '성공 전략'이 아니라
# '사용자 철학과 가장 잘 맞았던 사건 중심 전략 예시'로 보관한다.
