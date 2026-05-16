# short_main v8 진입 조건

## 기준선

- strategy: `short_main_v8_wick125_actual_bar_engine`
- source_candidate: `SM21_A05_wick125`
- parent_strategy: `short_main_v6_timeout210_actual_bar_engine`
- previous_baseline: `short_main/v7`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`

## v7 대비 변경점

v8에서 v7 대비 바뀐 진입 조건은 하나다.

- `short_wick_mult`: 1.30 -> 1.25

그 외 진입 조건, 점수 계산, 청산 조건, DD brake, 수수료, 자산 분할, actual bar engine은 v7과 동일하다.

## 사용 데이터 범위

- train_end: `2025-12-31 23:59:59`
- holdout_start: `2026-01-01 00:00:00`
- 2026년 데이터는 검증용 holdout으로 남긴다.
- 2026년 이후 데이터는 결과 계산 후 제외하는 것이 아니라, 지표 계산 전부터 제외한다.

## 지표

각 심볼의 5분봉 OHLCV에서 다음 지표를 계산한다.

- EMA20: close 기준 EWM span 20, adjust false
- RSI14: close diff 기준 Wilder 방식 EWM alpha 1/14, adjust false
- ATR14: true range 기준 EWM alpha 1/14, adjust false
- body: abs(close - open)
- upper_wick: high - max(open, close)

## 신호 캔들 기준

신호는 캔들 `t`의 close가 확정된 뒤 평가한다.
실제 진입은 다음 캔들 `t+1` open에서 pending entry 방식으로 실행한다.

## 진입 필수 조건

신호 캔들 `t`에서 다음 조건을 모두 만족해야 한다.

1. 과열 이격 조건

`close[t] / EMA20[t] - 1 >= 0.035`

2. 윗꼬리 조건

`upper_wick[t] >= 1.25 * body[t]`

3. RSI direct gate 미사용

`use_rsi_gate = false`

RSI가 77 이상이어야 한다는 직접 조건은 사용하지 않는다.
다만 RSI는 아래 `short_score` 내부의 보조 점수로만 사용된다.

4. short_score 조건

`short_score[t] >= 2.35`

이 조건은 portfolio selection 단계에서 따로 거는 것이 아니라 entry mask 내부에서 적용한다.

5. 기대 TP 조건

다음 캔들 open을 entry로 잡았을 때 기대 TP 비율이 최소 0.3% 이상이어야 한다.

`expected_tp = (entry - target) / entry >= 0.003`

## short_score 계산

기본 값:

- short_dev: 0.035
- short_rsi_min: 77.0
- score_dev_weight: 1.0
- score_rsi_weight: 0.8
- score_wick_weight: 0.7
- score_dev_cap: 2.0
- score_rsi_cap: 2.0
- score_wick_cap: 2.5
- wick_atr_floor_mult: 0.2

계산:

```python
dev_raw = max(0.0, close / EMA20 - 1.0)
rsi_raw = max(0.0, RSI14 - 77.0)
wick_ratio = upper_wick / max(abs(body), ATR14 * 0.2, 1e-12)

dev_score = min(dev_raw / 0.035, 2.0)
rsi_score = min(rsi_raw / 10.0, 2.0)
wick_score = min(log1p(wick_ratio), 2.5)

short_score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score
```

## 진입 가격

진입 가격은 신호 캔들 `t`가 아니라 다음 캔들 `t+1`의 open이다.

```python
entry = open[t + 1]
```

## stop / target

진입 시점의 ATR은 신호 캔들 `t`의 ATR14를 사용한다.

```python
risk = ATR14[t] * 1.8975
stop = entry + risk
target = entry - 5.75 * risk
```

## actual bar engine 체결 순서

5분봉 timestamp가 `12:00`이면 해당 캔들은 `12:00:00 ~ 12:04:59` 구간이다.
따라서 12:00 캔들 내부의 TP/SL 청산 결과를 12:00 open 신규 진입 판단에 사용하면 안 된다.

처리 순서:

1. `t` open에서 `t-1` close에 만들어진 pending entry를 진입시킨다.
2. 같은 timestamp 후보는 score 높은 순서로 처리한다.
3. 같은 timestamp의 후보들은 동일 equity snapshot 기준으로 position_fraction 1%를 배정한다.
4. `t` 캔들의 high/low/close로 청산을 평가한다.
5. `t` 캔들 내부 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
6. `t` close에서 신규 신호가 생기면 `t+1` open pending entry로 등록한다.
7. 같은 timestamp에서 청산된 자금으로 즉시 재진입하지 않는다.
8. same-bar TP/SL은 허용한다.
9. DD brake는 `t` 캔들 종료 후 발생한 drawdown edge를 다음 timestamp부터 적용한다.
10. train 마지막까지 남은 active position은 마지막 close로 forced_end 청산한다.

## 포트폴리오 설정

- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- side: short only

## DD brake

- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5
- dd_brake_mode: edge_current

drawdown이 peak 대비 -3% 이하로 새롭게 진입하는 edge가 발생하면 다음 timestamp부터 5번의 pending entry 처리를 차단한다.

## 재현 체크포인트

정상 재현 시 2025년까지 train 구간에서 다음 값이 나와야 한다.

- trades: 35,803
- wins: 5,070
- losses: 30,733
- max_return_pct: 1156.1081244457819
- max_drawdown_pct: 4.612307655489422
- official_cd_value: 1198.1725532607445
- same_bar_trades: 3,246
- active_leftover: 0
- pending_leftover: 0
- load_errors: 0
