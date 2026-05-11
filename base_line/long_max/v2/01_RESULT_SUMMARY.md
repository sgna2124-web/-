# long_max v2 결과 요약

## 1. 갱신 판정

long_max 기준선을 v1 `8V4_V51_V002_core_rare22_c1`에서 v2 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`으로 갱신한다.

long_max의 공식 선별 기준은 `MDD 제한 없이 cd_value 최대`다. 새 전략은 V11에서 1위로 발견된 뒤, V12 단독 재백테스트에서도 같은 결과가 재현되었다.

따라서 이 전략은 long_max 새 공식 기준선이다.

---

## 2. 개발 및 검증 원천

- 발견 배치: `LONG_MAX_PARENT_SIGNAL_DEV_V11`
- 단독 재검증 배치: `LONG_MAX_SINGLE_TOP_RETEST_DEV_V12`
- 결과 위치: `local_results/long_max/LONG_MAX_SINGLE_TOP_RETEST_DEV_V12/`
- 단독 재현 대상: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`
- 재현 판정: `pass_basic_reproduction_gate = true`
- 데이터 수: 597 CSV
- 포지션 비중: `position_fraction = 0.01`
- 수수료: `round_trip_cost_bps = 8.0`
- max_bars: 0, 전체 캔들 사용

---

## 3. long_max v1 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V51_V002_core_rare22_c1 |
| trades | 2276 |
| wins | 1032 |
| losses | 1244 |
| win_rate_pct | 45.3427 |
| final_return_pct | 44.3226 |
| max_return_pct | 44.9123 |
| max_drawdown_pct | 6.8270 |
| official_cd_value | 134.4697 |

---

## 4. long_max v2 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
| side | long |
| entry_key | child::orig_V09_extreme_vol18::tp03 |
| atr_stop | 1.01 |
| rr_target | 2.90 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |
| trades | 57243 |
| wins | 20312 |
| losses | 36931 |
| win_rate_pct | 35.4838146149 |
| final_return_pct | 214.7144460828 |
| max_return_pct | 215.2271020267 |
| max_drawdown_pct | 1.2219870757 |
| official_cd_value | 311.3750675807 |
| max_conc | 429 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

---

## 5. v1 대비 변화

| 항목 | v1 | v2 | 변화 |
|---|---:|---:|---:|
| trades | 2276 | 57243 | +54967 |
| wins | 1032 | 20312 | +19280 |
| losses | 1244 | 36931 | +35687 |
| win_rate_pct | 45.3427 | 35.4838146149 | -9.8588853851 |
| final_return_pct | 44.3226 | 214.7144460828 | +170.3918460828 |
| max_return_pct | 44.9123 | 215.2271020267 | +170.3148020267 |
| max_drawdown_pct | 6.8270 | 1.2219870757 | -5.6050129243 |
| official_cd_value | 134.4697 | 311.3750675807 | +176.9053675807 |

cd_value 개선율: 약 +131.56%

---

## 6. long_max 기준 충족 여부

long_max 기준은 `전체 전략 중 cd_value 최대`다.

v2는 V11 combined 결과에서 1위였고, V12 단독 재백테스트에서도 동일하게 재현되었다.

단독 재현 차이:

- trades delta: 0
- wins delta: 0
- losses delta: 0
- final_return_pct delta: 약 +0.000046
- max_return_pct delta: 약 +0.000002
- max_drawdown_pct delta: 약 -0.0000129
- cd_value delta: 약 -0.000032

따라서 V11 결과가 우연이 아니라 단독 재현 가능한 전략임을 확인했다.

---

## 7. 전략 성격

v1은 희소 진입형 V51 기준선이었다.

v2는 V09 extreme_vol18 부모 신호에 TP03 기대값 게이트와 risk_rr_plus20 청산 프로파일을 결합한 초고빈도 누적수익형 전략이다.

v2는 승률은 낮지만, 다음 특성이 매우 강하다.

1. 거래 수가 매우 많다.
2. MDD가 낮다.
3. max_return과 final_return이 높다.
4. cd_value가 기존 v1을 크게 초과한다.
5. 단독 재현이 성공했다.

---

## 8. 다음 개선 기준

다음 long_max 개선은 반드시 이 폴더의 다음 파일을 기준으로 한다.

- `02_ENTRY_EXIT_CONDITIONS.md`
- `03_STRATEGY_CODE_REFERENCE.py`
- `04_STRENGTHS_WEAKNESSES.md`
- `05_REPRODUCTION_AND_NEXT_DEV_RULES.md`

이전 v1 `8V4_V51_V002_core_rare22_c1`은 히스토리로 보존한다. 앞으로 long_max 개발의 기준은 v2다.
