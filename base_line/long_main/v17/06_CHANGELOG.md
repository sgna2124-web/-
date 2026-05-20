# LONG MAIN v17 변경 기록

## v16에서 v17로 갱신한 이유

LM24 current-calc 계열을 기준으로 개선을 진행한 뒤, v25와 v26에서 성과가 상승했다. 그중 LM26_S1280_RR5050_B0360_H17_CD32가 단독 리테스트를 통과했다.

## 핵심 변경

직전 강한 후보 구조:
- atr_stop 1.28
- rr_target 5.05
- body_atr_min 0.32
- max_hold_bars 17
- cooldown_bars 31

v17 기준선 구조:
- atr_stop 1.28
- rr_target 5.05
- body_atr_min 0.36
- max_hold_bars 17
- cooldown_bars 32

즉 stop, rr, hold는 유지하고 body_atr과 cooldown을 강화했다.

## 리테스트 결과

검증 폴더:
local_results/long_main/LONG_MAIN_LM26_TOP_CD32_RETEST_20260520_140001

후보명:
LM26R_001_RETEST_S128_RR505_B360_H17_CD32

판정:
VALID
pass_frozen_reproduction_gate true

official_cd_value:
603.3485179858741

## 다음 작업 시 주의

다음 개발 파일에서는 반드시 이 v17 조건을 0번 exact 후보로 넣고 재현 게이트를 먼저 통과시킨다.

max_conc는 공식 하드 게이트가 아니다. max_conc 차이만으로 개선 후보 전체를 무효 처리하지 않는다.
