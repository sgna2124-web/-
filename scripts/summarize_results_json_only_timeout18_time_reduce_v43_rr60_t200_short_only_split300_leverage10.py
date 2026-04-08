from __future__ import annotations
from pathlib import Path
import summarize_results_json_only_short_strict as base
ROOT=Path(__file__).resolve().parents[1]
base.RESULTS_DIR=ROOT/'results_json_only_timeout18_time_reduce_v43_rr60_t200_short_only_split300_leverage10'
base.BASELINE_NAME='short_only_split300_1x'
if __name__=='__main__':
    base.main()
