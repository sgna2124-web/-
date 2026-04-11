from pathlib import Path
import summarize_results_json_only_short_strict_cd as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v66_short_only_balanced_split_bridge_hybrid'
base.BASELINE_NAME = 'short_balanced_bridge_atr050_baseline'

if __name__ == '__main__':
    base.main()
