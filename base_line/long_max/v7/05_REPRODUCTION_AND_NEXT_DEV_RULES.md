# long_max v7 재현 및 다음 개발 규칙

## 공식 기준선

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420`
- source_candidate: `LM15_031_V10_RR420`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- atr_stop: 1.10
- rr_target: 4.20
- max_hold_bars: 21
- cooldown_bars: 31
- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- train_end_exclusive_utc: `2026-01-01 00:00:00`

## 재현해야 할 값

| metric | expected |
|---|---:|
| trades | 56651 |
| wins | 20168 |
| losses | 36483 |
| max_return_pct | 359.3568623293992 |
| max_drawdown_pct | 1.2516306589841375 |
| official_cd_value | 453.60741100633686 |
| max_conc | 442 |
| errors | 0 |
| ruined | false |

## 다음 개발 첫 후보

다음 long_max 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LMAX##_000_LONG_MAX_V7_EXACT_FROZEN`

이 후보는 기존 v15의 `LM15_031_V10_RR420`과 동일한 조건이어야 한다.

## 갱신 조건

long_max 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. official_cd_value > 453.60741100633686
5. 단독 재백테스트에서 재현 가능

## 기준선 재현 실패 시 규칙

기준선 exact가 실패하면 개선 후보 결과를 인정하지 않는다. summary 순위를 말하지 않고 `BASELINE_REPRODUCTION_FAILED`로 처리한다.

## 금지 사항

- 기준선 전략명을 보고 조건을 추정하지 않는다.
- V09/extreme/vol18/tp03를 임의로 재해석하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
- 기준선 exact 없이 개선 후보를 평가하지 않는다.
