# long_main v4 기준선 갱신 기록

## 1. 공식 기준선 갱신

이 폴더는 long_main 공식 기준선을 v3에서 v4로 갱신하기 위한 기록이다.

- 이전 공식 기준선: `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- 갱신 기준선: `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`
- 개발 결과 원천 폴더: `local_results/long_main/LONG_MAIN_DEV_V8_20260511_101823`
- 기준선 갱신 근거 후보: `LM8_021_LOOSER_BODY_GUARD_220`

v4는 완전히 새로운 전략이 아니다. v3 기준선의 핵심 구조를 그대로 유지하면서, `body_atr <= 1.60` 상한을 `body_atr <= 2.20`으로 완화한 기준선 기반 개선안이다.

v4의 핵심 변화는 다음 하나다.

```text
body_atr <= 1.60  →  body_atr <= 2.20
```

즉, v3에서 확인된 `ret20 <= -0.08` 하락 압력 필터와 `vol_ratio >= 1.45` 거래량 필터는 유지하고, 충분히 빠진 뒤 강하게 반전하는 장대 회복봉을 더 허용한다.

---

## 2. 갱신 전 기준선 v3

전략명:

- `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 1.60
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

복원 결과:

- trades: 469
- wins: 303
- losses: 166
- win_rate_pct: 64.6055437100
- final_return_pct: 24.6575066055
- max_return_pct: 24.9228703822
- max_drawdown_pct: 1.0181358195
- official_cd_value: 123.3883238790
- profit_factor: 4.6238644584

---

## 3. 갱신 후 기준선 v4

전략명:

- `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`

원본 개발 후보명:

- `LM8_021_LOOSER_BODY_GUARD_220`

핵심 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 2.20
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

중요 복원 포인트:

```text
v4에는 close_pos >= 0.77 추가 조건이 없다.
하지만 v1 raw_l01_cap_reclaim 내부의 close_pos > 0.70은 유지한다.
```

결과:

- trades: 479
- wins: 310
- losses: 169
- win_rate_pct: 64.7181628392
- final_return_pct: 24.9404780954
- max_return_pct: 25.2063735035
- max_drawdown_pct: 1.0904624350
- official_cd_value: 123.5780610685
- profit_factor: 4.5655373148
- verdict: baseline_win

---

## 4. v3 대비 개선

v3 대비 v4는 다음 항목에서 개선되었다.

- trades: 469 → 479
- wins: 303 → 310
- losses: 166 → 169
- win_rate_pct: 64.6055 → 64.7182
- final_return_pct: 24.6575 → 24.9405
- max_return_pct: 24.9229 → 25.2064
- official_cd_value: 123.3883 → 123.5781

다만 MDD는 소폭 증가했다.

- max_drawdown_pct: 1.0181 → 1.0905

해석:

- v4는 v3보다 더 많은 거래를 허용한다.
- 수익률과 max_return이 개선되었다.
- cd_value도 상승했다.
- MDD는 증가했지만 상승폭이 제한적이다.

따라서 long_main v4 공식 기준선으로 갱신한다.

---

## 5. 수수료와 자산분할 조건

v4 결과는 다음 조건에서 산출되었다.

- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- CSV 파일 수: 597

기존 기준선의 수수료와 자산분할 조건을 유지했다.

---

## 6. 폴더 파일 구성

- `README.md`: v4 기준선 갱신 요약
- `01_RESULT_SUMMARY.md`: 성과 결과 및 v3 대비 비교
- `02_ENTRY_CONDITIONS.md`: 진입 조건 상세 설명
- `03_STRENGTHS_WEAKNESSES_AND_NEXT.md`: 장단점과 다음 개발 방향
- `long_main_v4_lm8_021_strategy.py`: v4 기준선 진입 조건 코드

---

## 7. 향후 사용 규칙

앞으로 long_main 개발은 이 v4 기준선을 기준으로 진행한다.

다음 개발 파일에는 반드시 다음 후보를 포함해야 한다.

- `LONG_MAIN_V4_EXACT_EMBEDDED`

이 후보가 아래 값을 재현하지 못하면 개선안 평가로 넘어가면 안 된다.

- trades: 479
- max_return_pct: 약 25.2064
- max_drawdown_pct: 약 1.0905
- official_cd_value: 약 123.5781

즉, v4 기준선 복원이 먼저이고, 그다음에 추가 개선안을 평가한다.
