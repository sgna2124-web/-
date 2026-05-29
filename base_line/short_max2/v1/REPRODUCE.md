short_max2 v1 재현 가이드

목적
Q4 저비중 순위 1위 후보 smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1을 동일 조건으로 재현한다.

실행 파일
base_line/short_max2/v1/frozen_reproduce_runner.py

실행 명령
python base_line/short_max2/v1/frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time"

메모리가 부족하면 다음처럼 chunk를 줄인다.
python base_line/short_max2/v1/frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time" --signal-chunk-size 5000

공식 데이터 조건
- CSV 폴더: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
- full train CSV 수: 597개
- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외한다.
- 2026 데이터는 지표 계산 전부터 제외한다.

pre-Q4 진단 조건
- pre-Q4 end: 2025-09-30 23:59:59
- 2025-Q4는 특수 고변동 구간으로 간주하고 일반 구간 평가에서 제외한다.
- pre-Q4 평가에서는 일부 심볼이 유효 데이터 부족으로 제외될 수 있다.
- 공식 기준선 gate는 full train 597개 결과를 우선한다.

공식 실행 환경
- initial_asset: 100.0
- position_fraction: 0.01
- leverage: 1.0
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- external config: 없음
- 외부 json: 없음

공식 엔진
- actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- same-bar TP/SL은 유지한다.
- 같은 캔들에서 stop과 target이 동시에 닿으면 stop 우선 처리한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.

전략 파라미터
- short_dev: 0.032
- short_wick_mult: 1.3
- score_min_short: 2.35
- atr_stop_mult: 2.45
- rr_mult: 5.2
- timeout_bars: 320
- time_reduce_bars: 3
- time_reduce_to_risk_frac: 0.00
- fail_fast_bars: 12
- dd_brake_trigger_pct: 0.035
- dd_brake_freeze_steps: 4

full train 재현 gate
다음 값과 일치해야 한다.

- trades: 65265
- wins: 5130
- losses: 60135
- win_rate_pct: 7.860262008733625
- max_return_pct: 14902.949980048708
- max_drawdown_pct: 2.2774507674795497
- official_cd_value: 14661.265180583516
- profit_factor: 2.567757993841345
- active_leftover: 0
- pending_leftover: 0
- load_errors: 0

pre-Q4 참고 gate
다음 값은 Q4 저비중 선정의 핵심 참고값이다.

- trades: 53649
- wins: 4158
- losses: 49491
- win_rate_pct: 7.750377453447409
- max_return_pct: 3466.4855917171863
- max_drawdown_pct: 2.2774507674795497
- official_cd_value: 3485.2606382365757
- profit_factor: 2.2589719429377744
- positive_month_ratio_pct: 92.95774647887323
- avg_month_pnl: 48.823740728411394
- positive_year_ratio_pct: 100.0

Q4 의존성 참고값
- q4_delta_return_pct: 11436.464388331522
- q4_share_of_full_return_pct: 76.73960124433124
- full_top3_month_share_pct: 76.94581060709373

결과 파일
실행 후 다음 경로에 결과가 생성된다.
C:/Users/user/Desktop/LCD/파이썬/local_results/short_max/short_max_v13_q4_low_weight_top1_stop245_rr520_retest_v1_results

생성 파일
- summary_compact.csv
- scored_summary.csv
- preq4_raw_summary.csv
- fulltrain_raw_summary.csv
- run_metadata.json

재현 실패 시 확인 순서
1. data_dir가 실제 OHLCV 5분봉 CSV 폴더인지 확인한다.
2. full train에서 CSV 597개가 로딩되는지 확인한다.
3. 수수료가 0.0004인지 확인한다.
4. position_fraction이 0.01인지 확인한다.
5. 2026 데이터가 지표 계산 전 제외되는지 확인한다.
6. same timestamp 청산 재진입 금지 규칙이 적용되는지 확인한다.
7. forced_end 청산이 적용되는지 확인한다.

판정
full train gate가 통과하면 short_max2/v1 기준선 재현 성공으로 본다. pre-Q4 값은 Q4 저비중 선정의 근거로 함께 확인한다.
