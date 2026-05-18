# short_main v8 superseded by v9

short_main v8은 short_main v9 기준선으로 대체되었다.

## 이전 기준선

- baseline_version: `short_main/v8`
- strategy: `short_main_v8_wick125_actual_bar_engine`
- official_cd_value: `1198.1725532607445`
- max_return_pct: `1156.1081244457819`
- max_drawdown_pct: `4.612307655489422`
- trades: `35,803`

## 새 기준선

- baseline_version: `short_main/v9`
- strategy: `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`
- source_candidate: `SM23_D02_wick120_dev03475_timeout215`
- official_cd_value: `1233.487844954492`
- max_return_pct: `1195.2759019740386`
- max_drawdown_pct: `4.770262221769094`
- trades: `36,791`

## 핵심 변경

v9은 v8의 actual bar engine을 그대로 유지하고, 다음 3개 값만 변경한다.

- `short_wick_mult`: 1.25 -> 1.20
- `short_dev`: 0.035 -> 0.03475
- `timeout_bars`: 210 -> 215

## 판정

이후 short_main 개선은 `base_line/short_main/v9`을 기준으로 한다.
