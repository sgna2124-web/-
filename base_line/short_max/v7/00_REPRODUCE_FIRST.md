# short_max v7 재현 우선 문서

이 폴더에서 공식 성과를 재현할 때 `strategy_code.py`만 복사하면 안 된다.

`strategy_code.py`는 전략의 진입/청산 정의를 설명하는 파일이고, 공식 결과는 다음 요소까지 포함한 포트폴리오 실행 엔진으로 산출되었다.

## 반드시 포함할 요소

- 597개 CSV 전체를 timestamp 기준으로 통합 평가
- 현재 equity 기준 `position_fraction = 0.01` 분할 진입
- `fee_per_side = 0.0004` 왕복 수수료 반영
- 신호 다음 봉 open 진입
- RSI 직접 gate 비활성화: `use_rsi_gate = False`
- RSI는 `short_score` 내부 보조 점수로만 사용
- `score_min_short = 2.35`는 entry mask 내부에서 적용
- 공식 trade generator는 `expected_tp >= 0.003`만 필수 검증한다. `target > 0` 같은 추가 조건을 넣으면 재현이 깨질 수 있다.
- `same-bar` 거래는 진입 직후 같은 timestamp에서 즉시 청산
- `dd_brake_mode = edge_current`: DD가 -3% 아래로 처음 진입하는 edge에서만 5 timestamp 신규 진입 차단
- DD가 -3% 아래에 계속 머문다고 freeze를 계속 연장하지 않는다.
- `active_leftover = 0` 확인

## 공식 기준선

- strategy: `short_max_v7_devw120`
- trades: 43,681
- max_return_pct: 1221.9746135454966
- max_drawdown_pct: 5.6636954922983485
- official_cd_value: 1247.1019969487918
- generated_trades_before_score_filter: 43,833
- blocked_by_guard: 152
- same_bar_trades: 3,694
- active_leftover: 0
- errors: 0

## 재현 실패 시 판정

`baseline_gate`가 실패하면 후보 개선 결과는 신뢰하지 않는다. 먼저 기준선 재현부터 맞춘다.

## source of truth

공식 재현의 source of truth는 `frozen_reproduce_runner.py`이다.
`strategy_code.py` 단독 복사는 금지한다.
