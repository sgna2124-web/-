# short_max v5 기준선

## 공식 기준선명

SM16_C05_remove_no_rsi_dev035

## short_max v5 기록명

short_max_v5_SM16_C05_remove_no_rsi_dev035

## 승격 배경

이 전략은 원래 short_main v4 개발 중 발견되어 short_main 기준선으로 승격된 전략이다. 그러나 short_max의 기준은 단순히 `official_cd_value 1위`이므로, short_main v4 기준선인 `SM16_C05_remove_no_rsi_dev035`는 short_max v4 기준선이었던 `short_max_v4_combo_rsi755_timeout280`보다 높은 official_cd_value를 기록한다.

따라서 short_max 최신 기준선도 `SM16_C05_remove_no_rsi_dev035`로 갱신한다.

## 기준선 계보

- short_main 계보: `short_beh_dd_brake -> SM15_B10_rr575_tr8_f005 -> SM16_C05_remove_no_rsi_dev035`
- short_max 계보: `short_max_v3_combo_dev033_timeout240 -> short_max_v4_combo_rsi755_timeout280 -> SM16_C05_remove_no_rsi_dev035`

## 이전 short_max v4와 비교

이전 short_max v4:

- strategy: short_max_v4_combo_rsi755_timeout280
- trades: 36,430
- max_return_pct: 536.5429980399269
- max_drawdown_pct: 6.373508371397563
- official_cd_value: 595.9728767723071

새 short_max v5:

- strategy: SM16_C05_remove_no_rsi_dev035
- trades: 31,798
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361

v5 개선폭:

- trades: -4,632
- max_return_pct: +285.4439271331702
- max_drawdown_pct: -1.6951600088583655
- official_cd_value: +282.880288184129

## 공식 테스트 환경

- 기준 데이터 수: 597 CSV
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- entry: signal candle i -> next bar open i+1
- side: short only
- active_leftover: 0
- errors: 0

## 공식 성과

- trades: 31,798
- wins: 4,638
- losses: 27,160
- win_rate_pct: 14.585823007736334
- final_asset: 921.5165864710646
- final_return_pct: 821.5165864710646
- peak_asset: 921.9869251730971
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361
- pf: 1.5778442611030818
- max_conc: 275
- max_conc_unique_symbols: 275
- same_bar_trades: 4,559
- active_leftover: 0
- gross_profit: 2243.2086266460665
- gross_loss: 1421.6920401750067
- raw_trades_generated: 61,818
- errors: 0

## 핵심 변경 구조

이 전략은 RSI 직접 gate를 제거하고, dev와 score를 강화한 숏 리버전 전략이다.

핵심 조건:

- short_dev: 0.035
- use_rsi_gate: false
- short_rsi_min: 77.0
- short_wick_mult: 1.3
- score_min_short: 2.35
- atr_stop_mult: 1.8975
- rr_mult: 5.75
- timeout_bars: 200
- time_reduce_bars: 8
- time_reduce_to_risk_frac: 0.05
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

중요:
RSI 직접 gate는 제거되었지만 RSI 지표 자체는 제거하지 않는다. score 계산 내부에서 rsi_score를 만들 때 short_rsi_min 77.0은 그대로 사용한다. 즉 RSI가 77을 넘으면 score에 가산점이 붙지만, RSI가 77을 넘지 않아도 dev/wick/score 조건이 충분하면 진입할 수 있다.

## short_max v5 채택 이유

1. short_max 공식 기준인 official_cd_value가 현재 확인된 숏 전략 중 가장 높다.
2. 이전 short_max v4 대비 max_return_pct가 크게 높다.
3. 이전 short_max v4 대비 MDD도 더 낮다.
4. max_conc가 295에서 275로 낮아졌다.
5. 수수료 0.04%, 자산 1% 분할 진입 환경에서 확인되었다.
6. active_leftover 0, errors 0이다.

## 다음 개발 기준

앞으로 short_max 개발은 이 v5 기준선을 부모 전략으로 사용한다.

개선 시 우선 탐색 범위:

- short_dev: 0.0345, 0.0350, 0.0355, 0.0360
- score_min_short: 2.30, 2.35, 2.40, 2.45
- short_wick_mult: 1.2, 1.3, 1.4
- rr_mult: 5.65, 5.75, 5.85
- time_reduce_bars: 7, 8, 9
- time_reduce_to_risk_frac: 0.04, 0.05, 0.06
- dd_brake_trigger_pct: 0.025, 0.030, 0.035
- dd_brake_freeze_steps: 3, 5, 7

## 반드시 유지할 규칙

- 완전히 새로운 전략으로 바꾸지 않는다.
- SM16_C05_remove_no_rsi_dev035의 진입 구조를 부모로 유지한다.
- RSI 직접 gate 제거 상태를 기준선으로 인식한다.
- score 내부 RSI 기여는 유지한다.
- next bar open 진입을 유지한다.
- fee_per_side 0.0004를 유지한다.
- position_fraction 0.01을 유지한다.
- expected_tp >= 0.003을 유지한다.
- dd_brake는 개별 트레이드 생성 단계가 아니라 포트폴리오 평가 단계에서 작동한다.
- active_leftover 0을 유지한다.
