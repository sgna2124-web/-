cd_value 및 결과 보고 규칙

최근 사용자 지시로 확정된 cd_value 정의
- cd_value = 기존 자산에 MDD를 먼저 적용하고, 적용한 값에 최대 수익률을 적용한 값
- 현재 프로젝트에서는 초기자산 100을 기준으로 계산
- 실사용 계산식
  cd_value = 100 × (1 - |mdd_pct|/100) × (1 + final_return_pct/100)

해석 예시
- 수익이 높아도 MDD가 크면 cd_value가 깎인다
- MDD가 매우 낮아도 수익이 거의 없으면 cd_value가 크게 오르지 않는다
- 즉 현재 목적과 잘 맞는 종합 지표로 사용할 수 있다

최근 확정된 사용자 정렬 규칙
- 먼저 MDD 5% 미만 전략만 남긴다
- 그 안에서 cd_value 내림차순으로 정렬한다
- 필요 시 숏 3위까지, 롱 3위까지처럼 별도 표기한다

보고 형식 추천
숏 전용 TOP 3
1위 전략명
- 최대수익률
- MDD
- cd_value
- 필요 시 PF, max_conc

롱 전용 TOP 3
1위 전략명
- 최대수익률
- MDD
- cd_value
- 필요 시 PF, max_conc

현재 구현 상태
- 새 summary 스크립트 summarize_results_json_only_short_strict_cd.py가 cd_value와 delta_cd_value를 master_summary에 포함한다
- v66, v67 wrapper는 이 새 스크립트를 사용한다
- 과거 family들은 이전 summary 스크립트로 생성되어 cd_value가 자동으로 없을 수 있다. 이 경우 수동 계산 또는 재요약이 필요하다

다음 어시스턴트가 해야 할 일
1. 새 family를 만들면 가능하면 cd_value 포함 summary wrapper를 사용한다
2. 결과 정렬 요청이 오면, 숏과 롱을 분리한다
3. 먼저 MDD 5% 미만 필터를 적용한다
4. 그 뒤 cd_value 순으로 정렬한다
5. 사용자가 3위까지만 원하면 3위까지만 출력한다

현재 참고용 최신 순위
숏 최근 family(v66) 기준
1) short_balanced_bridge_atr050_prior1_24
2) short_balanced_bridge_wick075_dense30
3) short_balanced_bridge_wick075_prior1_24

롱 최근 family(v67) 기준
1) long_hybrid_wick_bridge_halfhalf
2) long_hybrid_wick_bridge_quiet48
3) long_hybrid_wick_bridge_us_max40

주의
- 사용자가 전체 역사 기준 순위를 원하면, 단순히 최신 family만 보지 말고 과거 강한 후보까지 함께 계산해야 한다
- 최근 실제 전체 역사 기준 숏 상위권은 short_beh_dd_brake, short_div_dense_skip30, short_beh_conservative_combo 쪽이 여전히 강하다
- 롱은 아직 과거 후보보다 최근 v67 계열이 MDD 5% 미만 + cd_value 조건에서 더 자주 상위권에 오른다
