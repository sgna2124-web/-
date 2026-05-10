# long_main v2 장단점 및 다음 개발 방향

## 1. 전략 성격

`LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`는 v1 기준선 `6V2_L01_doubleflush_core`의 구조를 유지한 상태에서 진입 품질을 높인 균형형 long_main 기준선이다.

핵심은 다음 세 가지다.

1. 반전 캔들의 종가 위치를 더 강하게 본다.
2. reclaim에 거래량이 동반되었는지 확인한다.
3. 너무 과도한 장대 반전봉 추격은 느슨하게 제거한다.

---

## 2. 장점

### 2.1 기준선 구조를 훼손하지 않는다

v2는 완전히 새로운 전략이 아니다.

기존 기준선의 핵심 구조인 다음 조건을 그대로 유지한다.

```text
raw_l01_cap_reclaim
AND
double_flush_ok
```

따라서 v1 기준선의 철학인 “double flush 이후 cap reclaim을 먹는 롱 반전 전략”이 유지된다.

### 2.2 수익과 MDD가 동시에 개선되었다

v1 대비 v2는 다음이 모두 개선되었다.

- final_return_pct 상승
- max_return_pct 상승
- max_drawdown_pct 감소
- official_cd_value 상승
- win_rate_pct 상승

특히 MDD 개선이 크다.

- v1 MDD: 1.7279904306
- v2 MDD: 1.3005547461

### 2.3 거래 수가 과도하게 줄지 않았다

v1 거래 수는 592건이고 v2 거래 수는 557건이다.

거래 수 감소율은 약 5.91%다.

거래 수를 극단적으로 줄여서 MDD만 낮춘 후보가 아니라, 기준선의 핵심 거래 대부분을 유지하면서 품질 낮은 거래 일부를 제거한 구조다.

### 2.4 close_pos와 volume 조합이 검증되었다

v3에서 `close_pos >= 0.77` 단독도 기준선을 이겼고, `close_pos >= 0.77 + vol_ratio >= 1.45` 조합은 더 좋은 성과를 냈다.

v4에서는 여기에 `body_atr <= 1.60`을 붙인 후보가 최종 최우수가 되었다.

이는 v2 조건이 우연한 단일 필터가 아니라 단계적으로 검증된 조건 조합임을 의미한다.

### 2.5 loose chase guard가 효과적이었다

`body_atr <= 1.60`은 과도하게 큰 반전봉 일부만 제거한다.

강한 과열 방지 필터가 아니라 느슨한 추격 방지 필터다.

이 조건은 v3 attack anchor보다 MDD를 낮추면서 cd_value를 개선했다.

---

## 3. 단점

### 3.1 거래 수가 줄었다

v2는 v1보다 거래 수가 35건 줄었다.

- v1: 592건
- v2: 557건

거래 수가 과도하게 줄지는 않았지만, 일부 수익 거래도 제거되었을 가능성이 있다.

### 3.2 v3 공격형 anchor보다 final_return은 낮다

v3 공격형 anchor였던 `LM3_020_CP077_VOL145` 또는 v4의 `LM4_002_V3_ATTACK_ANCHOR_CP077_VOL145`는 final_return_pct가 24.1324였다.

v2 갱신 기준선인 `LM4_014`는 final_return_pct가 23.9515다.

즉, v2는 가장 공격적인 수익 후보는 아니다. 대신 MDD를 낮춰 cd_value를 더 높인 균형형 후보다.

### 3.3 body_atr upper guard는 민감하다

`body_atr <= 1.60`은 유효했지만, `body_atr <= 1.35`는 너무 강해서 실패했다.

따라서 다음 개발에서 body upper guard를 더 강하게 조이면 전략의 수익 구조가 훼손될 수 있다.

### 3.4 TP03은 실질 필터가 아닐 수 있다

개선안 규칙상 TP03을 유지하지만, 현재 atrp_min과 청산 파라미터 구조상 TP03은 대부분의 진입을 통과시킬 가능성이 크다.

따라서 TP03 자체가 v2 개선의 핵심 원인은 아니다.

---

## 4. v4에서 실패한 방향

다음 조건들은 long_main v2 이후 개발에서 우선순위를 낮춘다.

### 4.1 ret1 상한

ret1 상한은 수익 거래를 크게 제거했다.

롱 메인은 강한 반전봉에서 수익이 나오는 구조이므로 ret1 상한은 매우 조심해야 한다.

### 4.2 ATRP 상한

ATRP 상한은 롱 메인의 변동성 확장 수익 구조를 훼손했다.

