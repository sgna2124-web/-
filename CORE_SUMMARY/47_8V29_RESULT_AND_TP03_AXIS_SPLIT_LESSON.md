8V29 결과 및 TP03 축별 적용 교훈

대상 배치
BATCH: 8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H
결과 위치: local_results/8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H/
master_summary: local_results/8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H/master_summary.txt
registry: local_results/8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H/8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H_registry.csv
strategies: local_results/8V29_LONG_QUALITY_SHORT_NO_TP03_LOCAL_1H/strategies.json

전체 판정
- ROWS: 8
- ERRORS: 0
- BASELINE_GATE: PASSED
- TOP_ANY_MDD: 없음
- TOP_MDD_UNDER_5: 없음
- 개선안 4개 전부 무효

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

8V29 개선안별 결과
1. long_main / 8V29_long_main_001_shocklow_reclaim_quality_stack_tp03
- tag: long_keep_shocklow_reclaim_add_quality_stack_tp03
- verdict: invalid_trade_explosion
- trades: 6697
- baseline_trades: 592
- parent_trade_ratio: 11.312500
- wins: 2307
- losses: 4390
- win_rate_pct: 34.448260
- final_return_pct: -7.669911
- max_return_pct: 0.0
- max_drawdown_pct: 45.546841
- official_cd_value: 54.453159
- 판정: 거래 폭증은 줄었지만 여전히 기준선 대비 11.3배다. 8V28의 약 22배보다 개선되었으나 기준선 로컬 변형으로 보기에는 너무 멀다. close_pos, wick, upper_wick, vol, body, range, lowanchor, strict, TP03을 모두 추가했는데도 long 거래 폭증이 남아 있다.

2. long_max / 8V29_long_max_001_rare22_quality_stack_tp03
- tag: long_keep_rare22_add_strict_lowanchor_quality_stack_tp03
- verdict: invalid_trade_explosion
- trades: 167541
- baseline_trades: 2276
- parent_trade_ratio: 73.612039
- wins: 56594
- losses: 110947
- win_rate_pct: 33.779194
- final_return_pct: -83.241291
- max_return_pct: 0.0
- max_drawdown_pct: 99.991579
- official_cd_value: 0.008421
- 판정: 8V28의 약 190.6배보다 줄었지만 여전히 기준선 대비 73.6배다. 품질 조건을 강하게 추가했는데도 폭증이 계속된다. long_max는 조건 추가만으로는 기준선 거래 규모에 접근하지 못한다.

3. short_main / 8V29_short_main_001_no_tp03_wick_to_sweep_reject_guard
- tag: short_remove_tp03_replace_wick_with_sweep_reject_guard
- verdict: invalid_zero_trade
- trades: 0
- baseline_trades: 28017
- parent_trade_ratio: 0.0
- wins: 0
- losses: 0
- win_rate_pct: 0.0
- final_return_pct: 0.0
- max_return_pct: 0.0
- max_drawdown_pct: 0.0
- official_cd_value: 100.0
- 판정: TP03을 제거했는데도 0트레이드다. 원인은 TP03이 아니라 require_upper_sweep + require_ema_reject + shock/close_pos 강화 조합이 지나치게 강했을 가능성이 높다.

4. short_max / 8V29_short_max_001_no_tp03_blowoff_reject_mdd_guard
- tag: short_remove_tp03_keep_blowoff_add_reject_mdd_guard
- verdict: invalid_zero_trade
- trades: 0
- baseline_trades: 36505
- parent_trade_ratio: 0.0
- wins: 0
- losses: 0
- win_rate_pct: 0.0
- final_return_pct: 0.0
- max_return_pct: 0.0
- max_drawdown_pct: 0.0
- official_cd_value: 100.0
- 판정: TP03 제거에도 0트레이드다. short_max 역시 추가 조건이 기준선의 과열 진입 구조를 완전히 막았다.

8V29 장점
1. 축별 TP03 적용 문제를 분리했다.
- long에는 TP03을 유지했고 short에는 TP03을 제거했다.
- 이를 통해 short 거래 기근의 원인이 TP03만은 아니라는 점을 확인했다.

2. long 거래 폭증이 일부 줄었다.
- long_main parent_trade_ratio는 8V28 약 21.97배에서 8V29 약 11.31배로 줄었다.
- long_max parent_trade_ratio는 8V28 약 190.60배에서 8V29 약 73.61배로 줄었다.
- 즉, long에서 품질 조건 추가는 방향성 자체는 맞지만 강도와 구조가 아직 부족하다.

3. 캔들 제한 없는 동일 환경 비교가 유지되었다.
- 기준선과 개선안은 전체 데이터 환경에서 비교되었다.
- max-bars를 사용하지 않았다.

4. baseline gate는 계속 정상 작동했다.
- 기준선 4개 reference는 모두 통과했다.
- 저장소 접근 경로와 실행 cwd 분리 원칙도 유지되었다.

