# 07_STATE_MINER_CONTEXT

state_miner 목적
- 가능한 많은 OHLCV 연속형 상태를 single/pair/triple 조합으로 스캔
- 각 상태에서 TP-first, SL-first, net EV를 계산
- strict survivor만 남김

이미 확인된 사실
- BTC 단독 strict survivors = 0
- 다른 단일 알트도 strict survivors = 0
- 단일 종목 테스트로는 얻을 정보가 거의 없음

중요한 판정 규칙
- strict survivors = 0 이면 5분 OHLCV-only 공간 종료를 진지하게 고려
- strict survivors가 1개 이상이면 바로 기존 엔진에 삽입해 전략 테스트
- 이 단계에서는 새 전략 아이디어 남발보다, 공간 자체를 종료할지 판정하는 것이 중요

사용자 입장
- 이 실험은 마지막 판정에 가까움
- 여기서 0이면 5분 공간은 공식 종료 가능
- survivors가 나오면 즉시 전략화