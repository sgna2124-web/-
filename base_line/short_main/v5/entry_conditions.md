# short_main v5 진입 조건

## 전략명

SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

## 요약

EMA20 대비 가격 과열과 상단 꼬리, 강화된 short_score를 이용하는 숏 리버전 전략이다. RSI 직접 gate는 제거되어 있으며, RSI는 score 내부 가산점으로만 사용한다.

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

## 진입 조건

신호 캔들 i 기준:

```python
dev_ok = close[i] / ema20[i] - 1.0 >= 0.035
wick_ok = upper_wick[i] >= 1.3 * body[i]
score_ok = short_score[i] >= 2.35
```

최종 신호:

```python
short_signal = dev_ok and wick_ok and score_ok
```

중요:

```python
rsi14[i] > 77.0
```

위 조건은 직접 gate로 사용하지 않는다.

## RSI 역할

RSI 직접 gate는 false다.

```python
use_rsi_gate = False
```

하지만 RSI는 score 내부에서 다음처럼 사용된다.

```python
raw_rsi = max(0.0, rsi14 - 77.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)
```

따라서 RSI가 77을 넘으면 점수에 보탬이 되지만, RSI가 77을 넘지 않아도 dev_score와 wick_score가 충분하면 진입할 수 있다.

## 진입가

신호 캔들 i에서 조건을 만족하면 다음 캔들 open으로 진입한다.

```python
entry_index = i + 1
entry_price = open[entry_index]
```

## 리스크와 타겟

```python
risk = atr14[i] * 1.8975
stop = entry_price + risk
target = entry_price - 5.75 * risk
expected_tp = (entry_price - target) / entry_price
```

진입 후보는 다음 조건을 만족해야 한다.

```python
stop > entry_price
target > 0
expected_tp >= 0.003
```

## 청산 우선순위

숏 포지션 기준 같은 캔들에서 stop과 target이 동시에 닿으면 stop을 먼저 적용한다.

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

포트폴리오 평가 중 현재 drawdown이 -3% 이하로 처음 내려가는 edge에서 5 timestamp 동안 신규 진입을 멈춘다. drawdown이 -3% 이하로 계속 머무른다고 매 timestamp마다 freeze를 새로 연장하지 않는다.

## same-bar 처리

entry_ts == exit_ts인 거래는 포트폴리오 평가 단계에서 신규 진입 직후 같은 timestamp에서 즉시 청산한다.

이번 기준선의 same_bar_trades는 3,115다. 이 처리를 제거하면 재현이 깨진다.

## 공식 리테스트 결과

```python
trades = 34005
max_return_pct = 899.0095709169104
max_drawdown_pct = 4.559023920452521
official_cd_value = 953.4644856111984
generated_trades_before_score_filter = 34044
errors = 0
active_leftover = 0
```
