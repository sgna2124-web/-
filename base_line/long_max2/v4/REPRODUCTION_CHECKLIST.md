# LONG_MAX2 V4 REPRODUCTION CHECKLIST

목적:
- 처음 보는 사람과 미래의 작업자가 주관적 해석 없이 long_max2 v4를 재현하도록 한다.
- v4는 V46 단독 리테스트를 통과한 최신 공식 실전 기준선이다.
- 이 문서는 official_expected.json과 함께 재현 절차 및 실패 판정을 고정한다.

공식 실행 파일:
- run_long_max2_v46_v45_top1_retest_standalone.py

공식 결과 폴더:
- local_results/long_max/LONG_MAX2_V46_2025_V46_TOP1_RETEST_STANDALONE

필수 결과 파일:
- v46_retest_chron_audit_report.txt
- v46_retest_chronological_portfolio_audit.csv
- v46_retest_trade_list_results.csv
- run_meta.json

공식 기준선 파일:
- base_line/long_max2/v4/official_expected.json
- base_line/long_max2/v4/REPRODUCTION_CHECKLIST.md

실행 범위:
- result_scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: 2026-01-01 00:00:00
- 2026년 데이터는 기준선 개발/갱신에 사용하지 않는다.

공식 전략명:
- LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_BASELINE_S130_RR625_B400_H17_C32__V46_RETEST_V45_TOP1_C38_FR035_WEAK_M010

핵심 조건:
- side: long
- body_atr_min: 0.48
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 38
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.35
- weak_check_bars: 1
- weak_close_r: -0.10
- weak_exit_mode: tighten_be_next
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_cost_bps: 8.0

실전 체결 원칙:
- signal_timing: signal candle close
- entry_timing: next candle open
- management_observation: bar close only
- management_activation: next bar only
- no_future_entry_filter: true
- no_same_bar_retroactive_stop: true
- same_bar_stop_target_collision: stop first

절대 금지:
- 신호봉 내부 고가/저가를 보고 진입 여부를 고르지 않는다.
- 신호봉 종가 조건 성립 후 같은 봉에서 stop/target을 소급 적용하지 않는다.
- 관리 조건이 종가에서 확인되었다고 같은 봉에 즉시 적용하지 않는다.
- trade-list MDD를 공식 실전 MDD로 사용하지 않는다.
- 2026년 데이터를 기준선 갱신에 섞지 않는다.
- v4 기준선 재현 전에 개선 후보를 먼저 평가하지 않는다.

재현 순서:
1. run_long_max2_v46_v45_top1_retest_standalone.py를 실행한다.
2. 결과 폴더가 아래 이름으로 생성되는지 확인한다.
   - LONG_MAX2_V46_2025_V46_TOP1_RETEST_STANDALONE
3. v46_retest_chron_audit_report.txt를 연다.
4. baseline_reproduction_ok가 True인지 확인한다.
5. baseline_cd_expected가 618.2592886468248인지 확인한다.
6. baseline_cd_actual이 618.2592886468248인지 확인한다.
7. chron_audit_top_strategy가 V46_RETEST_V45_TOP1_C38_FR035_WEAK_M010 계열인지 확인한다.
8. chronological_portfolio_audit_top 수치가 official_expected.json과 일치하는지 확인한다.

공식 성공 기준:
- baseline_reproduction_ok: True
- baseline_cd_actual: 618.2592886468248
- chron_final_return_pct: 1354.9732560631458
- chron_max_return_pct: 1355.238912828799
- chron_max_drawdown_pct: 8.518206175003654
- chron_cd_value: 1331.2786618951602
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0
- chron_trades: 55155
- chron_win_rate_pct: 59.03907170700753

허용 오차:
- 부동소수점 차이는 소수점 6자리 이내만 허용한다.
- trades, max_open_positions, gross_exposure는 반드시 동일해야 한다.

실패 판정:
- baseline_reproduction_ok가 False
- baseline_cd_actual이 618.2592886468248과 다름
- chron_audit_top_strategy가 V46_RETEST_V45_TOP1_C38_FR035_WEAK_M010 계열이 아님
- chron_cd_value가 1331.2786618951602와 크게 다름
- chron_max_drawdown_pct가 8.518206175003654와 크게 다름
- errors가 0이 아님
- result_scope가 2025년까지가 아님

공식 비교 기준:
- v3 chron_cd_value: 1108.5166462173966
- v3 chron_max_drawdown_pct: 9.525300865204432
- v4 chron_cd_value: 1331.2786618951602
- v4 chron_max_drawdown_pct: 8.518206175003654
- delta CD vs v3: +222.76201567776356
- delta MDD vs v3: -1.007094690200778

주의:
- v4는 CD와 MDD가 개선되었지만 max gross exposure는 738%로 여전히 높다.
- 다음 개선의 핵심은 exposure 감소, portfolio-level entry throttling, 또는 time_reduce_to_risk_frac 0.35 이상 구간 검증이다.
- 기준선 갱신은 반드시 개발 배치 이후 단독 리테스트까지 통과한 경우만 허용한다.
