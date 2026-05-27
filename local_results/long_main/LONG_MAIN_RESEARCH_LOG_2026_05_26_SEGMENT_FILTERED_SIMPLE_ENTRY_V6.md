# LONG_MAIN_RESEARCH_LOG_2026_05_26_SEGMENT_FILTERED_SIMPLE_ENTRY_V6

## 목적
롱 메인 새 원류 전략 탐색 6차 결과를 기록한다.
다음 대화창에서 동일한 segment filter + simple entry 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
1~5차에서 다음 long family가 실패했다.

- Persistence continuation
- Shallow reclaim
- Pullback continuation
- Breakout follow-through
- Failed breakout recovery
- Quiet accumulation / Low volatility drift
- Broad momentum chase
- RS rank continuation
- Leader pullback continuation

5차까지 단일 진입 family가 계속 실패했으므로, 6차에서는 새로운 candle pattern을 만드는 대신 long 허용 구간을 먼저 찾는 방식으로 전환했다.

## 6차 시도
파일:
run_long_segment_filtered_simple_entry_v6_1h.py

결과 폴더:
local_results/long_main/LONG_SEGMENT_FILTERED_SIMPLE_ENTRY_V6_1H

탐색 family:
- Moderate Uptrend Segment
- Stabilized After Weakness Segment
- Low Vol Allowed Segment
- Relative Safe Segment

핵심 가설:
롱 edge는 특정 candle pattern보다 특정 OHLCV segment에서만 발생할 수 있다.
따라서 먼저 long 허용 구간을 필터링하고, 그 안에서 단순 entry를 적용하면 기존 패턴 탐색보다 나을 수 있다.

조건 방향:
- ATR percentile / ATR range
- range20 / range60
- ret20 / ret60 / ret120 segment
- EMA 위치
- RSI 범위
- volume ratio 범위
- wick/body 품질
- relative rank proxy
- 단순 green candle 또는 close_above_prev entry

## 결과
master_summary 기준:
- 후보 66개
- rows 66
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
이번 6차는 진입 조건을 새로 만든 것이 아니라, long 허용 segment를 먼저 찾고 단순 진입만 얹는 구조였다.
그럼에도 유효 후보가 나오지 않았다.

따라서 개별 종목 내부 OHLCV 상태만으로 long이 유리한 구간을 찾는 방식은 현재 설계로는 부족하다.

현재까지 long side에서 제거된 중심축:
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry

## 반복 금지
다음 구조는 그대로 반복하지 말 것.

- ATR/range/trend/EMA/RSI segment만으로 long 허용 구간을 만드는 방식
- 개별 종목 내부 상태만 보고 simple_green 진입
- 개별 종목 내부 상태만 보고 close_above_prev 진입
- moderate uptrend segment 단독
- stabilized weakness segment 단독
- low vol allowed segment 단독
- relative safe segment 단독

## 살아남은 단서
개별 종목 내부 상태만으로는 long edge 탐색에 한계가 크다.
다음은 cross-sectional 구조로 이동해야 한다.
즉 같은 시점의 전체 종목 분포에서 상대적으로 강하거나 안정적인 종목을 선택하는 방식이 필요하다.

## 다음 방향
다음 탐색 family:
Cross-Sectional Relative Strength / Relative Safety Long

핵심 전환:
개별 종목 내부 상태 -> 같은 시점의 전체 종목 분포 기반 선택

새 가설:
롱 edge는 개별 종목의 절대 상태보다 같은 시점 전체 시장 내 상대적 위치에서 더 잘 나타날 수 있다.

탐색 후보:
- 같은 timestamp에서 ret20/ret60 상위 percentile 종목만 long
- 같은 timestamp에서 최근 낙폭이 작은 종목군만 long
- market-wide breadth proxy가 양호한 구간만 long
- 전체 종목 중 상승 유지 비율이 높은 구간만 long
- 상대강도 상위 + 변동성 중간 이하
- 상대강도 상위 + 과열 제외
- 상대적으로 덜 빠진 종목의 회복

주의:
다음 방향은 종목 단독 파일 내부 rolling rank만으로 처리하면 안 된다.
가능하면 timestamp 기준으로 여러 종목을 모아 cross-sectional rank를 계산해야 한다.
