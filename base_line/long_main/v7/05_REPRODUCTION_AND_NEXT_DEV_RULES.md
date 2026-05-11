# long_main v7 재현 및 다음 개발 규칙

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`

## 재현 기준값

| 항목 | 값 |
|---|---:|
| trades | 57114 |
| wins | 20911 |
| losses | 36203 |
| win_rate_pct | 36.6127394334 |
| final_return_pct | 240.7307747654 |
| max_return_pct | 241.3427142366 |
| max_drawdown_pct | 1.3408670828 |
| official_cd_value | 336.7657621418 |
| max_conc | 435 |
| errors | 0 |
| ruined | false |

## 재현 성공 조건

1. trades == 57114
2. wins == 20911
3. losses == 36203
4. errors == 0
5. ruined == false
6. official_cd_value가 336.7657621418 근처일 것
7. max_drawdown_pct가 1.3408670828 근처일 것
8. max_return_pct가 241.3427142366 근처일 것

trades, wins, losses가 다르면 재현 실패다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_main 기준은 `max_drawdown_pct < 5` 조건을 만족하는 전략 중 official_cd_value 최대다.

## 다음 개발의 시작점

다음 long_main 개선은 반드시 v7에서 시작한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 atr_stop: `1.10`
- 기준 rr_target: `2.90`
- 기준 max_hold_bars: `21`
- 기준 cooldown_bars: `31`
- 기준 cd_value: `336.7657621418`

## 기준선 갱신 후보 판정 규칙

long_main 후보는 다음 조건을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. max_drawdown_pct < 5
4. official_cd_value > 336.7657621418
5. 단독 재백테스트에서 결과 재현 가능

보조 선호 조건:

- max_conc < 435
- win_rate_pct > 36.6127394334
- 수수료 민감도 감소
- 거래 수가 지나치게 증가하지 않을 것

## 허용되는 개선 방식

1. `candidate_entry = baseline_entry AND filter`
2. `candidate_entry = baseline_entry`
3. `candidate_entry = baseline_entry OR near_parent_entry`, 단 MDD 5% 미만 유지 필수
4. 기준 entry 유지 + `atr_stop`, `rr_target`, `max_hold_bars`, `cooldown_bars` 조정
5. TP03 기준 강화, 단 기준선과의 차이를 명확히 기록

## 금지 및 주의 사항

1. 이전 v6를 다음 개선 기준으로 삼지 않는다.
2. v7의 atr_stop은 1.10이다. 1.01을 쓰면 v6 재현이 된다.
3. V09, extreme, vol18 조건을 이름만 보고 새로 해석하지 않는다.
4. cd_value 계산 시 final_return_pct가 아니라 max_return_pct를 사용한다.
5. 기준선 재현 없이 개선 후보를 평가하지 않는다.

## 인수인계 문장

`long_main 현재 기준선은 v7 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110이다. MDD 5% 미만 조건을 유지하면서 cd_value 336.7657621418 초과를 목표로 개선한다. 기준선 entry_key는 child::orig_V09_extreme_vol18::tp03이며, 청산 파라미터는 atr_stop 1.10, rr_target 2.90, max_hold 21, cooldown 31이다.`
