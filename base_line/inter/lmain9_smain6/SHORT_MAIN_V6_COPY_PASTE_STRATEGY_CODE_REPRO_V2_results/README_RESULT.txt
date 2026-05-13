SHORT_MAIN_V6_COPY_PASTE_STRATEGY_CODE_REPRO_V2

방식:
- base_line/short_main/v6/strategy_code.py 원문을 그대로 복사 붙여넣기했다.
- 원문 전략 함수 블록은 수정하지 않았다.
- 그 아래에 OHLCV 로딩/거래목록 생성/portfolio-level edge_current runner만 추가했다.

                                      run_label                                                    method  raw_trades_from_strategy_code  generated_trades_before_guard  blocked_by_same_symbol  blocked_by_guard  trades  expected_trades  trades_match  wins  losses  win_rate_pct  same_bar_trades  expected_same_bar_trades  max_conc  expected_max_conc  active_leftover  final_return_pct  expected_final_return_pct  max_return_pct  expected_max_return_pct  max_drawdown_pct  expected_max_drawdown_pct  official_cd_value  expected_official_cd_value
SHORT_MAIN_V6_COPY_PASTE_STRATEGY_CODE_REPRO_V2 strategy_code_py_exact_copy_plus_minimal_portfolio_runner                          52481                          36856                   15625               314   36542            33989             0  5020   31522     13.737617             3938                      3112       284                277                0        526.745331                 931.143355      527.051093                931.64641          4.992791                   4.506694         595.743742                   985.15326