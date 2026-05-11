# long_max v3 결과 요약

## 1. 갱신 판정

long_max 기준선을 v2 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`에서 v3 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`으로 갱신한다.

갱신 이유:

- long_max 기준인 `MDD 제한 없이 cd_value 최대` 조건을 충족한다.
- v3의 cd_value는 `336.7657621418`로 v2의 `311.3750675807`보다 높다.
- 기준선 진입 조건은 그대로 유지하고, `atr_stop`만 1.01에서 1.10으로 조정한 직접 개선이다.

## 2. 개발 및 검증 원천

- 개발 배치: `LONG_MAX_V2_BASELINE_ENTRY_DEV_V13`
- 결과 위치: `local_results/long_max/LONG_MAX_V2_BASELINE_ENTRY_DEV_V13/`
- 기준선 재현 상태: `baseline_reproduction_ok = True`
- 기존 기준선 cd_value expected: `311.3750675807`
- 기존 기준선 cd_value actual: `311.37506758074795`
- V13 1위 전략: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`

## 3. v2 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20 |
| trades | 57243 |
| wins | 20312 |
| losses | 36931 |
| win_rate_pct | 35.4838146149 |
| final_return_pct | 214.7144460828 |
| max_return_pct | 215.2271020267 |
| max_drawdown_pct | 1.2219870757 |
| official_cd_value | 311.3750675807 |
| max_conc | 429 |

## 4. v3 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
| side | long |
| entry_key | child::orig_V09_extreme_vol18::tp03 |
| atr_stop | 1.10 |
| rr_target | 2.90 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |
| trades | 57114 |
| wins | 20911 |
| losses | 36203 |
| win_rate_pct | 36.6127394334 |
| final_return_pct | 240.7307747654 |
| max_return_pct | 241.3427142366 |
| max_drawdown_pct | 1.3408670828 |
| official_cd_value | 336.7657621418 |
| max_conc | 435 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 5. v2 대비 변화

| 항목 | v2 | v3 | 변화 |
|---|---:|---:|---:|
| trades | 57243 | 57114 | -129 |
| wins | 20312 | 20911 | +599 |
| losses | 36931 | 36203 | -728 |
| win_rate_pct | 35.4838146149 | 36.6127394334 | +1.1289248185 |
| final_return_pct | 214.7144460828 | 240.7307747654 | +26.0163286826 |
| max_return_pct | 215.2271020267 | 241.3427142366 | +26.1156122099 |
| max_drawdown_pct | 1.2219870757 | 1.3408670828 | +0.1188800071 |
| official_cd_value | 311.3750675807 | 336.7657621418 | +25.3906945610 |
| max_conc | 429 | 435 | +6 |

cd_value 개선율: 약 `+8.1544%`

## 6. long_max 기준 충족 여부

long_max 기준:

`MDD 제한 없이 전체 전략 중 official_cd_value 최대`

v3의 cd_value는 `336.7657621418`이고, v2 기준선 `311.3750675807`을 초과한다.

따라서 long_max 공식 기준선으로 갱신한다.

## 7. 다음 개선 기준

앞으로 long_max 개선은 v3을 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.10`, `rr_target 2.90`, `max_hold 21`, `cooldown 31`
- 목표: `official_cd_value > 336.7657621418`
