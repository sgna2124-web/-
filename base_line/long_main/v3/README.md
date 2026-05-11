# long_main v3 기준선 갱신 기록

## 1. 공식 기준선 갱신

이 폴더는 long_main 공식 기준선을 v2에서 v3로 갱신하기 위한 기록이다.

- 이전 공식 기준선: `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`
- 갱신 기준선: `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- 개발 결과 원천 폴더: `local_results/long_main/LONG_MAIN_DEV_V7_20260510_221655`
- 기준선 갱신 근거 후보: `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

v3는 완전히 새로운 전략이 아니다. v1의 `raw_l01_cap_reclaim + double_flush_ok` 구조를 그대로 유지하고, v2에서 검증된 `vol_ratio >= 1.45`, `body_atr <= 1.60`을 유지한 상태에서, v6 진단 결과로 확인된 `ret20 <= -0.08` 조건을 추가한 기준선 기반 개선안이다.

중요한 차이는 v2의 추가 조건이었던 `close_pos >= 0.77`을 제거했다는 점이다. 단, close_pos 조건이 완전히 사라진 것은 아니다. v1 raw 조건 안의 `close_pos > 0.70`은 그대로 유지된다.

---

## 2. 갱신 전 기준선 v2

전략명:

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND close_pos >= 0.77
AND vol_ratio >= 1.45
AND body_atr <= 1.60
AND expected_tp >= 0.003
```

복원 결과:

- trades: 557
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- profit_factor: 3.8956015265

---

## 3. 갱신 후 기준선 v3

전략명:

- `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

원본 개발 후보명:

- `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 1.60
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

주의:

```text
v2의 close_pos >= 0.77 추가 조건은 제거한다.
하지만 v1 raw_l01_cap_reclaim 내부의 close_pos > 0.70은 유지한다.
```

결과:

- trades: 469
- trade_ratio_vs_ref: 0.8420107720
- wins: 303
- losses: 166
- win_rate_pct: 64.6055437100
- final_return_pct: 24.6575066055
- max_return_pct: 24.9228703822
- max_drawdown_pct: 1.0181358195
- official_cd_value: 123.3883238790
- profit_factor: 4.6238644584
- verdict: baseline_win

---

## 4. v2 대비 개선

v2 대비 v3는 다음 항목이 모두 개선되었다.

- win_rate_pct: 59.7846 → 64.6055
- final_return_pct: 23.9515 → 24.6575
- max_return_pct: 24.1477 → 24.9229
- max_drawdown_pct: 1.3006 → 1.0181
- official_cd_value: 122.3394 → 123.3883
- profit_factor: 3.8956 → 4.6239

거래 수는 557건에서 469건으로 줄었다. 그러나 수익률, 최대수익, 승률, MDD, cd_value가 모두 개선되었으므로 long_main v3 공식 기준선으로 갱신한다.

---

## 5. 수수료와 자산분할 조건

v3 결과는 다음 조건에서 산출되었다.

- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- CSV 파일 수: 597

기존 기준선의 수수료와 자산분할 조건을 유지했다.

---

## 6. 폴더 파일 구성

- `README.md`: v3 기준선 갱신 요약
- `01_RESULT_SUMMARY.md`: 성과 결과 및 v2 대비 비교
- `02_ENTRY_CONDITIONS.md`: 진입 조건 상세 설명
- `03_STRENGTHS_WEAKNESSES_AND_NEXT.md`: 장단점과 다음 개발 방향
- `long_main_v3_lm7_070_strategy.py`: v3 기준선 진입 조건 코드

---

## 7. 향후 사용 규칙

앞으로 long_main 개발은 이 v3 기준선을 기준으로 진행한다.

다음 개발 파일에는 반드시 다음 후보를 포함해야 한다.

- `LONG_MAIN_V3_EXACT_EMBEDDED`

이 후보가 아래 값을 재현하지 못하면 개선안 평가로 넘어가면 안 된다.

- trades: 469
- max_return_pct: 약 24.9229
- max_drawdown_pct: 약 1.0181
- official_cd_value: 약 123.3883

즉, v3 기준선 복원이 먼저이고, 그다음에 추가 개선안을 평가한다.
