from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'v83_long_base.json'
COMB = ROOT / 'experiments' / 'v83_long_combinations.json'
V57 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v57_long_only_hybrid_guards_and_entry_modes.py'

spec = importlib.util.spec_from_file_location('v57mod', str(V57))
v57mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v57mod)

if __name__ == '__main__':
    v57mod.run_batch(BASE, COMB)
