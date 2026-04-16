# CORE SUMMARY INDEX

이 폴더는 저장소 전체의 통합 핵심 요약 레이어다.
기존 test 폴더들(TEST6, test8, test10 등)은 아카이브/세부 인수인계 기록으로 유지하고,
앞으로의 실험 진행은 이 CORE_SUMMARY를 가장 먼저 확인한 뒤 세부 폴더로 내려가는 방식으로 운영한다.

## 목적
- 과거의 수많은 테스트 기록을 하나의 상위 구조로 통합한다.
- 앞으로 새 전략을 시도할 때 무엇을 어디에 기록해야 하는지 고정한다.
- 비교 기준선, 금지수칙, 로컬 백테스트 원칙, 결과 업데이트 규칙을 중앙집중화한다.

## 읽는 순서
1. 01_OBJECTIVE_AND_METRICS.md
2. 02_NONNEGOTIABLE_RULES.md
3. 03_CURRENT_BASELINES.md
4. 04_STRATEGY_REGISTRY.md
5. 05_EXPERIMENT_UPDATE_PROTOCOL.md
6. 06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md
7. 07_EXPERIMENT_ENTRY_TEMPLATE.md

## 운영 원칙
- 기존 test 폴더는 삭제하지 않는다. 아카이브로 보존한다.
- 앞으로의 핵심 판단은 CORE_SUMMARY에서 먼저 확인한다.
- 새 전략/새 실험이 나오면 반드시 CORE_SUMMARY와 해당 실험 폴더를 같이 갱신한다.

## 권장 디렉터리 역할 분담
- CORE_SUMMARY/: 전체 판단 기준, 기준선, 업데이트 프로토콜
- scripts/: 백테스트 러너 및 전략 코드
- experiments/: 조합/설정 JSON
- results_*/: 결과 산출물
- test*/TEST*/: 시기별 상세 인수인계 및 사후 분석 아카이브

## 앞으로의 업데이트 최소 단위
새 전략 또는 새 실험을 추가할 때 최소한 아래 4개는 갱신한다.
1. 해당 전략 코드 또는 러너 파일
2. 결과 폴더
3. CORE_SUMMARY/04_STRATEGY_REGISTRY.md
4. CORE_SUMMARY/03_CURRENT_BASELINES.md 또는 05_EXPERIMENT_UPDATE_PROTOCOL.md에서 지정한 비교 기록
