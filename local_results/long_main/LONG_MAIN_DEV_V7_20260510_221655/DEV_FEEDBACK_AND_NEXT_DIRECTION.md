# LONG_MAIN_DEV_V7 피드백 및 다음 개발 방향

## 1. 결론

v7은 성공이다.

공식 long_main v2 기준선을 정상 복원했고, v2 기준선을 명확히 넘는 신규 개선 후보를 발굴했다.

현재 v7 최우수 후보:

- `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

이 후보는 v2 기준선 대비 다음을 모두 개선했다.

- final_return_pct 개선
- max_return_pct 개선
- max_drawdown_pct 개선
- official_cd_value 개선
- win_rate_pct 개선

따라서 다음 단계에서는 이 후보를 중심으로 기준선 갱신 후보 검토 또는 추가 구조형 개선을 진행할 수 있다.

---

## 2. 실행 정보

- 결과 폴더: `local_results/long_main/LONG_MAIN_DEV_V7_20260510_221655`
- batch_label: `LONG_MAIN_DEV_V7_DIAG_BASED_STRUCTURAL_TEST`
- csv_files: 597
- variants: 26
- round_trip_cost_bps: 8.0
- position_fraction: 0.01
- elapsed_sec: 3561.9745
- errors: 없음

path_policy:

- 외부 하드코딩 경로 없음
- CLI 또는 현재/스크립트 기준 자동 탐색
- 결과는 실행 위치 기준 저장

---

## 3. 기준선 v2 복원 확인

기준선 감사 후보:

- `LM7_000_LONG_MAIN_V2_EXACT_EMBEDDED`

결과:

- trades: 557
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- pf: 3.8956015265
- verdict: baseline_win

판정:

- long_main v2 기준선 복원 성공
- v7 개선안 결과 해석 가능

---

## 4. v7 최우수 후보

### LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08

조건:

- v1 raw_l01_cap_reclaim 통과
- double_flush_ok 통과
- v2의 vol_ratio >= 1.45 유지
- v2의 body_atr <= 1.60 유지
- v2의 close_pos >= 0.77 추가 조건 제거
- ret20 <= -0.08 추가
- TP03 유지

중요:

- close_pos 조건을 완전히 없앤 것이 아니다.
- v1 raw 조건 안의 close_pos >= 0.70은 그대로 유지된다.
- 제거된 것은 v2에서 추가했던 close_pos >= 0.77 강화 조건이다.

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
- pf: 4.6238644584
- verdict: baseline_win

v2 기준선 대비:

- trades: 557 → 469
- wins: 333 → 303
- losses: 224 → 166
- win_rate_pct: 59.7846 → 64.6055
- final_return_pct: 23.9515 → 24.6575
- max_return_pct: 24.1477 → 24.9229
- max_drawdown_pct: 1.3006 → 1.0181
- official_cd_value: 122.3394 → 123.3883

판정:

- v7 최우수 후보
- 공격형/균형형 기준선 갱신 후보
- v6 진단에서 확인된 ret20 약한 하락 구간 손실 문제를 실제 백테스트에서 개선함

---

## 5. 주요 상위 후보

### 5.1 LM7_010_V2_RET20_DEEP_PULLBACK_08

조건:

- v2 기준선 유지
- ret20 <= -0.08 추가

결과:

- trades: 456
- wins: 298
- losses: 158
- win_rate_pct: 65.3508771930
- final_return_pct: 24.5580114246
- max_return_pct: 24.7475663428
- max_drawdown_pct: 0.9871119683
- official_cd_value: 123.3284843863
- pf: 4.8202538289

해석:

- v2 조건을 보존한 상태에서 가장 좋은 순수 개선 후보다.
- LM7_070보다 cd는 약간 낮지만 MDD는 더 낮다.
- 보수적으로 기준선을 갱신한다면 LM7_010도 강력한 후보가 된다.

### 5.2 LM7_063_V2_RET20_08_RECLAIM190

조건:

- v2 기준선 유지
- ret20 <= -0.08
- reclaim_atr <= 1.90

결과:

- trades: 418
- win_rate_pct: 66.9856459330
- final_return_pct: 24.2273151026
- max_return_pct: 24.4163667605
- max_drawdown_pct: 0.7949918724
- official_cd_value: 123.2397180443

해석:

- MDD를 0.795까지 낮춘 방어형/균형형 후보
- 수익률은 LM7_010, LM7_070보다 낮지만 안정성이 강하다.

### 5.3 LM7_064_V2_RET20_08_RECLAIM175

조건:

- v2 기준선 유지
- ret20 <= -0.08
- reclaim_atr <= 1.75

결과:

- trades: 402
- win_rate_pct: 67.9104477612
- final_return_pct: 24.1375509840
- max_return_pct: 24.3264660370
- max_drawdown_pct: 0.7253519568
- official_cd_value: 123.2371168288

해석:

- MDD는 더 낮지만 거래 수와 수익률이 더 줄었다.
- 방어형 기준 후보로는 가치가 있다.

### 5.4 LM7_065_V2_RET20_08_SHOCK3

조건:

- v2 기준선 유지
- ret20 <= -0.08
- shock_recency <= 3

결과:

- trades: 428
- win_rate_pct: 66.8224299065
- final_return_pct: 24.3767516310
- max_return_pct: 24.5410550894
- max_drawdown_pct: 0.9621049226
- official_cd_value: 123.1801167810

해석:

- ret20 + 신선한 shock 조합은 유효하다.
- 단, LM7_010보다 cd는 낮다.

### 5.5 LM7_020_V2_RET20_08_RET10_06

조건:

- v2 기준선 유지
- ret20 <= -0.08
- ret10 <= -0.06

결과:

- trades: 444
- win_rate_pct: 65.7657657658
- final_return_pct: 24.4370748636
- max_return_pct: 24.6264457381
- max_drawdown_pct: 1.0115619106
- official_cd_value: 123.1783168116

해석:

- ret20 단독보다 약간 낮다.
- ret10 추가는 일부 좋은 거래도 제거한 것으로 보인다.

---

## 6. v7의 핵심 발견

### 6.1 ret20 <= -0.08이 핵심 개선축이다

v6 진단에서 손실 거래는 덜 빠진 상태의 reclaim에 많이 몰려 있었다.

v7에서 이를 실제 백테스트로 검증한 결과 `ret20 <= -0.08` 계열이 상위권을 장악했다.

의미:

- long_main은 충분히 빠진 뒤의 reclaim에서 강하다.
- ret20이 덜 빠진 구간은 손실 과대표현 구간이다.
- ret20 <= -0.08은 공식 백테스트에서도 유효했다.

### 6.2 close_pos 0.77 강화 조건은 절대 필수가 아니다

LM7_070은 v2의 close_pos >= 0.77 추가 조건을 제거하고 ret20 <= -0.08을 붙인 후보다.

결과는 v7 전체 1위다.

해석:

- close_pos 0.77은 v2에서 MDD를 낮추는 데 유효했다.
- 그러나 ret20 <= -0.08로 충분한 하락 압력을 확인하면 close_pos 0.77 강화 없이도 더 좋은 결과가 가능하다.
- 단, v1 raw 조건의 close_pos >= 0.70은 유지되어야 한다.

### 6.3 ret20을 너무 강하게 조이면 수익이 줄어든다

- ret20 <= -0.08: cd 123.3285
- ret20 <= -0.10: cd 123.1130
- ret20 <= -0.12: cd 121.8847

해석:

- ret20 <= -0.08이 현재 가장 좋은 균형점이다.
- -0.10부터는 거래 수 감소와 수익률 손실이 커진다.
- -0.12는 너무 강하다.

### 6.4 RSI 상단 제한은 단독으로 약하다

- rsi14 <= 34: cd 122.3833
- rsi14 <= 32: cd 121.5531
- rsi14 <= 30: cd 120.6015

해석:

- rsi14 <= 34는 기준선을 아주 약하게 넘지만 개선폭이 작다.
- 더 강한 RSI 상한은 수익률을 크게 깎는다.
- RSI는 단독 핵심축이 아니라 보조 후보에 가깝다.

### 6.5 reclaim_atr 상한은 느슨해야 한다

- reclaim_atr <= 1.90: cd 122.3683
- reclaim_atr <= 1.75: cd 122.2895
- reclaim_atr <= 1.60: cd 119.7709

해석:

- reclaim_atr 상한은 너무 강하면 성능을 무너뜨린다.
- 1.90 수준은 기준선보다 약간 좋지만, 핵심 개선축은 아니다.
- ret20과 결합했을 때는 MDD 방어에 효과가 있다.

### 6.6 close_pos 0.90, upper_wick 0.12는 너무 강하다

`LM7_067`과 `LM7_066`은 승률은 높지만 거래 수와 수익률 손실이 커서 실패했다.

해석:

- v2 이후 마감 품질 조건을 더 강하게 조이는 것은 좋은 거래를 많이 제거한다.
- close_pos 강화와 upper wick 제한은 후순위로 둔다.

---

## 7. 현재 기준선 갱신 후보 분류

### 7.1 공격/균형형 1순위

- `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- cd: 123.3883
- final_return_pct: 24.6575
- max_drawdown_pct: 1.0181
- trades: 469

