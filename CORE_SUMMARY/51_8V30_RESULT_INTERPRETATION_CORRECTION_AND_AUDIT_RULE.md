8V30 결과 해석 정정 및 백테스트 감사 규칙

작성 이유
8V30 결과에서 사용자가 중요한 논리 오류를 지적했다. 기준선 전략에 TP 기대값 0.3% 이상 진입 조건을 추가했다면 거래 수는 같거나 줄어야 한다. 그런데 8V30 long TP03-only 후보는 기준선보다 거래 수가 크게 증가했다. 이는 TP03 조건의 효과로 해석할 수 없다.

정정 결론
8V30의 TP03-only 결과는 TP03 조건의 순수 효과로 보지 않는다. 8V30 결과는 기준선과 improve 후보가 같은 실행 경로에서 비교되지 않았을 가능성을 보여주는 감사 신호로 본다.

근거 1: TP03-only가 실제로 조건을 더 좁히지 않았다
8V30 전략 목록에서 long_main 기준선과 8V30_long_main_001_tp03_only_probe는 주요 조건값이 동일하다.
- baseline long_main atrp_min: 0.003
- TP03-only long_main atrp_min: 0.003
- stop_atr: 1.04
- rr: 1.85

단순 ATR 기반 TP 기대값 조건을 atrp_min >= 0.003 / (stop_atr * rr) 방식으로 구현했다면, long_main의 필요 atrp_min은 약 0.00156이다. 기존 atrp_min 0.003이 이미 이보다 높기 때문에 TP03-only 후보는 실질적으로 기준선보다 더 엄격해지지 않았다.

long_max도 동일하다.
- stop_atr: 1.10
- rr: 2.05
- 필요 atrp_min 약 0.00133
- 기존 atrp_min: 0.0035
따라서 TP03-only는 long_max에서도 실질적인 신규 필터가 아니다.

short_main/short_max도 동일하다.
- stop_atr: 1.8975
- rr: 6.0
- 필요 atrp_min 약 0.000264
- 기존 atrp_min: 0.0018
따라서 TP03-only는 숏에서도 실질적인 신규 필터가 아니다.

근거 2: 실질 조건이 같다면 결과도 같아야 한다
같은 데이터, 같은 엔진, 같은 entry/exit, 같은 수수료, 같은 포지션 비중이라면 TP03-only 후보는 기준선과 거의 같은 거래 수/수익/MDD를 보여야 한다.
그러나 8V30 결과는 다음과 같이 크게 다르다.
- long_main 기준선 trades 592 vs TP03-only trades 13116
- long_max 기준선 trades 2276 vs TP03-only trades 433571
- short_main 기준선 trades 28017 vs TP03-only trades 1032
- short_max 기준선 trades 36505 vs TP03-only trades 3197

이는 TP03 효과가 아니라 baseline reference 경로와 improve 후보 실행 경로가 서로 다르다는 신호다.

근거 3: baseline row는 실측 clone이 아니라 embedded reference일 가능성이 높다
8V30 registry의 기준선 행 note는 embedded_reference_pass_no_repo_path_dependency로 기록된다. 즉 baseline row는 현재 improve 후보와 같은 방식으로 계산된 clone 결과가 아니라, 코드에 박아 둔 기준선 reference 값일 가능성이 있다.

따라서 다음과 같이 정정한다.
기존 해석: TP03-only가 long에서는 거래 폭증, short에서는 거래 기근을 만들었다.
정정 해석: TP03-only라는 이름의 후보조차 기준선 clone을 재현하지 못했다. 따라서 TP03의 효과를 논하기 전에 baseline과 improve 실행 경로 일치 여부부터 검증해야 한다.

수수료/포지션 비중 감사
8V30 generated 코드에는 POS_FRAC = 0.01로 되어 있어 자산 1% 진입 비중은 equity_stats에서 적용된다.
하지만 COST_PCT = 0.10으로 되어 있다. 사용자의 공식 고정 환경은 수수료 0.04%다. 따라서 현재 코드의 수수료 상수는 공식 환경과 불일치한다.

중요:
- COST_PCT가 거래당 총 비용 0.10%라면 공식 0.04%보다 크다.
- 공식이 진입 0.04% + 청산 0.04%의 왕복 0.08%라 하더라도 0.10%는 여전히 다르다.
- 수수료가 0.10%로 되어 있으면 결과가 더 보수적으로 왜곡될 수 있다.
- 다음 백테스트 전에는 수수료 적용 위치와 횟수도 반드시 감사한다.

MDD 해석 보정
거래 수가 줄어도 MDD가 커지는 것은 이론상 가능하다. 줄어든 거래가 손실 군집만 선택하거나, 기준선의 회복 거래를 제거하면 거래 수는 줄어도 equity curve의 drawdown은 커질 수 있다.
하지만 8V30에서는 그보다 먼저 기준선 clone 재현 실패가 확인되므로, 현재 MDD 수치는 전략적 의미로 해석하지 않는다.

다음 단계 강제 규칙
1. 다음 버전은 개선 배치가 아니라 감사 배치로 만든다.
2. 이름 예시: 8V31_AUDIT_CLONE_TP03_FEE
3. 기준선 4개를 embedded reference로만 두지 말고, 같은 improve 실행 경로에서 clone 후보를 반드시 별도로 계산한다.
4. clone 후보는 base_spec(axis) 그대로 사용하며 name/kind/tag만 바꾼다.
5. clone 후보에는 TP03, 손실 컷, 완화, 강화, 파라미터 변경을 절대 넣지 않는다.
6. clone이 기준선과 trades/max_return/MDD를 재현하지 못하면 그 축의 개선은 중단한다.
7. TP03 효과는 clone이 통과한 축에서만 별도 후보로 측정한다.
8. TP03은 atrp_min 대체 방식이 아니라 실제 기대 TP 조건으로 명시 검증해야 한다.
9. 수수료는 사용자 공식 환경인 0.04%에 맞춘다. 왕복 기준인지 단방향 기준인지 코드 변수명으로 명확히 구분한다.
10. 진입 비중 1%는 POS_FRAC = 0.01이 equity 계산에 반영되는지 로그로 확인한다.

무효 처리
8V30 TP03-only 결과는 TP03의 장단점 기록으로 사용하지 않는다. 8V30은 clone failure / path mismatch / fee mismatch를 드러낸 감사 이벤트로 기록한다.

기존 문서 보정
CORE_SUMMARY/49_8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_PLAN.md 와 CORE_SUMMARY/50_8V30_RESULT_AND_NEXT_DIRECTION.md 의 TP03-only 해석은 이 문서가 우선한다.
특히 00_START_HERE에 남아 있는 TP03 필수 적용 문구는 현재 기준으로 보류한다. 기준선 clone 및 수수료 감사가 끝나기 전까지 TP03을 신규 개선안의 공통 필수 조건으로 적용하지 않는다.
