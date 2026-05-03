8V25_FAST1H 결과 및 장단점 업데이트

대상 배치
BATCH: 8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH
결과 위치: local_results/8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH/
master_summary: local_results/8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH/master_summary.txt
registry: local_results/8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH/8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH_registry.csv
strategies: local_results/8V25_TP03_FAST1H_FORCE_LOCAL_RESULTS_KEEP_DATA_CWD_NO_BASELINE_TOUCH/strategies.json

결과 요약
- ROWS: 8
- ERRORS: 0
- BASELINE_GATE: PASSED
- TOP_ANY_MDD: 없음
- TOP_MDD_UNDER_5: 없음
- 판정: no_promotion_all_improvements_invalid

기준선 확인
long_main 기준선 6V2_L01_doubleflush_core
- trades 592
- max_return_pct 23.919060
- max_drawdown_pct 1.751183
- official_cd_value 121.749029

long_max 기준선 8V4_V51_V002_core_rare22_c1
- trades 2276
- max_return_pct 44.266371
- max_drawdown_pct 6.758722
- official_cd_value 134.515867

short_main 기준선 short_beh_dd_brake
- trades 28017
- max_return_pct 311.812150
- max_drawdown_pct 4.758886
- official_cd_value 392.214469

short_max 기준선 short_only_reference_1x
- trades 36505
- max_return_pct 394.614496
- max_drawdown_pct 7.779240
- official_cd_value 456.137449

개선안 결과
1. long_main / 8V25_long_main_001_balanced_tp03_fast1h
- verdict: invalid_trade_starvation
- trades 8
- parent_trade_ratio 0.0135
- win_rate_pct 25.0
- final_return_pct -0.005949
- max_return_pct 0.0
- max_drawdown_pct 0.083090
- official_cd_value 99.916910

2. long_max / 8V25_long_max_001_mdd_clip_tp03_fast1h
- verdict: invalid_no_peak_growth
- trades 642
- parent_trade_ratio 0.2821
- win_rate_pct 34.2679
- final_return_pct -1.047539
- max_return_pct 0.0
- max_drawdown_pct 3.104331
- official_cd_value 96.895669

3. short_main / 8V25_short_main_001_stable_dd_tp03_fast1h
- verdict: invalid_trade_starvation
- trades 2
- parent_trade_ratio 0.000071
- win_rate_pct 50.0
- final_return_pct 0.028356
- max_return_pct 0.028356
- max_drawdown_pct 0.025625
- official_cd_value 100.002723

4. short_max / 8V25_short_max_001_blowoff_guard_tp03_fast1h
- verdict: invalid_trade_starvation
- trades 5
- parent_trade_ratio 0.000137
- win_rate_pct 40.0
- final_return_pct -0.025466
- max_return_pct 0.0
- max_drawdown_pct 0.132397
- official_cd_value 99.867603

장점
1. 기준선 보호 구조는 정상 작동했다.
- 8V25에서 4개 기준선은 모두 baseline gate를 통과했다.
- 직전 문제였던 baseline 훼손, cwd 강제, 데이터 루트 오인식 문제는 이번 결과에서는 재발하지 않았다.
- 따라서 wrapper 구조의 핵심 방향은 맞다. 저장소 접근 경로와 실행 위치를 분리하고, 기준선 조건을 건드리지 않는 방향은 유지한다.

2. 1시간 예산형 실험의 필요성이 명확해졌다.
- 8V24처럼 4축 50개씩 총 200개를 실행하는 방식은 실전 반복 속도가 너무 느렸다.
- 8V25는 개선안 수를 과감히 줄여 결과 확인 루프를 만들기 위한 전환점이다.
- 이후부터는 개선안 개수가 아니라 1시간 내외에 끝나는 실행량을 기준으로 설계해야 한다.

3. 실패가 빠르게 판별되었다.
- 총 4개 개선안만으로도 TP03과 추가 필터가 현재 기준선 계열의 엣지를 과도하게 죽이는 문제가 바로 드러났다.
- 이렇게 작은 배치로 실패 원인을 빠르게 확인한 것은 다음 설계에서 불필요한 대규모 낭비를 막는 데 유효하다.

