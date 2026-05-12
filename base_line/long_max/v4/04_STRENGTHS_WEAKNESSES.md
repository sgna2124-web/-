# long_max v4 장단점

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`

## 1. 장점

1. cd_value가 v3보다 크게 높다.

- v3: `336.7657621418`
- v4: `363.5507495661`
- 개선폭: `+26.7849874243`
- 개선율: 약 `+7.9536%`

2. MDD 증가가 거의 없다.

- v3 MDD: `1.3408670828%`
- v4 MDD: `1.3412321126%`
- 변화: `+0.0003650298%p`

3. 기준 진입 조건을 유지했다.

- entry_key: `child::orig_V09_extreme_vol18::tp03`
- family/anchor/guard 구조는 유지
- 수정 지점은 rr_target 2.90 → 3.20

따라서 다음 개선에서 진입 조건을 기준으로 추가/변형/제거 실험을 이어가기 쉽다.

4. max_return이 크게 개선되었다.

- v3 max_return_pct: `241.3427142366`
- v4 max_return_pct: `268.4930973199`
- 변화: `+27.1503830833%p`

5. 단독 리테스트에서 재현됐다.

V14 탐색 결과의 1위가 V15 단독 리테스트에서 trades/wins/losses/cd_value까지 동일하게 재현되었다.

## 2. 단점

1. 승률은 낮아졌다.

- v3: `36.6127394334%`
- v4: `36.1202137913%`
- 변화: `-0.4925256421%p`

rr_target을 높인 만큼 target 도달 비율은 낮아졌다.

2. losses가 증가했다.

- v3 losses: `36203`
- v4 losses: `36453`
- 변화: `+250`

3. max_conc가 증가했다.

- v3 max_conc: `435`
- v4 max_conc: `439`
- 변화: `+4`

long_max는 cd_value 중심이라 갱신 가능하지만, 실거래 부담 측면에서는 max_conc 감소 개선이 필요하다.

4. 거래 수는 여전히 많다.

- trades: `57065`

수수료, 슬리피지, 체결 지연 민감도는 계속 관리해야 한다.

## 3. 다음 개선 방향

long_max의 다음 목표는 `official_cd_value > 363.5507495661`이다.

우선순위:

1. cd_value 초과
2. ruined 방지
3. max_conc 439 이하 완화
4. 승률 하락 보완
5. MDD 급증 방지
6. 수수료 민감도 감소

추천 실험:

- rr_target 3.10 / 3.25 / 3.30 / 3.40 주변 재탐색
- atr_stop 1.06 / 1.08 / 1.12 / 1.14 조합
- max_hold 18 / 24 / 28 조합
- cooldown 24 / 35 / 42 조합
- baseline_entry AND 고변동 과열 회피
- baseline_entry AND max_conc 감소 필터
- baseline_entry OR parent 근접 신호, 단 ruined와 MDD 감시

## 4. 갱신 후보 판정

다음 long_max 후보는 다음을 모두 만족해야 한다.

1. errors == 0
2. ruined == false
3. official_cd_value > 363.5507495661
4. 단독 재백테스트에서 trades/wins/losses 및 cd_value 재현
