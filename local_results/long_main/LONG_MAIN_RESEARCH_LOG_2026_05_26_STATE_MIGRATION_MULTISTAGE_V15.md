# LONG_MAIN_RESEARCH_LOG_2026_05_26_STATE_MIGRATION_MULTISTAGE_V15

## 목적
롱 메인 새 원류 전략 탐색 15차 결과를 기록한다.
다음 대화창에서 v15를 단순 실패로 오해하지 않고, 반응이 나온 하위 family만 이어가기 위한 append 로그다.

## 이전 배경
v8~v14에서 다음 신규 정보축이 실패했다.

- v8 Cross-Sectional Oversold Reversal
- v9 Cross-Sectional State Transition
- v10 Cross-Sectional Decoupling / Recoupling
- v11 Intrabar Risk Shape / Stop-Take Interaction
- v12 Holding-Time Edge / Early Path Filter
- v13 Compression / Expansion Microcycle
- v14 Time-Position / Cycle Transition Edge

v15에서는 v9처럼 1-step 변화량을 본 것이 아니라, 여러 구간의 상태 이동 순서를 테스트했다.

## 15차 시도
파일:
run_long_state_migration_multistage_v15_1h.py

결과 폴더:
local_results/long_main/LONG_STATE_MIGRATION_MULTISTAGE_V15_1H

탐색 family:
- Selloff Calm Reclaim
- Drawdown Volatility Slowdown
- Weak Contract Recovery
- Strict Multi-Stage Migration

핵심 가설:
롱 edge는 한 시점의 상태가 아니라 최근 N봉 동안 상태가 다음 순서로 이주했을 때 발생할 수 있다.

예시:
1. 이전 구간: 하락 / 약세
2. 중간 구간: 변동성 둔화 또는 매도 압력 완화
3. 최근 구간: 회복 시도
4. 현재: 재하락 실패 또는 회복 확인

## 결과
master_summary 기준:
- 후보 36개
- rows 36
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 2개 존재
- BEST_BY_FAMILY 1개 존재

TOP_ANY_MDD:
1. SMG_A_008
   - family: selloff_calm_reclaim
   - verdict: valid_any_mdd
   - cd: 53.469370
   - max_return_pct: 0.078656
   - max_drawdown_pct: 46.572654
   - trades: 9716

2. SMG_A_007
   - family: selloff_calm_reclaim
   - verdict: valid_any_mdd
   - cd: 49.470364
   - max_return_pct: 0.214244
   - max_drawdown_pct: 50.635397
   - trades: 10892

## 판정
기준선 후보로는 실패.
MDD가 약 46~50%로 너무 높아 레버리지 적용 전제에서는 탈락이다.

다만 v8~v14와 다르게 TOP_ANY_MDD 후보가 발생했다.
따라서 v15는 완전 무효 축이 아니라 '반응은 있으나 리스크가 과도한 축'으로 분류한다.

## 중요한 결론
제거 금지:
- selloff_calm_reclaim

제거 또는 우선순위 하향:
- drawdown_vol_slowdown
- weak_contract_recovery
- strict_multistage_migration

이유:
실제 반응이 나온 family는 selloff_calm_reclaim 하나뿐이다.

## 다음 방향
v16은 완전 신규 축이 아니라 selloff_calm_reclaim 계열을 확대/세분화한다.

개선 방향:
1. selloff 강도 구간 세분화
2. calm 조건을 완화/강화한 버전 분리
3. reclaim 방식 세분화
4. MDD 압축용 risk gate 추가
5. 거래 수가 과도하므로 trade density 감소 조건 추가
6. 최근 저점 이탈 실패 확인 추가
7. market/segment/candle shape를 보조 필터로 섞되, cross-sectional rank 중심 접근은 피한다.

## 반복 금지
다음 단계에서 v15 전체를 폐기하지 말 것.
반드시 selloff_calm_reclaim 하위 family를 중심으로 확장한다.
