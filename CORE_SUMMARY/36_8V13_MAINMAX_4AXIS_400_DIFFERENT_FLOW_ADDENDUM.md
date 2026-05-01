8V13 MAINMAX 4AXIS 400 DIFFERENT FLOW ADDENDUM

목적
- long main, long max, short main, short max 각 1위 기준선을 부모로 두고 축별 100개씩 총 400개 개선안을 생성했다.
- 최근 기준선 확정 이후 눈에 띄는 성과가 없었기 때문에, 기존의 단순 파라미터 조정이나 기존 모듈의 직접 연장보다 다른 흐름의 개선을 시도했다.
- 거래 수 제한은 두지 않았다. 기준선 비교는 각 축 기준선과 공식 장기 기준선 모두를 함께 본다.

실행 산출물
- code_file: run_8v13_mainmax_4axis_400_different_flow_no_trade_cap.py
- result_dir: local_results/8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_NO_TRADE_CAP_20260429_153955/
- all_results: local_results/8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_NO_TRADE_CAP_20260429_153955/all_results.csv
- axis_leaders: local_results/8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_NO_TRADE_CAP_20260429_153955/axis_leaders.json
- run_summary: local_results/8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_NO_TRADE_CAP_20260429_153955/run_summary.txt

전체 판정
- verdict: no_promotion_all_axes_failed_different_flow_underperformed
- baseline_updated: false
- long_main_update: false
- long_max_update: false
- short_main_update: false
- short_max_update: false
- failed_symbols: 0

축별 1위 결과

1. long_main
- leader: long_main_v1_31_lm13_reversal_gravity_lm13_1_10
- parent: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176
- family: 8V13_LONG_MAIN_DIFFERENT_FLOW
- group: lm13_reversal_gravity_lm13_1
- trades: 214
- win_rate_pct: 55.1402
- final_return_pct: 2.6725
- max_return_pct: 2.8410
- max_drawdown_pct: 0.3431
- cd_value: 102.4879
- mdd_under_5: true
- beats_axis_reference: false
- interpretation: MDD는 잘 눌렀지만 edge가 거의 사라졌다. long_main의 다음 개선에서 entry를 더 희소화하거나 reverse confirmation을 강하게 거는 방식은 금지한다.

2. long_max
- leader: long_max_v1_33_lx13_asymmetric_unlock_lx13_1_12
- parent: 8V4_V51_V002_core_rare22_c1
- family: 8V13_LONG_MAX_DIFFERENT_FLOW
- group: lx13_asymmetric_unlock_lx13_1
- trades: 8248
- win_rate_pct: 35.0206
- final_return_pct: 18.8625
- max_return_pct: 26.3942
- max_drawdown_pct: 8.1185
- cd_value: 116.1376
- mdd_under_5: false
- beats_axis_reference: false
- interpretation: 거래 밀도와 max_return은 살아났지만 MDD가 8.1185로 커졌고, cd_value도 official long reference 121.7490보다 낮다. asymmetric unlock은 raw upside 보존 힌트로만 보관하고, 단독 승격 후보가 아니다.

3. short_main
- leader: short_main_v1_21_sm13_micro_squeeze_sm13_1_00
- parent: short_main_v1_40_sm12_volatility_squeeze_sm12_03_00
- family: 8V13_SHORT_MAIN_DIFFERENT_FLOW
- group: sm13_micro_squeeze_sm13_1
- trades: 1
- win_rate_pct: 100.0000
- final_return_pct: 0.0038
- max_return_pct: 0.0038
- max_drawdown_pct: 0.0000
- cd_value: 100.0038
- mdd_under_5: true
- beats_axis_reference: false
- interpretation: 거래 수 1회라서 무효에 가깝다. short_main은 새 희소 엔트리를 만들면 안 되고, 기존 short edge의 거래 밀도를 유지한 상태에서 exit/stop만 조정해야 한다.

