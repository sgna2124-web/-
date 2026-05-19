# long_main v16 완전 재현 사양

이 파일은 완전 실행형 러너가 아니어도, 처음 보는 사람이 base_line 기록만 보고 동일 전략을 다시 구현할 수 있도록 필요한 계산식을 코드 수준으로 고정한다.

## 0. 공식 기준선

- axis: long_main
- version: v16
- source batch: `LONG_MAIN_LM23_RANK1_RETEST_20260519_213610`
- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

공식 기대값:

```python
EXPECTED = {
    "trades": 56551,
    "wins": 21969,
    "losses": 34582,
    "win_rate_pct": 38.84811939665081,
    "final_return_pct": 454.0898854634718,
    "max_return_pct": 455.0171719748199,
    "max_drawdown_pct": 1.3974597812998368,
    "official_cd_value": 547.2610302171641,
    "max_conc": 445,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}
```

## 1. 입력 데이터 표준화

필수 컬럼:

```text
timestamp, open, high, low, close, volume
```

허용되는 timestamp 별칭:

```text
timestamp, open_time, opentime, time, date, datetime
```

허용되는 volume 별칭:

```text
volume, vol
```

표준화 규칙:

```python
def standardize_ohlcv_columns(df):
    cols = {str(c).lower().strip(): c for c in df.columns}
    rename_map = {}
    aliases = [
        ("timestamp", "timestamp"), ("open_time", "timestamp"), ("opentime", "timestamp"),
        ("time", "timestamp"), ("date", "timestamp"), ("datetime", "timestamp"),
        ("open", "open"), ("high", "high"), ("low", "low"), ("close", "close"),
        ("volume", "volume"), ("vol", "volume"),
    ]
    for low_name, target in aliases:
        if low_name in cols:
            rename_map[cols[low_name]] = target
    df = df.rename(columns=rename_map).copy()
    df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
    if not np.issubdtype(df["timestamp"].dtype, np.number):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        df["timestamp"] = (ts.astype("int64") // 10**9).astype("float64")
    for c in ["timestamp", "open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
```

## 2. 2025년까지 데이터 필터

`2026-01-01 00:00:00 UTC` 미만 데이터만 사용한다.

```python
TRAIN_END_EXCLUSIVE_EPOCH_SEC = 1767225600
TRAIN_END_EXCLUSIVE_EPOCH_MS = 1767225600000

def apply_train_end_filter(df):
    ts = pd.to_numeric(df["timestamp"], errors="coerce")
    median_ts = float(ts[np.isfinite(ts)].median())
    if median_ts > 1e14:
        cutoff = TRAIN_END_EXCLUSIVE_EPOCH_MS * 1000
    elif median_ts > 1e11:
        cutoff = TRAIN_END_EXCLUSIVE_EPOCH_MS
    else:
        cutoff = TRAIN_END_EXCLUSIVE_EPOCH_SEC
    return df.loc[ts < cutoff].reset_index(drop=True)
```

## 3. 지표 계산

```python
def rma(s, length):
    return s.ewm(alpha=1.0 / max(1, length), adjust=False).mean()

def atr(df, length=14):
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return rma(tr, length).bfill().fillna(0.0)

def rsi(series, length=14):
    diff = series.diff().fillna(0.0)
    up = diff.clip(lower=0.0)
    down = (-diff).clip(lower=0.0)
    avg_up = rma(up, length)
    avg_down = rma(down, length)
    rs = avg_up / avg_down.replace(0, np.nan)
    return (100.0 - (100.0 / (1.0 + rs))).fillna(50.0)
```

Feature:

```python
atr14 = atr(df, 14)
atrp = (atr14 / close.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
rsi14 = rsi(close, 14)
vol_ma20 = volume.rolling(20, min_periods=1).mean()
vol_ratio = (volume / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
body = (close - open).abs()
lower_wick = pd.concat([open, close], axis=1).min(axis=1) - low
body_atr = (body / atr14.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
bar_range = (high - low).replace(0, np.nan)
close_pos = ((close - low) / bar_range).replace([np.inf, -np.inf], np.nan).fillna(0.5)
lower_wick_body_ratio = (lower_wick / body.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
ll20 = low.rolling(20, min_periods=1).min()
hh20 = high.rolling(20, min_periods=1).max()
tr = pd.concat([(high - low).abs(), (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
quiet_ratio = (tr.ewm(span=6, adjust=False).mean() / tr.ewm(span=24, adjust=False).mean().replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
ret3 = close.pct_change(3).fillna(0.0)
ret5 = close.pct_change(5).fillna(0.0)
```

## 4. raw signal 계산

WARMUP_BARS는 120이다.

```python
WARMUP_BARS = 120

def raw_l01_signal_at(f, i):
    if i < 21:
        return False
    ll20_prev = f.ll20[i - 1]
    bull_reclaim = (
        f.low[i] < ll20_prev
        and f.close[i] > ll20_prev
        and f.close[i] > f.open[i]
        and f.close_pos[i] > 0.70
    )
    return (
        (f.ret3[i] < -0.04 or f.ret5[i] < -0.06)
        and bull_reclaim
        and f.vol_ratio[i] > 1.40
        and f.body_atr[i] > 0.35
        and f.atrp[i] > 0.003
    )

def raw_shock_down_at(f, i):
    return (
        (f.ret3[i] <= -0.035 or f.ret5[i] <= -0.050)
        and f.vol_ratio[i] >= 1.10
        and f.body_atr[i] >= 0.25
    )

def raw_extreme_reclaim_at(f, i):
    return (
        raw_l01_signal_at(f, i)
        and f.close_pos[i] >= 0.80
        and f.lower_wick_body_ratio[i] >= 1.50
        and f.vol_ratio[i] >= 1.60
    )

def raw_shock_reversal_balance_at(f, i):
    if i < 22:
        return False
    return (
        (f.ret3[i] <= -0.025 or f.ret5[i] <= -0.040)
        and f.close[i] > f.open[i]
        and f.close_pos[i] >= 0.70
        and f.vol_ratio[i] >= 0.90
        and f.body_atr[i] >= 0.16
        and f.rsi14[i] <= 48.0
        and f.quiet_ratio[i] <= 1.45
    )
```

