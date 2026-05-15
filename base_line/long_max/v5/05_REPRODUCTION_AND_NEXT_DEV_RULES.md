# long_max v5 재현 및 다음 개발 규칙

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 재현 기준값: 2025년까지의 기록

- trades: 56704
- wins: 20348
- losses: 36356
- win_rate_pct: 35.884593679458234
- final_return_pct: 305.5299492881062
- max_return_pct: 305.8271270102085
- max_drawdown_pct: 1.24324515986044
- official_cd_value: 400.7817008962534
- max_conc: 441
- errors: 0
- ruined: false

## 재현 성공 조건

trades, wins, losses가 모두 일치해야 한다. errors는 0이어야 하고 ruined는 false여야 한다. official_cd_value, max_drawdown_pct, max_return_pct는 위 기준값과 근접해야 한다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_max 기준은 MDD 제한 없이 official_cd_value 최대다.

## 다음 개발의 시작점

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 atr_stop: `1.10`
- 기준 rr_target: `3.50`
- 기준 max_hold_bars: `21`
- 기준 cooldown_bars: `31`
- 기준 cd_value: `400.7817008962534`

## 기준선 갱신 후보 판정 규칙

1. errors == 0
2. ruined == false
3. 2025년까지의 데이터 기준 official_cd_value > 400.7817008962534
4. 단독 재백테스트에서 결과 재현 가능
