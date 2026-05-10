# long_main v2 결과 요약

## 1. 갱신 판정

long_main 기준선을 v1 `6V2_L01_doubleflush_core`에서 v2 `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`로 갱신한다.

v2는 v1 기준선 진입 조건을 기본으로 두고, v4 개발 결과에서 확인된 유효한 추가 조건을 붙인 기준선 기반 개선안이다.

---

## 2. 개발 결과 원천

- 결과 폴더: `local_results/long_main/LONG_MAIN_DEV_V4_20260509_235230`
- 개발 배치: `LONG_MAIN_DEV_V4_BASELINE_BASED_CONDITION_DEV`
- 후보명: `LM4_014_ATTACK_BODY_NOT_HUGE`
- 후보 설명: v3 attack anchor + body_atr <= 1.60; loose chase guard
- 기준선 entry source: `base_line/6V2_long10_reviewed.py`의 `raw_l01_cap_reclaim + double_flush_ok`

---

## 3. v1 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 6V2_L01_doubleflush_core |
| trades | 592 |
| wins | 346 |
| losses | 246 |
| win_rate_pct | 58.4459459459 |
| final_return_pct | 23.8426079030 |
| max_return_pct | 24.0623399724 |
| max_drawdown_pct | 1.7279904306 |
| official_cd_value | 121.7026194894 |

---

## 4. v2 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE |
| source_variant | LM4_014_ATTACK_BODY_NOT_HUGE |
| trades | 557 |
| trade_ratio_vs_ref | 0.9408783784 |
| wins | 333 |
| losses | 224 |
| win_rate_pct | 59.7845601436 |
| final_return_pct | 23.9514570645 |
| max_return_pct | 24.1477253403 |
| max_drawdown_pct | 1.3005547461 |
| official_cd_value | 122.3394005068 |
| profit_factor | 3.8956015265 |
| verdict | baseline_win |

---

## 5. v1 대비 변화

| 항목 | v1 | v2 | 변화 |
|---|---:|---:|---:|
| trades | 592 | 557 | -35 |
| wins | 346 | 333 | -13 |
| losses | 246 | 224 | -22 |
| win_rate_pct | 58.4459 | 59.7846 | +1.3386 |
| final_return_pct | 23.8426 | 23.9515 | +0.1088 |
| max_return_pct | 24.0623 | 24.1477 | +0.0854 |
| max_drawdown_pct | 1.7280 | 1.3006 | -0.4274 |
| official_cd_value | 121.7026 | 122.3394 | +0.6368 |

---

## 6. 해석

v2는 거래 수를 592건에서 557건으로 줄였지만, 제거된 거래가 손실 또는 품질 낮은 진입 쪽에 더 가까웠다.

핵심 개선은 MDD 감소다. max_drawdown_pct가 1.7280에서 1.3006으로 줄었다. 동시에 final_return_pct와 max_return_pct도 소폭 상승했기 때문에 단순 방어형이 아니라 균형형 기준선 개선으로 본다.

v2의 성격은 다음과 같다.

- 공격성은 v3 attack anchor보다 약간 낮다.
- 안정성은 v3 attack anchor보다 좋다.
- 기준선 v1 대비 수익, 최대수익, MDD, cd_value가 모두 개선되었다.

---

## 7. 실행 조건

- csv_files: 597
- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- TP03: 개선안 규칙에 따라 적용

---

## 8. 기준선 갱신 결론

v2는 다음 이유로 long_main 공식 기준선으로 갱신한다.

1. v1 기준선 진입 조건을 그대로 기본값으로 유지했다.
2. 완전히 새로운 전략이 아니라 기준선 기반 개선안이다.
3. 거래 수가 과도하게 줄지 않았다.
4. 수익률과 MDD가 동시에 개선되었다.
5. official_cd_value가 121.7026에서 122.3394로 개선되었다.

따라서 앞으로 long_main 개발의 기준은 `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`다.
