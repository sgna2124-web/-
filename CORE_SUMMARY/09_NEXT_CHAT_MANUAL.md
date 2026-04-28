새 대화창의 어시스턴트 행동 순서

1. 가장 먼저 CORE_SUMMARY/00_START_HERE.md 를 읽는다.
2. 그 다음 CORE_SUMMARY/03_CURRENT_BASELINES.md 를 읽어 현재 공식 기준선을 확인한다.
3. 그 다음 CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md 를 읽어 현재 백테스트 고정 환경을 확인한다.
4. 그 다음 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 읽어 현재 유효 결과만 파악한다.
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 읽어 최근 전략군의 구조적 장단점을 파악한다.
6. 최신 addendum인 CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/25_8V5_LONG300_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/26_8V6_TOP3_300_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/29_8V7_AB_BEST_200_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/30_8V8_LONG_DUAL_BEST_200_UNTRIED_ADDENDUM.md, CORE_SUMMARY/31_8V9_LONG_DUAL_BEST_200_NO_TRADE_CAP_ADDENDUM.md, CORE_SUMMARY/32_8V10_LONG_DUAL_LEADERS_400_NO_TRADE_CAP_ADDENDUM.md, CORE_SUMMARY/33_8V11_LONG_SHORT_MAIN_MAX_400_ADDENDUM.md, CORE_SUMMARY/34_8V12_LONG_SHORT_MAIN_MAX_400_ADDENDUM.md 를 읽는다.
7. CORE_SUMMARY/27_NEXT_STEP_AFTER_8V6.md 는 과거 참고로만 읽고, 최신 판단은 34번 addendum을 우선한다.
8. CORE_SUMMARY/28_BASELINE_AND_IMPROVEMENT_CANDIDATE_RULES.md 를 읽고 기준선 및 개선 후보 선정 규칙을 확인한다.
9. 이후 사용자 요청에 맞춰 전략 설계, 결과 해석, 문서 갱신을 진행한다.

새 대화창에서 반드시 확인할 현재 전제
공식 판정은 cd_value와 MDD 기준이다.
현재 프로젝트의 공식 cd_value는 사용자가 정의한 자산 기준 계산식으로 고정한다.

cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))

해석:
1) 기초 자산 100에 MDD를 먼저 적용한다.
2) MDD 적용 후 남은 자산에 max_return_pct를 적용한다.
3) final_return_pct는 공식 cd_value 계산에 사용하지 않는다.
4) max_return_pct / max_drawdown_pct 방식은 폐기된 비공식 ratio이며 앞으로 공식 cd_value로 쓰지 않는다.

현재 long 공식 기준선 6V2_L01_doubleflush_core의 official_cd_value는 121.7490이다.
계산: 100 * (1 - 0.017512) * (1 + 0.239191) = 121.7490
현재 short 공식 기준선은 short_beh_dd_brake다.
자산 진입 비중은 1%다.
수수료는 0.04%다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
결과 요약에는 max_return_pct가 반드시 포함되어야 한다.
거래 수 제한은 두지 않는다. 거래 수가 많아 손실이면 조건의 질이 낮은 것으로 해석한다.

기준선 및 개선 후보 선정 규칙
공식 기준선은 MDD 5% 미만 전략 중 공식 cd_value 1위다.
개선 후보는 매 배치마다 최대 2개를 뽑는다.
후보 A는 MDD 5% 미만 중 공식 cd_value 1위 전략이다.
후보 B는 MDD와 관계없이 전체 공식 cd_value 1위 전략이다.
후보 A와 후보 B가 같으면 중복 후보로 기록한다.
MDD가 5%를 넘더라도 전체 공식 cd_value 1위라면 다음 개선 후보로 올린다.
official_cd_value가 현재 공식 기준선보다 높고 MDD만 초과한 전략은 candidate_cd_win_mdd_fail로 강하게 표시한다.

