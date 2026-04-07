v41 목적

사용자 요구에 맞춰 이번 라운드는 파라미터 조정이 아니라 구조 조건 탐색이다.
새 기준선은 rr60_t300이다.
핵심은 숫자를 조금 만지는 것이 아니라, 어떤 상황에서 신규 진입 자체를 막을지를 실험하는 것이다.

기준선 성과
- 최대 수익률 4867.8295%
- MDD -31.4192%
- 최대 보유 포지션 385
- 승률 12.2145%
- cd_value 3409.1818

핵심 철학
- RR, timeout 숫자 조정보다 구조적 진입 차단 정책을 본다.
- burst가 너무 크면 그 시점 전체를 건너뛸지,
- short가 몰리면 short만 막을지,
- 한쪽 방향이 과도하게 우세하면 dominant side를 차단할지,
- active 포지션이 과열이면 일정 시간 신규 진입을 동결할지,
- long/short가 동시에 뜨면 minority side만 취할지,
- active side bias가 심하면 해당 방향 신규 진입을 막을지
를 비교한다.

실험 축
1. burst 차단
- struct_skip_total_burst
- struct_skip_short_burst

2. dominant side 차단
- struct_block_dominant_short
- struct_block_dominant_any

3. conflict 처리
- struct_minority_only_on_conflict

4. active 과열 동결
- struct_active_freeze

5. active side bias 차단
- struct_active_short_bias_block

6. 구조 조합
- struct_short_burst_plus_freeze
- struct_dominant_short_plus_freeze
- struct_minority_plus_active_bias
- struct_defense_combo

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

핵심 질문
- topN 없이도 과열 진입 차단만으로 MDD와 max_conc를 줄일 수 있는가
- short 쏠림을 막는 것이 실제로 효과가 있는가
- dominant side 차단이 수익 훼손 없이 방어력을 주는가
- active 포지션 과열 시 신규 진입 동결이 의미가 있는가
