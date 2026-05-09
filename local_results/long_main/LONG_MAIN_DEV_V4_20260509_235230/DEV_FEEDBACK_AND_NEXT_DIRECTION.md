# LONG_MAIN_DEV_V4 피드백 및 다음 개발 방향

## 1. 문서 목적

이 문서는 `LONG_MAIN_DEV_V4_20260509_235230` 결과 폴더 안에서 v4 롱 메인 개발 결과의 장점, 단점, 보완점, 다음 개발 방향을 기록하기 위한 문서다.

v4의 목적은 미세 파라미터 조정이 아니라, 기준선 전략과 v3 우수 후보를 기반으로 구조형 추가 조건을 붙여보는 것이었다.

결론은 다음과 같다.

- 기준선 복원: 성공
- v3 공격형 anchor 재현: 성공
- v3 anchor를 넘는 신규 후보 발굴: 성공
- 최우수 후보: `LM4_014_ATTACK_BODY_NOT_HUGE`
- 다음 방향: v3 attack anchor 위에 과도한 반전봉만 제거하는 loose chase guard 계열을 중심으로 추가 개발

---

## 2. 기준선 복원 확인

기준선 감사 후보:

- `LM4_000_BASELINE_EXACT_EMBEDDED`

결과:

- trades: 592
- wins: 346
- losses: 246
- win_rate_pct: 58.4459459459
- final_return_pct: 23.8426079030
- max_return_pct: 24.0623399724
- max_drawdown_pct: 1.7279904306
- official_cd_value: 121.7026194894
- verdict: baseline_win

판정:

- 기준선 복원은 정상이다.
- v4 개선안 결과를 해석해도 된다.

---

## 3. v4 최우수 후보

### LM4_014_ATTACK_BODY_NOT_HUGE

조건:

- 기준선 진입 조건 통과
- close_pos >= 0.77
- vol_ratio >= 1.45
- body_atr <= 1.60
- TP03 적용

결과:

- trades: 557
- trade_ratio_vs_ref: 0.9408783784
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- pf: 3.8956015265
- verdict: baseline_win

기준선 대비:

- trades: 592 → 557
- win_rate_pct: 58.4459% → 59.7846%
- final_return_pct: 23.8426% → 23.9515%
- max_return_pct: 24.0623% → 24.1477%
- max_drawdown_pct: 1.7280% → 1.3006%
- official_cd_value: 121.7026 → 122.3394

v3 공격형 anchor 대비:

- `LM4_002_V3_ATTACK_ANCHOR_CP077_VOL145` cd: 122.2930
- `LM4_014_ATTACK_BODY_NOT_HUGE` cd: 122.3394

판정:

- v4 최우수 후보
- v3 공격형 anchor보다 cd_value가 높다.
- 수익률은 v3 anchor보다 약간 낮지만 MDD가 크게 낮아졌다.
- loose overextension guard, 즉 과도하게 큰 반전봉만 제거하는 방향은 유효하다.

---

## 4. v3 anchor 재현

### LM4_002_V3_ATTACK_ANCHOR_CP077_VOL145

결과:

- trades: 568
- wins: 340
- losses: 228
- win_rate_pct: 59.8591549296
- final_return_pct: 24.1323630760
- max_return_pct: 24.3289178035
- max_drawdown_pct: 1.4817728785
- official_cd_value: 122.2930033864
- verdict: baseline_win

판정:

- v3 최우수 후보가 v4에서도 그대로 재현됐다.
- 공격형 anchor로 계속 사용할 수 있다.

---

## 5. 기준선을 이긴 주요 후보

### 5.1 LM4_014_ATTACK_BODY_NOT_HUGE

- cd: 122.3394
- MDD: 1.3006
- final_return_pct: 23.9515
- 최우수 후보

### 5.2 LM4_002_V3_ATTACK_ANCHOR_CP077_VOL145

- cd: 122.2930
- MDD: 1.4818
- final_return_pct: 24.1324
- 공격형 anchor

### 5.3 LM4_010_ATTACK_NO_UPPER_REJECT_060

- 결과가 LM4_002와 동일
- upper_wick_ratio <= 0.60은 이번 기준선/v3 anchor 진입군에서 실질 필터로 작동하지 않았다.

### 5.4 LM4_011_ATTACK_NO_UPPER_REJECT_055

- 결과가 LM4_002와 동일
- upper_wick_ratio <= 0.55도 실질 필터로 작동하지 않았다.

