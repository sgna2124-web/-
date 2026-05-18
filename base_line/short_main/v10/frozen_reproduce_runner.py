"""
short_main v10 frozen reproduce runner.

이 파일은 short_max/v8 frozen runner의 actual bar engine을 재사용하고,
공식 short_main v10 파라미터와 gate 값만 덮어쓴다.

실행:
python base_line/short_main/v10/frozen_reproduce_runner.py --data-dir "C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인\\Data\\time"
"""
from __future__ import annotations
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ENGINE_RUNNER = REPO / "short_max" / "v8" / "frozen_reproduce_runner.py"
if not ENGINE_RUNNER.exists():
    raise FileNotFoundError(f"required engine file not found: {ENGINE_RUNNER}")

ns = runpy.run_path(str(ENGINE_RUNNER), run_name="short_main_v10_engine")
CFG = ns["CFG"]
EXPECTED = ns["EXPECTED"]
main = ns["main"]

CFG.update(
    strategy="smv8_mix2_02_prev_mix18_top2_top3_timereduce6",
    axis="short_main",
    short_dev=0.035,
    short_wick_mult=1.3,
    score_min_short=2.35,
    score_dev_weight=1.3,
    score_rsi_weight=0.8,
    score_wick_weight=0.7,
    atr_stop_mult=2.0,
    rr_mult=5.5,
    min_expected_tp=0.003,
    timeout_bars=200,
    time_reduce_bars=6,
    fail_fast_bars=10,
)

EXPECTED.clear()
EXPECTED.update(
    trades=50501,
    max_return_pct=1973.4472303933733,
    max_drawdown_pct=4.814092666588577,
    official_cd_value=1973.629559329422,
    active_leftover=0,
    pending_leftover=0,
    load_errors=0,
)

# engine 출력명/metadata 일부는 원본 runner 문자열을 유지할 수 있으나,
# gate와 전략 파라미터는 위 short_main v10 공식값으로 고정된다.
if __name__ == "__main__":
    main()
