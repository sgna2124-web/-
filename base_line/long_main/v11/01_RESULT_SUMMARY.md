# long_main v11 결과 요약

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

## 이전 기준선 v10 대비

| metric | v10 | v11 | change |
|---|---:|---:|---:|
| trades | 56673 | 56651 | -22 |
| wins | 20255 | 20168 | -87 |
| losses | 36418 | 36483 | +65 |
| win_rate_pct | 35.740123162705345 | 35.600430707313194 | -0.139692455392151 |
| final_return_pct | 332.2800895520915 | 358.93258386772163 | +26.65249431563013 |
| max_return_pct | 332.5601665725121 | 359.3568623293992 | +26.7966957568871 |
| max_drawdown_pct | 1.2943172013524573 | 1.2516306589841375 | -0.0426865423683198 |
| official_cd_value | 426.96146593036525 | 453.60741100633686 | +26.64594507597161 |
| max_conc | 442 | 442 | 0 |

## 해석

v11은 거래 수, 승률, wins/losses 구조만 보면 v10보다 약간 불리하다. 그러나 rr_target을 4.20으로 올리면서 max_return_pct가 크게 증가했고, max_drawdown_pct는 오히려 낮아졌다. long_main 기준인 MDD 5% 미만을 충분히 만족하면서 official_cd_value가 약 +26.6459 증가했으므로 기준선 갱신이 가능하다.

## cd_value 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

final_return_pct가 아니라 max_return_pct를 사용한다.
