# V28 V14 BASELINE REFINE RESULT VALID

실험 배치:
- LONG_MAX_V28_2025_V14_BASELINE_REFINE_DEV_STANDALONE

목적:
- 새 공식 기준선 long_max v14를 기준으로 주변 조건을 정밀 개선.
- 완전히 새로운 축이 아니라 기존 v14 time_reduce 엔진을 갈고 닦는 방식.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

runtime:
- elapsed_minutes: 95.09772406021754
- strategy_count: 18
- symbol_files: 597

시간 판정:
- 1시간 목표 초과.
- 18개 후보 기준 95.1분.
- 다음 후보 수는 10~12개 수준이 적정.

전체 1위:
- V28_B2_FR010
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.10
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 32
- body_atr_min: 0.48

성과:
- trades: 55896
- win_rate_pct: 75.27372262773723
- final_return_pct: 909.1282541417137
- max_return_pct: 909.5094646389022
- max_drawdown_pct: 0.5057558732981193
- official_cd_value: 1004.4038112299907

비교:
- V14 official CD: 890.9656224153265
- V28 top CD: 1004.4038112299907
- delta vs V14: +113.4381888146642
- delta vs V35 baseline: +386.1445225831659

핵심 해석:
- time_reduce 보호 시점은 3봉보다 2봉이 더 강한 것으로 보임.
- 2봉 후 +0.10R 보호가 수익률, MDD, CD를 모두 개선.
- v14 기준선 주변 갈고 닦기 방식은 여전히 유효.

상위 패턴:
- B2_FR010이 압도적 1위.
- FR015, S135_FR010, FR012도 v14 대비 개선.
- RR 8.0/8.25는 v14보다 소폭 개선했으나 B2_FR010에는 크게 못 미침.

다음 단계:
1. V28_B2_FR010 단독 리테스트.
2. 성공 시 long_max 기준선 v15 후보.
3. 그 후 B2_FR010 주변에서 bars 1~3, frac 0.08~0.15, stop 1.25~1.35 소수 탐색.

주의:
- 단독 리테스트 전까지 기준선 갱신 확정 금지.
