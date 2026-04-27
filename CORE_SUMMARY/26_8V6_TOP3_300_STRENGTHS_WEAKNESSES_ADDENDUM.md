8V6 TOP3 300 장단점 추가 기록

배치명: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
대상: 8V5 상위 3개 전략을 부모로 하여 각 100개씩 개선
부모 1: 8V5_V51P_V002_core_rare22_c1
부모 2: 8V5_V51P_V001_core_base
부모 3: 8V5_V51P_V032_shocklow_rare22_c1
전략 수: 300
실패 심볼: 0
공식 승격 조건: max_drawdown_pct < 5.0
공식 cd_value: max_return_pct / max_drawdown_pct
결과 위치: local_results/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3/

중요 보정
8V6 결과 파일은 cd_value와 legacy_equity_cd_value를 분리했다.
8V6의 cd_value는 공식 정의인 max_return_pct / max_drawdown_pct다.
이전 6V2~8V5 문서에 남아 있는 121.5300, 132.7352 같은 숫자는 legacy_equity_cd_value 성격이 섞여 있으므로, 공식 ratio 비교가 필요할 때는 max_return_pct / max_drawdown_pct로 재계산한다.
현재 long 공식 기준선 6V2_L01_doubleflush_core의 공식 ratio는 23.9191 / 1.7512 = 13.6587이다.
8V6 최고 공식 cd_value는 2.4639이므로 공식 기준선 교체와는 거리가 멀다.

상위 결과
1. 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18
parent: 8V5_V51P_V001_core_base
family: core_base
group: hybrid_cover
trades: 652
win_rate_pct: 43.7117
final_return_pct: 3.0599
max_return_pct: 5.2510
max_drawdown_pct: 2.1312
cd_value: 2.4639
legacy_equity_cd_value: 100.8636
verdict: official_mdd_pass

2. 8V6_P2_CORE_BASE_I050_mdd_compress_mdd15
parent: 8V5_V51P_V001_core_base
family: core_base
group: mdd_compress
trades: 501
win_rate_pct: 47.9042
final_return_pct: 2.2944
max_return_pct: 3.7822
max_drawdown_pct: 1.5658
cd_value: 2.4155
legacy_equity_cd_value: 100.6927
verdict: official_mdd_pass

3. 8V6_P3_SHOCKLOW_RARE22_C1_I088_hybrid_cover_hyb18
parent: 8V5_V51P_V032_shocklow_rare22_c1
family: shocklow_rare22_c1
group: hybrid_cover
trades: 666
win_rate_pct: 43.0931
final_return_pct: 2.7986
max_return_pct: 5.1129
max_drawdown_pct: 2.2018
cd_value: 2.3222
legacy_equity_cd_value: 100.5352
verdict: official_mdd_pass

4. 8V6_P1_CORE_RARE22_C1_I088_hybrid_cover_hyb18
parent: 8V5_V51P_V002_core_rare22_c1
family: core_rare22_c1
group: hybrid_cover
trades: 668
win_rate_pct: 42.6647
final_return_pct: 2.6855
max_return_pct: 4.9854
max_drawdown_pct: 2.1985
cd_value: 2.2677
legacy_equity_cd_value: 100.4280
verdict: official_mdd_pass

핵심 해석
8V6는 MDD 압축에는 성공했지만 edge 보존에는 실패했다.
상위권 대부분이 MDD 1.5~2.3대로 내려오면서 공식 MDD 조건은 쉽게 통과했다.
하지만 max_return_pct가 3~5%대로 급격히 줄어 공식 cd_value가 2.46 이하에 머물렀다.
즉 8V6는 V51의 위험을 줄인 라운드가 아니라, V51의 진입 밀도와 raw edge를 과도하게 잘라낸 라운드다.

부모별 해석
core_base는 이번 라운드에서 가장 잘 버텼다.
P2 core_base의 hybrid_cover_hyb18과 mdd_compress_mdd15가 전체 1, 2위를 차지했다.
이는 rare22_c1보다 core_base가 추가 필터와 혼합될 때 edge 손실이 상대적으로 덜하다는 뜻이다.
다만 절대 수익이 너무 낮아 공식 후보가 아니다.

