# long_main v16 실행 순서 및 감사 사양

이 파일은 06_FULL_REPRODUCTION_SPEC와 08_STANDALONE_FROZEN_RUNNER.py를 연결하는 재현 감사 문서다. 전략 조건만 맞아서는 충분하지 않다. 데이터 수집, 심볼 처리 순서, pnl 누적 순서, max_conc 계산 방식까지 같아야 공식 결과가 재현된다.

## 1. 데이터 수집 범위

- 데이터 폴더는 실행 인자로 받는다.
- 예시: `python 08_STANDALONE_FROZEN_RUNNER.py --data-dir ./Data/time`
- 외부 절대경로를 코드에 박지 않는다.
- 결과 폴더, base_line 폴더, local_results 폴더를 데이터 입력으로 읽지 않는다.
- OHLCV CSV 파일만 입력으로 사용한다.
- 2025년까지의 데이터만 사용한다.
- `timestamp < 2026-01-01 00:00:00 UTC` 조건을 적용한다.
- 최종 기준 `symbol_files == 597`이어야 한다.

## 2. 파일/심볼 처리 순서

데이터 파일은 파일 시스템 기본 순서에 의존하지 않는다.

```python
for p in sorted(data_root.rglob("*.csv"), key=lambda x: str(x).lower()):
    ...
```

이후 심볼명은 `infer_symbol(path)`로 추출하고, 실제 백테스트 처리 순서는 다음처럼 고정한다.

```python
symbols = sorted({infer_symbol(p) for p in data_file_map.values()})
for symbol in symbols:
    run_symbol_backtest(symbol)
```

## 3. 심볼 내부 거래 시뮬레이션 순서

각 심볼 안에서는 signal index 오름차순으로만 돈다.

```python
next_allowed_signal_i = WARMUP_BARS
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
- 실제 진입은 `signal_i + 1` open이다.
- stop/target이 같은 캔들에서 동시에 닿으면 stop 우선이다.
- 청산 후 다음 진입 가능 signal index는 `exit_i + cooldown_bars`다.
- 5분봉에서 12:00 캔들에서 청산되면 그 캔들은 12:00~12:04:59 구간이므로, 새 진입은 최소 다음 캔들 조건 확정 이후가 되어야 한다. 본 엔진에서는 cooldown 규칙으로 signal index를 제어한다.

## 4. 공식 equity 누적 순서

중요: 현재 기준선 기대값 547.2610302171641은 전체 trade를 timestamp로 재정렬한 값이 아니다.

공식 재현은 개발/리테스트 러너 계열과 동일하게 다음 순서를 사용한다.

1. symbols를 정렬한다.
2. 각 symbol 내부에서 signal index 오름차순으로 trade를 만든다.
3. symbol 처리 순서대로 pnl 리스트에 append한다.
4. append된 pnl 순서 그대로 equity를 누적한다.

```python
pnls = []
for symbol in sorted_symbols:
    trades = simulate_symbol(symbol)
    pnls.extend([t.pnl_pct for t in trades])

equity = 1.0
for pnl_pct in pnls:
    equity *= 1.0 + 0.01 * pnl_pct / 100.0
```

절대 주의:

```python
all_trades.sort(key=lambda t: (t.entry_ts, t.exit_ts, t.symbol, t.entry_i, t.exit_i))
```

위처럼 전체 trade를 timestamp 기준으로 다시 정렬하면 복리 경로가 바뀌어 공식 기준값과 달라진다. timestamp 정렬은 이 버전의 공식 equity 재현에 사용하지 않는다.

## 5. 수수료와 자산분할

```python
round_trip_cost_bps = 8.0
pnl_pct = gross_pct - 0.08
position_fraction = 0.01
```

수수료는 편도 4bps를 두 번 더한 왕복 8bps다. equity 반영은 거래당 총자산의 1%만 사용한다.

## 6. max_conc 계산

max_conc는 equity 누적 순서와 별도로 entry/exit 이벤트를 timestamp로 정렬해서 계산한다.

```python
events.append((entry_ts, +1))
events.append((exit_ts, -1))
events.sort(key=lambda x: (x[0], x[1]))
```

동일 timestamp에서는 exit(-1)이 entry(+1)보다 먼저 처리된다.

## 7. 감사 파일 필수 생성

08_STANDALONE_FROZEN_RUNNER.py 실행 결과 폴더에는 다음 파일이 있어야 한다.

```text
baseline_audit.json
summary_all.csv
summary_long_main_mdd_lt5.csv
summary_long_max_cd_rank.csv
run_config.json
errors.csv
README_REPRODUCTION_RESULT.md
```

baseline_audit.json 필수 항목:

```text
expected
actual
diffs
pass_frozen_reproduction_gate
symbol_files
errors
baseline_candidate
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
abs(max_return_pct - 455.0171719748199) <= 0.001
abs(max_drawdown_pct - 1.3974597812998368) <= 0.001
abs(official_cd_value - 547.2610302171641) <= 0.001
max_conc == 445
symbol_files == 597
errors == 0
ruined == false
```

## 9. 처음 보는 사람이 가장 자주 틀릴 지점

1. TP03 source를 final 1.21/5.05로 재계산하는 것
2. body_atr >= 0.22를 raw signal 안에 넣는 것
3. signal_i에서 바로 진입하는 것
4. stop/target 동시 히트 시 target 우선 처리하는 것
5. 2026년 데이터를 포함하는 것
6. 전체 trade를 timestamp 기준으로 정렬한 뒤 equity를 계산하는 것
7. cd_value를 final_return_pct 기준으로 계산하는 것
8. 수수료를 편도 4bps가 아니라 왕복 8bps로 차감하지 않는 것
9. position_fraction을 1.0으로 계산하는 것
10. symbol_files 597이 아닌 상태에서 결과를 비교하는 것
