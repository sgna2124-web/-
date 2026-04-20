이 파일은 새 대화창의 첫 진입점이다.
새 대화창의 어시스턴트는 다른 요약 문서보다 먼저 이 파일을 읽고 현재 프로젝트 상태를 복원한다.

현재 프로젝트 목표
코인/주식 차트 전략 중 MDD 5% 미만 전략을 우선 후보로 보고, 그중 cd_value가 가장 높은 전략을 찾는다.
롱 전용 전략 1위와 숏 전용 전략 1위를 별도 기준으로 유지하며, 앞으로의 모든 백테스트 결과는 이 기준과 비교한다.

성과 판단 기준
공식 판단 기준은 cd_value와 max_drawdown_pct(MDD)이다.
max_return_pct는 단독 판단 지표는 아니지만 cd_value 산출에 반드시 포함된다.
final_return_pct는 참고 지표로 기록하되, 공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.

cd_value 정의
cd_value는 max_return_pct / max_drawdown_pct 로 해석한다.
문서와 결과 해석에서 cd_value를 final_return_pct 기준으로 계산하면 안 된다.
현재 프로젝트에서 cd_value는 max_return_pct 기준이다.

고정 백테스트 환경
자산 진입 비중은 1%다.
수수료는 0.04%다.
공식 판정은 전체 종목 풀 백테스트 기준이다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
백테스트 결과 요약에는 max_return_pct를 반드시 포함한다.

무효 실험 처리 규칙
정상 환경에서 실패한 전략은 기록으로 남긴다.
하지만 환경 설정 오류, 엔진 설정 오류, 자산 비중 오류, 수수료 오류, 비교 불가능한 실험은 invalid_env로 간주한다.
invalid_env 실험은 실패 전략 기록으로 보존하지 않고, 비교 체계 오염 방지를 위해 결과와 카탈로그에서 제거한다.

현재 상태 요약
V2 실험군은 환경 전제 오류가 있었으므로 4V2R1을 제외하고 전부 제거했다.
새 대화창의 어시스턴트는 기존 V2 결과를 비교 근거로 사용하면 안 된다.
최근 4V2R4 ~ 4V2R9 신규 진입 조건 실험군은 공식 1위 교체 없이 종료되었고, 장단점은 별도 문서로 정리한다.

역할 분담
사용자는 로컬 컴퓨터에서 백테스트를 실행하고, 전략 코드와 결과 요약 파일을 저장소에 업로드한다.
어시스턴트는 업로드된 결과를 검토하고, 통합 요약/결과 카탈로그/장단점 문서/다음 단계 매뉴얼을 갱신하며, 다음 실험 전략을 설계한다.

결과 업로드 후 반드시 할 일
1. 업로드된 local_results 또는 결과 폴더를 확인한다.
2. 공식 long-only / short-only 기준선과 비교한다.
3. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
4. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 갱신한다.
5. 승격이면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 갱신한다.
6. 결과만 보고 끝내지 말고, 왜 그런 결과가 나왔는지 장점과 단점을 남긴다.

다음으로 읽을 문서
1. CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md
2. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md
3. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md
4. CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md
