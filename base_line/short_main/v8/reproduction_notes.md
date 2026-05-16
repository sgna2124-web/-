# short_main v8 재현 노트

## 핵심 목적

이 폴더의 목적은 처음 보는 사람이 `short_main_v8_wick125_actual_bar_engine`을 다시 재현할 수 있도록 하는 것이다.

이 기준선은 단순히 진입 조건만 복사해서는 재현되지 않는다. 반드시 동일한 actual bar engine 순서를 사용해야 한다.

## 공식 기준선

- strategy: `short_main_v8_wick125_actual_bar_engine`
- baseline_version: `short_main/v8`
- source_candidate: `SM21_A05_wick125`
- parent_strategy: `short_main_v6_timeout210_actual_bar_engine`
- previous_baseline: `short_main/v7`
- official_cd_value: `1198.1725532607445`

## 공식 결과가 나온 개발 파일

- runner: `short_main_v7_actualbar_dev_v2_1_frozen_engine.py`
- result_dir: `local_results/short_main/SHORT_MAIN_V7_ACTUALBAR_DEV_V2_1_FROZEN_ENGINE`
- result_file: `summary_full.csv`
- selected_row: `SM21_A05_wick125`

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

5. v8 진입 조건을 사용한다.

v7 대비 변경값은 하나다.

- short_wick_mult: 1.25

나머지는 v7과 동일하다.

## 공식 재현 목표값

정상 재현이면 다음 값이 나와야 한다.

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
- same_bar_trades: 3,246
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 42
- generated_entry_candidates: 35,845
- executed_entries: 35,803
- load_errors: 0

## 재현 실패 시 우선 확인할 것

1. 2026년 데이터를 지표 계산 후에 자르지 않았는가?

반드시 지표 계산 전에 `date <= 2025-12-31 23:59:59`로 잘라야 한다.

2. 같은 timestamp에서 청산 자금을 즉시 재진입에 사용하고 있지 않은가?

이 오류가 있으면 거래 수와 수익률이 크게 달라진다.

3. 신호 캔들 close에서 바로 진입하지 않았는가?

신호는 t close에서 확정되고 실제 진입은 t+1 open이다.

4. score gate를 portfolio 단계에서 따로 걸고 있지 않은가?

`score_min_short >= 2.35`는 entry mask 내부에 들어가야 한다.

5. RSI direct gate를 켜지 않았는가?

`use_rsi_gate`는 false다. RSI는 score 내부에서만 사용한다.

6. forced_end 청산을 빼먹지 않았는가?

train 마지막 active position은 마지막 close로 강제 정산해야 한다.

7. 같은 timestamp 후보의 notional 계산 방식이 달라지지 않았는가?

같은 timestamp에 진입하는 후보들은 동일 equity snapshot 기준으로 각각 1% notional을 배정한다.

## 다음 개발 기준

앞으로 short_main 개선은 v8을 기준으로 한다.

권장 다음 실험:

- wick 주변값: 1.20 / 1.225 / 1.25 / 1.275
- wick125 + dev03475
- wick125 + score2375
- wick125 + dd00275_f5
- wick125 + timeout215

단, 다음 실험도 반드시 v8 actual bar engine과 2025 train only 조건을 유지해야 한다.
