v36 목적

새 기준선은 rrff_baseline이다.
이번 라운드는 미세 조정이 아니라, rr_only + earlyreduce 코어 위에서 완전히 다른 축을 얹어보는 구조 탐색이다.

기준선 성과
- 최대 수익률 1359.0129%
- MDD -38.7698%
- 최대 보유 포지션 386
- 승률 29.5478%
- cd_value 893.9171

핵심 철학
- rr_only와 earlyreduce10/0.05는 코어 후보로 유지
- fail-fast, timeout 구조, RR 강도, stop 철학, guard 결합을 크게 흔들어 본다
- 작은 숫자 조정이 아니라 구조 변화를 본다

실험 축
1. 코어 분해
- rrcore_no_failfast
- rrcore_no_earlyreduce

2. 시간 구조 변경
- rrcore_timeout18
- rrcore_timeout40

3. RR 철학 변경
- rrcore_rr15
- rrcore_rr30
- rrcore_timeout40_rr30
- rrcore_timeout18_rr15

4. stop 구조 변경
- rrcore_wick_or_atr
- rrcore_wick_or_atr_asym_short_s22

5. guard 결합
- rrcore_asym_short_s22
- rrcore_asym_both_balanced

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

이번 라운드 핵심 질문
- fail-fast는 여전히 필요 없는가
- earlyreduce가 빠지면 정말 급격히 약해지는가
- rr_mult와 timeout을 크게 바꾸면 더 강한 수익/방어 조합이 나오는가
- wick_or_atr stop이 rr_only 코어와 결합하면 의미 있는 변화가 생기는가
- short/asym guard가 수익을 덜 해치면서 MDD를 줄일 수 있는가
