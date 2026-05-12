INTEGRATED_LONG_MAIN_V9_SHORT_MAIN_V6_V3_SHORT_EXACT

v3 핵심:
- 숏 same-side/same-symbol cooldown 제거
- 숏 max_per_symbol/max_active_cap 제한 없음
- 숏 dd_brake는 통합 equity가 아니라 숏 기준선 독립 equity(position_fraction=0.01) 기준 edge_current
- 롱/숏 전략 조건 함수는 통합용으로 재해석하지 않음

run_label: INTEGRATED_LONG_MAIN_V9_SHORT_MAIN_V6_V3_SHORT_EXACT
initial_asset: 100.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
position_fraction: 0.00125
max_total_positions: 800
allow_long_short_simultaneous: True
long_strategy: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350
short_strategy: short_main_v6_timeout210
symbol_files: 597
raw_long_candidates: 126615
raw_short_candidates: 52481
trades: 109204
long_trades: 57035
short_trades: 52169
wins: 27987
losses: 81217
win_rate_pct: 25.62818211787114
final_return_pct: 103.79712316800367
max_return_pct: 103.81750318383838
max_drawdown_pct: 1.9633713265642148
official_cd_value: 199.8158087678078
max_conc: 586
same_bar_trades: 20773
active_leftover: 0
blocked_by_cap: 0
blocked_by_long_cooldown: 69580
blocked_by_short_guard: 312
skipped_invalid: 0
errors: 0
short_guard_equity_final_return_pct: 7092.175321163421
short_guard_max_return_pct: 7097.931800618051
short_guard_max_drawdown_pct: 7.091630737380717
short_guard_max_conc: 586
short_expected_trades: 33989
short_expected_blocked_by_guard: 30
long_expected_trades: 57035
ruined: False