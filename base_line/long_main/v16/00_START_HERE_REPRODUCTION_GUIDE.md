# long_main v16 기준선 재현 시작 문서

## 공식 기준선

- axis: long_main
- version: v16
- source batch: `LONG_MAIN_LM23_RANK1_RETEST_20260519_213610`
- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- development origin: `LONG_MAIN_DEV_V23_NARROW_STOP_RR_BODY_20260519_205353`
- winning candidate in v23: `LM23_S121_RR505_B022_H17`
- side: long
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외한다.

## 공식 전략명

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18__LM21_stop115_rr480_body020_hold17__LM22_stop120_rr500_body020_hold17__LM23_stop121_rr505_body022_hold17`

## 재현 핵심

이 기준선은 기존 entry source를 바꾸지 않는다.

```text
entry_source = child::orig_V09_extreme_vol18::tp03
final_entry = entry_source AND body_atr >= 0.22
```

TP03 entry source 계산은 다음 기준이다.

```text
ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80
TP03_MIN_TARGET_PCT = 0.30
```

최종 청산은 다음 기준이다.

```text
ATR_STOP = 1.21
RR_TARGET = 5.05
MAX_HOLD_BARS = 17
COOLDOWN_BARS = 31
```

TP03 gate를 최종 RR 5.05로 다시 계산하면 안 된다. entry source는 반드시 기존 TP03 계산 기준인 atr_stop 1.10, rr_target 3.80으로 만든다.

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

## 재현 검증 reference

단독 리테스트에서 다음 두 gate가 모두 true였다.

```text
pass_frozen_reproduction_gate = true
pass_rank1_retest_gate = true
```

reference 기준선 `LM22R_068`도 완전 재현됐다.

| reference metric | expected |
|---|---:|
| trades | 56591 |
| wins | 21871 |
| losses | 34720 |
| max_return_pct | 447.0278919263715 |
| max_drawdown_pct | 1.4424051244910419 |
| official_cd_value | 539.1375335808302 |
| max_conc | 444 |
| errors | 0 |
| ruined | false |

## 먼저 확인할 파일

1. `01_RESULT_SUMMARY.md`
2. `02_ENTRY_EXIT_CONDITIONS.md`
3. `03_STRATEGY_CODE_REFERENCE.py`
4. `04_STRENGTHS_WEAKNESSES.md`
5. `05_REPRODUCTION_AND_NEXT_DEV_RULES.md`
6. `06_FULL_REPRODUCTION_SPEC.md`

## 다음 개발 첫 후보

다음 long_main 개발 파일의 0번 후보는 반드시 다음이어야 한다.

`LM##_000_LONG_MAIN_V16_EXACT_FROZEN`

이 후보는 `LM23R_001_RETEST_S121_RR505_B022_H17`와 동일해야 한다.
