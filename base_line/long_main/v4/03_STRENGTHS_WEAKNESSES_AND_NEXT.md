# long_main v4 장단점 및 다음 개발 방향

## 1. 전략 성격

`LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`은 v3 기준선의 구조를 유지하면서 body_atr 상한만 완화한 공격/균형형 long_main 기준선이다.

핵심은 다음이다.

1. `raw_l01_cap_reclaim + double_flush_ok` 원형 구조를 유지한다.
2. `vol_ratio >= 1.45`로 거래량 동반 reclaim을 확인한다.
3. `ret20 <= -0.08`로 충분한 20봉 하락 압력을 확인한다.
4. `body_atr <= 1.60`을 `body_atr <= 2.20`으로 완화한다.
5. v3와 동일하게 `close_pos >= 0.77` 추가 조건은 사용하지 않는다.

---

## 2. 장점

### 2.1 v3 대비 수익성과 cd_value가 개선되었다

v4는 v3보다 다음이 개선되었다.

- trades 증가
- wins 증가
- win_rate_pct 소폭 상승
- final_return_pct 상승
- max_return_pct 상승
- official_cd_value 상승

특히 max_return_pct가 24.9229에서 25.2064로 상승했다.

### 2.2 추가된 거래의 순효과가 긍정적이다

v4는 v3보다 거래가 10건 증가했다.

- wins: +7
- losses: +3

추가된 거래의 승패 구조가 나쁘지 않다. 따라서 body_atr 상한을 1.60으로 제한한 v3가 일부 좋은 강한 반전 거래를 막고 있었던 것으로 해석할 수 있다.

### 2.3 v3의 핵심 구조를 훼손하지 않는다

v4는 v3에서 성과를 만든 핵심 조건을 유지한다.

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND ret20 <= -0.08
```

변경점은 body_atr 상한 완화 하나뿐이다.

### 2.4 충분히 빠진 뒤 강한 반전봉을 더 허용한다

v3 이후 ret20 <= -0.08이 들어가면서 “충분히 빠진 상태”가 확인된다.

이 상태에서는 body_atr가 1.60을 넘는 강한 반전봉이 오히려 수익 기회가 될 수 있다.

v4는 이 거래를 body_atr <= 2.20까지 허용한다.

---

## 3. 단점

### 3.1 MDD가 소폭 증가했다

v3 대비 MDD는 증가했다.

- v3 MDD: 1.0181358195
- v4 MDD: 1.0904624350

증가폭은 크지 않지만, v4는 v3보다 약간 더 공격적인 기준선이다.

### 3.2 profit_factor는 소폭 낮아졌다

- v3 PF: 4.6238644584
- v4 PF: 4.5655373148

이는 추가로 허용된 거래가 수익성은 있지만, v3의 압축도보다는 약간 낮은 품질일 수 있음을 의미한다.

### 3.3 body_atr 상한을 더 완화하면 MDD가 커질 수 있다

v4는 body_atr <= 2.20을 사용한다.

이 상한을 더 느슨하게 하거나 제거하면 수익률은 더 올라갈 수 있지만, MDD도 함께 증가할 가능성이 있다.

따라서 다음 개발에서 body_atr 상한을 더 완화하려면 반드시 v4 exact와 비교해야 한다.

### 3.4 거래 수가 아직 479건이다

v4는 v3보다 거래 수가 늘었지만, v2의 557건보다는 적다.

추가 필터를 붙이면 거래 수가 다시 과도하게 줄어들 수 있다.

---

## 4. v8에서 비교된 의미 있는 후보

### 4.1 v8 1위: LM8_021

`LM8_021_LOOSER_BODY_GUARD_220`

- body_atr <= 2.20
- cd: 123.5781
- final_return_pct: 24.9405
- max_return_pct: 25.2064
- MDD: 1.0905

선택 이유:

- v8 전체 1위
- v3 대비 cd_value 개선
- 수익률과 max_return 개선
- MDD 증가폭 제한적

### 4.2 v3 exact

`LM8_000_LONG_MAIN_V3_EXACT_EMBEDDED`

- cd: 123.3883
- MDD: 1.0181

해석:

- v3는 더 압축된 균형형 기준선이다.
- v4는 v3보다 더 공격적으로 수익률을 끌어올린다.

---

## 5. 다음 개발 방향

다음 개발은 v4 기준선을 기본으로 둔다.

기본 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 2.20
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

### 5.1 추천 방향 A: body_atr 상한 주변 구조 확인

목적:

- 2.20이 정말 최적 근처인지 확인한다.

가능한 구조형 후보:

- body_atr 상한 유지 + 방어 조건 추가
- body_atr 상한 완화 + reclaim_atr cap 결합
- body_atr 상한 완화 + shock_recency 결합

주의:

- 단순 미세 파라미터 조정으로 2.05, 2.10, 2.15 등을 촘촘히 훑는 방식은 우선순위가 낮다.
- 구조형 조합을 우선한다.

### 5.2 추천 방향 B: MDD 방어 보조 조건

v4는 v3보다 MDD가 소폭 증가했다.

따라서 다음 개선은 v4의 수익률을 유지하면서 MDD를 낮추는 방향이 좋다.

후보:

- reclaim_atr loose cap
- shock_recency <= 3 또는 <= 4
- close quality 보조 조건 약하게 재검토

주의:

- reclaim_atr <= 1.10 같은 강한 제한은 금지한다.
- close_pos >= 0.90, upper_wick_ratio <= 0.12 같은 강한 마감 품질 조건은 과거 실패했다.

### 5.3 추천 방향 C: volume 조건 유지 여부 검증

v4에서 ret20과 body_atr 완화가 들어갔으므로, vol_ratio >= 1.45가 여전히 필요한지 재확인할 수 있다.

주의:

- 거래량 필터는 reclaim 품질 확인에 중요했다.
- 제거 후보는 반드시 v4 exact와 함께 비교해야 한다.

### 5.4 추천 방향 D: 방어형 후보 따로 관리

v7의 방어형 후보였던 `LM7_064_V2_RET20_08_RECLAIM175`는 여전히 참고 가치가 있다.

다만 공식 기준선은 cd_value가 더 높은 v4를 사용한다.

방어형 후보는 별도의 risk-reduced long_main 후보로 관리한다.

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

다음 long_main 개발 파일은 반드시 v4 exact 후보를 포함해야 한다.

예시 이름:

- `LM9_000_LONG_MAIN_V4_EXACT_EMBEDDED`

이 후보는 다음 값을 재현해야 한다.

- trades: 479
- final_return_pct: 약 24.9405
- max_return_pct: 약 25.2064
- max_drawdown_pct: 약 1.0905
- official_cd_value: 약 123.5781

이 값이 맞지 않으면 개선안 평가로 넘어가면 안 된다.

---

## 8. 최종 판단

`LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`은 long_main 공식 기준선으로 채택한다.

이유:

- 현재 v8 전체 1위다.
- v3 대비 수익률과 max_return이 개선되었다.
- official_cd_value가 상승했다.
- 변경점이 body_atr 상한 완화 하나로 명확하다.
- v3의 핵심 구조와 진입 철학을 유지한다.

따라서 다음 개발은 v4를 기준선으로 한다.
