v32 목적

현재 공식 기준선은 non_top200_reference_atr020이다.
이번 라운드는 수익 극대화보다 MDD 대폭 절감을 목표로 한다.
즉 개선의 1순위는 MDD고, 수익은 2순위다.

기준선 성과
- 최대 수익률 1096.0061%
- MDD -40.9433%
- 최대 보유 포지션 386
- 승률 37.8582%
- cd_value 722.12695

핵심 철학
- top200 계열은 더 이상 신뢰 기준으로 사용하지 않는다.
- 비랭킹 구조 유지
- 이번엔 진입을 더 까다롭게 하고, 위험 축소를 더 빠르게 한다.
- 수익이 조금 줄더라도 MDD가 의미 있게 내려가면 승격 후보로 본다.

실험 축
1. short threshold 강화
- mdd_short_s21
- mdd_short_s22

2. long/short 동시 강화
- mdd_balanced_l17_s22
- mdd_balanced_l17_s23

3. quality guard 강화
- mdd_asym_short
- mdd_asym_short_s22
- mdd_asym_both
- mdd_asym_both_s22

4. 조기 위험 축소
- mdd_early_reduce14_r012
- mdd_early_reduce14_r010_asym_short_s22
- mdd_early_reduce12_r010_asym_both_s22

5. wick 안정화 결합
- mdd_atr025_cap22_asym_short_s22

우선순위
1순위
- mdd_asym_short_s22
- mdd_early_reduce14_r010_asym_short_s22
- mdd_early_reduce12_r010_asym_both_s22

2순위
- mdd_balanced_l17_s22
- mdd_asym_both_s22
- mdd_atr025_cap22_asym_short_s22

3순위
- 나머지 조합

판정 기준
반드시 아래 5개를 같이 본다.
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

이번 라운드의 핵심 질문
- MDD가 얼마나 크게 줄었는가
- max_conc 386이 조금이라도 줄었는가
- cd_value가 너무 크게 무너지지 않는가
- 수익 감소가 감수 가능한 수준인가
