short_max v13 재현 가이드

목적
처음 보는 사람이 short_max v13 기준선을 같은 데이터셋에서 주관적 해석 없이 재현하도록 실행 조건과 gate 값을 고정한다.

공식 기준선
strategy: smv12_topmix2_07_mix2_07_top1_reduce_frac000
axis: short_max
baseline_version: short_max/v13
이전 기준선: short_max/v12
공식 결과 출처: local_results/short_max/short_max_v12_topmix2_07_retest_v2_results/summary_compact.csv
공식 러너 출처: run_short_max_v12_topmix2_07_retest_v2.py

필수 데이터
OHLCV 5분봉 CSV 597개가 필요하다.
공식 데이터 경로 예시:
C:\Users\user\Desktop\LCD\파이썬\코인\Data\time

데이터 범위
train_end: 2025-12-31 23:59:59
holdout_start: 2026-01-01 00:00:00
2026 데이터는 기준선 산출에서 제외한다.
2026 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.

공식 실행 환경
initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
loaded_symbols: 597
load_errors: 0

공식 실행 명령
python base_line/short_max/v13/frozen_reproduce_runner.py --data-dir "C:\Users\user\Desktop\LCD\파이썬\코인\Data\time"

현재 v13의 frozen_reproduce_runner.py는 공식 리테스트 러너 run_short_max_v12_topmix2_07_retest_v2.py의 조건과 gate 값을 기준으로 한다.
외부 json config를 사용하지 않는다.
외부 runner import를 사용하지 않는다.

공식 gate 값
아래 값과 일치해야 공식 재현 성공이다.
trades: 66572
max_return_pct: 6864.507074601753
max_drawdown_pct: 3.2701695697124222
official_cd_value: 6736.755883567657
profit_factor: 2.190937542731158
active_leftover: 0
pending_leftover: 0
load_errors: 0

실패 판정
BASELINE_GATE_FAILED_DO_NOT_USE.txt가 생성되면 공식 재현 실패다.
summary_compact.csv에 expected_gate_ok가 True이고 expected_gate_mismatches가 비어 있어야 한다.

전략 핵심
진입 조건은 short_max v12와 동일하다.
청산/방어 조건이 v13의 핵심이다.
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
timeout_bars: 240
fail_fast_bars: 12
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4
atr_stop_mult: 2.15
rr_mult: 5.4

실제 바 엔진 규칙
1. t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
2. t 캔들 내부 청산 결과는 t open 신규 진입에 사용하지 않는다.
3. t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
4. t close에서 만들어진 신규 신호는 t+1 open pending entry가 된다.
5. same-bar TP/SL은 허용한다.
6. DD brake는 t 캔들 종료 후 발생한 edge를 t+1부터 적용한다.
7. train 종료 시 남은 active position은 마지막 close로 forced_end 정산한다.

재현 실패 시 확인 순서
1. CSV 파일 수가 597개인지 확인한다.
2. data-dir가 실제 OHLCV 5분봉 폴더인지 확인한다.
3. 2026 데이터가 지표 계산에 섞이지 않았는지 확인한다.
4. 수수료가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. same timestamp reentry 금지 엔진인지 확인한다.
7. forced_end 청산이 적용되었는지 확인한다.
