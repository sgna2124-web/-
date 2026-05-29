# V33 NEXT-BAR MANAGEMENT RESULT - REALISTIC RULE CHECK

실험 배치:
- LONG_MAX2_V33_2025_NEXT_BAR_MANAGEMENT_DEV_STANDALONE

목적:
- V32에서 발견된 intrabar retroactive stop 문제 제거.
- j봉 종가에서 관찰된 청산/보호 조건은 j+1봉부터만 적용.
- 진입 신호는 신호봉 종가, 진입은 다음 봉 시가.
- 진입과 청산/보호 변경이 같은 판단 시점에 동시에 발생하지 않도록 수정.

기준선 게이트:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

runtime:
- elapsed_minutes: 56.79874066114426
- strategy_count: 18
- symbol_files: 597

중요 발견:
- V33에서 next-bar activation을 엄격히 적용하자 LONG_MAX2 v1 reference가 기존 공식값과 달라짐.
- 기존 공식 LONG_MAX2 v1 CD: 1120.9401886015664
- V33 next-bar rule 적용 reference CD: 970.5145716189348
- 따라서 LONG_MAX2 v1의 기존 공식 성과에는 same-bar dynamic stop activation 효과가 포함되었을 가능성이 있음.

V33 전체 1위:
- V33_WEAK_E1_CLOSE_000_BE_NEXT
- weak_check_bars: 1
- weak_close_r: 0.00
- weak_exit_mode: tighten_be_next
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.15
- final_return_pct: 998.5993537197343
- max_drawdown_pct: 0.5592519919746852
- official_cd_value: 1092.9450669668074

비교:
- V33 realistic reference CD: 970.5145716189348
- V33 top CD: 1092.9450669668074
- improvement vs realistic reference: +122.4304953478726
- 하지만 기존 long_max2 v1 공식 CD 1120.9401886015664에는 미달.

판정:
- 기존 long_max2 v1 기준선은 실전 체결 원칙 기준으로 재검토 필요.
- V33 top은 realistic next-bar rule 내부에서는 개선 후보.
- 그러나 기존 long_max2 v1 공식 기준선과 직접 비교하면 갱신 후보 아님.

핵심 결론:
1. 실제 체결 원칙에서는 stop/protection 변경은 다음 봉부터 유효해야 한다.
2. 이 규칙을 적용하면 기존 long_max2 v1 성과가 하락한다.
3. 그래도 next-bar rule 환경에서 weak E1 close<0 tighten_be_next는 reference보다 개선된다.
4. 앞으로의 공식 기준선은 realistic next-bar rule을 명시해야 한다.

다음 단계:
- long_max2 v1을 그대로 공식 유지할지, realistic-rule 기준으로 long_max2 v2를 새로 잡을지 결정 필요.
- 새로 잡는다면 V33_REF 또는 V33_WEAK_E1_CLOSE_000_BE_NEXT를 단독 리테스트해야 함.
