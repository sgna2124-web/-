# long_max v4 재현 및 다음 개발 규칙

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`

## 재현 기준값

| 항목 | 값 |
|---|---:|
| trades | 57065 |
| wins | 20612 |
| losses | 36453 |
| win_rate_pct | 36.1202137913 |
| final_return_pct | 267.6967217810 |
| max_return_pct | 268.4930973199 |
| max_drawdown_pct | 1.3412321126 |
| official_cd_value | 363.5507495661 |
| max_conc | 439 |
| errors | 0 |
| ruined | false |

## 재현 성공 조건

1. trades == 57065
2. wins == 20612
3. losses == 36453
4. errors == 0
5. ruined == false
6. official_cd_value가 363.5507495661 근처일 것
7. max_drawdown_pct가 1.3412321126 근처일 것
8. max_return_pct가 268.4930973199 근처일 것

trades, wins, losses가 다르면 재현 실패다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_max 기준은 MDD 제한 없이 official_cd_value 최대다.

## 다음 개발의 시작점

다음 long_max 개선은 반드시 v4에서 시작한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 atr_stop: `1.10`
- 기준 rr_target: `3.20`
- 기준 max_hold_bars: `21`
- 기준 cooldown_bars: `31`
- 기준 cd_value: `363.5507495661`

## 기준선 갱신 후보 판정 규칙

long_max 후보는 다음 조건을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. official_cd_value > 363.5507495661
4. 단독 재백테스트에서 결과 재현 가능

보조 선호 조건:

- max_conc < 439
- MDD가 과도하게 상승하지 않을 것
- 수수료 민감도 감소
- 거래 수 증가가 실제 성과 개선으로 이어질 것

## 허용되는 개선 방식

1. `candidate_entry = baseline_entry AND filter`
2. `candidate_entry = baseline_entry`
3. `candidate_entry = baseline_entry OR near_parent_entry`
4. 기준 entry 유지 + `atr_stop`, `rr_target`, `max_hold_bars`, `cooldown_bars` 조정
5. TP03 게이트 강화 또는 완화

## 금지 및 주의 사항

1. 이전 v3를 다음 개선 기준으로 삼지 않는다.
2. v4의 rr_target은 3.20이다. 2.90을 쓰면 v3 계열 재현이 된다.
3. V09, extreme, vol18 조건을 이름만 보고 새로 해석하지 않는다.
4. cd_value 계산 시 final_return_pct가 아니라 max_return_pct를 사용한다.
5. 기준선 재현 없이 개선 후보를 평가하지 않는다.

## 인수인계 문장

`long_max 현재 기준선은 v4 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320이다. MDD 제한 없이 cd_value 363.5507495661 초과를 목표로 개선한다. 기준선 entry_key는 child::orig_V09_extreme_vol18::tp03이며, 청산 파라미터는 atr_stop 1.10, rr_target 3.20, max_hold 21, cooldown 31이다.`
