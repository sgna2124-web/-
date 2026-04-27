8V9 long dual best 200 no trade cap addendum

version_reference: 8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED
summary_file: local_results/8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED/master_summary.txt
registry_file: local_results/8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED/8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED_registry.csv
side: long_only
failed_symbols: 0
verdict: no_promotion

공식 판정
공식 long 기준선은 여전히 6V2_L01_doubleflush_core다.
공식 기준선 official_cd_value: 121.7490
8V9 최고 official_cd_value: 105.640342
공식 승격 실패 사유: MDD 5% 미만은 통과했지만 official_cd_value가 기준선보다 낮다.

8V9 배치 최고 후보
후보 A, MDD 5% 미만 중 cd_value 1위:
strategy_name: 8V9_RAWV51_I013_entry_timing_window_r013
parent: 8V4_V51_V002_core_rare22_c1
group: entry_timing_window
trades: 1292
win_rate_pct: 52.9412
final_return_pct: 6.3735
max_return_pct: 10.4863
max_drawdown_pct: 4.3852
official_cd_value: 105.640342

후보 B, MDD 무관 전체 cd_value 1위:
strategy_name: 8V9_RAWV51_I013_entry_timing_window_r013
parent: 8V4_V51_V002_core_rare22_c1
group: entry_timing_window
trades: 1292
win_rate_pct: 52.9412
final_return_pct: 6.3735
max_return_pct: 10.4863
max_drawdown_pct: 4.3852
official_cd_value: 105.640342

후보 A와 후보 B는 동일 전략이다.

상위권 참고
1. 8V9_RAWV51_I013_entry_timing_window_r013 | trades 1292 | max_return_pct 10.4863 | max_drawdown_pct 4.3852 | official_cd_value 105.640342
2. 8V9_RAWV51_I014_entry_timing_window_r014 | trades 1387 | max_return_pct 9.2488 | max_drawdown_pct 4.0206 | official_cd_value 104.857076
3. 8V9_RAWV51_I012_entry_timing_window_r012 | trades 1403 | max_return_pct 10.7723 | max_drawdown_pct 5.7564 | official_cd_value 104.392873 | MDD 초과
4. 8V9_RAWV51_I054_candle_quality_gate_cq054 | trades 1123 | max_return_pct 8.7562 | max_drawdown_pct 4.2363 | official_cd_value 104.149400
5. 8V9_RAWV51_I046_candle_quality_gate_cq046 | trades 1546 | max_return_pct 8.7499 | max_drawdown_pct 5.0119 | official_cd_value 103.299765 | MDD 초과

8V8 대비 해석
8V8 최고 전략은 8V8_RAWV51_I080_raw_official_conversion_r080 이었다.
8V8 최고값: trades 1027 | max_return_pct 9.6311 | max_drawdown_pct 3.5251 | official_cd_value 105.766560
8V9 최고값: trades 1292 | max_return_pct 10.4863 | max_drawdown_pct 4.3852 | official_cd_value 105.640342
8V9는 8V8보다 trades와 max_return_pct는 증가했지만 MDD도 함께 상승하여 official_cd_value는 소폭 낮아졌다.
따라서 8V9는 엣지 회복 방향은 맞지만, 위험 증가를 충분히 제어하지 못했다.

장점
1. 거래 수 제한을 두지 않았음에도 top 후보 거래 수가 1292~1546 수준으로 회복되었다.
2. 8V6, 8V7의 과도한 희소화 실패에서 벗어나 V51 raw edge를 일부 복원했다.
3. entry_timing_window 계열이 MDD 5% 미만을 유지하면서 max_return_pct 10%대를 회복했다.
4. candle_quality_gate 계열도 일부 상위권에 진입해 candle/body/wick 품질 게이트가 보조 모듈로는 유효함을 보였다.
5. failed_symbols가 0으로 실행 안정성은 정상이다.

단점
1. 기준선 121.7490과 비교하면 official_cd_value가 여전히 16포인트 이상 낮다.
2. 8V5 raw 후보의 max_return_pct 41~42%대와 비교하면 edge 손실이 매우 크다.
3. 8V8보다 max_return_pct는 높아졌지만 MDD도 상승해 cd_value 순 개선은 실패했다.
4. entry_timing_window가 진입 품질을 고르긴 하지만 아직 상승 구간 보존보다 위험 구간 동반 노출이 크다.
5. candle_quality_gate는 단독 hard gate로 쓰면 수익 회복력보다 압축 효과가 먼저 나타나 기준선 돌파 가능성이 낮다.

핵심 학습
거래 수를 인위적으로 제한하지 않는 방향은 맞다.
좋은 질의 조건이라면 거래 수가 많아도 이익이어야 하며, 거래 수 증가 때문에 손실이 난다면 조건의 질이 낮은 것이다.
8V9는 trade cap을 제거하고도 전체 붕괴는 발생하지 않았으므로 방향 자체는 8V6/8V7보다 낫다.
다만 entry timing과 candle quality만으로는 V51 raw edge를 기준선 초과 수준까지 복원하지 못했다.

다음 설계 규칙
1. 다음 배치에서도 거래 수 제한을 전략 품질의 대체물로 사용하지 않는다.
2. trade cap, top N, 과도한 희소화 필터는 원칙적으로 사용하지 않는다.
3. 다음 개선 후보는 저장소 내 long 전략 중 MDD 5% 미만 cd_value 1위와 MDD 무관 전체 cd_value 1위로 선정한다.
4. 현재 후보 A와 후보 B는 8V9_RAWV51_I013_entry_timing_window_r013로 동일하다.
5. 단순 파라미터 조정은 하지 않는다.
6. 다음 개선은 entry_timing_window를 직접 더 좁히는 방식이 아니라, V51 raw core에 사후 위험 제어, 손실 군집 회피, exit/hold/stop 조정, 시장 상태 회피를 약하게 결합하는 방향이어야 한다.
7. candle_quality_gate는 단독 gate보다 risk throttle 또는 exit 보정 모듈로 이식한다.
8. strict/lowanchor는 safe branch 핵심 축이지만 전면 필터가 아니라 부분 브레이크와 상태 보정으로 쓴다.
9. 다음 목표는 최소 trades 1500 이상, 가능하면 2000 내외를 유지하면서 MDD를 5 미만으로 압축하고 max_return_pct를 20% 이상으로 회복하는 것이다.
