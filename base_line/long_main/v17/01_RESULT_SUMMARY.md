# LONG MAIN v17 결과 요약

공식 기준선: LONG_MAIN_V17_LM26_S128_RR505_B360_H17_CD32

리테스트 결과 폴더: local_results/long_main/LONG_MAIN_LM26_TOP_CD32_RETEST_20260520_140001

리테스트 후보: LM26R_001_RETEST_S128_RR505_B360_H17_CD32

성과:

| metric | value |
|---|---:|
| trades | 55821 |
| wins | 22425 |
| losses | 33396 |
| win_rate_pct | 40.17305315203956 |
| final_return_pct | 508.8757953955824 |
| max_return_pct | 510.01650319972197 |
| max_drawdown_pct | 1.0930827574126778 |
| official_cd_value | 603.3485179858741 |
| max_conc | 436, diagnostic only |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

직전 long_main 기준선 대비 핵심 변화:

- body_atr_min 0.32에서 0.36으로 강화
- cooldown_bars 31에서 32로 증가
- atr_stop 1.28, rr_target 5.05, max_hold_bars 17 유지
- 수익률과 CD가 크게 개선됨
- MDD는 약간 증가했으나 1.1% 근처로 유지됨

공식 재현 판정:

- pass_frozen_reproduction_gate true
- max_conc는 하드 게이트에서 제외하고 진단값으로만 사용
