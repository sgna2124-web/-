from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'v82_short_base.json'
COMB = ROOT / 'experiments' / 'v82_short_combinations.json'
V56 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes.py'

spec = importlib.util.spec_from_file_location('v56mod', str(V56))
v56mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v56mod)

if __name__ == '__main__':
    v56mod.run_batch(BASE, COMB)