장점:

- 전체 1위
- 수익과 MDD가 동시에 개선
- v2보다 거래 수는 줄지만 성과 개선폭이 충분함

주의:

- v2의 close_pos >= 0.77 추가 조건을 제거한 변형이다.
- 기준선 갱신 전에는 코드와 진입 조건을 명확히 기록해야 한다.

### 7.2 보수적 기준선 갱신 후보

- `LM7_010_V2_RET20_DEEP_PULLBACK_08`
- cd: 123.3285
- final_return_pct: 24.5580
- max_drawdown_pct: 0.9871
- trades: 456

장점:

- v2 조건을 그대로 유지하고 ret20 <= -0.08만 추가
- 구조 설명이 단순함
- MDD가 LM7_070보다 낮음

주의:

- 전체 1위는 아니다.
- 거래 수가 LM7_070보다 조금 더 적다.

### 7.3 방어형 후보

- `LM7_064_V2_RET20_08_RECLAIM175`
- cd: 123.2371
- final_return_pct: 24.1376
- max_drawdown_pct: 0.7254
- trades: 402

장점:

- MDD가 매우 낮다.
- 방어형 long_main 후보로 가치가 있다.

주의:

- 거래 수와 수익률이 줄었다.
- 공식 메인 기준선보다는 risk-reduced 후보로 따로 관리하는 편이 좋다.

