short_main2 v4 재현 지침

목표
short_main2 v4 공식 기준선 V3MIX07_N02_stop255_rr630_t375를 주관적 해석 없이 재현한다.

공식 기준선
strategy: V3MIX07_N02_stop255_rr630_t375
axis: short_main2
baseline_version: base_line/short_main2/v4
previous_baseline: base_line/short_main2/v3, MIX05_A02_A03_failfast14_rr630

필수 데이터
OHLCV CSV 폴더를 직접 지정한다.
기준 개발 환경의 데이터 위치는 다음과 같다.
C:/Users/user/Desktop/LCD/파이썬/코인/Data/time

CSV 파일 수
597개

데이터 사용 범위
train end: 2025-12-31 23:59:59
holdout start: 2026-01-01 00:00:00
2026 데이터는 기준선 산출에 사용하지 않는다.
2026 데이터는 EMA, RSI, ATR, volume, return 지표 계산 전부터 제외한다.

실행 환경
initial_asset: 100.0
position_fraction: 0.01
leverage: 1.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
slippage_per_side: 0.0
position_limit: 없음
외부 json config 참조: 없음
외부 전략 파일 참조: 없음

공식 엔진
actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231

공식 엔진 규칙
1. 5분봉 timestamp가 12:00이면 해당 캔들은 12:00:00 ~ 12:04:59 구간이다.
2. t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
3. t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
4. t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
5. 같은 timestamp에서 청산된 자리를 같은 timestamp 신규 진입에 재사용하지 않는다.
6. same-bar TP/SL은 허용한다.
7. same-bar에서 stop과 target이 동시에 닿으면 stop 우선으로 처리한다.
8. DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
9. train 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

공식 재현 실행
python short_main2_v3_V3MIX07_single_retest_q4_v1_3.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time" --out-dir ./local_results/short_main/SHORT_MAIN2_V4_OFFICIAL_RETEST_Q4

주의
현재 공식 전체 러너 파일명은 개발 당시 이름인 short_main2_v3_V3MIX07_single_retest_q4_v1_3.py를 그대로 사용한다.
전략 자체는 이 파일의 V3MIX07_N02_stop255_rr630_t375 후보이며, short_main2/v4 공식 기준선으로 승격되었다.
파일명보다 base_line/short_main2/v4/STRATEGY.md의 전략 정의를 우선한다.

공식 기대값, no slippage, 2025 train
trades: 149151
wins: 10603
losses: 138548
win_rate_pct: 7.108903057974804
max_return_pct: 113147.92211118022
max_drawdown_pct: 5.540389442518634
official_cd_value: 106973.54619066067
profit_factor: 1.9543969406097241
generated_signals: 267412
executed_entries: 149151
same_bar_trades: 7479
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0
mtm_close_max_drawdown_pct: 14.803514321510857
mtm_worstbar_max_drawdown_pct: 14.046920216852365
mtm_worstbar_cd_value: 97353.0658974033

정확 재현 판정
아래 값이 모두 일치해야 한다.
trades = 149151
official_cd_value = 106973.54619066067
max_drawdown_pct = 5.540389442518634
profit_factor = 1.9543969406097241
mtm_worstbar_cd_value = 97353.0658974033

Q4 의존도 기대값
FULL_TRAIN_TO_2025_END official_cd_value: 106973.54619066067
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 23933.648521901203
2025_Q4_ONLY official_cd_value: 425.66748937282097
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

Q4 제외 기준 v3 대비 개선
v3 EXCL_Q4 official_cd_value: 19227.287110761717
v4 EXCL_Q4 official_cd_value: 23933.648521901203
delta_excl_q4_cd_vs_v3: +4706.361411139485

결과 파일 원칙
기본 실행에서는 전체 거래 기록을 저장하지 않는다.
--save-trades 옵션을 붙이지 않는다.
저장소에는 summary, compact summary, runtime, metadata, load_errors 중심으로 남긴다.
무거운 all_trades.csv 또는 trade_rows.csv는 기준선 기록용으로 남기지 않는다.

재현 실패 시 점검 순서
1. data_dir가 실제 OHLCV CSV 폴더인지 확인한다.
2. CSV 파일 수가 597개 근처인지 확인한다.
3. 2026 데이터가 지표 계산 전에 제외되는지 확인한다.
4. fee_per_side가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. leverage가 1.0인지 확인한다.
7. no_position_limit 조건인지 확인한다.
8. entry가 signal close 다음 bar open인지 확인한다.
9. same timestamp 청산 후 재진입이 차단되는지 확인한다.
10. stop/target 동시 터치 시 stop 우선인지 확인한다.
