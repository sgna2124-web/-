from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v64_short_only_guarded_split_hybrid'
base.BASELINE_NAME = 'short_guarded_split_pure_atr050_2bar_baseline'

if __name__ == '__main__':
    base.main()
