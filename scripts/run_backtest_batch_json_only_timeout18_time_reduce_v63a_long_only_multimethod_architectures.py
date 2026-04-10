from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v63a_long_only_multimethod_architectures.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v63a_long_only_multimethod_architectures.json'
VSRC = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_multimethod.py'

spec = importlib.util.spec_from_file_location('vmultimod', str(VSRC))
vmultimod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vmultimod)

vmultimod.BASE_CONFIG_PATH = BASE
vmultimod.SINGLE_CHANGES_PATH = COMB

if __name__ == '__main__':
    vmultimod.main()
