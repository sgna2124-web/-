# long_main v16 진입/청산 조건

## 전략 식별

- source candidate: `LM23R_001_RETEST_S121_RR505_B022_H17`
- v23 winning candidate: `LM23_S121_RR505_B022_H17`
- side: long

## 최종 전략명

```text
8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18__LM21_stop115_rr480_body020_hold17__LM22_stop120_rr500_body020_hold17__LM23_stop121_rr505_body022_hold17
```

## 진입 구조

```text
entry_source = child::orig_V09_extreme_vol18::tp03
final_entry = entry_source AND body_atr >= 0.22
```

entry source는 기존 TP03 진입 마스크다. 기준선 개선 과정에서 entry source 자체를 새로 만든 것이 아니다.

## TP03 gate 기준

TP03 entry source 계산 기준:

| parameter | value |
|---|---:|
| entry_source_atr_stop | 1.10 |
| entry_source_rr_target | 3.80 |
| tp03_min_target_pct | 0.30 |

```python
target_pct = (1.10 * atr14 * 3.80 / close) * 100
entry_source = parent_entry & (target_pct >= 0.30)
```

주의:

- 최종 청산 RR 5.05로 TP03 gate를 다시 계산하지 않는다.
- 최종 stop 1.21로 TP03 gate를 다시 계산하지 않는다.
- TP03 source는 반드시 1.10/3.80 기준이다.

## 추가 필터

```python
body_atr = abs(close - open) / atr14
final_entry = entry_source & (body_atr >= 0.22)
```

## 청산 조건

| parameter | value |
|---|---:|
| atr_stop | 1.21 |
| rr_target | 5.05 |
| max_hold_bars | 17 |
| cooldown_bars | 31 |

롱 포지션 청산 가격:

```python
entry_i = signal_i + 1
entry_price = open[entry_i]
risk = 1.21 * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * 5.05
last_i = min(n - 1, entry_i + 17)
```

청산 우선순위:

1. 같은 캔들에서 stop과 target이 모두 닿으면 stop-first 처리한다.
2. stop만 닿으면 stop 청산한다.
3. target만 닿으면 target 청산한다.
4. `max_hold_bars=17`까지 stop/target이 없으면 `close[last_i]`로 time exit 처리한다.

## 진입 타이밍

- signal_i 캔들에서 entry 조건을 계산한다.
- 실제 진입은 `signal_i + 1` 캔들의 open 가격이다.
- 5분봉에서 12:00 캔들 조건은 12:00~12:04:59 완성 후 확정되므로 실제 진입은 12:05 open이다.

## 수수료와 자산분할

| parameter | value |
|---|---:|
| round_trip_cost_bps | 8.0 |
| cost_pct | 0.08 |
| position_fraction | 0.01 |

```python
gross_pct = (exit_price / entry_price - 1.0) * 100.0
pnl_pct = gross_pct - 0.08
equity *= 1.0 + 0.01 * pnl_pct / 100.0
```

## 공식 cd 계산식

```python
official_cd_value = 100 * (1 - max_drawdown_pct / 100) * (1 + max_return_pct / 100)
```

final_return_pct가 아니라 max_return_pct 기준이다.
