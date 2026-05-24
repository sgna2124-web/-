# short_max v12 재현 가이드

## 목적

처음 보는 사람이 short_max v12 공식 기준선을 주관적 해석 없이 재현하기 위한 실행 절차를 기록한다.

## 공식 기준선

- axis: short_max
- baseline_version: short_max/v12
- strategy: smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540
- 이전 기준선: short_max/v11, smv10_dev1_01_v10_stop210_rr550
- train_end: 2025-12-31 23:59:59
- holdout_start: 2026-01-01 00:00:00
- 2026 데이터는 지표 계산 전부터 제외한다.

## 필수 데이터

OHLCV 5분봉 CSV 폴더가 필요하다.
공식 재현 기준 파일 수는 597개다.

공식 실행 당시 데이터 경로 예시:

```powershell
C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
```

동일 결과를 재현하려면 같은 CSV 데이터셋이 필요하다.

## 실행 명령

저장소 루트에서 실행한다.

```powershell
python base_line/short_max/v12/frozen_reproduce_runner.py --data-dir "C:\Users\user\Desktop\LCD\파이썬\코인\Data\time"
```

작은 샘플 데이터로 코드 동작만 확인할 때는 다음 옵션을 붙일 수 있으나, 공식 기준선 재현에는 사용하지 않는다.

```powershell
--allow-small-data --no-strict-gate
```

## 정상 재현 gate 값

아래 값이 정확히 맞아야 공식 재현 성공이다.

- trades: 63863
- max_return_pct: 4220.190005886
- max_drawdown_pct: 4.260534220480682
- official_cd_value: 4136.12683229544
- active_leftover: 0
- pending_leftover: 0
- load_errors: 0

## 결과 폴더

기본 결과 폴더:

```text
base_line/short_max/v12/short_max_v12_frozen_reproduce_results
```

결과 파일에서 확인할 항목:

- summary_compact.csv
- summary_full.csv
- run_metadata.json
- BASELINE_GATE_FAILED_DO_NOT_USE.txt가 없어야 함

## 독립형 runner 원칙

short_max/v12/frozen_reproduce_runner.py는 완전 독립형 단일 파일이다.

- 외부 runner import 없음
- short_max/v11 의존성 없음
- 외부 json config 참조 없음
- 전략 파라미터, 지표 계산, 진입/청산 엔진, gate 값을 파일 내부에 모두 내장

따라서 short_max/v12 폴더만 복사해도 같은 OHLCV 데이터셋이 있으면 재현 가능해야 한다.

## 공식 환경 설정

- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- csv_files: 597
- loaded_symbols: 597
- data_scope: train_only_until_2025_12_31_end
- actual bar engine 사용

## 실제 바 엔진 규칙

- t open 진입은 t-1 close에서 만들어진 pending entry만 사용한다.
- t 캔들 내부 청산 결과는 t open 신규 진입에 사용하지 않는다.
- t 캔들 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close 신호는 t+1 open pending entry가 된다.
- same-bar TP/SL은 허용한다.
- DD brake는 t 캔들 종료 후 발생한 edge를 t+1부터 적용한다.
- train 종료 시 남은 포지션은 마지막 close로 forced_end 정산한다.

## 공식 결과 출처

- local_results/short_max/short_max_v11_top_exit_combo_fast_1h_v1_results/summary_compact.csv
- local_results/short_max/short_max_v11_top_exit_combo_fast_1h_v1_results/run_metadata.json

## 재현 실패 시 우선 확인

1. CSV 파일 수가 597개인지 확인한다.
2. data-dir가 실제 OHLCV 5분봉 폴더인지 확인한다.
3. LFS pointer CSV가 섞이지 않았는지 확인한다.
4. 2026 데이터가 지표 계산에 섞이지 않는지 확인한다.
5. fee_per_side가 0.0004인지 확인한다.
6. position_fraction이 0.01인지 확인한다.
7. BASELINE_GATE_FAILED_DO_NOT_USE.txt가 생성되었는지 확인한다.
