# 코드 스캐폴드 및 메트릭 규격

## 최소 코드 구조
1. 데이터 로드
- zip 내부 전체 csv 순회
- open/high/low/close/volume/date 사용

2. 공통 지표
- EMA 20 / 50 / 100
- RSI 14
- ATR 14
- rolling high/low
- rolling volume mean
- std 기반 압축도
- 꼬리/몸통/close position

3. 전략별 신호 블록
- long_sig
- short_sig
- entry / stop / target / hold 설정
- 기대 TP 0.3% 이상 필터

4. 체결/청산 엔진
- 신호 다음 봉 시가 진입
- stop / target / 시간청산
- 수수료 2회 반영

5. 평가 함수
- trades
- final_asset
- final_return
- peak_asset
- peak_growth
- win_rate
- pf
- mdd
- max_conc

## 출력 규격
전략 하나당 아래 딕셔너리 형태를 유지하면 비교가 편함.
{
  "strategy": "name",
  "trades": int,
  "final_asset": float,
  "final_return": float,
  "peak_asset": float,
  "peak_growth": float,
  "win_rate": float,
  "pf": float,
  "mdd": float,
  "max_conc": int
}

## 구현 메모
- 실행 도구 세션이 중간에 리셋될 수 있으므로, 전략 배치 결과는 json 파일로 중간 저장하는 방식이 유리함
- 전략명을 명확히 남기고, 결과 로그를 파일로 남겨서 다음 세션에서 바로 이어받을 수 있게 할 것