단점
1. TP03 + 추가 품질 필터가 거래 기근을 만들었다.
- long_main은 trades 592에서 8로 급감했다.
- short_main은 trades 28017에서 2로 급감했다.
- short_max는 trades 36505에서 5로 급감했다.
- parent_trade_ratio가 극단적으로 낮으면 수익률, 승률, MDD가 좋아 보여도 재현성 있는 전략 후보가 아니다.

2. long_max는 거래 수는 남았지만 peak growth가 사라졌다.
- long_max 개선안은 trades 642로 완전 기근은 아니었지만 max_return_pct가 0.0이었다.
- MDD는 3.1043으로 낮아졌으나 수익 peak가 없으므로 승격 후보가 아니다.
- V51 계열에 require_lowanchor, sym_dd, hold/rr/trail 축소, 품질 필터를 동시에 넣으면 MDD는 줄지만 방향성 수익이 끊긴다.

3. short 계열에 DD 브레이크와 과열 품질 강화가 동시에 들어가면 신호가 사라진다.
- short_main/short_max는 기존 기준선이 수만 건의 거래를 만들며 큰 max_return을 낸다.
- 여기에 dev_short, rsi_short_min, post_loss, sym_dd를 동시에 강화하면 거래 수가 2~5건까지 감소한다.
- 숏 기준선은 이미 과열 포착 엣지가 큰 구조이므로, 진입 필터 강화보다 사후 손실 관리 또는 exit 쪽 조정이 우선이다.

핵심 학습
1. 기준선과 개선안의 역할을 더 엄격히 분리한다.
- 기준선 조건, base_spec, BASELINES, entry/exit 엔진, parent gate는 절대 수정하지 않는다.
- 신규 개선안만 TP03 및 추가 조건을 적용한다.

2. TP03 필터는 필수지만, 추가 필터와 동시에 강하게 결합하면 안 된다.
- TP03 자체가 최소 기대폭 필터 역할을 한다.
- 여기에 거래 품질, DD 브레이크, lowanchor, post_loss, shock guard를 동시에 올리면 거래 기근이 발생한다.
- 다음 개선안은 한 번에 하나의 축만 약하게 바꾼다.

3. 1시간 예산형 실험은 후보 탐색용이다.
- 1시간 예산형 결과만으로 공식 승격하지 않는다.
- 1시간 예산형에서 살아남은 후보만 max-bars와 데이터 범위를 단계적으로 늘려 공식 판정으로 확장한다.
- 공식 승격은 여전히 기준선 대비 MDD 5% 미만 여부, official_cd_value, max_return_pct, trades 재현성을 확인해야 한다.

다음 개선 방향
1. 8V26은 더 약한 단일축 변화로 간다.
- long_main: rr/hold/trail 중 하나만 조정하고, close_pos/vol/cooldown 동시 강화는 피한다.
- long_max: lowanchor 강제와 sym_dd 동시 적용을 피한다. V51의 거래 밀도를 최소 50% 이상 보존하는 방향으로 간다.
- short_main: dev_short/rsi_short_min 강화보다 exit/hold/trail만 약하게 조정한다.
- short_max: blowoff guard를 진입 필터로 강하게 넣지 말고, 손실 군집 이후 휴식 또는 exit 쪽으로만 약하게 적용한다.

2. parent_trade_ratio 하한을 실험 판단에 둔다.
- 기본적으로 parent_trade_ratio 0.20 미만은 후보로 보지 않는다.
- short 기준선처럼 원래 거래 수가 매우 큰 축은 0.05 미만이면 trade starvation으로 본다.
- 단, 신규 완전 다른 구조 실험에서는 별도 표기하되 공식 승격 후보로는 보지 않는다.

3. 시간 예산 기반 실행량을 기본 행동 규칙으로 고정한다.
- 앞으로 개선 파일을 만들 때 개선안 개수는 중요하지 않다.
- 목표는 1시간 내외에 백테스트 가능한 데이터 양이다.
- processed/elapsed 로그를 기준으로 다음 배치의 축 수, max-bars, 개선안 수를 역산한다.
