8V27 결과 및 기준선 로컬 변형 규칙 보강

대상 배치
BATCH: 8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH
결과 위치: local_results/8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH/
master_summary: local_results/8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH/master_summary.txt
registry: local_results/8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH/8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH_registry.csv
strategies: local_results/8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH/strategies.json

결과 요약
- ROWS: 8
- ERRORS: 0
- BASELINE_GATE: PASSED
- TOP_ANY_MDD: 없음
- TOP_MDD_UNDER_5: 없음
- 판정: 개선안 전부 무효

기준선 확인
long_main 기준선 6V2_L01_doubleflush_core
- trades: 592
- max_return_pct: 23.919060
- max_drawdown_pct: 1.751183
- official_cd_value: 121.749029

long_max 기준선 8V4_V51_V002_core_rare22_c1
- trades: 2276
- max_return_pct: 44.266371
- max_drawdown_pct: 6.758722
- official_cd_value: 134.515867

short_main 기준선 short_beh_dd_brake
- trades: 28017
- max_return_pct: 311.812150
- max_drawdown_pct: 4.758886
- official_cd_value: 392.214469

short_max 기준선 short_only_reference_1x
- trades: 36505
- max_return_pct: 394.614496
- max_drawdown_pct: 7.779240
- official_cd_value: 456.137449

8V27 개선안별 결과
1. long_main / 8V27_long_main_001_rr_only_tp03_nocap
- verdict: invalid_trade_explosion
- trades: 13116
- baseline_trades: 592
- parent_trade_ratio: 22.155405
- win_rate_pct: 34.431229
- final_return_pct: -11.423378
- max_return_pct: 0.0
- max_drawdown_pct: 72.342441
- official_cd_value: 27.657559
- 판정: 기준선 보존형 개선이 아니라 거래 폭증. 단순 rr 조정만으로도 parent ratio가 22배가 되었으므로 현재 개선 실행 경로와 embedded 기준선 reference 사이에 구조적 차이가 있음을 의심해야 한다.

2. long_max / 8V27_long_max_001_exit_only_tp03_nocap
- verdict: invalid_trade_explosion
- trades: 434013
- baseline_trades: 2276
- parent_trade_ratio: 190.691125
- win_rate_pct: 33.630790
- final_return_pct: -98.913484
- max_return_pct: 0.0
- max_drawdown_pct: 100.0
- official_cd_value: 0.0
- 판정: 심각한 거래 폭증. hold -2 같은 exit-only 변화로 해석했지만 실제 결과는 기준선과 비교 불가능한 수준이다. V51 기준선의 rare22 구조가 개선 경로에서 기준선과 동일하게 재현되지 않을 가능성을 반드시 점검해야 한다.

3. short_main / 8V27_short_main_001_exit_only_tp03_nocap
- verdict: invalid_trade_starvation
- trades: 1032
- baseline_trades: 28017
- parent_trade_ratio: 0.036835
- win_rate_pct: 28.682171
- final_return_pct: 14.436373
- max_return_pct: 14.436373
- max_drawdown_pct: 27.952081
- official_cd_value: 82.449025
- 판정: 거래 기근. 기준선 대비 거래량이 3.7%에 불과하다. 단순 hold 조정만으로도 기준선 규모가 유지되지 않았다.

4. short_max / 8V27_short_max_001_trail_only_tp03_nocap
- verdict: invalid_trade_starvation
- trades: 3197
- baseline_trades: 36505
- parent_trade_ratio: 0.087577
- win_rate_pct: 27.869878
- final_return_pct: 46.433522
- max_return_pct: 46.433522
- max_drawdown_pct: 63.890660
- official_cd_value: 52.876179
- 판정: 거래 기근 및 MDD 악화. 기준선 대비 거래량이 8.8%에 불과하고 MDD가 63.89%로 커졌다.

장점
1. 캔들 제한 제거 규칙은 정상 반영되었다.
- 8V27은 max-bars 없이 전체 데이터 환경에서 실행되었다.
- 기준선과 비교 가능한 데이터 범위 원칙은 회복되었다.

2. 기준선 gate는 정상 통과했다.
- baseline gate 자체는 문제없이 작동했다.
- 저장소 접근 경로와 실행 cwd 분리, 결과 저장 위치 강제 규칙도 유지되었다.

3. parent_trade_ratio의 중요성이 확정되었다.
- 수익률/MDD 이전에 거래량 규모가 기준선과 너무 다르면 개선 후보가 될 수 없다는 점이 명확해졌다.

