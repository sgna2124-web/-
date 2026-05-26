# LONG_MAIN_RESEARCH_LOG_2026_05_26_NEW_EDGE_FAMILY_ATTEMPTS

## 목적
롱 메인 개발 과정에서 실패한 새 edge family와 다음 탐색 방향을 기록한다.
다음 대화창에서 동일한 실패 방향을 반복하지 않기 위함이다.

## 1차 시도
파일:
run_long_new_edge_family_probe_1h.py

결과 폴더:
local_results/long_main/LONG_NEW_EDGE_FAMILY_PROBE_1H

탐색 family:
- Volatility Contraction -> Expansion Continuation
- Slow Momentum Persistence
- Relative Strength Long Proxy
- Breadth Leadership Proxy
- Regime Transition Continuation

결과:
- 후보 126개
- errors 0
- MDD 5% 미만 후보 없음
- 유효 top_any_mdd 후보 없음

실패 원인:
- EMA 유지 + persistence + rank proxy 단독 구조는 fee bleed 발생
- broad continuation 구조는 반복 손절 발생
- 거래수 과다

반복 금지:
- ret60 persistence 단독
- EMA reclaim 단독
- RS rank continuation 단독
- broad continuation 구조

## 2차 시도
파일:
run_long_new_edge_family_pullback_reclaim_v2_1h.py

결과 폴더:
local_results/long_main/LONG_NEW_EDGE_PULLBACK_RECLAIM_V2_1H

탐색 family:
- RS Pullback Reclaim
- Leader Shallow Pullback Continuation
- Failed Breakdown Reclaim
- Tight Leader Re-Acceleration

결과:
- 후보 99개
- errors 0
- MDD 5% 미만 후보 없음
- 유효 top_any_mdd 후보 없음

실패 원인:
- 강한 종목 + 눌림 + reclaim 구조는 long edge 부족
- 거래수 과다
- shallow reclaim 구조는 반복 손절 유발

반복 금지:
- shallow pullback reclaim 단독
- failed breakdown reclaim 단독
- broad leader pullback 구조

## 살아남은 단서
- 강한 종목 필터 자체는 유지 가능
- 눌림 회복보다 breakout 이후 follow-through가 유력
- 거래수 강제 제한 필요

## 다음 방향
Leader Breakout Follow-through

핵심 가설:
강한 종목의 breakout candle 이후 1~3봉 follow-through가 edge일 수 있다.

구조:
- ret60/ret120 강한 종목
- breakout candle 확인
- body_atr 강함
- close_pos 높음
- upper_wick 낮음
- volume ratio 상승
- 1~3봉 follow-through
- 짧은 stop
- 짧은 hold
- 거래수 제한
