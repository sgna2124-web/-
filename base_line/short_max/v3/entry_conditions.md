# short_max v3 진입 조건

## 전략명

short_max_v3_combo_dev033_timeout240

## 기본 방향

이 전략은 short_max v2 기준선의 과열 숏 리버전 구조를 유지한다.

핵심 변화는 두 가지다.

1. EMA20 대비 과열 이격 조건을 0.032에서 0.033으로 소폭 강화한다.
2. timeout 청산 시간을 200봉에서 240봉으로 늘린다.

즉, 더 강한 과열 신호만 선별하고, 목표가까지 갈 시간을 더 준다.

## 지표

필수 지표:

- EMA20
- RSI14
- ATR14
- body = abs(close - open)
- upper_wick = high - max(open, close)
- short_score

## 기본 신호 조건

신호 캔들 기준:

```python
short_dev_ok = close / ema20 - 1.0 >= 0.033
short_rsi_ok = rsi14 > 76.0
short_wick_ok = upper_wick >= 1.3 * body
```

기본 숏 신호:

```python
short_signal = short_dev_ok and short_rsi_ok and short_wick_ok
```

## short_score 계산

short_score는 신호 품질 점수다.

```python
raw_dev = max(0.0, close / ema20 - 1.0)
raw_rsi = max(0.0, rsi14 - 76.0)

dev_score = clip(raw_dev / 0.033, 0.0, 2.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)

wick_floor = max(abs(body), atr14 * 0.2, 1e-12)
wick_ratio = upper_wick / wick_floor
wick_score = clip(log1p(wick_ratio), 0.0, 2.5)

short_score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score
```

## score 필터 적용 위치

중요:

`short_score >= 2.0`은 종목별 신호 생성 단계가 아니라 포트폴리오 평가 단계에서 적용한다.

공식 기준선 재현 엔진에서는 종목별로 dev/rsi/wick/expected_tp 조건을 만족하는 거래 후보를 먼저 만들고, 전체 timestamp 평가 단계에서 score_min_short 조건을 적용한다.

```python
selected = [trade for trade in entry_trades_at_timestamp if trade.score >= 2.0]
```

이 조건을 entry mask 안에 먼저 넣으면 종목 내부 포지션 점유 순서가 달라져 기준선 재현이 깨질 수 있다.

## 진입 가격

진입은 신호 캔들의 종가가 아니라 다음 캔들의 open이다.

```python
entry_index = signal_index + 1
entry_price = open[entry_index]
```

## expected TP 조건

숏 포지션 기준:

```python
risk = atr14[signal_index] * 1.8975
stop = entry_price + risk
target = entry_price - 6.0 * risk
expected_tp = (entry_price - target) / entry_price
```

진입 후보는 다음 조건을 만족해야 한다.

```python
stop > entry_price
target > 0
expected_tp >= 0.003
```

## 청산 조건

청산 우선순위:

1. stop
2. target
3. fail_fast
4. timeout

숏 기준 stop/target이 같은 캔들에서 동시에 닿으면 stop을 우선한다.

```python
if high >= stop:
    exit = stop
elif low <= target:
    exit = target
elif bars_since_entry >= 10 and mfe < 0.1 and close > entry:
    exit = close
elif bars_since_entry >= 240:
    exit = close
```

## time_reduce 보호

진입 후 10봉 이상 지났고, MFE가 양수이면 stop을 entry + 0.05R 이하로 낮춘다.

```python
if bars_since_entry >= 10 and mfe > 0:
    stop = min(stop, entry + risk * 0.05)
```

## same-bar 처리

entry_ts == exit_ts인 거래는 포트폴리오 평가 단계에서 신규 진입 직후 같은 timestamp에서 즉시 청산한다.

이 처리를 하지 않으면 active_leftover가 생기거나 기준선 수익률이 어긋난다.

## 최종 핵심 파라미터

```python
short_dev = 0.033
short_rsi_min = 76.0
short_wick_mult = 1.3
score_min_short = 2.0
atr_stop_mult = 1.8975
rr_mult = 6.0
min_expected_tp = 0.003
timeout_bars = 240
time_reduce_bars = 10
time_reduce_to_risk_frac = 0.05
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
fee_per_side = 0.0004
position_fraction = 0.01
initial_asset = 100.0
```
