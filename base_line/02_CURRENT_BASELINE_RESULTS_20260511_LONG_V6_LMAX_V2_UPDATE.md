# 현재 롱 기준선 갱신 기록

## 1. 갱신 요약

동일 전략 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`을 long_main v6와 long_max v2 기준선으로 동시에 등록한다.

갱신 이유:

1. V11에서 전체 후보 중 1위로 발견되었다.
2. V12 단독 재백테스트에서 동일 결과가 재현되었다.
3. long_main 기준인 MDD 5% 미만을 충족한다.
4. long_max 기준인 cd_value 최대 조건을 충족한다.
5. 기존 long_main v5와 long_max v1을 모두 압도한다.

---

## 2. 새 기준선 공통 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
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
| errors | 0 |
| ruined | false |

---

## 3. 저장 위치

long_main:

`base_line/long_main/v6/`

long_max:

`base_line/long_max/v2/`

각 폴더에는 다음 파일을 둔다.

1. `01_RESULT_SUMMARY.md`
2. `02_ENTRY_EXIT_CONDITIONS.md`
3. `03_STRATEGY_CODE_REFERENCE.py`
4. `04_STRENGTHS_WEAKNESSES.md`
5. `05_REPRODUCTION_AND_NEXT_DEV_RULES.md`

---

## 4. 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

---

## 5. 축별 기준

long_main:

- MDD 5% 미만 전략 중 official_cd_value 최대
- 현재 기준선: long_main v6
- 목표: MDD 5% 미만 유지 + cd_value 311.3750675807 초과

long_max:

- MDD 제한 없이 official_cd_value 최대
- 현재 기준선: long_max v2
- 목표: cd_value 311.3750675807 초과

---

## 6. 다음 개발 기준 문장

long_main:

`long_main 현재 기준선은 v6 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20이다. MDD 5% 미만 조건을 유지하면서 cd_value 311.3750675807 초과를 목표로 개선한다.`

long_max:

`long_max 현재 기준선은 v2 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20이다. MDD 제한 없이 cd_value 311.3750675807 초과를 목표로 개선한다.`
