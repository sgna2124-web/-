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
전략명: smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540
축: short_max
기준선 버전: base_line/short_max/v12
이전 기준선: base_line/short_max/v11
선택 기준: short_max식, MDD 10% 미만, 기존 v11보다 official_cd_value가 높고 MDD가 낮음
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v12
결과 출처: local_results/short_max/short_max_v11_top_exit_combo_fast_1h_v1_results/summary_compact.csv

2025 train 기준 결과
trades: 63863
wins: 7025
losses: 56838
win_rate_pct: 11.000109609633121
final_return_pct: 4220.190005886
max_return_pct: 4220.190005886
max_drawdown_pct: 4.260534220480682
official_cd_value: 4136.12683229544
profit_factor: 1.7783712609125915
max_conc: 310
max_conc_unique_symbols: 310
same_bar_trades: 3477
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 169
generated_entry_candidates: 64032
executed_entries: 63863
load_errors: 0

이전 short_max v11 기준선
strategy: smv10_dev1_01_v10_stop210_rr550
trades: 64128
max_return_pct: 3942.1044355472736
max_drawdown_pct: 4.38893845928694
official_cd_value: 3864.6989594109964
profit_factor: 1.7555392280496656

차이
delta_cd_vs_v11: +271.4278728844438
delta_mdd_vs_v11: -0.12840423880625718
delta_trades_vs_v11: -265
판단: short_max 공식 기준선으로 승격한다. 이후 short_max 개선은 v12 기준으로 한다.

2. short_main 현재 기준선
전략명: smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540
축: short_main
기준선 버전: base_line/short_main/v13
이전 기준선: base_line/short_main/v12
선택 기준: short_main식, MDD 5% 미만, 기존 v12보다 official_cd_value가 높고 MDD가 낮음
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main/v13
결과 출처: local_results/short_max/short_max_v11_top_exit_combo_fast_1h_v1_results/summary_compact.csv

2025 train 기준 결과
trades: 63863
wins: 7025
losses: 56838
win_rate_pct: 11.000109609633121
final_return_pct: 4220.190005886
max_return_pct: 4220.190005886
max_drawdown_pct: 4.260534220480682
official_cd_value: 4136.12683229544
profit_factor: 1.7783712609125915
max_conc: 310
max_conc_unique_symbols: 310
same_bar_trades: 3477
active_leftover: 0
pending_leftover: 0
blocked_by_guard: 169
generated_entry_candidates: 64032
executed_entries: 63863
load_errors: 0

이전 short_main v12 기준선
strategy: smv10_dev1_01_v10_stop210_rr550
trades: 64128
max_return_pct: 3942.1044355472736
max_drawdown_pct: 4.38893845928694
official_cd_value: 3864.6989594109964
profit_factor: 1.7555392280496656

차이
delta_cd_vs_v12: +271.4278728844438
delta_mdd_vs_v12: -0.12840423880625718
delta_trades_vs_v12: -265
판단: MDD 4.260534220480682로 short_main식 5% 미만 조건을 통과하므로 short_main 공식 기준선으로도 승격한다. 이후 short_main 개선은 v13 기준으로 한다.

운영 판단
short_max는 v12, short_main은 v13이 현재 공식 기준선이다. 이후 숏 계열 후보 개발은 반드시 actual bar engine과 2025 train / 2026 holdout 분리 규칙을 따른다. 구엔진 결과는 참고값으로만 사용한다.
