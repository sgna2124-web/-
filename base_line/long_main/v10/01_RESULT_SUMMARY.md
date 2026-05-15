# long_main v10 결과 요약

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 기준선 전략

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380`

## 공식 결과값: 2025년까지의 기록

| 항목 | 값 |
|---|---:|
| trades | 56673 |
| wins | 20255 |
| losses | 36418 |
| win_rate_pct | 35.740123162705345 |
| final_return_pct | 332.2800895520915 |
| max_return_pct | 332.5601665725121 |
| max_drawdown_pct | 1.2943172013524573 |
| official_cd_value | 426.96146593036525 |
| max_conc | 442 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## v9 대비 변화

| 항목 | v9 | v10 | 변화 |
|---|---:|---:|---:|
| trades | 56704 | 56673 | -31 |
| wins | 20348 | 20255 | -93 |
| losses | 36356 | 36418 | +62 |
| win_rate_pct | 35.884593679458234 | 35.740123162705345 | -0.144470516752889 |
| final_return_pct | 305.5299492881062 | 332.2800895520915 | +26.7501402639853 |
| max_return_pct | 305.8271270102085 | 332.5601665725121 | +26.7330395623036 |
| max_drawdown_pct | 1.24324515986044 | 1.2943172013524573 | +0.0510720414920173 |
| official_cd_value | 400.7817008962534 | 426.96146593036525 | +26.179765034111824 |
| max_conc | 441 | 442 | +1 |

## long_main 기준 충족 여부

- MDD: `1.2943172013524573 < 5`
- 기준: `MDD 5% 미만 전략 중 official_cd_value 최대`

## 다음 개선 기준

앞으로 long_main 개선은 v10을 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.10`, `rr_target 3.80`, `max_hold 21`, `cooldown 31`
- 목표: `max_drawdown_pct < 5` 유지 + `official_cd_value > 426.96146593036525`
