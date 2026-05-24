smv10_dev1 reverse long + original short 2026 result

data_dir: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
out_dir: C:\Users\user\Desktop\LCD\파이썬\local_results\reverse\smv10_dev1_reverse_long_plus_original_short_2026_lev10_split500_20260524_172812
csv_files: 597
loaded_symbols: 597
load_errors: 0

fixed conditions:
- 2026 data only
- leverage 10
- fee_per_side 0.0004
- position_fraction 1/500
- original short: smv10_dev1_01_v10_stop210_rr550
- reverse long: smv10_dev1_01_v10_stop210_rr550 inverted
- no external runner import
- no external json config

summary:
                                                              strategy                 source_strategy                                        data_scope  initial_asset  leverage  position_fraction  fee_per_side  round_trip_fee  trades  wins  losses  win_rate_pct  final_asset  final_return_pct  peak_asset  max_return_pct  max_drawdown_pct  official_cd_value  profit_factor  gross_profit  gross_loss  max_conc  max_conc_unique_symbols  same_bar_trades  generated_entry_candidates  executed_entries  blocked_by_guard  blocked_by_active_symbol  active_leftover_after_forced_close  pending_leftover            side_counts_json                              leg_counts_json                                                             exit_counts_json
smv10_dev1_01_v10_stop210_rr550__reverse_long_plus_original_short_2026 smv10_dev1_01_v10_stop210_rr550 2026_only_indicators_calculated_after_2026_filter          100.0      10.0              0.002        0.0004          0.0008    1155   157     998     13.593074   110.038104         10.038104  110.038104       10.038104          3.495356          106.19188       1.424931     33.660996   23.622893        30                       30               72                        1161              1155                 6                         0                                   0                 0 {"short": 849, "long": 306} {"original_short": 849, "reverse_long": 306} {"stop": 997, "timeout": 127, "target": 26, "forced_end": 4, "fail_fast": 1}
