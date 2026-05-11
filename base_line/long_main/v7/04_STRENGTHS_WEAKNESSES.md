# long_main v7 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`

## 1. 장점

1. cd_value가 v6보다 높다.

- v6: `311.3750675807`
- v7: `336.7657621418`
- 개선폭: `+25.3906945610`
- 개선율: 약 `+8.1544%`

2. long_main 기준을 통과한다.

- long_main 조건: `MDD < 5`
- v7 MDD: `1.3408670828%`

3. 진입 조건을 바꾸지 않은 직접 개선이다.

- entry_key는 v6와 동일하다.
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

- v6: `1.2219870757%`
- v7: `1.3408670828%`
- 변화: `+0.1188800071%p`

long_main 기준인 5% 미만에는 여유가 있지만, 다음 개선에서 MDD가 계속 증가하면 방어성이 약해질 수 있다.

2. max_conc가 증가했다.

- v6: `429`
- v7: `435`
- 변화: `+6`

실거래에서는 동시 포지션 부담을 더 확인해야 한다.

3. 거래 수가 여전히 매우 많다.

- trades: `57114`

초고빈도 누적형 전략이므로 수수료, 슬리피지, 체결 지연 민감도가 있다.

4. 승률은 아직 낮은 편이다.

- win_rate_pct: `36.6127394334%`

높은 손익비와 누적 구조로 성과를 내지만, 심리적/운영상 연속 손실 관리가 필요하다.

## 3. 다음 개선 방향

long_main의 다음 개선은 `MDD < 5`를 반드시 유지해야 한다.

우선순위:

1. cd_value 336.7657621418 초과
2. MDD 5% 미만 유지
3. max_conc 435 이하로 완화
4. 수수료 민감도 감소
5. 승률 개선
6. 거래 수 과다 문제 완화

추천 실험:

- `baseline_entry AND volatility_overheat_avoid`
- `baseline_entry AND recent_loss_cluster_avoid`
- `baseline_entry AND max_conc_proxy_filter`
- `atr_stop 1.06 / 1.14 / 1.18`
- `rr_target 2.80 / 3.00 / 3.10`
- `max_hold 18 / 24`
- `cooldown 35 / 40`

## 4. 갱신 후보 판정

다음 long_main 후보는 다음을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. max_drawdown_pct < 5
4. official_cd_value > 336.7657621418
5. 단독 재현에서 trades/wins/losses 및 cd_value가 다시 확인될 것
