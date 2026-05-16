# long_main v13 재현 체크리스트

## 실행 파일

- 권장 실행 파일: `base_line/long_main/v13/run_long_main_v13_frozen.py`
- shared core: `base_line/shared_frozen_runner_v09/runner_core.py`

참고: `06_FROZEN_BASELINE_RUNNER.py` 이름은 일부 업로드 환경에서 차단될 수 있어, 동일 기능 wrapper를 `run_long_main_v13_frozen.py`로 저장했다.

## 실행 명령

저장소 루트 또는 데이터 폴더가 탐색 가능한 위치에서 실행한다.

```bash
python base_line/long_main/v13/run_long_main_v13_frozen.py
```

데이터 경로를 직접 지정할 때:

```bash
python base_line/long_main/v13/run_long_main_v13_frozen.py --data-root "./Data/time"
```

또는 shared core를 직접 실행한다.

```bash
python base_line/shared_frozen_runner_v09/runner_core.py --axis long_main
```

## 결과 저장 위치

`./local_results/long_main/LONG_MAIN_FROZEN_BASELINE_2025_V13/`

## 확인 파일

- `frozen_baseline_aggregate_results.csv`
- `frozen_reproduction_report.json`
- `frozen_reproduction_report.txt`
- `frozen_baseline_errors.json`

## 재현 성공 기준

`frozen_reproduction_report.txt`의 첫 줄이 다음이어야 한다.

`baseline_reproduction_ok: True`

## 공식 기대값

- trades: `56697`
- wins: `20962`
- losses: `35735`
- win_rate_pct: `36.97197382577562`
- final_return_pct: `405.1480528315248`
- max_return_pct: `405.8734002703171`
- max_drawdown_pct: `1.228290350505734`
- official_cd_value: `499.6598061090216`
- max_conc: `444`
- symbol_files: `597`
- errors: `0`
- ruined: `false`

## long_main 판정 기준

- `max_drawdown_pct < 5`
- 위 조건을 만족하는 전략 중 `official_cd_value` 최대

## 주의

- 기준선 산출 데이터는 2025년까지다.
- `train_end_exclusive_utc = 2026-01-01 00:00:00`
- 결과 폴더는 `local_results`다. `local_result`가 아니다.
- 이 runner는 외부 기준선 파일을 참조하지 않는다.
