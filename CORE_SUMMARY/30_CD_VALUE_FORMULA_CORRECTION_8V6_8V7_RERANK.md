# 30_CD_VALUE_FORMULA_CORRECTION_8V6_8V7_RERANK

## 핵심 정정

기존 문서 일부에는 cd_value를 `max_return_pct / max_drawdown_pct` 방식의 ratio로 해석한 기록이 남아 있다.
이제부터 공식 cd_value는 사용자 정의 방식으로 계산한다.

```text
cd_value = 기존자산 × (1 - (abs(max_drawdown_pct) / 100)) × (1 + (max_return_pct / 100))
```

기존자산을 100으로 두면 다음과 같다.

```text
cd_value_100 = 100 × (1 - abs(MDD)/100) × (1 + max_return_pct/100)
```

예시:
- 기존자산 100
- MDD 10% 적용 후 90
- max_return_pct 10% 적용 후 99
- cd_value = 99

따라서 `max_return_pct / max_drawdown_pct`는 더 이상 cd_value가 아니다. 필요하면 참고용 `return_drawdown_ratio` 또는 `ratio`로만 표기한다.

## 공식 승격 기준

공식 승격 기준은 그대로 유지한다.

```text
official promotion = max_drawdown_pct < 5.0
```

다만 후보는 항상 두 축으로 본다.

1. 후보 A: MDD 5% 미만 중 corrected cd_value 1위
2. 후보 B: MDD와 관계없이 전체 corrected cd_value 1위
3. A와 B가 같으면 동일 전략 1개를 우선 심화한다.
4. MDD가 5%를 넘더라도 corrected cd_value가 높으면 개선 후보로 기록한다. 단, 공식 승격은 아니다.

## 8V6~8V7 corrected cd_value 재계산 순위

기초자산은 100으로 계산했다.

| rank | batch | strategy | max_return_pct | max_drawdown_pct | corrected_cd_value_100 | official_mdd_lt_5 |
|---:|---|---|---:|---:|---:|---|
| 1 | 8V7 | 8V7_AB_BEST_I065_post_loss_brake_plb15 | 7.996104 | 4.033795 | 103.638721 | yes |
| 2 | 8V7 | 8V7_AB_BEST_I055_post_loss_brake_plb05 | 8.995962 | 4.994738 | 103.551899 | yes |
| 3 | 8V6 | 8V6_P1_CORE_RARE22_C1_I083_hybrid_cover_hyb13 | 8.227282 | 4.442034 | 103.419789 | yes |
| 4 | 8V6 | 8V6_P3_SHOCKLOW_RARE22_C1_I083_hybrid_cover_hyb13 | 8.046307 | 4.334413 | 103.363134 | yes |
| 5 | 8V6 | 8V6_P2_CORE_BASE_I083_hybrid_cover_hyb13 | 8.060175 | 4.369205 | 103.338804 | yes |
| 6 | 8V6 | 8V6_P1_CORE_RARE22_C1_I011_edge_preserve_edge11 | 9.636343 | 5.744029 | 103.338800 | no |
| 7 | 8V6 | 8V6_P3_SHOCKLOW_RARE22_C1_I011_edge_preserve_edge11 | 9.349358 | 5.544783 | 103.286173 | no |
| 8 | 8V7 | 8V7_AB_BEST_I090_post_loss_brake_plb40 | 6.867317 | 3.594439 | 103.025878 | yes |
| 9 | 8V7 | 8V7_AB_BEST_I005_edge_restore_er05 | 7.878080 | 4.508571 | 103.013850 | yes |
| 10 | 8V6 | 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | 5.251008 | 2.131159 | 103.007864 | yes |
| 11 | 8V7 | 8V7_AB_BEST_I063_post_loss_brake_plb13 | 7.442342 | 4.134624 | 103.000009 | yes |

## 현재 결론

8V6부터 8V7까지 corrected cd_value 기준 전체 1위와 MDD 5% 미만 1위가 모두 동일하다.

```text
현재 후보 A = 8V7_AB_BEST_I065_post_loss_brake_plb15
현재 후보 B = 8V7_AB_BEST_I065_post_loss_brake_plb15
```

따라서 다음 개선은 I065 post_loss_brake_plb15를 중심으로 한다.
이전 ratio 기준으로 8V7 I070이 상위였던 해석은 폐기한다. I070은 낮은 MDD와 낮은 수익률 조합이라 ratio는 높지만, corrected cd_value 방식에서는 핵심 기준선이 아니다.

## 다음 작업 지시

1. 단순 파라미터 조정 금지.
2. I065의 장점인 `post_loss_brake` 계열의 손실 후 과매매 억제, 안정화 효과를 유지한다.
3. 단점인 수익 확장 한계와 진입 수 감소 위험을 보완한다.
4. V51 core_base/core_rare22_c1의 edge를 보강하되 MDD 5% 미만을 유지한다.
5. strict/lowanchor safe branch는 보조 안전축으로 혼합 가능하다.
6. 다음 배치는 I065 중심 200개 이상 개선안으로 진행한다.
7. 결과 평가 시 corrected cd_value_100, max_return_pct, max_drawdown_pct, trades, official_mdd_lt_5를 함께 기록한다.
