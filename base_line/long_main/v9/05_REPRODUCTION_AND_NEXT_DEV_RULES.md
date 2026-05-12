# long_main v9 재현 및 다음 개발 규칙

## 재현 기준값

- trades: 57035
- wins: 20451
- losses: 36584
- win_rate_pct: 35.8569299553
- final_return_pct: 305.0347181084
- max_return_pct: 305.8775211164
- max_drawdown_pct: 1.2432451599
- official_cd_value: 400.8314684802
- max_conc: 441
- errors: 0
- ruined: false

## 재현 성공 조건

trades, wins, losses가 모두 일치해야 한다. errors는 0이어야 하고 ruined는 false여야 한다. official_cd_value, max_drawdown_pct, max_return_pct는 위 기준값과 근접해야 한다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_main 기준은 `max_drawdown_pct < 5` 조건을 만족하는 전략 중 official_cd_value 최대다.

## 다음 개발의 시작점

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 atr_stop: `1.10`
- 기준 rr_target: `3.50`
- 기준 max_hold_bars: `21`
- 기준 cooldown_bars: `31`
- 기준 cd_value: `400.8314684802`
- 기준 MDD: `1.2432451599`

## 기준선 갱신 후보 판정 규칙

1. errors == 0
2. ruined == false
3. max_drawdown_pct < 5
4. official_cd_value > 400.8314684802
5. 단독 재백테스트에서 결과 재현 가능

## 허용되는 개선 방식

- 기준 entry에 방어 필터 추가
- 기준 entry에 과열 회피 필터 추가
- 기준 entry에 max_conc 감소 필터 추가
- 기준 entry 유지 후 atr_stop, rr_target, max_hold_bars, cooldown_bars 조정
- TP03 게이트 강화 또는 완화

## 금지 및 주의 사항

1. 이전 v8을 다음 개선 기준으로 삼지 않는다.
2. v9의 rr_target은 3.50이다. 3.20을 쓰면 v8 계열 재현이 된다.
3. V09, extreme, vol18 조건을 이름만 보고 새로 해석하지 않는다.
4. cd_value 계산 시 final_return_pct가 아니라 max_return_pct를 사용한다.
5. 기준선 재현 없이 개선 후보를 평가하지 않는다.
