# long_main v5 진입 조건

## 1. 전략명

- 공식명: `LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3`
- 개발 후보명: `LM9_012_V4_SHOCK_RECENCY_3`
- 기반 전략: `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`
- 원형 구조: `6V2_L01_doubleflush_core`
- 방향: long

---

## 2. 최종 진입 조건 개요

v5는 v1 기준선의 핵심 진입 조건을 먼저 통과해야 한다.

v1 핵심:

```text
raw_l01_cap_reclaim
AND
double_flush_ok
```

v5 추가/유지 조건:

```text
vol_ratio >= 1.45
AND
body_atr <= 2.20
AND
ret20 <= -0.08
AND
shock_recency <= 3
AND
expected_tp >= 0.003
```

v5에는 다음 조건이 없다.

```text
close_pos >= 0.77
```

단, close_pos 조건이 완전히 제거된 것은 아니다. raw 조건 안의 `close_pos > 0.70`은 그대로 유지된다.

최종 구조:

```text
LONG_MAIN_V5_ENTRY =
    raw_l01_cap_reclaim
    AND double_flush_ok
    AND vol_ratio >= 1.45
    AND body_atr <= 2.20
    AND ret20 <= -0.08
    AND shock_recency <= 3
    AND expected_tp >= 0.003
```

---

## 3. raw_l01_cap_reclaim 조건

`raw_l01_cap_reclaim`은 long_main의 원형 구조다.

구조:

```text
atrp >= 0.003
AND atrp <= 0.070
AND range20p <= 0.180
AND vol_ratio >= 1.35
AND body_atr >= 0.34
AND close > open
AND close_pos > 0.70
AND low <= previous ll20 * 1.003
AND close >= previous ll20
AND ret5 <= 0.025
AND ret10 <= 0.040
AND ret20 <= 0.075
AND ema_guard_soft
```

의미:

- 변동성이 너무 낮은 구간은 제외한다.
- 변동성이 과도한 구간도 제외한다.
- 최근 20봉 range가 과도하게 넓은 구간은 제외한다.
- 거래량이 평균보다 강해야 한다.
- 몸통이 ATR 대비 충분히 있어야 한다.
- 양봉이어야 한다.
- 종가가 캔들 중상단 이상에 있어야 한다.
- 이전 20봉 저점 부근을 찌른 뒤 회복해야 한다.
- 이미 많이 오른 추격 구간은 제외한다.
- EMA guard는 hard trend filter가 아니라 soft guard다.

---

## 4. double_flush_ok 조건

`double_flush_ok`는 최근 10봉 안에 shock_down 또는 flush 흔적이 있었는지 확인한다.

의미:

```text
현재 봉 cap reclaim
AND
최근 10봉 내 shock_down 존재
```

해석:

- 단순 저점 터치 매수가 아니다.
- 먼저 강한 하방 충격이 있어야 한다.
- 그 뒤 현재 봉에서 reclaim이 발생해야 한다.
- long_main의 기본 철학인 “급락 후 reclaim 반전”을 유지한다.

---

## 5. shock_recency <= 3 조건

v5의 핵심 신규 조건이다.

정의:

```text
shock_recency = 현재 진입 후보봉 i 기준, 최근 10봉 내 가장 가까운 shock_down이 몇 봉 전인지 나타내는 값
```

v5 조건:

```text
shock_recency <= 3
```

즉, double_flush_ok가 단순히 최근 10봉 안에 shock_down이 있었는지를 확인한다면, v5는 그 shock_down이 너무 오래된 것이 아닌지 한 번 더 확인한다.

의미:

- 오래된 shock 이후 뒤늦게 나오는 reclaim을 제거한다.
- 더 신선한 하방 충격 직후의 reclaim만 허용한다.
- v4보다 MDD와 승률을 개선하는 방어형 조건이다.

주의:

- `shock_recency <= 3`은 `double_flush_ok`를 대체하지 않는다.
- 반드시 `double_flush_ok`를 먼저 통과한 상태에서 추가로 적용한다.
- shock_recency 계산은 진입 후보봉 기준 과거 데이터만 사용해야 한다.
- 미래 봉 정보를 사용하면 안 된다.

