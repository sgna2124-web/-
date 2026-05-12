# long_max v5 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`

## 1. 장점

1. cd_value가 v4보다 크게 높다.

- v4: `363.5507495661`
- v5: `400.8314684802`
- 개선폭: `+37.2807189141`
- 개선율: 약 `+10.25%`

2. MDD가 오히려 낮아졌다.

- v4 MDD: `1.3412321126%`
- v5 MDD: `1.2432451599%`
- 변화: `-0.0979869527%p`

3. 기준 진입 조건을 유지했다.

- entry_key: `child::orig_V09_extreme_vol18::tp03`
- family/anchor/guard 구조는 유지
- 수정 지점은 rr_target 3.20 → 3.50

4. max_return이 크게 개선되었다.

- v4 max_return_pct: `268.4930973199`
- v5 max_return_pct: `305.8775211164`
- 변화: `+37.3844237965%p`

5. 단독 리테스트에서 재현됐다.

V16 탐색 결과의 1위가 V17 단독 리테스트에서 trades/wins/losses/cd_value까지 동일하게 재현되었다.

## 2. 단점

1. 승률은 낮아졌다.

- v4: `36.1202137913%`
- v5: `35.8569299553%`
- 변화: `-0.2632838360%p`

2. losses가 증가했다.

- v4 losses: `36453`
- v5 losses: `36584`
- 변화: `+131`

3. max_conc가 증가했다.

- v4 max_conc: `439`
- v5 max_conc: `441`
- 변화: `+2`

4. 거래 수는 여전히 많다.

- trades: `57035`

수수료, 슬리피지, 체결 지연 민감도는 계속 관리해야 한다.

## 3. 다음 개선 방향

long_max의 다음 목표는 `official_cd_value > 400.8314684802`이다.

우선순위:

1. cd_value 초과
2. ruined 방지
3. max_conc 441 이하 완화
4. 승률 하락 보완
5. MDD 급증 방지
6. 수수료 민감도 감소

추천 실험:

- rr_target 3.40 / 3.45 / 3.55 / 3.60 주변 재탐색
- atr_stop 1.06 / 1.08 / 1.12 / 1.14 조합
- max_hold 18 / 20 / 24 / 28 조합
- cooldown 24 / 35 / 42 조합
- baseline_entry AND 고변동 과열 회피
- baseline_entry AND max_conc 감소 필터

## 4. 갱신 후보 판정

다음 long_max 후보는 다음을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. official_cd_value > 400.8314684802
4. 단독 재백테스트에서 trades/wins/losses 및 cd_value 재현
