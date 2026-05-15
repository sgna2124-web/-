# ACTUAL BAR ENGINE RULES

이 문서는 5분봉 OHLCV 기반 백테스트에서 반드시 지켜야 하는 공식 시간 처리 규칙이다.

## 핵심 전제

5분봉 timestamp가 `12:00`이면 해당 캔들은 `12:00:00 ~ 12:04:59` 구간이다.
따라서 `12:00` 캔들의 high, low, close로 확인되는 청산은 `12:00 open` 시점에 알 수 없다.

실전 봇 관점에서는 보통 다음과 같이 처리한다.

- `12:00:05`에 데이터를 불러오면 `11:55` 캔들이 확정되어 있다.
- `11:55` 캔들의 종가와 지표로 신호를 판단한다.
- 이 신호의 백테스트 진입가는 `12:00 open`으로 근사한다.
- `12:30` 캔들 내부에서 TP/SL이 체결되더라도 그 사실은 `12:35` 데이터 확인 시점부터 신규 진입 판단에 반영한다.
- `12:30` 캔들의 종가 조건으로 생긴 신호는 `12:35 open` 진입 후보가 된다.

## 공식 엔진 순서

각 timestamp `t`에서 다음 순서를 따른다.

1. `t` bar open에서 pending entry를 먼저 처리한다.
   - pending entry는 반드시 `t-1` 캔들 close에서 확정된 신호여야 한다.
   - 이때 position sizing은 `t` 시작 시점 equity 기준이다.
2. `t` 캔들의 high/low/close로 active position의 청산을 평가한다.
   - `t` open에 새로 진입한 포지션도 같은 캔들 안에서 TP/SL에 닿으면 same-bar 청산될 수 있다.
3. `t` 캔들 내부 청산 결과는 equity, DD, slot에 반영하되, 이미 끝난 `t` open 신규 진입에는 절대 사용하지 않는다.
4. `t` 캔들 close 후 flat symbol에 대해 신규 신호를 계산한다.
5. `t` close에서 만들어진 신호는 `t+1` open pending entry로 넘긴다.
6. DD brake는 `t` 캔들 청산 후 drawdown edge가 발생하면 `t+1`부터 신규 진입 차단에 적용한다.
7. 백테스트 종료 시점에 남은 active position은 해당 심볼의 마지막 close로 forced_end 청산한다.

## 금지 사항

- 같은 timestamp에서 기존 포지션을 먼저 청산한 뒤 그 자금이나 slot으로 같은 timestamp 신규 진입을 허용하면 안 된다.
- `12:30` 캔들 내부 청산 결과로 `12:30 open` 진입 가능 여부를 바꾸면 안 된다.
- `12:30` 캔들 close에서 만들어진 신호를 `12:30 open`에 진입시키면 안 된다.
- current candle high/low/close를 보고 current candle open 진입 여부를 바꾸면 안 된다.

## 유지되는 사항

- 신호 확정 후 다음 봉 open 진입은 유지한다.
- same-bar TP/SL 청산은 유지한다.
- 수수료는 편도 `0.0004`, 왕복 `0.0008`이다.
- 진입 금액은 현재 timestamp open 기준 equity의 `0.01`이다.
- 2025 train 결과 산출 시 2026 데이터는 지표 계산 전부터 제외한다.

## 기준선 버전 반영

이 규칙 적용으로 숏 계열 기준선은 다음 버전으로 갱신한다.

- short_main: v6 구엔진 기준선 -> v7 actual bar engine 기준선
- short_max: v7 구엔진 기준선 -> v8 actual bar engine 기준선

구엔진 결과는 참고값으로만 남기고, 이후 개발과 기준선 비교는 actual bar engine 기준을 따른다.
