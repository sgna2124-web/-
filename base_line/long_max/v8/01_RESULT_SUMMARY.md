# long_max v8 결과 요약

## 기준선

- axis: long_max
- version: v8
- source batch: `LONG_MAIN_DEV_V18_20260516_213239`
- source candidate: `LM18_041_STOP115_RR520_BODY025`
- data scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

## 공식 결과

| metric | value |
|---|---:|
| trades | 56428 |
| wins | 20531 |
| losses | 35897 |
| win_rate_pct | 36.38441908272489 |
| final_return_pct | 397.7275034318756 |
| max_return_pct | 398.29373996834414 |
| max_drawdown_pct | 1.4367182391297861 |
| official_cd_value | 491.134662921777 |
| max_conc | 443 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## long_max v7 대비

| metric | v7 | v8 | change |
|---|---:|---:|---:|
| trades | 56651 | 56428 | -223 |
| wins | 20168 | 20531 | +363 |
| losses | 36483 | 35897 | -586 |
| max_return_pct | 359.3568623293992 | 398.29373996834414 | +38.93687763894494 |
| max_drawdown_pct | 1.2516306589841375 | 1.4367182391297861 | +0.1850875801456486 |
| official_cd_value | 453.60741100633686 | 491.134662921777 | +37.52725191544014 |
| max_conc | 442 | 443 | +1 |

## 해석

long_max는 MDD 5% 제한보다 official_cd_value 최대를 우선한다. v8은 v7 대비 cd_value를 크게 높였고, wins/losses 구조도 개선됐다. 따라서 long_max 기준선 갱신이 가능하다.
