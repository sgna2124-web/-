SHORT_MAIN_V6_ONLY_REPRO_V1_1

방식:
- short_main v6만 단독 재현한다.
- 전략 함수는 base_line/short_main/v6/strategy_code.py 구조를 내장했다.
- OHLCV에서 raw trade plan을 만들고 runner 제어 variant를 자동 시험한다.
- exact_match_full이 1이면 공식 숏 기준선 재현 성공이다.

raw_plans: 52481
errors: 0

official_targets:
trades=33989
generated_before_guard=34019
blocked_by_guard=30
same_bar_trades=3112
max_conc=277

best_variant:
                                        variant           same_symbol_mode close_due_mode dd_mode freeze_decrement dd_trigger_mode guard_count_position  trades  generated_trades_before_guard  blocked_by_guard  blocked_by_same_symbol  skipped  max_conc  active_leftover  wins  same_bar_trades  final_return_pct  max_return_pct  max_drawdown_pct  official_cd_value  score_distance_fast  losses  win_rate_pct  profit_factor  exact_match_core  exact_match_full  score_distance_full
signal_block_exit_i_plus_1|per_timestamp|dd_off signal_block_exit_i_plus_1  per_timestamp     off             none            none                 none   33685                          33685                 0                   18796        0       278                0  4789             3093        759.987014      760.406565          4.561387          821.16009               340410   28896     14.217011       1.431298                 0                 0               340600

exact_match: NONE