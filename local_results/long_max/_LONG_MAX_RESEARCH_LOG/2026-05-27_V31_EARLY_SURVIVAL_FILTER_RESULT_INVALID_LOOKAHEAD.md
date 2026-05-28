# V31 EARLY SURVIVAL FILTER RESULT INVALID - LOOKAHEAD

실험 배치:
- LONG_MAX2_V31_2025_EARLY_SURVIVAL_FILTER_DEV_STANDALONE

목적:
- long_max2 v1 기준선 유지.
- 개선 후보에만 early survival strength filter 추가.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

표면상 전체 1위:
- V31_E1_CLOSE005
- early_check_bars: 1
- min_early_close_r: 0.05
- final_return_pct: 57405.88456788379
- max_drawdown_pct: 0.26847140759515
- official_cd_value: 57351.497710134354
- win_rate_pct: 91.79294564607348

판정:
- 공식 후보로 인정 금지.
- 룩어헤드 가능성이 매우 높음.

이유:
- early survival filter가 entry 이후 1~2봉의 high/close/cp/uwbr를 이용해 해당 trade를 사전에 필터링함.
- 실제 운용에서는 진입 시점에 아직 알 수 없는 미래 정보를 사용한 셈.
- 결과 수치가 비정상적으로 폭증함.

중요 결론:
- V31 결과는 전략 성과가 아니라 미래정보 필터 효과로 간주한다.
- long_max2 v1 기준선은 여전히 유효.
- early survival 개념 자체는 가능하지만, 구현 방식은 반드시 진입 이후 청산/관리 로직으로만 사용해야 한다.

다음 단계:
1. early survival filter를 entry pre-filter로 사용하지 않는다.
2. 같은 아이디어를 fail_fast / conditional time_reduce / delayed protection 형태로 재구현한다.
3. 예: 진입은 그대로 하고, 1봉 후 close_r < 0.05R이면 조기 청산.
4. 예: 1봉 후 close_r >= 0.05R일 때만 +0.15R protection 활성화.
5. 기준선 재현 게이트와 long_max2 v1 reference는 그대로 유지한다.
