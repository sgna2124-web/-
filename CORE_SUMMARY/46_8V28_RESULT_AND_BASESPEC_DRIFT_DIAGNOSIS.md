8V28 결과 및 base_spec 개선 경로 드리프트 진단

대상 배치
BATCH: 8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH
결과 위치: local_results/8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH/
master_summary: local_results/8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH/master_summary.txt
registry: local_results/8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH/8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH_registry.csv
strategies: local_results/8V28_LOCAL_MUTATION_NO_CANDLE_LIMIT_1H_NO_BASELINE_TOUCH/strategies.json

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

8V28 개선안별 결과
1. long_main / 8V28_long_main_001_reclaim_lowanchor_local_tp03
- tag: add_lowanchor_small_rr_tp03
- verdict: invalid_trade_explosion
- trades: 13009
- baseline_trades: 592
- parent_trade_ratio: 21.974662
- wins: 4473
- losses: 8536
- win_rate_pct: 34.383888
- final_return_pct: -11.838898
- max_return_pct: 0.0
- max_drawdown_pct: 72.080258
- official_cd_value: 27.919742
- 판정: 기준선보다 거래가 약 22배 증가했다. lowanchor 추가, close_pos 소폭 강화, rr 소폭 상향이라는 제한형 변형인데도 거래가 폭증했다. 이는 조건 설계 자체보다 base_spec 기반 개선 실행 경로가 embedded 기준선 reference와 다른 경로를 타는 문제가 핵심일 가능성이 크다.

2. long_max / 8V28_long_max_001_rare22_lowanchor_exit_local_tp03
- tag: add_lowanchor_soft_exit_tp03
- verdict: invalid_trade_explosion
- trades: 433797
- baseline_trades: 2276
- parent_trade_ratio: 190.596221
- wins: 145306
- losses: 288491
- win_rate_pct: 33.496313
- final_return_pct: -98.915650
- max_return_pct: 0.0
- max_drawdown_pct: 100.0
- official_cd_value: 0.0
- 판정: 기준선보다 거래가 약 190.6배 증가했다. V51 rare22 유지, lowanchor 추가, upper_wick 소폭 강화, hold 1봉 축소였는데도 거래가 폭증했다. 이 정도면 개선안이 느슨해서가 아니라 기준선 재현 경로와 개선안 실행 경로의 불일치가 거의 확실하다.

3. short_main / 8V28_short_main_001_dev_rsi_soft_replace_tp03
- tag: soft_replace_dev_rsi_keep_quality_tp03
- verdict: invalid_trade_starvation
- trades: 1134
- baseline_trades: 28017
- parent_trade_ratio: 0.040475
- wins: 324
- losses: 810
- win_rate_pct: 28.571429
- final_return_pct: 17.202797
- max_return_pct: 17.202797
- max_drawdown_pct: 30.270345
- official_cd_value: 81.725106
- 판정: 기준선 거래량의 약 4.0%만 남았다. dev/rsi 소폭 완화와 close_pos 품질 보존을 넣었지만 거래 기근이 유지되었다. short 축도 단순 Spec 변형이 기준선의 embedded 거래 집합을 보존하지 못하고 있다.

4. short_max / 8V28_short_max_001_blowoff_soft_replace_tp03
- tag: soft_replace_blowoff_keep_wick_tp03
- verdict: invalid_trade_starvation
- trades: 3423
- baseline_trades: 36505
- parent_trade_ratio: 0.093768
- wins: 945
- losses: 2478
- win_rate_pct: 27.607362
- final_return_pct: 48.239330
- max_return_pct: 48.239330
- max_drawdown_pct: 66.434271
- official_cd_value: 49.757612
- 판정: 기준선 거래량의 약 9.4%만 남았고 MDD가 66.43%로 악화되었다. 수익이 일부 발생해도 기준선 대비 MDD, 거래량, CD가 모두 부적합하다.

8V28 장점
1. 캔들 제한 없는 동일 환경 비교 원칙은 지켜졌다.
- max-bars 없이 전체 데이터 기준으로 실행되었다.
- 기준선과 개선안의 비교 환경은 8V25/8V26보다 올바르다.

2. baseline gate는 통과했다.
- 기준선 reference 자체는 정상적으로 로드되고 통과했다.
- 저장소 접근 경로와 실행 cwd 분리도 유지되었다.

3. 기준선 보존의 핵심 병목이 명확해졌다.
- 8V27에 이어 8V28에서도 long은 극단적 거래 폭증, short는 거래 기근이 반복되었다.
- 조건 변형 방향을 바꿔도 같은 패턴이 반복되었기 때문에, 단순 파라미터 조정 문제가 아니라 embedded 기준선과 base_spec 개선 경로의 불일치 문제를 우선 점검해야 한다.

