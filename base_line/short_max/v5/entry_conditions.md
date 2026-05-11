# short_max v5 진입 조건과 청산 조건

## 전략명

SM16_C05_remove_no_rsi_dev035

## short_max v5 기록명

short_max_v5_SM16_C05_remove_no_rsi_dev035

## 전략 목적

RSI 직접 gate를 제거하고, EMA20 대비 과열 이격과 상단 꼬리, 강화된 score 조건으로 숏 리버전 진입을 수행한다.

short_max 기준에서는 official_cd_value 1위를 목표로 한다. 이 전략은 short_main v4 기준선이기도 하지만, official_cd_value가 이전 short_max v4를 크게 넘었으므로 short_max v5 기준선으로도 사용한다.

## 1. 공통 실행 조건

```python
initial_asset = 100.0
position_fraction = 0.01
fee_per_side = 0.0004
round_trip_fee = 0.0008
min_bars = 120
entry_on_next_bar_open = True
allow_long = False
allow_short = True
csv_file_count = 597
```

## 2. 지표

필수 지표:

- EMA20
- RSI14
- ATR14
- body
- upper_wick
- short_score

계산 방식:

```python
ema20 = close.ewm(span=20, adjust=False).mean()

avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
rsi14 = 100 - 100 / (1 + avg_gain / avg_loss)

true_range = max(high - low, abs(high - prev_close), abs(low - prev_close))
atr14 = true_range.ewm(alpha=1/14, adjust=False).mean()

body = abs(close - open)
upper_wick = high - max(open, close)
```

## 3. 숏 진입 기본식

v5 short_signal 조건:

```python
close / ema20 - 1 >= 0.035
upper_wick >= 1.3 * body
short_score >= 2.35
expected_tp >= 0.003
```

사용하지 않는 직접 gate:

```python
rsi14 > 77.0
```

즉 RSI 직접 gate는 사용하지 않는다.

## 4. RSI의 역할

RSI 직접 gate는 제거되었지만 RSI 지표는 제거하지 않는다.

RSI는 short_score 계산 내부에서 보조 점수로만 사용한다.

```python
raw_rsi = max(0.0, rsi14 - 77.0)
rsi_score = clip(raw_rsi / 10.0, 0.0, 2.0)
```

따라서 RSI가 77을 넘으면 점수에 가산점이 붙지만, RSI가 77을 넘지 않아도 dev/wick/score가 충분하면 진입할 수 있다.

## 5. score 계산

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

진입 점수 기준:

```python
score_min_short = 2.35
```

## 6. v5 핵심 파라미터

```python
short_dev = 0.035
short_rsi_min = 77.0
use_rsi_gate = False
short_wick_mult = 1.3
score_min_short = 2.35
atr_stop_mult = 1.8975
rr_mult = 5.75
min_expected_tp = 0.003
timeout_bars = 200
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
time_reduce_bars = 8
time_reduce_to_risk_frac = 0.05
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
```

## 7. 진입가

신호 캔들 i에서 조건을 만족하면 i+1 캔들의 open으로 숏 진입한다.

```python
entry = open[i + 1]
```

close 진입으로 바꾸면 기준선이 아니다.

## 8. 스탑과 타겟

숏 포지션 기준:

```python
risk = atr14[i] * 1.8975
stop = entry + risk
target = entry - 5.75 * risk
expected_tp = (entry - target) / entry
```

진입 후보는 다음 조건을 만족해야 한다.

```python
stop > entry
target > 0
expected_tp >= 0.003
```

## 9. 청산 우선순위

숏 포지션에서 같은 캔들에 stop과 target이 동시에 닿으면 stop을 먼저 적용한다.

청산 순서:

```python
if high >= stop:
    exit = stop
elif low <= target:
    exit = target
elif bars_since_entry >= 10 and mfe_r < 0.1 and close > entry:
    exit = close
elif bars_since_entry >= 200:
    exit = close
```

## 10. time_reduce 보호

진입 후 8봉 이상 지났고 MFE가 양수이면 stop을 entry + 0.05R 이하로 낮춘다.

숏 기준으로 stop은 낮아질수록 위험이 줄어든다.

```python
if bars_since_entry >= 8 and mfe_r > 0:
    stop = min(stop, entry + risk * 0.05)
```

## 11. fail_fast

```python
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
```

진입 후 10봉 이상 지났고 MFE가 0.1R 미만이며 close > entry이면 close로 청산한다.

## 12. timeout

```python
timeout_bars = 200
```

진입 후 200봉 이상 지나면 close로 청산한다.

## 13. dd_brake

```python
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
```

포트폴리오 평가 중 현재 drawdown이 -3% 이하로 내려가면 5 timestamp 동안 신규 진입을 멈춘다.

중요:
이 조건은 개별 트레이드 생성 단계가 아니라 포트폴리오 실행 단계에서 작동한다.

## 14. same-bar 처리

entry_ts == exit_ts인 거래는 포트폴리오 평가 단계에서 신규 진입 직후 같은 timestamp에서 즉시 청산한다.

이 처리를 하지 않으면 active_leftover가 생기거나 기준선 수익률이 어긋날 수 있다.

## 15. 승격 기준 충족 여부

- short_max 기준 official_cd_value 1위: 충족
- MDD 10% 미만: 충족. 4.6783483625391975
- trades 20,000 이상: 충족. 31,798
- active_leftover 0: 충족
- errors 0: 충족
- position_fraction 0.01: 충족
- fee_per_side 0.0004: 충족
- next bar open 진입: 충족

## 16. 향후 개선 시 금지 사항

1. 외부 경로, 외부 json, 외부 runner 참조 금지
2. fee_per_side 0.0004 유지
3. position_fraction 0.01 유지
4. next bar open 진입 유지
5. dd_brake를 개별 트레이드 생성 단계로 이동 금지
6. RSI 직접 gate 제거 상태를 기준선으로 인식할 것
7. score 내부 RSI 기여와 RSI 직접 gate 제거를 혼동하지 말 것
8. 기준선 진입 조건을 완전히 다른 전략으로 대체하지 말 것

## 17. 다음 개선 허용 범위

```python
short_dev: 0.0345 ~ 0.0360
score_min_short: 2.30 ~ 2.45
short_wick_mult: 1.2 ~ 1.4
rr_mult: 5.65 ~ 5.85
time_reduce_bars: 7 ~ 9
time_reduce_to_risk_frac: 0.04 ~ 0.06
fail_fast_bars: 8 ~ 12
dd_brake_trigger_pct: 0.025 ~ 0.035
dd_brake_freeze_steps: 3 ~ 7
```
