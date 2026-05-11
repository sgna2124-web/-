# long_main v5 결과 요약

## 1. 갱신 판정

long_main 기준선을 v4 `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`에서 v5 `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`으로 갱신한다.

v5는 v4 기준선의 진입 조건을 바탕으로 `shock_recency <= 3` 조건을 추가한 기준선 기반 방어형 개선안이다.

---

## 2. 개발 결과 원천

- 결과 폴더: `local_results/long_main/LONG_MAIN_DEV_V9_20260511_132134`
- 개발 배치: `LONG_MAIN_DEV_V9_RESOURCE_AWARE_V4_STRUCTURAL_TEST`
- 후보명: `LM9_012_V4_SHOCK_RECENCY_3`
- 후보 설명: v4 기준선에 shock_recency <= 3 추가
- 기준선 entry source: `raw_l01_cap_reclaim + double_flush_ok`
- 리소스 프로필: workers=1, variants=14

---

## 3. v4 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220 |
| trades | 479 |
| wins | 310 |
| losses | 169 |
| win_rate_pct | 64.7181628392 |
| final_return_pct | 24.9404780954 |
| max_return_pct | 25.2063735035 |
| max_drawdown_pct | 1.0904624350 |
| official_cd_value | 123.5780610685 |
| profit_factor | 4.5655373148 |

---

## 4. v5 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3 |
| source_variant | LM9_012_V4_SHOCK_RECENCY_3 |
| trades | 447 |
| wins | 297 |
| losses | 150 |
| win_rate_pct | 66.4429530201 |
| final_return_pct | 24.8492730067 |
| max_return_pct | 25.0899569668 |
| max_drawdown_pct | 0.9930660871 |
| official_cd_value | 123.6093482796 |
| profit_factor | 4.9302639666 |
| verdict | baseline_win |

---

## 5. v4 대비 변화

| 항목 | v4 | v5 | 변화 |
|---|---:|---:|---:|
| trades | 479 | 447 | -32 |
| wins | 310 | 297 | -13 |
| losses | 169 | 150 | -19 |
| win_rate_pct | 64.7182 | 66.4430 | +1.7248 |
| final_return_pct | 24.9405 | 24.8493 | -0.0912 |
| max_return_pct | 25.2064 | 25.0900 | -0.1164 |
| max_drawdown_pct | 1.0905 | 0.9931 | -0.0974 |
| official_cd_value | 123.5781 | 123.6093 | +0.0313 |
| profit_factor | 4.5655 | 4.9303 | +0.3647 |

---

## 6. 해석

v5는 v4보다 거래를 32건 적게 허용했다.

감소한 거래의 구성은 다음과 같다.

- wins: -13
- losses: -19

즉, `shock_recency <= 3` 조건은 손실 거래를 더 많이 제거했다.

v5는 수익률과 max_return이 아주 소폭 낮아졌지만, 다음 항목이 개선되었다.

- 승률 상승
- MDD 감소
- profit_factor 상승
- official_cd_value 상승

따라서 v5는 v4보다 더 방어적인 long_main 기준선이다.

---

## 7. 실행 조건

- csv_files: 597
- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- TP03: 개선안 규칙에 따라 적용
- workers: 1
- variants: 14

---

## 8. 기준선 갱신 결론

v5는 다음 이유로 long_main 공식 기준선으로 갱신한다.

1. v4의 핵심 진입 구조를 유지했다.
2. 변경점이 `shock_recency <= 3` 추가로 명확하다.
3. v4 대비 official_cd_value가 상승했다.
4. MDD, 승률, profit_factor가 개선되었다.
5. 리소스 절약형 개발 조건에서도 기준선 exact 재현과 개선안 검증이 정상적으로 완료되었다.

따라서 앞으로 long_main 개발의 기준은 `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`다.