롱 메인은 안정장보다 급락 후 반전 구간을 먹는다.

### 4.3 RSI 하한

RSI 하한 또는 waterfall guard는 급락 후 반전 전략의 핵심 구간을 제거했다.

### 4.4 EMA/quiet/trend floor

v2 이전 실험에서 EMA50 gap, EMA50 slope, trend floor, quiet ratio, ret20 floor 계열은 롱 메인과 맞지 않았다.

롱 메인은 안정 추세장 전략이 아니라 급락 후 reclaim 전략이다.

### 4.5 true double shock 강화

shock_count >= 2 계열은 너무 강했다.

기준선의 double flush 구조는 이미 충분한 선별력을 갖고 있다.

---

## 5. 다음 개발 방향

다음 개발은 v2 기준선을 기본으로 둔다.

기본 구조:

```text
raw_l01_cap_reclaim
AND double_flush_ok
AND close_pos >= 0.77
AND vol_ratio >= 1.45
AND body_atr <= 1.60
AND expected_tp >= 0.003
```

다음 개선안은 이 위에 구조형 조건을 추가하거나, 아주 제한적으로 변형한다.

### 5.1 추천 방향 A: 실제 저점 이탈 품질

목적:

- low가 이전 ll20을 실제로 의미 있게 찔렀는지 확인한다.

주의:

- 너무 강한 low break는 거래 수를 줄일 수 있다.
- 약한 조건으로만 시도한다.

### 5.2 추천 방향 B: loose lower wick confirmation

목적:

- 하방을 찔렀다가 회복한 흔적이 있는지 확인한다.

주의:

- wick 조건을 강하게 걸면 수익률이 감소했다.
- 1.45 이상 같은 강한 wick 조건은 피한다.

### 5.3 추천 방향 C: candle range/body balance

목적:

- body_atr <= 1.60과 유사하게 과도한 추격을 줄이되, 다른 방식으로 측정한다.

예시:

- candle_range_atr가 너무 큰 경우 제외
- body/range가 지나치게 1에 가까운 일방향 장대봉 제외

주의:

- 과열 방지 조건은 loose해야 한다.

### 5.4 추천 방향 D: shock 최근성 약한 확인

v4에서 shock_recent_6은 기준선을 이겼지만 최우수는 아니었다.

v2 기준선 위에 약한 shock 최근성 조건을 붙이는 것은 재검토할 가치가 있다.

주의:

- shock_count >= 2 같은 반복 강화는 피한다.

### 5.5 추천 방향 E: 방어형 후보 분리 관리

공격/균형형 기준선은 v2로 갱신한다.

방어형 후보는 별도로 관리한다.

현재 방어형 후보:

- `LM4_003_V3_DEFENSE_ANCHOR_CP080_VOL145`
- MDD: 1.1432
- cd: 121.9325

방어형 후보는 공식 long_main 기준선과 별도로 “risk-reduced long_main” 후보로 관리할 수 있다.

---

## 6. 다음 개발 금지 또는 후순위 조건

다음은 우선 제외한다.

- 기준선 진입 구조를 proxy로 새로 만드는 것
- `raw_l01_cap_reclaim + double_flush_ok`를 제거하는 것
- ret1 상한
- ATRP 상한
- RSI 하한
- EMA50 gap
- EMA50 slope
- trend floor
- quiet ratio
- ret20 floor
- shock_count >= 2
- body_atr <= 1.35 같은 강한 body upper guard
- wick 1.45 이상 같은 강한 wick 강화

---

## 7. 다음 개발 파일 필수 검증

다음 long_main 개발 파일은 반드시 v2 exact 후보를 포함해야 한다.

예시 이름:

- `LM5_000_LONG_MAIN_V2_EXACT_EMBEDDED`

이 후보는 다음 값을 재현해야 한다.

- trades: 557
- final_return_pct: 약 23.9515
- max_return_pct: 약 24.1477
- max_drawdown_pct: 약 1.3006
- official_cd_value: 약 122.3394

이 값이 맞지 않으면 개선안 평가로 넘어가면 안 된다.

---

## 8. 최종 판단

`LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`는 long_main 공식 기준선으로 채택할 가치가 있다.

이유:

- v1 기준선의 구조를 보존했다.
- 기준선 기반 추가 조건만 사용했다.
- 수익률과 MDD가 동시에 개선되었다.
- 거래 수 감소가 과도하지 않다.
- v3, v4 두 단계에 걸쳐 조건 조합이 검증되었다.

따라서 다음 개발은 v2를 기준선으로 한다.
