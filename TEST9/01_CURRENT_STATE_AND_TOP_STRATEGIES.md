현재 상태 요약

최신 전체 1위
- experiment: atr19_t27_b17_r020
- family: results_json_only_timeout18_time_reduce_v4
- 구조:
  - stop_mode = atr_only
  - target_mode = ema_only
  - timeout_bars = 27
  - atr_stop_mult = 1.9
  - protect_mode = time_reduce
  - time_reduce_bars = 17
  - time_reduce_to_risk_frac = 0.20
- 주요 수치:
  - final_return_pct = 2467.844989645954
  - peak_growth_pct = 2512.901345050304
  - mdd_pct = -39.4285119329169
  - pf = 1.2757368695425308
  - cd_value = 1582.6732

직전 1위와 비교
- 직전 1위: atr19_t27_b17_r025_baseline
- 직전 수치:
  - final_return_pct = 2324.1363964006264
  - peak_growth_pct = 2379.765281915955
  - mdd_pct = -40.627964259342995
  - pf = 1.2678989748499474
  - cd_value = 1472.2871
- 개선 방향:
  - time_reduce_to_risk_frac 를 0.25에서 0.20으로 더 강하게 줄인 것이 핵심 승리 포인트였다.
  - 수익 증가 + MDD 개선이 동시에 발생했다.

현재 상위권 전략들
1. atr19_t27_b17_r020
   - cd_value 1582.6732
   - final_return_pct 2467.844989645954
   - mdd_pct -39.4285119329169
   - 메모: 현 전체 1위

2. atr19_t27_b18_r020
   - cd_value 1578.8114
   - final_return_pct 2473.9807297159823
   - mdd_pct -39.82518765708628
   - 메모: 수익은 높지만 cd_value는 1위보다 약간 낮음

3. atr19_t27_b16_r020
   - cd_value 1558.5800
   - final_return_pct 2410.4198073829148
   - mdd_pct -39.10836685010328
   - 메모: MDD는 상위권 중 가장 좋음

4. atr195_t27_b17_r025
   - cd_value 1518.4674
   - final_return_pct 2387.4423610853264
   - mdd_pct -40.23412084106748
   - 메모: atr_stop_mult 1.95도 유효하나 1.9보다 미세하게 뒤짐

5. atr1925_t27_b17_r025
   - cd_value 1495.1243
   - final_return_pct 2346.9116101323657
   - mdd_pct -40.20221382038095
   - 메모: 1.925는 중간 구간 후보

안정형 관점 보조 후보
- atr195_t27_b17_r025_long_light
  - final_return_pct 2099.8755671005592
  - mdd_pct -38.991996261959116
  - pf 1.2831406587957113
  - 메모: 절대 수익 1위는 아니지만, MDD와 PF 관점에서 매우 우수한 안정형 보조 후보

현재 전략 구조에 대한 결론
- 지배 변수 1: timeout 27
- 지배 변수 2: time_reduce 타이밍 16~18봉, 중심축은 17봉
- 지배 변수 3: time_reduce 강도 0.20이 현재 최상단
- 지배 변수 4: atr_stop_mult 1.9 부근
- 보조 변수: long_light는 안정형에서는 도움되지만, 공격형 최상단은 아님
- 상대적으로 중요도가 낮아진 변수: confirmation, retrace entry, 조기 breakeven, aggressive trailing

현재 기준선으로 삼아야 할 것
- 다음 대화창에서는 atr19_t27_b17_r020 을 공식 기준선으로 삼아야 한다.
- 이후 모든 후속 레인은 이 기준선 대비 개선 여부를 판단한다.
