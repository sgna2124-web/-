INTEGRATED_LONG_MAIN_V9_SHORT_MAX_V7_V6_FROZEN_SHORT_RUNNER

핵심 방식:
- long_main v9 기준선 전략 코드를 파일 안에 내장한다.
- short_max v7 기준선 전략 코드를 파일 안에 내장한다.
- 롱 단독 기준선 거래목록을 먼저 생성한다.
- 숏 단독 기준선 거래목록을 먼저 생성한다.
- 생성된 두 거래목록을 merged_trade_plan으로 합친다.
- merged_trade_plan을 entry_ts/exit_ts 시계열로 처리해서 1/800 실전 통합 결과를 산출한다.
- 런타임에 base_line, CORE_SUMMARY2, local_results의 전략 파일을 import/read 하지 않는다.

long_generated_trades: 57035
long_expected_trades: 57035
long_count_match: 1
short_generated_trades: 43681
short_expected_trades: 43681
short_count_match: 1
short_generated_before_guard: 43833
short_blocked_by_guard: 152

integrated_result:
trades: 100716
long_trades: 57035
short_trades: 43681
wins: 26491
losses: 74225
win_rate_pct: 26.302672862305894
final_return_pct: 65.88566016364885
max_return_pct: 65.90080817948028
max_drawdown_pct: 1.9124056931679936
official_cd_value: 162.7281116788442
max_conc: 454
blocked_by_cap: 0
errors: 0

outputs:
- long_main_v9_generated_trades.csv
- short_max_v7_generated_trades.csv
- merged_trade_plan.csv
- integrated_closed_trades.csv or integrated_closed_trades_head.csv
- equity_curve.csv
- integrated_embedded_tradelogs.sqlite