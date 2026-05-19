# short_max v9 진입/청산 조건

## 버전 정의

- 기준선: short_max v9
- 전략명: smv8_mix2_13_all_timereduce5
- 축: short_max
- 출처: short_max v8 기반 mix2 후보
- 선택 기준: short_max식, MDD 10% 미만, 리테스트 통과 후 official_cd_value 1위

## 데이터 사용 범위

- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 이 기준선 산출에서 완전히 제외
- 2026 데이터는 지표 계산 전부터 제외하여 EMA, RSI, ATR에 섞이지 않음

## 지표

- EMA20: close 기준 ewm span 20, adjust false
- RSI14: Wilder 계열 ewm alpha 1/14, adjust false
- ATR14: true range의 ewm alpha 1/14, adjust false

## 진입 조건

캔들 `t` close 기준으로 다음 조건을 모두 만족하면 `t+1` open pending entry가 생성된다.

1. EMA 이격 조건

`close[t] / EMA20[t] - 1 >= 0.032`

2. 윗꼬리 조건

`upper_wick[t] >= 1.3 * body[t]`

여기서:

- `upper_wick = high - max(open, close)`
- `body = abs(close - open)`

3. RSI 직접 gate 없음

`use_rsi_gate = False`

RSI가 77보다 커야 한다는 직접 필터는 사용하지 않는다. 단, RSI는 short_score 계산 내부의 보조 점수로 사용한다.

4. short_score 조건

`short_score >= 2.35`

short_score 계산:

```python
raw_dev = max(0.0, close / EMA20 - 1.0)
raw_rsi = max(0.0, RSI14 - 77.0)

dev_score = clamp(raw_dev / 0.032, 0.0, 2.0)
rsi_score = clamp(raw_rsi / 10.0, 0.0, 2.0)

floor = max(abs(body), ATR14 * 0.2, 1e-12)
wick_score = clamp(log1p(max(0.0, upper_wick / floor)), 0.0, 2.5)

short_score = 1.3 * dev_score + 0.8 * rsi_score + 0.7 * wick_score
```

5. 기대 TP 조건

다음 봉 open을 entry로 잡았을 때 기대 TP 비율이 0.3% 이상이어야 한다.

```python
entry = open[t + 1]
stop = entry + ATR14[t] * 2.0
risk = stop - entry
target = entry - 5.5 * risk
expected_tp = (entry - target) / entry
expected_tp >= 0.003
```

## 청산 조건

1. Stop

`high >= stop`이면 stop 가격 청산.

2. Target

`low <= target`이면 target 가격 청산.

3. Time reduce

진입 후 5봉 이상 경과했고 MFE가 0보다 크면 stop을 다음 수준 이하로 축소한다.

`stop = min(stop, entry + risk * 0.05)`

4. Fail fast

진입 후 10봉 이상 경과했고, MFE가 0.1R 미만이며, close가 entry보다 높으면 close 청산.

5. Timeout

진입 후 200봉 이상 경과하면 close 청산.

6. Forced end

백테스트 train 구간 마지막까지 남은 포지션은 해당 심볼의 마지막 close로 forced_end 청산한다.

## 실제 바 엔진 시간 처리

- `t` open 진입은 반드시 `t-1` close에서 만들어진 신호만 사용한다.
- `t` 캔들 안에서 발생한 청산은 `t` open 신규 진입에 영향을 주면 안 된다.
- `t` 캔들 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
- `t` close에서 만들어진 신호는 `t+1` open 진입 후보가 된다.
- same-bar TP/SL은 허용한다.
- DD brake도 `t` 캔들 청산 후 발생한 edge를 `t+1`부터 적용한다.

## 포지션 사이징과 수수료

- initial_asset: 100.0
- position_fraction: 현재 equity의 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- short return 계산: `entry / exit - 1 - 2 * fee_per_side`

주의: position_fraction은 포지션당 1%다. 전체 총노출 1% 제한이 아니다.

## DD brake

- trigger: drawdown <= -3%
- freeze_steps: 5 timestamp
- mode: edge_current
- DD가 -3% 아래로 처음 진입하는 edge에서만 freeze를 건다.
- DD가 -3% 아래에 계속 머문다고 freeze를 계속 연장하지 않는다.
- actual bar engine에서는 `t` 캔들 청산 후 edge가 발생하면 `t+1`부터 적용한다.
