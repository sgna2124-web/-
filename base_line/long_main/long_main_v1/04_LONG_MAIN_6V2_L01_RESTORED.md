# LONG MAIN 기준선 복원 완료: 6V2_L01_doubleflush_core

## 1. 복원 판정

- 상태: 복원 성공
- 축: long_main
- 전략명: `6V2_L01_doubleflush_core`
- 원본 배치: `6V2_LONG10_REVIEWED`
- 복원 실행 배치: `RESTORE_EXACT_6V2_L01_FEE008_V4`
- 기준 역할: 공식 롱 메인 기준선

## 2. 복원 결과

fee_004 기준, 즉 편도 수수료 0.04%, 왕복 수수료 0.08% 환경에서 재실행한 결과다.

| 항목 | 복원 결과 |
|---|---:|
| trades | 592 |
| wins | 346 |
| losses | 246 |
| win_rate_pct | 58.4459 |
| final_return_pct | 23.8426 |
| max_return_pct | 24.0623 |
| max_drawdown_pct | 1.7280 |
| official_cd_value | 121.7026 |
| verdict | baseline_win |

기존 기록의 핵심값은 trades 592, win_rate 약 58.1081%, max_return 약 23.9191%, MDD 약 1.7512%였다. 복원본은 거래 수가 정확히 일치했고, fee_004 적용 상태에서 수익률과 MDD가 기존 기록과 매우 근접하게 재현되었다. 따라서 long_main 기준선은 복원 완료로 확정한다.

## 3. 실행 환경

| 항목 | 값 |
|---|---|
| side | long |
| position_fraction | 0.01 |
| fee_per_side | 0.0004 |
| round_trip_fee | 0.0008 |
| ROUND_TRIP_COST_BPS | 8.0 |
| 데이터 경로 | `코인/Data/time` |
| 실행 방식 | 원본 `6V2_long10_reviewed.py` 사용, STRATEGIES를 target 1개로 필터링 |
| 병렬 처리 | Windows 안정성을 위해 sequential 실행 가능 |

## 4. 전략 파라미터

원본 전략 정의 기준:

| 항목 | 값 |
|---|---:|
| strategy | 6V2_L01_doubleflush_core |
| description | cap reclaim + double flush core |
| atr_stop | 1.05 |
| rr_target | 2.50 |
| max_hold_bars | 18 |
| cooldown_bars | 18 |

## 5. 진입 조건 요약

이 전략은 단순 과매도 진입이 아니라 `double flush` 이후 `cap reclaim`이 확인되는 롱 반전 구조다.

핵심 구조:

1. 하락/저점 압박 구간에서 flush 이벤트가 발생한다.
2. 단일 저점 터치가 아니라, 이전 flush 흔적까지 포함한 double flush 성격을 가진다.
3. 이후 가격이 단순 반등하는 것이 아니라 cap reclaim 조건을 만족해야 한다.
4. 변동성, 거래량, 캔들 구조, 추격 매수 방지 조건을 함께 통과해야 한다.
5. 진입 후 ATR 기반 stop, RR 기반 target, 최대 보유 봉수, cooldown을 적용한다.

정확한 진입 Boolean은 원본 `base_line/6V2_long10_reviewed.py`의 로직을 기준으로 한다. 이 문서의 요약은 전략의 의미를 설명하기 위한 것이며, 실제 백테스트 기준은 원본 코드 실행 결과를 우선한다.

## 6. 청산 조건 요약

- ATR 기반 손절: `entry - atr_stop * ATR`
- RR 기반 익절: `entry + rr_target * ATR risk`
- 최대 보유 봉수: 18 bars
- 거래 후 cooldown: 18 bars
- 수수료: 왕복 8bps 차감
- 포지션 크기: 현재 equity의 1%

## 7. 장점

1. 거래 수가 과도하지 않다.
   - 전체 597개 심볼 기준 592건으로, 무분별한 진입이 아니라 선별된 반전 구간만 잡는다.

2. MDD가 낮다.
   - 복원 결과 MDD 약 1.728%로, 롱 기준선 중 안정성이 매우 좋다.

3. 승률이 높다.
   - 복원 결과 승률 약 58.45%로, 롱 전략치고 손익비와 승률의 균형이 좋다.

4. 기준선으로 사용하기 적합하다.
   - 거래 수, 수익률, MDD가 기존 기록과 거의 일치하므로 향후 개선안의 검증 기준으로 사용할 수 있다.

## 8. 단점

1. 진입 빈도가 낮다.
   - 희소 전략이므로 단독 실전 운용 시 기회가 적을 수 있다.

2. 강한 상승 추세 추종형 전략은 아니다.
   - 핵심은 하락 후 flush/reclaim 반전 구조이므로, 지속 상승장에서 모든 기회를 잡는 구조가 아니다.

3. 원본 Boolean 조건 의존도가 높다.
   - `doubleflush_core`, `cap reclaim`의 세부 조건을 임의로 추정하면 성과가 크게 달라진다. 반드시 원본 코드 기준으로 유지해야 한다.

4. 개선 시 과최적화 위험이 있다.
   - 이미 MDD가 낮고 거래 수가 희소하기 때문에, 작은 조건 추가만으로도 거래 수가 급감하거나 기준선과 비교 불가능해질 수 있다.

## 9. 향후 개선 기준

long_main을 개선할 때는 다음 기준을 반드시 지킨다.

1. 기준선 592 trades, max_return 약 24%, MDD 약 1.7%를 항상 비교 기준으로 삼는다.
2. 거래 수만 늘리는 개선은 실패로 본다.
3. MDD가 급증하면 수익률이 좋아도 기준선 대체 후보로 보지 않는다.
4. TP 기대값 0.3% 이상 필터를 적용하는 후속 개선안에서는 기준선 원본과 개선안을 분리하여 평가한다.
5. 원본 기준선은 건드리지 않는다. 개선안은 별도 파일/별도 배치로 만든다.

## 10. 현재 다음 과제

long_main은 복원 완료로 잠정 확정한다.

다음 집중 대상은 long_max 복원이다.

- 대상 전략: `8V4_V51_V002_core_rare22_c1`
- 기존 기준: trades 2276, win_rate 약 45.2548%, max_return 약 44.2664%, MDD 약 6.7587%
- v4 실패 원인: 8V4는 전략명이 소스에 리터럴로 존재하지 않고 400개 조합에서 런타임 생성된다. 또한 1개 전략만 먼저 필터링하면 내부 생성/평가 흐름이 깨져 trades 0이 발생했다.
- 다음 복원 방식: 8V4 원본 400개 전체를 그대로 실행한 뒤 결과에서 `8V4_V51_V002_core_rare22_c1`만 추출한다.
