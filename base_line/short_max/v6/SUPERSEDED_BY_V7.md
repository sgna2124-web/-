# short_max v6 superseded by v7

short_max v6 기준선 `SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge`는 short_max v7 `devw120`에 의해 대체되었다.

## v6

- strategy: SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge
- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

## v7

- strategy: short_max_v7_devw120
- trades: 43,681
- max_return_pct: 1221.9746135454966
- max_drawdown_pct: 5.6636954922983485
- official_cd_value: 1247.1019969487918

## 교체 이유

short_max 기준은 official_cd_value 1위다. v7은 MDD 10% 미만을 유지하면서 official_cd_value를 +293.6375113375934 개선했다.

앞으로 short_max 개발 기준선은 `base_line/short_max/v7`을 사용한다.
