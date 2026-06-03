# LONG_MAIN_RESEARCH_LOG_2026_05_26_RANGE_BODY_COMPRESSION_V22

## 목적
롱 메인 신규 탐색 v22 결과를 기록한다.
v21에서 유일하게 살아남은 range_body_compression 계열을 확장했으나, 유효 후보가 전부 사라졌음을 남긴다.

## 실험명
LONG_RANGE_BODY_COMPRESSION_V22_1H

파일:
run_long_range_body_compression_v22_1h.py

결과 폴더:
local_results/long_main/LONG_RANGE_BODY_COMPRESSION_V22_1H

## 배경
v21 LONG_COMPRESSION_RELEASE_V21_1H에서 살아남은 후보는 모두 range_body_compression 계열이었다.

v21 상위:
- CR21_C_022: cd 98.569079, max_return_pct 0.686717, MDD 2.103195, trades 538
- CR21_C_023: cd 98.166303, max_return_pct 0.555938, MDD 2.376423, trades 610
- CR21_C_024: cd 98.151534, max_return_pct 0.549569, MDD 2.384928, trades 614

따라서 v22는 CR21_C_022~024 주변을 넓혀 실행 시간이 너무 짧지 않도록 더 넓은 local grid로 탐색했다.

## v22 탐색 방향
- Range/Body 압축 조건 주변 local search
- release range/body 조건 확장
- close position / upper wick 품질 조건 확장
- stop / RR / hold / cooldown 출구 구조 확장
- 상태 구간 및 risk cap 일부 확장

금지 유지:
- A016 계열 반복 아님
- ATR compression 단독 반복 아님
- Volume compression 단독 반복 아님
- trailing stop 없음
- break-even 없음
- dynamic TP 없음
- 진입 후 SL/TP 수정 없음

## 결과
master_summary 기준:
- specs: 148
- rows: 148
- errors: 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

즉 유효 후보가 전혀 없었다.

## 판정
v22는 실패다.

v21에서 살아남은 range_body_compression 계열을 넓게 확장했지만, 유효 후보가 전부 사라졌다.
이는 CR21_C_022~024가 넓은 조건 주변에서 안정적으로 확장되는 구조가 아니라, 매우 좁은 조건에서만 잠깐 살아난 형태에 가깝다는 뜻이다.

## 결론
range_body_compression 축은 우선순위를 하향한다.

보관할 점:
- v21 CR21_C_022~024는 참고 단서로 남긴다.
- Range/Body 압축이라는 아이디어가 완전히 무효라고 단정하지는 않는다.

하지만 현재 방식으로는:
- 기준선 대체 후보 아님
- local expansion 실패
- 단순 조건 확장 반복 금지

## 반복 금지
다음은 반복하지 않는다.

1. v22 전체 grid 반복
2. CR21_C_022~024 주변 단순 local grid 재반복
3. range/body compression 조건만 넓히는 방식
4. release range/body 단독 확장
5. stop/RR/hold/cooldown 단순 출구 확장

## 다음 방향
다음 개선은 range_body_compression을 계속 붙잡기보다 다른 축으로 이동한다.

새 방향 조건:
- 기준선과 비교 가능한 성장성 필요
- 단순 저MDD 후보가 아니라 max_return이 충분히 커야 함
- trades도 기준선 철학에 맞게 너무 적지 않아야 함
- 좁은 조건 하나에만 의존하는 구조는 피한다.

## 결과 확인 절차 메모
이번부터 결과 확인은 반드시 다음 순서를 따른다.
1. 배치명으로 search
2. master_summary.txt 경로 확인
3. fetch_file로 master_summary.txt 직접 열기
4. 수치 판정

검색 결과만 보고 내부 수치를 확인하지 않은 상태에서 판정하지 않는다.
