v31 목적

v30까지의 결론은 명확하다.
- score 미세조정만으로는 non-top200 기준선을 넘기 어렵다.
- max_conc 386이 전혀 내려오지 않는다.
- 따라서 다음 단계는 같은 축 미세조정이 아니라 비랭킹형 노출 제어다.

이번 v31의 핵심
- 종목을 정렬하지 않는다.
- topN을 사용하지 않는다.
- 특정 시점의 모든 후보에게 동일한 동적 문턱을 적용한다.
- 활성 포지션 수가 높아질수록 점수 하한을 자동으로 높인다.
- burst 시점에서는 short 쪽 문턱을 추가로 높인다.

즉 이 실험은 cross-sectional ranking 없이 과열 구간을 제어하는 첫 라운드다.

기준선
- non_top200_reference_atr020

동적 문턱 규칙
- active_count가 soft_cap을 넘으면 step마다 long/short score floor를 추가 상향
- burst_count가 burst_threshold를 넘으면 long/short burst boost를 추가 상향
- 모든 후보는 정렬 없이 동일 규칙을 적용받음

주요 조합
- guard_short_soft
- guard_short_med
- guard_short_burst180
- guard_short_burst150
- guard_balanced_soft
- atr025_cap22_guard_short_soft
- atr025_cap22_guard_short_burst180
- wick06_guard_short_soft
- wick06_guard_short_burst180
- atr025_cap22_wick06_guard_short_soft
- atr025_cap22_wick06_guard_short_burst180
- soft_asym_short_guard_soft

우선순위
1순위
- guard_short_burst180
- atr025_cap22_guard_short_burst180
- atr025_cap22_wick06_guard_short_burst180

2순위
- guard_short_soft
- atr025_cap22_guard_short_soft
- wick06_guard_short_soft

3순위
- 나머지 조합

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

이번 라운드에서 가장 중요한 질문
- max_conc 386이 실제로 내려오는가
- 수익 훼손을 감수하더라도 cd_value가 유지되거나 올라가는가
- burst 시점 제어가 topN 없이도 의미 있게 작동하는가
