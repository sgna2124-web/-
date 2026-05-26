# V44 REVERSAL EXIT STRUCTURE RESULT

실험 배치:
- LONG_MAX_V25_2025_REVERSAL_EXIT_DEV_V44_STANDALONE

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248

실행 시간:
- elapsed_minutes: 141.78131736914318
- strategy_count: 32
- symbol_files: 597

시간 판정:
- 1시간 목표 실패.
- 32개 후보 기준 약 141.8분.
- 후보 1개당 약 4.43분.
- 다음 1시간 목표는 12~14개 후보가 적절.

전체 1위:
- strategy: V44_TR_B3_FR00
- exit_profile: time_reduce
- condition: time_reduce_bars 3, time_reduce_to_risk_frac 0.0
- final_return_pct: 659.6972833137083
- max_return_pct: 660.2503360522596
- max_drawdown_pct: 0.8068643683832977
- official_cd_value: 754.1161469801397
- trades: 55725
- win_rate_pct: 24.520412741139523

기존 V38 reference:
- final_return_pct: 533.1034733807187
- max_drawdown_pct: 1.0889127793824005
- official_cd_value: 627.2845620812368

개선폭:
- CD +126.8315848989029 vs V38 reference
- final_return_pct +126.5938099329896 vs V38 reference
- MDD 개선: 1.0889 -> 0.8069

핵심 결론:
- 기존 reversal entry 유지 + exit 구조 개선 방향은 강하게 유효.
- 특히 time_reduce only가 압도적으로 강함.
- fail_fast는 단독으로는 소폭 개선에 그침.
- trailing 조합은 일부 개선은 있으나 top time_reduce 단독보다 약함.

다음 단계:
- V44_TR_B3_FR00 단독 리테스트 필요.
- 후보 수 12~14개로 줄여 1시간 내외 준수.
- time_reduce_bars 2~5, risk_frac -0.05~0.10 주변을 세밀 탐색.
- V44 top을 기준선 갱신 후보로 취급하되, 단독 재검증 전까지 공식 기준선 갱신 금지.