4. parent_trade_ratio를 핵심 지표로 보는 규칙은 유효했다.
- max_return/MDD만 보면 원인 파악이 어렵지만, parent_trade_ratio를 보면 전략 계열 이탈 여부가 즉시 드러난다.

8V28 단점
1. 개선안 전부 무효다.
- long_main, long_max는 invalid_trade_explosion.
- short_main, short_max는 invalid_trade_starvation.
- 승격 후보가 없다.

2. long 계열은 제한형 변형인데도 거래가 폭증했다.
- long_main은 기준선 대비 21.97배.
- long_max는 기준선 대비 190.60배.
- lowanchor 추가, upper_wick 강화, close_pos 강화 같은 제한형 변화가 거래를 늘릴 수는 없다. 따라서 실제로는 base_spec 개선안이 embedded 기준선의 진입 구조를 그대로 재현하지 못하고 있을 가능성이 높다.

3. short 계열은 완화형 변형인데도 거래 기근이 이어졌다.
- short_main은 기준선 대비 4.05%.
- short_max는 기준선 대비 9.38%.
- dev/rsi/wick/shock를 소폭 완화했는데도 기준선 거래 규모로 회복되지 않았다. short 기준선도 개선안 실행 경로가 embedded 기준선과 다르다고 봐야 한다.

4. 현재 방식으로 8V29를 또 만들면 같은 실패를 반복할 가능성이 높다.
- base_spec(axis)에서 파생한 Spec 개선안이 기준선의 embedded_exact_reference 거래 집합을 보존하지 못한다.
- 따라서 다음 단계는 신규 조건 실험이 아니라 기준선 재현 경로 검증이다.

핵심 진단
8V27과 8V28의 반복 패턴은 다음과 같다.
- long_main: 약 22배 거래 폭증 반복
- long_max: 약 190배 거래 폭증 반복
- short_main: 약 3.7~4.0% 수준 거래 기근 반복
- short_max: 약 8.8~9.4% 수준 거래 기근 반복

이 패턴은 개선 조건의 세부 차이보다 실행 경로 차이를 의심하게 한다.
현재 baseline 행은 embedded exact reference 값으로 들어가지만, improve 행은 base_spec(axis)에서 생성된 Spec으로 실제 엔진을 돌린다. 만약 base_spec이 embedded 기준선의 실제 진입 구조를 완전히 재현하지 못한다면, 어떤 소폭 변형을 해도 기준선 로컬 개선이 되지 않는다.

다음 단계 우선순위
1. 8V29를 바로 신규 조건 실험으로 만들지 않는다.
2. 먼저 base_spec(axis) 그대로 kind=improve로 실행했을 때 embedded 기준선과 같은 trades, max_return, MDD가 나오는지 검증한다.
3. 이를 clone sanity check라고 부른다.
4. clone sanity check가 실패하면 기준선 개선은 불가능하다. 기준선과 같은 로직을 복제하지 못한 상태에서 변형을 만들고 있기 때문이다.
5. clone sanity check가 통과한 축만 작은 추가/대체/완화 변형을 진행한다.

8V29 권장 설계
BATCH 예시: 8V29_CLONE_SANITY_THEN_LOCAL_MUTATION_NO_CANDLE_LIMIT

구성
1. baseline embedded reference 4개 유지.
2. axis별 clone 후보 1개 추가.
   - clone은 base_spec(axis) 그대로 name/kind/tag만 바꾼 것이다.
   - TP03 신규 조건도 clone에는 추가하지 않는다. clone은 기준선 재현 검증용이다.
3. clone 결과가 parent_trade_ratio 0.95~1.05, max_return/MDD 근접이면 그 축만 변형 후보 실행.
4. clone 실패 축은 변형 후보를 실행하지 않거나 별도 failed_clone으로 기록한다.
5. clone 통과 후 변형은 작은 추가/대체/완화만 허용한다.

중요 규칙 수정
1. 기준선 보존은 조건 불변이 아니다.
2. 기준선 보존은 전략 계열과 거래 집합 규모를 보존한다는 뜻이다.
3. 일부 조건 대체, 조건 추가, 약한 제거는 허용한다.
4. 그러나 그 전에 base_spec 기반 clone이 embedded 기준선을 재현해야 한다.
5. clone이 기준선을 재현하지 못하면 개선이 아니라 다른 실행 경로의 새 전략이 된다.

다음 코드 작성 체크리스트
- 캔들 제한 없음.
- max-bars 자동 주입 없음.
- 기준선 embedded reference 유지.
- clone sanity check 내장.
- clone에는 TP03 추가 금지.
- TP03은 clone 통과 후 실제 개선안에만 적용.
- clone 실패 축은 개선안 실행 금지 또는 결과에서 제외.
- 결과 저장 경로는 C:\Users\user\Documents\GitHub\-\local_results\{BATCH} 유지.
