from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v65_long_only_guarded_wick_split_hybrid'
base.BASELINE_NAME = 'long_guarded_wick_split_quarter_threequarters_baseline'

if __name__ == '__main__':
    base.main()
