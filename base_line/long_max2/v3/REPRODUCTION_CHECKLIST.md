# LONG_MAX2 V3 REPRODUCTION CHECKLIST

목적:
- 처음 보는 사람과 미래의 작업자가 주관적 해석 없이 long_max2 v3를 재현하도록 한다.
- 이 문서는 official_expected.json보다 우선해서 실행/판정 절차를 명확히 안내한다.
- v3는 V43 단독 리테스트를 통과한 최신 공식 실전 기준선이다.

공식 실행 파일:
- run_long_max2_v43_v42_top1_retest_standalone.py

공식 결과 폴더:
- local_results/long_max/LONG_MAX2_V43_2025_V43_TOP1_RETEST_STANDALONE

필수 결과 파일:
- v43_retest_chron_audit_report.txt
- v43_retest_chronological_portfolio_audit.csv
- v43_retest_trade_list_results.csv
- run_meta.json

실행 범위:
- 2025년까지의 데이터만 사용한다.
- train_end_exclusive_utc: 2026-01-01 00:00:00
- 2026년 데이터는 기준선 갱신용으로 사용하지 않는다.

공식 전략명:
- LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_BASELINE_S130_RR625_B400_H17_C32__V43_RETEST_V42_TOP1_C38_FR025_WEAK_M010

핵심 조건:
- side: long
- entry_key: child::orig_V09_extreme_vol18::tp03
- body_atr_min: 0.48
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 38
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.25
- weak_check_bars: 1
- weak_close_r: -0.10
- weak_exit_mode: tighten_be_next
- position_fraction: 0.01
- fee: round_trip_cost_bps 8.0, equivalent to 0.04% per side

실전 체결 원칙:
- signal_timing: signal candle close
- entry_timing: next candle open
- management_observation: bar close only
- management_activation: next bar only
- no_future_entry_filter: true
- no_same_bar_retroactive_stop: true
- same_bar_stop_target_collision: stop first

절대 금지:
- 신호봉 내부에서 이미 발생한 고가/저가를 보고 진입 여부를 고르면 안 된다.
- 신호봉 종가에서 조건이 성립했다고 같은 봉 안에서 stop/target을 소급 적용하면 안 된다.
- 관리 조건이 종가에서 확인되었다고 같은 봉에 즉시 적용하면 안 된다.
- trade-list MDD를 공식 실전 MDD로 사용하면 안 된다.
- 2026년 데이터를 기준선 개발/갱신에 섞으면 안 된다.

재현 순서:
1. run_long_max2_v43_v42_top1_retest_standalone.py를 실행한다.
2. 결과 폴더가 아래 이름으로 생성되는지 확인한다.
   - LONG_MAX2_V43_2025_V43_TOP1_RETEST_STANDALONE
3. v43_retest_chron_audit_report.txt를 연다.
4. baseline_reproduction_ok가 True인지 확인한다.
5. baseline_cd_expected가 618.2592886468248인지 확인한다.
6. baseline_cd_actual이 618.2592886468248인지 확인한다.
7. chron_audit_top_strategy가 아래 전략인지 확인한다.
   - LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_BASELINE_S130_RR625_B400_H17_C32__V43_RETEST_V42_TOP1_C38_FR025_WEAK_M010
8. chronological_portfolio_audit_top 항목의 수치가 official expected와 일치하는지 확인한다.

공식 성공 기준:
- baseline_reproduction_ok: True
- baseline_cd_actual: 618.2592886468248
- chron_final_return_pct: 1124.9991377608462
- chron_max_drawdown_pct: 9.525300865204432
- chron_cd_value: 1108.5166462173966
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0
- chron_trades: 55105
- chron_win_rate_pct: 59.012793757372286

허용 오차:
- 정렬/부동소수점 차이를 고려해 소수점 6자리 이내는 동일로 본다.
- trades, max_open_positions, gross_exposure는 정수/고정값이므로 반드시 동일해야 한다.

실패 판정:
- baseline_reproduction_ok가 False
- baseline_cd_actual이 618.2592886468248과 다름
- chron_audit_top_strategy가 V43_RETEST_V42_TOP1_C38_FR025_WEAK_M010 계열이 아님
- chron_cd_value가 1108.5166462173966과 크게 다름
- chron_max_drawdown_pct가 9.525300865204432와 크게 다름
- errors가 0이 아님
- result_scope가 2025년까지가 아님

공식 비교 기준:
- v2 audited reference CD: 832.1846538467717
- v2 audited MDD: 16.983488215379623
- v3 audited CD: 1108.5166462173966
- v3 audited MDD: 9.525300865204432
- delta CD: +276.3319923706249
- delta MDD: -7.458187350175191

주의:
- v3는 수익률과 MDD가 크게 개선되었지만 max gross exposure는 738%로 여전히 높다.
- 다음 개선의 핵심은 exposure 감소 또는 portfolio-level entry throttling이다.
- 기준선 갱신은 반드시 개발 배치 이후 단독 리테스트까지 통과한 경우만 허용한다.
