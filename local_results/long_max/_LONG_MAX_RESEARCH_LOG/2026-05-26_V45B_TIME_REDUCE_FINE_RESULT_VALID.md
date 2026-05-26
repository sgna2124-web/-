# V45B TIME REDUCE FINE RESULT VALID

실험 배치:
- LONG_MAX_V26B_2025_TIME_REDUCE_FINE_DEV_V45_FIXED_LOW_MEM_STANDALONE

수정 목적:
- V45에서 발생한 memory error 22개 제거.
- 사용하지 않는 V42/V43 trend/pullback feature 계산 제거.
- baseline reproduction 복구.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

runtime:
- elapsed_minutes: 57.49058713912964
- strategy_count: 16
- symbol_files: 597

시간 판정:
- 1시간 내외 목표 달성.
- 16개 후보 기준 약 57.5분.
- 현재 환경에서 time_reduce 계열은 후보 16개 내외가 적정.

전체 1위:
- V45B_TR_B3_FR010
- time_reduce_bars: 3
- time_reduce_to_risk_frac: 0.10
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 32
- body_atr_min: 0.48

성과:
- trades: 55776
- win_rate_pct: 67.89658634538152
- final_return_pct: 796.3586309471458
- max_return_pct: 796.9146790906065
- max_drawdown_pct: 0.6632801105799446
- official_cd_value: 890.9656224153265

비교:
- V44 top CD: 754.1161469801397
- V45B top CD: 890.9656224153265
- delta vs V44 top: +136.8494754351868
- delta vs V35 baseline: +272.70633376850174

핵심 결론:
- V45B는 유효한 개선 결과.
- time_reduce 3봉 후 +0.10R stop 보호가 현재 최강 후보.
- win_rate가 67.9%로 상승하면서 MDD도 0.663%로 감소.
- 기존 reversal entry + early positive stop protection 구조가 long_max에 매우 강하게 작동.

다음 단계:
1. V45B_TR_B3_FR010 단독 리테스트.
2. 리테스트 성공 시 long_max 기준선 갱신 후보.
3. 이후 B3_FR010 주변에서 frac 0.08~0.15, bars 2~4, RR 7.50~8.25 소수 탐색.

주의:
- V45 invalid 결과는 공식 후보로 사용 금지.
- V45B 결과만 공식 후보로 취급.
