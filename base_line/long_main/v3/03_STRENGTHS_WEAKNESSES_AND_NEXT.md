# long_main v3 장단점 및 다음 개발 방향

## 1. 전략 성격

`LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`은 v1의 double flush reclaim 구조를 유지하면서, v6 진단 결과로 확인된 손실 과대표현 구간을 제거한 진단 기반 long_main 기준선이다.

핵심은 다음이다.

1. `raw_l01_cap_reclaim + double_flush_ok` 원형 구조를 유지한다.
2. `vol_ratio >= 1.45`로 거래량 동반 reclaim을 확인한다.
3. `body_atr <= 1.60`으로 과도한 장대 반전봉 추격을 완화한다.
4. `ret20 <= -0.08`로 충분히 빠진 뒤 reclaim만 허용한다.
5. v2의 `close_pos >= 0.77` 추가 조건은 제거한다.

---

## 2. 장점

### 2.1 v2 대비 모든 핵심 지표가 개선되었다

v3는 v2 대비 다음이 모두 개선되었다.

- 승률 상승
- final_return_pct 상승
- max_return_pct 상승
- max_drawdown_pct 감소
- official_cd_value 상승
- profit_factor 상승

특히 승률은 59.7846%에서 64.6055%로 크게 상승했다.

### 2.2 손실 거래 제거 효율이 높다

v2 대비 거래 수는 88건 줄었다.

- wins: 333 → 303, 30건 감소
- losses: 224 → 166, 58건 감소

즉, 줄어든 거래 중 손실 거래의 비중이 더 높다. 이것은 `ret20 <= -0.08` 조건이 v6 진단에서 찾은 손실 과대표현 구간을 실제로 잘 제거했다는 의미다.

### 2.3 MDD가 1% 근처까지 낮아졌다

- v2 MDD: 1.3005547461
- v3 MDD: 1.0181358195

MDD가 1.0% 근처까지 내려갔다. 동시에 final_return과 max_return도 상승했기 때문에 단순 방어형 후보가 아니다.

### 2.4 v6 진단과 v7 검증이 연결되어 있다

v3는 무작위 필터가 아니다.

- v6: 손실 거래가 ret20이 덜 빠진 구간에 몰려 있음을 확인
- v7: ret20 <= -0.08을 실제 백테스트 후보로 검증
- v7 결과: LM7_070이 전체 1위

따라서 조건 추가의 논리적 근거가 강하다.

### 2.5 v1 원형 구조를 보존한다

v3는 `raw_l01_cap_reclaim + double_flush_ok`를 제거하지 않는다.

따라서 여전히 long_main의 본질은 “double flush 이후 cap reclaim 롱 반전”이다.

---

## 3. 단점

### 3.1 거래 수가 줄었다

v3는 v2보다 거래 수가 88건 줄었다.

- v2: 557건
- v3: 469건

현재 성과상 문제는 아니지만, 추가 필터를 더 붙이면 거래 수가 과도하게 줄어들 위험이 있다.

### 3.2 close_pos 0.77 제거는 설명상 주의가 필요하다

v3는 v2의 `close_pos >= 0.77` 추가 조건을 제거했다.

단, v1 raw 조건의 `close_pos > 0.70`은 유지된다.

다음 개발자가 이 차이를 혼동하면 기준선 복원 실패로 이어질 수 있다.

### 3.3 ret20 조건은 너무 강하게 조이면 안 된다

v7에서 다음이 확인되었다.

- ret20 <= -0.08: 우수
- ret20 <= -0.10: 성과 하락
- ret20 <= -0.12: 너무 강함

따라서 다음 개발에서 ret20을 더 강하게 조이는 방식은 우선순위가 낮다.

### 3.4 v3는 v2보다 더 선별적인 전략이다

v3는 더 좋은 성과를 냈지만, 거래 수가 줄어든 만큼 특정 시장 구간에서는 신호가 부족할 수 있다.

따라서 공격형 보조 후보나 방어형 후보를 별도로 관리할 수 있다.

---

## 4. v7에서 비교된 대안 후보

### 4.1 보수적 기준선 후보: LM7_010

`LM7_010_V2_RET20_DEEP_PULLBACK_08`

