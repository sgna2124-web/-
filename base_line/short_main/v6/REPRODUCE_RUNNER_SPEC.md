# short_main v6 재현 러너 사양

공식 결과를 재현할 때는 전략 정의만 복사하면 안 된다. 전체 포트폴리오 실행 사양까지 동일해야 한다.

필수 구성:

1. CSV 597개 로딩
2. EMA20, RSI14, ATR14 계산
3. short_score 계산
4. score gate를 entry mask 내부에서 적용
5. 신호 다음 봉 open 진입
6. 전체 심볼 거래를 timestamp 기준으로 통합
7. 현재 equity의 1%로 진입 금액 계산
8. 편도 수수료 0.0004, 왕복 0.0008 차감
9. 같은 timestamp 진입 청산 즉시 처리
10. drawdown이 -3% 아래로 처음 내려가는 edge에서만 5 timestamp 신규 진입 차단
11. baseline gate 검증

공식 기준값:

strategy: short_main_v6_timeout210
trades: 33989
max_return_pct: 931.6464095007982
max_drawdown_pct: 4.506694290977831
official_cd_value: 985.153259660748
generated_trades_before_score_filter: 34019
active_leftover: 0
errors: 0

핵심 설정:

score_dev_weight: 1.0
timeout_bars: 210
fee_per_side: 0.0004
position_fraction: 0.01
use_rsi_gate: false
score_min_short: 2.35
dd_brake_mode: edge_current

추가 주의:

공식 trade generator와 동일하게 조건을 맞춰야 한다. 임의 필터를 추가하면 거래 수가 달라질 수 있다.
