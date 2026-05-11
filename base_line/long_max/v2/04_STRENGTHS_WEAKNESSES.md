# long_max v2 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`

---

## 1. 핵심 장점

1. cd_value가 기존 long_max v1을 크게 초과한다.

- v1: 134.4697
- v2: 311.3750675807
- 개선폭: +176.9053675807

2. 단독 재현에 성공했다.

- V11 1위로 발견
- V12 단독 재백테스트에서 동일 결과 재현
- pass_basic_reproduction_gate = true

3. MDD가 v1보다 낮다.

- v1 MDD: 6.8270%
- v2 MDD: 1.2219870757%

4. max_return과 final_return이 높다.

- v2 final_return_pct: 214.7144460828
- v2 max_return_pct: 215.2271020267

5. long_max 기준에 정확히 맞는다.

long_max는 MDD 제한보다 cd_value 최대화를 우선한다. v2는 V12 단독 검증 기준 cd_value 311.3750675807을 기록했다.

---

## 2. 핵심 단점

1. 승률이 낮다.

- v2 win_rate_pct: 35.4838146149%

2. 거래 수가 많다.

- trades: 57243
- 수수료, 슬리피지, 체결 지연에 민감할 수 있다.

3. max_conc가 높다.

- max_conc: 429
- 실거래에서는 동시 포지션 관리가 중요하다.

4. 기존 v1의 희소 진입 성격과 다르다.

- v1은 V51 희소 진입형이었다.
- v2는 V09 고빈도 누적수익형이다.

5. 과최적화 가능성을 계속 감시해야 한다.

- V11에서 발견되고 V12 단독 재현은 성공했지만, 향후 수수료·슬리피지·기간 확장 검증이 필요하다.

---

## 3. long_max 개선 방향

long_max는 cd_value 극대화가 목적이다.

우선순위:

1. cd_value 상승
2. ruined 방지
3. MDD 과도 상승 방지
4. max_conc 감소
5. 수수료 민감도 감소
6. 거래 수 과다로 인한 실거래 부담 완화

추천 실험:

- TP03 게이트 강화: 0.3% → 0.35% / 0.4%
- TP03 게이트 완화: 0.3% → 0.25%, 단 cd_value 증가 여부 확인
- rr_target: 2.90 → 2.70 / 3.10 / 3.30
- atr_stop: 1.01 → 0.92 / 1.08 / 1.15
- max_hold_bars: 21 → 18 / 24 / 28
- cooldown_bars: 31 → 24 / 36 / 42
- child_entry AND high-risk-context 제거
- child_entry OR near-parent-entry, 단 기준선 이탈률 기록

---

## 4. long_max에서 주의할 점

long_max는 MDD 제한이 없지만, 기준선보다 cd_value가 낮으면 갱신하지 않는다.

다음 개선 결과 판단 순서:

1. errors == 0
2. ruined == false
3. cd_value > 311.3750675807
4. 가능하면 MDD가 크게 악화되지 않을 것
5. 가능하면 max_conc가 429보다 낮을 것

---

## 5. 최종 판정

v2는 기존 long_max v1보다 cd_value가 크게 높고, 단독 재현까지 통과했다.

앞으로 long_max의 기준선은 v2로 고정한다.
