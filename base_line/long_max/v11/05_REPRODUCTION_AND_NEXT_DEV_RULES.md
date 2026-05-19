# long_max v11 재현 및 다음 개발 규칙

## 다음 개발 첫 후보

다음 long_max 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LMAX##_000_LONG_MAX_V11_EXACT_FROZEN`

이 후보는 `LM23R_001_RETEST_S121_RR505_B022_H17`와 동일해야 한다.

## 공식 기대값

| metric | expected |
|---|---:|
| trades | 56551 |
| wins | 21969 |
| losses | 34582 |
| win_rate_pct | 38.84811939665081 |
| final_return_pct | 454.0898854634718 |
| max_return_pct | 455.0171719748199 |
| max_drawdown_pct | 1.3974597812998368 |
| official_cd_value | 547.2610302171641 |
| max_conc | 445 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 갱신 조건

long_max 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. official_cd_value > 547.2610302171641
5. 단독 리테스트에서 재현 가능
6. 06_FULL_REPRODUCTION_SPEC까지 기록 완료

## 기준선 재현 실패 시

기준선 exact가 실패하면 개선 후보 결과는 전부 무효 처리한다.

체크 순서:

1. 597개 심볼 사용 여부
2. 2026년 데이터 제외 여부
3. TP03 source가 1.10/3.80인지 여부
4. final exit가 1.21/5.05/17/31인지 여부
5. body_atr >= 0.22 추가 위치
6. signal_i + 1 open 진입 여부
7. stop-first 처리 여부
8. 수수료 0.08% 차감 여부
9. position_fraction 0.01 여부
10. cd_value가 max_return_pct 기준인지 여부

## 우선 탐색 방향

- stop: 1.21, 1.22, 1.23
- rr_target: 5.05, 5.10, 5.15
- body_atr: 0.20, 0.22, 0.24, 0.26
- hold: 17 고정 우선
