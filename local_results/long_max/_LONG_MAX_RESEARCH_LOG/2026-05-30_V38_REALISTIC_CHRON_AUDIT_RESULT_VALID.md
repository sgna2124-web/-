# V38 REALISTIC CHRON AUDIT RESULT VALID

실험 배치:
- LONG_MAX2_V38_2025_REALISTIC_CHRON_AUDIT_MEMSAFE_DEV_STANDALONE

목적:
- V37의 run_meta-only 문제를 해결.
- 전략별 chronological portfolio audit을 실제 공식 판정 기준으로 저장.
- trade-list 기준이 아니라 실제 시간순 realized equity 기준으로 후보를 선택.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248

공식 판정 기준:
- chronological_portfolio_audit

V2 reference audited baseline:
- strategy: V38_REF_LONG_MAX2_V2_AUDITED_WEAK_E1_BE_NEXT
- chron_final_return_pct: 902.1352059886217
- chron_max_drawdown_pct: 16.983488215379623
- chron_cd_value: 832.1846538467717
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0

V38 chronological top:
- strategy: V38_H14_C40_TR2_FR020
- condition: hold 14, cooldown 40, time_reduce 2 -> +0.20R, weak 1 close<0 then tighten BE next bar
- trades: 54770
- trade_list_return_pct: 980.0824411021135
- trade_list_mdd_pct: 0.6742097374279221
- trade_list_cd_value: 1073.3179529915608
- chron_final_return_pct: 893.0034173779171
- chron_max_drawdown_pct: 12.386873220754179
- chron_cd_value: 870.1601924680137
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0

비교:
- delta_chron_cd_vs_ref: +37.975538621242094
- delta_chron_mdd_vs_ref: -4.596614994625444
- delta_chron_exposure_vs_ref: 0.0

판정:
- V38_H14_C40_TR2_FR020은 실전 chronological audit 기준 개선 후보.
- 기준선 갱신은 아직 단독 리테스트 전까지 보류.
- MDD 절감 성공.
- chron CD 개선 성공.
- 노출 감소 실패: max exposure 738% 유지.

핵심 해석:
- hold 14 + cooldown 40 + time_reduce +0.20R는 v2보다 수익은 소폭 낮지만 실제 포트폴리오 MDD를 크게 줄임.
- 노출은 여전히 진입 군집 자체가 많아서 hold/cooldown 조정만으로는 해결되지 않음.
- 다음 개선은 포지션 수 제한, symbol clustering 제한, timestamp 진입 컷오프 같은 포트폴리오 레벨 제어가 필요.

다음 단계:
1. V38_H14_C40_TR2_FR020 단독 리테스트.
2. 동시에 포트폴리오 레벨 최대 동시 포지션 제한 실험 준비.
3. 단독 리테스트 성공 시 long_max2 v3 후보 가능.

주의:
- 앞으로 공식 판정은 반드시 v38_chronological_portfolio_audit.csv 기준.
- trade-list top이 reference여도 chronological top은 다를 수 있음.
