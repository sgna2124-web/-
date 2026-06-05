short_max2 v3_highperf_N02 baseline

Strategy
SMX2V2_C08_EX20_02_N02_stop257_rr5075

Axis
short_max2

Location
base_line/short_max2/v3_highperf_N02

Lineage
This baseline is not a direct overwrite of base_line/short_max2/v2. The v2 folder remains the official Q4-low branch. This folder records the separate v3 high-performance branch discovered from the combo08 expansion tests.

Core parameters
short_dev: 0.032
short_rsi_min: 76.0
short_wick_mult: 1.30
score_min_short: 2.35
atr_stop_mult: 2.57
rr_mult: 5.075
timeout_bars: 320
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.0
fail_fast_bars: 12
fail_fast_min_progress_r: 0.10
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4

Execution
engine: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231_FAST_SIGNAL_PRECOMPUTE_CHUNKED_MEMSAFE
csv_files: 597
fee_per_side: 0.0004
position_fraction: 0.01
initial_asset: 100.0
full_2025_end: 2025-12-31 23:59:59
all_end: 2026-12-31 23:59:59

2025 frozen gate
PRE-Q4: trades 88892, return 5636.697084804827, MDD 5.655961392725716, CD 5412.231712470644, PF 1.9410396856986845
FULL 2025: trades 104753, return 19461.28974837902, MDD 5.655961392725716, CD 18454.91075229149, PF 2.0040638913290496

All through 2026
trades 106337, return 20964.787242703645, MDD 5.655961392725716, CD 19873.371008796516, PF 2.0010696725618833

Year summary
2023: return 58.13785276936261, MDD 1.9196538272639008, CD 155.1021534263226, PF 1.8189380113743816
2024: return 134.59296305171026, MDD 1.822985917841291, CD 230.31636637103094, PF 1.9135547532977255
2025: return 1529.7313609927087, MDD 5.655961392725628, CD 1537.5543844098192, PF 2.098346033746182
2026: return 7.8345965695261865, MDD 1.1085064239765963, CD 106.63924313928375, PF 2.024525285956021

Judgement
The strategy is positive in 2023, 2024, and 2025. The largest expansion occurs in 2025. The 2026 period has low activity and only small positive contribution. This branch should be recorded as a high-performance short_max2 variant with a clear note that 2026 activity is low.
