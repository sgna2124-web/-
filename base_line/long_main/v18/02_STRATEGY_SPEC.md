# LONG MAIN v18 전략 명세

## 공식 전략명

`LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`

## 진입 소스

- entry_key: `child::orig_V09_extreme_vol18::tp03`
- TP03 source atr_stop: 1.10
- TP03 source rr_target: 3.80
- TP03 minimum target pct: 0.30

## 최종 필터

- body_atr_min: 0.40
- filter_name: `body_atr >= 0.40`

## 청산/리스크 파라미터

- side: long
- atr_stop: 1.30
- rr_target: 6.25
- max_hold_bars: 17
- cooldown_bars: 32
- same-bar stop/target 충돌 처리: stop first

## 비용/자금 파라미터

- round_trip_cost_bps: 8.0
- round_trip_cost_pct: 0.08
- fee interpretation: round trip 0.08%, per side 0.04%
- position_fraction: 0.01

## 데이터 범위

- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2025년까지 데이터만 사용
- symbol_files: 597

## 공식 성과

- trades: 55597
- wins: 22513
- losses: 33084
- win_rate_pct: 40.493192078709285
- final_return_pct: 525.6012732388051
- max_return_pct: 526.8003775673284
- max_drawdown_pct: 1.3626489750456883
- official_cd_value: 618.2592886468248
- max_conc: 446
- errors: 0
- ruined: false

## 장점

- 기존 LM26 기준선 대비 CD가 상승했다.
- 기존 LM26 기준선 대비 final_return과 max_return이 상승했다.
- 거래 수가 55597로 기존 55821 대비 감소해 거래 폭증이 없다.
- body_atr 0.40 강화로 신호 품질을 높인 상태에서 RR 6.25를 적용한다.

## 금지사항

- body_atr_min 0.36과 혼동하지 말 것.
- atr_stop 1.28 / rr 5.05와 혼동하지 말 것.
- cooldown 31로 바꾸지 말 것.
- round_trip_cost_bps를 4.0으로 바꾸지 말 것. 공식은 왕복 8.0 bps다.
