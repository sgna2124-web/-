# LONG MAX v12 재현 노트

실행 코드: 08_STANDALONE_FROZEN_RUNNER.py

기본 실행:
python 08_STANDALONE_FROZEN_RUNNER.py

직접 데이터 경로 지정:
python 08_STANDALONE_FROZEN_RUNNER.py --data-dir ./Data/time

부하 절약:
python 08_STANDALONE_FROZEN_RUNNER.py --cooldown-ms 30

결과 폴더:
Path.cwd()/local_results/long_max

필수 출력 파일:
baseline_audit.json
summary_all.csv
summary_long_main_mdd_lt5.csv
summary_long_max_cd_rank.csv
run_config.json
errors.csv
README_NEXT_DIRECTION.md

공식 expected:
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

max_conc는 진단값이며 하드 게이트에서 제외한다.
