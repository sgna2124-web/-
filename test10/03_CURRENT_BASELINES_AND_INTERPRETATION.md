# 현재 공식 기준선 / 보조 기준선 / 대체 후보

## 1. 공식 기준선

현재 공식 비교 기준선은 `official_top200_reference`다.

최근 기준 수치:
- final_return_pct 1120.69995
- pf 1.2199649
- mdd_pct -36.03441
- max_conc 271

이 기준선을 유지하는 이유:
- v23 baseline_top200 이후, v26/v27 기준으로도 여전히 가장 종합 성과가 좋음
- 수익, MDD, max_conc를 모두 같이 봤을 때 아직까지 가장 강한 기준선

단, 주의:
- 이 규칙은 “현재 최고 성과의 기준선”이지 “이론적으로 확정된 최종 규칙”이 아님
- top200 자체에 대한 구조적 의심은 여전히 남아 있음

## 2. 방어형 / 균형형 참고 기준선

### asym_guard_top200
의미:
- 공식 기준선보다 수익은 낮지만, PF와 MDD 균형이 좋았던 대표적 방어형 후보

주요 수치(v23 기준):
- final_return_pct 1030.7929
- pf 1.2327923
- mdd_pct -35.22274
- max_conc 269

해석:
- 수익 일부를 포기하고 효율/안정성 균형을 노릴 때 참고할 만한 기준선

### asym_guard_top150
의미:
- v24-3 MDD 방어 레인에서 practical defense 후보로 가장 의미 있었음

주요 수치(v24-3 기준):
- final_return_pct 898.76
- pf 1.21856
- mdd_pct -32.53
- max_conc 269

해석:
- 수익을 완전히 무너뜨리지 않으면서 drawdown을 줄이는 방어형 기준선으로 유용

## 3. top200 없는 최선 후보

현재 top200 제거 상태에서 가장 근접한 후보는 `score_l16_s20_shortheavy`다.

최근 수치(v27 기준):
- final_return_pct 1089.0657
- pf 1.2242424
- mdd_pct -41.06885
- max_conc 386

왜 주목하는가:
- 수익 보존율이 가장 높음(공식 기준선 대비 약 97.18%)
- 숏 쪽 threshold를 더 엄격하게 둘 때 top200 대체 가능성이 가장 높게 나옴

왜 아직 채택 못하는가:
- MDD가 공식 기준선보다 약 5%p 이상 나쁨
- max_conc도 공식 기준선보다 훨씬 큼
- 즉 아직 “대체 성공”이라고 부를 수 없음

## 4. top200 없는 보조 후보

### score_l16_s18
- final_return_pct 1088.0037
- pf 1.2195171
- mdd_pct -40.79565
- max_conc 386

해석:
- 절대 score 컷 중에서는 무난하게 근접
- 하지만 short-heavy보다 특별히 낫다고 보기 어려움

### asym_guard_score_l16_s20_shortheavy
- final_return_pct 1027.1190
- pf 1.2416775
- mdd_pct -39.53297
- max_conc 379

해석:
- PF는 가장 좋음
- 그러나 수익이 공식 기준선보다 더 많이 낮음
- 방어형/대체형 후보로 보조 참고 가능

## 5. 무엇을 공식으로 믿고 무엇을 보류해야 하는가

지금 공식적으로 믿는 것:
- same-bar 수정 이후 엔진 결과
- official_top200_reference의 현재 우위
- short-heavy 절대 score 컷이 top200 대체 탐색에서 가장 유망하다는 점

지금 보류해야 하는 것:
- top200이 최종 원리라는 결론
- 절대 score 컷만으로 이미 대체 가능하다는 결론
- fail-fast가 대체 구조로 유의미하다는 결론

## 6. 다음 실험 출발점

공식 비교 기준선:
- official_top200_reference

대체 후보 주축:
- score_l16_s20_shortheavy
- score_l16_s18
- asym_guard_score_l16_s20_shortheavy

실질적 다음 질문:
- short-heavy 축을 더 다듬으면 top200을 진짜 대체할 수 있는가?
- long/short quality guard와 hardened score 정규화를 같이 조정하면 MDD와 max_conc를 다시 낮출 수 있는가?
