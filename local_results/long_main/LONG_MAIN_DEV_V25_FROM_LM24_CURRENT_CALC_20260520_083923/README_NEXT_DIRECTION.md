# LONG_MAIN_DEV_V25_FROM_LM24_CURRENT_CALC 결과

## 기준선 재현

- baseline_candidate: `LM25_000_LM24_CURRENT_CALC_EXACT_FROZEN`
- pass_frozen_reproduction_gate: `True`
- expected cd: `548.1970984672943`
- actual cd: `548.1970984672943`
- errors: `0`

## 1위 요약

LONG_MAIN 1위: LM25_S128_RR505_B320_H17_CD31 | cd=572.4040640458543 | max_return=478.3711677059826 | mdd=1.0317083549990613 | trades=56171 | wins=22531 | losses=33640

## 판정 규칙

`pass_frozen_reproduction_gate`가 false이면 summary의 개선 후보는 전부 무효다.

이번 v24는 갱신된 기준선 v16/v11에서 다음 조합만 좁게 확인한다.

- stop: 1.21, 1.22, 1.23
- rr_target: 5.05, 5.10, 5.15, 5.20
- body_atr: 0.20, 0.22, 0.24, 0.26, 0.28
- hold: 17 고정

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
