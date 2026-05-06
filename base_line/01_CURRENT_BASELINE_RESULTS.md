현재 기준선 결과 기록

작성 목적
현재 데이터 기준으로 재현된 기준선 결과를 보존한다. 이후 전략 개선, clone audit, baseline gate, 기준선 승격 여부 판단의 기준 자료로 사용한다.

공식 성과 계산
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)

실행 환경
launch_cwd: C:\Users\user\Desktop\LCD\파이썬
data_dir: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
csv_file_count: 597
initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
외부 runner import: 없음
외부 json config 참조: 없음

1. short_max 기준선
전략명: short_only_reference_1x
축: short_max
엔진 계열: v42 rr60 t200 short_only reference 계열 내장 복원
실행 코드: base_line/restore_original_short_baselines_embedded_v2.py

현재 597 CSV 기준 결과
trades: 36834
final_return_pct: 408.6547709998406
max_return_pct: 408.9954916988155
max_drawdown_pct: 7.395550425783604
official_cd_value: 471.3524734452645
win_rate: 0.1471466579790411
pf: 1.4013066651299806
max_conc: 294
max_conc_unique_symbols: 294
same_bar_trades: 3766
active_leftover: 0

기존 reference 결과
trades: 36505
max_return_pct: 394.614496
max_drawdown_pct: 7.779240
official_cd_value: 456.137449

차이
trade_diff: +329
trade_ratio: 1.0090124640460212
max_return_diff_pct: +14.380995698815525
mdd_diff_pct: -0.3836895742163957
판단: 현재 데이터 기준 결과가 기존 reference보다 좋다.

2. short_main 기준선
전략명: short_beh_dd_brake
축: short_main
엔진 계열: v52 short_only_behavioral_guards 계열 내장 복원
실행 코드: base_line/restore_original_short_baselines_embedded_v2.py

현재 597 CSV 기준 결과
trades: 28308
final_return_pct: 322.48410704162137
max_return_pct: 322.7577232826396
max_drawdown_pct: 4.4066222161057595
official_cd_value: 404.12838752816384
win_rate: 0.15257171117705243
pf: 1.441356672437088
max_conc: 286
max_conc_unique_symbols: 286
same_bar_trades: 3357
active_leftover: 0

기존 reference 결과
trades: 28017
max_return_pct: 311.812150
max_drawdown_pct: 4.758886
official_cd_value: 392.214469

차이
trade_diff: +291
trade_ratio: 1.0103865510225933
max_return_diff_pct: +10.9455732826396
mdd_diff_pct: -0.35226378389424085
판단: 현재 데이터 기준 결과가 기존 reference보다 좋다.

3. long_main 기존 기준선
전략명: 6V2_L01_doubleflush_core
축: long_main
기존 reference 결과
trades: 592
max_return_pct: 23.919060
max_drawdown_pct: 1.751183
official_cd_value: 121.749029
상태: 아직 원본 엔진 내장 복원 미완료. CORE_SUMMARY2 조건 및 V40 clone 전략 객체는 있으나 현재 clone 결과가 기준선과 크게 달라 원본 복원 전까지 공식 갱신 금지.

4. long_max 기존 기준선
전략명: 8V4_V51_V002_core_rare22_c1
축: long_max
기존 reference 결과
trades: 2276
max_return_pct: 44.266371
max_drawdown_pct: 6.758722
official_cd_value: 134.515867
상태: 아직 원본 엔진 내장 복원 미완료. CORE_SUMMARY2 조건 및 V40 clone 전략 객체는 있으나 현재 clone 결과가 기준선과 크게 달라 원본 복원 전까지 공식 갱신 금지.

운영 판단
현재 기준으로 short_main과 short_max는 새 기준선 후보로 승격 가능하다.
다만 기존 reference와 거래 수가 약 1% 차이 나므로, 데이터 기간 확장에 따른 차이인지 확인하기 위해 trades.csv 저장 후 tail audit을 권장한다.
