# long_main v16 실행 순서 및 감사 사양

이 파일은 06_FULL_REPRODUCTION_SPEC를 보완한다. 전략 조건은 이미 06에 고정되어 있으나, 처음 보는 사람이 재현할 때 흔히 틀리는 데이터 수집, 거래 정렬, 집계, 감사 파일 생성 순서를 추가로 고정한다.

## 1. 데이터 수집 범위

- 기준 데이터 폴더는 실행 인자로 받는다.
- 예시: `--data-dir ./Data/time`
- 외부 절대경로를 코드에 박지 않는다.
- 결과 폴더, base_line 폴더, local_results 폴더를 데이터 입력으로 읽지 않는다.
- CSV/parquet 등 OHLCV 파일만 입력으로 사용한다.
- 최종 기준 symbol_files는 597이어야 한다.

## 2. 파일별 처리 순서

파일 시스템 순서에 의존하지 않는다.

```python
files = sorted(discovered_files, key=lambda p: str(p).lower())
```

각 파일은 다음 순서로 처리한다.

1. 파일 읽기
2. OHLCV 컬럼 표준화
3. timestamp 정렬 및 중복 제거
4. 2026-01-01 00:00:00 UTC 미만 필터
5. feature 계산
6. entry_source 계산
7. final_entry 계산
8. symbol 내부 trade simulation
9. symbol별 error 수집

## 3. 심볼 내부 거래 시뮬레이션 순서

각 심볼 안에서는 signal index 오름차순으로만 돈다.

```python
next_allowed_signal_i = 0
for signal_i in np.flatnonzero(final_entry):
    if signal_i < next_allowed_signal_i:
        continue
    entry_i = signal_i + 1
    if entry_i >= n:
        continue
    simulate_exit(...)
    next_allowed_signal_i = exit_i + 31
```

주의:

- signal_i 캔들 close 시점에 조건이 확정된다.
- 실제 진입은 signal_i + 1 open이다.
- 청산 후 다음 진입 가능 index는 exit_i + cooldown_bars다.
- 5분봉에서 12:00 캔들에서 청산되면 그 캔들은 12:00~12:04:59 구간이므로, 새 진입은 최소 다음 캔들 조건 확정 이후가 되어야 한다. 본 엔진에서는 cooldown 규칙으로 signal index를 제어한다.

## 4. 전체 심볼 거래 집계 순서

모든 심볼의 trade를 합친 뒤, equity 계산 전에 반드시 정렬한다.

권장 정렬 키:

```python
all_trades.sort(key=lambda t: (t.entry_ts, t.exit_ts, t.symbol, t.entry_i, t.exit_i))
```

동일 timestamp 거래가 많기 때문에 정렬 키가 흔들리면 복리 곡선이 미세하게 달라질 수 있다. symbol 이름과 index까지 넣어 결정론적 순서를 고정한다.

## 5. equity 계산

정렬된 all_trades의 pnl_pct를 순서대로 반영한다.

```python
equity = 1.0
for trade in all_trades:
    equity *= 1.0 + 0.01 * trade.pnl_pct / 100.0
```

공식 수수료:

```python
pnl_pct = gross_pct - 0.08
```

## 6. max_conc 계산

max_conc는 equity 정렬과 별도로 entry/exit 이벤트로 계산한다.

```python
events.append((entry_ts, +1))
events.append((exit_ts, -1))
events.sort(key=lambda x: (x[0], x[1]))
```

동일 timestamp에서는 -1이 +1보다 먼저 처리된다.

## 7. 감사 파일 필수 생성

다음 개발/리테스트 러너는 최소한 다음 파일을 결과 폴더에 생성해야 한다.

```text
baseline_audit.json
summary_all.csv
summary_long_main_mdd_lt5.csv
summary_long_max_cd_rank.csv
run_config.json
errors.csv 또는 no_errors marker
```

baseline_audit.json 필수 항목:

```text
expected
actual
diff
pass_frozen_reproduction_gate
train_end_exclusive_utc
symbol_files
errors
round_trip_cost_bps
position_fraction
entry_source_atr_stop
entry_source_rr_target
final_atr_stop
final_rr_target
max_hold_bars
cooldown_bars
out_dir_policy
```

## 8. 공식 재현 판정

다음 조건을 모두 만족해야 재현 성공이다.

```text
trades == 56551
wins == 21969
losses == 34582
abs(max_return_pct - 455.0171719748199) <= 1e-6
abs(max_drawdown_pct - 1.3974597812998368) <= 1e-6
abs(official_cd_value - 547.2610302171641) <= 1e-6
max_conc == 445
symbol_files == 597
errors == 0
ruined == false
```

부동소수점 환경 차이를 감안해 운영상 판정 tolerance는 1e-3까지 허용할 수 있지만, 기준선 기록값은 위 값을 목표로 한다.

## 9. 처음 보는 사람이 가장 자주 틀릴 지점

1. TP03 source를 final 1.21/5.05로 재계산하는 것
2. body_atr >= 0.22를 raw signal 안에 넣는 것
3. signal_i에서 바로 진입하는 것
4. stop/target 동시 히트 시 target 우선 처리하는 것
5. 2026년 데이터를 포함하는 것
6. trade 정렬 순서를 고정하지 않는 것
7. cd_value를 final_return_pct 기준으로 계산하는 것
8. 수수료를 편도 4bps가 아니라 왕복 8bps로 차감하지 않는 것
9. position_fraction을 1.0으로 계산하는 것
10. symbol_files 597이 아닌 상태에서 결과를 비교하는 것
