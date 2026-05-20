# LONG MAX v12 변경 기록

## 갱신 이유

LM26_S1280_RR5050_B0360_H17_CD32가 CD 603.3485179858741을 기록했고, 단독 리테스트를 통과했다. long_max식 summary에서도 VALID로 확인되어 long_max 기준선으로 승격한다.

## 기준선 구조

entry_source: child::orig_V09_extreme_vol18::tp03

source 파라미터:
entry_source_atr_stop 1.10
entry_source_rr_target 3.80
tp03_min_target_pct 0.30

final 파라미터:
atr_stop 1.28
rr_target 5.05
body_atr_min 0.36
max_hold_bars 17
cooldown_bars 32

## 리테스트 결과

검증 폴더: local_results/long_main/LONG_MAIN_LM26_TOP_CD32_RETEST_20260520_140001

후보명: LM26R_001_RETEST_S128_RR505_B360_H17_CD32

판정: VALID, pass_frozen_reproduction_gate true

## 주의

max_conc는 하드 게이트가 아니다. 다음 long_max 개선에서도 max_conc 차이만으로 후보 전체를 무효 처리하지 않는다.
