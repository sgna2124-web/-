# long_main v11 재현 및 다음 개발 규칙

## source of truth

long_main v11의 source of truth는 다음 파일이다.

1. `00_START_HERE_REPRODUCTION_GUIDE.md`
2. `01_RESULT_SUMMARY.md`
3. `02_ENTRY_EXIT_CONDITIONS.md`
4. `03_FROZEN_BASELINE_RUNNER.py`

설명과 코드가 충돌하면 frozen runner의 상수와 v15 재현 결과를 우선한다.

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

## 다음 개발의 첫 후보

다음 롱메인 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LM##_000_LONG_MAIN_V11_EXACT_FROZEN`

이 후보는 기존 v15의 `LM15_031_V10_RR420`과 동일한 조건이어야 한다.

## baseline audit 규칙

다음 개발 코드에는 반드시 `baseline_audit.json`을 생성한다.

필수 항목:

- baseline_strategy
- baseline_version: `long_main/v11`
- baseline_candidate
- expected
- actual
- pass_frozen_reproduction_gate
- train_end_exclusive_utc
- out_dir_policy
- round_trip_cost_bps
- position_fraction

## 기준선 재현 실패 시 규칙

`LM##_000_LONG_MAIN_V11_EXACT_FROZEN`이 아래 중 하나라도 틀리면 개선 후보 결과는 무효다.

- trades
- wins
- losses
- max_conc
- errors
- ruined
- official_cd_value
- max_drawdown_pct
- max_return_pct

재현 실패 시 해야 할 일:

1. summary 순위를 말하지 않는다.
2. 기준선 갱신 가능 여부를 말하지 않는다.
3. `BASELINE_REPRODUCTION_FAILED`로 기록한다.
4. entry/feature/exit/cooldown/time filter 구현 차이를 먼저 찾는다.

## 다음 갱신 조건

long_main 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. max_drawdown_pct < 5
5. official_cd_value > 453.60741100633686
6. 단독 재백테스트에서 재현 가능

## 개발 금지 사항

- 기준선 전략명을 보고 조건을 추정하지 않는다.
- V09/extreme/vol18/tp03를 임의로 재해석하지 않는다.
- 기준선 entry를 대체하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
- 기준선 exact 없이 개선 후보를 평가하지 않는다.

## 허용되는 개발 방향

- 기준선 entry 위에 AND 필터 추가
- 기준선 entry 일부를 명시적으로 완화/강화하되, 기존 조건과 차이를 문서화
- rr_target, atr_stop, max_hold, cooldown 변형
- MDD 방어 필터
- max_conc 또는 동시성 제어 실험
- 2026년 별도 검증
