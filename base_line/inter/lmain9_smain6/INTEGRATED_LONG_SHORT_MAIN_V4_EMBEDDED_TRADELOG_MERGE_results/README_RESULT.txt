INTEGRATED_LONG_MAIN_V9_SHORT_MAIN_V6_V4_EMBEDDED_TRADELOG_MERGE

핵심 방식:
- long_main v9 기준선 전략 코드를 파일 안에 내장한다.
- short_main v6 기준선 전략 코드를 파일 안에 내장한다.
- 롱 단독 기준선 거래목록을 먼저 생성한다.
- 숏 단독 기준선 거래목록을 먼저 생성한다.
- 생성된 두 거래목록을 merged_trade_plan으로 합친다.
- merged_trade_plan을 entry_ts/exit_ts 시계열로 처리해서 1/800 실전 통합 결과를 산출한다.
- 런타임에 base_line, CORE_SUMMARY2, local_results의 전략 파일을 import/read 하지 않는다.

long_generated_trades: 57035
long_expected_trades: 57035
long_count_match: 1
short_generated_trades: 36542
short_expected_trades: 33989
short_count_match: 0
short_generated_before_guard: 36856
short_blocked_by_guard: 314

integrated_result:
trades: 93577
long_trades: 57035
short_trades: 36542
wins: 25471
losses: 68106
win_rate_pct: 27.2192953396668
final_return_pct: 50.06143242284355
max_return_pct: 50.07058059777785
max_drawdown_pct: 1.940006672416613
official_cd_value: 147.1592013208466
max_conc: 453
blocked_by_cap: 0
errors: 0

outputs:
- long_main_v9_generated_trades.csv
- short_main_v6_generated_trades.csv
- merged_trade_plan.csv
- integrated_closed_trades.csv or integrated_closed_trades_head.csv
- equity_curve.csv
- integrated_embedded_tradelogs.sqlite