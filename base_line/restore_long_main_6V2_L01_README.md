# restore_long_main_6V2_L01 실행 안내

long_main 기준선 `6V2_L01_doubleflush_core`는 `restore_exact_long_baselines_v4_stable.py` 실행 결과로 복원 성공했다.

## 검증된 실행 명령

```powershell
python .\restore_exact_long_baselines_v4_stable.py --strategy long_main
```

또는 전체 실행:

```powershell
python .\restore_exact_long_baselines_v4_stable.py --strategy all
```

## 검증 결과

- 결과 폴더: `local_results/RESTORE_EXACT_6V2_L01_FEE008_V4`
- 전략명: `6V2_L01_doubleflush_core`
- trades: 592
- win_rate_pct: 58.4459
- final_return_pct: 23.8426
- max_return_pct: 24.0623
- max_drawdown_pct: 1.7280
- official_cd_value: 121.7026

## 기준선 코드 원칙

- 원본 소스: `base_line/6V2_long10_reviewed.py`
- 복원 방식: 원본 코드 사용 + STRATEGIES를 `6V2_L01_doubleflush_core` 1개로 필터링
- fee_004 기준: `ROUND_TRIP_COST_BPS = 8.0`
- 진입 비중: `POSITION_FRACTION = 0.01`

## 주의

이 전략은 복원 성공 기준선이다. 개선 실험에서 원본 조건을 직접 수정하지 않는다. 개선안은 별도 배치/별도 파일로 만든다.
