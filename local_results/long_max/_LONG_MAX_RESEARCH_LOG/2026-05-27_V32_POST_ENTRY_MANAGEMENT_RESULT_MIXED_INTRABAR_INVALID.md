# V32 POST-ENTRY MANAGEMENT RESULT - MIXED / INTRABAR INVALID

실험 배치:
- LONG_MAX2_V32_2025_POST_ENTRY_MANAGEMENT_DEV_STANDALONE

목적:
- V31의 룩어헤드 entry filter 문제를 제거.
- entry는 long_max2 v1과 동일하게 유지.
- 진입 후 실제 관찰된 1~2봉 결과로만 조기 청산/보호 강화를 시도.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- baseline_trades: 55597
- errors: 0

runtime:
- elapsed_minutes: 45.791544409592944
- strategy_count: 17
- symbol_files: 597

표면상 전체 1위:
- V32_WEAK_E1_CLOSE_000_TO_BE
- weak_check_bars: 1
- weak_close_r: 0.00
- weak_exit_mode: tighten_be
- final_return_pct: 5033.604720805917
- max_drawdown_pct: 0.20649742659751835
- official_cd_value: 5123.044943525313

판정:
- V32 top 후보는 공식 후보로 인정 금지.
- 사유: intrabar retroactive stop 적용 가능성.

문제 설명:
- weak_check_bars=1에서 1봉 종가를 확인한 뒤 BE로 stop을 상향한다.
- 그런데 현재 코드 구조에서는 같은 캔들의 low/high 판정에도 상향된 stop이 적용될 수 있다.
- 이는 실제 운용에서 1봉 종가가 닫힌 뒤에야 알 수 있는 정보를 같은 1봉 내부 low에 소급 적용하는 효과가 된다.
- 따라서 entry lookahead는 제거됐지만, intrabar lookahead/retroactive stop 문제가 남아 있다.

유효하게 볼 수 있는 부분:
- exit_close 계열은 관찰된 종가에서 즉시 청산하므로 구조적으로 더 보수적이다.
- 그러나 exit_close 계열은 long_max2 v1보다 크게 부진했다.
- long_max2 v1 reference는 그대로 유효하다.

참고 결과:
- V32_REF_LONG_MAX2_V1_B2_FR015 CD: 1120.9401886015664
- V32_WEAK_E2_CLOSE_005_TO_BE CD: 1132.4128434211902, 단 이 역시 같은 봉 stop 소급 문제 가능성 때문에 공식 후보 불가.
- strong protection 계열은 v1 reference보다 낮음.

다음 단계:
1. stop 상향/보호 강화는 반드시 다음 캔들부터 적용되게 수정한다.
2. weak/strong check가 bar j close에서 발생하면, 새 stop은 j+1부터 유효해야 한다.
3. 같은 캔들 low/high에 새 stop을 소급 적용하지 않는다.
4. V33에서 next-bar-activation 방식으로 재검증한다.

핵심 원칙:
- 진입 시 미래 정보 금지.
- 진입 후 관리에서도 관찰된 정보는 다음 체결 가능 시점부터만 적용.
- same-bar stop/target 충돌은 보수적으로 처리.
