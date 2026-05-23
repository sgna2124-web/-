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
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

실행 환경
- data_dir: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
- csv_file_count: 597
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- 외부 json config 참조: 없음

데이터 분리
- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.
- 2026 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.

1. short_max 현재 기준선
전략명: smv9_topcombo1_01_tr4_stop205_rr550
축: short_max
기준선 버전: base_line/short_max/v10
이전 기준선: base_line/short_max/v9
선택 기준: short_max식, MDD 10% 미만, 단독 리테스트 통과 후 official_cd_value 1위
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v10
결과 출처: local_results/short_max/short_max_v9_topcombo1_01_retest_v2_results/summary_compact.csv

2025 train 기준 결과
trades: 64339
wins: 7025
losses: 57314
win_rate_pct: 10.918727365983308
final_return_pct: 3689.4315334640614
max_return_pct: 3689.4315334640614
max_drawdown_pct: 4.629389056231814
official_cd_value: 3614.004004760479
profit_factor: 1.726703002070718
max_conc: 309
max_conc_unique_symbols: 309
same_bar_trades: 3945
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 207
generated_entry_candidates: 64546
executed_entries: 64339
load_errors: 0

이전 short_max v9 기준선
strategy: smv8_mix2_13_all_timereduce5
trades: 63105
max_return_pct: 2743.3304850694603
max_drawdown_pct: 5.686879318598392
official_cd_value: 2681.6337117546423
profit_factor: 1.5925867541542813

차이
delta_cd_vs_v9: +932.3702930058366
delta_mdd_vs_v9: -1.0574902623665787
delta_trades_vs_v9: +1234
판단: short_max 공식 기준선으로 승격한다. 이후 short_max 개선은 v10 기준으로 한다.

2. short_main 현재 기준선
전략명: smv9_topcombo1_01_tr4_stop205_rr550
축: short_main
기준선 버전: base_line/short_main/v11
이전 기준선: base_line/short_main/v10
선택 기준: short_main식, MDD 5% 미만, 단독 리테스트 통과 후 official_cd_value 1위
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main/v11
결과 출처: local_results/short_max/short_max_v9_topcombo1_01_retest_v2_results/summary_compact.csv

2025 train 기준 결과
trades: 64339
wins: 7025
losses: 57314
win_rate_pct: 10.918727365983308
final_return_pct: 3689.4315334640614
max_return_pct: 3689.4315334640614
max_drawdown_pct: 4.629389056231814
official_cd_value: 3614.004004760479
profit_factor: 1.726703002070718
max_conc: 309
max_conc_unique_symbols: 309
same_bar_trades: 3945
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 207
generated_entry_candidates: 64546
executed_entries: 64339
load_errors: 0

이전 short_main v10 기준선
strategy: smv8_mix2_02_prev_mix18_top2_top3_timereduce6
trades: 50501
max_return_pct: 1973.4472303933733
max_drawdown_pct: 4.814092666588577
official_cd_value: 1973.629559329422
profit_factor: 1.5675065791005796

차이
delta_cd_vs_v10: +1640.374445431057
delta_mdd_vs_v10: -0.1847036103567627
delta_trades_vs_v10: +13838
판단: short_main 공식 기준선으로 승격한다. 이후 short_main 개선은 v11 기준으로 한다.

운영 판단
short_max는 v10, short_main은 v11이 현재 공식 기준선이다. 이후 숏 계열 후보 개발은 반드시 actual bar engine과 2025 train / 2026 holdout 분리 규칙을 따른다. 구엔진 결과는 참고값으로만 사용한다.
