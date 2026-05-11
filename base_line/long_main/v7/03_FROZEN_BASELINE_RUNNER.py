# -*- coding: utf-8 -*-
"""
long_main v7 frozen baseline runner

long_main v7과 long_max v3는 같은 공식 기준선 전략을 사용한다.

공식 전략:
8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110

공식 고정값:
- parent entry: orig_V09_extreme_vol18
- child entry: child::orig_V09_extreme_vol18::tp03
- atr_stop: 1.10
- rr_target: 2.90
- max_hold_bars: 21
- cooldown_bars: 31
- position_fraction: 0.01
- round_trip_cost_bps: 8.0

공식 결과:
- trades: 57114
- wins: 20911
- losses: 36203
- win_rate_pct: 36.6127394334
- final_return_pct: 240.7307747654
- max_return_pct: 241.3427142366
- max_drawdown_pct: 1.3408670828
- official_cd_value: 336.7657621418
- max_conc: 435
- errors: 0

중요:
중복 코드가 갈라지는 문제를 막기 위해 실제 frozen runner 본체는 아래 파일 하나로 고정한다.

base_line/long_max/v3/03_FROZEN_BASELINE_RUNNER.py

이 파일은 long_main v7 위치에서 실행해도 위 본체를 찾아 실행하는 얇은 실행 파일이다.
결과 폴더는 본체와 동일하게 실행 위치 기준 ./local_result/long_max/LONG_MAIN_V7_LONG_MAX_V3_FROZEN_BASELINE 에 생성된다.
"""

from __future__ import annotations

import runpy
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "base_line" / "long_max" / "v3" / "03_FROZEN_BASELINE_RUNNER.py").exists():
            return p
    raise FileNotFoundError("base_line/long_max/v3/03_FROZEN_BASELINE_RUNNER.py 를 찾지 못했다.")


def main() -> None:
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    runner = repo_root / "base_line" / "long_max" / "v3" / "03_FROZEN_BASELINE_RUNNER.py"
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
