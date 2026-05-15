# long_main v10 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380`

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 결과값

- trades: `56673`
- wins: `20255`
- losses: `36418`
- win_rate_pct: `35.740123162705345`
- final_return_pct: `332.2800895520915`
- max_return_pct: `332.5601665725121`
- max_drawdown_pct: `1.2943172013524573`
- official_cd_value: `426.96146593036525`
- max_conc: `442`
- errors: `0`
- ruined: `false`

## 장점

1. v9 대비 cd_value가 크게 상승했다.

- v9: `400.7817008962534`
- v10: `426.96146593036525`
- 개선폭: `+26.179765034111824`

2. long_main의 MDD 제한을 충분히 통과한다.

- 기준: `MDD < 5%`
- v10 MDD: `1.2943172013524573%`

3. 진입 조건을 유지한 직접 개선이다.

- entry_key: `child::orig_V09_extreme_vol18::tp03`
- 변경점: `rr_target 3.50 -> 3.80`

4. 단독 리테스트에서 완전 재현됐다.

- V19 탐색 결과와 V20 단독 리테스트 결과가 trades, wins, losses, cd_value까지 일치했다.

## 단점

1. MDD가 소폭 증가했다.

- v9: `1.24324515986044`
- v10: `1.2943172013524573`
- 변화: `+0.0510720414920173%p`

2. 승률이 소폭 낮아졌다.

- v9: `35.884593679458234%`
- v10: `35.740123162705345%`

3. max_conc가 442로 증가했다.

- v9: `441`
- v10: `442`

## 다음 개선 방향

long_main의 다음 목표는 2025년까지의 데이터 기준 `max_drawdown_pct < 5` 유지와 `official_cd_value > 426.96146593036525` 달성이다.

우선순위:

1. MDD 5% 미만 유지
2. cd_value 초과
3. max_conc 442 이하 완화
4. 승률 하락 보완
5. 수수료 민감도 감소
