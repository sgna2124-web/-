# long_main v2 진입 조건

## 1. 전략명

- 공식명: `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`
- 개발 후보명: `LM4_014_ATTACK_BODY_NOT_HUGE`
- 기반 전략: `6V2_L01_doubleflush_core`
- 방향: long

---

## 2. 진입 조건 개요

v2는 v1 기준선의 진입 조건을 먼저 통과해야 한다.

v1 기준선 핵심:

```text
raw_l01_cap_reclaim
AND
double_flush_ok
```

v2 추가 조건:

```text
close_pos >= 0.77
AND
vol_ratio >= 1.45
AND
body_atr <= 1.60
AND
expected_tp >= 0.003
```

최종 구조:

```text
LONG_MAIN_V2_ENTRY =
    raw_l01_cap_reclaim
    AND double_flush_ok
    AND close_pos >= 0.77
    AND vol_ratio >= 1.45
    AND body_atr <= 1.60
    AND expected_tp >= 0.003
```

---

## 3. v1 기준선 진입 조건

### 3.1 raw_l01_cap_reclaim

`raw_l01_cap_reclaim`은 기준선 v1의 핵심 cap reclaim 조건이다.

구조:

```text
atrp >= 0.003
AND atrp <= 0.070
AND range20p <= 0.180
AND vol_ratio >= 1.35
AND body_atr >= 0.34
AND close > open
AND close_pos >= 0.70
AND low <= previous ll20 * 1.003
AND close >= previous ll20
AND ret5 <= 0.025
AND ret10 <= 0.040
AND ret20 <= 0.075
AND ema_guard_soft
```

의미:

- 변동성이 너무 낮은 구간은 제외한다.
- 변동성이 너무 과도한 구간도 제외한다.
- 최근 20봉 range가 너무 넓은 혼란 구간은 제외한다.
- 거래량이 평균보다 강해야 한다.
- 몸통이 ATR 대비 충분히 커야 한다.
- 양봉이어야 한다.
- 종가가 캔들 상단부에 위치해야 한다.
- 이전 20봉 저점 부근을 찌른 뒤 회복해야 한다.
- 이미 너무 많이 오른 추격 구간은 제외한다.
- EMA guard는 hard trend filter가 아니라 soft guard다.

### 3.2 double_flush_ok

`double_flush_ok`는 최근 구간에서 이미 한 번 이상의 shock_down 또는 flush 흔적이 있었는지 확인한다.

핵심 의미:

- 단순 저점 터치 매수가 아니다.
- 먼저 한 번 이상 강한 하방 충격 또는 flush가 있어야 한다.
- 그 이후 현재 봉에서 cap reclaim이 발생해야 한다.
- 즉, 한 번의 저점이 아니라 double flush 맥락을 요구한다.

구조적 의미:

```text
현재 봉 cap reclaim
AND
최근 lookback 내 shock_down 존재
```

v2에서는 double_flush lookback 자체를 바꾸지 않는다. v1 기준선의 double flush 구조를 그대로 유지한다.

---

## 4. v2 추가 조건

### 4.1 close_pos >= 0.77

캔들 내부에서 종가가 어느 위치에 있는지 보는 조건이다.

```text
close_pos = (close - low) / (high - low)
```

v1 기준선은 close_pos >= 0.70 수준의 reclaim 품질을 요구했다. v2는 이를 추가로 강화해 close_pos >= 0.77을 요구한다.

의미:

- 단순히 저점을 찍고 회복한 정도가 아니라, 종가가 캔들 상단부에 더 강하게 붙어야 한다.
- 반전 의지가 약한 봉을 제거한다.
- v3 결과에서 close_pos 0.77 단독 조건이 기준선을 이긴 것으로 확인되었다.

주의:

- close_pos를 0.80 이상으로 강하게 조이면 MDD는 더 줄 수 있지만 수익률 손실이 커질 수 있다.
- 현재 기준선 v2는 공격성과 안정성의 균형을 위해 0.77을 사용한다.

### 4.2 vol_ratio >= 1.45

현재 거래량이 평균 거래량 대비 얼마나 강한지 보는 조건이다.

v1 기준선은 vol_ratio >= 1.35를 요구했다. v2는 추가 품질 조건으로 vol_ratio >= 1.45를 요구한다.

의미:

- reclaim이 거래량을 동반했는지 확인한다.
- 거래량 없는 약한 반등을 제거한다.
- v3에서 close_pos 0.77 + vol_ratio 1.45 조합이 수익률과 MDD를 동시에 개선했다.

주의:

- vol_ratio 1.50 이상은 좋은 거래를 일부 제거하는 경향이 있었다.
- v2에서는 1.45를 사용한다.

### 4.3 body_atr <= 1.60

현재 캔들 몸통이 ATR 대비 너무 과도하게 크지 않은지 보는 조건이다.

v2의 목적은 너무 과도하게 튄 반전봉을 느슨하게 제거하는 것이다.

의미:

- 지나치게 큰 장대양봉 종가 추격을 줄인다.
- 과열된 반전봉 일부를 제거해 MDD를 낮춘다.
- v4에서 body_atr <= 1.60이 v3 attack anchor보다 cd_value를 개선했다.

주의:

- body_atr <= 1.35는 너무 강했다.
- 강한 body upper guard는 수익률을 크게 깎을 수 있다.
- v2에서는 loose guard로 body_atr <= 1.60만 사용한다.

### 4.4 expected_tp >= 0.003

개선안 규칙에 따라 TP03 확인을 유지한다.

```text
expected_tp = atr_stop * rr_target * atrp
expected_tp >= 0.003
```

v2에서 사용한 기본 청산 파라미터는 다음이다.

- atr_stop: 1.05
- rr_target: 2.50
- max_hold_bars: 18
- cooldown_bars: 18

현재 v1/v2 구조에서는 atrp_min이 이미 0.003이므로 TP03은 대부분 실질 필터로 강하게 작동하지 않을 수 있다. 하지만 프로젝트 규칙상 개선안에는 유지한다.

---

## 5. 청산 조건

v2는 v1 기준선의 청산 구조를 유지한다.

- ATR 기반 stop
- RR 기반 target
- max_hold_bars: 18
- cooldown_bars: 18
- position_fraction: 0.01
- round_trip_cost_bps: 8.0

기본 파라미터:

```text
atr_stop = 1.05
rr_target = 2.50
max_hold_bars = 18
cooldown_bars = 18
```

---

## 6. 조건의 역할 요약

| 조건 | 역할 |
|---|---|
| raw_l01_cap_reclaim | v1 기준선 핵심 회복 조건 |
| double_flush_ok | 단일 저점 터치가 아닌 double flush 맥락 확인 |
| close_pos >= 0.77 | 종가 위치 품질 강화 |
| vol_ratio >= 1.45 | 거래량 동반 reclaim 확인 |
| body_atr <= 1.60 | 과도한 장대양봉 추격 제거 |
| expected_tp >= 0.003 | 개선안 TP 기대값 규칙 유지 |

---

## 7. 다음 개발 시 주의

v2 기준선을 개발할 때는 다음을 지켜야 한다.

1. `raw_l01_cap_reclaim + double_flush_ok`를 제거하지 않는다.
2. v2 추가 조건을 기본값으로 둔다.
3. 다음 개선안은 v2 기준선 위에 추가하거나 소폭 변형한다.
4. EMA50 gap, EMA50 slope, trend floor, quiet ratio, ret20 floor는 우선 제외한다.
5. ret1 상한, ATRP 상한, RSI 하한은 롱 메인과 궁합이 나빴으므로 우선 제외한다.
6. body upper guard는 강하게 조이지 않는다.
