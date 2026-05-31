# LONG_MAIN_RESEARCH_LOG_2026_05_26_COMPRESSION_EXPANSION_MICROCYCLE_V13

## 목적
롱 메인 새 원류 전략 탐색 13차 결과를 기록한다.
다음 대화창에서 동일한 Event Compression / Expansion Microcycle 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
v8~v12에서 다음 축이 실패했다.

- v8 Cross-Sectional Oversold Reversal
- v9 Cross-Sectional State Transition
- v10 Cross-Sectional Decoupling / Recoupling
- v11 Intrabar Risk Shape / Stop-Take Interaction
- v12 Holding-Time Edge / Early Path Filter

따라서 v13에서는 조용한 상태 자체가 아니라, 압축이 끝나고 확장이 시작되는 이벤트를 테스트했다.

## 13차 시도
파일:
run_long_compression_expansion_microcycle_v13_1h.py

결과 폴더:
local_results/long_main/LONG_COMPRESSION_EXPANSION_MICROCYCLE_V13_1H

탐색 family:
- Same-Bar Compression Release
- Volume Contraction Expansion
- Body Compression Directional Expansion
- Longer Compression Release

핵심 가설:
직전 N봉 range/ATR, volume, body가 압축된 뒤 range expansion + volume expansion + close position 개선이 동시에 나오면 확장 초입 long edge가 있을 수 있다.

조건 방향:
- 직전 N봉 range/ATR 압축
- 직전 body/ATR 압축
- 직전 volume contraction
- 직전 ret abs 압축
- 현재 range expansion
- 현재 body expansion
- 현재 volume expansion
- close position 개선
- 상단 꼬리 제한
- 고정 SL/TP

## 결과
master_summary 기준:
- 후보 45개
- rows 45
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
v13은 기존 Quiet Drift와 다르다.
Quiet Drift는 조용한 상태 자체를 매수하는 구조였고, v13은 압축 해제 이벤트를 매수하는 구조였다.
그러나 현재 조건에서는 유효 후보가 전혀 나오지 않았다.

따라서 다음 구조는 현재 형태로 반복하지 않는다.

- same-bar compression release 단독
- volume contraction 후 expansion 단독
- body compression 후 directional expansion 단독
- longer compression release 단독
- range/volume/body 압축 해제 이벤트만으로 long edge 탐색

## 현재까지 제거된 long side 중심축
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry
7. cross-sectional oversold reversal
8. cross-sectional state transition
9. cross-sectional decoupling / recoupling
10. intrabar risk shape / stop-take interaction
11. holding-time edge / early path filter
12. compression / expansion microcycle

## 살아남은 단서
v7 cross-sectional relative safety에서만 약한 TOP_ANY_MDD 후보가 있었지만, MDD가 높아 신규 기준선 후보로는 약하다.
현재 단계에서는 다른 정보축 탐색을 계속한다.

## 다음 방향 후보
다음은 단일 이벤트나 진입 후 경로가 아니라, 시장의 시간대/캔들 위치별 구조를 보는 것이 적합하다.

후보:
Time-Position / Sessionless Cycle Edge Long

핵심 가설:
암호화폐는 24시간 시장이지만, 5분봉/1시간봉 내부에서 특정 시간 간격, 일중 위치, 주기적 변동성 전환 구간에 long edge가 있을 수 있다.

주의:
기존 세션 테스트를 그대로 반복하면 안 된다.
다음은 단순 세션 필터가 아니라, candle index modulo / volatility cycle / periodic reset 구조를 탐색해야 한다.
