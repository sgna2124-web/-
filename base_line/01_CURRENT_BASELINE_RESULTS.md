현재 기준선 결과 기록

공식 성과 계산
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)

공식 체결/청산 엔진
숏 계열 기준선은 actual bar engine 기준을 사용한다.

5분봉 timestamp가 12:00이면 해당 캔들은 12:00:00 ~ 12:04:59 구간이다. 따라서 12:00 캔들 내부에서 발생한 TP/SL 청산 결과는 12:00 open 신규 진입 판단에 사용할 수 없다.

공식 처리 규칙:
- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- same-bar TP/SL은 유지한다.
- same-bar에서 stop과 target이 동시에 닿으면 stop 우선으로 처리한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

실행 환경
- data_dir: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
- csv_file_count: 597
- initial_asset: 100.0
- position_fraction: 0.01
- leverage: 1.0
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- 외부 json config 참조: 없음

데이터 분리
- 기본 train end: 2025-12-31 23:59:59
- holdout start: 2026-01-01 00:00:00
- 기준선 산출은 기본적으로 2025까지를 우선한다.
- 별도 검증 파일에서는 2026 포함 전체 결과도 기록할 수 있다.

1. short_max 현재 기준선
전략명: smv12_topmix2_07_mix2_07_top1_reduce_frac000
축: short_max
기준선 버전: base_line/short_max/v13
이전 기준선: base_line/short_max/v12
선택 기준: short_max식, 기존 v12보다 official_cd_value가 높고 MDD가 낮음
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max/v13

2025 train 기준 공식 단독 리테스트 결과
trades: 66572
wins: 5664
losses: 60908
win_rate_pct: 8.508081475695487
final_return_pct: 6864.507074601753
max_return_pct: 6864.507074601753
max_drawdown_pct: 3.2701695697124222
official_cd_value: 6736.755883567657
profit_factor: 2.190937542731158
max_conc: 305
same_bar_trades: 3524

판단: short_max 공식 기준선으로 유지한다. 이후 short_max 개선은 v13 기준으로 한다.

2. short_main2 현재 기준선
전략명: SM60_C03_stop240_score270_timeout315
축: short_main2
기준선 버전: base_line/short_main2/v2
이전 기준선: base_line/short_main2/v1
선택 기준: short_main2 v1 진입 조건 유지 + 청산/방어 파라미터 변형 + 단독 리테스트 완전 재현 + Q4 의존성/실전성 점검 통과
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_main2/v2

2025 train 기준 공식 단독 리테스트 결과
trades: 152030
wins: 11364
losses: 140666
win_rate_pct: 7.4748404920081555
max_return_pct: 73746.55353592646
max_drawdown_pct: 5.888592725709996
official_cd_value: 69498.03075622236
profit_factor: 1.8286053579584032
max_conc: 364
same_bar_trades: 8883

실전성 MTM 참고 결과
mtm_close_max_drawdown_pct: 15.017466599306728
mtm_worstbar_max_drawdown_pct: 14.23277215250176
mtm_worstbar_cd_value: 63347.67993125091

판단: short_main2 공식 기준선으로 갱신한다. 이후 short_main2 개선은 v2 기준으로 한다.

3. short_max2 Q4-low 공식 기준선
전략명: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1
축: short_max2
기준선 버전: base_line/short_max2/v2
이전 기준선: base_line/short_max2/v1
선택 기준: 2025-Q4 특수 구간 저비중, pre-Q4 월평균 수익과 MDD 우선, float64 단독 리테스트 통과
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231
실행 코드/사양: base_line/short_max2/v2

2025 train 기준 공식 단독 리테스트 결과
trades: 65180
wins: 5130
losses: 60050
win_rate_pct: 7.8705124271248845
max_return_pct: 15588.585271121465
max_drawdown_pct: 2.274010039088681
official_cd_value: 15331.825267065175
profit_factor: 2.6142284817799504
positive_month_ratio_pct: 93.24324324324324
q4_share_of_full_return_pct: 77.19914436251436
top3_month_share_pct: 77.40116227608569

판단: short_max2/v2는 Q4-low 정책 기준선으로 보존한다.

4. short_max2 high-performance 기준선
전략명: SMX2V2_C08_EX20_02_N02_stop257_rr5075
축: short_max2
기준선 버전: base_line/short_max2/v3_highperf_N02
이전 참조 기준선: base_line/short_max2/v2
선택 기준: combo08 v3 high-performance 확장형 중 N02 단독 리테스트 통과, 2023~2025 연도별 플러스, all-through-2026 결과 플러스
엔진: actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231_FAST_SIGNAL_PRECOMPUTE_CHUNKED_MEMSAFE
실행 코드/사양: base_line/short_max2/v3_highperf_N02
결과 출처: local_results/short_max/short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3_results

핵심 파라미터
short_dev: 0.032
short_wick_mult: 1.30
score_min_short: 2.35
atr_stop_mult: 2.57
rr_mult: 5.075
timeout_bars: 320
fail_fast_bars: 12
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4

2025 frozen gate 결과
PRE-Q4:
trades: 88892
final_return_pct: 5636.697084804827
max_drawdown_pct: 5.655961392725716
official_cd_value: 5412.231712470644
profit_factor: 1.9410396856986845

FULL 2025:
trades: 104753
final_return_pct: 19461.28974837902
max_drawdown_pct: 5.655961392725716
official_cd_value: 18454.91075229149
profit_factor: 2.0040638913290496

2026 포함 전체 결과
trades: 106337
final_return_pct: 20964.787242703645
max_drawdown_pct: 5.655961392725716
official_cd_value: 19873.371008796516
profit_factor: 2.0010696725618833

연도별 분리 결과
2023_FULL_ONLY: return 58.13785276936261, MDD 1.9196538272639008, CD 155.1021534263226, PF 1.8189380113743816
2024_FULL_ONLY: return 134.59296305171026, MDD 1.822985917841291, CD 230.31636637103094, PF 1.9135547532977255
2025_FULL_ONLY: return 1529.7313609927087, MDD 5.655961392725628, CD 1537.5543844098192, PF 2.098346033746182
2026_FULL_ONLY: return 7.8345965695261865, MDD 1.1085064239765963, CD 106.63924313928375, PF 2.024525285956021

판단
- short_max2/v3_highperf_N02는 v2 Q4-low 기준선을 대체하는 단일 공식 기준선이 아니라 별도 high-performance branch다.
- 2023, 2024, 2025 모두 플러스이며 2025에서 강한 확장이 발생했다.
- 2026은 저활동 플러스 구간으로 기록한다.
- 이후 short_max2 고성과 개선은 v3_highperf_N02를 기준으로 진행할 수 있다.
