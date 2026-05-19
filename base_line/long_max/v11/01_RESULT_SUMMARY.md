# long_max v11 결과 요약

## 기준선

- axis: long_max
- version: v11
- source batch: `LONG_MAIN_LM23_RANK1_RETEST_20260519_213610`
- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- result scope: 2025년까지의 데이터 기준

## 공식 결과

| metric | value |
|---|---:|
| trades | 56551 |
| wins | 21969 |
| losses | 34582 |
| win_rate_pct | 38.84811939665081 |
| final_return_pct | 454.0898854634718 |
| max_return_pct | 455.0171719748199 |
| max_drawdown_pct | 1.3974597812998368 |
| official_cd_value | 547.2610302171641 |
| max_conc | 445 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## long_max v8 대비

| metric | v8 | v11 | change |
|---|---:|---:|---:|
| trades | 56428 | 56551 | +123 |
| wins | 20531 | 21969 | +1438 |
| losses | 35897 | 34582 | -1315 |
| max_return_pct | 398.29373996834414 | 455.0171719748199 | +56.7234320064758 |
| max_drawdown_pct | 1.4367182391297861 | 1.3974597812998368 | -0.0392584578299493 |
| official_cd_value | 491.134662921777 | 547.2610302171641 | +56.1263672953871 |
| max_conc | 443 | 445 | +2 |

## 직전 검증 기준 LM22R_068 대비

| metric | LM22R_068 | v11 | change |
|---|---:|---:|---:|
| official_cd_value | 539.1375335808302 | 547.2610302171641 | +8.1234966363339 |
| max_return_pct | 447.0278919263715 | 455.0171719748199 | +7.9892800484484 |
| max_drawdown_pct | 1.4424051244910419 | 1.3974597812998368 | -0.0449453431912051 |
| wins | 21871 | 21969 | +98 |
| losses | 34720 | 34582 | -138 |
| max_conc | 444 | 445 | +1 |

## 판정

long_max 기준선 갱신 가능.

long_max는 official_cd_value 최대를 중심으로 평가한다. v11은 v8과 직전 검증 기준 LM22R_068을 모두 넘었고, 단독 리테스트에서 errors 0으로 재현됐다.
