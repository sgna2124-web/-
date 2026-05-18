# short_main v9 재현 노트

## 핵심 목적

이 폴더의 목적은 처음 보는 사람이 `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`을 다시 재현할 수 있도록 하는 것이다.

이 기준선은 단순히 진입 조건만 복사해서는 재현되지 않는다. 반드시 동일한 actual bar engine 순서를 사용해야 한다.

## 공식 기준선

- strategy: `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`
- baseline_version: `short_main/v9`
- source_candidate: `SM23_D02_wick120_dev03475_timeout215`
- parent_strategy: `short_main_v8_wick125_actual_bar_engine`
- previous_baseline: `short_main/v8`
- official_cd_value: `1233.487844954492`

## 공식 결과가 나온 개발 파일

- runner: `short_main_v8_combo_dev_v2_3_ultralite.py`
- result_dir: `local_results/short_main/SHORT_MAIN_V8_COMBO_DEV_V2_3_ULTRALITE`
- result_file: `summary_full.csv`
- selected_row: `SM23_D02_wick120_dev03475_timeout215`

## 재현에 반드시 필요한 조건

1. 2025년까지의 train 데이터만 사용한다.

- train_end: `2025-12-31 23:59:59`
- holdout_start: `2026-01-01 00:00:00`
- 2026년 이후 데이터는 지표 계산 전부터 제거한다.

2. CSV 597개를 사용한다.

- csv_files: 597
- loaded_symbols: 597
- load_errors: 0

3. actual bar engine을 사용한다.

- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 같은 timestamp의 신규 진입에 사용하지 않는다.
- t close 신호는 t+1 open pending entry로 등록한다.
- same-bar TP/SL은 허용한다.
- DD brake는 drawdown edge 발생 다음 timestamp부터 적용한다.
- train 마지막 active position은 마지막 close로 forced_end 청산한다.

4. 자산/수수료 설정을 고정한다.

- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004

5. v9 진입/청산 조건을 사용한다.

v8 대비 변경값은 3개다.

- short_wick_mult: 1.20
- short_dev: 0.03475
- timeout_bars: 215

나머지는 v8과 동일하다.

## 공식 재현 목표값

정상 재현이면 다음 값이 나와야 한다.

- trades: 36,791
- wins: 5,171
- losses: 31,620
- win_rate_pct: 14.055067815498356
- final_asset: 1294.9206565723089
- final_return_pct: 1194.9206565723089
- peak_asset: 1295.2759019740386
- max_return_pct: 1195.2759019740386
- max_drawdown_pct: 4.770262221769094
- official_cd_value: 1233.487844954492
- profit_factor: 1.5698636647889879
- max_conc: 287
- same_bar_trades: 3,354
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 56
- generated_entry_candidates: 36,847
- executed_entries: 36,791
- load_errors: 0

## 재현 실패 시 우선 확인할 것

1. 2026년 데이터를 지표 계산 후에 자르지 않았는가?

반드시 지표 계산 전에 `date <= 2025-12-31 23:59:59`로 잘라야 한다.

2. 같은 timestamp에서 청산 자금을 즉시 재진입에 사용하고 있지 않은가?

이 오류가 있으면 거래 수와 수익률이 크게 달라진다.

3. 신호 캔들 close에서 바로 진입하지 않았는가?

신호는 t close에서 확정되고 실제 진입은 t+1 open이다.

4. v9 변경값 3개를 정확히 반영했는가?

- short_wick_mult = 1.20
- short_dev = 0.03475
- timeout_bars = 215

5. score gate를 portfolio 단계에서 따로 걸고 있지 않은가?

`score_min_short >= 2.35`는 entry mask 내부에 들어가야 한다.

6. RSI direct gate를 켜지 않았는가?

`use_rsi_gate`는 false다. RSI는 score 내부에서만 사용한다.

7. forced_end 청산을 빼먹지 않았는가?

train 마지막 active position은 마지막 close로 강제 정산해야 한다.

8. 같은 timestamp 후보의 notional 계산 방식이 달라지지 않았는가?

같은 timestamp에 진입하는 후보들은 동일 equity snapshot 기준으로 각각 1% notional을 배정한다.

## 다음 개발 기준

앞으로 short_main 개선은 v9을 기준으로 한다.

권장 다음 실험:

- wick 주변값: 1.175 / 1.20 / 1.2125 / 1.225
- dev 주변값: 0.0345 / 0.03475 / 0.0350
- timeout 주변값: 210 / 215 / 220
- MDD 방어형: v9 + dd00285, v9 + wick12125, v9 + timeout220

단, 다음 실험도 반드시 v9 actual bar engine과 2025 train only 조건을 유지해야 한다.
