from __future__ import annotations
from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT=Path(__file__).resolve().parents[1]
base.RESULTS_DIR=ROOT/'results_json_only_timeout18_time_reduce_refine'
base.BASELINE_NAME='time_reduce_b16_r050_baseline'
if __name__=='__main__':
    base.main()
