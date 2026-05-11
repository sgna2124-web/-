# short_max v4 superseded notice

short_max v4 기준선 `short_max_v4_combo_rsi755_timeout280`은 short_max 전용 개발 결과 기준으로는 당시 1위였지만, 이후 short_main v4 개발에서 발견된 `SM16_C05_remove_no_rsi_dev035`가 short_max 계산 기준인 official_cd_value에서 더 높은 성과를 기록했기 때문에 short_max v5로 대체되었다.

## v4 기준선

- strategy: short_max_v4_combo_rsi755_timeout280
- trades: 36,430
- max_return_pct: 536.5429980399269
- max_drawdown_pct: 6.373508371397563
- official_cd_value: 595.9728767723071

## 새 v5 기준선

- strategy: SM16_C05_remove_no_rsi_dev035
- short_max record name: short_max_v5_SM16_C05_remove_no_rsi_dev035
- trades: 31,798
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361

## 교체 이유

short_max 기준은 official_cd_value 1위다. v5는 v4보다 official_cd_value가 +282.880288184129 높고, MDD도 더 낮다.

따라서 앞으로 short_max 개발의 부모 기준선은 `base_line/short_max/v5`의 `SM16_C05_remove_no_rsi_dev035`를 사용한다.

v4는 계보 추적용으로만 남긴다.
