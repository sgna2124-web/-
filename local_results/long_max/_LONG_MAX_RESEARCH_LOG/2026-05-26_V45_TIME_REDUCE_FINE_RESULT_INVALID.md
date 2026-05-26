# V45 TIME REDUCE FINE RESULT INVALID

실험 배치:
- LONG_MAX_V26_2025_TIME_REDUCE_FINE_DEV_V45_STANDALONE

판정:
- 공식 기준선 갱신 불가.
- 결과 수치는 참고만 가능.

실패 사유:
1. baseline_reproduction_ok: False
2. baseline_cd_expected: 618.2592886468248
3. baseline_cd_actual: 587.5923902408401
4. baseline_trades_expected: 55597
5. baseline_trades_actual: 53576
6. top20 모든 주요 행에 errors 22 발생

runtime:
- elapsed_minutes: 70.1818540652593
- strategy_count: 16
- symbol_files: 597

시간 판정:
- 16개 후보 기준 약 70.18분.
- 1시간 목표에는 약간 초과.
- 다음 후보 수는 12~14개가 적절.

참고상 1위:
- V45_TR_B3_FR010
- time_reduce_bars: 3
- time_reduce_to_risk_frac: 0.10
- final_return_pct: 739.300067325562
- max_drawdown_pct: 0.6632801105799779
- official_cd_value: 834.2503558958178
- errors: 22

중요:
- 위 수치는 baseline reproduction 실패와 errors 22 때문에 공식 후보로 인정 금지.
- 단, B3_FR010 방향은 탐색 힌트로 유지.

다음 단계:
1. V45 코드를 수정하여 baseline reproduction true를 회복한다.
2. errors 0을 확인한다.
3. 같은 후보군 또는 B3_FR010 중심 12~14개 후보를 재실행한다.
4. V44 top CD 754.1161469801397과 비교한다.

주의:
- V45 결과를 기준선 갱신에 사용하지 않는다.
- V44_TR_B3_FR00은 여전히 유효한 최신 검증 후보다.
