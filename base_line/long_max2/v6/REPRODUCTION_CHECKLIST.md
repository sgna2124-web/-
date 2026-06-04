# LONG_MAX2 V6 REPRODUCTION CHECKLIST

목적:
- 처음 보는 사람과 미래의 작업자가 주관적 해석 없이 long_max2 v6를 재현하도록 한다.
- v6는 V51 상위 조건 혼합 결과와 V52 기간 감사를 통과한 최신 공식 기준선이다.
- 특히 미래의 내가 다시 와도 경로, 전략명, 수치, 실패 조건을 헷갈리지 않도록 고정한다.

공식 기준선 파일:
- base_line/long_max2/v6/official_expected.json
- base_line/long_max2/v6/REPRODUCTION_CHECKLIST.md

공식 결과 폴더:
- local_results/long_max/LONG_MAX2_V51_2025_V51_TOP_CONDITION_MIX_DEV_STANDALONE
- local_results/long_max/LONG_MAX2_V52_V52_TOP1_PERIOD_AUDIT_STANDALONE

공식 결과 파일:
- local_results/long_max/LONG_MAX2_V51_2025_V51_TOP_CONDITION_MIX_DEV_STANDALONE/v51_topmix_chron_audit_report.txt
- local_results/long_max/LONG_MAX2_V51_2025_V51_TOP_CONDITION_MIX_DEV_STANDALONE/v51_topmix_chronological_portfolio_audit.csv
- local_results/long_max/LONG_MAX2_V52_V52_TOP1_PERIOD_AUDIT_STANDALONE/v52_period_chron_audit_report.txt
- local_results/long_max/LONG_MAX2_V52_V52_TOP1_PERIOD_AUDIT_STANDALONE/v52_period_target_monthly_trade_audit.csv

공식 실행 파일:
- 권장 공식 러너명: run_long_max2_v52_v51_top1_period_audit_standalone.py
- 주의: 이 파일은 반드시 base_line/long_max2/v6/OFFICIAL_RUNNER.py로도 보관되어야 완전 재현 패키지가 된다.
- OFFICIAL_RUNNER.py가 없으면 v6는 재현 가능하지만 100점짜리 패키지는 아니다.

공식 전략명:
- LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_BASELINE_S130_RR625_B400_H17_C32__V51_C38_FR085_WEAK_M025_RR800

공식 전략 파라미터:
- side: long
- body_atr_min: 0.48
- atr_stop: 1.30
- rr_target: 8.00
- max_hold_bars: 17
- cooldown_bars: 38
- time_reduce_bars: 2
- time_reduce_to_risk_frac: 0.85
- weak_check_bars: 1
- weak_close_r: -0.25
- weak_exit_mode: tighten_be_next
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_cost_bps: 8.0

실행 범위:
- result_scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: 2026-01-01 00:00:00
- 2026년 데이터는 기준선 개발/갱신에 사용하지 않는다.

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
- v6 기준선 재현 전에 개선 후보를 먼저 평가하지 않는다.
- v6 기준선 블록을 재해석하거나 파라미터를 추측하지 않는다.

재현 순서:
1. run_long_max2_v52_v51_top1_period_audit_standalone.py 또는 base_line/long_max2/v6/OFFICIAL_RUNNER.py를 실행한다.
2. 결과 폴더가 아래 이름으로 생성되는지 확인한다.
   - LONG_MAX2_V52_V52_TOP1_PERIOD_AUDIT_STANDALONE
3. v52_period_chron_audit_report.txt를 연다.
4. baseline_reproduction_ok가 True인지 확인한다.
5. baseline_cd_expected가 618.2592886468248인지 확인한다.
6. baseline_cd_actual이 618.2592886468248인지 확인한다.
7. chron_audit_top_strategy가 V52_AUDIT_V51_TOP1_C38_FR085_WEAK_M025_RR800 계열인지 확인한다.
8. chronological_portfolio_audit_top 수치가 official_expected.json과 일치하는지 확인한다.
9. v52_period_target_monthly_trade_audit.csv에서 2025년 1월~12월이 모두 플러스인지 확인한다.

공식 성공 기준:
- baseline_reproduction_ok: True
- baseline_cd_actual: 618.2592886468248
- chron_final_return_pct: 7368.472441514601
- chron_max_return_pct: 7369.836074986842
- chron_max_drawdown_pct: 6.414126919816894
- chron_cd_value: 6990.711308434917
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0
- chron_trades: 55244
- chron_win_rate_pct: 62.902758670624856

기간 감사 성공 기준:
- 2025년 1월~12월 월별 trade-sum이 모두 플러스
- Q1 합계 약 3548.090870062308
- Q2 합계 약 3423.914719863803
- Q3 합계 약 4815.380154478314
- Q4 합계 약 7581.408113741057
- Q1~Q3 합계 약 11787.385744404425
- 결론: Q4가 가장 강하지만 Q4 단독 특이점 전략은 아님

허용 오차:
- 부동소수점 차이는 소수점 6자리 이내만 허용한다.
- trades, max_open_positions, gross_exposure는 반드시 동일해야 한다.

실패 판정:
- baseline_reproduction_ok가 False
- baseline_cd_actual이 618.2592886468248과 다름
- chron_audit_top_strategy가 V51/V52 top1 계열이 아님
- chron_cd_value가 6990.711308434917과 크게 다름
- chron_max_drawdown_pct가 6.414126919816894와 크게 다름
- errors가 0이 아님
- result_scope가 2025년까지가 아님
- 2025년 월별 수익이 특정 Q4 한 구간에만 집중되고 Q1~Q3가 무력화됨

공식 비교 기준:
- v5 chron_cd_value: 2385.3856209991263
- v5 chron_max_drawdown_pct: 6.619263071116042
- v6 chron_cd_value: 6990.711308434917
- v6 chron_max_drawdown_pct: 6.414126919816894
- delta CD vs v5: +4605.325687435791
- delta MDD vs v5: -0.205136151299148

주의:
- v6는 성과와 MDD가 개선되었지만 max gross exposure는 738%로 여전히 높다.
- 다음 개선의 핵심은 exposure 감소, portfolio-level entry throttling, 또는 FR 0.85 이상 구간의 과도한 조임 여부 검증이다.
- 기준선 갱신은 반드시 개발 배치 이후 단독/기간 감사까지 통과한 경우만 허용한다.
