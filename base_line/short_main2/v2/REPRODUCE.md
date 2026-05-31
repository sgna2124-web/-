short_main2 v2 재현 가이드

공식 기준선
strategy: SM60_C03_stop240_score270_timeout315
runner strategy: SMAUD_C03_stop240_score270_timeout315_slip000000
candidate_key: C03_stop240_score270_timeout315
axis: short_main2
baseline_version: short_main2/v2
이전 기준선: short_main2/v1, SM52_B04_stop230_score270_single_retest
공식 결과 출처: local_results/short_main/SHORT_MAIN2_V2_C03_SINGLE_RETEST_V1_3_ENVLOCKED/single_retest_summary_compact.csv
Q4 및 실전성 점검 출처: local_results/short_main/SHORT_MAIN2_V1_Q4_REALISM_RECHECK_V1_2_1_MEMFIX/q4_realism_summary_compact.csv
공식 러너: short_main2_v2_C03_single_retest_v1_3_envlocked.py

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
포지션 수 제한: 없음

공식 실행 명령
python short_main2_v2_C03_single_retest_v1_3_envlocked.py --out-dir ./local_results/short_main/SHORT_MAIN2_V2_C03_SINGLE_RETEST_V1_3_ENVLOCKED

외부 json config를 사용하지 않는다.
외부 runner import를 사용하지 않는다.
전략 조건은 실행 파일 내부에 내장한다.

공식 gate 값
trades: 152030
wins: 11364
losses: 140666
win_rate_pct: 7.4748404920081555
max_return_pct: 73746.55353592646
max_drawdown_pct: 5.888592725709996
official_cd_value: 69498.03075622236
profit_factor: 1.8286053579584032
generated_signals: 267412
executed_entries: 152030
blocked_entries: 0
same_bar_trades: 8883
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0
environment_lock_pass: True
gate_target_exact_retest_pass: True

실전성 gate 값
mtm_close_max_drawdown_pct: 15.017466599306728
mtm_worstbar_max_drawdown_pct: 14.23277215250176
mtm_worstbar_cd_value: 63347.67993125091
gate_realized_mdd10_pass: True
gate_mtm_worstbar_mdd_under_15: True

전략 핵심
short_main2 v2는 short_main2 v1의 climax_exhaustion 진입 조건을 그대로 유지한다.
v1 대비 변형된 부분은 다음뿐이다.
atr_stop_mult: 2.30 -> 2.40
timeout_bars: 285 -> 315
dd_brake_trigger_pct: 0.075 -> 0.080
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
atr_stop_mult: 2.40
rr_mult: 6.20
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
timeout_bars: 315
dd_brake_trigger_pct: 0.080
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
9. 기간 시작 전 신호로 기간 첫 캔들에 진입하지 않는다.
10. 2026 데이터는 지표 계산 전 제외한다.

2025년 4분기 특이점 및 실전성 점검
자동 판정: GENERAL_EDGE_CONFIRMED
FULL_TRAIN_TO_2025_END official_cd_value: 69498.03075622236
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 16979.64262769056
2025_Q4_ONLY official_cd_value: 390.894405739309
판정: 2025년 Q4를 제거해도 C03은 v1 기준선보다 강하며, Q4 단독 성과가 전체를 설명할 정도로 크지 않다. Q4 몰빵 전략이 아니다.

편도 0.05% 슬리피지 점검
FULL_TRAIN_TO_2025_END official_cd_value: 15177.194065003236
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 4617.4606705665265
2025_Q4_ONLY official_cd_value: 310.33515316809167
FULL_TRAIN_TO_2025_END mtm_worstbar_cd_value: 14001.429941017343
판정: 비용 스트레스 조건에서도 v1 기준선보다 우위가 유지된다.

재현 실패 시 확인 순서
1. CSV 파일 수가 597개인지 확인한다.
2. data-dir가 실제 OHLCV 5분봉 폴더인지 확인한다.
3. 2026 데이터가 지표 계산에 섞이지 않았는지 확인한다.
4. 수수료가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. leverage가 1.0인지 확인한다.
7. 포지션 수 제한이 없는지 확인한다.
8. same timestamp reentry 금지 엔진인지 확인한다.
9. forced_end 청산이 적용되었는지 확인한다.
10. 탐색 결과가 아니라 단독 리테스트 v1.3 결과를 공식값으로 사용한다.
