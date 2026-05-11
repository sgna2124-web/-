# long_main v6 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`

---

## 1. 핵심 장점

1. cd_value가 매우 높다.

- v5: 123.6093482796
- v6: 311.3750675807
- 개선폭: +187.7657193011

2. long_main 기준인 MDD 5% 미만을 충족한다.

- v6 MDD: 1.2219870757%
- 허용 기준: 5% 미만

3. 단독 재현에 성공했다.

- V11 1위로 발견
- V12 단독 재백테스트에서 trades, wins, losses가 완전 일치
- pass_basic_reproduction_gate = true

4. 누적 수익률이 기존 long_main v5를 크게 초과한다.

- v5 max_return_pct: 25.0899569668
- v6 max_return_pct: 215.2271020267

5. 거래 수가 많아 표본이 풍부하다.

- v5 trades: 447
- v6 trades: 57243

---

## 2. 핵심 단점

1. 승률이 낮다.

- v5 승률: 66.4429530201%
- v6 승률: 35.4838146149%

2. 거래 수가 매우 많다.

- 수수료 민감도가 커질 수 있다.
- 실거래에서는 체결 품질, 슬리피지, API 지연 영향을 더 받을 수 있다.

3. max_conc가 높다.

- v6 max_conc: 429
- 동시 포지션 부담이 크다.

4. 기존 long_main 계보와 성격이 다르다.

- v5는 고승률·저빈도·방어형이다.
- v6는 저승률·초고빈도·누적수익형이다.

5. 다음 개선 시 기준선 정체성이 흐려지기 쉽다.

- V09/extreme/vol18/TP03 구조를 유지해야 한다.
- 완전히 다른 family/anchor/guard로 바꾸면 v6 개선이 아니라 신규 전략이다.

---

## 3. long_main 개선 방향

long_main에서는 MDD 5% 미만을 유지해야 한다.

우선순위:

1. cd_value 상승
2. MDD 5% 미만 유지
3. max_conc 감소
4. 수수료 민감도 감소
5. 승률 개선
6. 거래 수 과다 문제 완화

추천 실험:

- `child_entry AND volatility_not_hot`
- `child_entry AND spread_like_risk_low`
- `child_entry AND recent_loss_cluster_avoid`
- `child_entry AND max_conc_proxy_filter`
- `child_entry` 유지 + cooldown 31 → 35/40
- `child_entry` 유지 + max_hold 21 → 18/24
- `child_entry` 유지 + rr_target 2.90 → 2.70/3.10

---

## 4. long_main에서 주의할 점

long_main은 방어 기준이 있으므로, cd_value가 높아도 MDD 5% 이상이면 기준선 후보로 인정하지 않는다.

다음 개선 결과를 볼 때는 반드시 다음 순서로 판단한다.

1. errors == 0
2. ruined == false
3. MDD < 5
4. cd_value > 311.3750675807
5. 가능하면 max_conc가 429보다 낮을 것

---

## 5. 최종 판정

v6는 기존 long_main v5와 계보는 다르지만, long_main 공식 기준을 압도적으로 충족한다.

앞으로 long_main의 기준선은 v6로 고정한다.
