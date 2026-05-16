# short_main v8 기준선

## 상태

공식 기준선 갱신 완료.

이 버전은 `short_main v7`의 actual bar engine과 핵심 위험관리 구조를 그대로 유지하면서, 진입 조건 중 `short_wick_mult`만 1.30에서 1.25로 완화한 버전이다.

완전히 새로운 전략이 아니다. v7 기준선의 진입 조건을 아주 작게 수정한 short_main 개발형 기준선이다.

## 기준선 이름

- strategy: `short_main_v8_wick125_actual_bar_engine`
- axis: `short_main`
- baseline_version: `short_main/v8`
- source_candidate: `SM21_A05_wick125`
- parent_strategy: `short_main_v6_timeout210_actual_bar_engine`
- previous_baseline: `short_main/v7`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`
- train_end: `2025-12-31 23:59:59`
- holdout_start: `2026-01-01 00:00:00`

## 공식 성과

2025-12-31 23:59:59까지의 train 구간 결과다. 2026 데이터는 검증용 holdout으로 남기며, 지표 계산 전부터 제외했다.

- trades: 35,803
- wins: 5,070
- losses: 30,733
- win_rate_pct: 14.16082451191241
- final_asset: 1255.7636213036806
- final_return_pct: 1155.7636213036806
- peak_asset: 1256.1081244457819
- max_return_pct: 1156.1081244457819
- max_drawdown_pct: 4.612307655489422
- official_cd_value: 1198.1725532607445
- profit_factor: 1.5763819188582828
- max_conc: 285
- max_conc_unique_symbols: 285
- same_bar_trades: 3,246
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 42
- generated_entry_candidates: 35,845
- executed_entries: 35,803
- load_errors: 0

## v7 기준선 대비

v7 기준선:

- strategy: `short_main_v6_timeout210_actual_bar_engine`
- trades: 35,330
- max_return_pct: 1115.0033786152128
- max_drawdown_pct: 4.607649926423363
- official_cd_value: 1159.0202763344078
- profit_factor: 1.5743323511471792
- max_conc: 284
- same_bar_trades: 3,187

v8 개선폭:

- delta_trades: +473
- delta_max_return_pct: +41.10474583056907
- delta_max_drawdown_pct: +0.004657729066058991
- delta_official_cd_value: +39.152276926336754
- delta_same_bar_trades: +59
- delta_max_conc: +1

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
- dd_brake_mode: edge_current
- runtime_external_path_reference: false
- no_candle_limit: true
- train_only_until_2025: true
- holdout_2026_reserved: true

## 핵심 파라미터

v8에서 v7 대비 바뀐 값은 하나다.

- short_wick_mult: 1.30 -> 1.25

나머지 값은 v7 기준선과 동일하다.

- ema_period: 20
- rsi_period: 14
- atr_period: 14
- short_dev: 0.035
- short_rsi_min: 77.0
- use_rsi_gate: false
- short_wick_mult: 1.25
- score_min_short: 2.35
- score_dev_weight: 1.0
- score_rsi_weight: 0.8
- score_wick_weight: 0.7
- score_dev_cap: 2.0
- score_rsi_cap: 2.0
- score_wick_cap: 2.5
- wick_atr_floor_mult: 0.2
- atr_stop_mult: 1.8975
- rr_mult: 5.75
- min_expected_tp: 0.003
- timeout_bars: 210
- time_reduce_bars: 8
- time_reduce_to_risk_frac: 0.05
- fail_fast_bars: 10
- fail_fast_min_progress_r: 0.1
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

## 실제 바 엔진 규칙

5분봉 timestamp가 `12:00`이면 해당 캔들은 `12:00:00 ~ 12:04:59` 구간이다. 따라서 `12:00` 캔들 내부의 TP/SL 청산 결과를 `12:00 open` 신규 진입 판단에 사용하면 안 된다.

공식 처리 순서:

1. `t` open에서는 `t-1` close에서 확정된 pending entry만 진입한다.
2. `t` 캔들의 high/low/close로 청산을 평가한다.
3. `t` 캔들 내부 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
4. `t` close에서 새 신호가 나오면 `t+1` open pending entry가 된다.
5. same-bar TP/SL은 허용한다.
6. DD brake는 `t` 캔들 종료 후 발생한 drawdown edge를 `t+1`부터 적용한다.
7. 백테스트 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.

## 진입 조건 요약

- close가 EMA20보다 최소 3.5% 이상 위에 있어야 한다.
- upper wick이 body의 1.25배 이상이어야 한다.
- RSI 직접 gate는 사용하지 않는다.
- RSI는 `short_score` 내부 보조 점수로만 사용한다.
- `short_score >= 2.35`를 entry mask 내부에서 만족해야 한다.
- 기대 TP 비율은 최소 0.3% 이상이어야 한다.
- 신호는 `t` close에서 확정되고, 실제 진입은 `t+1` open pending entry로 실행한다.

## 청산 조건 요약

- stop: entry + ATR14 * 1.8975
- target: entry - rr_mult * risk, rr_mult = 5.75
- time reduce: 진입 후 8봉 이상 지나고 유리한 진행이 있으면 stop을 entry + risk * 0.05 이하로 축소
- fail fast: 10봉 이상 경과, MFE가 0.1R 미만이고 close가 entry보다 위면 청산
- timeout: 210봉 경과 시 close 청산
- forced_end: train 구간 마지막 close에서 잔여 포지션 강제 정산

## 장점

- v7 기준선의 actual bar engine을 그대로 유지하므로 실전 5분봉 시간 해석이 보존된다.
- short_wick_mult만 1.25로 완화하여 완전히 새로운 전략이 아니라 v7의 연속 개선이다.
- MDD 5% 미만을 유지하면서 official_cd_value가 1159.0203에서 1198.1726으로 상승했다.
- profit_factor도 1.5743에서 1.5764로 소폭 개선됐다.
- 기준선 재현 게이트가 통과된 frozen engine 결과에서 승격된 후보라 재현 신뢰도가 높다.

## 단점과 주의사항

- MDD가 v7 대비 +0.004657729066058991%p 증가했다.
- same_bar_trades가 v7 대비 59개 증가했다.
- max_conc가 v7 대비 1 증가하여 동시 포지션 밀도가 약간 높아졌다.
- win_rate는 14.1608% 수준으로 낮다. 수익 구조는 낮은 승률과 큰 RR에 의존한다.
- 이 기준선은 2025년까지의 train 기준이다. 2026 holdout 검증은 별도로 수행해야 한다.

## 기준선 판정

short_main v8은 short_main 공식 기준선으로 승격한다.
이후 short_main 개선은 이 버전을 기준으로 한다.
