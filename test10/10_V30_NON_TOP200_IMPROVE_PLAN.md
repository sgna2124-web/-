v30 목적

이제부터 official_top200_reference는 공식 기준선에서 제외한다.
이 라운드의 기준선은 non-top200 1위인 score_l16_s20_shortheavy_atr020이다.
즉 새 기준선 이름은 아래와 같다.
- non_top200_reference_atr020

기준선 성과
- 최대 수익률 1096.0061%
- MDD -40.9433%
- 최대 보유 포지션 386
- 승률 37.8582%
- cd_value 722.12695

핵심 철학
- top200은 더 이상 신뢰 기준으로 두지 않는다.
- cross-sectional topN cap 없이도 설명 가능한 구조만 개선한다.
- 이번 라운드는 atr020 기반 비랭킹 구조 개선이다.

실험 축

1. wick 안정화
- non_top200_wick06
- non_top200_atr020_wick06
- non_top200_atr025_cap22
- non_top200_atr025_cap22_wick06

2. short side 강화
- non_top200_atr020_short_s21
- non_top200_atr020_short_s22
- non_top200_atr025_cap22_short_s21

3. short-only soft asym
- non_top200_atr020_soft_asym_short
- non_top200_atr020_soft_asym_short_s21
- non_top200_atr025_cap22_soft_asym_short
- non_top200_atr025_cap22_soft_asym_short_s21

4. 보조 축
- non_top200_atr020_rsi10

우선순위
1순위
- non_top200_atr020_wick06
- non_top200_atr025_cap22
- non_top200_atr025_cap22_wick06

2순위
- non_top200_atr020_soft_asym_short
- non_top200_atr020_soft_asym_short_s21
- non_top200_atr025_cap22_soft_asym_short

3순위
- 나머지 조합

판정 기준
반드시 아래 5개를 같이 본다.
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

특히 이번에는 max_conc 386을 조금이라도 낮출 수 있는지가 중요하다.
다만 수익 훼손이 너무 크면 승격하지 않는다.
