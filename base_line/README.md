base_line 기준선 보존 폴더

목적
이 폴더는 현재 프로젝트에서 기준선 전략을 재현하거나, 기준선 위에 개선안을 붙일 때 반드시 확인해야 하는 기준 자료를 보존한다.

저장 원칙
1. 기준선 전략명, 축, 성과, 진입 조건, 청산 조건, 환경 설정을 한곳에 모은다.
2. 기준선 복원에 필요한 코드는 가능한 한 독립 실행형으로 보존한다.
3. 외부 runner, 외부 json, 다른 scripts 경로를 실행 중 참조하지 않는 코드를 우선 보존한다.
4. 데이터 루트는 CORE_SUMMARY 기준 후보를 코드 내부에 내장하거나, 실행 로그로 명확히 출력한다.
5. 기준선 갱신 시에는 기존 기준선과 새 기준선을 구분한다.
6. 전략 개선 전에는 이 폴더의 기준선 조건과 결과를 먼저 확인한다.

현재 상태
현재 완전 코드 복원에 가장 근접한 기준선은 숏 2개다.

short_max
전략명: short_only_reference_1x
복원 코드: base_line/restore_original_short_baselines_embedded_v2.py
현재 데이터 기준 결과: trades 36834, max_return_pct 408.9954916988155, max_drawdown_pct 7.395550425783604, official_cd_value 471.3524734452645
기존 reference 결과: trades 36505, max_return_pct 394.614496, max_drawdown_pct 7.779240, official_cd_value 456.137449

short_main
전략명: short_beh_dd_brake
복원 코드: base_line/restore_original_short_baselines_embedded_v2.py
현재 데이터 기준 결과: trades 28308, max_return_pct 322.7577232826396, max_drawdown_pct 4.4066222161057595, official_cd_value 404.12838752816384
기존 reference 결과: trades 28017, max_return_pct 311.812150, max_drawdown_pct 4.758886, official_cd_value 392.214469

아직 보류 상태인 기준선
long_main: 6V2_L01_doubleflush_core
long_max: 8V4_V51_V002_core_rare22_c1
이 둘은 CORE_SUMMARY2와 V40 clone 계열에는 조건이 정리되어 있으나, 현재 숏처럼 원본 엔진 계열을 안정적으로 복원했다고 판단하지 않는다. 별도 추적 후 이 폴더에 추가해야 한다.

필수 환경 설정
position_fraction: 0.01
fee_per_side: 0.0004
왕복 수수료: 0.0008
initial_asset: 100.0
데이터 루트 후보 우선순위: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time 포함
CSV 파일 수 기준: 현재 실행 결과 597개

기준선 갱신 판단
현재 597개 CSV 기준으로 숏 2개는 기존 reference보다 결과가 좋다. 수수료와 진입 비중이 정상 반영되었으므로, 현재 데이터 기준 공식 기준선으로 승격 가능하다.
단, 기존 reference와 약 1% 내외 거래 수 차이가 있으므로, 데이터 기간 확장에 의한 차이인지 trade tail audit으로 확인하면 더 정확하다.
