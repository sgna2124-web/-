# LONG_MAX2 V2 REPRODUCTION CHECKLIST

목적:
- long_max2 v2를 처음 보는 사람이 주관적 해석 없이 재현하도록 한다.
- v2는 실전 체결 원칙 기준 baseline이다.
- v1은 legacy same-bar activation baseline으로 취급한다.

필수 실행 결과 폴더:
- local_results/long_max/LONG_MAX2_V34_2025_REALISTIC_RULE_DUAL_RETEST_STANDALONE

필수 리테스트 파일:
- run_long_max2_v34_realistic_rule_dual_retest_standalone.py

재현 순서:
1. V34 dual retest runner를 실행한다.
2. 결과 폴더가 아래 이름으로 생성되는지 확인한다.
   - LONG_MAX2_V34_2025_REALISTIC_RULE_DUAL_RETEST_STANDALONE
3. v34_baseline_and_top_report.txt를 연다.
4. baseline_reproduction_ok가 True인지 확인한다.
5. baseline_cd_actual이 618.2592886468248인지 확인한다.
6. baseline_trades가 55597인지 확인한다.
7. errors가 0인지 확인한다.
8. top_strategy가 아래 전략인지 확인한다.
   - V34_RETEST_V33_TOP_WEAK_E1_CLOSE_000_BE_NEXT
9. top_cd_value가 1092.9450669668074인지 확인한다.
10. top_final_return_pct가 998.5993537197343인지 확인한다.
11. top_max_drawdown_pct가 0.5592519919746852인지 확인한다.

공식 후보 조건:
- entry_key: child::orig_V09_extreme_vol18::tp03
- body_atr_min: 0.48
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 32
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.15
- weak_check_bars: 1
- weak_close_r: 0.00
- weak_exit_mode: tighten_be_next

공식 성과:
- trades: 55842
- win_rate_pct: 55.683893843343725
- final_return_pct: 998.5993537197343
- max_return_pct: 999.0917595255839
- max_drawdown_pct: 0.5592519919746852
- official_cd_value: 1092.9450669668074
- errors: 0
- ruined: false

실패 판정:
- baseline_reproduction_ok가 False
- baseline_cd_actual이 618.2592886468248과 다름
- baseline_trades가 55597과 다름
- errors가 0이 아님
- top_strategy가 V34_RETEST_V33_TOP_WEAK_E1_CLOSE_000_BE_NEXT가 아님
- official_cd_value가 1092.9450669668074와 다름

주의:
- V31 결과는 미래정보 필터 문제로 공식 후보 금지.
- V32 결과는 same-bar stop 소급 문제로 공식 후보 금지.
- V33은 개발/탐색 배치이고, V34는 단독 재현 배치다.
- v2 공식 기준선은 V34 리테스트 결과만 사용한다.
