from __future__ import annotations
import os
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v38_rr40_t60_adventurous.json'
DST = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.json'
V38_COMB_DEFAULT = 'experiments/combinations_json_only_timeout18_time_reduce_v38_rr40_t60_adventurous.json'
RUNNER = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py'

if __name__ == '__main__':
    backup = DST.read_text(encoding='utf-8')
    try:
        DST.write_text(SRC.read_text(encoding='utf-8'), encoding='utf-8')
        os.environ['V27_COMB'] = os.environ.get('V38_COMB', V38_COMB_DEFAULT)
        runpy.run_path(str(RUNNER), run_name='__main__')
    finally:
        DST.write_text(backup, encoding='utf-8')
