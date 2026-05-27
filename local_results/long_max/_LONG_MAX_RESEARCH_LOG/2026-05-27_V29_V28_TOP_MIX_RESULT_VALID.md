# V29 V28 TOP MIX RESULT VALID

실험 배치:
- LONG_MAX_V29_2025_V28_TOP_MIX_DEV_STANDALONE

목적:
- V28 상위 후보 조건 조합.
- 중심축: B2_FR010
- 조합 축: FR015, S135, RR800/RR825, hold/cool variants

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

runtime:
- elapsed_minutes: 41.86804902553558
- strategy_count: 15
- symbol_files: 597

시간 판정:
- 1시간 내외 목표 성공.

전체 1위:
- V29_B2_FR015
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.15
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 32
- body_atr_min: 0.48

성과:
- trades: 55919
- win_rate_pct: 75.70235519233177
- final_return_pct: 1027.8680633622162
- max_return_pct: 1028.2345486260276
- max_drawdown_pct: 0.646528687970449
- official_cd_value: 1120.9401886015664

비교:
- V28 top CD: 1004.4038112299907
- V29 top CD: 1120.9401886015664
- delta vs V28 top: +116.5363773715757
- delta vs V14: +229.9745661862399
- delta vs V35 baseline: +502.6808999547417

핵심 해석:
- B2_FR010보다 B2_FR015가 더 강함.
- 보호 시점은 2봉으로 유지.
- 보호폭은 +0.10R보다 +0.15R이 더 강함.
- stop 1.35 조합도 강했지만 B2_FR015 단독에는 미달.

상위 패턴:
- 1위: B2_FR015
- 2위: B2_FR012_S135
- 3위: B2_FR010_S135
- 4위: B2_FR012
- RR 8.0/8.25는 소폭 개선이나 top에는 미달.

다음 단계:
1. V29_B2_FR015 단독 리테스트.
2. 성공 시 long_max 기준선 v15 후보.
3. 이후 B2_FR015 주변에서 frac 0.13~0.20, stop 1.30~1.40, bars 1~2를 소수 탐색.

주의:
- 단독 리테스트 전까지 기준선 갱신 확정 금지.
