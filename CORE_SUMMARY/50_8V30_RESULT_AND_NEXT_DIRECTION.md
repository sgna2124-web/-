8V30 결과 및 다음 개선 방향

대상 배치
BATCH: 8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H
결과 위치: local_results/8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H/
master_summary: local_results/8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H/master_summary.txt
registry: local_results/8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H/8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H_registry.csv
strategies: local_results/8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H/strategies.json

전체 판정
- ROWS: 12
- ERRORS: 0
- BASELINE_GATE: PASSED
- TOP_ANY_MDD: 없음
- TOP_MDD_UNDER_5: 없음
- 개선안 8개 전부 승격 실패

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

8V30 개선안별 결과
1. long_main / 8V30_long_main_001_tp03_only_probe
- tag: tp03_only_probe_on_baseline_spec
- verdict: invalid_trade_explosion
- trades: 13116
- baseline_trades: 592
- parent_trade_ratio: 22.155405
- wins: 4536
- losses: 8580
- win_rate_pct: 34.583715
- final_return_pct: -11.588722
- max_return_pct: 0.0
- max_drawdown_pct: 72.282116
- official_cd_value: 27.717884
- 판정: TP03 only임에도 기준선 대비 22.16배 거래 폭증. TP03은 long_main에서 기준선 재현을 돕지 못한다. 또한 base_spec 개선 경로가 embedded 기준선 거래 구조와 다르게 작동한다는 의심이 더 강해졌다.

2. long_main / 8V30_long_main_002_loosen_reclaim_wick_close_range
- tag: long_loosen_same_family_wick_close_range_no_tp03
- verdict: invalid_trade_explosion
- trades: 24794
- baseline_trades: 592
- parent_trade_ratio: 41.881757
- wins: 8597
- losses: 16197
- win_rate_pct: 34.673711
- final_return_pct: -16.591494
- max_return_pct: 0.0
- max_drawdown_pct: 92.371558
- official_cd_value: 7.628442
- 판정: 롱 완화는 거래 폭증과 MDD 악화로 이어졌다. 기준선 long_main의 낮은 MDD 장점을 완전히 훼손했다. long_main은 완화 방향보다 기준선 핵심 anchor 복원이 먼저다.

3. long_max / 8V30_long_max_001_tp03_only_probe
- tag: tp03_only_probe_on_baseline_spec
- verdict: invalid_trade_explosion
- trades: 433571
- baseline_trades: 2276
- parent_trade_ratio: 190.496924
- wins: 144447
- losses: 289124
- win_rate_pct: 33.315651
- final_return_pct: -98.942442
- max_return_pct: 0.0
- max_drawdown_pct: 100.0
- official_cd_value: 0.0
- 판정: TP03 only임에도 기준선 대비 약 190.5배 거래 폭증. long_max에서 TP03은 폭증 억제에 거의 의미가 없다. V51 기준선의 실제 제한 구조가 improve 경로에 반영되지 않은 것으로 본다.

4. long_max / 8V30_long_max_002_loosen_rare22_range_vol_upper
- tag: long_rare22_loosen_range_vol_upper_no_tp03
- verdict: invalid_trade_explosion
- trades: 538228
- baseline_trades: 2276
- parent_trade_ratio: 236.479789
- wins: 179154
- losses: 359074
- win_rate_pct: 33.285894
- final_return_pct: -100.0
- max_return_pct: 0.0
- max_drawdown_pct: 100.0
- official_cd_value: 0.0
- 판정: long_max 완화는 최악에 가깝다. 기준선 대비 236.48배 거래 폭증, MDD 100%, 최종 -100%. long_max에서 완화 방향은 현재 improve 경로에서는 금지해야 한다.

5. short_main / 8V30_short_main_001_tp03_only_probe
- tag: tp03_only_probe_on_baseline_spec
- verdict: invalid_trade_starvation
- trades: 1032
- baseline_trades: 28017
- parent_trade_ratio: 0.036835
- wins: 294
- losses: 738
- win_rate_pct: 28.488372
- final_return_pct: 14.850291
- max_return_pct: 14.850291
- max_drawdown_pct: 27.998117
- official_cd_value: 82.694373
- 판정: TP03 only는 short_main 거래를 기준선의 3.68%로 줄이고 MDD를 크게 악화시켰다. short_main에 TP03을 기본 적용하면 안 된다.

6. short_main / 8V30_short_main_002_no_tp03_profit_keep_loss_trim
- tag: short_keep_dev_rsi_add_soft_loss_trim_no_tp03
- verdict: invalid_trade_starvation
- trades: 891
- baseline_trades: 28017
- parent_trade_ratio: 0.031802
- wins: 261
- losses: 630
- win_rate_pct: 29.292929
- final_return_pct: 13.439815
- max_return_pct: 13.439815
- max_drawdown_pct: 24.149456
- official_cd_value: 86.044717
- 판정: TP03을 제거했지만 손실 컷/품질 제한 조합이 여전히 과도하여 거래 기근이다. TP03보다도 improve 경로의 short 조건 추가가 매우 민감하게 거래를 죽인다.

7. short_max / 8V30_short_max_001_tp03_only_probe
- tag: tp03_only_probe_on_baseline_spec
- verdict: invalid_trade_starvation
- trades: 3197
- baseline_trades: 36505
- parent_trade_ratio: 0.087577
- wins: 891
- losses: 2306
- win_rate_pct: 27.869878
- final_return_pct: 46.433522
- max_return_pct: 46.433522
- max_drawdown_pct: 63.890660
- official_cd_value: 52.876179
- 판정: TP03 only는 short_max 거래를 기준선의 8.76%로 줄이고 MDD를 크게 악화시킨다. short_max에도 TP03 기본 적용 금지.

