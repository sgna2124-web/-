v35 목적

새 기준선은 advb_rr_only_failfast10이다.
이번 라운드는 미세 파라미터 조정이 아니라, rr_only + failfast + earlyreduce 구조에서 어떤 조건이 본체인지 분해해보는 라운드다.

기준선 성과
- 최대 수익률 1359.0129%
- MDD -38.7698%
- 최대 보유 포지션 386
- 승률 29.5478%
- cd_value 893.9171

핵심 철학
- rr_only 코어 유지
- fail-fast 제거, early-reduce 제거, guard 추가, stop 구조 변경, 방향 분해를 섞어서 본다
- cooldown과 wick_only처럼 이미 약했던 축은 주력으로 밀지 않는다
- 목적은 다음 라운드에서 rr_only 코어를 어디까지 고정하고 무엇을 버릴지 정하는 것

실험 축
1. 핵심 분해
- rrff_remove_failfast
- rrff_remove_earlyreduce
- rrff_ema_or_rr_failfast

2. guard 추가
- rrff_asym_short_s22
- rrff_asym_both_balanced_l18_s24
- rrff_asym_short_s22_remove_failfast
- rrff_asym_short_s22_remove_earlyreduce
- rrff_asym_short_s22_ema_or_rr

3. stop 구조 변경
- rrff_wick_or_atr_asym_both_s22

4. 방향 분해
- rrff_short_only
- rrff_long_only

핵심 질문
- rr_only가 본체인지 fail-fast가 본체인지
- early-reduce 10/0.05가 본체인지
- guard를 추가하면 수익이 무너지지 않으면서 MDD를 더 줄일 수 있는지
- short-only가 여전히 방어형 극단값을 보여주는지

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value
