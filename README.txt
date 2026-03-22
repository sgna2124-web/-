돈버는 차트 전략 찾기 - 실험 로그/코드 아카이브

이 저장소는 OHLCV만으로 코인 선물 자동매매(다종목/시간순 포트폴리오 백테스트) 전략을 실험한 코드와 기록을 정리한 것입니다.

구성
- docs/
  - handoff_manual_2026-03-22.txt : 새 대화/새 작업자에게 넘기는 인수인계 매뉴얼(요구사항/제약/진행과정/결론)
  - strategy_timeline.txt : Pine/Python 버전별 변화 요약
  - results_log.txt : 백테스트 출력 로그(핵심 구간)
- backtests/trendpullback/
  - engine_trendpullback_v42_v42N_mix_Aminstop.py : 기존 학습형엔진 틀을 유지하면서 ‘진입/상태/SLTP’만 TrendPullback으로 교체한 파일(3모드 + A안 최소 파동폭 필터)

주의
- 원본 엔진(학습형엔진)의 엑셀 입출력/print/plt/순차 시뮬(시간순 재순환) 등 ‘틀’은 그대로 두고, 진입 조건/상태변수/SLTP만 변경하는 방식으로 작업했습니다.