---

## 8. 다음 v8 방향

다음 단계는 두 갈래 중 하나다.

### A안: 기준선 갱신 기록

v7 결과를 기준으로 long_main 기준선을 v3로 갱신할 수 있다.

후보:

- 1순위: `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- 보수적 후보: `LM7_010_V2_RET20_DEEP_PULLBACK_08`

A안을 택하면 `base_line/long_main/v3` 폴더를 만들고 다음을 기록한다.

- README.md
- 01_RESULT_SUMMARY.md
- 02_ENTRY_CONDITIONS.md
- 03_STRENGTHS_WEAKNESSES_AND_NEXT.md
- long_main_v3 strategy code

### B안: v7 최우수 후보 주변 구조형 추가 검증

기준선 갱신 전에 한 번 더 구조형 개선을 시도할 수도 있다.

추천 중심 후보:

- `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

추천 추가/변형 방향:

1. LM7_070 + reclaim_atr loose cap
   - 1.90 또는 1.75 계열

2. LM7_070 + shock_recency <= 3

3. LM7_070 + RSI14 <= 34
   - 이미 `LM7_071`에서 테스트되었고 cd 122.8013으로 LM7_070보다 낮았으므로 우선순위 낮음

4. LM7_070에서 body_atr <= 1.60 제거 여부 검증
   - 공격성이 더 커질 수 있으나 MDD 증가 가능성 있음

5. LM7_070에서 vol_ratio 1.45 유지 여부 검증
   - vol 조건 제거는 위험하므로 신중히 테스트

6. LM7_010 중심의 방어형 변형
   - ret20 <= -0.08 + reclaim_atr cap
   - ret20 <= -0.08 + shock_recency <= 3

---

## 9. 다음 개발에서 반복 금지할 방향

다음은 v7에서 실패했거나 후순위다.

- ret20 <= -0.12
- rsi14 <= 32 또는 30
- reclaim_atr <= 1.60
- close_pos >= 0.90
- upper_wick_ratio <= 0.12
- ret20 + rsi14 <= 32

기존 금지/후순위 조건도 유지한다.

- MFE/MAE 사용 금지
- range_atr <= 2.40 반복 금지
- body/range balance 반복 금지
- body_atr <= 1.45 반복 금지
- lower wick 단독 반복 금지
- real_break 단독 반복 금지
- reclaim_atr <= 1.10 같은 강한 제한 금지
- EMA/quiet/trend floor 계열 제외

---

## 10. 최종 판단

v7은 성공이다.

v6 진단에서 확인된 손실 구조인 “ret20이 덜 빠진 상태의 reclaim”을 실제 백테스트로 검증했고, `ret20 <= -0.08` 계열이 명확히 기준선을 개선했다.

현재 가장 강한 후보는 다음이다.

- `LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`

보수적 기준선 갱신 후보는 다음이다.

- `LM7_010_V2_RET20_DEEP_PULLBACK_08`

방어형 후보는 다음이다.

- `LM7_064_V2_RET20_08_RECLAIM175`

공식 기준선 갱신 여부는 다음 단계에서 결정한다.
