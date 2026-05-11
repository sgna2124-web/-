# long_main v5 기준선 갱신 기록

## 1. 공식 기준선 갱신

이 폴더는 long_main 공식 기준선을 v4에서 v5로 갱신하기 위한 기록이다.

- 이전 공식 기준선: `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`
- 갱신 기준선: `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`
- 개발 결과 원천 폴더: `local_results/long_main/LONG_MAIN_DEV_V9_20260511_132134`
- 기준선 갱신 근거 후보: `LM9_012_V4_SHOCK_RECENCY_3`

v5는 완전히 새로운 전략이 아니다. v4 기준선의 핵심 구조를 그대로 유지하면서, 최근 shock 문맥이 너무 오래된 진입을 제거하기 위해 `shock_recency <= 3` 조건을 추가한 기준선 기반 방어형 개선안이다.

v5의 핵심 변화는 다음 하나다.

```text
v4 기준선
+
shock_recency <= 3
```

즉, v4에서 확인된 `ret20 <= -0.08`, `vol_ratio >= 1.45`, `body_atr <= 2.20` 구조는 유지하고, double flush 문맥 안에서 가장 최근 shock_down이 현재 진입봉 기준 3봉 이내에 있어야 한다.

---

## 2. 갱신 전 기준선 v4

전략명:

- `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 2.20
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

복원 결과:

- trades: 479
- wins: 310
- losses: 169
- win_rate_pct: 64.7181628392
- final_return_pct: 24.9404780954
- max_return_pct: 25.2063735035
- max_drawdown_pct: 1.0904624350
- official_cd_value: 123.5780610685
- profit_factor: 4.5655373148

---

## 3. 갱신 후 기준선 v5

전략명:

- `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`

원본 개발 후보명:

- `LM9_012_V4_SHOCK_RECENCY_3`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 2.20
AND ret20 <= -0.08
AND shock_recency <= 3
AND expected_tp >= 0.003
```

중요 복원 포인트:

```text
v5에는 close_pos >= 0.77 추가 조건이 없다.
하지만 raw_l01_cap_reclaim 내부의 close_pos > 0.70은 유지한다.

double_flush_ok는 기존처럼 최근 10봉 안의 shock_down을 요구한다.
v5는 그중 가장 최근 shock_down이 현재 진입봉 기준 3봉 이내인지 추가로 확인한다.
```

결과:

- trades: 447
- wins: 297
- losses: 150
- win_rate_pct: 66.4429530201
- final_return_pct: 24.8492730067
- max_return_pct: 25.0899569668
- max_drawdown_pct: 0.9930660871
- official_cd_value: 123.6093482796
- profit_factor: 4.9302639666
- verdict: baseline_win

---

## 4. v4 대비 개선

v4 대비 v5는 다음 항목에서 개선되었다.

- win_rate_pct: 64.7182 → 66.4430
- max_drawdown_pct: 1.0905 → 0.9931
- official_cd_value: 123.5781 → 123.6093
- profit_factor: 4.5655 → 4.9303

다만 수익 관련 절대값은 소폭 낮아졌다.

- trades: 479 → 447
- final_return_pct: 24.9405 → 24.8493
- max_return_pct: 25.2064 → 25.0900

해석:

- v5는 v4보다 더 방어적인 기준선이다.
- 수익률은 아주 약간 낮아졌지만 MDD, 승률, PF, cd_value가 개선되었다.
- 프로젝트 기준상 cd_value가 개선되었고 기준선 갱신이 가능하므로 v5로 갱신한다.

---

## 5. 수수료와 자산분할 조건

v5 결과는 다음 조건에서 산출되었다.

- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- CSV 파일 수: 597
- workers: 1
- variants: 14

기존 기준선의 수수료와 자산분할 조건을 유지했다.

---

## 6. 리소스 절약형 개발 기록

v5는 v9 리소스 절약형 개발 배치에서 나왔다.

v9의 리소스 설계:

- 기본 workers=1
- 후보 수 14개로 축소
- 파일 단위 순차 처리 중심
- 4축(long_main, long_max, short_main, short_max) 동시 백테스트 시 CPU/RAM 과부하를 줄이기 위한 구조

다음 long_main 개발도 이 원칙을 유지한다.

---

## 7. 폴더 파일 구성

- `README.md`: v5 기준선 갱신 요약
- `01_RESULT_SUMMARY.md`: 성과 결과 및 v4 대비 비교
- `02_ENTRY_CONDITIONS.md`: 진입 조건 상세 설명
- `03_STRENGTHS_WEAKNESSES_AND_NEXT.md`: 장단점과 다음 개발 방향
- `long_main_v5_lm9_012_strategy.py`: v5 기준선 진입 조건 코드

---

## 8. 향후 사용 규칙

앞으로 long_main 개발은 이 v5 기준선을 기준으로 진행한다.

다음 개발 파일에는 반드시 다음 후보를 포함해야 한다.

- `LONG_MAIN_V5_EXACT_EMBEDDED`

이 후보가 아래 값을 재현하지 못하면 개선안 평가로 넘어가면 안 된다.

- trades: 447
- max_return_pct: 약 25.0900
- max_drawdown_pct: 약 0.9931
- official_cd_value: 약 123.6093

즉, v5 기준선 복원이 먼저이고, 그다음에 추가 개선안을 평가한다.
