# LONG MAIN v17 기준선

기준선 이름: LONG_MAIN_V17_LM26_S128_RR505_B360_H17_CD32

원천 후보: LM26_S1280_RR5050_B0360_H17_CD32

단독 리테스트 후보명: LM26R_001_RETEST_S128_RR505_B360_H17_CD32

검증 결과 폴더: local_results/long_main/LONG_MAIN_LM26_TOP_CD32_RETEST_20260520_140001

판정: pass_frozen_reproduction_gate = true

공식 성과:
trades 55821
wins 22425
losses 33396
win_rate_pct 40.17305315203956
final_return_pct 508.8757953955824
max_return_pct 510.01650319972197
max_drawdown_pct 1.0930827574126778
official_cd_value 603.3485179858741
symbol_files 597
errors 0
ruined false

max_conc는 리테스트에서 436으로 관측되었으나 공식 하드 게이트에서 제외한다. 진단값으로만 기록한다.

실행 파일: 08_STANDALONE_FROZEN_RUNNER.py

기본 실행: python 08_STANDALONE_FROZEN_RUNNER.py

결과 저장: Path.cwd()/local_results/long_main
