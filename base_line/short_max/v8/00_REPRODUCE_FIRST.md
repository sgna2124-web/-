# short_max v8 재현 우선 문서

이 기준선을 재현할 때는 `strategy_code.py`만 복사하면 안 된다. `actual bar engine`의 시간 처리와 포트폴리오 정산까지 동일해야 한다.

## 실행

```bash
python base_line/short_max/v8/frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time"
```

## 데이터 범위

- 사용 데이터: 2025-12-31 23:59:59까지
- holdout: 2026-01-01 00:00:00 이후
- 2026 데이터는 지표 계산 전부터 제외한다.

## 공식 기준값

- strategy: short_max_v7_devw120_actual_bar_engine
- trades: 45500
- final_return_pct: 1422.7683542126408
- max_return_pct: 1424.4317435070927
- max_drawdown_pct: 6.104584306764704
- official_cd_value: 1431.3715225256192
- win_rate_pct: 13.738461538461538
- profit_factor: 1.4976180824186338
- max_conc: 299
- same_bar_trades: 3786
- active_leftover: 0
- pending_leftover: 0
- load_errors: 0

## 필수 재현 요소

- 597개 CSV 로딩
- 2026 데이터 지표 계산 전 제외
- EMA20, RSI14, ATR14 계산
- next-bar open 진입
- same timestamp exit 후 same timestamp 신규 진입 금지
- same-bar TP/SL 유지
- 현재 equity 기준 1% 진입
- fee_per_side 0.0004 반영
- RSI 직접 gate 비활성화
- score_min_short 2.35를 entry mask 내부 적용
- expected_tp >= 0.003 검증
- dd_brake edge_current 적용
- 종료 시 forced_end close 정산

## actual bar engine 핵심

5분봉 `12:00` 캔들은 `12:00:00 ~ 12:04:59` 구간이다. `12:00` 캔들 안에서 발생한 청산 결과는 `12:00 open` 진입 판단에 사용할 수 없다.

- `12:00 open` 진입은 `11:55 close`에서 확정된 신호만 가능하다.
- `12:00` 캔들 내부 청산 결과는 `12:05 open`부터 반영한다.
- `12:00 close`에서 생긴 새 신호는 `12:05 open` 진입 후보가 된다.

## 재현 실패 시

기준값과 다르면 후보 개발을 중단한다. 먼저 engine ordering, 데이터 범위, forced_end 정산, 수수료, position_fraction을 확인한다.