### 5.5 LM4_024_ATTACK_RECLAIM_COMMITTED

- 결과가 LM4_002와 동일
- reclaim extension >= 0.20 ATR도 실질 필터로 작동하지 않았다.

### 5.6 LM4_030_ATTACK_SHOCK_RECENT_6

- trades: 556
- final_return_pct: 24.0750
- max_return_pct: 24.2715
- MDD: 1.5916
- cd: 122.1002

해석:

- 기준선은 이겼지만 v3 anchor와 LM4_014에는 못 미친다.
- shock recent 6은 유효하지만 최우선 후보는 아니다.

### 5.7 LM4_061_ATTACK_QUALITY_BALANCED_B

- trades: 549
- final_return_pct: 23.7202
- MDD: 1.3784
- cd: 122.0149

해석:

- MDD 방어형 후보로 의미는 있지만 LM4_014보다 열위다.

### 5.8 LM4_003_V3_DEFENSE_ANCHOR_CP080_VOL145

- trades: 542
- final_return_pct: 23.3425
- MDD: 1.1432
- cd: 121.9325

해석:

- 여전히 방어형 후보로 가치가 있다.
- 다만 공격형/균형형 최우수는 LM4_014다.

---

## 6. v4의 핵심 발견

### 6.1 body_atr <= 1.60은 유효했다

`LM4_014_ATTACK_BODY_NOT_HUGE`가 최우수 후보가 되었다.

해석:

- 기준선 + cp 0.77 + vol 1.45 구조는 유지한다.
- 여기에 body_atr <= 1.60을 붙이면 너무 과도하게 튄 반전봉 일부가 제거된다.
- 수익률은 v3 anchor보다 조금 낮아지지만 MDD가 크게 낮아져 cd_value가 상승한다.

중요:

- body_atr <= 1.35는 너무 강했다.
- `LM4_013_ATTACK_BODY_NOT_EXTREME`은 cd 121.1305로 실패했다.
- 따라서 body upper guard는 너무 강하게 걸면 안 된다.
- 현재 유효한 건 loose guard인 body_atr <= 1.60이다.

### 6.2 upper wick reject guard는 효과가 없었다

`LM4_010`과 `LM4_011`은 v3 anchor와 완전히 동일했다.

해석:

- 기준선 + cp 0.77 + vol 1.45를 통과한 거래들은 이미 upper wick 문제가 거의 없는 것으로 보인다.
- upper_wick_ratio 0.55~0.60 수준은 실질 필터가 아니다.
- 다음 개발에서는 이 조건을 반복할 필요가 낮다.

### 6.3 reclaim committed 조건도 효과가 없었다

`LM4_024_ATTACK_RECLAIM_COMMITTED`는 v3 anchor와 동일했다.

해석:

- 기준선 + cp 0.77 + vol 1.45 거래들은 이미 reclaim extension >= 0.20 ATR 조건을 대부분 만족하는 것으로 보인다.
- 이 강도에서는 반복할 필요가 없다.

### 6.4 ret1 chase guard는 성능을 크게 훼손했다

`LM4_012_ATTACK_NO_RET1_CHASE`

- trades: 505
- final_return_pct: 13.8172
- MDD: 1.1104
- cd: 112.5534

해석:

- ret1 <= 5.5%는 롱 메인 전략의 큰 수익 거래를 대거 제거했다.
- 롱 메인은 강한 반전봉 추격 성격이 일부 포함되어 있으므로 ret1 상한은 매우 조심해야 한다.
- 다음 개발에서 ret1 상한은 우선 제외한다.

### 6.5 ATRP 상한/risk guard는 실패했다

`LM4_040_ATRP_RISK_GUARD_065`, `LM4_041_ATRP_RISK_GUARD_055`는 모두 실패했다.

해석:

- 롱 메인 전략은 변동성 확장 구간에서 수익을 만든다.
- atrp 상한을 걸면 좋은 거래를 많이 제거한다.
- 다음 개발에서 ATRP 상한은 우선 제외한다.

### 6.6 RSI waterfall guard는 실패했다

`LM4_043`, `LM4_044`는 모두 성능이 크게 낮다.

해석:

- RSI 하한을 걸면 급락 후 반전 전략의 핵심 구간이 제거된다.
- 롱 메인에는 RSI 안정장 필터가 맞지 않는다.

### 6.7 true double shock 조건은 너무 강했다

`LM4_032`, `LM4_033`은 trade 수가 260개 수준으로 줄고 수익률도 크게 낮아졌다.

