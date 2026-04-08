다음 대화창에서 즉시 할 일

현재 공식 기준선
- atr19_t27_b17_r020
- 구조: atr_only + ema_only + timeout 27 + atr_stop_mult 1.9 + time_reduce 17봉 후 위험 20% 축소

가장 먼저 할 실험
- timeout 27과 atr 1.9는 고정한다.
- time_reduce 축만 더 초미세 조정한다.
- 우선 탐색 추천 구간:
  - time_reduce_bars: 16, 17, 18
  - time_reduce_to_risk_frac: 0.18, 0.20, 0.22
- 이 축은 이미 v4에서 0.20이 0.25를 넘어섰기 때문에, 0.18~0.22 부근의 미세 탐색이 가장 우선이다.

2순위 실험
- atr_stop_mult는 1.90을 중심으로 아주 미세하게 조정한다.
- 추천 구간:
  - 1.88, 1.90, 1.92
- timeout은 27을 중심으로 유지하되, 비교용으로 28을 소수 넣을 수 있다.
- 하지만 현재 데이터상 timeout 27이 주력이다.

3순위 실험
- 안정형 보조 레인을 별도로 유지하고 싶다면 아래 후보를 추적한다.
  - atr195_t27_b17_r025_long_light
- 이 후보는 절대 수익형 1위는 아니지만 MDD와 PF가 매우 좋다.
- 다만 주 흐름은 공격형 1위 갱신이다.

당분간 하지 말 것
- confirmation 재탐색
- pure retrace entry 재탐색
- 조기 breakeven 중심 레인
- aggressive trailing 중심 레인
- short_light 단독 대량 탐색
이들은 지금까지의 누적 결과상 주력 축이 아니다.

다음 대화창에서의 추천 작업 순서
1. TEST9/01_CURRENT_STATE_AND_TOP_STRATEGIES.md 읽기
2. TEST9/03_EXPERIMENT_HISTORY_AND_LESSONS.md 읽기
3. timeout 27 + atr 1.9 + time_reduce 16~18 / 0.18~0.22 레인 생성
4. workflow 생성
5. 백테스트 실행
6. cd_value 기준 재정렬
7. 수익과 MDD가 함께 개선됐는지 판정

판정 기준
- 같은 1위가 유지되고 MDD 개선이 없으면 또 다시 새로운 개선안을 만든다.
- 수익 증가와 MDD 감소가 동시에 일어나면 승격 후보로 본다.
- cd_value 우선, 그 다음 final_return_pct와 mdd_pct를 같이 본다.
