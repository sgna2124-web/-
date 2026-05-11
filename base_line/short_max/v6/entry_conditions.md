# short_max v6 진입 조건

## 전략명

SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

## 개요

EMA20 대비 과열 이격, 상단 꼬리, short_score를 이용하는 숏 리버전 전략이다. RSI 직접 gate는 제거되어 있고, RSI는 score 내부 보조 점수로만 사용된다.

## 실행 조건

```python
initial_asset = 100.0
position_fraction = 0.01
fee_per_side = 0.0004
entry_on_next_bar_open = True
allow_short = True
allow_long = False
min_bars = 120
```

## 지표

```python
ema20 = EMA(close, 20)
rsi14 = RSI(close, 14)
atr14 = ATR(high, low, close, 14)
body = abs(close - open)
upper_wick = high - max(open, close)
```

## score 계산

```python
raw_dev = max(0.0, close / ema20 - 1.0)
raw_rsi = max(0.0, rsi14 - 77.0)

dev_score = clip(raw_dev / 0.035, 0.0, 2.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)

wick_floor = max(abs(body), atr14 * 0.2, 1e-12)
wick_ratio = upper_wick / wick_floor
wick_score = clip(log1p(wick_ratio), 0.0, 2.5)

short_score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score
```

## entry mask

신호 캔들 i 기준:

```python
dev_ok = close[i] / ema20[i] - 1.0 >= 0.035
wick_ok = upper_wick[i] >= 1.3 * body[i]
score_ok = short_score[i] >= 2.35
short_signal = dev_ok and wick_ok and score_ok
```

직접 RSI gate는 사용하지 않는다.

```python
use_rsi_gate = False
```

## 진입가

```python
entry_index = signal_index + 1
entry_price = open[entry_index]
```

## stop / target

```python
risk = atr14[signal_index] * 1.8975
stop = entry_price + risk
target = entry_price - 5.75 * risk
expected_tp = (entry_price - target) / entry_price
```

진입 후보 필수 조건:

```python
stop > entry_price
target > 0
expected_tp >= 0.003
```

## 청산 조건

숏 포지션에서 같은 캔들에 stop과 target이 동시에 닿으면 stop 우선이다.

```python
if high >= stop:
    exit = stop
elif low <= target:
    exit = target
elif bars_since_entry >= 10 and mfe_r < 0.1 and close > entry_price:
    exit = close
elif bars_since_entry >= 200:
    exit = close
```

## time_reduce

```python
if bars_since_entry >= 8 and mfe_r > 0:
    stop = min(stop, entry_price + risk * 0.05)
```

## dd_brake

```python
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
dd_brake_mode = "edge_current"
```

현재 drawdown이 -3% 이하로 처음 내려가는 edge에서만 신규 진입 freeze를 건다. drawdown이 -3% 이하에 계속 머무른다고 freeze를 계속 연장하지 않는다.

## same-bar 처리

entry_ts == exit_ts인 거래는 같은 timestamp에서 즉시 청산한다.

## 공식 리테스트 결과

```python
trades = 34005
max_return_pct = 899.0095709169104
max_drawdown_pct = 4.559023920452521
official_cd_value = 953.4644856111984
generated_trades_before_score_filter = 34044
active_leftover = 0
errors = 0
```
