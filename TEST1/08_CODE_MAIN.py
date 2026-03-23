import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# NOTE
# This file is a checkpoint scaffold for the current backtest structure.
# The detailed probability engine logic is stored in TEST1/09_CODE_ENGINE.py.
# The original user workflow keeps these pieces:
# - symbol loop
# - excel result save
# - print summary
# - sequential simulation
# - plt equity curve

FILE_NAME = '5m CasinoProbEngine RESTORE v2'
EXCLUDE_SYMBOLS = {
    'BTCST/USDT', 'USDC/USDT', 'GAIB/USDT', 'XEM/USDT', 'VOXEL/USDT', 'BAKE/USDT', 'UNFI/USDT'
}


def expected_runtime_note():
    return 'Backtest can be slow because each bar rebuilds probability state from the latest 1500 candles.'


def current_design_note():
    return {
        'timeframe': '5m',
        'window': 1500,
        'long_short_same_time_allowed': True,
        'same_direction_pyramiding': False,
        'fee_rate_one_way': 0.0004,
        'initial_capital': 100,
        'leverage': 10,
        'position_split': 100,
    }


def current_paths_note():
    return {
        'symbol_list_csv': 'symbol_cost',
        'ohlcv_path_pattern': '코인/Data/time/{SYMBOL}_5m.xlsx',
        'trade_output_pattern': '코인/Data/cir/거래결과{FILE_NAME}.xlsx',
        'summary_output_pattern': '코인/Data/cir/{FILE_NAME}.xlsx',
        'sequential_output_pattern': '코인/Data/cir/순차결과_{FILE_NAME}.xlsx',
    }


def checkpoint_summary():
    return {
        'engine_file': 'TEST1/09_CODE_ENGINE.py',
        'docs': [
            'TEST1/00_PROJECT_RULES.txt',
            'TEST1/01_STRATEGY_CORE.txt',
            'TEST1/02_ENGINE_SPEC.txt',
            'TEST1/03_FEATURE_SPEC.txt',
            'TEST1/05_CURRENT_RESULT.txt',
            'TEST1/06_PROBLEMS.txt',
            'TEST1/07_NEXT_STEP.txt',
            'TEST1/10_EXPERIMENT_LOG.txt',
        ]
    }


if __name__ == '__main__':
    print(FILE_NAME)
    print(expected_runtime_note())
    print(current_design_note())
    print(current_paths_note())
    print(checkpoint_summary())
