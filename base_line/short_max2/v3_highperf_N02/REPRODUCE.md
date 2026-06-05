short_max2 v3_highperf_N02 reproduce guide

Baseline
SMX2V2_C08_EX20_02_N02_stop257_rr5075

Folder
base_line/short_max2/v3_highperf_N02

Full backtest runner
The full runner that produced the accepted result is:
run_short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3.py

Recommended command
python run_short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3.py --clean --max-runtime-min 180 --workers 4 --period-workers 1

Expected result folder
local_results/short_max/short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3_results

Required files in result folder
- retest_gate_2025.json
- run_metadata.json
- README_RESULT.txt
- period_summary.csv
- scored_summary.csv
- summary_full_unsorted.csv

Result verifier in this baseline folder
base_line/short_max2/v3_highperf_N02/frozen_result_verifier.py

Verification command after full runner completes
python base_line/short_max2/v3_highperf_N02/frozen_result_verifier.py --result-dir local_results/short_max/short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3_results

Expected verifier output
[OK] short_max2 v3_highperf_N02 frozen result verification passed

Expected metadata
status: OK_2025_GATE_PASSED_ALL_THROUGH_2026_RETEST_COMPLETED
csv_files: 597
period_workers: 1
fee_per_side: 0.0004
position_fraction: 0.01

2025 gate target
PRE-Q4:
trades: 88892
final_return_pct: 5636.697084804827
max_drawdown_pct: 5.655961392725716
official_cd_value: 5412.231712470644
profit_factor: 1.9410396856986845

FULL 2025:
trades: 104753
final_return_pct: 19461.28974837902
max_drawdown_pct: 5.655961392725716
official_cd_value: 18454.91075229149
profit_factor: 2.0040638913290496

All-through-2026 expected result
trades: 106337
final_return_pct: 20964.787242703645
max_drawdown_pct: 5.655961392725716
official_cd_value: 19873.371008796516
profit_factor: 2.0010696725618833

Period summary checks
2023_FULL_ONLY CD: 155.1021534263226
2024_FULL_ONLY CD: 230.31636637103094
2025_FULL_ONLY CD: 1537.5543844098192
2026_FULL_ONLY CD: 106.63924313928375

Important runtime note
Use --period-workers 1 for period_summary on Windows. Repeated ProcessPool creation during period splits may cause BrokenProcessPool if period workers are set too high.

Acceptance rule
The baseline is accepted only if:
1. retest_gate_2025.json has gate_ok true.
2. retest_gate_2025.json has gate_misses [].
3. frozen_result_verifier.py passes.

Current limitation
The complete full backtest runner file is referenced by exact filename and result path. The baseline folder now contains the verifier and all frozen target values. If the full runner file is moved, copy it into the working directory or run it from its existing project location using the command above.
