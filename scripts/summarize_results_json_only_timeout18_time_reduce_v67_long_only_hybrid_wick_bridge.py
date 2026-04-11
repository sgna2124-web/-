from pathlib import Path
import summarize_results_json_only_short_strict_cd as base
ROOT = Path(__file__).resolve().parents[1]
base.RESULTS_DIR = ROOT / 'results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge'
base.BASELINE_NAME = 'long_hybrid_wick_bridge_baseline'

if __name__ == '__main__':
    base.main()
