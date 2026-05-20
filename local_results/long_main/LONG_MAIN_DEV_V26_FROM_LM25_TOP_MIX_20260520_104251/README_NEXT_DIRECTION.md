# LONG_MAIN_DEV_V26_FROM_LM25_TOP_MIX 결과

## 기준선 재현

- baseline_candidate: `LM26_000_LM25_S128_RR505_B320_H17_CD31_EXACT_FROZEN`
- pass_frozen_reproduction_gate: `False`
- expected cd: `572.4040640458543`
- actual cd: `572.4040640458543`
- errors: `0`

## 1위 요약

기준선 exact 재현 실패 또는 유효 후보 없음. 개선 후보 평가는 무효.

## 판정 규칙

`pass_frozen_reproduction_gate`가 false이면 summary의 개선 후보는 전부 무효다.

이번 v26은 V25 1위 LM25_S128_RR505_B320_H17_CD31을 기준선으로 두고 상위 후보의 장점만 섞는다.

- core: stop 1.26~1.30, rr 5.00~5.10, body_atr 0.30~0.38
- top1/top2 bridge: stop 1.265~1.295, rr 5.04~5.08, body_atr 0.32~0.35
- mdd repair: stop 1.25~1.27, rr 5.08~5.15, body_atr 0.28~0.34
- quality body: body_atr 0.36~0.45
- hold/cooldown: 상위 조건에 한해 hold 16/18, cooldown 29/30/32/33
- optional guards: close_pos_min, quiet_ratio_max, vol_ratio_min, lower_wick_body_ratio_min

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
