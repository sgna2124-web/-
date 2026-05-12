# short_main v5 superseded by v6

short_main v5 기준선 `SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge`는 short_main v6 `timeout210`에 의해 대체되었다.

## v5

- strategy: SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge
- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

## v6

- strategy: short_main_v6_timeout210
- trades: 33,989
- max_return_pct: 931.6464095007982
- max_drawdown_pct: 4.506694290977831
- official_cd_value: 985.153259660748

## 교체 이유

short_main 기준은 MDD 5% 미만에서 official_cd_value를 개선하는 것이다. v6는 MDD를 4.506694290977831로 낮추면서 official_cd_value를 +31.68877404954958 개선했다.

앞으로 short_main 개발 기준선은 `base_line/short_main/v6`을 사용한다.
