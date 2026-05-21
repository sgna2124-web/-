# LONG_MAIN_DEV_V27_FROM_V17_LM26_BASELINE 결과

## 기준선 재현

- baseline_candidate: `LM27_000_LONG_MAIN_V17_LM26_S128_RR505_B360_H17_CD32_EXACT_FROZEN`
- pass_frozen_reproduction_gate: `True`
- expected cd: `603.3485179858741`
- actual cd: `603.3485179858741`
- errors: `0`
- max_conc: diagnostic only, hard gate excluded

## 1위 요약

LONG_MAIN 1위: LM27_S1290_RR5150_B0460_H17_CD32 | cd=614.089471282701 | max_return=520.5122954395083 | mdd=1.0350841077626183 | trades=55247 | wins=22313 | losses=32934

## 판정 규칙

`pass_frozen_reproduction_gate`가 false이면 summary의 개선 후보는 전부 무효다.
단, max_conc는 하드 게이트가 아니다. max_conc 차이만으로 기준선 재현 실패 처리하지 않는다.

이번 v27은 long_main v17 / long_max v12 기준선인 LM26_S1280_RR5050_B0360_H17_CD32를 기준으로 둔다.

- baseline: stop 1.28, rr 5.05, body_atr 0.36, hold 17, cooldown 32
- core: stop 1.26~1.32, rr 5.00~5.20, body_atr 0.34~0.46, cooldown 32
- cooldown extension: cooldown 33~34
- hold repair: hold 16/18
- mdd guard: stop 1.24~1.27, rr 5.08~5.15, body_atr 0.36~0.42
- return extension: stop 1.29/1.31/1.34, rr 5.15/5.25/5.30
- optional guards: close_pos_min, quiet_ratio_max, vol_ratio_min, lower_wick_body_ratio_min

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
