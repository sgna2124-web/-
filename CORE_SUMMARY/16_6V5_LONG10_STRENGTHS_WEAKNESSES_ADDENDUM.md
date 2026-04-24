6V5_LONG10_REVIEWED 장단점 보정 메모

이 문서는 6V5_LONG10_REVIEWED 결과를 long 생성 규칙에 반영하기 위한 추가 메모다.
이번 배치는 L01 계열 5개, L04 계열 5개만으로 구성되었다.
핵심 목적은 6V4의 hard gate 과선택화와 과다거래 문제를 피하면서, 기존 double flush family 안에서 장점은 살리고 단점은 줄일 수 있는지 검증하는 것이었다.

배치 결과 요약
- best: 6V5_L05_core_score_shockfresh | final_return_pct 3.9127 | max_return_pct 4.3842 | max_drawdown_pct 1.0476 | cd_value 102.8241 | trades 337
- next: 6V5_L10_extreme_score_shockfresh | final_return_pct 2.5475 | max_return_pct 3.0029 | max_drawdown_pct 0.7294 | cd_value 101.7995 | trades 254
- next: 6V5_L06_extreme_score_balance | final_return_pct 2.4189 | max_return_pct 2.8736 | max_drawdown_pct 0.6719 | cd_value 101.7307 | trades 254
- L02_core_score_quiet, L07_extreme_score_quiet는 0트레이드였다.
- 나머지 전략들은 61~337 trades 범위, 0.62%~1.05% MDD 범위에 수렴했다.
- 공식 승격은 없었고, long 기준선은 여전히 6V2_L01_doubleflush_core 유지다.

이번 라운드에서 확인된 장점
1. soft score + spacing은 분명히 유효했다.
6V4에서 발생한 폭발적 과다거래는 이번 배치에서 사라졌다.
즉 state 요소를 hard gate가 아니라 완만한 점수화로 낮추고, signal spacing을 결합하는 구조는 거래수 통제 장치로는 효과가 있다.

2. shockfresh 축은 재사용 가치가 있다.
L05, L10이 각각 코어군과 extreme군에서 배치 1위와 2위를 차지했다.
즉 최근 shock/downflush 직후의 fresh rebound 문맥은 double flush family와의 궁합이 나쁘지 않다.
새 family를 만들더라도 recent shock age 또는 fresh dislocation 축은 재사용 후보로 본다.

3. extreme branch는 낮은 MDD 성향을 유지했다.
L10과 L06은 max_drawdown_pct가 각각 0.7294, 0.6719였다.
즉 L04 계열의 극단 위치 필터는 공격성은 약해도 방어력 측면의 성향은 여전히 긍정적이다.
새 family에서도 extreme-context branch를 보조 슬롯으로 둘 가치는 있다.

4. 이번 배치는 샘플 수가 완전히 죽지 않았다.
6V3, 6V4처럼 0트레이드/1트레이드 위주로 무너지지 않았고, 대부분 전략이 의미 있는 거래 수를 확보했다.
즉 후속 실험에서 signal spacing, recent-fire suppression, cooldown 기본 규칙은 유지 가치가 있다.

이번 라운드에서 확인된 단점
1. quiet gate는 반복적으로 과선택화로 이어진다.
L02, L07이 다시 0트레이드였다.
quiet_ratio 계열은 문서상 그럴듯해도 실제 long 승격용 엔트리 생성에는 지나치게 좁은 구조일 가능성이 높다.
향후 quiet는 단독 필수 gate로 쓰지 않는다.
필요하면 tie-break나 랭킹 보조점수 정도로만 제한한다.

2. score 덧칠만으로는 수익 엣지가 희석된다.
6V4의 hard gate 붕괴를 고친 대신, 이번에는 수익 잠재력이 지나치게 줄었다.
즉 double flush core 위에 보조점수를 더하는 방식은 안정화에는 기여하지만, 기준선 초과 성과를 만드는 방향으로는 약하다.
향후 같은 family 안에서 score 항목을 더 추가하는 반복은 우선순위를 낮춘다.

3. reclaim/trendfloor 보정은 core 강화보다 오히려 둔화로 이어졌다.
L03, L04, L08, L09는 모두 best보다 뒤처졌고, core 원형 대비 의미 있는 초과 성과가 없었다.
즉 reclaim strength나 trend floor는 long의 설명력은 있지만, double flush family 안에서 추가 필수요건으로 넣으면 edge를 강화하기보다 희석할 가능성이 높다.

4. current champion과의 격차가 너무 크다.
6V2_L01_doubleflush_core의 cd_value 121.5300 대비, 이번 best는 102.8241에 그쳤다.
단순 미세개선으로 메울 수 있는 차이가 아니다.
현재 family 내부 조정만으로는 승격 가능성이 낮다고 본다.

생성 규칙 업데이트
1. 다음 long 배치는 신규 family 개발 우선으로 전환한다.
현재 double flush family는 기준선 보유 family로 유지하되, 적극 확장 우선순위는 낮춘다.

2. 신규 family에도 다음 통제 장치는 기본 탑재한다.
- signal spacing
- recent-fire suppression
- same-symbol cooldown 또는 refractory bars
- 과다거래 발생 시 one-shot rarity 성격의 제어 장치

3. 신규 family에서 재사용할 가치가 있는 요소
- shockfresh 문맥
- extreme branch의 낮은 MDD 성향
- hard gate가 아닌 soft context weighting

4. 신규 family에서 피할 요소
- quiet를 필수 gate로 넣는 구조
- post-signal 패턴을 너무 많이 덧붙이는 구조
- 기존 코어 위에 score 항목만 계속 추가하는 구조

실전 해석
이번 6V5는 실패 배치이지만, 실패 방식이 중요하다.
6V4처럼 구조가 망가진 실패가 아니라, 제어는 성공했으나 엣지가 사라진 실패다.
즉 이제 long 쪽은 같은 family를 더 안전하게 다듬는 단계보다, 새로운 edge source를 찾는 단계로 넘어가는 것이 맞다.
다음 배치에서는 기존 family 개선보다 신규 long family 발굴을 우선한다.
