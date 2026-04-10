from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v63b_long_only_split_architectures'
base.BASELINE_NAME = 'long_split_baseline'

if __name__ == '__main__':
    base.main()
