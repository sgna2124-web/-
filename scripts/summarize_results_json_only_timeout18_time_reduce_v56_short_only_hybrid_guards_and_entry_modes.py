from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes'
base.BASELINE_NAME = 'short_hybrid_baseline_ddbrake'

if __name__ == '__main__':
    base.main()
