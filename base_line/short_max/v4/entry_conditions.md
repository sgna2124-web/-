# short_max v4 진입 조건

## 전략명

short_max_v4_combo_rsi755_timeout280

## 전략 구조

short_max v4는 과열 숏 리버전 전략이다.

EMA20 대비 가격이 충분히 과열되어 있고, RSI14가 높은 상태이며, 상단 꼬리가 body 대비 충분히 길 때 숏 후보를 만든다. 이후 포트폴리오 평가 단계에서 short_score가 2.0 이상인 후보만 실제 진입으로 선택한다.

## v3 대비 변경점

- short_rsi_min: 76.0 → 75.5
- timeout_bars: 240 → 280

## 필수 지표

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
short_rsi_ok = rsi14 > 75.5
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
raw_rsi = max(0.0, rsi14 - 75.5)

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

즉 종목별 거래 후보 생성 단계에서는 다음 조건만 본다.

```python
close / ema20 - 1.0 >= 0.033
rsi14 > 75.5
upper_wick >= 1.3 * body
expected_tp >= 0.003
```

그 뒤 전체 timestamp 평가 단계에서 다음 필터를 적용한다.

```python
selected = [trade for trade in entry_trades_at_timestamp if trade.score >= 2.0]
```

이 순서를 바꾸면 종목 내부 포지션 점유 순서가 달라져 기준선 재현이 깨질 수 있다.

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

숏 기준 같은 캔들에서 stop과 target이 동시에 닿으면 stop을 우선한다.

```python
if high >= stop:
    exit = stop
elif low <= target:
    exit = target
elif bars_since_entry >= 10 and mfe < 0.1 and close > entry:
    exit = close
elif bars_since_entry >= 280:
    exit = close
```

## time_reduce 보호

진입 후 10봉 이상 지났고 MFE가 양수이면 stop을 entry + 0.05R 이하로 낮춘다.

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
short_rsi_min = 75.5
short_wick_mult = 1.3
score_min_short = 2.0
atr_stop_mult = 1.8975
rr_mult = 6.0
min_expected_tp = 0.003
timeout_bars = 280
time_reduce_bars = 10
time_reduce_to_risk_frac = 0.05
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
fee_per_side = 0.0004
position_fraction = 0.01
initial_asset = 100.0
```

## 포트폴리오 평가 규칙

- 각 진입은 현재 equity의 1%로 계산한다.
- 수수료는 편도 0.04%, 왕복 0.08%다.
- top N 제한은 사용하지 않는다.
- max_active_cap은 사용하지 않는다.
- DD brake는 사용하지 않는다.
- loss streak freeze는 사용하지 않는다.
