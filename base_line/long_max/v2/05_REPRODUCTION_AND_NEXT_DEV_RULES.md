# long_max v2 재현 및 다음 개발 규칙

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`

---

## 1. 재현 기준

v2 기준선은 V12 단독 재백테스트 결과를 기준으로 한다.

기준값:

| 항목 | 값 |
|---|---:|
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

재현 성공 최소 조건:

1. trades, wins, losses가 일치할 것
2. final_return_pct, max_return_pct, MDD, cd_value가 허용 오차 안에 있을 것
3. errors == 0
4. ruined == false

---

## 2. 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_max 기준:

`MDD 제한 없이 전체 전략 중 official_cd_value 최대`

---

## 3. 다음 개발의 시작점

다음 long_max 개선은 반드시 v2 기준선에서 시작한다.

기준선 entry:

`child::orig_V09_extreme_vol18::tp03`

기준선 청산:

- atr_stop = 1.01
- rr_target = 2.90
- max_hold_bars = 21
- cooldown_bars = 31
- use_tp03_gate = true

---

## 4. 개선 후보 판정 규칙

long_max 후보는 다음 조건을 모두 만족해야 기준선 갱신 후보가 된다.

1. errors == 0
2. ruined == false
3. official_cd_value > 311.3750675807
4. 단독 재백테스트에서 결과 재현 가능

보조 선호 조건:

- max_conc < 429
- MDD가 과도하게 상승하지 않을 것
- 수수료 민감도가 낮아질 것
- 거래 수 증가가 성과 개선으로 이어질 것

---

## 5. 허용되는 개선 방식

1. 기준선 entry에 추가 필터를 붙이는 방식

`candidate_entry = baseline_entry AND filter`

2. 기준선 entry는 유지하고 청산만 바꾸는 방식

`candidate_entry = baseline_entry`

3. 기준선 주변 신호를 일부 추가하는 방식

`candidate_entry = baseline_entry OR near_parent_entry`

4. TP03 조건을 강화/완화하는 방식

단, TP03을 제거하거나 완화한 경우에는 기준선과의 차이를 반드시 기록한다.

---

## 6. 금지/주의 사항

1. 이전 long_max v1 V51 기준선을 다음 개선 기준으로 삼지 않는다.
2. V09/extreme/vol18 구조를 임의로 해석해 새로 만들지 않는다.
3. cd_value 계산 시 final_return_pct가 아니라 max_return_pct를 사용한다.
4. 기준선 갱신은 단독 재현 성공 후에만 한다.
5. V11/V12에서 나온 숫자와 다르면 원인 확인 전 기준선 갱신 금지.

---

## 7. 인수인계 문장

다음 대화창에서 long_max 개선을 시작할 때는 다음 문장을 기준으로 한다.

`long_max 현재 기준선은 v2 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20이다. MDD 제한 없이 cd_value 311.3750675807 초과를 목표로 개선한다. 기준선 entry_key는 child::orig_V09_extreme_vol18::tp03이며, 청산 파라미터는 atr_stop 1.01, rr_target 2.90, max_hold 21, cooldown 31이다.`
