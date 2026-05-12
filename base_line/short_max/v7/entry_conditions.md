# short_max v7 진입 조건과 청산 조건

## 전략명

short_max_v7_devw120

## 구조 요약

부모 기준선 `SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge`의 진입 구조를 유지하되, dev_score 가중치를 1.0에서 1.2로 높인 숏 리버전 전략이다.

RSI 직접 gate는 사용하지 않는다. RSI는 short_score 내부에서만 가산점으로 사용한다.

## 실행 환경

```python
initial_asset = 100.0
position_fraction = 0.01
fee_per_side = 0.0004
entry_on_next_bar_open = True
allow_short = True
allow_long = False
min_bars = 120
```

## 필수 지표

```python
ema20 = EMA(close, 20)
rsi14 = RSI(close, 14)
atr14 = ATR(high, low, close, 14)
body = abs(close - open)
upper_wick = high - max(open, close)
```

## score 계산

v7의 핵심 변경점은 `score_dev_weight = 1.2`다.

```python
raw_dev = max(0.0, close / ema20 - 1.0)
raw_rsi = max(0.0, rsi14 - 77.0)

dev_score = clip(raw_dev / 0.035, 0.0, 2.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)

wick_floor = max(abs(body), atr14 * 0.2, 1e-12)
wick_ratio = upper_wick / wick_floor
wick_score = clip(log1p(wick_ratio), 0.0, 2.5)

short_score = 1.2 * dev_score + 0.8 * rsi_score + 0.7 * wick_score
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

즉 아래 조건은 직접 진입 조건이 아니다.

```python
rsi14[i] > 77.0
```

## RSI의 역할

RSI는 short_score 내부에서만 사용한다.

```python
raw_rsi = max(0.0, rsi14 - 77.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)
```

RSI가 77보다 높으면 점수가 올라가지만, RSI가 77 이하라도 dev와 wick 점수가 충분하면 진입 가능하다.

## 진입가

신호 캔들 i에서 조건을 만족하면 다음 캔들 open으로 숏 진입한다.

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

## 청산 우선순위

숏 포지션에서는 같은 캔들에서 stop과 target이 동시에 닿으면 stop을 우선한다.

```python
if high >= stop:
    exit_price = stop
    reason = "stop"
elif low <= target:
    exit_price = target
    reason = "target"
elif bars_since_entry >= 10 and mfe_r < 0.1 and close > entry_price:
    exit_price = close
    reason = "fail_fast"
elif bars_since_entry >= 200:
    exit_price = close
    reason = "timeout"
```

## time_reduce

진입 후 8봉 이상 지났고 MFE가 양수이면 stop을 entry + 0.05R 이하로 낮춘다.

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

현재 drawdown이 -3% 이하로 처음 내려가는 edge에서 5 timestamp 동안 신규 진입을 멈춘다. drawdown이 -3% 이하로 계속 머무른다고 매 timestamp마다 freeze를 새로 연장하지 않는다.

## same-bar 처리

entry_ts == exit_ts인 거래는 포트폴리오 평가 단계에서 신규 진입 직후 같은 timestamp에서 즉시 청산한다.

## 공식 리테스트 결과

```python
trades = 43681
max_return_pct = 1221.9746135454966
max_drawdown_pct = 5.6636954922983485
official_cd_value = 1247.1019969487918
generated_trades_before_score_filter = 43833
active_leftover = 0
errors = 0
```
