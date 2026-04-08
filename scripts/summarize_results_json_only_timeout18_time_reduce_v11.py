from __future__ import annotations
from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT=Path(__file__).resolve().parents[1]
base.RESULTS_DIR=ROOT/'results_json_only_timeout18_time_reduce_v11'
base.BASELINE_NAME='atr18975_t27_b17_r155_baseline'
if __name__=='__main__':
    base.main()
