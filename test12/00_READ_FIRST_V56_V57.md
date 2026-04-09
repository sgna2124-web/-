TEST12 즉시 인수인계 문서

이번 단계에서 실제로 추가한 것
- v56 숏 전용 hybrid 러너 추가
- v57 롱 전용 hybrid 러너 추가
- v56/v57 base_config 추가
- v56/v57 combinations 추가
- v56/v57 summarize wrapper 추가

이번 단계의 핵심 판단
1. 이제 목표는 cd_value 자체가 아니라 저MDD 전략에 레버리지를 얹었을 때 살아남는 전용 전략군 구축이다.
2. 따라서 아무리 MDD가 낮아도 수익이 지나치게 약한 후보는 우선순위가 낮다.
3. 평가 순서는 다음이 적절하다.
   a. 비레버리지 기준 MDD 10% 미만 또는 그에 근접한지
   b. 수익이 레버리지 증폭을 버틸 만큼 충분한지
   c. PF와 max_conc가 실전적으로 견딜 만한지
   d. 그 뒤 cd_value 참고

v56 숏 전용 hybrid의 목적
- v52 behavioral guard와 v54 diverse entry modes를 한 엔진 안에서 동시에 검증 가능하게 만든 것
- 이제 dd_brake, loss_streak, max_active_cap, max_per_symbol 와 dense_skip, reentry_gap, quiet_after_first, confirmation 을 동시에 조합할 수 있다

v57 롱 전용 hybrid의 목적
- v53 behavioral guard와 v55 diverse entry modes를 한 엔진 안에서 동시에 검증 가능하게 만든 것
- 이제 max50/lossbrake 계열과 confirmation/reentry/dense/quiet 철학을 동시에 조합할 수 있다

현재 즉시 실행 우선순위
숏
1. short_hybrid_ddbrake_dense30
2. short_hybrid_conservative_reentry48
3. short_hybrid_conservative_dense30
4. short_hybrid_dense30_confirm24_dd

롱
1. long_hybrid_confirmation24_reentry48
2. long_hybrid_dense30_confirm24
3. long_hybrid_conservative_dense30_confirm
4. long_hybrid_conservative_reentry48

중요한 해석 포인트
- 숏은 이미 baseline/dd_brake 계열이 강하므로, dense skip 과 reentry gap 으로 max_conc와 MDD를 더 깎아내릴 수 있는지가 핵심이다.
- 롱은 behavioral guard가 특히 강하게 먹혔으므로, confirmation/reentry/dense 를 얹어도 수익이 심하게 훼손되지 않는지가 핵심이다.
- 롱은 PF 1.3 이상, MDD 10% 미만, 수익 70% 이상대가 당분간 현실적인 중간 목표다.

이번 단계에서 보류한 것
- retrace entry, split entry를 hybrid 1순위로 넣지는 않았다.
- 이유는 기존 단독 lane 결과에서 MDD는 개선됐지만 수익 유지력이 너무 약하거나 max_conc가 오히려 늘어난 사례가 많았기 때문이다.
- 따라서 retrace/split은 hybrid 1차 검증 뒤 2차 진입 철학 축으로 다루는 것이 맞다.

다음 어시스턴트가 해야 할 일
1. v56/v57 결과를 먼저 확보한다.
2. 결과가 나오면 MDD 10% 미만 후보만 따로 모아 비교한다.
3. 그 다음에 retrace/split/delayed entry 를 다시 저MDD 전용 구조에 제한적으로 접목한다.
4. summary에 cd_value를 넣는 작업은 병행하되, 실험 우선순위는 아니다.