현재 이름 규칙
long_main_v(기준선 버전)_(개선안 버전)_(전략명)
long_max_v(기준선 버전)_(개선안 버전)_(전략명)
short_main_v(기준선 버전)_(개선안 버전)_(전략명)
short_max_v(기준선 버전)_(개선안 버전)_(전략명)
예시: long_main_v1_1_strategy_name
main은 MDD 5% 미만 공식 cd_value 1위 기준선이다.
max는 MDD 무관 official_cd_value 1위 raw 개선 후보다.
main 또는 max를 명확히 넘는 뛰어난 전략이 나오면 기준선 버전을 v2, v3 식으로 올린다.
개선안만 이어가면 마지막 개선안 번호를 올린다.

현재 기준선 명칭
long_main_v1 = 6V2_L01_doubleflush_core
- max_return_pct 23.9191
- max_drawdown_pct 1.7512
- official_cd_value 121.7490

long_max_v1 = 8V4_V51_V002_core_rare22_c1
- max_return_pct 44.2664
- max_drawdown_pct 6.7587
- official_cd_value 134.515867~134.5172
- MDD 초과 raw 개선 후보

short_main_v1 = short_beh_dd_brake
- max_drawdown_pct 4.7589
- official_cd_value 약 392.214469 또는 legacy 391.9606
- max_return_pct가 포함된 최신 비교에서는 392.214469를 사용한다.

short_max_v1 = short_only_reference_1x
- max_return_pct 394.6145
- max_drawdown_pct 7.7792
- official_cd_value 456.137449
- MDD 초과 raw 개선 후보

V2 실험군 처리 원칙
V2 실험군은 환경 전제 오류가 있었으므로 실패 전략으로 해석하지 않는다.
4V2R1을 제외한 V2 전략과 결과는 제거되었다.
새 대화창의 어시스턴트는 삭제된 V2 실험군을 비교 기준이나 실패 사례로 인용하면 안 된다.

사용자와 어시스턴트의 역할
사용자는 로컬 백테스트를 실행하고 결과와 코드를 저장소에 올린다.
어시스턴트는 그 결과를 분석하고, 결과 카탈로그와 통합 요약을 갱신하며, 다음 전략을 제안한다.

결과 해석 전 점검 체크
자산 1% 진입이 반영되었는가
수수료 0.04%가 반영되었는가
FAST 예비검사가 개입되지 않았는가
결과 파일에 max_return_pct가 포함되었는가
공식 비교가 전체 종목 풀 백테스트 기준인가
거래 수가 0이거나 지나치게 적은 전략을 숫자만 보고 승격 후보로 착각하지 않았는가
cd_value가 사용자 정의 공식인 100 * (1 - abs(MDD)/100) * (1 + max_return_pct/100)로 계산되었는가
max_return_pct / max_drawdown_pct 비공식 ratio를 공식 cd_value로 착각하지 않았는가

반드시 해야 되는 일 목록
1. 사용자가 결과를 저장소에 올렸다면 local_results 또는 해당 결과 폴더를 먼저 확인한다.
2. 결과를 기존 공식 long-only / short-only 기준선과 비교한다.
3. MDD 5% 미만 중 official_cd_value 1위와 MDD 관계없는 전체 official_cd_value 1위를 각각 확인한다.
4. 두 후보가 같으면 중복 후보로 기록한다.
5. 단순 수치 비교로 끝내지 말고, 왜 성과가 나왔는지 장점과 단점을 함께 정리한다.
6. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
7. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 또는 별도 addendum을 갱신한다.
8. 승격이 발생하면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 같이 갱신한다.
9. 지표 정의 충돌이 발견되면 현재 공식 정의인 사용자 정의 cd_value를 기준으로 다른 문서를 정정한다.
10. 결과를 확인만 하고 문서 업데이트를 빼먹지 않는다.
11. 각 신규 배치 결과를 반영할 때, 배치 내 최고 후보를 max_return_pct, max_drawdown_pct, official_cd_value 기준으로 명시한다.
12. 전 전략이 탈락한 배치라도 과다거래, 방향 필터 부족, 진입 지연, 추세 위치 오류, edge 희석 같은 구조적 실패 원인을 문장으로 남긴다.
13. 압축 사다리, midband tag, wick accumulation처럼 거래 수가 비정상적으로 치솟는 구조를 발견하면, 재사용 금지 또는 추가 방향 필터 필요 여부를 명시한다.
14. 다음 전략을 제안하기 전에 방금 갱신한 장단점 기록을 다시 읽고, 그 항목을 실제 생성 규칙으로 반영한다.
15. 새 전략을 설명할 때는 최근 장단점 문서의 어떤 항목을 반영했는지 근거를 함께 적는다.
16. MDD 초과 전략은 공식 기준선으로 승격하지 않는다. 다만 전체 official_cd_value 1위라면 개선 후보로 기록한다.
17. 0트레이드 전략은 구조 검증 실패로 간주하고 별도 표시한다.
18. 전략 코드 생성 시 기존 백테스트 파일의 구조를 최대한 유지하고, 조건부 로직만 바꾸는 방식으로 작성한다.
19. 정의되지 않은 FeaturePack 필드, StrategyParams, entry_signal 참조 같은 과거 오류를 반복하지 않는다.
20. 업로드 전 py_compile 수준의 문법 검사를 통과시킨다.
21. print 출력은 갱신된 기준선만 상세 출력한다. 단, 네 축 모두 갱신 실패면 no baseline update 요약과 각 축 best candidate 요약만 출력한다.

