from __future__ import annotations
from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT=Path(__file__).resolve().parents[1]
base.RESULTS_DIR=ROOT/'results_json_only_timeout18_time_reduce_v34_adv_baseline_exploration'
base.BASELINE_NAME='adv_baseline_earlyreduce10_r005'
if __name__=='__main__':
    base.main()