- v2 조건을 그대로 유지
- ret20 <= -0.08만 추가
- cd: 123.3285
- MDD: 0.9871
- final_return_pct: 24.5580

장점:

- 구조 설명이 더 보수적이다.
- MDD가 LM7_070보다 낮다.

선택하지 않은 이유:

- official_cd_value가 LM7_070보다 낮다.
- final_return과 max_return도 LM7_070보다 낮다.
- 현재 프로젝트 원칙상 갱신 가능하면 1위를 기준선으로 갱신한다.

### 4.2 방어형 후보: LM7_064

`LM7_064_V2_RET20_08_RECLAIM175`

- cd: 123.2371
- MDD: 0.7254
- final_return_pct: 24.1376

해석:

- 방어형 long_main 후보로 따로 관리할 가치가 있다.
- 공식 메인 기준선보다는 risk-reduced 후보로 적합하다.

---

## 5. 다음 개발 방향

다음 개발은 v3 기준선을 기본으로 둔다.

기본 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND vol_ratio >= 1.45
AND body_atr <= 1.60
AND ret20 <= -0.08
AND expected_tp >= 0.003
```

### 5.1 추천 방향 A: LM7_070 기반 reclaim_atr loose cap

목적:

- ret20 조건으로 충분한 하락 압력은 확인했으므로, 너무 멀리 회복한 종가 추격만 느슨하게 줄인다.

주의:

- reclaim_atr <= 1.10은 과거 실패했다.
- reclaim_atr <= 1.60도 v7에서 약했다.
- 1.75~1.90 수준의 loose cap만 검토한다.

### 5.2 추천 방향 B: shock_recency 보조 조건

목적:

- 너무 오래된 shock 기반 진입을 줄인다.

주의:

- shock recent 단독은 핵심축이 아니었다.
- v3 기준선 위에서 보조 조건으로만 검토한다.

### 5.3 추천 방향 C: body_atr <= 1.60 유지 여부 검증

목적:

- v3에서 body guard를 유지하고 있지만, ret20 조건이 들어간 뒤에도 body_atr <= 1.60이 필요한지 확인한다.

주의:

- 제거하면 수익은 증가할 수 있지만 MDD도 증가할 수 있다.
- 반드시 v3 exact와 함께 비교한다.

### 5.4 추천 방향 D: vol_ratio >= 1.45 유지 여부 검증

목적:

- ret20 조건이 들어간 뒤에도 volume 강화 조건이 필요한지 확인한다.

주의:

- vol 조건 제거는 품질 저하 위험이 있다.
- 단독 제거 후보와 보조 조건 결합 후보를 구분한다.

### 5.5 추천 방향 E: 방어형 후보 분리 관리

방어형 후보:

- `LM7_064_V2_RET20_08_RECLAIM175`

이 후보는 MDD가 0.7254로 매우 낮다.

공식 기준선과 별도로 risk-reduced long_main 후보로 기록할 가치가 있다.

---

## 6. 다음 개발 금지 또는 후순위 조건

다음은 우선 제외한다.

- MFE/MAE 사용: 미래 정보라 금지
- ret20 <= -0.12
- rsi14 <= 32 또는 30
- reclaim_atr <= 1.60 이하의 강한 제한
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

다음 long_main 개발 파일은 반드시 v3 exact 후보를 포함해야 한다.

예시 이름:

- `LM8_000_LONG_MAIN_V3_EXACT_EMBEDDED`

이 후보는 다음 값을 재현해야 한다.

- trades: 469
- final_return_pct: 약 24.6575
- max_return_pct: 약 24.9229
- max_drawdown_pct: 약 1.0181
- official_cd_value: 약 123.3883

이 값이 맞지 않으면 개선안 평가로 넘어가면 안 된다.

---

## 8. 최종 판단

`LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`은 long_main 공식 기준선으로 채택한다.

이유:

- 현재 v7 전체 1위다.
- v2 대비 모든 핵심 성과 지표가 개선되었다.
- 진단 기반 조건인 ret20 <= -0.08이 실제 백테스트에서 검증되었다.
- v1의 원형 구조를 보존한다.
- v2의 volume/body 품질 조건도 유지한다.

따라서 다음 개발은 v3를 기준선으로 한다.
