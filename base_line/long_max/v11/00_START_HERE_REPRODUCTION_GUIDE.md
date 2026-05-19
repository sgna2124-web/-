# long_max v11 기준선 재현 시작 문서

## 공식 기준선

- axis: long_max
- version: v11
- source batch: `LONG_MAIN_LM23_RANK1_RETEST_20260519_213610`
- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- development origin: `LONG_MAIN_DEV_V23_NARROW_STOP_RR_BODY_20260519_205353`
- side: long
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

## 공식 전략명

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18__LM21_stop115_rr480_body020_hold17__LM22_stop120_rr500_body020_hold17__LM23_stop121_rr505_body022_hold17`

## 재현 핵심

long_max v11은 long_main v16과 같은 후보를 기준선으로 승격한 것이다.

```text
entry_source = child::orig_V09_extreme_vol18::tp03
final_entry = entry_source AND body_atr >= 0.22
```

TP03 source:

```text
atr_stop = 1.10
rr_target = 3.80
min_target_pct = 0.30
```

Final exit:

```text
atr_stop = 1.21
rr_target = 5.05
max_hold_bars = 17
cooldown_bars = 31
```

## 공식 결과값

| metric | expected |
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

## 다음 개발 첫 후보

다음 long_max 개발 파일의 0번 후보는 반드시 다음이어야 한다.

`LMAX##_000_LONG_MAX_V11_EXACT_FROZEN`

이 후보는 `LM23R_001_RETEST_S121_RR505_B022_H17`와 동일해야 한다.