8V29 단점
1. 개선안 4개 전부 승격 후보가 아니다.
- long 2개는 trade explosion.
- short 2개는 zero trade.

2. long은 품질 조건을 크게 추가해도 기준선 거래 규모에 접근하지 못했다.
- long_main 11.31배, long_max 73.61배는 여전히 기준선 이탈이다.
- 특히 long_max는 품질 스택이 강했는데도 거래가 167,541건 발생했다.
- 이는 long 개선 경로가 embedded 기준선의 원형을 충분히 재현하지 못하거나, 기준선의 실제 핵심 제한 조건이 base_spec 개선 경로에서 빠져 있을 가능성을 다시 보여준다.

3. short는 TP03 제거보다 추가 조건의 영향이 더 컸다.
- TP03을 없앴는데도 short_main/short_max 모두 0트레이드가 나왔다.
- require_upper_sweep, require_ema_reject, shock_ret5/shock_range 강화, close_pos_short 제한, post_loss/sym_dd guard가 동시에 결합되어 과도하게 막힌 것으로 본다.

4. 한 번에 너무 많은 조건을 추가했다.
- long은 폭증을 잡기 위해 품질 조건을 많이 쌓았다.
- short는 TP03 제거 후 품질 보호를 위해 추가 조건을 많이 쌓았다.
- 결과적으로 어떤 조건이 실제 병목인지 분해되지 않았다.

핵심 교훈
1. TP03은 전 축 공통 필수 조건으로 유지하면 안 된다.
- short에서는 TP03이 거래 기근을 유발했을 가능성이 있었지만, 8V29 결과상 zero trade의 직접 원인은 추가 조건 조합이었다.
- 향후 short 개선안에서는 TP03을 기본 제거하되, 추가 조건은 한 번에 하나만 넣어야 한다.

2. long은 조건 추가 방향이 맞지만 아직 충분하지 않다.
- 거래 폭증이 줄어든 것은 긍정적이다.
- 그러나 기준선 대비 10배 이상이면 로컬 변형이 아니다.
- long은 기준선의 실제 핵심 제한 조건을 찾아야 한다. close_pos/wick/vol/range/lowanchor보다 더 직접적인 baseline entry anchor가 필요하다.

3. short는 0트레이드 원인 분해가 먼저다.
- 다음 배치에서는 short에 require_upper_sweep, require_ema_reject, shock 강화, close_pos 제한을 동시에 넣으면 안 된다.
- short는 TP03 제거 상태에서 조건 하나씩만 추가하거나, 기존 wick/dev/rsi 중 하나만 대체해야 한다.

4. clone sanity 또는 base_spec drift 진단 필요성은 더 강해졌다.
- 8V27, 8V28, 8V29 모두 기준선 대비 거래 규모가 극단적으로 벗어났다.
- base_spec(axis) 개선 경로가 embedded exact baseline과 같은 거래 구조를 재현하는지 확인하지 않으면, 계속 기준선 개선이 아니라 다른 경로 실험이 된다.

다음 단계 권장
1. 8V30은 신규 강한 조합이 아니라 분해 실험으로 간다.
2. long은 품질 조건을 하나씩 추가하는 단일 조건 분해형으로 간다.
   - 예: lowanchor only, strict only, close_pos only, upper_wick only, vol only, range20 only.
   - 목적은 어떤 조건이 trade explosion을 가장 효율적으로 줄이는지 확인하는 것이다.
3. short는 TP03 제거 상태에서 단일 대체/추가만 테스트한다.
   - 예: dev/rsi 원형 유지 + wick 완화 only.
   - 예: dev/rsi 원형 유지 + close_pos_short only.
   - 예: dev/rsi 원형 유지 + upper_sweep only.
   - 예: dev/rsi 원형 유지 + ema_reject only.
4. parent_trade_ratio를 1차 목표로 둔다.
   - long_main 목표: 0.5~1.2 근처 접근.
   - long_max 목표: 0.5~1.2 근처 접근.
   - short_main 목표: 0.6~1.1 근처 접근.
   - short_max 목표: 0.6~1.1 근처 접근.
5. 수익률/MDD 승격 판단은 parent_trade_ratio가 정상 범위에 들어온 뒤에 한다.

행동 규칙 추가
- 기준선 개선에서 조건을 많이 쌓아 한 번에 해결하려 하지 않는다.
- 거래량 문제가 있으면 먼저 단일 조건 분해 실험으로 어떤 조건이 거래량을 얼마나 변화시키는지 파악한다.
- short에는 TP03을 기본 적용하지 않는다.
- long에는 TP03을 유지할 수 있지만, TP03만으로 폭증을 막을 수 없다고 본다.
- long 거래 폭증은 추가 품질 조건보다 기준선 진입 원형 재현 문제를 우선 의심한다.
