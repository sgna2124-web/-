# long_max v11 실행 순서 및 감사 사양

long_max v11은 long_main v16과 같은 전략이다. 이 파일은 재현자가 long_max 개발/리테스트에서 같은 결과를 얻도록 실행 순서와 감사 항목을 고정한다.

## 1. 데이터 수집

- 데이터 폴더는 실행 인자로 받는다.
- 외부 절대경로를 코드에 박지 않는다.
- 결과 폴더나 base_line 폴더를 입력으로 읽지 않는다.
- 2025년까지의 OHLCV 데이터만 사용한다.
- 최종 symbol_files는 597이어야 한다.

## 2. 파일 처리 순서

```python
files = sorted(discovered_files, key=lambda p: str(p).lower())
```

각 파일은 다음 순서로 처리한다.

1. OHLCV 읽기
2. 컬럼 표준화
3. timestamp 정렬/중복 제거
4. `2026-01-01 00:00:00 UTC` 미만 필터
5. feature 계산
6. entry_source 계산
7. final_entry 계산
8. trade simulation
9. error 수집

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
next_allowed_signal_i = 0
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

## 5. 전체 trade 정렬

```python
all_trades.sort(key=lambda t: (t.entry_ts, t.exit_ts, t.symbol, t.entry_i, t.exit_i))
```

정렬 순서가 흔들리면 복리 경로가 달라질 수 있으므로 반드시 고정한다.

## 6. max_conc

```python
events.append((entry_ts, +1))
events.append((exit_ts, -1))
events.sort(key=lambda x: (x[0], x[1]))
```

동일 timestamp에서는 exit(-1)을 entry(+1)보다 먼저 처리한다.

## 7. 감사 파일

long_max 개발/리테스트 결과 폴더에는 다음이 필요하다.

```text
baseline_audit.json
summary_all.csv
summary_long_max_cd_rank.csv
summary_long_main_mdd_lt5.csv
run_config.json
errors.csv 또는 no_errors marker
```

## 8. 공식 재현 판정

```text
trades == 56551
wins == 21969
losses == 34582
max_return_pct == 455.0171719748199
max_drawdown_pct == 1.3974597812998368
official_cd_value == 547.2610302171641
max_conc == 445
symbol_files == 597
errors == 0
ruined == false
```

운영상 tolerance는 1e-3까지 허용 가능하지만, 기준선 목표값은 위 값이다.

## 9. long_max 갱신 판정

다음 long_max 기준선은 아래 조건을 모두 만족해야 한다.

1. 기준선 exact 재현 성공
2. errors 0
3. ruined false
4. official_cd_value > 547.2610302171641
5. 단독 리테스트 재현 성공
6. base_line/long_max 다음 버전에 00~07 파일 기록