8. short_max / 8V30_short_max_002_no_tp03_blowoff_loss_trim
- tag: short_blowoff_keep_edge_add_soft_loss_trim_no_tp03
- verdict: invalid_trade_starvation
- trades: 2676
- baseline_trades: 36505
- parent_trade_ratio: 0.073305
- wins: 753
- losses: 1923
- win_rate_pct: 28.139013
- final_return_pct: 37.074256
- max_return_pct: 37.074256
- max_drawdown_pct: 56.496386
- official_cd_value: 59.632255
- 판정: TP03 제거에도 거래 기근과 MDD 악화. 손실 컷을 추가했지만 기준선의 raw upside와 거래량을 모두 잃었다.

8V30 장점
1. TP03 단독 효과를 축별로 확인했다.
- long에서는 TP03만 추가해도 거래 폭증이 유지되었다.
- short에서는 TP03만 추가하면 거래 기근과 MDD 악화가 발생했다.
- 따라서 TP03은 short 기준선 개선에 부적합하며, long에서도 폭증 해결책이 아니다.

2. 롱 완화 방향의 위험을 확인했다.
- long_main 완화는 parent ratio 41.88배, MDD 92.37%.
- long_max 완화는 parent ratio 236.48배, MDD 100%.
- 현재 improve 경로에서는 롱 완화가 성과 개선이 아니라 거래 폭발로 연결된다.

3. 숏 손실 컷 방향도 너무 민감하다는 점을 확인했다.
- TP03 없이도 short_main 손실 컷 후보는 기준선 거래량의 3.18%에 그쳤다.
- short_max 손실 컷 후보는 기준선 거래량의 7.33%에 그쳤다.
- 숏에서 조건을 조금만 추가해도 기준선 거래 집합이 거의 사라진다.

4. 다음 단계의 우선순위가 명확해졌다.
- 신규 개선보다 base_spec/improve 경로가 embedded 기준선과 왜 다른지 진단해야 한다.

8V30 단점
1. 개선안 8개 전부 무효다.
- long은 전부 trade explosion.
- short는 전부 trade starvation.

2. long의 거래 폭증 원인이 조건 강도 문제가 아님이 더 분명해졌다.
- TP03 only도 폭증, 완화도 폭증이다.
- 따라서 long은 조건을 더 넣고 빼는 방식보다 기준선 clone 재현 여부를 먼저 확인해야 한다.

3. short는 TP03 제거만으로 기준선 거래량이 복원되지 않았다.
- 손실 컷 후보도 3~7% 거래량에 그쳤다.
- short도 base_spec 개선 경로가 embedded 기준선을 재현하지 못하고 있거나, 추가 조건이 엔진에서 예상보다 강한 병목으로 작동한다.

4. 현재 상태에서 v31을 또 일반 개선으로 만들면 같은 실패를 반복할 가능성이 높다.

핵심 교훈
1. TP03은 신규 개선안의 공통 필수 조건에서 제외한다.
2. short에는 TP03을 기본 적용하지 않는다.
3. long도 TP03만으로 거래 폭증을 막을 수 없다.
4. long 완화는 현재 경로에서 금지한다.
5. short 손실 컷은 지금처럼 여러 값을 한 번에 조정하면 안 된다.
6. parent_trade_ratio가 정상화되기 전에는 수익률/MDD 개선을 평가하지 않는다.

가장 중요한 진단
8V30 결과는 clone sanity check 필요성을 확정한다.
base_spec(axis) 그대로 실행한 improve clone이 embedded 기준선과 같은 거래 수/수익/MDD를 내는지 먼저 확인해야 한다.

만약 clone이 실패하면 다음과 같이 판정한다.
- 현재 개선안은 기준선의 변형이 아니다.
- embedded baseline reference와 improve Spec 실행 경로가 다르다.
- 이 상태에서 조건을 더하거나 빼는 것은 기준선 개선이 아니라 다른 전략 실험이다.

8V31 권장 방향
BATCH 예시: 8V31_CLONE_SANITY_AND_ONE_DELTA

구성
1. baseline embedded reference 4개 유지.
2. 각 축별 clone 1개 추가.
   - base_spec(axis) 그대로 사용.
   - name/kind/tag만 바꿈.
   - TP03 추가 금지.
   - 조건 변경 금지.
3. clone 결과와 embedded 기준선 비교.
   - trades ratio 0.95~1.05 목표.
   - max_return/MDD 근접 여부 확인.
4. clone 통과 축만 one-delta 후보 1개 추가.
   - long: 기존 조건 1개만 소폭 완화 또는 강화.
   - short: 손실 컷 1개만 추가 또는 exit 파라미터 1개만 조정.
5. clone 실패 축은 개선 후보를 만들지 않고 clone_failed로 기록.

8V31에서 금지할 것
1. TP03 공통 적용 금지.
2. 여러 조건 동시 조정 금지.
3. 롱 완화 대량 적용 금지.
4. 숏 손실 컷 복합 적용 금지.
5. 캔들 제한 금지.
6. clone 검증 없이 일반 개선 진행 금지.

실무적 결론
현재 문제는 개선 아이디어 부족이 아니라 기준선 재현 경로 불일치다. v31은 성과 개선 배치가 아니라 clone sanity 진단 배치로 만들어야 한다. clone이 기준선을 재현하는 축만 다음 개선 대상으로 인정한다.
