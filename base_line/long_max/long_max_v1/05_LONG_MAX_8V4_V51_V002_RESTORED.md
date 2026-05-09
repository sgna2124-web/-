# LONG MAX 기준선 복원 완료: 8V4_V51_V002_core_rare22_c1

## 1. 복원 판정

- 상태: 복원 성공
- 축: long_max
- 전략명: `8V4_V51_V002_core_rare22_c1`
- 원본 배치: `8V4_LONG400_REVIEWED`
- 복원 실행 배치: `RESTORE_EXACT_8V4_LONG400_FULL_FEE008_V1`
- 기준 역할: 롱 raw 개선 후보 기준선 / long_max 기준선

## 2. 복원 방식

8V4 계열은 400개 전략 조합을 전제로 생성·평가되는 구조다. 따라서 `8V4_V51_V002_core_rare22_c1`만 먼저 필터링하면 내부 평가 흐름이 깨져 trades 0이 발생한다.

복원 성공 방식은 다음과 같다.

1. `base_line/8V4_long400_reviewed.py` 원본을 사용한다.
2. 8V4 400개 전략 전체를 그대로 실행한다.
3. 수수료와 진입 비중만 기준 환경으로 고정한다.
4. 실행 완료 후 결과 폴더에서 `8V4_V51_V002_core_rare22_c1`만 추출한다.
5. 기존 기준값과 비교한다.

## 3. 복원 결과

fee_004 기준, 즉 편도 수수료 0.04%, 왕복 수수료 0.08% 환경에서 재실행한 결과다.

| 항목 | 복원 결과 |
|---|---:|
| trades | 2276 |
| wins | 1032 |
| losses | 1244 |
| win_rate_pct | 45.3427 |
| final_return_pct | 44.3226 |
| max_return_pct | 44.9123 |
| max_drawdown_pct | 6.8270 |
| official_cd_value | 134.4697 |
| verdict | restore_success |

기존 기준값과의 차이:

| 항목 | 차이 |
|---|---:|
| trades | 0 |
| win_rate_pct | +0.0879%p |
| final_return_pct | +0.6553%p |
| max_return_pct | +0.6459%p |
| max_drawdown_pct | +0.0683%p |
| official_cd_value | +0.5125 |

거래 수가 정확히 2276개로 일치했고, 수익률·MDD·CD가 기존 기준값과 매우 근접하게 재현되었다. 따라서 long_max 기준선은 복원 성공으로 확정한다.

## 4. 실행 환경

| 항목 | 값 |
|---|---|
| side | long |
| position_fraction | 0.01 |
| fee_per_side | 0.0004 |
| round_trip_fee | 0.0008 |
| ROUND_TRIP_COST_BPS | 8.0 |
| 데이터 경로 | `코인/Data/time` |
| 실행 방식 | 8V4 400개 전체 실행 후 target 전략 추출 |
| 복원 코드 | `base_line/restore_long_max_8V4_fullrun_extract_v1.py` |
| 결과 폴더 | `local_results/RESTORE_EXACT_8V4_LONG400_FULL_FEE008_V1` |
| 추출 폴더 | `local_results/RESTORE_LONG_MAX_8V4_FULLRUN_EXTRACT_V1/extracted_target` |

## 5. 전략 생성 구조

8V4 원본은 전략명이 소스에 완성 문자열로 직접 박혀 있는 방식이 아니다. 다음 조합으로 런타임 생성된다.

- family seed: `V51`
- V51 설명: `l09 v51 microbase pop`
- variant number: `V002`
- anchor tag: `core`
- guard tag: `rare22_c1`
- 최종 전략명: `8V4_V51_V002_core_rare22_c1`

전략명 생성 규칙은 다음 형태다.

`8V4_{seed}_V{variant_no:03d}_{anchor}_{guard}`

따라서 long_max는 `V51 + V002 + core + rare22_c1` 조합으로 생성되는 전략이다.

## 6. 진입 조건 요약

이 전략은 단순 눌림목 매수나 단순 과매도 반등이 아니라, V51 microbase pop 계열에 core anchor와 rare22_c1 guard가 결합된 롱 구조다.

