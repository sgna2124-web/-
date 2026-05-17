# -*- coding: utf-8 -*-
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / 'shared_frozen_runner_v09'
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from runner_core import main
if __name__ == '__main__':
    main('long_main')
