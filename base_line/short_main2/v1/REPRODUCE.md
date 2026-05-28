short_main2 v1 재현 가이드

공식 기준선
strategy: SM52_B04_stop230_score270_single_retest
source strategy: SM50_B04_stop230_score270
axis: short_main2
baseline_version: short_main2/v1
이전 기준선: short_main/v15
공식 결과 출처: local_results/short_main/SHORT_MAIN_V15_B04_SINGLE_RETEST_V5_2_ENVLOCKED/summary_compact.csv
Q4 점검 출처: local_results/short_main/SHORT_MAIN_V15_B04_Q4_REGIME_CHECK_V5_1/period_summary_compact.csv
공식 러너: short_main_v15_B04_single_retest_v5_2_envlocked.py

필수 데이터
OHLCV 5분봉 CSV 597개가 필요하다.
공식 데이터 경로 예시:
C:/Users/user/Desktop/LCD/파이썬/코인/Data/time

데이터 범위
train_end: 2025-12-31 23:59:59
holdout_start: 2026-01-01 00:00:00
2026 데이터는 기준선 산출에서 제외한다.
2026 데이터는 EMA, RSI, ATR, volume, return 지표 계산 전부터 제외한다.

공식 실행 환경
initial_asset: 100.0
position_fraction: 0.01
leverage: 1.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
loaded_symbols: 597
load_errors: 0

공식 실행 명령
python short_main_v15_B04_single_retest_v5_2_envlocked.py --out-dir ./local_results/short_main/SHORT_MAIN_V15_B04_SINGLE_RETEST_V5_2_ENVLOCKED

외부 json config를 사용하지 않는다.
외부 runner import를 사용하지 않는다.
전략 조건은 실행 파일 내부에 내장한다.

공식 gate 값
trades: 154015
wins: 11824
losses: 142191
max_return_pct: 53676.46264218497
max_drawdown_pct: 5.923149464550481
official_cd_value: 50591.202383140204
profit_factor: 1.7648350795085153
generated_signals: 267412
executed_entries: 154015
blocked_entries: 0
same_bar_trades: 9995
max_conc: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0
environment_lock_pass: True

gate 결과
gate_retest_match_strict: True
gate_retest_match_loose: True
gate_mdd10_search_pass: True
gate_short_main_improve_vs_v15: True
gate_v16_candidate: True

전략 핵심
short_main2 v1은 short_main v15의 climax_exhaustion 계열을 유지한다.
v15 대비 완화/확장된 부분은 다음이다.
climax_score_min: 2.8 -> 2.7
atr_stop_mult: 2.20 -> 2.30
timeout_bars: 270 -> 285
dd_brake_trigger_pct: 0.070 -> 0.075
rr_mult: 6.20 유지

진입 핵심값
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
atr_pct_min: 0.0008
atr_pct_max: 0.135
range_spike_min: 0.0
dist_roll_high20_min: -0.08
climax_score_min: 2.7

청산/방어 핵심값
atr_stop_mult: 2.30
rr_mult: 6.20
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
timeout_bars: 285
dd_brake_trigger_pct: 0.075
dd_brake_freeze_steps: 3

실제 바 엔진 규칙
1. t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
2. t 캔들 내부 청산 결과는 t open 신규 진입에 사용하지 않는다.
3. t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
4. t close에서 만들어진 신규 신호는 t+1 open pending entry가 된다.
5. same-bar TP/SL은 허용한다.
6. same-bar에서 stop과 target이 동시에 닿으면 stop 우선으로 처리한다.
7. DD brake는 t 캔들 종료 후 발생한 edge를 t+1부터 적용한다.
8. train 종료 시 남은 active position은 마지막 close로 forced_end 정산한다.

2025년 4분기 특이점 점검
자동 판정: GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14
FULL_TRAIN_TO_2025_END official_cd_value: 50591.2024
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 12736.7326
2025_Q4_ONLY official_cd_value: 378.1772
판정: 2025년 Q4를 제거해도 성과가 강하며, Q4 단독 성과가 전체를 설명할 정도로 크지 않다. Q4 몰빵 전략이 아니다.

재현 실패 시 확인 순서
1. CSV 파일 수가 597개인지 확인한다.
2. data-dir가 실제 OHLCV 5분봉 폴더인지 확인한다.
3. 2026 데이터가 지표 계산에 섞이지 않았는지 확인한다.
4. 수수료가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. leverage가 1.0인지 확인한다.
7. same timestamp reentry 금지 엔진인지 확인한다.
8. forced_end 청산이 적용되었는지 확인한다.
9. 탐색 결과가 아니라 단독 리테스트 v5.2 결과를 공식값으로 사용한다.
