8V15 4AXIS PARENT PRESERVE 50 EACH STREAMSAFE 결과 및 장단점 Addendum

배치 정보
batch: 8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE
result_path: local_results/8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE/
summary_file: local_results/8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE/master_summary.txt
registry_file: local_results/8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE/8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE_registry.csv
failed_symbols_file: local_results/8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE/failed_symbols.json
strategies: 200
axis 구성: long_main 50개, long_max 50개, short_main 50개, short_max 50개
실행 에러: failed_symbols []
trade_cap: none
의도: 각 기준선 1위 전략의 기본 조건을 보존한 상태에서 조건 추가/일부 파라미터 수정/리스크 제어만 얹는 parent-preserve 개선

참조 기준선
long_main_v1: 6V2_L01_doubleflush_core | cd 121.7490287208 | baseline_trades 592
long_max_v1: 8V4_V51_V002_core_rare22_c1 | cd 134.5158668232 | baseline_trades 2276
short_main_v1: short_beh_dd_brake | cd 392.214469 | baseline_trades 28017
short_max_v1: short_only_reference_1x | cd 456.137449 | baseline_trades 36505

기준선 갱신 여부
long_main_v1: 갱신 없음
long_max_v1: 갱신 없음
short_main_v1: 갱신 없음
short_max_v1: 갱신 없음

중요 판정
8V15도 공식 후보로는 실패다.
다만 8V14와 실패 양상이 다르다.
8V14는 broad entry 재작성으로 거래수가 폭발한 overtrade collapse였다.
8V15는 parent-preserve를 의도했으나 long 축에서 parent signal reproduction에 실패하여 long_main/long_max가 전부 0트레이드가 되었다.
short 축은 거래수 폭발은 막았지만, equity가 시작 이후 의미 있게 우상향하지 못하고 max_return_pct 0.0, MDD 94~97%대로 붕괴했다.
따라서 8V15의 어떤 전략도 다음 부모 후보로 사용하지 않는다.

축별 결과

1. long_main
MDD<5 best: none
any-MDD best: none
전체 long_main 50개가 trades 0으로 출력됨.
대표 출력: 8V15_long_main_001_base_keep | trades 0 | parent_trade_ratio 0.000 | max_return_pct 0.0 | MDD 0.0 | official_cd_value 100.0
판정: invalid_zero_trade_parent_reproduction_failure

해석:
- 원본 long_main 기준선은 6V2_L01_doubleflush_core이고 baseline_trades는 592다.
- 그런데 8V15 long_main은 base_keep부터 0트레이드이므로, 원본 신호를 보존한 것이 아니라 원본 entry를 재현하지 못한 것이다.
- 0트레이드 cd 100은 실전 후보가 아니며, registry/top30 정렬에서 제외되어야 한다.

2. long_max
MDD<5 best: none
any-MDD best: none
판정: invalid_zero_trade_parent_reproduction_failure

해석:
- 원본 long_max 기준선은 8V4_V51_V002_core_rare22_c1이고 baseline_trades는 2276다.
- long_max도 후보가 출력되지 않았으므로 parent mask 재현 또는 게이트 연결이 실패한 것으로 본다.
- 다음 코드에서 long_max는 V51 원본 family의 실제 조건 또는 기존 registry/config를 직접 불러와야 한다.

3. short_main
MDD<5 best: none
any-MDD best: 8V15_short_main_024_s52_wick_guard
parent: short_beh_dd_brake
trades: 21020
parent_baseline_trades: 28017
parent_trade_ratio: 0.7502587715
win_rate_pct: 36.4557564225
final_return_pct: -46.2837590697
max_return_pct: 0.0
max_drawdown_pct: 94.3527294359
official_cd_value: 5.6472705641
판정: invalid_equity_collapse

해석:
- 거래수는 parent 대비 75% 수준으로, 8V14식 과다거래는 아니다.
- 그러나 win_rate가 36.45%로 숫자상 높아졌음에도 final_return은 -46.28%, MDD는 94.35%로 붕괴했다.
- 이 결과는 short parent의 entry 자체보다 exit/stop/target/position timing/fee 또는 equity aggregation이 원본 엔진과 다르게 구현되었을 가능성을 시사한다.
- short_beh_dd_brake는 원본 엔진에서 trades 28017, max_return_pct 311.8122, MDD 4.7589였으므로, parent-preserve라면 base_keep 후보가 최소한 유사한 equity shape을 보여야 한다.

