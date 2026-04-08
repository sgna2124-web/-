TEST9 인수인계 폴더

목적
- 다음 대화창의 어시스턴트가 이 폴더만 읽고 현재 상태를 즉시 파악하고 다음 실험을 이어갈 수 있게 한다.
- 사용자의 장기 목표는 돈을 벌 수 있는 전략을 찾는 것이며, 현재는 차트 기반 자동매매 백테스트를 반복 개선하는 단계다.
- 이번 TEST9는 TEST8 이후 진행된 모든 핵심 실험, 현재 최강 후보, 실패 패턴, 실행 방법, 다음 우선순위를 기록한다.

가장 먼저 읽을 파일
1. 01_CURRENT_STATE_AND_TOP_STRATEGIES.md
2. 02_BACKTEST_RULES_AND_USER_REQUIREMENTS.md
3. 03_EXPERIMENT_HISTORY_AND_LESSONS.md
4. 04_WORKFLOWS_AND_RESULTS_MAP.md
5. 05_NEXT_STEPS_IMMEDIATE.md
6. state_snapshot.json

현재 최강 전략 한 줄 요약
- 현 시점 전체 1위는 atr19_t27_b17_r020 이다.
- 구조: atr_only stop + ema_only target + timeout 27 + time_reduce 17봉 후 위험 20% 축소 + atr_stop_mult 1.9
- 이 전략은 직전 1위 대비 수익이 증가했고 MDD도 개선됐다.

현재 단계의 큰 결론
- 전략 우위의 핵심은 진입 필터 강화보다 청산/리스크 구조 설계에 있다.
- 특히 아래 순서로 개선이 발생했다.
  timeout_18bars baseline -> ema_only target -> atr_only stop -> longer timeout -> time_reduce 보호 구조 -> time_reduce 초미세 조정
- 이제 주력 탐색 축은 timeout 27, atr_stop_mult 1.9 부근, time_reduce 16~18봉, risk_frac 0.20~0.25 부근이다.

중요 원칙
- 사용자 요청상 최대 포지션 보유수는 제약하지 않는다.
- top_n_per_timestamp 같은 동시 진입 제한은 사용하지 않는다.
- 개선이 안 되면 계속 새 개선안을 적용한다. 되묻지 말고 바로 반영하고 백테스트 가능한 상태로 만들어야 한다.
- 결과 정렬 시 중복 전략은 제거하고, cd_value를 핵심 정렬 기준으로 사용한다.

cd_value 정의
- 사용자가 명시한 방식은 초기 자산 100에 MDD를 먼저 적용한 뒤 peak_growth를 반영하는 것이다.
- 수식: cd_value = 100 * (1 + mdd_pct / 100) * (1 + peak_growth_pct / 100)
- mdd_pct는 음수 값이다.
- 이 값이 높을수록 사용자 기준에서 좋은 전략이다.

주의
- 본 폴더는 사람이 보기 위한 요약이면서 동시에 다음 어시스턴트가 즉시 행동하기 위한 운영 문서다.
- 다음 대화창에서는 현재 1위 기준선부터 바로 후속 레인을 추가하고 실행하면 된다.
