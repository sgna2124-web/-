# long_max v5 기준선 재현 시작 문서

## 공식 기준선

- axis: long_max
- version: v5
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 검증용으로 제외한다.

## 공식 결과값: 2025년까지의 기록

아래 값이 long_max v5의 공식 재현 기준이다.

| 항목 | 값 |
|---|---:|
| trades | 56704 |
| wins | 20348 |
| losses | 36356 |
| win_rate_pct | 35.884593679458234 |
| final_return_pct | 305.5299492881062 |
| max_return_pct | 305.8271270102085 |
| max_drawdown_pct | 1.24324515986044 |
| official_cd_value | 400.7817008962534 |
| max_conc | 441 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

cd_value 계산에는 final_return_pct가 아니라 max_return_pct를 사용한다.

## 재현 성공 판정

1. trades == 56704
2. wins == 20348
3. losses == 36356
4. errors == 0
5. ruined == false
6. official_cd_value가 400.7817008962534 근처일 것
7. max_drawdown_pct가 1.24324515986044 근처일 것
8. max_return_pct가 305.8271270102085 근처일 것

## 다음 개발 기준

long_max 다음 개선 목표는 2025년까지의 데이터 기준 `official_cd_value > 400.7817008962534` 달성이다.