4. short_max
- leader: short_max_v1_21_sx13_tail_reversal_sx13_1_00
- parent: short_max_v1_78_sx12_failure_sweep_sx12_06_05
- family: 8V13_SHORT_MAX_DIFFERENT_FLOW
- group: sx13_tail_reversal_sx13_1
- trades: 4
- win_rate_pct: 25.0000
- final_return_pct: 0.0293
- max_return_pct: 0.0293
- max_drawdown_pct: 0.0000
- cd_value: 100.0293
- mdd_under_5: true
- beats_axis_reference: false
- interpretation: 거래 수 4회라서 실전 전략 후보로 보지 않는다. short_max 역시 진입 구조를 새로 만들기보다 기존 reference의 진입 밀도를 보존하는 쪽으로 돌아가야 한다.

핵심 학습
- 8V13의 다른 흐름 접근은 성과 개선에 실패했다.
- long_main은 지나치게 안전한 흐름으로 바뀌면 max_return이 2.8410까지 붕괴한다.
- long_max는 raw upside를 어느 정도 살릴 수 있었지만 MDD 8.1185와 cd 116.1376으로 기준선에 못 미쳤다.
- short 계열은 가장 큰 문제가 low-trade collapse다. 승률이나 MDD가 좋아 보여도 trades 1~4는 평가 대상에서 제외한다.
- 다음 라운드에서 entry replacement 중심의 다른 흐름은 금지한다. 다른 흐름을 쓰더라도 기존 부모의 entry density는 보존하고, regime-aware exit/hold/stop/risk throttle 쪽으로 바꿔야 한다.

폐기 또는 낮은 우선순위
- lm13_reversal_gravity: MDD 압축은 되지만 edge kill이 심하므로 단독 확장 금지.
- lm13_micro_pullback_reentry류: long_main의 거래 수와 수익률을 동시에 낮추는 경향이 있으면 폐기.
- lx13_breakout_pullback_gate: 일부 변형에서 final_return이 크게 음수로 흐르고 max_return 0에 가까워지는 패턴이 나타나므로 다음 라운드 주력으로 쓰지 않는다.
- short micro_squeeze/tail_reversal의 새 진입형: trades가 1~4까지 붕괴했으므로 폐기.

보관할 수 있는 힌트
- lx13_asymmetric_unlock은 long_max에서 max_return_pct 26.3942까지는 만들었다. 그러나 MDD가 너무 커서, 다음에는 entry가 아니라 보유/청산의 비대칭 profit unlock 힌트로만 재사용한다.
- long_main의 극저 MDD 결과는 위험 차단 모듈 자체가 작동할 수 있음을 보여준다. 다만 이 모듈은 진입 전 필터가 아니라 손실 구간에서만 부분적으로 켜지는 soft throttle로 바꿔야 한다.

다음 단계 지침
- 8V14는 8V13 top을 부모로 삼지 않는다.
- long_main은 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176을 계속 부모로 두되, entry를 더 줄이지 말고 exit/hold/stop에 regime-aware profit unlock과 shallow-loss brake를 붙인다.
- long_max는 8V4_V51_V002_core_rare22_c1 또는 8V5 core/rare22 계열을 부모로 두되, lx13_asymmetric_unlock의 장점은 profit-side hold 쪽으로만 이식한다.
- short_main과 short_max는 8V13 short top을 버리고, 기존 short_main/short_max 기준선 또는 공식 short reference의 entry density를 보존하는 개선으로 돌아간다.
- 다음 400개는 4축을 유지하되, 각 축 100개를 다음 네 그룹으로 나눈다.
  - 25개: 부모 entry 유지 + exit/hold/stop만 변경
  - 25개: 손실 군집이 발생한 뒤에만 켜지는 soft throttle
  - 25개: 이익 구간에서만 보유시간을 늘리는 asymmetric profit unlock
  - 25개: 시장 상태 회피를 entry gate가 아니라 position sizing/hold shortening으로 적용
- short 축은 최소 거래 수 가드를 결과 판정에 강제한다. trades가 50 미만이면 cd_value가 높아도 무효 처리한다. 가능하면 100회 미만도 보조 참고로만 본다.

한 줄 결론
- 8V13은 기준선 갱신 실패다. 다음은 완전히 새로운 진입 흐름을 더 만들 것이 아니라, 기준선의 진입 밀도를 유지한 채 청산/보유/손실군집 제어를 상태별로 바꾸는 8V14로 가야 한다.
