# long_main v5 장단점 및 다음 개발 방향

## 1. 전략 성격

`LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`은 v4 기준선의 구조를 유지하면서 shock freshness 조건을 추가한 방어형 long_main 기준선이다.

핵심은 다음이다.

1. `raw_l01_cap_reclaim + double_flush_ok` 원형 구조를 유지한다.
2. `vol_ratio >= 1.45`로 거래량 동반 reclaim을 확인한다.
3. `ret20 <= -0.08`로 충분한 20봉 하락 압력을 확인한다.
4. `body_atr <= 2.20`으로 강한 반전봉을 허용하되 과도한 추격을 제한한다.
5. `shock_recency <= 3`으로 너무 오래된 shock 문맥의 reclaim을 제거한다.
6. v4와 동일하게 `close_pos >= 0.77` 추가 조건은 사용하지 않는다.

---

## 2. 장점

### 2.1 v4 대비 cd_value가 개선되었다

v5는 v4보다 official_cd_value가 소폭 개선되었다.

- v4 cd: 123.5780610685
- v5 cd: 123.6093482796

개선폭은 크지 않지만, 공식 계산 기준에서 기준선을 넘어섰다.

### 2.2 MDD가 1% 아래로 내려갔다

- v4 MDD: 1.0904624350
- v5 MDD: 0.9930660871

v4에서 소폭 증가했던 MDD를 다시 낮췄다.

### 2.3 승률과 PF가 개선되었다

- win_rate_pct: 64.7182 → 66.4430
- profit_factor: 4.5655 → 4.9303

손실 거래를 상대적으로 더 많이 제거한 결과다.

### 2.4 추가 조건의 논리가 명확하다

v5는 오래된 shock 이후 늦게 나온 reclaim을 제거한다.

즉, long_main의 기본 철학인 “급락 후 빠른 reclaim 반전”에 더 가깝게 만든다.

### 2.5 리소스 절약형 개발에서 도출되었다

v9 개발 코드는 다음 조건으로 실행되었다.

- workers=1
- variants=14
- 파일 단위 처리
- 4축 동시 백테스트 상황 고려

따라서 v5는 과부하 환경을 감안한 실무형 개발 흐름에서 나온 기준선이다.

---

## 3. 단점

### 3.1 수익률과 max_return은 v4보다 소폭 낮다

- final_return_pct: 24.9405 → 24.8493
- max_return_pct: 25.2064 → 25.0900

즉, v5는 수익성 극대화형이 아니라 방어형 cd 개선 기준선이다.

### 3.2 거래 수가 줄었다

- trades: 479 → 447

거래 수가 32건 감소했다. 다음 개발에서 추가 필터를 더 붙이면 거래 수가 과도하게 줄어들 수 있다.

### 3.3 개선폭이 매우 작다

- cd_value 개선폭: 약 +0.0313

갱신 가능하므로 기준선으로 채택하지만, 큰 구조적 도약이라기보다는 미세 방어형 개선에 가깝다.

### 3.4 shock_recency 조건은 너무 강하게 조이면 위험하다

현재 값은 `shock_recency <= 3`이다.

이를 2 이하로 조이면 거래 수가 더 줄고 수익률이 낮아질 수 있다.

반대로 4 이상으로 완화하면 v4와 가까워져 MDD 방어 효과가 약해질 수 있다.

---

## 4. v9에서 비교된 의미 있는 후보

### 4.1 v9 1위: LM9_012

`LM9_012_V4_SHOCK_RECENCY_3`

- shock_recency <= 3
- cd: 123.6093
- final_return_pct: 24.8493
- max_return_pct: 25.0900
- MDD: 0.9931
- win_rate_pct: 66.4430

선택 이유:

- v9 전체 1위
- v4 대비 cd_value 개선
- MDD, 승률, PF 개선

### 4.2 v4 exact

`LM9_000_LONG_MAIN_V4_EXACT_EMBEDDED`

- cd: 123.5781
- MDD: 1.0905

