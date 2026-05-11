# short_main v4 superseded by v5

short_main v4 기준선 `SM16_C05_remove_no_rsi_dev035`는 원본 결과행 기준으로 기록되어 있었다.

이후 같은 전략을 exact-entry-mask + edge_current dd_brake 방식으로 단독 리테스트했고, 더 높은 성과가 완전히 재현되었다.

## v4

- strategy: SM16_C05_remove_no_rsi_dev035
- trades: 31,798
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361

## v5

- strategy: SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge
- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

## 교체 이유

v5는 MDD 5% 미만을 유지하면서 official_cd_value가 기존 v4보다 +74.6113206547623 높다. 따라서 앞으로 short_main 개발 기준선은 `base_line/short_main/v5`를 사용한다.
