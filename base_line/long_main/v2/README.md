# long_main v2 기준선 갱신 기록

## 1. 공식 기준선 갱신

이 폴더는 long_main 공식 기준선을 v1에서 v2로 갱신하기 위한 기록이다.

- 이전 공식 기준선: `6V2_L01_doubleflush_core`
- 갱신 기준선: `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`
- 개발 결과 원천 폴더: `local_results/long_main/LONG_MAIN_DEV_V4_20260509_235230`
- 기준선 갱신 근거 후보: `LM4_014_ATTACK_BODY_NOT_HUGE`

v2는 완전히 새로운 전략이 아니다. v1 기준선인 `6V2_L01_doubleflush_core`의 진입 구조를 그대로 기본값으로 두고, 그 위에 추가 품질 조건을 붙인 기준선 기반 개선안이다.

---

## 2. 갱신 전 기준선 v1

전략명:

- `6V2_L01_doubleflush_core`

핵심 구조:

- cap reclaim
- double flush
- shock low 재확인
- bullish reclaim candle

복원 결과:

- trades: 592
- wins: 346
- losses: 246
- win_rate_pct: 58.4459459459
- final_return_pct: 23.8426079030
- max_return_pct: 24.0623399724
- max_drawdown_pct: 1.7279904306
- official_cd_value: 121.7026194894

---

## 3. 갱신 후 기준선 v2

전략명:

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

원본 개발 후보명:

- `LM4_014_ATTACK_BODY_NOT_HUGE`

핵심 구조:

- v1 기준선 진입 조건을 먼저 통과한다.
- 그 위에 `close_pos >= 0.77`을 추가한다.
- 그 위에 `vol_ratio >= 1.45`를 추가한다.
- 그 위에 `body_atr <= 1.60`을 추가한다.
- 개선안 규칙에 따라 TP03 확인을 유지한다.

결과:

- trades: 557
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- profit_factor: 3.8956015265
- verdict: baseline_win

---

## 4. v1 대비 개선

v1 대비 v2는 다음 항목에서 개선되었다.

- win_rate_pct: 58.4459 → 59.7846
- final_return_pct: 23.8426 → 23.9515
- max_return_pct: 24.0623 → 24.1477
- max_drawdown_pct: 1.7280 → 1.3006
- official_cd_value: 121.7026 → 122.3394

거래 수는 592건에서 557건으로 감소했다. 그러나 수익률과 MDD가 동시에 개선되었으므로 long_main v2 기준선으로 갱신한다.

---

## 5. 수수료와 자산분할 조건

v2 결과는 다음 조건에서 산출되었다.

- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- CSV 파일 수: 597

수수료와 자산분할 조건은 기존 기준선 규칙을 유지했다.

---

## 6. 폴더 파일 구성

- `README.md`: v2 기준선 갱신 요약
- `01_RESULT_SUMMARY.md`: 성과 결과 및 v1 대비 비교
- `02_ENTRY_CONDITIONS.md`: 진입 조건 상세 설명
- `03_STRENGTHS_WEAKNESSES_AND_NEXT.md`: 장단점과 다음 개발 방향
- `long_main_v2_lm4_014_strategy.py`: v2 기준선 진입 조건 코드

---

## 7. 향후 사용 규칙

앞으로 long_main 개발은 이 v2 기준선을 기준으로 진행한다.

다음 개발 파일에는 반드시 다음 후보를 포함해야 한다.

- `LONG_MAIN_V2_EXACT_EMBEDDED`

이 후보가 아래 값을 재현하지 못하면 개선안 평가로 넘어가면 안 된다.

- trades: 557
- max_return_pct: 약 24.1477
- max_drawdown_pct: 약 1.3006
- official_cd_value: 약 122.3394

즉, v2 기준선 복원이 먼저이고, 그다음에 추가 개선안을 평가한다.