핵심 구조:

1. V51 계열의 microbase pop 후보를 찾는다.
2. microbase는 짧은 압축·베이스 형성 이후 상단 돌파 성격을 가진다.
3. `core` anchor는 기본 품질 조건을 담당한다.
4. `rare22_c1` guard는 22봉 계열 희소 조건과 c1 confirmation 성격을 결합한 방어 필터로 해석한다.
5. 신호 발생 후 ATR 기반 stop, RR 기반 target, 최대 보유 봉수, cooldown을 적용한다.

정확한 Boolean 조건은 `base_line/8V4_long400_reviewed.py` 원본 코드가 기준이다. 이 문서는 전략 의미와 복원 기준을 설명하기 위한 기록이며, 실제 백테스트 기준은 원본 코드 실행 결과를 우선한다.

## 7. 청산 조건 요약

복원 로그 기준 핵심 파라미터:

| 항목 | 값 |
|---|---:|
| atr_stop | 0.92 |
| rr_target | 2.55 |
| max_hold_bars | 18 |
| cooldown_bars | 25 |

청산 구조:

- ATR 기반 손절
- RR 기반 익절
- 최대 보유 봉수 18 bars
- 거래 후 cooldown 25 bars
- 수수료 왕복 8bps 차감
- 포지션 크기 현재 equity의 1%

## 8. 장점

1. 수익 포텐셜이 long_main보다 크다.
   - 복원 결과 max_return 약 44.91%로, long_main의 약 24%보다 높다.

2. 거래 수가 충분하다.
   - 2276 trades로 long_main 592 trades보다 기회가 많다.

3. microbase pop 계열이라 추세 초입/압축 해소 구간을 포착할 가능성이 있다.
   - 단순 저점 반전형보다 상승 확장 구간을 더 많이 잡을 수 있다.

4. raw 개선 후보 기준선으로 가치가 높다.
   - MDD가 공식 기준선 한도보다 높더라도, 수익 창출 구조가 뚜렷해 개선 재료로 적합하다.

## 9. 단점

1. MDD가 높다.
   - 복원 결과 MDD 약 6.827%로 long_main보다 훨씬 크다.

2. 승률이 낮다.
   - 승률 약 45.34%로, 손익비 구조에 의존한다.

3. 공식 안정 기준선으로는 부담이 있다.
   - MDD 5% 기준을 넘기므로 공식 long_main 대체 기준선이 아니라 long_max/raw 개선 후보 기준선으로 다룬다.

4. 복원 방식이 특수하다.
   - 8V4 전체 400개 전략을 먼저 실행해야 정상 재현된다. target 1개만 먼저 필터링하면 trades 0이 발생할 수 있다.

5. 개선 시 리스크 제어가 핵심이다.
   - 수익률을 더 키우기보다 MDD와 연속 손실을 줄이는 방향이 우선이다.

## 10. 향후 개선 기준

long_max를 개선할 때는 다음 기준을 사용한다.

1. target 기준값은 trades 2276, max_return 약 44.9%, MDD 약 6.8%다.
2. 수익률 상승만으로 성공 판정하지 않는다.
3. MDD를 5% 이하로 줄이는 개선은 우선순위가 높다.
4. 거래 수가 급감하면 long_max의 장점이 사라지므로 주의한다.
5. `rare22_c1`, `microbase_pop`, `core` 조건을 임의 추정해서 별도 구현하지 않는다. 원본 8V4 생성 구조를 기준으로 개선한다.
6. TP 기대값 0.3% 이상 필터를 적용하는 후속 개선안은 원본 기준선과 분리해 평가한다.

## 11. 현재 기준선 복원 상태

- long_main: `6V2_L01_doubleflush_core` 복원 성공
- long_max: `8V4_V51_V002_core_rare22_c1` 복원 성공
- short_main: 기존 복원 성공 기준선 유지
- short_max: 기존 복원 성공 기준선 유지

이제 4축 기준선 복원 체계는 실험 기준으로 사용할 수 있다.
