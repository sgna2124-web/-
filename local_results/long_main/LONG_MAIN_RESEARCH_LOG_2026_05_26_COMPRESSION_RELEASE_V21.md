# LONG_MAIN_RESEARCH_LOG_2026_05_26_COMPRESSION_RELEASE_V21

## 목적
롱 메인 신규 탐색 v21 결과를 기록한다.
A016 계열 종료 후 기준선 철학에 더 가까운 반복성 중심 축으로 전환한 첫 실험이다.

## 실험명
LONG_COMPRESSION_RELEASE_V21_1H

파일:
run_long_compression_release_v21_1h.py

결과 폴더:
local_results/long_main/LONG_COMPRESSION_RELEASE_V21_1H

## 핵심 가설
A016처럼 희귀한 정밀 진입이 아니라, 시장 전체에서 반복될 수 있는 압축 -> 확장 구조를 찾는다.

조건 개요:
- 최근 ATR / Range / Body / Volume 압축
- 현재 봉에서 Range / Body / Volume 확장
- 종가가 봉 상단부에 위치
- 고정 SL/TP
- trailing stop 없음
- break-even 없음
- dynamic TP 없음
- 진입 후 TP/SL 수정 없음

## 결과
master_summary 기준:
- specs: 65
- rows: 65
- errors: 0
- MDD 5% 미만 후보: 3개

TOP_MDD_LT5:
1. CR21_C_022
   - family: range_body_compression
   - cd: 98.569079
   - max_return_pct: 0.686717
   - MDD: 2.103195
   - trades: 538
   - win_rate_pct: 39.219

2. CR21_C_023
   - family: range_body_compression
   - cd: 98.166303
   - max_return_pct: 0.555938
   - MDD: 2.376423
   - trades: 610
   - win_rate_pct: 38.033

3. CR21_C_024
   - family: range_body_compression
   - cd: 98.151534
   - max_return_pct: 0.549569
   - MDD: 2.384928
   - trades: 614
   - win_rate_pct: 37.948

BEST_BY_FAMILY:
- range_body_compression: CR21_C_022

## 판정
v21은 기준선 대체 후보로는 아직 부족하다.

장점:
- A016보다 거래수 증가
- MDD는 A016보다 더 낮은 후보가 나옴
- cd는 98 이상으로 준수
- 살아남은 family가 명확함

한계:
- max_return이 0.55~0.69% 수준으로 매우 약함
- 기준선 대비 성장성이 부족함
- 살아남은 후보가 3개뿐이며 모두 range_body_compression 계열

## 중요한 단서
살아남은 축:
- range_body_compression

탈락 또는 우선순위 하향:
- ATR compression 단독
- volume contraction/release 단독
- payoff expand 단독
- frequency expand 단독
- balanced compression release 단독

즉 압축 -> 확장 아이디어 전체가 무효는 아니지만, 현재 형태에서는 Range/Body 압축 계열만 의미 있는 반응을 보였다.

## 다음 방향
v22를 진행한다면 CR21_C_022~024만 중심으로 세분화한다.

다음 실험 방향:
1. Range/Body 압축 조건 주변 local search
2. max_return 증대를 위한 출구 구조 실험
3. trades 500~1000 유지
4. MDD 3% 이하 유지
5. max_return 최소 2~3% 이상으로 개선되는지 확인

단, A016과 동일하게 max_return이 계속 1% 미만이면 기준선 대체 후보가 아니므로 종료한다.

## 반복 금지
다음은 그대로 반복하지 않는다.

- ATR compression 단독 확장
- volume contraction 단독 확장
- frequency loose compression 반복
- payoff expand만 단독 반복
- v21 전체 조건 grid 재반복

## 작업 절차 메모
결과 확인 시 반드시 다음 순서를 지킨다.
1. 배치명으로 search
2. master_summary.txt path 확인
3. fetch_file로 master_summary.txt 직접 열기
4. 수치 판정

경로 검색만 하고 파일 내용을 읽지 않은 상태에서 결과를 판정하지 않는다.
