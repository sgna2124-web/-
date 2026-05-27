# LONG_MAIN_RESEARCH_LOG_2026_05_26_QUIET_ACCUMULATION_DRIFT_V5

## 목적
롱 메인 새 원류 전략 탐색 5차 결과를 기록한다.
다음 대화창에서 동일한 Quiet Accumulation / Low Volatility Drift 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
이미 실패한 큰 long family:
- Persistence continuation
- Shallow reclaim
- Pullback continuation
- Breakout follow-through
- Failed breakout recovery
- Broad momentum chase
- RS rank continuation
- Leader pullback continuation

4차까지 강한 움직임 중심 계열이 실패했기 때문에, 5차에서는 강한 움직임을 완전히 배제하고 조용한 축적과 저변동성 drift를 테스트했다.

## 5차 시도
파일:
run_long_quiet_accumulation_drift_v5_1h.py

결과 폴더:
local_results/long_main/LONG_QUIET_ACCUMULATION_DRIFT_V5_1H

탐색 family:
- Quiet Low Vol Drift
- Quiet EMA Accumulation
- Quiet Range Upper Drift
- Low Volume Micro Drift

핵심 가설:
롱 edge는 강한 움직임을 따라붙거나 실패 후 회복을 잡는 것이 아니라, 관심이 적고 변동성이 낮은 구간에서 서서히 위로 쏠리는 구조에 있을 수 있다.

조건 방향:
- low ATR
- low range
- low wick
- volume spike 없음
- ret20/ret60 약한 양수 또는 중립
- EMA 위 미세 유지
- breakout 조건 배제
- reclaim 조건 배제
- 강한 candle 조건 배제
- 중간 hold도 테스트

## 결과
master_summary 기준:
- 후보 81개
- rows 81
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
이번에는 강한 움직임을 완전히 배제하고 저변동성, 조용한 축적, 미세 drift를 테스트했지만 유효 후보가 나오지 않았다.

현재까지 long side에서 제거된 중심축:
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift

따라서 다음부터는 단일 가격 패턴으로 long edge를 찾는 접근을 줄이고, long이 덜 죽는 구간을 먼저 찾는 시간/구간 필터형 접근으로 전환해야 한다.

## 반복 금지
다음 구조는 그대로 반복하지 말 것.

- low ATR + weak positive drift 단독
- EMA 위 조용한 축적 단독
- range 중상단 유지 단독
- low volume micro drift 단독
- no breakout / no reclaim / low noise 조건만으로 long 진입

## 살아남은 단서
롱에서 단일 진입 패턴 family를 계속 바꿔도 성과가 나오지 않고 있다.
이는 진입 패턴 자체보다 구간 선택이 먼저일 가능성을 시사한다.

## 다음 방향
다음 탐색 family:
Time / Segment Filtered Long

핵심 전환:
진입 패턴 중심 -> long이 덜 죽는 구간을 먼저 찾는 구조

새 가설:
롱 edge는 특정 candle pattern보다 특정 시간/상태/구간에서만 발생할 수 있다.
따라서 먼저 long이 구조적으로 덜 손상되는 구간을 찾고, 그 안에서 단순 진입 구조를 얹는 방식이 더 적합할 수 있다.

탐색 후보:
- 구간별 long expectancy map
- 시장 전체 breadth proxy 기반 long 허용 구간
- 최근 N봉 전체 종목 중 상승 유지 비율 proxy
- BTC/ETH 또는 대형 코인 drift proxy가 양호한 구간
- 과거 long 손실이 적었던 volatility/range segment
- 시간대 또는 날짜 구간이 아니라 OHLCV 기반 market condition segment

주의:
다음 방향은 새로운 candle pattern을 만드는 것이 아니다.
먼저 long을 허용할 수 있는 구간을 찾고, 그 다음 매우 단순한 entry를 얹는 방식으로 가야 한다.
