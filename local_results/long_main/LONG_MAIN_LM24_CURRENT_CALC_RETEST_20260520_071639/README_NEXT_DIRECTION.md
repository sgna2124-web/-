# LONG_MAIN_LM24_CURRENT_CALC_RETEST 결과

## 기준선 재현

- baseline_candidate: `LM24R_001_RETEST_CURRENT_CALC_S121_RR505_B022_H17`
- pass_frozen_reproduction_gate: `True`
- expected cd: `548.1970984672943`
- actual cd: `548.1970984672943`
- errors: `0`

## 1위 요약

LONG_MAIN 1위: LM24R_001_RETEST_CURRENT_CALC_S121_RR505_B022_H17 | cd=548.1970984672943 | max_return=455.0171719748191 | mdd=1.2288040536220124 | trades=56551 | wins=21969 | losses=34582

## 판정 규칙

`pass_frozen_reproduction_gate`가 false이면 summary의 개선 후보는 전부 무효다.

이번 파일은 개선 후보 없이 v24 current-calc 방식의 단독 재현만 확인한다.

- stop: 1.21
- rr_target: 5.05
- body_atr: 0.22
- hold: 17
- cooldown: 31

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
이 파일에서 pass_frozen_reproduction_gate가 true이면 현재 v24 방식은 새 기준선 expected로 고정할 수 있다.
