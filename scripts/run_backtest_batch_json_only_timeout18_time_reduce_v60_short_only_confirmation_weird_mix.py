from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v60_short_only_confirmation_weird_mix.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v60_short_only_confirmation_weird_mix.json'
VCONF = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_confirmation.py'

spec = importlib.util.spec_from_file_location('vconfmod', str(VCONF))
vconfmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vconfmod)

vconfmod.BASE_CONFIG_PATH = BASE
vconfmod.SINGLE_CHANGES_PATH = COMB

if __name__ == '__main__':
    vconfmod.main()
