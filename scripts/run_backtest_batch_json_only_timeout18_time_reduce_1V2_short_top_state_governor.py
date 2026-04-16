from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v86_short_state_governor_runnable.py'

spec = importlib.util.spec_from_file_location('v86mod', str(TARGET))
v86mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v86mod)

v86mod.BASE = ROOT / 'experiments' / '1V2_short_top_state_governor_base.json'
v86mod.COMB = ROOT / 'experiments' / '1V2_short_top_state_governor_combinations.json'

if __name__ == '__main__':
    v86mod.run_batch()
