short_main v15 재현 가이드

목적
처음 보는 사람이 short_main v15 기준선을 같은 데이터셋에서 주관적 해석 없이 재현하도록 실행 조건과 gate 값을 고정한다.

공식 기준선
strategy: SM42_mdd10_aggr_v01_single_retest
axis: short_main
baseline_version: short_main/v15
이전 기준선: short_main/v14
이전 전략: smv12_topmix2_07_mix2_07_top1_reduce_frac000
공식 결과 출처: local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_SINGLE_RETEST_V4_2_ENVLOCKED/summary_compact.csv
공식 러너: base_line/short_main/v15/frozen_reproduce_runner.py
원본 개발 러너: short_main_mdd10_aggr_v01_single_retest_v4_2_envlocked.py

필수 데이터
OHLCV 5분봉 CSV 597개가 필요하다.
공식 데이터 경로 예시:
C:\Users\user\Desktop\LCD\파이썬\코인\Data\time

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
python base_line/short_main/v15/frozen_reproduce_runner.py --data-dir "C:\Users\user\Desktop\LCD\파이썬\코인\Data\time"

출력 폴더 예시
local_results/short_main/SHORT_MAIN_V15_FROZEN_REPRODUCE

외부 json config를 사용하지 않는다.
외부 runner import를 사용하지 않는다.
전략 조건은 frozen_reproduce_runner.py 내부에 내장한다.

공식 gate 값
아래 값과 일치해야 공식 재현 성공이다.
trades: 140827
wins: 11167
losses: 129660
max_return_pct: 25200.7456885644
max_drawdown_pct: 5.524791831439535
official_cd_value: 23902.932157469306
profit_factor: 1.7005605337643628
generated_signals: 239776
executed_entries: 140827
blocked_entries: 0
same_bar_trades: 10412
max_conc: 361
active_leftover: 0
pending_leftover: 0
load_errors: 0
environment_lock_pass: True

허용 오차
floating value 비교 허용 오차: 1e-9 수준.
trades, wins, losses, generated_signals, executed_entries, same_bar_trades, max_conc, active_leftover, pending_leftover는 정수 완전 일치.

실패 판정
BASELINE_GATE_FAILED_DO_NOT_USE.txt가 생성되면 공식 재현 실패다.
summary_compact.csv에 expected_gate_ok가 True이고 expected_gate_mismatches가 비어 있어야 한다.

전략 핵심
v15는 v14와 다른 신규축이다.
기존 v14는 EMA20 대비 과열, 윗꼬리, RSI 점수형 평균회귀 구조였다.
v15는 넓은 과열/급등/거래량/윗꼬리 클라이맥스 구조다.

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
climax_score_min: 2.8

청산/방어 핵심값
atr_stop_mult: 2.20
rr_mult: 6.20
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
timeout_bars: 270
dd_brake_trigger_pct: 0.070
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
결과 출처: local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_Q4_REGIME_CHECK_V4_3
자동 판정: GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14
FULL_TRAIN_TO_2025_END official_cd_value: 23902.932157469306
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 6891.0141
2025_Q4_ONLY official_cd_value: 329.1503
판정: 2025년 Q4를 제거해도 기존 v14 official_cd_value 6736.755883567657을 넘는다. Q4는 후반 복리 증폭에 기여했지만, Q4 특이점만으로 만들어진 전략은 아니다.

short_main 승격 기준
이번 v15는 기존 v14의 MDD 5% 미만 안정형 기준이 아니라 MDD 10% 미만 고 CD 기준으로 승격한다.
공식 리테스트 MDD는 5.524791831439535%이므로 MDD 10% 미만 조건을 통과한다.
기존 short_main v14보다 official_cd_value와 max_return_pct가 크게 개선되었다.

재현 실패 시 확인 순서
1. CSV 파일 수가 597개인지 확인한다.
2. data-dir가 실제 OHLCV 5분봉 폴더인지 확인한다.
3. 2026 데이터가 지표 계산에 섞이지 않았는지 확인한다.
4. 수수료가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. leverage가 1.0인지 확인한다.
7. same timestamp reentry 금지 엔진인지 확인한다.
8. forced_end 청산이 적용되었는지 확인한다.
9. period check와 기준선 리테스트를 혼동하지 않는다. 공식 기준선 값은 단독 리테스트 v4.2 결과다.
