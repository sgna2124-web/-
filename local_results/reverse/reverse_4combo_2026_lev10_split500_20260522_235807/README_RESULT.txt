reverse 4-combo 2026 result

data_dir: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
out_dir: C:\Users\user\Desktop\LCD\파이썬\local_results\reverse\reverse_4combo_2026_lev10_split500_20260522_235807
csv_files: 597
loaded_symbols: 597
load_errors: 0

fixed conditions:
- 2026 data only
- leverage 10
- fee_per_side 0.0004
- position_fraction 1/500
- baseline conditions embedded in script
- no external runner import
- no external json config

summary:
                      combo_id             description                 legs                                        data_scope  initial_asset  leverage  position_fraction  fee_per_side  round_trip_fee  trades  wins  losses  win_rate_pct  final_asset  final_return_pct  peak_asset  max_return_pct  max_drawdown_pct  official_cd_value  profit_factor  gross_profit  gross_loss  max_conc  max_conc_unique_symbols  same_bar_trades  generated_entry_candidates  executed_entries  blocked_by_guard  blocked_by_active_symbol  blocked_by_cooldown  active_leftover_after_forced_close  pending_leftover              side_counts_json                         leg_counts_json                                                                   exit_counts_json
  REV_04_SMAX_LONG__LMAX_SHORT 숏 맥스 반전(롱) + 롱 맥스 반전(숏)   short_max+long_max 2026_only_indicators_calculated_after_2026_filter          100.0      10.0              0.002        0.0004          0.0008    6442  2012    4430     31.232536    90.118182         -9.881818  100.050462        0.050462         10.714242          89.330813       0.835952     50.355676   60.237494       222                      222              801                        6520              6442                78                         0                    0                                   0                 0  {"short": 6121, "long": 321}    {"long_max": 6121, "short_max": 321}                   {"stop": 4192, "target": 1635, "timeout": 590, "forced_end": 25}
 REV_03_SMAIN_LONG__LMAX_SHORT 숏 메인 반전(롱) + 롱 맥스 반전(숏)  short_main+long_max 2026_only_indicators_calculated_after_2026_filter          100.0      10.0              0.002        0.0004          0.0008    6344  2008    4336     31.651955    89.700732        -10.299268  100.061567        0.061567         11.240992          88.813654       0.826050     48.909061   59.208329       222                      222              805                        6465              6344               121                         0                    0                                   0                 0  {"short": 6089, "long": 255}   {"long_max": 6089, "short_main": 255}                   {"stop": 4098, "target": 1638, "timeout": 582, "forced_end": 26}
 REV_02_LMAIN_SHORT__SMAX_LONG 롱 메인 반전(숏) + 숏 맥스 반전(롱)  long_main+short_max 2026_only_indicators_calculated_after_2026_filter          100.0      10.0              0.002        0.0004          0.0008   12554  4028    8526     32.085391    81.251283        -18.748717  100.000000        0.000000         19.595518          80.404482       0.783802     67.971512   86.720229       265                      265             1977                       12592             12554                38                         0                    0                                   0                 0 {"short": 12241, "long": 313}  {"long_main": 12241, "short_max": 313} {"stop": 7031, "target": 3691, "fail_pnl": 1407, "timeout": 403, "forced_end": 22}
REV_01_LMAIN_SHORT__SMAIN_LONG 롱 메인 반전(숏) + 숏 메인 반전(롱) long_main+short_main 2026_only_indicators_calculated_after_2026_filter          100.0      10.0              0.002        0.0004          0.0008   12522  4029    8493     32.175371    80.012989        -19.987011  100.000000        0.000000         20.909330          79.090670       0.767299     65.904447   85.891458       265                      265             1987                       12538             12522                16                         0                    0                                   0                 0 {"short": 12277, "long": 245} {"long_main": 12277, "short_main": 245} {"stop": 6994, "target": 3698, "fail_pnl": 1411, "timeout": 396, "forced_end": 23}
