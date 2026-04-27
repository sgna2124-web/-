8V6 이후 다음 단계 지시서

현재 공식 long 기준선
- 6V2_L01_doubleflush_core
- max_return_pct 23.9191
- max_drawdown_pct 1.7512
- official cd_value ratio 13.6587
- legacy_equity_cd_value 121.5300
- status: unchanged official long reference

8V6 결과 판정
- batch: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
- result: no_promotion
- failed_symbols: 0
- best: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18
- best max_return_pct: 5.2510
- best max_drawdown_pct: 2.1312
- best official cd_value: 2.4639
- conclusion: MDD 5 미만 압축은 성공했지만, V51 raw edge가 과도하게 손실됨.

핵심 학습
V51의 MDD를 낮추는 방향은 맞지만, 진입 전 필터를 강하게 추가하면 edge가 먼저 사라진다.
8V6은 8V5의 2277 trades 구조를 500~700 trades 수준으로 줄이면서 수익률도 41~42%대에서 3~5%대로 낮췄다.
따라서 다음 라운드는 진입 희소화가 아니라 edge 보존형 risk brake여야 한다.

다음 실험 방향
1. 부모 전략은 V51 core_base와 V51 core_rare22_c1을 유지한다.
2. shocklow는 단독 부모보다 위험 구간 보조 커버로만 사용한다.
3. strict/lowanchor는 safe branch 핵심 축으로 유지하되 전면 필터가 아니라 부분 브레이크로 사용한다.
4. 목표 trades는 8V5의 2277에 최대한 가깝게 유지한다.
5. 목표 MDD는 6.28~6.31에서 4.9대로 낮추는 것이다.
6. max_return_pct는 최소 30% 이상, 이상적으로 38~42% 보존을 목표로 한다.

금지 방향
- 8V6의 mdd_compress/hybrid_cover를 더 강하게 밀지 않는다.
- rare22 위에 추가 희소 필터를 계속 덧대지 않는다.
- quality_hold 다수 조합, 과도한 microguard, ema_mid, prevhigh, noshock14, vol16_quiet 계열은 주력 확장으로 쓰지 않는다.
- 새로운 family 탐색은 후순위다.

권장 개선 방식
1. 사후 drawdown brake
- 진입 조건은 거의 유지하고, 손실 군집 이후 짧은 cooldown 또는 재진입 제한만 적용한다.
- 특정 조건에서 모든 진입을 차단하지 말고, 직전 실패 패턴 직후만 제한한다.

2. 변동성 폭발 구간 일시 회피
- 진입 신호 전체를 줄이지 말고, 극단적 adverse volatility 직후 몇 캔들만 회피한다.
- V51의 microbase_pop 반복 구조를 살리는 것이 중요하다.

3. exit/hold/stop 재조정
- core_rare22_c1은 진입을 더 줄이지 말고 exit/hold/stop에서 MDD를 조절한다.
- 손절 폭을 무조건 좁히는 방식은 연속 손절을 만들 수 있으므로 ATR/캔들 범위 기반 적응형 조정이 낫다.

4. safe branch 부분 혼합
- strict/lowanchor를 entry gate로 전면 적용하지 않고, 위험 구간에서만 brake로 사용한다.
- 8V5 strict/lowanchor의 장점은 MDD 안정성이고 단점은 수익 축소다.

다음 라운드 설계 요약
- 300개를 다시 만든다면 구성은 다음이 적절하다.
  A그룹 100개: core_base edge 보존형 drawdown brake
  B그룹 100개: core_rare22_c1 exit/hold/stop 재조정
  C그룹 100개: strict/lowanchor/shocklow 부분 브레이크 혼합
- 평가 시 첫 기준은 MDD<5 여부지만, max_return_pct가 10% 미만이면 공식 후보로 보지 않는다.
- 이상적 후보는 MDD 4.8~4.99, max_return_pct 30% 이상, trades 1500 이상이다.

문서 업데이트 상태
- CORE_SUMMARY/26_8V6_TOP3_300_STRENGTHS_WEAKNESSES_ADDENDUM.md 추가 완료
- CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 에 8V6 항목 추가 완료
- CORE_SUMMARY/03_CURRENT_BASELINES.md 에 공식 cd_value ratio 보정 및 8V6 상태 반영 완료
- CORE_SUMMARY/27_NEXT_STEP_AFTER_8V6.md 추가 완료

다음 대화창 진입 시 반드시 읽을 것
1. CORE_SUMMARY/00_START_HERE.md
2. CORE_SUMMARY/03_CURRENT_BASELINES.md
3. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md
4. CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md
5. CORE_SUMMARY/25_8V5_LONG300_STRENGTHS_WEAKNESSES_ADDENDUM.md
6. CORE_SUMMARY/26_8V6_TOP3_300_STRENGTHS_WEAKNESSES_ADDENDUM.md
7. CORE_SUMMARY/27_NEXT_STEP_AFTER_8V6.md
8. CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md