현재 기준선 결과 기록

공식 성과 계산
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)

공식 체결/청산 엔진
숏 계열 기준선은 actual bar engine 기준을 사용한다.

5분봉 timestamp가 12:00이면 해당 캔들은 12:00:00 ~ 12:04:59 구간이다. 따라서 12:00 캔들 내부에서 발생한 TP/SL 청산 결과는 12:00 open 신규 진입 판단에 사용할 수 없다.

공식 처리 규칙:
- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- same-bar TP/SL은 유지한다.
- same-bar에서 stop과 target이 동시에 닿으면 stop 우선으로 처리한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

실행 환경
- data_dir: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
- csv_file_count: 597
- initial_asset: 100.0
- position_fraction: 0.01
- leverage: 1.0
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- 외부 json config 참조: 없음

데이터 분리
- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.
- 2026 데이터는 EMA, RSI, ATR, volume, return 지표 계산 전부터 제외한다.

1. short_max 현재 기준선
전략명: smv12_topmix2_07_mix2_07_top1_reduce_frac000
축: short_max
기준선 버전: base_line/short_max/v13
이전 기준선: base_line/short_max/v12
선택 기준: short_max식, 기존 v12보다 official_cd_value가 높고 MDD가 낮음
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v13
결과 출처: local_results/short_max/short_max_v12_topmix2_07_retest_v2_results/summary_compact.csv

2025 train 기준 공식 단독 리테스트 결과
trades: 66572
wins: 5664
losses: 60908
win_rate_pct: 8.508081475695487
final_return_pct: 6864.507074601753
max_return_pct: 6864.507074601753
max_drawdown_pct: 3.2701695697124222
official_cd_value: 6736.755883567657
profit_factor: 2.190937542731158
max_conc: 305
max_conc_unique_symbols: 305
same_bar_trades: 3524
forced_end_trades: 12
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_max v12 기준선
strategy: smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540
trades: 63863
max_return_pct: 4220.190005886
max_drawdown_pct: 4.260534220480682
official_cd_value: 4136.12683229544
profit_factor: 1.7783712609125915

차이
delta_cd_vs_v12: +2600.629051272217
delta_mdd_vs_v12: -0.9903646507682602
delta_trades_vs_v12: +2709
delta_pf_vs_v12: +0.4125662818185667
판단: short_max 공식 기준선으로 유지한다. 이후 short_max 개선은 v13 기준으로 한다.

short_max v13 핵심 변경
진입 조건은 short_max v12 그대로 유지한다.
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
timeout_bars: 240
fail_fast_bars: 12
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4
atr_stop_mult: 2.15
rr_mult: 5.4

2. short_main 현재 기준선
전략명: SM42_mdd10_aggr_v01_single_retest
축: short_main
기준선 버전: base_line/short_main/v15
이전 기준선: base_line/short_main/v14
선택 기준: short_main식, MDD 10% 미만 후보 중 official_cd_value 최대
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main/v15
결과 출처: local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_SINGLE_RETEST_V4_2_ENVLOCKED/summary_compact.csv

2025 train 기준 공식 단독 리테스트 결과
trades: 140827
wins: 11167
losses: 129660
win_rate_pct: 7.9295873660590654
final_return_pct: 25200.7456885644
max_return_pct: 25200.7456885644
max_drawdown_pct: 5.524791831439535
official_cd_value: 23902.932157469306
profit_factor: 1.7005605337643628
generated_signals: 239776
executed_entries: 140827
blocked_entries: 0
max_conc: 361
same_bar_trades: 10412
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_main v14 기준선
strategy: smv12_topmix2_07_mix2_07_top1_reduce_frac000
trades: 66572
max_return_pct: 6864.507074601753
max_drawdown_pct: 3.2701695697124222
official_cd_value: 6736.755883567657
profit_factor: 2.190937542731158

차이
delta_cd_vs_v14: +17166.17627390165
delta_mdd_vs_v14: +2.254622261727113
delta_trades_vs_v14: +74255
delta_pf_vs_v14: -0.490377008966795
판단: short_main v15는 MDD 5% 안정형 기준은 아니지만, MDD 10% 미만 고 CD 기준에서 v14를 크게 초과하므로 short_main 공식 기준선으로 승격한다. 이후 short_main 개선은 v15 기준으로 한다.

short_main v15 핵심 변경
v15는 기존 v14의 EMA/RSI/윗꼬리 점수형 기준선과 다른 신규축이다.
entry_mode: climax_exhaustion
precompute_signals: True
short_dev: 0.025
ret12_min: 0.030
ret3_min: 0.004
volume_spike_min: 0.75
upper_range_ratio_min: 0.16
close_position_max: 0.94
green_streak_min: 0
ema20_slope12_min: -0.025
ema20_slope12_max: 0.095
climax_score_min: 2.8
atr_stop_mult: 2.20
rr_mult: 6.20
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
timeout_bars: 270
fail_fast_bars: 12
dd_brake_trigger_pct: 0.070
dd_brake_freeze_steps: 3

2025년 4분기 특이점 점검
결과 출처: local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_Q4_REGIME_CHECK_V4_3
자동 판정: GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14
Q4 제외 official_cd_value: 6891.0141
기존 v14 official_cd_value: 6736.755883567657
판단: Q4를 제거해도 v14를 넘으므로 Q4 특이점만으로 만들어진 전략은 아니다. 다만 전체 CD 23902.932157469306은 Q4 후반 복리 증폭 효과가 크다.

운영 판단
short_max는 v13, short_main은 v15가 현재 공식 기준선이다. 이후 숏 계열 후보 개발은 반드시 actual bar engine과 2025 train / 2026 holdout 분리 규칙을 따른다. 구엔진 결과는 참고값으로만 사용한다.

재현 관련 주의
공식값은 탐색 결과가 아니라 환경 잠금 단독 리테스트 v4.2 결과를 사용한다.
short_main v15 재현 gate 값:
- trades 140827
- max_return_pct 25200.7456885644
- max_drawdown_pct 5.524791831439535
- official_cd_value 23902.932157469306
- profit_factor 1.7005605337643628
- active_leftover 0
- pending_leftover 0
- load_errors 0
