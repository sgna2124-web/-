short_main2 v5 재현 지침

목표
short_main2 v5 공식 기준선 V4R05_stop262_rr620_t390_ff15를 주관적 해석 없이 재현한다.

공식 기준선
strategy: V4R05_stop262_rr620_t390_ff15
axis: short_main2
baseline_version: base_line/short_main2/v5
previous_baseline: base_line/short_main2/v4, V3MIX07_N02_stop255_rr630_t375

필수 데이터
OHLCV CSV 폴더를 직접 지정한다.
기준 개발 환경의 데이터 위치는 다음과 같다.
C:/Users/user/Desktop/LCD/파이썬/코인/Data/time

CSV 파일 수
597개

데이터 사용 범위, 기준선 갱신용
train end: 2025-12-31 23:59:59
holdout start: 2026-01-01 00:00:00
2026 데이터는 기준선 갱신용 train에는 사용하지 않는다.

데이터 사용 범위, validation
2026 Q1은 별도 validation으로만 사용했다.
현재 데이터에서는 2026 Q2 유효 심볼 수가 0개로 확인되어 Q2 이후는 검증하지 않았다.

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

공식 재현 실행, 2025 train + Q4 점검
python short_main2_v4_V4R05_single_retest_q4_v1_2_1_memfix.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time" --out-dir ./local_results/short_main/SHORT_MAIN2_V5_OFFICIAL_RETEST_Q4

2026 validation 실행
python short_main2_v4_V4R05_2026_quarter_validation_v1_1_skip_empty.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time" --out-dir ./local_results/short_main/SHORT_MAIN2_V5_2026_VALIDATION

주의
현재 공식 전체 러너 파일명은 개발 당시 이름인 short_main2_v4_V4R05_single_retest_q4_v1_2_1_memfix.py를 그대로 사용한다.
전략 자체는 이 파일의 V4R05_stop262_rr620_t390_ff15 후보이며, short_main2/v5 공식 기준선으로 승격되었다.
파일명보다 base_line/short_main2/v5/STRATEGY.md의 전략 정의를 우선한다.

공식 기대값, no slippage, 2025 train
trades: 148281
wins: 10414
losses: 137867
win_rate_pct: 7.023151988454354
max_return_pct: 129234.32408204528
max_drawdown_pct: 5.692488096031778
official_cd_value: 121971.9830795917
profit_factor: 1.998821411024562
generated_signals: 267412
executed_entries: 148281
same_bar_trades: 6944
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0
mtm_close_max_drawdown_pct: 14.81208179975927
mtm_worstbar_max_drawdown_pct: 14.059033930133126
mtm_worstbar_cd_value: 111166.12280897668

정확 재현 판정
아래 값이 모두 일치해야 한다.
trades = 148281
official_cd_value = 121971.9830795917
max_drawdown_pct = 5.692488096031778
profit_factor = 1.998821411024562
mtm_worstbar_cd_value = 111166.12280897668

Q4 의존도 기대값
FULL_TRAIN_TO_2025_END official_cd_value: 121971.9830795917
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 26794.776804338213
2025_Q4_ONLY official_cd_value: 434.2372391750604
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

Q4 제외 기준 v4 대비 개선
v4 EXCL_Q4 official_cd_value: 23933.648521901203
v5 EXCL_Q4 official_cd_value: 26794.776804338213
delta_excl_q4_cd_vs_v4: +2861.12828243701

2026 validation 기대값, 현재 데이터 기준 Q1
v4 2026_Q1 official_cd_value: 108.34692571427838
v5 2026_Q1 official_cd_value: 109.22776166037053
delta_2026_q1_cd_vs_v4: +0.880835946092148

결과 파일 원칙
기본 실행에서는 전체 거래 기록을 저장하지 않는다.
--save-trades 옵션을 붙이지 않는다.
저장소에는 summary, compact summary, runtime, metadata, load_errors 중심으로 남긴다.
무거운 all_trades.csv 또는 trade_rows.csv는 기준선 기록용으로 남기지 않는다.

재현 실패 시 점검 순서
1. data_dir가 실제 OHLCV CSV 폴더인지 확인한다.
2. CSV 파일 수가 597개 근처인지 확인한다.
3. 2025 train 기준 재현 시 2026 데이터가 지표 계산 전에 제외되는지 확인한다.
4. fee_per_side가 0.0004인지 확인한다.
5. position_fraction이 0.01인지 확인한다.
6. leverage가 1.0인지 확인한다.
7. no_position_limit 조건인지 확인한다.
8. entry가 signal close 다음 bar open인지 확인한다.
9. same timestamp 청산 후 재진입이 차단되는지 확인한다.
10. stop/target 동시 터치 시 stop 우선인지 확인한다.
