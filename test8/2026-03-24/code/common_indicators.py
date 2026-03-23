from __future__ import annotations

import numpy as np
import pandas as pd


def ema(arr: np.ndarray, span: int) -> np.ndarray:
    return pd.Series(arr).ewm(span=span, adjust=False).mean().to_numpy()


def rsi(arr: np.ndarray, period: int = 14) -> np.ndarray:
    s = pd.Series(arr)
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = up / (dn + 1e-12)
    return (100 - 100 / (1 + rs)).to_numpy()


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    prev_close = pd.Series(close).shift(1)
    tr = pd.concat(
        [
            pd.Series(high - low),
            (pd.Series(high) - prev_close).abs(),
            (pd.Series(low) - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean().to_numpy()


def rolling_high(arr: np.ndarray, window: int, shift: int = 1) -> np.ndarray:
    return pd.Series(arr).rolling(window).max().shift(shift).to_numpy()


def rolling_low(arr: np.ndarray, window: int, shift: int = 1) -> np.ndarray:
    return pd.Series(arr).rolling(window).min().shift(shift).to_numpy()


def rolling_mean(arr: np.ndarray, window: int, shift: int = 1) -> np.ndarray:
    return pd.Series(arr).rolling(window).mean().shift(shift).to_numpy()


def rolling_std(arr: np.ndarray, window: int, shift: int = 1) -> np.ndarray:
    return pd.Series(arr).rolling(window).std().shift(shift).to_numpy()


def candle_features(open_: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> dict:
    rng = np.maximum(high - low, 1e-12)
    return {
        "body": np.abs(close - open_),
        "upper_wick": high - np.maximum(close, open_),
        "lower_wick": np.minimum(close, open_) - low,
        "close_pos": (close - low) / rng,
        "range": rng,
    }
