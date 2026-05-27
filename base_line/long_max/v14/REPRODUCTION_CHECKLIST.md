# LONG_MAX V14 REPRODUCTION CHECKLIST

절대 원칙:
- 기준선 재현 부분은 해석/추측/변형 금지.
- entry 조건 변경 금지.
- baseline gate 수정 금지.

재현 순서:
1. LONG_MAX_V27_2025_V45B_TOP1_RETEST_STANDALONE 실행
2. baseline_reproduction_ok == True 확인
3. baseline_cd_actual == 618.2592886468248 확인
4. baseline_trades == 55597 확인
5. errors == 0 확인
6. top strategy == V27_RETEST_V45B_TOP1_TR_B3_FR010 확인
7. official_cd_value == 890.9656224153265 확인

실패 판정:
- baseline_reproduction_ok false
- errors > 0
- baseline trades mismatch
- baseline CD mismatch

핵심 철학:
- reversal entry 유지
- time_reduce exit 적용
- 3 bars 이후 +0.10R stop 보호
- dead trade 보호 + 살아남는 반등 유지
