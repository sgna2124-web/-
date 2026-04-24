6V3_LONG10_REVIEWED 장단점 추가 기록

목적
이 문서는 6V3_LONG10_REVIEWED 결과를 기반으로, 다음 long 전략 설계 전에 반드시 반영해야 할 장점/단점을 별도로 정리한 보정 문서다.
핵심은 6V2의 승리 구조를 유지하되, 6V3에서 실패한 후행 패턴 게이트를 반복하지 않도록 생성 규칙을 명문화하는 것이다.

배치 결과 요약
- 공식 승격 없음.
- batch best: 6V3_L04_core_redtogreen | trades 9 | final_return_pct 0.2983 | max_return_pct 0.3507 | max_drawdown_pct 0.0542 | cd_value 100.2439
- next best: 6V3_L08_extreme_inside_pop | trades 8 | final_return_pct 0.0975 | max_return_pct 0.0975 | max_drawdown_pct 0.0591 | cd_value 100.0384
- zero trade: 6V3_L03_core_precompress_release
- severe degradation: 6V3_L05_core_holdbreak_follow | trades 115 | final_return_pct -0.7699 | max_drawdown_pct 1.3228 | cd_value 97.9175

이번 라운드에서 확인된 장점
1. double flush 계열 코어 자체는 여전히 붕괴하지 않았다.
- 6V3의 상위권도 모두 L01/L04 계열 shock-reclaim 파생 구조에서 나왔다.
- 즉 다음 배치에서도 출발점은 double flush core / extreme close core 여야 한다.

2. red-to-green, inside-pop 같은 후속 확인은 방향성 설명력은 있다.
- 완전히 무의미한 조건은 아니었다.
- trades 8~9 수준이라 매우 적지만, 최상위 후보가 전부 이 계열에서 나왔다는 점은 후속 패턴이 아예 틀린 것은 아니라는 뜻이다.
- 다만 현재 방식처럼 독립 진입 트리거나 강한 추가 필터로 쓰면 너무 좁아진다.

3. extreme close 파생 구조는 계속 보관 가치가 있다.
- 6V2의 2위도 extreme close 계열이었고, 6V3에서도 inside-pop, ema20hold, vrecover 같은 파생 실험들이 모두 extreme 계열에서 파생되었다.
- 즉 L04 계열은 폐기 대상이 아니라, 재가공 대상이다.

이번 라운드에서 확인된 단점
1. post-signal 패턴을 새 진입 트리거로 격상하면 샘플 수가 급감한다.
- mid reclaim, ema20 snap, pre-compression, inside-pop 류는 대부분 0~9트레이드 수준으로 줄었다.
- 이런 구조는 전략 품질을 올리는 것이 아니라 전략 자체를 사라지게 만들 위험이 크다.

2. hold-break follow-through는 늦은 추격 진입으로 변질될 위험이 크다.
- L05는 trades 115로 갑자기 많아졌고, final_return_pct와 cd_value가 동시에 악화됐다.
- 이는 shock-reclaim 이후의 follow-through를 다시 추격하는 구조가, 본래의 역발상 저점 회수 엣지를 지워버릴 수 있음을 의미한다.

3. pre-compression은 현 코어와 결합 시 과선택화로 이어졌다.
- L03 0트레이드는 우연이 아니라 구조 경고로 봐야 한다.
- selective shock-reclaim 코어에 또 다른 희소 이벤트를 직렬 결합하면 재현성이 급감한다.

4. ema20/midline 재탈환은 보조 점수로는 의미가 있을 수 있어도, 단독 필수 게이트로는 과하다.
- L01/L06/L02/L07 계열 결과를 보면, 회수형 코어 위에 ema20 또는 range-mid reclaim을 강제하는 순간 trades가 크게 줄거나 품질이 오히려 약화된다.
- 즉 이런 요소는 hard gate보다 soft score에 가깝다.

생성 규칙으로 바꿔야 할 것
1. 다음 long 전략은 후행 패턴 추가형이 아니라 상태 진단 보강형으로 설계한다.
- 하지 말 것: red-to-green, inside-pop, hold-break, pre-compression을 진입의 주조건으로 승격.
- 할 것: double flush core 또는 extreme close core는 유지하고, 종목 상태 필터를 얇게 덧붙인다.

2. 얇은 상태 필터 후보
- 최근 1500캔들 기준 변동성 레짐 구간 필터
- 최근 과열/과매수 해소 여부
- 중기 하락 과확장 후 회수 상태 여부
- 종목별 과거 유사 상태 성과 점수
- 동일 코어 시그널의 최근 실패 누적 여부

3. hard gate보다 ranking/score 방식으로 옮긴다.
- ema20 reclaim, mid reclaim, red-to-green, inside-pop은 진입 필요조건으로 두지 말고 우선순위 점수나 포지션 사이징 점수에 반영하는 쪽이 낫다.
- 즉 yes/no 필터보다 가산점 구조가 적합하다.

4. 거래 수 경고 규칙
- 설계 단계에서 예상상 지나치게 희소한 이벤트를 직렬 결합하지 않는다.
- 결과 평가 단계에서 trades 20 미만 전략은 아이디어 기록은 하되, 공식 승격 후보로 보지 않는다.
- 0트레이드와 1트레이드 전략은 실패가 아니라 과선택화 경고로 따로 표시한다.

다음 배치 설계용 한 줄 결론
6V3는 double flush 승리 구조 위에 후행 패턴을 덧붙여 개선하려는 시도가 대부분 실패했다.
따라서 다음 long 개선은 패턴 추가가 아니라 상태 점수화, 위치 필터, 종목별 적응형 레짐 판단 쪽으로 옮겨야 한다.
