# short_max v8 frozen runner spec

## source of truth

`base_line/short_max/v8/frozen_reproduce_runner.py`는 이 사양을 그대로 구현해야 한다.

현재 기준선 산출에 사용한 원본 실행 파일명은 다음과 같다.

`run_short_actual_bar_engine_train_to_20251231_v2.py`

## 실행 범위

- data_dir: 사용자가 지정하는 OHLCV CSV 폴더
- csv_files: 597
- train_end: 2025-12-31 23:59:59
- holdout_start: 2026-01-01 00:00:00
- 2026 데이터는 지표 계산 전에 제외

## strategy config

```python
strategy = {
    "strategy": "short_max_v7_devw120_actual_bar_engine",
    "axis": "short_max",
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "fee_per_side": 0.0004,
    "min_bars": 120,
    "ema_period": 20,
    "rsi_period": 14,
    "atr_period": 14,
    "short_dev": 0.035,
    "short_rsi_min": 77.0,
    "use_rsi_gate": False,
    "short_wick_mult": 1.3,
    "score_min_short": 2.35,
    "score_dev_weight": 1.2,
    "score_rsi_weight": 0.8,
    "score_wick_weight": 0.7,
    "score_dev_cap": 2.0,
    "score_rsi_cap": 2.0,
    "score_wick_cap": 2.5,
    "wick_atr_floor_mult": 0.2,
    "atr_stop_mult": 1.8975,
    "rr_mult": 5.75,
    "min_expected_tp": 0.003,
    "timeout_bars": 200,
    "time_reduce_bars": 8,
    "time_reduce_to_risk_frac": 0.05,
    "fail_fast_bars": 10,
    "fail_fast_min_progress_r": 0.1,
    "dd_brake_trigger_pct": 0.03,
    "dd_brake_freeze_steps": 5,
    "dd_brake_mode": "edge_current",
}
```

## official result gate

```python
expected = {
    "trades": 45500,
    "max_return_pct": 1424.4317435070927,
    "max_drawdown_pct": 6.104584306764704,
    "official_cd_value": 1431.3715225256192,
    "active_leftover": 0,
    "pending_leftover": 0,
    "load_errors": 0,
}
```

## required engine behavior

- pending entry first at bar open
- pending entry must be created by previous candle close
- current candle exits cannot fund same timestamp entries
- current candle close signal becomes next timestamp pending entry
- same-bar stop/target remains enabled
- DD brake edge detected after candle exits and applies from next timestamp
- forced_end close for active positions at train window end

## output files

Runner must save:

- `summary_compact.csv`
- `summary_full.csv`
- `run_metadata.json`
- `README_RESULT_INTERPRETATION.txt`

## failure policy

If official result gate fails, do not develop candidates from the result.
Fix baseline reproduction first.