단점 및 문제 인식
1. 8V27은 기준선 로컬 변형이라고 보기 어렵다.
- long_main은 parent ratio 22배, long_max는 190배로 거래가 폭증했다.
- short_main과 short_max는 각각 3.7%, 8.8%로 거래가 급감했다.
- 이것은 사용자가 원하는 현재 1위 전략의 더 나은 버전 탐색과 맞지 않는다.

2. 현재 개선 경로가 embedded 기준선 reference와 다를 수 있다.
- 기준선 행은 embedded exact reference로 통과한다.
- 하지만 개선안은 Spec 기반 실행 경로를 탄다.
- 단순 rr/hold/trail 변화만으로도 거래 규모가 극단적으로 바뀐 것은 base_spec 개선 경로가 실제 기준선 거래 구조를 충분히 재현하지 못한다는 신호다.

3. 기준선 보존을 절대 고정으로 오해하면 안 된다.
- 사용자는 기준선 조건을 하나도 바꾸지 말라는 뜻이 아니다.
- 원하는 것은 기준선 조건군을 중심으로 한 작은 변형이다.
- 허용되는 변화: 일부 조건의 유사 지표 대체, 약한 조건 추가, 약한 조건 제거, 파라미터 소폭 조정, exit/risk 관리 조정.
- 금지되는 변화: 거래량이 몇십 배 늘거나 90% 이상 사라지는 신규 전략급 이탈.

기준선 로컬 변형의 수정된 정의
기준선 로컬 변형은 기준선의 핵심 아이디어와 상태 진단 구조를 유지하되, 조건군 내부에서 작게 실험하는 방식이다.

허용 예시
- long 기준선의 reclaim/shocklow/rare22 계열을 유지하면서 lowanchor, close_pos, wick, vol 조건을 약하게 추가한다.
- long 기준선의 close position 조건을 비슷한 성격의 wick 또는 low-anchor 조건으로 일부 대체한다.
- short 기준선의 과열 포착 구조(dev/rsi/wick/shock)를 유지하면서 dev 또는 rsi를 소폭 완화/강화한다.
- short 기준선의 blowoff 성격을 유지하면서 wick, shock_ret5, shock_range를 약하게 조정한다.
- entry를 완전히 넓히는 OR 조건은 피한다.
- exit-only 변화라도 거래량이 기준선과 극단적으로 달라지면 로컬 변형으로 인정하지 않는다.

8V28 설계 방향
1. 캔들 제한 없음.
2. 각 축 1개씩 총 4개 후보만 실행해 1시간 내외를 목표로 한다.
3. long 축은 8V27에서 거래 폭증이 있었으므로 진입 확장 금지, 기준선 조건군 내 약한 추가 제한 중심으로 간다.
4. short 축은 8V27에서 거래 기근이 있었으므로 과도한 제한 금지, dev/rsi/wick/shock의 유사 성격 소폭 대체/완화 중심으로 간다.
5. 기준선 조건 전체를 절대 고정하지는 않되, 거래량 규모가 기준선과 비교 가능한 범위에 들어오는지 parent_trade_ratio로 판정한다.
6. 결과 분석 시 parent_trade_ratio를 수익률/MDD와 동급 핵심 지표로 본다.

8V28 후보 방향
long_main
- reclaim/shocklow 구조는 유지
- lowanchor를 약하게 추가
- close_pos와 rr만 소폭 상향

long_max
- V51 rare22 구조는 유지
- lowanchor와 upper_wick 제한을 약하게 추가
- hold는 1봉만 줄임

short_main
- dev/rsi 과열 구조는 유지
- dev_short와 rsi_short_min을 소폭 완화
- close_pos_short_max를 소폭 낮춰 품질을 보존
- rr은 아주 약하게 낮춤

short_max
- blowoff 구조는 유지
- dev/rsi/wick/shock 계열을 비슷한 성격 안에서 소폭 완화
- 신규 독립 진입 조건은 추가하지 않음

추가 행동 규칙
1. 기준선 보존은 조건 불변이 아니라 전략 계열 보존으로 해석한다.
2. 로컬 변형은 작은 추가, 작은 제거, 유사 지표 대체, 파라미터 소폭 조정만 허용한다.
3. parent_trade_ratio가 극단적으로 벗어나면 성과와 관계없이 baseline drift로 판정한다.
4. 8V27처럼 단순 변화가 극단적 거래량 변화를 만들면, 해당 축은 다음 배치에서 조건 추가/완화 방향을 축별로 반대로 잡는다.
5. long에서 폭증하면 추가 제한, short에서 기근이면 소폭 완화가 우선이다.
