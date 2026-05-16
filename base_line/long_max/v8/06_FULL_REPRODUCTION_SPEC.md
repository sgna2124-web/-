# long_max v8 완전 재현 사양

이 파일은 long_main v12와 동일한 기준선 후보 `LM18_041_STOP115_RR520_BODY025`를 long_max 축 기준으로 재현하기 위한 사양이다.

long_max v8과 long_main v12는 같은 전략, 같은 결과값, 같은 계산 규칙을 사용한다. 차이는 갱신 축의 평가 기준뿐이다.

## 0. 공식 기준선

- axis: long_max
- version: v8
- source batch: `LONG_MAIN_DEV_V18_20260516_213239`
- source candidate: `LM18_041_STOP115_RR520_BODY025`
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

공식 기대값:

```python
EXPECTED = {
    "trades": 56428,
    "wins": 20531,
    "losses": 35897,
    "win_rate_pct": 36.38441908272489,
    "final_return_pct": 397.7275034318756,
    "max_return_pct": 398.29373996834414,
    "max_drawdown_pct": 1.4367182391297861,
    "official_cd_value": 491.134662921777,
    "max_conc": 443,
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

허용 timestamp 별칭:

```text
timestamp, open_time, opentime, time, date, datetime
```

허용 volume 별칭:

```text
volume, vol
```

표준화 규칙은 long_main/v12/06_FULL_REPRODUCTION_SPEC.md의 `standardize_ohlcv_columns(df)`와 동일하다.

## 2. 2025년까지 데이터 필터

`2026-01-01 00:00:00 UTC` 미만 데이터만 사용한다.

timestamp가 초, 밀리초, 마이크로초일 수 있으므로 중앙값으로 단위를 판별한다.

```python
TRAIN_END_EXCLUSIVE_EPOCH_SEC = 1767225600
TRAIN_END_EXCLUSIVE_EPOCH_MS = 1767225600000
```

## 3. 지표 계산

long_main/v12와 동일하다.

필수 feature:

```text
atr14, atrp, rsi14, vol_ma20, vol_ratio, body, lower_wick,
body_atr, close_pos, lower_wick_body_ratio, ll20, hh20,
range_mid20, tr, quiet_ratio, ret3, ret5
```

핵심 계산:

```python
body_atr = abs(close - open) / atr14
vol_ratio = volume / volume.rolling(20, min_periods=1).mean()
close_pos = (close - low) / (high - low)
ret3 = close.pct_change(3)
ret5 = close.pct_change(5)
```

0 나눗셈과 NaN은 v12 사양처럼 0 또는 중립값으로 채운다.

## 4. raw signal

long_main/v12의 raw signal과 동일하다.

필수 함수:

```text
raw_l01_signal_at
raw_shock_down_at
raw_extreme_reclaim_at
raw_shock_reversal_balance_at
```

중요 임계값:

```text
raw_l01: ret3 < -0.04 또는 ret5 < -0.06, vol_ratio > 1.40, body_atr > 0.35, atrp > 0.003
raw_shock_down: ret3 <= -0.035 또는 ret5 <= -0.050, vol_ratio >= 1.10, body_atr >= 0.25
raw_extreme_reclaim: raw_l01 AND close_pos >= 0.80 AND lower_wick_body_ratio >= 1.50 AND vol_ratio >= 1.60
raw_shock_reversal_balance: ret3 <= -0.025 또는 ret5 <= -0.040, close > open, close_pos >= 0.70, vol_ratio >= 0.90, body_atr >= 0.16, rsi14 <= 48.0, quiet_ratio <= 1.45
```

## 5. v8 frozen entry source

long_max v8의 entry source는 long_max v7 frozen entry다. 실제로는 long_main v11과 같은 entry source를 사용한다.

```python
ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80

family_v09 = raw_shock_down | raw_l01 | raw_shock_reversal_balance
anchor_extreme = raw_extreme_reclaim | (rsi14 <= 34.0)
guard_vol18 = vol_ratio >= 1.18
parent = family_v09 & anchor_extreme & guard_vol18

target_pct = (ENTRY_SOURCE_ATR_STOP * atr14 * ENTRY_SOURCE_RR_TARGET / max(close, 1e-12)) * 100
entry_source = parent & (target_pct >= 0.30)
entry_source[:120] = False
entry_source[-1:] = False
```

## 6. 최종 entry

```python
final_entry = entry_source & (body_atr >= 0.25)
final_entry[:120] = False
final_entry[-1:] = False
```

## 7. 최종 청산

```python
ATR_STOP = 1.15
RR_TARGET = 5.20
MAX_HOLD_BARS = 21
COOLDOWN_BARS = 31
ROUND_TRIP_COST_BPS = 8.0
POSITION_FRACTION = 0.01
```

진입은 signal_i + 1 open이다.

```python
entry_i = signal_i + 1
entry_price = open[entry_i]
risk = ATR_STOP * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * RR_TARGET
```

청산 우선순위:

```text
1. 같은 캔들 stop/target 동시 히트 시 stop-first
2. stop만 히트하면 stop
3. target만 히트하면 target
4. MAX_HOLD_BARS까지 없으면 close[last_i] time exit
```

손익:

```python
gross_pct = (exit_price / entry_price - 1) * 100
pnl_pct = gross_pct - 0.08
```

cooldown:

```python
next_allowed_signal_i = exit_i + 31
```

## 8. 평가 계산

복리:

```python
equity *= 1 + 0.01 * pnl_pct / 100
```

cd_value:

```python
official_cd_value = 100 * (1 - max_drawdown_pct / 100) * (1 + max_return_pct / 100)
```

long_max는 MDD 5% 제한 없이 `official_cd_value` 최대를 본다. 단, ruined false와 errors 0은 유지해야 한다.

## 9. 재현 실패 체크 순서

1. 597개 심볼 사용 여부
2. 2026년 데이터 제외 여부
3. entry source TP03가 rr 3.80 기준인지 여부
4. final exit가 atr_stop 1.15, rr 5.20인지 여부
5. body_atr >= 0.25가 entry source 뒤에 붙었는지 여부
6. signal_i + 1 open 진입 여부
7. stop-first 처리 여부
8. cooldown exit_i + 31 여부
9. 수수료 0.08% 차감 여부
10. position_fraction 0.01 여부
11. cd_value가 max_return_pct 기준인지 여부
