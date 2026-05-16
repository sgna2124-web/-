# short_main v7 superseded by v8

short_main v7은 short_main v8 기준선으로 대체되었다.

## 이전 기준선

- baseline_version: `short_main/v7`
- strategy: `short_main_v6_timeout210_actual_bar_engine`
- official_cd_value: `1159.0202763344078`
- max_return_pct: `1115.0033786152128`
- max_drawdown_pct: `4.607649926423363`
- trades: `35,330`

## 새 기준선

- baseline_version: `short_main/v8`
- strategy: `short_main_v8_wick125_actual_bar_engine`
- source_candidate: `SM21_A05_wick125`
- official_cd_value: `1198.1725532607445`
- max_return_pct: `1156.1081244457819`
- max_drawdown_pct: `4.612307655489422`
- trades: `35,803`

## 핵심 변경

v8은 v7의 actual bar engine을 그대로 유지하고, `short_wick_mult`만 변경한다.

- v7: `short_wick_mult = 1.30`
- v8: `short_wick_mult = 1.25`

## 판정

이후 short_main 개선은 `base_line/short_main/v8`을 기준으로 한다.
