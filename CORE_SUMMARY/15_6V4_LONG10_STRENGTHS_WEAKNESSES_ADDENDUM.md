6V4_LONG10_REVIEWED 장단점 보정 메모

문서 목적
이 문서는 6V4_LONG10_REVIEWED 결과에서 드러난 장단점을 다음 전략 생성 규칙으로 바로 반영하기 위한 보정 문서다.
12번 본문과 13, 14 addendum 위에 이어 붙는 최신 규칙으로 사용한다.

배치 요약
공식 승격 없음.
공식 long 기준선은 여전히 6V2_L01_doubleflush_core 유지.

결과 핵심
- 6V4_L01_core_volcool_state: trades 0, final_return_pct 0.0000, max_return_pct 0.0000, max_drawdown_pct 0.0000, cd_value 100.0000
- 6V4_L02_core_oversold_reset: trades 0, final_return_pct 0.0000, max_return_pct 0.0000, max_drawdown_pct 0.0000, cd_value 100.0000
- 6V4_L04_extreme_volcool_state: trades 0, final_return_pct 0.0000, max_return_pct 0.0000, max_drawdown_pct 0.0000, cd_value 100.0000
- 6V4_L05_extreme_depth_reclaim: trades 1, final_return_pct -0.0177, max_return_pct 0.0000, max_drawdown_pct 0.0177, cd_value 99.9645
- 6V4_L06_extreme_regime_score: trades 44, final_return_pct -0.1578, max_return_pct 0.1927, max_drawdown_pct 0.3498, cd_value 99.4930
- 6V4_L03_core_regime_score: trades 67, final_return_pct -0.2640, max_return_pct 0.2167, max_drawdown_pct 0.4797, cd_value 99.2575
- 6V4_L07_reset_reclaim_rangeflip: trades 1701, final_return_pct 1.1176, max_return_pct 2.2483, max_drawdown_pct 1.7168, cd_value 99.3817
- 6V4_L10_failed_breakdown_trendflip: trades 334127, final_return_pct -97.1233, max_return_pct 0.0000, max_drawdown_pct 97.1251, cd_value 0.0827
- 6V4_L08_nested_sweep_reversal: trades 875873, final_return_pct -99.9947, max_return_pct 0.0055, max_drawdown_pct 99.9947, cd_value 0.0000
- 6V4_L09_volcrush_reclaim: trades 1644460, final_return_pct -100.0000, max_return_pct 0.0058, max_drawdown_pct 100.0000, cd_value 0.0000

강점 해석
1. 방향성 자체는 맞다.
6V3에서 확인한 post-signal 패턴 강화 실패 이후 state/position/regime 요소를 보려 했던 방향 전환 자체는 타당했다.
L03, L06처럼 40~70 trades 수준으로 줄어든 사례는 적어도 state 요소가 거래 억제에는 강하게 작동한다는 점을 보여준다.

2. extremeclose 계열은 still salvageable 하다.
L06_extreme_regime_score는 성과는 약했지만 44 trades, max_drawdown_pct 0.3498 수준으로 core 위에 얇은 품질 필터를 얹을 때 붕괴 없이 버틸 수 있는 여지를 보여줬다.
즉 L04 계열은 완전 폐기보다 soft score형으로 재가공할 가치가 있다.

3. 신규 전략도 MDD 관점에서 완전히 무가치는 아니다.
L07_reset_reclaim_rangeflip은 trades 1701로 많았지만 max_drawdown_pct 1.7168은 5% 미만이다.
즉 아이디어 자체가 완전히 틀린 것은 아니고, 거래 수 제어와 선택도 개선만 붙이면 재사용 가능성이 있다.

약점 해석
1. hard gate state filter는 과선택화로 무너졌다.
L01, L02, L04는 0트레이드, L05는 1트레이드였다.
즉 volatility cool, oversold reset, extreme vol cool, depth reclaim 같은 상태 필터를 core 위에서 동시 hard gate로 쓰면 샘플이 사실상 사라진다.
다음부터는 state를 필수 진입 조건으로 겹겹이 얹지 말고, soft score, rank, priority, tie-break 용도로 낮춰야 한다.

2. 신규 전략에는 기본적인 거래 수 억제 장치가 없었다.
L08, L09, L10은 각각 87만, 164만, 33만 trades 수준까지 폭증했다.
이는 전략 아이디어 이전에 signal cooldown, same-symbol refractory period, recent-fire suppression, one-shot rarity guard 같은 기본 안전장치가 빠졌다는 뜻이다.
다음 신규 전략은 아이디어가 무엇이든 이 장치들을 기본 옵션이 아니라 필수 장치로 넣어야 한다.

3. state filter는 단독 고정 임계값보다 상대 비교 점수형이 더 적합하다.
이번 실패는 volatility_cool_state_ok, oversold_reset_state_ok 같은 절대형 하드 조건이 종목별/국면별 차이를 흡수하지 못했음을 시사한다.
다음에는 최근 20~50봉 내 상대 순위, 분위수, 점수 합산, or top-k priority 방식으로 바꿔야 한다.

4. 신규 전략은 core 없이 단독 패턴으로 풀면 쉽게 과다거래화된다.
reset reclaim, nested sweep, volcrush reclaim, failed breakdown flip 계열은 이름상 매력적이지만, core context 없이 단독 발화 조건으로 만들면 모든 미세 변동을 다 잡아버린다.
다음에는 신규 전략도 최소한 context anchor를 둬야 한다.
예: 최근 N봉 내 shock 흔적 존재, 이전 flush 발생, distance-from-low 구간 제한, symbol-level cooldown 등.

다음 생성 규칙
1. L01 개선안은 3개만 유지하되, state 요소는 hard gate가 아니라 soft score로 넣는다.
예: core 진입은 유지하고, state score가 낮으면 skip하는 대신 tp/sl, 우선순위, 동시 진입 경쟁 해소에만 사용.

2. L04 개선안도 3개 유지하되, 6V4_L06처럼 상대적으로 덜 무너진 구조를 중심으로 간다.
extremeclose 코어에 regime_score를 약하게 결합하거나, recent shock 흔적이 있을 때만 통과시키는 정도로 제한한다.

3. 신규 전략 4개는 반드시 다음 4개 안전장치를 공통 내장한다.
- signal cooldown
- same-symbol refractory bars
- recent-fire suppression
- rarity guard or contextual anchor
이 4개 중 하나라도 빠진 신규 전략은 생성하지 않는다.

4. 다음 배치에서는 hard filter 수를 줄이고, 점수화와 단계화로 바꾼다.
권장 구조는 다음과 같다.
- step 1: core or anchor condition
- step 2: state score 0~N 산출
- step 3: 점수에 따라 진입 허용 또는 우선순위 배정
- step 4: cooldown/refractory로 재발화 억제

5. 과선택화와 과다거래를 동시에 경계한다.
다음 전략 생성 전 체크리스트:
- 최근 6V3처럼 0~9 trades 수준으로 죽는가?
- 최근 6V4처럼 1,000+ 또는 그 이상으로 폭증하는가?
- hard gate가 3개 이상 겹치는가?
- 신규 단독 패턴에 cooldown이 없는가?
이 중 하나라도 걸리면 설계를 다시 본다.

실전용 한 줄 요약
6V4의 교훈은 명확하다.
state는 hard gate가 아니라 soft score로, 신규 패턴은 자유 발화가 아니라 cooldown 달린 context 전략으로 다뤄야 한다.
