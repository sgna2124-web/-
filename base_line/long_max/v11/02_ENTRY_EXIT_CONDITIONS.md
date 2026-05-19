# long_max v11 진입/청산 조건

long_max v11은 long_main v16과 동일한 전략을 long_max 축 기준선으로 승격한 것이다.

## 진입 조건

```text
entry_source = child::orig_V09_extreme_vol18::tp03
final_entry = entry_source AND body_atr >= 0.22
```

## TP03 source 기준

| parameter | value |
|---|---:|
| entry_source_atr_stop | 1.10 |
| entry_source_rr_target | 3.80 |
| tp03_min_target_pct | 0.30 |

```python
target_pct = (1.10 * atr14 * 3.80 / close) * 100
entry_source = parent_entry & (target_pct >= 0.30)
```

최종 청산 파라미터 1.21/5.05로 TP03 source를 다시 계산하지 않는다.

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
| round_trip_cost_bps | 8.0 |
| position_fraction | 0.01 |

```python
entry_i = signal_i + 1
entry_price = open[entry_i]
risk = 1.21 * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * 5.05
last_i = min(n - 1, entry_i + 17)
```

청산 우선순위:

1. 같은 캔들 stop/target 동시 히트 시 stop-first
2. stop만 히트하면 stop
3. target만 히트하면 target
4. max_hold까지 없으면 close[last_i] time exit

## 수수료와 복리

```python
gross_pct = (exit_price / entry_price - 1) * 100
pnl_pct = gross_pct - 0.08
equity *= 1 + 0.01 * pnl_pct / 100
```

## long_max 평가식

```python
official_cd_value = 100 * (1 - max_drawdown_pct / 100) * (1 + max_return_pct / 100)
```
