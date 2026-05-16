# long_max v7 결과 요약

## 기준선

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420`
- source_candidate: `LM15_031_V10_RR420`
- result_scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외
- symbol_files: 597
- fee: round_trip_cost_bps 8.0
- position_fraction: 0.01

## 공식 결과

| metric | value |
|---|---:|
| trades | 56651 |
| wins | 20168 |
| losses | 36483 |
| win_rate_pct | 35.600430707313194 |
| final_return_pct | 358.93258386772163 |
| max_return_pct | 359.3568623293992 |
| max_drawdown_pct | 1.2516306589841375 |
| official_cd_value | 453.60741100633686 |
| max_conc | 442 |
| errors | 0 |
| ruined | false |

## 이전 기준선 v6 대비

| metric | v6 | v7 | change |
|---|---:|---:|---:|
| trades | 56673 | 56651 | -22 |
| wins | 20255 | 20168 | -87 |
| losses | 36418 | 36483 | +65 |
| final_return_pct | 332.2800895520915 | 358.93258386772163 | +26.65249431563013 |
| max_return_pct | 332.5601665725121 | 359.3568623293992 | +26.7966957568871 |
| max_drawdown_pct | 1.2943172013524573 | 1.2516306589841375 | -0.0426865423683198 |
| official_cd_value | 426.96146593036525 | 453.60741100633686 | +26.64594507597161 |
| max_conc | 442 | 442 | 0 |

## 해석

long_max는 MDD 제한 없이 official_cd_value 최대를 기준으로 본다. v7은 v6 대비 official_cd_value를 크게 높였고, max_drawdown_pct도 낮아졌다. 따라서 long_max 기준선 갱신이 가능하다.
