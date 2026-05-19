현재 기준선 결과 기록

작성 목적
현재 데이터 기준으로 재현된 기준선 결과를 보존한다. 이후 전략 개선, clone audit, baseline gate, 기준선 승격 여부 판단의 기준 자료로 사용한다.

공식 성과 계산
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)

공식 체결/청산 엔진
2026-05-15부터 숏 계열 기준선은 actual bar engine 기준을 사용한다.

5분봉 timestamp가 12:00이면 해당 캔들은 12:00:00 ~ 12:04:59 구간이다.
따라서 12:00 캔들 내부에서 발생한 TP/SL 청산 결과는 12:00 open 신규 진입 판단에 사용할 수 없다.

공식 처리 규칙:
- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- same-bar TP/SL은 유지한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

실행 환경
launch_cwd: C:\Users\user\Desktop\LCD\파이썬
data_dir: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
csv_file_count: 597
initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
외부 runner import: 기준선 frozen runner 외 없음
외부 json config 참조: 없음

데이터 분리
- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.
- 2026 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.

1. short_max 현재 기준선
전략명: smv8_mix2_13_all_timereduce5
축: short_max
기준선 버전: base_line/short_max/v9
이전 기준선: base_line/short_max/v8
출처: short_max v8 derived mix2 candidate
선택 기준: short_max식, MDD 10% 미만, 리테스트 통과 후 official_cd_value 1위
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v9
결과 출처: local_results/short_max/short_max_v8_mix2_top_retest_v1_results/summary_compact.csv

2025 train 기준 결과
trades: 63105
wins: 7297
losses: 55808
win_rate_pct: 11.563267569923145
final_return_pct: 2743.319336054713
max_return_pct: 2743.3304850694603
max_drawdown_pct: 5.686879318598392
official_cd_value: 2681.6337117546423
profit_factor: 1.5925867541542813
max_conc: 307
max_conc_unique_symbols: 307
same_bar_trades: 4197
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 363
generated_entry_candidates: 63468
executed_entries: 63105
load_errors: 0

이전 short_max v8 기준선
strategy: short_max_v7_devw120_actual_bar_engine
trades: 45500
max_return_pct: 1424.4317435070927
max_drawdown_pct: 6.104584306764704
official_cd_value: 1431.3715225256192
profit_factor: 1.4976180824186338

차이
delta_cd_vs_v8: +1250.262189229023
delta_mdd_vs_v8: -0.41770498816631196
delta_trades_vs_v8: +17605
판단: short_max 공식 기준선으로 승격한다. 이후 short_max 개선은 v9 기준으로 한다.

2. short_main 현재 기준선
전략명: smv8_mix2_02_prev_mix18_top2_top3_timereduce6
축: short_main
기준선 버전: base_line/short_main/v10
이전 기준선: base_line/short_main/v9
출처: short_max v8 derived mix2 candidate
선택 기준: short_main식, MDD 5% 미만, 리테스트 통과 후 official_cd_value 1위
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main/v10
결과 출처: local_results/short_max/short_max_v8_mix2_top_retest_v1_results/summary_compact.csv

2025 train 기준 결과
trades: 50501
wins: 6382
losses: 44119
win_rate_pct: 12.637373517356092
final_return_pct: 1973.4390960274047
max_return_pct: 1973.4472303933733
max_drawdown_pct: 4.814092666588577
official_cd_value: 1973.629559329422
profit_factor: 1.5675065791005796
max_conc: 302
max_conc_unique_symbols: 302
same_bar_trades: 3533
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 119
generated_entry_candidates: 50620
executed_entries: 50501
load_errors: 0

이전 short_main v9 기준선
strategy: short_main_v9_wick120_dev03475_timeout215_actual_bar_engine
trades: 36791
max_drawdown_pct: 4.770262221769094
official_cd_value: 1233.487844954492

차이
delta_cd_vs_v9: +740.14171437493
delta_mdd_vs_v9: +0.04383044481948275
delta_trades_vs_v9: +13710
판단: short_main 공식 기준선으로 승격한다. 이후 short_main 개선은 v10 기준으로 한다.

3. 이전 short_main 참고 기준선
short_main v7: short_main_v6_timeout210_actual_bar_engine, CD 1159.0202763344078, MDD 4.607649926423363
short_main v8: short_main_v8_wick125_actual_bar_engine, CD 1198.1725532607445, MDD 4.612307655489422
short_main v9: short_main_v9_wick120_dev03475_timeout215_actual_bar_engine, CD 1233.487844954492, MDD 4.770262221769094

4. long_main 기존 기준선
전략명: 6V2_L01_doubleflush_core
축: long_main
기존 reference 결과
trades: 592
max_return_pct: 23.919060
max_drawdown_pct: 1.751183
official_cd_value: 121.749029
상태: 아직 actual bar engine 기준 재산출 전이다. 숏 계열과 같은 시간 처리 문제가 있을 수 있으므로 추후 재산출 필요.

5. long_max 기존 기준선
전략명: 8V4_V51_V002_core_rare22_c1
축: long_max
기존 reference 결과
trades: 2276
max_return_pct: 44.266371
max_drawdown_pct: 6.758722
official_cd_value: 134.515867
상태: 아직 actual bar engine 기준 재산출 전이다. 숏 계열과 같은 시간 처리 문제가 있을 수 있으므로 추후 재산출 필요.

운영 판단
short_max는 v9, short_main은 v10이 현재 공식 기준선이다.
이후 숏 계열 후보 개발은 반드시 actual bar engine과 2025 train / 2026 holdout 분리 규칙을 따른다.
구엔진 결과는 참고값으로만 사용한다.
