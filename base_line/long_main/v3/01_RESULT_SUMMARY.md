# long_main v3 결과 요약

## 1. 갱신 판정

long_main 기준선을 v2 `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`에서 v3 `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`로 갱신한다.

v3는 v6 손실 거래 진단과 v7 실제 백테스트 검증을 거친 기준선 기반 개선안이다.

---

## 2. 개발 결과 원천

- 결과 폴더: `local_results/long_main/LONG_MAIN_DEV_V7_20260510_221655`
- 개발 배치: `LONG_MAIN_DEV_V7_DIAG_BASED_STRUCTURAL_TEST`
- 후보명: `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- 후보 설명: v2에서 close_pos 0.77 추가 조건을 제거하고 ret20 <= -0.08을 추가한 공격/균형형 개선안
- 기준선 entry source: `raw_l01_cap_reclaim + double_flush_ok`

---

## 3. v2 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE |
| trades | 557 |
| wins | 333 |
| losses | 224 |
| win_rate_pct | 59.7845601436 |
| final_return_pct | 23.9514570645 |
| max_return_pct | 24.1477253403 |
| max_drawdown_pct | 1.3005547461 |
| official_cd_value | 122.3394005068 |
| profit_factor | 3.8956015265 |

---

## 4. v3 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08 |
| source_variant | LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08 |
| trades | 469 |
| trade_ratio_vs_ref | 0.8420107720 |
| wins | 303 |
| losses | 166 |
| win_rate_pct | 64.6055437100 |
| final_return_pct | 24.6575066055 |
| max_return_pct | 24.9228703822 |
| max_drawdown_pct | 1.0181358195 |
| official_cd_value | 123.3883238790 |
| profit_factor | 4.6238644584 |
| verdict | baseline_win |

---

## 5. v2 대비 변화

| 항목 | v2 | v3 | 변화 |
|---|---:|---:|---:|
| trades | 557 | 469 | -88 |
| wins | 333 | 303 | -30 |
| losses | 224 | 166 | -58 |
| win_rate_pct | 59.7846 | 64.6055 | +4.8210 |
| final_return_pct | 23.9515 | 24.6575 | +0.7060 |
| max_return_pct | 24.1477 | 24.9229 | +0.7751 |
| max_drawdown_pct | 1.3006 | 1.0181 | -0.2824 |
| official_cd_value | 122.3394 | 123.3883 | +1.0489 |
| profit_factor | 3.8956 | 4.6239 | +0.7283 |

---

## 6. 해석

v3는 거래 수를 557건에서 469건으로 줄였다. 그러나 줄어든 거래 중 손실 거래의 감소가 더 크다.

- wins 감소: -30
- losses 감소: -58

즉, v3의 `ret20 <= -0.08` 조건은 v6 진단에서 확인된 “덜 빠진 상태의 reclaim 손실 과대표현”을 실제 백테스트에서 효과적으로 제거했다.

v3는 다음 성격을 가진다.

- v2보다 더 선별적이다.
- 승률이 크게 상승했다.
- MDD가 1.0181까지 낮아졌다.
- 수익률과 max_return도 동시에 상승했다.
- 단순 방어형이 아니라 공격/균형형 기준선이다.

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

v3는 다음 이유로 long_main 공식 기준선으로 갱신한다.

1. 기존 `raw_l01_cap_reclaim + double_flush_ok` 구조를 보존했다.
2. v2에서 검증된 volume/body guard를 유지했다.
3. v6 진단에서 도출된 손실 과대표현 조건을 v7에서 공식 백테스트로 검증했다.
4. 수익률, max_return, MDD, 승률, cd_value가 모두 v2보다 개선되었다.
5. 거래 수는 감소했지만 손실 거래 감소폭이 더 크다.

따라서 앞으로 long_main 개발의 기준은 `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`다.
