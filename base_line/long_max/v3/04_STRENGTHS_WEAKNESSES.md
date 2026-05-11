# long_max v3 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`

## 1. 장점

1. cd_value가 v2보다 높다.

- v2: `311.3750675807`
- v3: `336.7657621418`
- 개선폭: `+25.3906945610`
- 개선율: 약 `+8.1544%`

2. long_max 기준에 정확히 맞는다.

long_max는 MDD 제한 없이 cd_value 최대를 기준으로 한다. v3은 v2보다 높은 cd_value를 기록했으므로 기준선 갱신 대상이다.

3. 진입 조건을 바꾸지 않은 직접 개선이다.

- entry_key는 v2와 동일하다.
- 개선 포인트는 atr_stop 1.01 → 1.10이다.
- 따라서 다음 개선도 같은 진입 조건에서 청산/필터를 조정하기 쉽다.

4. 승률과 손익 구조가 개선되었다.

- wins: `20312 → 20911`, +599
- losses: `36931 → 36203`, -728
- win_rate_pct: `35.4838 → 36.6127`, +1.1289%p

5. final_return과 max_return이 모두 개선되었다.

- final_return_pct: `214.7144 → 240.7308`
- max_return_pct: `215.2271 → 241.3427`

## 2. 단점

1. MDD가 소폭 증가했다.

- v2: `1.2219870757%`
- v3: `1.3408670828%`
- 변화: `+0.1188800071%p`

long_max는 MDD 제한이 없지만, MDD 악화가 cd_value를 훼손할 수 있으므로 계속 감시해야 한다.

2. max_conc가 증가했다.

- v2: `429`
- v3: `435`
- 변화: `+6`

실거래에서는 동시 포지션 부담을 더 확인해야 한다.

3. 거래 수가 여전히 매우 많다.

- trades: `57114`

초고빈도 누적형 전략이므로 수수료, 슬리피지, 체결 지연 민감도가 있다.

4. 승률은 아직 낮은 편이다.

- win_rate_pct: `36.6127394334%`

높은 손익비와 누적 구조로 성과를 내지만, 연속 손실 구간 관리가 필요하다.

## 3. 다음 개선 방향

long_max의 다음 개선은 cd_value 극대화가 핵심이다.

우선순위:

1. cd_value 336.7657621418 초과
2. ruined 방지
3. MDD 과도 상승 방지
4. max_conc 435 이하로 완화
5. 수수료 민감도 감소
6. 거래 수 증가가 실제 성과 개선으로 이어지는지 확인

추천 실험:

- `baseline_entry AND volatility_overheat_avoid`
- `baseline_entry OR near_parent_entry`
- `TP03 0.25 / 0.35 / 0.40`
- `atr_stop 1.06 / 1.14 / 1.18`
- `rr_target 2.80 / 3.00 / 3.10`
- `max_hold 18 / 24 / 28`
- `cooldown 24 / 35 / 42`

## 4. 갱신 후보 판정

다음 long_max 후보는 다음을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. official_cd_value > 336.7657621418
4. 단독 재현에서 trades/wins/losses 및 cd_value가 다시 확인될 것
