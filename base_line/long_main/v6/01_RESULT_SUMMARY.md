# long_main v6 결과 요약

## 1. 갱신 판정

long_main 기준선을 v5 `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`에서 v6 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`으로 갱신한다.

갱신 이유는 단순하다. 새 전략은 long_main 선별 기준인 `MDD 5% 미만 전략 중 cd_value 최대` 조건을 충족하면서 v5 기준선을 압도적으로 초과한다.

중요한 운영 원칙:

- 이 전략은 기존 long_main v5의 직접 파생 전략은 아니다.
- 그러나 현재 운영 원칙은 “우월한 전략이 해당 축의 기준을 충족하면 기준선을 교체한다”이다.
- 따라서 long_main의 다음 개선은 v5가 아니라 v6 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`을 기준으로 진행한다.

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

## 3. long_main v5 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3 |
| trades | 447 |
| wins | 297 |
| losses | 150 |
| win_rate_pct | 66.4429530201 |
| final_return_pct | 24.8492730067 |
| max_return_pct | 25.0899569668 |
| max_drawdown_pct | 0.9930660871 |
| official_cd_value | 123.6093482796 |
| profit_factor | 4.9302639666 |

---

## 4. long_main v6 갱신 기준선 결과

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

## 5. v5 대비 변화

| 항목 | v5 | v6 | 변화 |
|---|---:|---:|---:|
| trades | 447 | 57243 | +56796 |
| wins | 297 | 20312 | +20015 |
| losses | 150 | 36931 | +36781 |
| win_rate_pct | 66.4429530201 | 35.4838146149 | -30.9591384052 |
| final_return_pct | 24.8492730067 | 214.7144460828 | +189.8651730761 |
| max_return_pct | 25.0899569668 | 215.2271020267 | +190.1371450599 |
| max_drawdown_pct | 0.9930660871 | 1.2219870757 | +0.2289209886 |
| official_cd_value | 123.6093482796 | 311.3750675807 | +187.7657193011 |

cd_value 개선율: 약 +151.90%

---

## 6. long_main 기준 충족 여부

long_main 기준은 `MDD 5% 미만 전략 중 cd_value 최대`다.

v6의 MDD는 `1.2219870757%`로 5% 미만 조건을 충족한다.
v6의 official_cd_value는 `311.3750675807`로 v5의 `123.6093482796`을 크게 초과한다.

따라서 v6는 long_main 기준선으로 갱신한다.

---

## 7. 전략 성격

v5는 고승률·저빈도·방어형 전략이었다.

v6는 저승률·초고빈도·낮은 MDD·높은 누적 수익형 전략이다.

따라서 앞으로 long_main 개선은 다음 방향으로 진행한다.

1. v6 진입 구조는 유지한다.
2. MDD 5% 미만 조건은 반드시 유지한다.
3. cd_value 상승을 최우선으로 본다.
4. 필요하면 승률 개선, max_conc 감소, 수수료 민감도 감소를 보조 목표로 둔다.

---

## 8. 다음 개선 기준

다음 long_main 개선은 반드시 이 폴더의 다음 파일을 기준으로 한다.

- `02_ENTRY_EXIT_CONDITIONS.md`
- `03_STRATEGY_CODE_REFERENCE.py`
- `04_STRENGTHS_WEAKNESSES.md`
- `05_REPRODUCTION_AND_NEXT_DEV_RULES.md`

이전 long_main v5 조건을 기준으로 새 개선을 시작하지 않는다. v5는 히스토리로 보존하고, v6가 공식 기준선이다.
