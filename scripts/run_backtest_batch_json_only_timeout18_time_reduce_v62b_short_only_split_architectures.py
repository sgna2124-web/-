from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v62b_short_only_split_architectures.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v62b_short_only_split_architectures.json'
VSRC = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_split_entry.py'

spec = importlib.util.spec_from_file_location('vsplitmod', str(VSRC))
vsplitmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vsplitmod)

vsplitmod.BASE_CONFIG_PATH = BASE
vsplitmod.SINGLE_CHANGES_PATH = COMB

if __name__ == '__main__':
    vsplitmod.main()
