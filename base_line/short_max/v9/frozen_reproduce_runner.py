"""
short_max v9 frozen reproduce runner.

이 파일은 short_max/v8 frozen runner의 actual bar engine을 재사용하고,
공식 v9 파라미터와 gate 값만 덮어쓴다.
실행 위치와 무관하게 저장소 내부 base_line/short_max/v8/frozen_reproduce_runner.py를 찾는다.

실행:
python base_line/short_max/v9/frozen_reproduce_runner.py --data-dir "C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인\\Data\\time"
"""
from __future__ import annotations
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
V8_RUNNER = HERE.parent / "v8" / "frozen_reproduce_runner.py"
if not V8_RUNNER.exists():
    raise FileNotFoundError(f"required engine file not found: {V8_RUNNER}")

ns = runpy.run_path(str(V8_RUNNER), run_name="short_max_v9_engine")
CFG = ns["CFG"]
EXPECTED = ns["EXPECTED"]
main = ns["main"]

CFG.update(
    strategy="smv8_mix2_13_all_timereduce5",
    axis="short_max",
    short_dev=0.032,
    short_wick_mult=1.3,
    score_min_short=2.35,
    score_dev_weight=1.3,
    score_rsi_weight=0.8,
    score_wick_weight=0.7,
    atr_stop_mult=2.0,
    rr_mult=5.5,
    min_expected_tp=0.003,
    timeout_bars=200,
    time_reduce_bars=5,
    fail_fast_bars=10,
)

EXPECTED.clear()
EXPECTED.update(
    trades=63105,
    max_return_pct=2743.3304850694603,
    max_drawdown_pct=5.686879318598392,
    official_cd_value=2681.6337117546423,
    active_leftover=0,
    pending_leftover=0,
    load_errors=0,
)

# v8 runner 내부 출력명/metadata 일부는 v8 문자열을 유지할 수 있으나,
# gate와 전략 파라미터는 위 v9 공식값으로 고정된다.
if __name__ == "__main__":
    main()
