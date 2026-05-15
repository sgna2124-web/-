# short_max v8 기준선

## 상태

공식 기준선 갱신 완료.

이 버전은 기존 `short_max v7`의 진입 조건을 유지하되, 백테스트 체결/청산 시간 처리 엔진을 실제 5분봉 운용 방식에 맞춘 `actual bar engine`으로 교체한 버전이다.

따라서 전략 조건만 보면 v7 계열의 연장선이지만, 진입/청산 처리 방식이 바뀌었으므로 새 기준선 버전 `v8`로 기록한다.

## 기준선 이름

- strategy: `short_max_v7_devw120_actual_bar_engine`
- axis: `short_max`
- baseline_version: `short_max/v8`
- source_old_strategy: `short_max_v7_devw120`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`
- holdout_start: `2026-01-01 00:00:00`

## 공식 성과

2025-12-31 23:59:59까지의 train 구간 결과다. 2026 데이터는 검증용 holdout으로 남기며, 지표 계산 전부터 제외했다.

- trades: 45,500
- wins: 6,251
- losses: 39,249
- win_rate_pct: 13.738461538461538
- final_asset: 1522.7683542126408
- final_return_pct: 1422.7683542126408
- peak_asset: 1524.4317435070927
- max_return_pct: 1424.4317435070927
- max_drawdown_pct: 6.104584306764704
- official_cd_value: 1431.3715225256192
- profit_factor: 1.4976180824186338
- max_conc: 299
- max_conc_unique_symbols: 299
- same_bar_trades: 3,786
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 205
- generated_entry_candidates: 45,705
- executed_entries: 45,500
- load_errors: 0

## 이전 구엔진 기준선 대비

이전 기준선은 같은 timestamp에서 청산 후 신규 진입이 가능했던 구엔진 결과다.

- old_engine_strategy: `short_max_v7_devw120`
- old_engine_trades: 43,681
- old_engine_max_return_pct: 1221.9746135454966
- old_engine_max_drawdown_pct: 5.6636954922983485
- old_engine_official_cd_value: 1247.1019969487918

차이:

- delta_cd_vs_old_engine: +184.2695255768274
- delta_mdd_vs_old_engine: +0.44088881446635586
- delta_trades_vs_old_engine: +1,819

## 공식 성과 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

## 핵심 환경

- csv_files: 597
- loaded_symbols: 597
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- use_rsi_gate: false
- score_min_short: 2.35
- dd_brake_mode: edge_current
- runtime_external_path_reference: false

## 핵심 파라미터

- ema_period: 20
- rsi_period: 14
- atr_period: 14
- short_dev: 0.035
- short_rsi_min: 77.0
- short_wick_mult: 1.3
- score_min_short: 2.35
- score_dev_weight: 1.2
- score_rsi_weight: 0.8
- score_wick_weight: 0.7
- score_dev_cap: 2.0
- score_rsi_cap: 2.0
- score_wick_cap: 2.5
- wick_atr_floor_mult: 0.2
- atr_stop_mult: 1.8975
- rr_mult: 5.75
- min_expected_tp: 0.003
- timeout_bars: 200
- time_reduce_bars: 8
- time_reduce_to_risk_frac: 0.05
- fail_fast_bars: 10
- fail_fast_min_progress_r: 0.1
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

## 실제 바 엔진 규칙

5분봉 timestamp가 `12:00`이면 해당 캔들은 `12:00:00 ~ 12:04:59` 구간이다.
따라서 `12:00` 캔들 내부의 TP/SL 청산 결과를 `12:00 open` 신규 진입 판단에 사용하면 안 된다.

공식 처리 순서:

1. `t` open에서는 `t-1` close에서 확정된 pending entry만 진입한다.
2. `t` 캔들의 high/low/close로 청산을 평가한다.
3. `t` 캔들 내부 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
4. `t` close에서 새 신호가 나오면 `t+1` open pending entry가 된다.
5. same-bar TP/SL은 허용한다.
6. DD brake는 `t` 캔들 종료 후 발생한 drawdown edge를 `t+1`부터 적용한다.
7. 백테스트 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.

## 진입 조건 요약

숏 맥스 v8은 v7 진입 조건을 유지한다.

- close가 EMA20보다 최소 3.5% 이상 위에 있어야 한다.
- upper wick이 body의 1.3배 이상이어야 한다.
- RSI 직접 gate는 사용하지 않는다.
- RSI는 `short_score` 내부 보조 점수로만 사용한다.
- `short_score >= 2.35`를 entry mask 내부에서 만족해야 한다.
- 기대 TP 비율은 최소 0.3% 이상이어야 한다.

## 청산 조건 요약

- stop: entry + ATR14 * 1.8975
- target: entry - rr_mult * risk, rr_mult = 5.75
- time reduce: 진입 후 8봉 이상 지나고 유리한 진행이 있으면 stop을 entry + risk * 0.05 이하로 축소
- fail fast: 10봉 이상 경과, MFE가 0.1R 미만이고 close가 entry보다 위면 청산
- timeout: 200봉 경과 시 close 청산
- forced_end: train 구간 마지막 close에서 잔여 포지션 강제 정산

## 장점

- 실제 5분봉 운용 순서에 맞춰 미래 청산 정보를 같은 timestamp 진입에 사용하지 않는다.
- 2026 데이터를 지표 계산 전부터 제외하므로 holdout leakage가 없다.
- short_max 기준인 MDD 10% 미만을 유지하면서 CD가 구엔진 기준선보다 상승했다.
- active_leftover와 pending_leftover가 모두 0이라 기준선 기록 조건을 만족한다.
- score_dev_weight 1.2로 EMA 이격 기반 과열 신호를 더 강하게 반영한다.

## 단점과 주의사항

- MDD가 구엔진 대비 0.44088881446635586%p 증가했다.
- win_rate는 13.738% 수준으로 낮다. 수익 구조는 낮은 승률과 큰 RR에 의존한다.
- 같은 조건이라도 엔진 순서가 달라지면 거래 수와 성과가 크게 달라진다.
- 이 기준선은 2025년까지의 train 기준이다. 2026 holdout 검증은 별도로 수행해야 한다.
- `strategy_code.py`만 복사해서는 재현이 부족하다. 반드시 `frozen_reproduce_runner.py` 또는 동일한 actual bar engine을 사용해야 한다.

## 재현 source of truth

- 결과 출처: `local_results/short_max/short_actual_bar_engine_train_to_20251231_v2_results/summary_compact.csv`
- 메타데이터: `local_results/short_max/short_actual_bar_engine_train_to_20251231_v2_results/run_metadata.json`
- 공식 재현 코드: `base_line/short_max/v8/frozen_reproduce_runner.py`

## 기준선 판정

short_max v8은 short_max 공식 기준선으로 승격한다.
이후 short_max 개선은 이 버전을 기준으로 한다.
