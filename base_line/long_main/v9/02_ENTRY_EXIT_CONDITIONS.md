# long_main v9 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 검증용으로 제외한다.

## 공식 재현값: 2025년까지의 기록

- trades: `56704`
- wins: `20348`
- losses: `36356`
- win_rate_pct: `35.884593679458234`
- final_return_pct: `305.5299492881062`
- max_return_pct: `305.8271270102085`
- max_drawdown_pct: `1.24324515986044`
- official_cd_value: `400.7817008962534`
- max_conc: `441`
- symbol_files: `597`
- errors: `0`
- ruined: `false`

## 고정 청산 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| round_trip_cost_bps | 8.0 |
| position_fraction | 0.01 |
