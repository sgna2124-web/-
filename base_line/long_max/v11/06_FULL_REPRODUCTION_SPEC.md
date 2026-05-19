# long_max v11 완전 재현 사양

long_max v11은 long_main v16과 동일한 전략이다. 평가 축은 long_max이지만 entry, exit, 수수료, 복리, 데이터 필터는 모두 동일하다.

## 공식 기준선

```python
EXPECTED = {
    "trades": 56551,
    "wins": 21969,
    "losses": 34582,
    "win_rate_pct": 38.84811939665081,
    "final_return_pct": 454.0898854634718,
    "max_return_pct": 455.0171719748199,
    "max_drawdown_pct": 1.3974597812998368,
    "official_cd_value": 547.2610302171641,
    "max_conc": 445,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}
```

## 데이터 필터

2025년까지의 데이터만 사용한다.

```text
train_end_exclusive_utc = 2026-01-01 00:00:00
```

## 지표와 raw signal

지표, raw_l01, raw_shock_down, raw_extreme_reclaim, raw_shock_reversal_balance 계산은 `base_line/long_main/v16/06_FULL_REPRODUCTION_SPEC.md`와 동일하다.

## entry source

```python
ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80
TP03_MIN_TARGET_PCT = 0.30

family_v09 = raw_shock_down | raw_l01 | raw_shock_reversal_balance
anchor_extreme = raw_extreme_reclaim | (rsi14 <= 34.0)
guard_vol18 = vol_ratio >= 1.18
parent = family_v09 & anchor_extreme & guard_vol18

target_pct = (ENTRY_SOURCE_ATR_STOP * atr14 * ENTRY_SOURCE_RR_TARGET / np.maximum(close, 1e-12)) * 100.0
entry_source = parent & (target_pct >= TP03_MIN_TARGET_PCT)
entry_source[:120] = False
entry_source[-1:] = False
```

## 최종 entry

```python
final_entry = entry_source & (body_atr >= 0.22)
final_entry[:120] = False
final_entry[-1:] = False
```

## 최종 청산

```python
ATR_STOP = 1.21
RR_TARGET = 5.05
MAX_HOLD_BARS = 17
COOLDOWN_BARS = 31
ROUND_TRIP_COST_BPS = 8.0
POSITION_FRACTION = 0.01
```

진입:

```python
entry_i = signal_i + 1
entry_price = open[entry_i]
```

청산:

```python
risk = ATR_STOP * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * RR_TARGET
last_i = min(n - 1, entry_i + MAX_HOLD_BARS)
```

같은 캔들에서 stop과 target이 모두 닿으면 stop-first 처리한다.

손익:

```python
gross_pct = (exit_price / entry_price - 1.0) * 100.0
pnl_pct = gross_pct - 0.08
equity *= 1.0 + 0.01 * pnl_pct / 100.0
```

cooldown:

```python
next_allowed_signal_i = exit_i + 31
```

## cd_value

```python
official_cd_value = 100 * (1 - max_drawdown_pct / 100) * (1 + max_return_pct / 100)
```

## 재현 실패 체크

1. 597개 심볼인지 확인한다.
2. 2026년 데이터가 제외됐는지 확인한다.
3. TP03 source가 1.10/3.80 기준인지 확인한다.
4. final exit가 1.21/5.05/17/31인지 확인한다.
5. final_entry가 entry_source AND body_atr >= 0.22인지 확인한다.
6. signal_i + 1 open 진입인지 확인한다.
7. stop-first 처리인지 확인한다.
8. 수수료 0.08% 차감인지 확인한다.
9. position_fraction 0.01인지 확인한다.
10. cd_value가 max_return_pct 기준인지 확인한다.