해석:

- shock count >= 2는 너무 강하다.
- 기준선의 double flush 구조는 이미 충분히 선별력이 있다.
- shock recency는 약하게 쓸 수 있지만 count 강화는 우선 제외한다.

---

## 7. 다음 v5 개발 방향

v5도 미세 파라미터 조정이 아니라 기준선 기반 개선안 개발로 가야 한다.

중심 후보:

- `LM4_014_ATTACK_BODY_NOT_HUGE`

핵심 구조:

- 기준선 진입 조건
- close_pos >= 0.77
- vol_ratio >= 1.45
- body_atr <= 1.60

### 7.1 1순위: LM4_014 기반 구조형 보완

추천 방향:

- LM4_014 + shock_recent_6
- LM4_014 + real_break_min 0.05 ATR
- LM4_014 + loose lower wick confirmation
- LM4_014 + avoid same-symbol over-clustering proxy
- LM4_014 + candle body balance condition

주의:

- body_atr <= 1.35처럼 강한 조건은 피한다.
- ret1 상한은 피한다.
- ATRP 상한은 피한다.
- RSI 하한은 피한다.

### 7.2 2순위: 과도한 반전봉 제거 조건의 대체안

LM4_014가 성공한 이유는 과도하게 큰 반전봉을 느슨하게 제거했기 때문으로 보인다.

다음에는 body_atr 이외의 방식으로 같은 목적을 테스트할 수 있다.

추천:

- range20 대비 현재 candle range가 과도한 경우 제거
- body/range 비율이 너무 큰 일방향 장대양봉 제거
- close_to_high는 유지하되, candle_range_atr가 너무 큰 경우 제거
- ret3 급반등 과열 제거는 아주 약하게만 시도

### 7.3 3순위: 방어형 후보 별도 관리

방어형 후보:

- `LM4_003_V3_DEFENSE_ANCHOR_CP080_VOL145`
- `LM4_050_DEFENSE_NO_UPPER_REJECT_060`
- `LM4_053_DEFENSE_SHOCK_RECENT_6`

현재 가장 좋은 방어형은 여전히 `LM4_003`이다.

- MDD: 1.1432
- cd: 121.9325

v5에서는 공격형 후보와 방어형 후보를 분리해서 관리하는 것이 좋다.

---

## 8. 다음 파일 작성 규칙

다음 파일은 `run_long_main_dev_v5.py` 형태가 적합하다.

필수 규칙:

1. `LM5_000_BASELINE_EXACT_EMBEDDED`를 반드시 포함한다.
2. 기준선 exact 후보가 trades 592, max_return 약 24.0623, MDD 약 1.728, cd 약 121.7026을 재현해야 한다.
3. `LM5_001` 또는 `LM5_002`에 v4 최우수 후보 `LM4_014_ATTACK_BODY_NOT_HUGE`를 anchor로 포함한다.
4. 미세 파라미터 조정은 하지 않는다.
5. 기준선 기반 구조형 개선안만 만든다.
6. ret1 상한, ATRP 상한, RSI 하한, EMA/quiet/trend floor는 제외한다.
7. body upper guard는 loose하게만 사용한다. body_atr <= 1.60은 유효했지만 <= 1.35는 너무 강했다.
8. 결과는 현재 파이썬 파일 실행 위치 기준으로 저장한다.
9. 결과 폴더 안에 새 피드백 문서를 추가한다.

---

## 9. 최종 판정

v4는 성공이다.

v3 최우수 후보였던 `cp 0.77 + vol 1.45`를 재현했고, 그 위에 `body_atr <= 1.60`이라는 loose chase guard를 붙인 `LM4_014_ATTACK_BODY_NOT_HUGE`가 더 높은 cd_value를 기록했다.

최종 우선순위:

1. 공격/균형형 최우수
   - `LM4_014_ATTACK_BODY_NOT_HUGE`
   - cd: 122.3394
   - MDD: 1.3006
   - final_return_pct: 23.9515

2. 공격형 수익 우선 anchor
   - `LM4_002_V3_ATTACK_ANCHOR_CP077_VOL145`
   - cd: 122.2930
   - MDD: 1.4818
   - final_return_pct: 24.1324

3. 방어형 후보
   - `LM4_003_V3_DEFENSE_ANCHOR_CP080_VOL145`
   - cd: 121.9325
   - MDD: 1.1432

다음 v5는 LM4_014를 중심으로 구조형 보완 조건을 추가하는 방향이 가장 합리적이다.