해석:

- v4는 수익성과 max_return이 약간 더 높다.
- v5는 더 방어적이고 cd_value가 약간 더 높다.

---

## 5. 다음 개발 방향

다음 개발은 v5 기준선을 기본으로 둔다.

기본 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 2.20
AND ret20 <= -0.08
AND shock_recency <= 3
AND expected_tp >= 0.003
```

### 5.1 추천 방향 A: v5의 수익률 회복

v5는 MDD와 승률은 좋아졌지만 수익률과 max_return은 v4보다 소폭 낮다.

다음 개발은 v5의 방어력을 유지하면서 수익률을 회복하는 방향이 좋다.

가능 후보:

- shock_recency <= 3 유지 + body_atr 상한 구조 재확인
- shock_recency <= 3 유지 + reclaim_atr loose cap 결합
- shock_recency <= 3 유지 + volume 조건 변형

### 5.2 추천 방향 B: 리소스 절약형 후보 운영 유지

현재 컴퓨터에서 4축 동시 백테스트 시 CPU와 메모리 과부하가 발생한다.

따라서 다음 long_main 개발 파일도 기본값을 다음처럼 둔다.

- workers=1
- 후보 수 10~16개 수준
- `--cooldown-ms` 옵션 유지
- 결과 파일은 실행 위치 기준 저장
- 외부 절대경로 참조 금지

### 5.3 추천 방향 C: shock freshness 구조의 강도 확인

현재 기준은 `shock_recency <= 3`이다.

다음 개발에서 구조적으로 확인 가능한 후보:

- shock_recency <= 3 유지 + 다른 보조 조건 완화
- shock_recency <= 4 + 별도 방어 조건
- double_flush lookback 구조는 유지하되, shock freshness와 reclaim quality의 조합 확인

단순히 shock_recency를 1, 2, 3, 4, 5로 촘촘히 훑는 방식은 미세 파라미터 조정에 가깝기 때문에 우선순위가 낮다.

### 5.4 추천 방향 D: long_max와 분리 관리

v9 후보는 long_main 기준선은 소폭 갱신했지만 long_max 기준선은 넘지 못했다.

따라서 long_main 개발과 long_max 개발은 계속 분리해서 본다.

---

## 6. 다음 개발 금지 또는 후순위 조건

다음은 우선 제외한다.

- MFE/MAE 사용: 미래 정보라 금지
- ret20 <= -0.12
- rsi14 <= 32 또는 30
- reclaim_atr <= 1.60 이하의 강한 제한
- reclaim_atr <= 1.10
- close_pos >= 0.90
- upper_wick_ratio <= 0.12
- body_atr <= 1.45
- range_atr <= 2.40
- body/range balance
- lower wick 단독 강화
- real_break 단독 강화
- EMA50 gap
- EMA50 slope
- trend floor
- quiet ratio
- shock_count >= 2

---

## 7. 다음 개발 파일 필수 검증

다음 long_main 개발 파일은 반드시 v5 exact 후보를 포함해야 한다.

예시 이름:

- `LM10_000_LONG_MAIN_V5_EXACT_EMBEDDED`

이 후보는 다음 값을 재현해야 한다.

- trades: 447
- final_return_pct: 약 24.8493
- max_return_pct: 약 25.0900
- max_drawdown_pct: 약 0.9931
- official_cd_value: 약 123.6093

이 값이 맞지 않으면 개선안 평가로 넘어가면 안 된다.

---

## 8. 최종 판단

`LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`은 long_main 공식 기준선으로 채택한다.

이유:

- 현재 v9 전체 1위다.
- v4 대비 official_cd_value가 개선되었다.
- MDD, 승률, profit_factor가 개선되었다.
- 변경점이 shock_recency <= 3 추가로 명확하다.
- v4의 핵심 구조와 진입 철학을 유지한다.
- 리소스 절약형 개발 조건에서도 정상적으로 검증되었다.

따라서 다음 개발은 v5를 기준선으로 한다.
