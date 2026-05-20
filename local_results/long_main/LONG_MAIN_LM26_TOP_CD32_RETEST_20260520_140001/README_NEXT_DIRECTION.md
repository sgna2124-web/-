# LONG_MAIN_LM26_TOP_CD32_RETEST 결과

## 기준선 재현

- baseline_candidate: `LM26R_001_RETEST_S128_RR505_B360_H17_CD32`
- pass_frozen_reproduction_gate: `True`
- expected cd: `603.3485`
- actual cd: `603.3485179858741`
- errors: `0`

## 1위 요약

LONG_MAIN 1위: LM26R_001_RETEST_S128_RR505_B360_H17_CD32 | cd=603.3485179858741 | max_return=510.01650319972197 | mdd=1.0930827574126778 | trades=55821 | wins=22425 | losses=33396

## 판정 규칙

이번 파일은 개선 그리드가 아니라 단독 리테스트다.
대상은 V26에서 성장 결과로 확인된 `LM26_S1280_RR5050_B0360_H17_CD32` 하나다.

하드 재현 게이트에는 `max_conc`를 넣지 않는다.
`max_conc`는 별도 진단값으로 기록만 한다.

하드 게이트 대상:

- trades
- wins
- losses
- win_rate_pct
- final_return_pct
- max_return_pct
- max_drawdown_pct
- official_cd_value
- symbol_files
- errors
- ruined

전략 조건:

- entry_source: child::orig_V09_extreme_vol18::tp03
- entry_source atr_stop: 1.10
- entry_source rr_target: 3.80
- tp03_min_target_pct: 0.30
- final atr_stop: 1.28
- final rr_target: 5.05
- body_atr_min: 0.36
- max_hold_bars: 17
- cooldown_bars: 32
- fee: round trip 8bps
- position_fraction: 0.01
- data: 2025년까지 사용, 2026년 제외

공식 equity 경로는 전체 trade timestamp 정렬이 아니라 symbol 정렬 순서에 따른 pnl append 순서다.
