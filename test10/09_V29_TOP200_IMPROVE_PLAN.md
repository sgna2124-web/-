v29 목적

이번 라운드는 top200 제거 실험이 아니다.
현재 1위인 official_top200_reference를 기준으로 더 개선하는 라운드다.
핵심 가설은 두 가지다.

1. v28에서 신호가 좋았던 wick normalization 조정은 top200 위에서도 cd_value 개선 가능성이 있다.
2. long 쪽은 건드리지 않고 short 쪽만 아주 약하게 더 엄격하게 만들면 수익 훼손을 최소화하면서 MDD와 max_conc를 방어할 수 있다.

실험 구성

기준선
- official_top200_reference

후보
- top200_wick06
- top200_rsi10
- top200_atr020
- top200_atr025_cap22
- top200_shortfloor_s19
- top200_shortfloor_s20
- top200_soft_asym_short
- top200_soft_asym_short_s19
- top200_soft_asym_short_s20
- top200_atr020_shortfloor_s19
- top200_atr025_cap22_shortfloor_s19
- top200_atr020_soft_asym_short

우선순위 해석

1순위
- top200_atr020
- top200_atr025_cap22
- top200_atr020_shortfloor_s19

2순위
- top200_shortfloor_s19
- top200_soft_asym_short
- top200_atr020_soft_asym_short

3순위
- 나머지 조합

판정 기준

반드시 아래 항목을 같이 본다.
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

특히 이번 라운드는 cd_value 개선 여부를 가장 먼저 본다.
단, cd_value가 소폭 좋아져도 최대 수익률 훼손이 크면 승격 보류다.