## 5. entry source 계산

```python
ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80
TP03_MIN_TARGET_PCT = 0.30

family_v09 = raw_shock_down | raw_l01 | raw_shock_reversal_balance
anchor_extreme = raw_extreme_reclaim | (rsi14 <= 34.0)
guard_vol18 = vol_ratio >= 1.18
parent = family_v09 & anchor_extreme & guard_vol18

target_pct = (ENTRY_SOURCE_ATR_STOP * atr14 * ENTRY_SOURCE_RR_TARGET / np.maximum(close, 1e-12)) * 100.0
entry_source = parent & (target_pct >= TP03_MIN_TARGET_PCT)
entry_source[:120] = False
entry_source[-1:] = False
```

## 6. v16 최종 entry

```python
final_entry = entry_source & (body_atr >= 0.22)
final_entry[:120] = False
final_entry[-1:] = False
```

## 7. v16 청산 규칙

```python
ATR_STOP = 1.21
RR_TARGET = 5.05
MAX_HOLD_BARS = 17
COOLDOWN_BARS = 31
ROUND_TRIP_COST_BPS = 8.0
POSITION_FRACTION = 0.01
```

진입과 청산:

```python
signal_i = entry signal index
entry_i = signal_i + 1
entry_price = open[entry_i]
atr_val = atr14[signal_i]
stop_dist = ATR_STOP * atr_val
stop_price = entry_price - stop_dist
target_price = entry_price + stop_dist * RR_TARGET
last_i = min(n - 1, entry_i + MAX_HOLD_BARS)
```

청산 루프:

```python
exit_i = last_i
exit_price = close[last_i]
exit_reason = "time"
for j in range(entry_i, last_i + 1):
    hit_stop = low[j] <= stop_price
    hit_target = high[j] >= target_price
    if hit_stop and hit_target:
        exit_i, exit_price, exit_reason = j, stop_price, "stop_first_same_bar"
        break
    if hit_stop:
        exit_i, exit_price, exit_reason = j, stop_price, "stop"
        break
    if hit_target:
        exit_i, exit_price, exit_reason = j, target_price, "target"
        break
```

손익:

```python
gross_pct = (exit_price / entry_price - 1.0) * 100.0
cost_pct = ROUND_TRIP_COST_BPS * 0.01
pnl_pct = gross_pct - cost_pct
```

cooldown:

```python
next_allowed_signal_i = exit_i + COOLDOWN_BARS
```

`signal_i < next_allowed_signal_i`이면 해당 signal은 건너뛴다.

## 8. 복리, MDD, cd_value

```python
RUIN_THRESHOLD = 1e-12

def equity_curve_from_trade_pnls(trade_pnls_pct):
    eq = [1.0]
    cur = 1.0
    ruined = False
    for pnl_pct in trade_pnls_pct:
        cur *= 1.0 + POSITION_FRACTION * (pnl_pct / 100.0)
        eq.append(cur)
        if cur <= RUIN_THRESHOLD:
            ruined = True
            break
    return np.asarray(eq), ruined

def max_return_pct_from_equity(eq):
    return (np.max(eq) - 1.0) * 100.0

def max_drawdown_pct_from_equity(eq):
    peaks = np.maximum.accumulate(eq)
    dd = (eq / np.where(peaks == 0, 1.0, peaks) - 1.0) * 100.0
    return min(100.0, abs(np.min(dd)))

def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - max_drawdown_pct / 100.0) * (1.0 + max_return_pct / 100.0)
```

## 9. 동시성 max_conc

```python
events.append((entry_ts, +1))
events.append((exit_ts, -1))
events.sort(key=lambda x: (x[0], x[1]))
cur = 0
mx = 0
for _, delta in events:
    cur += delta
    mx = max(mx, cur)
```

동일 timestamp에서는 -1이 +1보다 먼저 정렬된다.

## 10. 재현 실패 체크 순서

1. 데이터가 597개 심볼로 잡혔는지 확인한다.
2. 2026년 데이터가 제외됐는지 확인한다.
3. timestamp 단위가 초/밀리초/마이크로초 중 올바르게 잘렸는지 확인한다.
4. TP03 gate가 `atr_stop=1.10`, `rr_target=3.80`으로 계산됐는지 확인한다.
5. final exit가 `atr_stop=1.21`, `rr_target=5.05`, `max_hold_bars=17`, `cooldown_bars=31`인지 확인한다.
6. `body_atr >= 0.22`가 entry_source 뒤에 AND로 붙었는지 확인한다.
7. entry가 signal_i가 아니라 signal_i + 1 open인지 확인한다.
8. 동일 캔들 stop/target 동시 히트가 stop-first인지 확인한다.
9. cooldown이 `exit_i + 31`인지 확인한다.
10. 수수료가 왕복 8bps, 즉 pnl_pct에서 0.08% 차감인지 확인한다.
11. position_fraction이 0.01인지 확인한다.
12. cd_value가 final_return_pct가 아니라 max_return_pct로 계산됐는지 확인한다.
