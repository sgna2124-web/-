# LONG_MAX2 V1 REPRODUCTION CHECKLIST

절대 원칙:
- 기준선 재현 부분은 해석/추측/최적화 금지.
- baseline gate 절대 수정 금지.
- entry 조건 변경 금지.

재현 파일:
- local_results/long_max/LONG_MAX_V30_2025_V29_TOP1_RETEST_STANDALONE

재현 순서:
1. LONG_MAX_V30_2025_V29_TOP1_RETEST_STANDALONE 실행
2. baseline_reproduction_ok == True 확인
3. baseline_cd_actual == 618.2592886468248 확인
4. baseline_trades == 55597 확인
5. errors == 0 확인
6. top strategy == V30_RETEST_V29_TOP1_B2_FR015 확인
7. official_cd_value == 1120.9401886015664 확인
8. final_return_pct == 1027.8680633622162 확인

실패 판정:
- baseline_reproduction_ok false
- errors > 0
- baseline trades mismatch
- baseline CD mismatch
- top CD mismatch

핵심 철학:
- reversal entry 유지
- 생존 판정은 빠르게
- 2 bars 이후 +0.15R 보호
- 초반 강한 반등을 공격적으로 보호
- 살아남는 놈은 강하게 유지
