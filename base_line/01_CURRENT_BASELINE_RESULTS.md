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
외부 runner import: 없음
외부 json config 참조: 없음

데이터 분리
- train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.
- 2026 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.

1. short_max 기준선
전략명: short_max_v7_devw120_actual_bar_engine
축: short_max
기준선 버전: base_line/short_max/v8
구전략 기반: short_max_v7_devw120
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v8
결과 출처: local_results/short_max/short_actual_bar_engine_train_to_20251231_v2_results

2025 train 기준 결과
trades: 45500
wins: 6251
losses: 39249
win_rate_pct: 13.738461538461538
final_return_pct: 1422.7683542126408
max_return_pct: 1424.4317435070927
max_drawdown_pct: 6.104584306764704
official_cd_value: 1431.3715225256192
profit_factor: 1.4976180824186338
max_conc: 299
max_conc_unique_symbols: 299
same_bar_trades: 3786
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 205
generated_entry_candidates: 45705
executed_entries: 45500
load_errors: 0

기존 구엔진 reference 결과
strategy: short_max_v7_devw120
trades: 43681
max_return_pct: 1221.9746135454966
max_drawdown_pct: 5.6636954922983485
official_cd_value: 1247.1019969487918

차이
delta_cd_vs_old_engine: +184.2695255768274
delta_mdd_vs_old_engine: +0.44088881446635586
delta_trades_vs_old_engine: +1819
판단: short_max 공식 기준선으로 승격한다. 이후 short_max 개선은 v8 기준으로 한다.

2. short_main 기준선
전략명: short_main_v6_timeout210_actual_bar_engine
축: short_main
기준선 버전: base_line/short_main/v7
구전략 기반: short_main_v6_timeout210
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main/v7
결과 출처: local_results/short_max/short_actual_bar_engine_train_to_20251231_v2_results

2025 train 기준 결과
trades: 35330
wins: 4997
losses: 30333
win_rate_pct: 14.143787149731107
final_return_pct: 1114.6701489565148
max_return_pct: 1115.0033786152128
max_drawdown_pct: 4.607649926423363
official_cd_value: 1159.0202763344078
profit_factor: 1.5743323511471792
max_conc: 284
max_conc_unique_symbols: 284
same_bar_trades: 3187
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 39
generated_entry_candidates: 35369
executed_entries: 35330
load_errors: 0

기존 구엔진 reference 결과
strategy: short_main_v6_timeout210
trades: 33989
max_return_pct: 931.6464095007982
max_drawdown_pct: 4.506694290977831
official_cd_value: 985.153259660748

차이
delta_cd_vs_old_engine: +173.8670166736598
delta_mdd_vs_old_engine: +0.10095563544553254
delta_trades_vs_old_engine: +1341
판단: short_main 공식 기준선으로 승격한다. 이후 short_main 개선은 v7 기준으로 한다.

3. long_main 기존 기준선
전략명: 6V2_L01_doubleflush_core
축: long_main
기존 reference 결과
trades: 592
max_return_pct: 23.919060
max_drawdown_pct: 1.751183
official_cd_value: 121.749029
상태: 아직 actual bar engine 기준 재산출 전이다. 숏 계열과 같은 시간 처리 문제가 있을 수 있으므로 추후 재산출 필요.

4. long_max 기존 기준선
전략명: 8V4_V51_V002_core_rare22_c1
축: long_max
기존 reference 결과
trades: 2276
max_return_pct: 44.266371
max_drawdown_pct: 6.758722
official_cd_value: 134.515867
상태: 아직 actual bar engine 기준 재산출 전이다. 숏 계열과 같은 시간 처리 문제가 있을 수 있으므로 추후 재산출 필요.

운영 판단
short_main과 short_max는 actual bar engine 기준으로 새 기준선 승격 완료.
이후 숏 계열 후보 개발은 반드시 actual bar engine과 2025 train / 2026 holdout 분리 규칙을 따른다.
구엔진 결과는 참고값으로만 사용한다.