최근 상태 인식
현재 공식 long 기준선은 6V2_L01_doubleflush_core다.
official_cd_value는 121.7490이다.
현재 공식 short 기준선은 short_beh_dd_brake다.
8V4와 8V5를 거치며 V51 microbase_pop 계열이 clear 최우선 long 코어가 되었다.
8V5의 핵심 후보는 다음과 같다.
- 8V5_V51P_V002_core_rare22_c1 | max_return_pct 42.1517 | max_drawdown_pct 6.3109 | official_cd_value 133.1863 | trades 2277
- 8V5_V51P_V001_core_base | max_return_pct 41.4900 | max_drawdown_pct 6.2801 | official_cd_value 132.6036 | trades 2277
- 8V5_V51P_V012_strict_rare22_c1 | max_return_pct 19.7596 | max_drawdown_pct 2.7359 | official_cd_value 116.4858 | trades 1040
8V6은 no_promotion이다.
8V7은 no_promotion이다.
8V8은 no_promotion이다.
8V9은 no_promotion이다.
8V10은 no_promotion이지만 8V8/8V9의 105대 정체를 115.524476까지 끌어올린 중요한 개선이다.
8V11은 no_promotion이며 long top은 114.028108, short top은 100.324360에 그쳤다.
8V12는 no_promotion이며 long top은 105.703904 또는 raw 108.517839, short top은 100.022693에 그쳤다.

8V10 핵심 후보
후보 A: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176
- type: MDD 5% 미만 official_cd_value 1위
- parent: 8V9_RAWV51_I013_entry_timing_window_r013
- group: b_rescue_mix
- trades: 1714
- max_return_pct: 20.9416
- max_drawdown_pct: 4.4791
- official_cd_value: 115.524476
- 의미: 안정성은 공식 조건에 들어왔고 거래 수도 좋으나 max_return_pct가 아직 부족하다.

후보 B: 8V10_B_ANYCD_I013_I302_b_trend_runner_b102
- type: MDD 무관 official_cd_value 1위
- parent: 8V9_RAWV51_I013_entry_timing_window_r013
- group: b_trend_runner
- trades: 1263
- max_return_pct: 26.3362
- max_drawdown_pct: 5.6679
- official_cd_value: 119.175585
- 의미: 공식 기준선 121.7490에 근접했지만 MDD가 5.6679라 승격 실패했다.

8V11 핵심 후보와 해석
8V11 long top: long_max_v1_51_lx_deep_absorb_lx051
- parent: 8V4_V51_V002_core_rare22_c1
- group: lx_deep_absorb
- trades: 1024
- max_return_pct: 18.2706
- max_drawdown_pct: 3.5871
- official_cd_value: 114.028108
- 의미: MDD 압축은 양호하지만 8V10 후보 A보다 cd_value가 낮다. 단독 심화보다 보조 모듈로 사용한다.

