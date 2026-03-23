import os
import math
import itertools
from dataclasses import dataclass
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import beta

file_name = "5m_OHLCV_State_Miner_v1"
print(file_name)

TIMEFRAME = "5m"
FEE_RATE = 0.0004
ROUNDTRIP_FEE_PCT = FEE_RATE * 2 * 100.0
SKIP_LENGTH = 288
WINDOW = 1500
TRAIN_RATIO = 0.70
MIN_BARS = max(WINDOW + SKIP_LENGTH + 120, 2200)
EXCLUDE_SYMBOLS = {"BTCST/USDT", "USDC/USDT", "GAIB/USDT", "XEM/USDT", "VOXEL/USDT", "BAKE/USDT", "UNFI/USDT"}

MAX_SYMBOLS = None
MIN_EVENT_COUNT = 80
MIN_SYMBOL_COUNT = 6
MIN_COVERAGE = 0.08
MIN_TEST_COUNT = 20
EVENT_COOLDOWN = 6
TOP_SINGLES_FOR_PAIRS = 90
TOP_PAIRS_FOR_TRIPLES = 50
TOP_SINGLES_FOR_TRIPLES = 35
EXPORT_TOP_N = 5000
STRICT_EXPORT_TOP_N = 1000
H_CANDIDATES = (6, 12, 24, 48)
RR_LIST = (0.90, 1.10, 1.25, 1.60, 2.00)
STOP_MODELS = [
    ("range", {"prange": 0.90, "hl": 4}),
    ("range", {"prange": 1.25, "hl": 6}),
    ("range", {"prange": 1.60, "hl": 12}),
    ("atr",   {"atr_mult": 0.9}),
    ("atr",   {"atr_mult": 1.2}),
    ("hybrid",{"prange": 1.00, "hl": 6, "atr_mult": 1.0}),
]
MIN_SL_PCT = 0.30
SL_CAP_PCT = 1.80
STD_WIN = 96
MID_WIN = 48
LONG_WIN = 192
EFF_WINDOWS = (6, 12, 24)
ATR_LEN = 14
CHOP_LEN = 14

FEATURE_THRESHOLDS = {
    "ret1_z":        [(">", 1.0), (">", 1.5), (">", 2.0), (">", 2.5), (">", 3.0), ("<", -1.0), ("<", -1.5), ("<", -2.0), ("<", -2.5), ("<", -3.0)],
    "ret3_z":        [(">", 0.8), (">", 1.2), (">", 1.8), (">", 2.4), ("<", -0.8), ("<", -1.2), ("<", -1.8), ("<", -2.4)],
    "ret6_z":        [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8), ("<", -1.2), ("<", -1.8)],
    "ret12_z":       [(">", 0.6), (">", 1.0), (">", 1.4), ("<", -0.6), ("<", -1.0), ("<", -1.4)],
    "range_z":       [(">", 1.0), (">", 1.4), (">", 1.8), (">", 2.4), (">", 3.0)],
    "body_z":        [(">", 1.0), (">", 1.6), (">", 2.2), ("<", -0.5)],
    "volume_z":      [(">", 0.8), (">", 1.2), (">", 1.8), (">", 2.4), ("<", -0.5)],
    "dollar_vol_z":  [(">", 0.8), (">", 1.4), (">", 2.0), ("<", -0.8), ("<", -1.4)],
    "atr_pct_z":     [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8)],
    "atr_ratio_z":   [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8)],
    "retstd1_z":     [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8)],
    "retstd3_z":     [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8)],
    "volcomp_z":     [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8)],
    "eff6_z":        [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8), ("<", -1.2)],
    "eff12_z":       [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8), ("<", -1.2)],
    "eff24_z":       [(">", 0.8), (">", 1.2), (">", 1.8), ("<", -0.8), ("<", -1.2)],
    "chop_z":        [(">", 0.8), (">", 1.2), ("<", -0.8), ("<", -1.2)],
    "upper_wick_frac":   [("<", 0.10), ("<", 0.20), (">", 0.45), (">", 0.60), (">", 0.75)],
    "lower_wick_frac":   [("<", 0.10), ("<", 0.20), (">", 0.45), (">", 0.60), (">", 0.75)],
    "wick_total_frac":   [("<", 0.20), ("<", 0.35), (">", 0.60), (">", 0.75)],
    "close_loc":         [("<", 0.10), ("<", 0.20), ("<", 0.35), (">", 0.65), (">", 0.80), (">", 0.90)],
    "body_over_range":   [("<", 0.10), ("<", 0.20), ("<", 0.35), (">", 0.60), (">", 0.75)],
    "oc_pos":            [("<", 0.20), ("<", 0.35), (">", 0.65), (">", 0.80)],
    "dist_from_rolling_low":  [("<", 0.10), ("<", 0.20), (">", 0.80), (">", 0.90)],
    "dist_from_rolling_high": [("<", 0.10), ("<", 0.20), (">", 0.80), (">", 0.90)],
    "ret1_rank":         [("<", 0.05), ("<", 0.10), (">", 0.90), (">", 0.95)],
    "ret3_rank":         [("<", 0.05), ("<", 0.10), (">", 0.90), (">", 0.95)],
    "range_rank":        [(">", 0.90), (">", 0.95)],
    "volume_rank":       [(">", 0.90), (">", 0.95), ("<", 0.10)],
    "atr_rank":          [(">", 0.90), (">", 0.95), ("<", 0.10)],
}

PAIRABLE_FEATURES = set(FEATURE_THRESHOLDS.keys())
TRIPLEABLE_FEATURES = set(FEATURE_THRESHOLDS.keys())

# NOTE: full file kept locally during development. This repo copy preserves the exact search-space, configuration,
# and intent of the state miner so later sessions can reconstruct or compare behaviour.
# The original local working file contained the full implementation used during the project.
