# long_max v11 실행 순서 및 감사 사양

long_max v11은 long_main v16과 같은 전략이다. 이 파일은 06_FULL_REPRODUCTION_SPEC와 08_STANDALONE_FROZEN_RUNNER.py를 연결하는 재현 감사 문서다.

## 1. 데이터 수집

- 데이터 폴더는 실행 인자로 받는다.
- 예시: `python 08_STANDALONE_FROZEN_RUNNER.py --data-dir ./Data/time`
- 외부 절대경로를 코드에 박지 않는다.
- 결과 폴더나 base_line 폴더를 입력으로 읽지 않는다.
- OHLCV CSV 파일만 입력으로 사용한다.
- 2025년까지의 데이터만 사용한다.
- `timestamp < 2026-01-01 00:00:00 UTC` 조건을 적용한다.
- 최종 기준 `symbol_files == 597`이어야 한다.

## 2. 파일/심볼 처리 순서

```python
for p in sorted(data_root.rglob("*.csv"), key=lambda x: str(x).lower()):
    ...

symbols = sorted({infer_symbol(p) for p in data_file_map.values()})
for symbol in symbols:
    run_symbol_backtest(symbol)
```

## 3. 전략 고정값

```text
entry_source = child::orig_V09_extreme_vol18::tp03
entry_source_atr_stop = 1.10
entry_source_rr_target = 3.80
tp03_min_target_pct = 0.30
final_entry = entry_source AND body_atr >= 0.22
final_atr_stop = 1.21
final_rr_target = 5.05
max_hold_bars = 17
cooldown_bars = 31
round_trip_cost_bps = 8.0
position_fraction = 0.01
```

## 4. trade simulation 순서

```python
next_allowed_signal_i = WARMUP_BARS
for signal_i in np.flatnonzero(final_entry):
    if signal_i < next_allowed_signal_i:
        continue
    entry_i = signal_i + 1
    if entry_i >= n:
        continue
    risk = 1.21 * atr14[signal_i]
    stop_price = open[entry_i] - risk
    target_price = open[entry_i] + risk * 5.05
    last_i = min(n - 1, entry_i + 17)
    # stop-first when same bar
    next_allowed_signal_i = exit_i + 31
```

## 5. 공식 equity 누적 순서

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

전체 trade를 timestamp 기준으로 다시 정렬하면 복리 경로가 바뀌어 공식 기준값과 달라진다.

## 6. max_conc

max_conc는 equity 누적 순서와 별도로 entry/exit 이벤트를 timestamp로 정렬해서 계산한다.

```python
events.append((entry_ts, +1))
events.append((exit_ts, -1))
events.sort(key=lambda x: (x[0], x[1]))
```

동일 timestamp에서는 exit(-1)이 entry(+1)보다 먼저 처리된다.

## 7. 감사 파일

08_STANDALONE_FROZEN_RUNNER.py 실행 결과 폴더에는 다음 파일이 있어야 한다.

```text
baseline_audit.json
summary_all.csv
summary_long_max_cd_rank.csv
summary_long_main_mdd_lt5.csv
run_config.json
errors.csv
README_REPRODUCTION_RESULT.md
```

## 8. 공식 재현 판정

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

## 9. long_max 갱신 판정

다음 long_max 기준선은 아래 조건을 모두 만족해야 한다.

1. 기준선 exact 재현 성공
2. errors 0
3. ruined false
4. official_cd_value > 547.2610302171641
5. 단독 리테스트 재현 성공
6. base_line/long_max 다음 버전에 00~08 파일 기록

## 10. 처음 보는 사람이 가장 자주 틀릴 지점

1. TP03 source를 final 1.21/5.05로 재계산하는 것
2. body_atr >= 0.22를 raw signal 안에 넣는 것
3. signal_i에서 바로 진입하는 것
4. stop/target 동시 히트 시 target 우선 처리하는 것
5. 2026년 데이터를 포함하는 것
6. 전체 trade를 timestamp 기준으로 정렬한 뒤 equity를 계산하는 것
7. cd_value를 final_return_pct 기준으로 계산하는 것
8. 수수료를 왕복 8bps로 차감하지 않는 것
9. position_fraction을 1.0으로 계산하는 것
10. symbol_files 597이 아닌 상태에서 결과를 비교하는 것
