현재 상태 및 상위 후보군 정리

주의
- 이 문서는 최신 대화창 기준 정리다.
- 과거 문서와 숫자가 조금 다를 수 있다. 최근 결과를 우선한다.
- 사용자가 최근 실제로 요구한 정렬 기준은 다음과 같다.
  MDD 5% 미만만 남기고, cd_value 내림차순으로 정렬

cd_value 계산식
- cd_value = 100 × (1 - |mdd_pct|/100) × (1 + final_return_pct/100)

현재 숏 전용 상위 후보군

A. 최근 전체 기준 MDD 5% 미만 + cd_value 상위 3
1) short_beh_dd_brake
- 최대 수익률 311.5456%
- MDD -4.7589%
- cd_value 391.9606
- 해석: 현재 숏 메인형 최상위권 후보. 수익과 방어의 균형이 매우 좋다.

2) short_div_dense_skip30
- 최대 수익률 251.3963%
- MDD -3.6805%
- cd_value 338.4632
- 해석: 밀집 타임스탬프 회피 철학이 유효했다. max_conc 억제 측면에서도 의미가 크다.

3) short_beh_conservative_combo
- 최대 수익률 144.8252%
- MDD -2.5182%
- cd_value 238.6600
- 해석: 극방어형에 가장 가깝지만 수익도 완전히 죽지 않았다.

B. 추가 핵심 후보
- short_next_rr30_t40_s22
- short_session_dense30_prior2_win48
- short_div_reentry_gap48
- short_div_first_after_quiet48

C. 공격형 별도 후보군
- v62 short_split_pure_atr050_2bar
  수익률 379.3259%, MDD -6.8730%, max_conc 531
- v62 short_split_pure_atr025_1bar
  수익률 334.6562%, MDD -7.5063%, max_conc 567
- v62 short_split_pure_wick075_2bar
  수익률 276.7436%, MDD -6.3551%, max_conc 515
- 해석: 수익은 강력하지만 동시포지션 과다가 심하다. 공격형 separate track으로 유지.

D. 최근 bridge형 후보(v66)
- short_balanced_bridge_atr050_prior1_24
  수익률 20.3501%, MDD -3.9261%, cd_value 115.6250
- short_balanced_bridge_wick075_dense30
  수익률 18.8686%, MDD -4.8026%, cd_value 113.1598
- short_balanced_bridge_wick075_prior1_24
  수익률 16.0450%, MDD -4.5060%, cd_value 110.8160
- 해석: 공격형과 방어형의 중간지대를 찾으려는 family. 아직 메인 교체 수준은 아니지만 구조 힌트는 있다.

현재 롱 전용 상위 후보군

A. 최근 전체 기준 MDD 5% 미만 + cd_value 상위 3
1) long_hybrid_wick_bridge_halfhalf
- 최대 수익률 9.9603%
- MDD -1.0456%
- cd_value 108.8106
- 해석: 최근 롱 계열 중 cd_value 기준 1위. 수익과 저MDD의 조합이 가장 낫다.

2) long_hybrid_wick_bridge_quiet48
- 최대 수익률 5.3621%
- MDD -0.4434%
- cd_value 104.8949
- 해석: 극저MDD형이면서 quiet 철학이 유효했다.

3) long_hybrid_wick_bridge_us_max40
- 최대 수익률 3.3983%
- MDD -0.3394%
- cd_value 103.0473
- 해석: US 시간대 + active cap 40 조합이 롱에서 꽤 안정적이다.

B. 추가 참고 후보
- long_hybrid_wick_bridge_us_only
- long_hybrid_wick_bridge_onethird_us_only
- long_guarded_wick_split_baseline_quiet48
- long_guarded_wick_split_baseline_us_only

C. 과거 핵심 메인 철학 후보
- long_hybrid_symbol1_dd_confirmation 계열
- long_hybrid_confirmation24 계열
- 해석: 롱 전용 메인 철학의 기준선 역할을 했으나, 최근 67 계열이 이를 대체/보강할 수 있는지 확인하는 중.

현재 해석 요약
숏
- 메인형은 여전히 short_beh_dd_brake, short_div_dense_skip30, short_beh_conservative_combo가 강하다.
- 공격형은 v62 split 계열을 별도로 유지한다.
- 중간지대/bridge형은 v66이 담당한다.

롱
- 아직 압도적 메인형은 없다.
- 최근에는 wick bridge 계열이 가장 유망하다.
- 극저MDD는 만들 수 있지만, 수익을 더 키우는 것이 핵심 과제다.

현재 다음 대화창에서 바로 참고할 추천 우선순위
숏 우선 참고
1. short_beh_dd_brake
2. short_div_dense_skip30
3. short_beh_conservative_combo
4. v62 공격형 split 계열
5. v66 bridge 계열

롱 우선 참고
1. long_hybrid_wick_bridge_halfhalf
2. long_hybrid_wick_bridge_quiet48
3. long_hybrid_wick_bridge_us_max40
4. long_guarded_wick_split_baseline_quiet48
5. 과거 long_hybrid_symbol1_dd_confirmation 철학
