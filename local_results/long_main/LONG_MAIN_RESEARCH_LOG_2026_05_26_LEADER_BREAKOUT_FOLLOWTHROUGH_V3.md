# LONG_MAIN_RESEARCH_LOG_2026_05_26_LEADER_BREAKOUT_FOLLOWTHROUGH_V3

## 목적
롱 메인 새 원류 전략 탐색 3차 결과를 기록한다.
다음 대화창에서 동일한 long breakout/follow-through 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
이미 실패한 새 long family:
- Volatility Contraction to Expansion Continuation
- Slow Momentum Persistence
- Relative Strength Long Proxy
- Breadth Leadership Proxy
- Regime Transition Continuation
- RS Pullback Reclaim
- Leader Shallow Pullback Continuation
- Failed Breakdown Reclaim
- Tight Leader Re-Acceleration

위 실패를 바탕으로 3차에서는 pullback/reclaim이 아니라 강한 리더의 breakout 이후 짧은 follow-through를 테스트했다.

## 3차 시도
파일:
run_long_leader_breakout_followthrough_v3_1h.py

결과 폴더:
local_results/long_main/LONG_LEADER_BREAKOUT_FOLLOWTHROUGH_V3_1H

탐색 family:
- Leader Breakout Follow-through
- Elite Leader Breakout
- Delayed Follow-through
- Tight Volume Breakout

핵심 가설:
강한 종목의 breakout candle 이후 1~3봉 이내 follow-through가 long edge일 수 있다.

조건 방향:
- ret60/ret120 강한 종목
- 최근 20/40/60봉 range 상단 돌파
- breakout candle body_atr 강함
- close_pos 높음
- upper_wick 낮음
- volume ratio 상승
- breakout 이후 1~3봉 follow-through 확인
- 짧은 stop
- 짧은 hold
- 거래수 강제 축소

## 결과
master_summary 기준:
- 후보 75개
- rows 75
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
3차는 이전 1차/2차보다 거래수를 줄이고, 강한 리더 필터와 breakout candle 품질 조건, follow-through 확인을 넣었다.
그럼에도 유효 후보가 나오지 않았다.

해석:
1. long side에서 단순 momentum chase는 약하다.
2. strong leader breakout follow-through는 장기 expectancy가 부족하다.
3. 강한 움직임을 따라붙는 계열은 fee bleed 또는 whipsaw에 취약하다.
4. long breakout은 직관적으로 좋아 보여도 600개 다종목 장기 백테스트에서는 구조적 edge로 확인되지 않았다.

## 반복 금지
다음 구조는 그대로 반복하지 말 것.

- strong leader breakout candle 이후 단순 follow-through 진입
- ret60/ret120 강세 + range high breakout + volume spike 조합
- close_pos 높고 upper_wick 낮은 breakout candle 추종
- 1~3봉 delayed follow-through 단독 확인
- tight range volume breakout 단독 long
- momentum chase 기반 long continuation

## 현재까지 제거된 큰 long family
1. Persistence continuation
2. Shallow reclaim
3. Pullback continuation
4. Breakout follow-through
5. Broad momentum chase
6. RS rank continuation
7. Leader pullback continuation

## 살아남은 단서
강한 종목을 따라붙는 방식은 실패했다.
따라서 다음은 강한 움직임 자체가 아니라, 강한 움직임이 실패한 뒤의 회복 구조를 연구해야 한다.

## 다음 방향
다음 탐색 family:
Failed Breakout / Failed Continuation 기반 long edge

핵심 전환:
강한 움직임 추종 -> 실패한 강한 움직임 이후 회복 구조 분석

새 가설:
강한 breakout이 이어지지 못한 뒤 가격 구조가 다시 회복되는 순간이 long edge일 수 있다.

탐색 후보:
- breakout failure 후 재회복
- failed continuation 이후 range 재진입
- momentum failure 이후 구조 회복
- liquidity sweep failure
- 강한 candle 이후 follow-through 실패 후 재회복

주의:
기존 flush recovery/reclaim 기준선과 혼동하지 말 것.
다음 방향은 큰 하락 후 반등이 아니라, breakout 실패와 momentum failure 이후의 구조 회복을 보는 것이다.

## 다음 대화창용 요약
롱 메인은 현재 새 원류 전략 탐색 단계다.
1차 persistence/continuation 실패.
2차 pullback/reclaim 실패.
3차 leader breakout follow-through 실패.

따라서 다음은 momentum을 따라붙는 것이 아니라, momentum failure 이후 회복 구조를 이용하는 long edge를 탐색해야 한다.
