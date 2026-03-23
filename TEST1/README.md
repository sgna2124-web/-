# TEST1

이 폴더는 사람이 보기 위한 정리본이 아니라, 이후 새로운 대화에서 모델이 바로 이어서 작업할 수 있도록 만든 체크포인트다.

핵심 목적
- 현재 프로젝트의 목표, 금지사항, 전략 철학, 파라미터, 백테스트 구조, 문제점, 다음 스텝을 잃지 않고 복원
- 최신 Casino Probability Engine 코드 스냅샷 보존
- 이후 대화에서 같은 실수와 중복 실험을 줄이기

새 대화에서 사용하는 방법
- GitHub 저장소 sgna2124-web/- 의 TEST1 폴더를 읽고 이어서 진행하라고 요청한다.
- 우선 읽을 파일 순서:
  1. 00_PROJECT_RULES.txt
  2. 01_STRATEGY_CORE.txt
  3. 02_ENGINE_SPEC.txt
  4. 03_FEATURE_SPEC.txt
  5. 05_CURRENT_RESULT.txt
  6. 06_PROBLEMS.txt
  7. 07_NEXT_STEP.txt
  8. 10_EXPERIMENT_LOG.txt
  9. 09_CODE_ENGINE.py
  10. 08_CODE_MAIN.py

현재 핵심 전략
- Casino Probability Engine
- 5분봉 OHLCV만 사용
- 최근 1500캔들만으로 매 캔들마다 상태-확률-EV를 다시 계산
- EV > 0 인 경우만 진입
- 롱/숏 동시 보유 가능, 같은 방향 중복 금지

보안 주의
- 거래소 API 키, 시크릿, .env, 개인 식별 정보는 절대 저장하지 않는다.
- GitHub 토큰도 저장하지 않는다.