8V11 short top: short_max_v1_87_sx_vol_reversal_sx087
- parent: short_only_reference_1x
- group: sx_vol_reversal
- trades: 6
- max_return_pct: 0.3800
- max_drawdown_pct: 0.0554
- official_cd_value: 100.324360
- 의미: 극단적 저거래수라 기준 후보로 보지 않는다.

8V12 핵심 후보와 해석
8V12 long_mdd5_cd_1: long_max_v1_55_lx12_second_leg_absorption_lx12_2_14
- parent: 8V4_V51_V002_core_rare22_c1
- group: lx12_second_leg_absorption
- trades: 849
- max_return_pct: 7.0913
- max_drawdown_pct: 1.2955
- official_cd_value: 105.703904
- 의미: MDD 압축 보조 모듈로는 유효하지만 edge를 과도하게 깎으므로 단독 부모로 쓰지 않는다.

8V12 long_any_cd_1: long_max_v1_1_lx12_range_expansion_runner_lx12_0_00
- parent: 8V4_V51_V002_core_rare22_c1
- group: lx12_range_expansion_runner
- trades: 5737
- max_return_pct: 17.3243
- max_drawdown_pct: 7.5061
- official_cd_value: 108.517839
- 의미: 거래 밀도와 수익률 회복 모듈로는 가치가 있지만 MDD 방어가 약하다. hard entry 조건으로 반복하지 않는다.

8V12 short top: short_max_v1_25_sx12_pullback_continuation_sx12_1_04
- trades: 3
- max_return_pct: 0.0304
- max_drawdown_pct: 0.0077
- official_cd_value: 100.022693
- 의미: 검증 불능. 다음 부모 후보로 쓰지 않는다.

다음 우선순위
1. 8V10 후보 A b_rescue_mix의 MDD 4.4~4.8%를 유지하면서 max_return_pct를 23.9% 이상으로 올린다.
2. 8V10 후보 B b_trend_runner의 max_return_pct 26%대를 유지하면서 MDD를 4.9% 이하로 낮춘다.
3. 8V11 lx_deep_absorb/lx_trend_repair와 8V12 lx12_second_leg_absorption/lx12_range_expansion_runner/lx12_asymmetric_trail은 단독 부모가 아니라 보조 모듈로 혼합한다.
4. V51 strict_base / strict_rare22_c1 safe branch 복원은 계속 보조 축으로 유지한다.
5. V51 lowanchor_base / lowanchor_rare22_c1 safe branch 복원은 계속 보조 축으로 유지한다.
6. short는 다음 라운드에서 원본 short edge를 보존하는 방향으로 재설계해야 하며, 8V11/8V12 short 방식처럼 trades가 2~6회로 사라지는 강한 전단 필터는 반복하지 않는다.

다음 전략 설계 방향
새로운 family 탐색보다 V51 및 8V10 후보 심화가 우선이다.
8V7 top 전략이나 8V8 top 전략을 직접 부모로 쓰지 않는다.
8V11/8V12 long top은 직접 부모보다 보조 모듈로 쓴다.
목표는 8V10 A/B를 기준선으로 삼아 long 공식 기준선 121.7490을 넘기는 것이다.
A는 수익률 보강, B는 MDD 압축이 목적이다.
전단 entry filter보다 사후 drawdown brake, 손실 군집 회피, 변동성 폭발 직후 일시 회피, exit/hold/stop 재조정을 우선한다.
strict/lowanchor는 safe branch 핵심 축이지만 전면 필터가 아니라 부분 브레이크로 사용하는 것이 우선이다.
shocklow는 단독 부모가 아니라 위험 구간 보조 커버로 사용한다.
post_loss_brake, soft_safe_mix, raw_official_conversion, lx_deep_absorb, lx12_second_leg_absorption, lx12_range_expansion_runner는 유효성이 확인됐지만 hard filter가 아니라 부분 모듈로만 이식한다.

환경 오류 발생 시 처리
환경 오류가 확인되면 그 실험군은 invalid_env로 처리한다.
invalid_env 실험은 보존형 실패 기록이 아니라 제거 대상이다.
