# REMAINING_CODE_INVENTORY

아래 파일들은 이 프로젝트에서 실제로 생성되었고, test3/09_CODE_REFERENCE/ 아래에 계속 보강 업로드할 대상이다.

남은 코드 목록
- cross_sectional_isolated_reversion_v1.py
- event_scanner_ohlcv_v1.py
- event_scanner_ohlcv_v2.py
- failed_displacement_reclaim_v1.py
- market_shock_propagation_v1.py
- minor_washout_reversal_v1.py
- minor_washout_reversal_v2.py
- symbol_fit_washout_reversal_v3.py
- symbol_fit_washout_reversal_v3_fix.py
- symbol_state_washout_reversal_v4.py
- symbol_state_washout_reversal_v4_hotfix.py
- symbol_state_washout_reversal_v5_simfix.py
- threshold_scanner_v1.py

각 파일의 의미 요약
- cross_sectional_isolated_reversion_v1.py : 개별 종목 수익률을 자기 최근 변동성으로 표준화하고, 메이저 바스켓 분포 대비 고립형 극단 이상치를 평균회귀로 진입하려던 전략
- event_scanner_ohlcv_v1.py / v2.py : 사람이 이름 붙인 OHLCV 이벤트를 대량 스캔하는 탐색기. v2는 train/test와 robust score 기반으로 강화됨
- failed_displacement_reclaim_v1.py : 기존 엔진과 별개로 아이디어 원형을 단순화해 본 전략 파일
- market_shock_propagation_v1.py : 메이저 바스켓 충격 후 후행 종목 캐치업을 노린 전략
- minor_washout_reversal_v1.py / v2.py : 마이너 알트 전용 washout 반발 전략. 파일 길이/최근 상태 기반 분류를 각각 시도
- symbol_fit_washout_reversal_v3.py / v3_fix.py : 시장 상대순위가 아니라 각 종목 자체의 최근 미시구조가 washout 친화적인지를 보려 한 변형
- symbol_state_washout_reversal_v4.py / v4_hotfix.py / v5_simfix.py : 종목 배제 대신 매 캔들 상태 필터 + washout trigger 구조를 시도한 버전들
- threshold_scanner_v1.py : 연속형 피처 임계값 조합을 자동으로 스캔하는 탐색기

중요
- 위 파일들은 대부분 성과상으로는 실패 상태다.
- 하지만 후임자가 같은 흐름을 반복하지 않기 위해 반드시 참조해야 하는 실험 기록이다.
- 이후 세션에서 GitHub write를 계속 사용할 수 있으면 이 inventory의 원본 소스도 순차적으로 계속 반영한다.