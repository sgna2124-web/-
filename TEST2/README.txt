TEST2 - 5m TrendPullback 실험 아카이브

이 폴더는 5분봉(5m)에서 OHLCV만으로 코인 선물 자동매매 전략(TrendPullback)을 시도했던 전체 과정을 보관합니다.

핵심 결론
- 5m + 고정 SL/TP(진입 후 수정 없음) + 추가 청산 없음(시간청산/BE/트레일링 금지) 조건에서 TrendPullback 계열은 수수료(왕복 0.08%) 환경에서 기대값이 얇거나 음수로 판단되어 ‘실패’로 정리했습니다.

구성
- docs/
  - handoff_manual_2026-03-22.txt : 새 대화/새 작업자에게 넘기는 인수인계 매뉴얼(요구사항/제약/진행과정/결론)
  - results_log_extended.txt : 백테스트 출력 로그(핵심 수치) 확장판
  - strategy_timeline.txt : 버전별(파인/파이썬) 변화 요약
  - variant_patches.txt : 단독 변경 테스트(숏 OFF, PB_DEPTH_MAX=0.9, PB_WAIT=5 등) 패치 요약
- backtests/5m_failed/
  - python/ : 학습형엔진 틀을 유지한 채 ‘진입/상태/SLTP’만 교체한 전체 스크립트(3모드 + A안)
  - pinescript/ : 파인스크립트 실험 버전(4.0~4.4 등)

주의
- 사용자가 제공한 학습형엔진.py ‘원본 파일’은 이 대화 세션에서 내용 확인이 되지 않아, TEST2/backtests/5m_failed/python/학습형엔진_original_PLACEHOLDER.txt로 자리만 만들어 두었습니다. 원본 파일을 업로드/붙여넣기 해주면 동일 폴더에 학습형엔진_original.py로 그대로 커밋할 수 있습니다.
