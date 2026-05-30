# LONG_MAIN_RESEARCH_LOG_2026_05_26_INTRABAR_RISK_SHAPE_V11

## 목적
롱 메인 새 원류 전략 탐색 11차 결과를 기록한다.
다음 대화창에서 동일한 Intrabar Risk Shape / Stop-Take Interaction 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
v8~v10에서 cross-sectional 계열은 우선순위를 크게 낮췄다.

- v8 Cross-Sectional Oversold Reversal: 실패
- v9 Cross-Sectional State Transition: 실패
- v10 Cross-Sectional Decoupling / Recoupling: 실패

따라서 v11에서는 종목 간 상대 비교를 버리고, 개별 종목 내부의 캔들 형태와 stop/take geometry를 보는 축으로 이동했다.

## 11차 시도
파일:
run_long_intrabar_risk_shape_v11_1h.py

결과 폴더:
local_results/long_main/LONG_INTRABAR_RISK_SHAPE_V11_1H

탐색 family:
- Lower Wick Reclaim Shape
- Compact Body Stop Geometry
- Down Sequence Absorption
- Low Prior Upper-Wick Noise Reclaim

핵심 가설:
롱 edge는 진입 패턴 자체보다, 진입 직전/진입 캔들의 high-low/wick/body/ATR 구조가 stop은 덜 맞고 take는 더 잘 맞는 형태일 때 발생할 수 있다.

조건 방향:
- lower wick 비율
- upper wick 제한
- close position
- body / ATR
- range / ATR
- wick balance
- prior upper wick noise
- prior down count
- ATR 기반 stop/take 거리
- 짧은 fail exit

## 결과
master_summary 기준:
- 후보 51개
- rows 51
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
v11은 cross-sectional 구조가 아니라 개별 캔들의 위험 형태와 stop/take interaction을 중심으로 설계했다.
그러나 현재 조건에서는 유효 후보가 전혀 나오지 않았다.

따라서 다음 구조는 현재 형태로 반복하지 않는다.

- lower wick reclaim 단독
- compact body stop geometry 단독
- prior down sequence absorption 단독
- low prior upper-wick noise reclaim 단독
- wick/body/range/ATR 조합만으로 long edge 탐색
- stop/take geometry만을 중심으로 한 단독 long entry

## 현재까지 제거된 long side 중심축
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry
7. cross-sectional oversold reversal
8. cross-sectional state transition
9. cross-sectional decoupling / recoupling
10. intrabar risk shape / stop-take interaction

## 살아남은 단서
v7 cross-sectional relative safety에서만 약한 TOP_ANY_MDD 후보가 있었지만, MDD가 높아 신규 기준선 후보로는 약하다.
현재 단계에서는 계속 새로운 정보축을 탐색하는 것이 우선이다.

## 다음 방향 후보
다음은 entry shape 자체가 아니라 holding-time edge를 탐색하는 것이 적합하다.

다음 후보:
Holding-Time Edge / Early Path Filter Long

핵심 가설:
같은 진입 조건이라도 진입 후 초반 N봉의 손익 경로가 유리한 시간창이 있을 수 있다.

탐색 아이디어:
- 진입 직후 1~3봉에서 불리하게 움직이면 빠르게 실패 처리
- 특정 hold window에서 TP 도달률이 높은 구조 탐색
- 고정 SL/TP는 유지하되 early adverse excursion 제한
- 초기 favorable excursion 발생 후 유지되는 구조
- entry signal보다 post-entry path compatibility를 중심으로 설계

주의:
다음 방향은 trailing stop이나 중간 TP 변경이 아니라, fixed SL/TP를 유지하면서 early fail exit와 holding window 적합성을 보는 것이다.
