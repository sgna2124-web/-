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

2. short_main2 현재 기준선
전략명: SM52_B04_stop230_score270_single_retest
원 탐색 전략명: SM50_B04_stop230_score270
축: short_main2
기준선 버전: base_line/short_main2/v1
이전 기준선: base_line/short_main/v15
선택 기준: short_main식, MDD 10% 미만 후보 중 official_cd_value 최대 + 단독 리테스트 재현 통과 + Q4 의존성 점검 통과
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main2/v1
결과 출처: local_results/short_main/SHORT_MAIN_V15_B04_SINGLE_RETEST_V5_2_ENVLOCKED/summary_compact.csv

2025 train 기준 공식 단독 리테스트 결과
trades: 154015
wins: 11824
losses: 142191
win_rate_pct: 7.6771743012044285
max_return_pct: 53676.46264218497
max_drawdown_pct: 5.923149464550481
official_cd_value: 50591.202383140204
profit_factor: 1.7648350795085153
generated_signals: 267412
executed_entries: 154015
blocked_entries: 0
max_conc: 364
same_bar_trades: 9995
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_main v15 기준선
strategy: SM42_mdd10_aggr_v01_single_retest

3. short_max2 현재 기준선
전략명: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1
원 탐색 전략명: smx2v1_devq4low_18_stop250_rr500_t320
축: short_max2
기준선 버전: base_line/short_max2/v2
이전 기준선: base_line/short_max2/v1
선택 기준: 2025-Q4 특수 구간 저비중, pre-Q4 월평균 수익과 MDD 우선, float64 단독 리테스트 통과
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max2/v2
결과 출처: local_results/short_max/short_max2_v1_q4low_top1_stop250_rr500_retest_v1_results/summary_compact.csv

2025 train 기준 공식 단독 리테스트 결과
trades: 65180
wins: 5130
losses: 60050
win_rate_pct: 7.8705124271248845
max_return_pct: 15588.585271121465
max_drawdown_pct: 2.274010039088681
official_cd_value: 15331.825267065175
profit_factor: 2.6142284817799504
positive_month_ratio_pct: 93.24324324324324
q4_share_of_full_return_pct: 77.19914436251436
top3_month_share_pct: 77.40116227608569
active_leftover: 0
pending_leftover: 0
load_errors: 0

Q4 제외 pre-Q4 공식 참고 결과
trades: 53580
wins: 4156
losses: 49424
win_rate_pct: 7.7566256065696155
max_return_pct: 3554.3308235947543
max_drawdown_pct: 2.1769570997805077
official_cd_value: 3574.7776092810404
profit_factor: 2.29014107209504
positive_month_ratio_pct: 92.95774647887323
avg_month_pnl: 50.0609975154197
positive_year_ratio_pct: 100.0

short_max2 v2 핵심 파라미터
진입 조건은 short_max2 v1 계열을 유지한다.
short_dev: 0.032
short_wick_mult: 1.30
score_min_short: 2.35
atr_stop_mult: 2.50
rr_mult: 5.00
timeout_bars: 320
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
fail_fast_bars: 12
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4

short_max2 v2 판정
v1 대비 pre-Q4 월평균 수익, MDD, CD, PF가 모두 개선되었고 full train에서도 CD와 PF가 개선되었다. 단, Q4 share와 top3 month share는 v1보다 약간 상승했으므로 이후 개선 방향은 수익 집중도 완화와 일반 구간 안정성 강화를 병행한다.