core_rare22_c1은 8V5의 최고 raw 후보였지만, 8V6의 강한 압축 조건에서는 core_base보다 약해졌다.
rare22는 원래 불필요한 진입을 줄이는 장점이 있었지만, 그 위에 mdd_compress/hybrid_cover가 추가되면 이중 희소화가 발생한다.
결과적으로 MDD는 낮아지지만 수익 곡선의 우상향 힘이 거의 사라졌다.

shocklow_rare22_c1은 core_rare22_c1보다 일부 조합에서 약간 더 잘 버텼지만, core_base를 넘지는 못했다.
shocklow는 원래 급락/저점 충격 구간을 더 선호하는 성격이 있어 MDD 압축과 결합하면 샘플 질은 유지될 수 있다.
그러나 이번 결과에서는 수익 절대값이 충분하지 않았다.
shocklow는 주력 부모가 아니라 보조 필터 또는 일부 구간의 리스크 브레이크 후보로 봐야 한다.

성공한 점
1. 코드 안정성: failed_symbols=0으로 정상 실행되었다.
2. 공식 MDD 조건: 상위권 다수가 MDD 5 미만을 통과했다.
3. core_base의 내구성 확인: 강한 필터 추가에도 P2 core_base가 가장 덜 무너졌다.
4. hybrid_cover_hyb18과 mdd_compress_mdd15는 MDD 압축 방향 자체는 유효했다.

실패한 점
1. raw edge 보존 실패: max_return_pct가 8V5의 41~42%대에서 8V6의 3~5%대로 축소되었다.
2. 과도한 전단 필터링: 진입 전에 너무 많이 잘라 V51의 핵심 장점인 반복적 microbase_pop edge가 사라졌다.
3. rare22 이중 희소화: rare22 위에 추가 희소 필터를 덧대면 trades와 수익이 함께 죽는다.
4. safe branch 강화 실패: MDD<5 조건은 충족했지만 기존 strict/lowanchor safe branch의 강한 cd 영역을 회복하지 못했다.
5. 공식 승격 실패: 기준선 대비 cd_value가 너무 낮아 승격 후보가 아니다.

다음 전략 생성 규칙
1. 8V6의 mdd_compress/hybrid_cover를 그대로 더 강하게 밀면 안 된다.
2. V51 core_base/core_rare22_c1의 MDD를 5 아래로 내리되, 전단 진입 필터를 추가하는 방식보다 사후 브레이크, 손실 군집 회피, 변동성 폭발 구간 일시 회피를 우선한다.
3. core_base는 8V6에서 가장 잘 버틴 부모이므로 다음 라운드의 기준 부모로 유지한다.
4. core_rare22_c1은 raw edge 기준으로 중요하지만, 추가 희소화가 아닌 exit/hold/stop 조정 중심으로 다뤄야 한다.
5. shocklow_rare22_c1은 주력 확장이 아니라 core_base/core_rare22의 보조 커버 조건으로 제한한다.
6. strict/lowanchor는 safe branch의 핵심 축이므로 버리지 않는다. 다만 이번처럼 수익을 3~5%대로 죽이는 방향은 피하고, strict/lowanchor를 부분 조건 또는 상황별 브레이크로 사용하는 쪽이 낫다.
7. 다음 라운드는 8V5 상위 raw 후보의 진입 조건을 더 자르는 것이 아니라, 8V5의 2277 trades 근처를 최대한 보존하면서 MDD만 6.3에서 4.9대로 낮추는 구조를 목표로 한다.

다음 우선순위
1. V51 core_base의 raw edge 유지형 drawdown brake
2. V51 core_rare22_c1의 exit/hold/stop 재조정
3. strict/lowanchor safe branch와 core_base의 부분 혼합
4. shocklow를 단독 부모가 아니라 위험 구간 회피 필터로만 제한 사용
5. 8V6의 강한 mdd_compress 계열은 보관하되 주력 확장에서는 후순위 처리

최종 판정
8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3는 no_promotion이다.
공식 MDD 조건은 통과했지만 수익과 공식 cd_value가 크게 낮아졌다.
이번 라운드의 가장 중요한 학습은 V51의 MDD 문제를 진입 희소화로 해결하려 하면 edge가 먼저 죽는다는 점이다.
다음 단계는 진입을 더 자르는 방식이 아니라, core edge를 살린 상태에서 drawdown 구간만 선택적으로 눌러야 한다.