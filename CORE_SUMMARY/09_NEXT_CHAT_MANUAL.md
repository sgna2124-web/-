새 대화창의 어시스턴트 행동 순서

1. 가장 먼저 CORE_SUMMARY/00_START_HERE.md 를 읽는다.
2. 그 다음 CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md 를 읽어 현재 백테스트 고정 환경을 확인한다.
3. 그 다음 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 읽어 현재 유효 결과만 파악한다.
4. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 읽어 최근 전략군의 구조적 장단점을 파악한다.
5. 이후 사용자 요청에 맞춰 전략 설계, 결과 해석, 문서 갱신을 진행한다.

새 대화창에서 반드시 확인할 현재 전제
공식 판정은 cd_value와 MDD 기준이다.
cd_value는 max_return_pct 기준으로 계산한다.
자산 진입 비중은 1%다.
수수료는 0.04%다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
결과 요약에는 max_return_pct가 반드시 포함되어야 한다.

V2 실험군 처리 원칙
V2 실험군은 환경 전제 오류가 있었으므로 실패 전략으로 해석하지 않는다.
4V2R1을 제외한 V2 전략과 결과는 제거되었다.
새 대화창의 어시스턴트는 삭제된 V2 실험군을 비교 기준이나 실패 사례로 인용하면 안 된다.

사용자와 어시스턴트의 역할
사용자는 로컬 백테스트를 실행하고 결과와 코드를 저장소에 올린다.
어시스턴트는 그 결과를 분석하고, 결과 카탈로그와 통합 요약을 갱신하며, 다음 전략을 제안한다.

결과 해석 전 점검 체크
자산 1% 진입이 반영되었는가
수수료 0.04%가 반영되었는가
FAST 예비검사가 개입되지 않았는가
결과 파일에 max_return_pct가 포함되었는가
공식 비교가 전체 종목 풀 백테스트 기준인가

반드시 해야 되는 일 목록
1. 사용자가 결과를 저장소에 올렸다면 local_results 또는 해당 결과 폴더를 먼저 확인한다.
2. 결과를 기존 공식 long-only / short-only 기준선과 비교한다.
3. 단순 수치 비교로 끝내지 말고, 왜 성과가 나왔는지 장점과 단점을 함께 정리한다.
4. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 갱신한다.
6. 승격이 발생하면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 같이 갱신한다.
7. 지표 정의 충돌이 발견되면 CORE_SUMMARY/01_OBJECTIVE_AND_METRICS.md 를 기준으로 다른 문서를 정정한다.
8. 결과를 확인만 하고 문서 업데이트를 빼먹지 않는다.
9. 각 신규 배치 결과를 반영할 때, 배치 내 long 최고 후보와 short 최고 후보를 max_return_pct 기준으로 명시한다.
10. 전 전략이 탈락한 배치라도 과다거래, 방향 필터 부족, 진입 지연, 추세 위치 오류 같은 구조적 실패 원인을 문장으로 남긴다.
11. 압축 사다리, midband tag, wick accumulation처럼 거래 수가 비정상적으로 치솟는 구조를 발견하면, 재사용 금지 또는 추가 방향 필터 필요 여부를 명시한다.

환경 오류 발생 시 처리
환경 오류가 확인되면 그 실험군은 invalid_env로 처리한다.
invalid_env 실험은 보존형 실패 기록이 아니라 제거 대상이다.
