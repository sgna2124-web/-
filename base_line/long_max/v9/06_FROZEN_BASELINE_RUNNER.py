# -*- coding: utf-8 -*-
"""long_max v9 기준선 완전 재현 실행 파일.

실행 예:
python base_line/long_max/v9/06_FROZEN_BASELINE_RUNNER.py

결과 저장:
./local_results/long_max/LONG_MAX_FROZEN_BASELINE_2025_V9/
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / "shared_frozen_runner_v09"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from runner_core import main

if __name__ == "__main__":
    main("long_max")
