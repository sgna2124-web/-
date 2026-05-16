# long_main v13 재현 및 다음 개발 규칙

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 재현 기준값

- trades: 56697
- wins: 20962
- losses: 35735
- win_rate_pct: 36.97197382577562
- final_return_pct: 405.1480528315248
- max_return_pct: 405.8734002703171
- max_drawdown_pct: 1.228290350505734
- official_cd_value: 499.6598061090216
- max_conc: 444
- errors: 0
- ruined: false

## 재현 성공 조건

trades, wins, losses, max_conc가 모두 일치해야 한다. errors는 0이어야 하고 ruined는 false여야 한다. official_cd_value, max_drawdown_pct, max_return_pct는 위 기준값과 근접해야 한다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_main 기준은 `max_drawdown_pct < 5` 조건을 만족하는 전략 중 official_cd_value 최대다.

## 다음 개발의 시작점

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 atr_stop: `1.12`
- 기준 rr_target: `4.70`
- 기준 max_hold_bars: `18`
- 기준 cooldown_bars: `31`
- 기준 cd_value: `499.6598061090216`
- 기준 MDD: `1.228290350505734`

## 기준선 갱신 후보 판정 규칙

1. errors == 0
2. ruined == false
3. max_drawdown_pct < 5
4. 2025년까지의 데이터 기준 official_cd_value > 499.6598061090216
5. 단독 재백테스트에서 결과 재현 가능

## 허용되는 개선 방식

- 기준 entry에 방어 필터 추가
- 기준 entry에 과열 회피 필터 추가
- 기준 entry에 max_conc 감소 필터 추가
- atr_stop, rr_target, max_hold_bars, cooldown_bars 조정
- TP03 게이트 강화 또는 완화
- V24 상위 조합대인 stop 1.12~1.14, rr 4.50~4.70, hold 18 주변 재탐색

## 금지 및 주의 사항

1. 이전 v12의 `body_atr >= 0.25` 필터를 자동 계승하지 않는다.
2. 다음 long_main 개선 기준은 v13의 cd_value `499.6598061090216`이다.
3. v12 기준값 `491.134662921777`을 다음 개선 기준으로 쓰지 않는다.
4. cd_value 계산 시 final_return_pct가 아니라 max_return_pct를 사용한다.
5. 기준선 재현 없이 개선 후보를 평가하지 않는다.
6. 결과 저장 경로는 `local_results`를 사용한다. `local_result`가 아니다.

## 인수인계 문장

`long_main 현재 기준선은 v13 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18이다. 2025년까지의 데이터 기준 MDD 5% 미만 조건을 유지하면서 cd_value 499.6598061090216 초과를 목표로 개선한다. 기준선 entry_key는 child::orig_V09_extreme_vol18::tp03이며, 청산 파라미터는 atr_stop 1.12, rr_target 4.70, max_hold 18, cooldown 31이다.`
