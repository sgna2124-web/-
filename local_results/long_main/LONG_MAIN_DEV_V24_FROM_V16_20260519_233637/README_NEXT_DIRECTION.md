# LONG_MAIN_DEV_V24_FROM_V16 결과

## 기준선 재현

- baseline_candidate: `LM24_000_LONG_MAIN_V16_EXACT_FROZEN`
- pass_frozen_reproduction_gate: `False`
- expected cd: `547.2610302171641`
- actual cd: `548.1970984672943`
- errors: `0`

## 1위 요약

기준선 exact 재현 실패 또는 유효 후보 없음. 개선 후보 평가는 무효.

## 판정 규칙

`pass_frozen_reproduction_gate`가 false이면 summary의 개선 후보는 전부 무효다.

이번 v24는 갱신된 기준선 v16/v11에서 다음 조합만 좁게 확인한다.

- stop: 1.21, 1.22, 1.23
- rr_target: 5.05, 5.10, 5.15, 5.20
- body_atr: 0.20, 0.22, 0.24, 0.26, 0.28
- hold: 17 고정

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