4. short_max
MDD<5 best: none
any-MDD best: 8V15_short_max_024_s42_wick_guard
parent: short_only_reference_1x
trades: 26208
parent_baseline_trades: 36505
parent_trade_ratio: 0.7179290508
win_rate_pct: 36.3858363858
final_return_pct: -50.2850566034
max_return_pct: 0.0
max_drawdown_pct: 97.2993909322
official_cd_value: 2.7006090678
판정: invalid_equity_collapse

해석:
- 거래수는 parent 대비 71.79%로 줄었으나 수익 곡선은 완전히 붕괴했다.
- short_only_reference_1x 원본은 trades 36505, max_return_pct 394.6145, MDD 7.7792였다.
- parent-preserve라면 risk/exit가 같거나 유사할 때 최소한 방향성은 보존되어야 하는데, 8V15는 원본 엔진과의 fidelity가 깨졌다.

8V15의 구조적 장점
1. 8V14의 가장 큰 문제였던 거래수 폭발은 막았다.
2. parent_trade_ratio를 출력하도록 한 것은 유효하다.
3. failed_symbols가 []로, 실행 데이터 로딩 자체는 안정적이었다.
4. 4축 50개 구조는 실험 단위로는 계속 유효하다.

8V15의 구조적 단점
1. long 축에서 base_keep조차 0트레이드가 되어 parent 신호 재현 검증에 실패했다.
2. short 축에서 거래수는 적정 범위로 줄었지만, equity가 원본과 반대로 붕괴했다.
3. 0트레이드 전략이 cd 100으로 top30에 올라오는 정렬 오류가 있다.
4. 원본 엔진의 entry_on_next_bar_open, time_reduce, fail_fast, target/stop handling, fee_per_side, same-bar ordering 등을 완전히 복제하지 못한 상태에서 독립 엔진으로 평가한 것이 문제다.
5. parent-preserve라는 이름과 달리 base_keep 후보가 원본 parent 결과와 일치하는지 사전 검증하지 않았다.

다음 코드 생성 필수 원칙
1. parent-preserve 개선 전 반드시 parent reproduction test를 먼저 실행한다.
2. 각 축의 base_keep 후보는 원본 기준선과 유사한 trades, max_return_pct, MDD를 보여야 한다.
3. base_keep이 원본 기준선과 불일치하면 개선 후보 50개를 생성하지 말고 즉시 중단하도록 한다.
4. 0트레이드 전략은 registry/top ranking에서 제외하고 invalid_zero_trade로 별도 기록한다.
5. cd_value가 100이라도 trades 0이면 후보가 아니다.
6. long_main, long_max는 원본 조건을 수식으로 재추정하지 말고 기존 원본 코드/registry/config에서 실제 조건을 직접 가져온다.
7. short_main, short_max는 독립 재구현보다 기존 v52/v42 runner/config를 그대로 활용해 combinations만 생성하는 쪽이 더 안전하다.
8. 개선은 다음 순서로 해야 한다.
   - 원본 base config 복사
   - combinations에 50개 변형 추가
   - 원본 runner로 실행
   - 결과 summary를 기존 기준선과 비교

다음 단계 권고
가장 안전한 다음 라운드는 독립 백테스트 엔진을 새로 쓰는 방식이 아니다.
기준선별 기존 runner와 base_config를 그대로 사용하고, combinations JSON만 50개씩 생성하는 방식으로 가야 한다.

short_main은 아래 원본을 사용한다.
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
base_config: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
baseline combination: short_beh_dd_brake

short_max는 아래 원본을 사용한다.
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v42_rr60_t200_short_only_leverage10.py
base_config: experiments/base_config_json_only_timeout18_time_reduce_v42_rr60_t200_short_only_leverage10.json
baseline combination: short_only_reference_1x

long_main/long_max는 원본 재현이 먼저다.
기존 로컬 결과만 기준으로 entry를 추정하지 말고, 6V2와 8V4를 만든 실제 코드 또는 결과 registry에 들어 있는 원본 조건을 찾아서 base_keep reproduction부터 통과시킨다.

핵심 교훈
기준선 개선의 첫 단계는 좋은 아이디어 생성이 아니라 원본 기준선 재현이다.
base_keep이 원본과 맞지 않으면 그 위의 50개 변형은 모두 무효다.

다음 작업 우선순위
1순위: 기존 runner/config 기반 short_main 50개 combinations 생성
2순위: 기존 runner/config 기반 short_max 50개 combinations 생성
3순위: 6V2_L01 원본 runner/config를 찾아 long_main base_keep 재현
4순위: 8V4_V51 원본 runner/config를 찾아 long_max base_keep 재현
5순위: 이후에만 각 50개 개선 후보 생성
