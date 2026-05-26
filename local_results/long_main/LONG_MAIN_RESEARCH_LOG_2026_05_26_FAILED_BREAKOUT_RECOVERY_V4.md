# LONG_MAIN_RESEARCH_LOG_2026_05_26_FAILED_BREAKOUT_RECOVERY_V4

## 목적
롱 메인 새 원류 전략 탐색 4차 결과를 기록한다.
다음 대화창에서 동일한 failed breakout recovery 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
이미 실패한 큰 long family:
- Persistence continuation
- Shallow reclaim
- Pullback continuation
- Breakout follow-through
- Broad momentum chase
- RS rank continuation
- Leader pullback continuation

3차에서 Leader Breakout Follow-through가 실패했기 때문에, 4차에서는 강한 움직임을 따라붙는 것이 아니라 강한 움직임 실패 후 구조 회복을 테스트했다.

## 4차 시도
파일:
run_long_failed_breakout_recovery_v4_1h.py

결과 폴더:
local_results/long_main/LONG_FAILED_BREAKOUT_RECOVERY_V4_1H

탐색 family:
- Failed Breakout Level Recovery
- Failed Hot Breakout Recovery
- EMA Structure Failed Breakout Recovery
- Tight Failed Breakout Recovery

핵심 가설:
강한 breakout 또는 continuation이 실패한 뒤 가격 구조가 다시 회복되는 순간이 long edge일 수 있다.

조건 방향:
- 최근 강한 breakout attempt 존재
- breakout 이후 1~6봉 안에 follow-through 실패
- 돌파 레벨 또는 EMA 주변으로 흔들림
- 이후 다시 돌파 레벨 또는 EMA20/EMA50 위 회복
- wick/volume spike 이후 안정화
- 짧은 stop
- 짧은 hold
- 거래수 제한

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
이번 결과는 강한 움직임 추종뿐 아니라 강한 움직임 실패 후 회복 구조도 현재 조건으로는 유효하지 않다는 의미다.

현재까지 long side에서 제거된 중심축:
1. 강한 움직임 지속
2. 강한 종목 눌림 후 회복
3. 강한 breakout 추종
4. 강한 breakout 실패 후 회복

즉 다음부터는 강한 움직임 자체를 중심에 두는 방식에서 벗어나야 한다.

## 반복 금지
다음 구조는 그대로 반복하지 말 것.

- breakout attempt 이후 단순 level recovery
- failed breakout 이후 EMA20/EMA50 reclaim 단독
- failed hot breakout 이후 재회복 단독
- tight range breakout 실패 후 회복 단독
- strong move failure recovery를 broad하게 여는 구조

## 살아남은 단서
강한 움직임과 그 실패를 모두 중심축으로 삼은 long family가 계속 실패했다.
다음은 강한 움직임이 아니라 조용한 축적, 저변동성, 미세한 drift 구조를 봐야 한다.

## 다음 방향
다음 탐색 family:
Quiet Accumulation / Low Volatility Drift

핵심 전환:
강한 움직임 중심 -> 조용한 축적과 미세한 상승 압력 중심

새 가설:
롱 edge는 강한 움직임을 따라붙거나 실패 후 회복을 잡는 것이 아니라, 관심이 적고 변동성이 낮은 구간에서 서서히 위로 쏠리는 구조에 있을 수 있다.

탐색 후보:
- low volatility drift
- quiet accumulation
- low ATR + positive micro returns
- range contraction without breakout
- EMA 위 미세 유지
- 거래량 과열 없음
- upper wick 낮음
- drawdown 얕음
- short hold보다 중간 hold 가능성 테스트

## 다음 대화창용 요약
롱 메인은 새 원류 전략 탐색 단계다.
1차 persistence/continuation 실패.
2차 pullback/reclaim 실패.
3차 leader breakout follow-through 실패.
4차 failed breakout recovery 실패.

다음은 강한 움직임을 중심에 두지 말고 Quiet Accumulation / Low Volatility Drift 계열을 탐색해야 한다.
