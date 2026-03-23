# 10_NEXT_ACTIONS

현재 가장 중요한 다음 단계
1. state_miner 전체 결과 확인
2. strict survivors 개수 판정
3. survivors가 0이면 5분 OHLCV-only 공간 종료 여부 결정
4. survivors가 1개 이상이면 기존 엔진에 즉시 삽입해 전략 테스트

판정 기준
- strict survivors = 0 : 일반적 5분 OHLCV-only 탐색 공간 종료를 공식 고려
- strict survivors 소수 : breadth와 test 구간 확인 후 바로 전략화 또는 폐기
- robust survivors 다수 : 즉시 엔진 삽입 및 포트폴리오 순차 백테스트

반복 금지
- 세션/시간/압축폭발/OI/일반 상태 분류로 되돌아가지 말 것
- state_miner 결과가 나오기 전에는 새 전략을 마구 늘리지 말 것
- 새 전략을 제안하더라도 사건 중심, 비정상 상태, 짧은 SL, 선명한 무효화 기준이 있는 철학만 검토

작업 루프
아이디어 -> 기존 엔진 삽입 -> 전체 백테스트 -> 결과를 test3에 기록