# long_max v5 결과 요약

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 기준선 전략

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`

## 공식 결과값: 2025년까지의 기록

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
| side | long |
| entry_key | child::orig_V09_extreme_vol18::tp03 |
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |
| trades | 56704 |
| wins | 20348 |
| losses | 36356 |
| win_rate_pct | 35.884593679458234 |
| final_return_pct | 305.5299492881062 |
| max_return_pct | 305.8271270102085 |
| max_drawdown_pct | 1.24324515986044 |
| official_cd_value | 400.7817008962534 |
| max_conc | 441 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 다음 개선 기준

앞으로 long_max 개선은 위 2025년까지의 결과값을 기준으로 한다.

- 목표: `official_cd_value > 400.7817008962534`
