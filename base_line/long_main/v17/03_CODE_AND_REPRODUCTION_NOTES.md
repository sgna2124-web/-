# LONG MAIN v17 코드 및 재현 노트

실행 코드:
08_STANDALONE_FROZEN_RUNNER.py

이 파일은 압축 내장형 standalone runner다.
실행 시 내부에 포함된 리테스트 소스를 메모리에서 복원하여 실행한다.
외부 코드 파일, base_line 문서, 저장소 내부 경로를 실행 중 참조하지 않는다.

기본 실행:
python 08_STANDALONE_FROZEN_RUNNER.py

직접 데이터 경로 지정:
python 08_STANDALONE_FROZEN_RUNNER.py --data-dir ./Data/time

부하 절약:
python 08_STANDALONE_FROZEN_RUNNER.py --cooldown-ms 30

결과 폴더:
Path.cwd()/local_results/long_main/LONG_MAIN_LM26_TOP_CD32_RETEST_날짜시간

필수 출력 파일:

- baseline_audit.json
- summary_all.csv
- summary_long_main_mdd_lt5.csv
- summary_long_max_cd_rank.csv
- run_config.json
- errors.csv
- README_NEXT_DIRECTION.md

재현 게이트:

하드 게이트 포함:
- trades
- wins
- losses
- win_rate_pct
- final_return_pct
- max_return_pct
- max_drawdown_pct
- official_cd_value
- symbol_files
- errors
- ruined

하드 게이트 제외:
- max_conc

max_conc는 진단값으로만 기록한다. 최대 보유 포지션이 과도해도 이 기준선의 공식 재현 성공 여부를 막지 않는다.

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

주의:
기준선 코드를 수정하지 말고, 다음 개선 파일에서는 이 기준선 조건을 0번 exact 후보로 넣은 뒤 주변 조건을 추가, 제거, 변형한다.
