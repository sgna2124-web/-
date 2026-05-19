# long_main v16 결과 요약

## 기준선

- axis: long_main
- version: v16
- source batch: `LONG_MAIN_LM23_RANK1_RETEST_20260519_213610`
- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- development source: `LONG_MAIN_DEV_V23_NARROW_STOP_RR_BODY_20260519_205353`
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

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

## 직전 기준 LM22R_068 대비

| metric | LM22R_068 | v16 | change |
|---|---:|---:|---:|
| trades | 56591 | 56551 | -40 |
| wins | 21871 | 21969 | +98 |
| losses | 34720 | 34582 | -138 |
| win_rate_pct | 38.64748811648495 | 38.84811939665081 | +0.20063128016586 |
| final_return_pct | 446.12552394206125 | 454.0898854634718 | +7.96436152141055 |
| max_return_pct | 447.0278919263715 | 455.0171719748199 | +7.9892800484484 |
| max_drawdown_pct | 1.4424051244910419 | 1.3974597812998368 | -0.0449453431912051 |
| official_cd_value | 539.1375335808302 | 547.2610302171641 | +8.1234966363339 |
| max_conc | 444 | 445 | +1 |

## long_main v13 대비

| metric | v13 | v16 | change |
|---|---:|---:|---:|
| trades | 56697 | 56551 | -146 |
| wins | 20962 | 21969 | +1007 |
| losses | 35735 | 34582 | -1153 |
| max_return_pct | 405.8734002703171 | 455.0171719748199 | +49.1437717045028 |
| max_drawdown_pct | 1.228290350505734 | 1.3974597812998368 | +0.1691694307941028 |
| official_cd_value | 499.6598061090216 | 547.2610302171641 | +47.6012241081425 |

## 판정

long_main 기준선 갱신 가능.

이 후보는 리테스트에서 `pass_frozen_reproduction_gate=true`, `pass_rank1_retest_gate=true`, `errors=0`을 기록했다. cd_value와 max_return이 상승했고, 직전 기준 LM22R_068 대비 MDD는 낮아졌으며 wins는 늘고 losses는 줄었다. 단점은 max_conc가 445로 1 증가한 것이다.