---

## 6. v5 유지 조건

### 6.1 vol_ratio >= 1.45

v1의 기본 거래량 조건은 `vol_ratio >= 1.35`다.

v2부터 추가로 강화한 `vol_ratio >= 1.45`를 v5에서도 유지한다.

의미:

- reclaim이 거래량을 동반했는지 확인한다.
- 거래량 없는 약한 회복을 제거한다.
- v5에서는 ret20 조건과 shock_recency 조건과 결합해 “충분히 빠진 뒤 최근 shock을 동반한 거래량 회복”만 남긴다.

### 6.2 body_atr <= 2.20

v4에서 도입된 완화된 body upper guard다.

의미:

- 충분히 빠진 뒤 강한 반전봉이 나오는 거래를 허용한다.
- body_atr 상한을 완전히 제거하지 않고 2.20에서 제한한다.
- 과도한 장대봉 추격 위험은 일부 남아 있으므로 다음 개발에서도 MDD를 확인해야 한다.

### 6.3 ret20 <= -0.08

v3에서 도입된 핵심 조건이며, v5에서도 유지한다.

의미:

- 최근 20봉 기준 충분히 하락한 상태의 reclaim만 허용한다.
- 덜 빠진 상태에서 발생하는 약한 reclaim을 제거한다.

주의:

- ret20 <= -0.10은 성과가 낮아졌다.
- ret20 <= -0.12는 너무 강했다.
- 현재 기준선 v5에서는 -0.08을 사용한다.

### 6.4 expected_tp >= 0.003

개선안 규칙에 따라 TP03 확인을 유지한다.

```text
expected_tp = atr_stop * rr_target * atrp
expected_tp >= 0.003
```

기본 청산 파라미터:

- atr_stop: 1.05
- rr_target: 2.50
- max_hold_bars: 18
- cooldown_bars: 18

---

## 7. v5에 없는 조건

### 7.1 close_pos >= 0.77 없음

v2는 raw 조건의 `close_pos > 0.70` 위에 `close_pos >= 0.77`을 추가했다.

v3부터 이 추가 조건은 제거되었고, v5에서도 사용하지 않는다.

주의:

- close_pos를 완전히 제거한 것이 아니다.
- raw 조건의 `close_pos > 0.70`은 반드시 유지한다.

---

## 8. 청산 조건

v5는 v4의 청산 구조를 유지한다.

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

## 9. 조건의 역할 요약

| 조건 | 역할 |
|---|---|
| raw_l01_cap_reclaim | 원형 회복 조건 |
| double_flush_ok | 최근 10봉 안의 shock_down 문맥 확인 |
| vol_ratio >= 1.45 | 거래량 동반 reclaim 확인 |
| body_atr <= 2.20 | 강한 반전봉 허용, 과도한 추격 제한 |
| ret20 <= -0.08 | 충분한 20봉 하락 압력 확인 |
| shock_recency <= 3 | 최근 shock 직후의 신선한 reclaim만 허용 |
| expected_tp >= 0.003 | 개선안 TP 기대값 규칙 유지 |

---

## 10. 다음 개발 시 주의

v5 기준선을 개발할 때는 다음을 지켜야 한다.

1. `raw_l01_cap_reclaim + double_flush_ok`를 제거하지 않는다.
2. `vol_ratio >= 1.45`, `body_atr <= 2.20`, `ret20 <= -0.08`, `shock_recency <= 3`을 기본값으로 둔다.
3. `close_pos >= 0.77`은 v5 기준선에는 포함하지 않는다.
4. raw 조건의 `close_pos > 0.70`은 반드시 유지한다.
5. 다음 개선안은 v5 기준선 위에 추가하거나 소폭 변형한다.
6. shock_recency를 2 이하로 강하게 조이면 거래 수 감소 위험이 있으므로 우선순위는 낮다.
7. shock_recency를 4 이상으로 완화하면 v4에 가까워지므로 MDD 방어 효과가 약해질 수 있다.
8. MFE/MAE는 미래 정보이므로 진입 조건에 사용하지 않는다.
