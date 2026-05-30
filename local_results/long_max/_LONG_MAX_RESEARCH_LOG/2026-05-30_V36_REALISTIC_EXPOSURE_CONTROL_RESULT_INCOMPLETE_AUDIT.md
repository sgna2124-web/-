# V36 REALISTIC EXPOSURE CONTROL RESULT - INCOMPLETE AUDIT

실험 배치:
- LONG_MAX2_V36_2025_REALISTIC_EXPOSURE_CONTROL_DEV_STANDALONE

목적:
- long_max2 v2 audited baseline 기준으로 실제 운용 리스크를 줄이는 개선.
- 목표는 trade-list CD 증가가 아니라 chronological MDD, max open positions, max exposure 감소.

기준선 재현:
- baseline_reproduction_ok: True
- baseline_cd_expected: 618.2592886468248
- baseline_cd_actual: 618.2592886468248
- errors: 0

V36 리포트상 top:
- V36_REF_LONG_MAX2_V2_AUDITED_WEAK_E1_BE_NEXT
- 즉 개선 후보가 아니라 v2 reference가 1위.

reference chronological audit:
- chron_final_return_pct: 902.1352059886217
- chron_max_drawdown_pct: 16.983488215379623
- chron_cd_value: 832.1846538467717
- chron_max_open_positions: 738
- chron_max_gross_exposure_pct: 738.0

문제:
- v36_chronological_portfolio_audit.csv 파일이 비어 있음.
- 따라서 후보별 chronological MDD / max open positions / max exposure 비교가 불가능.
- v36_exposure_control_results.csv에는 trade-list 지표만 있음.
- 공식 판단 기준이 chronological audit이므로 V36 결과로 기준선 갱신 또는 개선 성공 판정 불가.

trade-list 참고:
- reference가 1위.
- 2위 V36_H14_C40_TR2_FR020: trade-list CD 1073.3179529915608
- 3위 V36_H17_C40: trade-list CD 1070.3995205278266
- 후보들이 reference trade-list CD 1092.9450669668074를 넘지 못함.

판정:
- 기준선 갱신 없음.
- 개선 성공 판정 보류/불가.
- V36은 audit 저장 구조가 불완전했으므로 V37에서 후보별 chronological audit을 반드시 생성해야 함.

다음 단계:
1. 후보별 chronological audit summary를 저장하도록 V37 runner 수정.
2. 각 후보별로 chron_return, chron_MDD, chron_CD, max_open_positions, max_gross_exposure를 산출.
3. 정렬 기준은 chron_CD 또는 MDD-adjusted score.
4. trade-list result는 참고만 하고 공식 판정에는 사용하지 않음.

주의:
- 앞으로 노출 제어형 개선은 v36_exposure_control_results.csv만 보고 판단 금지.
- 반드시 후보별 chronological audit summary가 있어야 함.
