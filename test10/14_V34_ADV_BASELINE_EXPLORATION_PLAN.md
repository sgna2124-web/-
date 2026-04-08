v34 목적

새 기준선은 adv_earlyreduce10_r005다.
이번 라운드는 미세 파라미터 조정이 아니다.
새 1위를 기준으로 조건을 추가, 제거, 변경하면서 구조가 어떻게 달라지는지 크게 흔들어 보는 라운드다.

기준선 성과
- 최대 수익률 1322.3922%
- MDD -39.1797%
- 최대 보유 포지션 386
- 승률 31.0495%
- cd_value 865.6453

핵심 철학
- 작은 값 조정 금지
- 조건의 존재 자체를 바꾼다
- 방향 제거, 청산 철학 변경, stop 구조 변경, cooldown, fail-fast, 강한 guard 결합을 동시에 본다
- 목적은 다음 라운드에서 버릴 축과 밀 축을 분명히 만드는 것

실험 축
1. 방향 제거
- advb_long_only
- advb_short_only

2. 청산 철학 변경
- advb_rr_only
- advb_ema_or_rr
- advb_rr_only_failfast10
- advb_ema_or_rr_cooldown12

3. 거래 템포 변경
- advb_failfast12_r010
- advb_cooldown12

4. 진입 강화
- advb_asym_short_s22
- advb_asym_both_balanced_l18_s24
- advb_asym_both_cooldown12
- advb_strict_combo

5. stop 구조 변경
- advb_wick_or_atr_asym_both_s22
- advb_wick_only_asym_short_s22

우선순위
1순위
- advb_rr_only
- advb_wick_or_atr_asym_both_s22
- advb_strict_combo

2순위
- advb_ema_or_rr
- advb_asym_both_balanced_l18_s24
- advb_asym_short_s22

3순위
- 나머지 전부

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

이번 라운드의 핵심 질문
- 조기 risk reduction이 1위를 만든 핵심인지
- RR only가 더 강한 수익 확대를 만드는지
- EMA 기반 청산이 제거되면 수익과 MDD가 어떻게 바뀌는지
- 강한 진입 강화가 max_conc 386을 줄일 수 있는지
- wick 기반 stop 변경이 구조를 크게 바꾸는지
