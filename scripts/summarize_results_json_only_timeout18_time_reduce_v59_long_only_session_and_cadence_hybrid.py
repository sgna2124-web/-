from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v59_long_only_session_and_cadence_hybrid'
base.BASELINE_NAME = 'long_session_baseline_symbol1_dd_conf'

if __name__ == '__main__':
    base.main()
