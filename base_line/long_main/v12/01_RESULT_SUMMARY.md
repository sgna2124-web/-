# long_main v12 결과 요약

## 기준선

- axis: long_main
- version: v12
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

## long_main v11 대비

| metric | v11 | v12 | change |
|---|---:|---:|---:|
| trades | 56651 | 56428 | -223 |
| wins | 20168 | 20531 | +363 |
| losses | 36483 | 35897 | -586 |
| win_rate_pct | 35.600430707313194 | 36.38441908272489 | +0.783988375411696 |
| final_return_pct | 358.93258386772163 | 397.7275034318756 | +38.79491956415397 |
| max_return_pct | 359.3568623293992 | 398.29373996834414 | +38.93687763894494 |
| max_drawdown_pct | 1.2516306589841375 | 1.4367182391297861 | +0.1850875801456486 |
| official_cd_value | 453.60741100633686 | 491.134662921777 | +37.52725191544014 |
| max_conc | 442 | 443 | +1 |

## v17 RR520 단독 대비

| metric | LM17_024_RR520 | LM18_041_STOP115_RR520_BODY025 | change |
|---|---:|---:|---:|
| wins | 20085 | 20531 | +446 |
| losses | 36537 | 35897 | -640 |
| max_drawdown_pct | 1.3226869764367266 | 1.4367182391297861 | +0.1140312626930595 |
| official_cd_value | 481.7602961439462 | 491.134662921777 | +9.3743667778308 |

## 해석

v12는 단순히 RR을 더 늘린 개선이 아니다. `atr_stop=1.15`, `rr_target=5.20`, `body_atr >= 0.25` 조합으로 wins가 늘고 losses가 줄었다. MDD는 v11과 RR520 단독보다 높아졌지만, long_main 기준인 MDD 5% 미만을 충분히 만족한다.

공식 cd 기준으로 long_main 기준선 갱신이 가능하다.
