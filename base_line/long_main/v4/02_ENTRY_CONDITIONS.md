# long_main v4 진입 조건

## 1. 전략명

- 공식명: `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`
- 개발 후보명: `LM8_021_LOOSER_BODY_GUARD_220`
- 기반 전략: `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`
- 원형 구조: `6V2_L01_doubleflush_core`
- 방향: long

---

## 2. 최종 진입 조건 개요

v4는 v1 기준선의 핵심 진입 조건을 먼저 통과해야 한다.

v1 핵심:

```text
raw_l01_cap_reclaim
AND
double_flush_ok
```

v4 추가/유지 조건:

```text
vol_ratio >= 1.45
AND
body_atr <= 2.20
AND
ret20 <= -0.08
AND
expected_tp >= 0.003
```

v4에는 다음 조건이 없다.

```text
close_pos >= 0.77
```

단, close_pos 조건이 완전히 제거된 것은 아니다. v1 raw 조건 안의 `close_pos > 0.70`은 그대로 유지된다.

최종 구조:

```text
LONG_MAIN_V4_ENTRY =
    raw_l01_cap_reclaim
    AND double_flush_ok
    AND vol_ratio >= 1.45
    AND body_atr <= 2.20
    AND ret20 <= -0.08
    AND expected_tp >= 0.003
```

---

## 3. v1 raw_l01_cap_reclaim 조건

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

`double_flush_ok`는 최근 구간에 shock_down 또는 flush 흔적이 있었는지 확인한다.

의미:

```text
현재 봉 cap reclaim
AND
최근 lookback 내 shock_down 존재
```

해석:

- 단순 저점 터치 매수가 아니다.
- 먼저 강한 하방 충격이 있어야 한다.
- 그 뒤 현재 봉에서 reclaim이 발생해야 한다.
- long_main의 기본 철학인 “급락 후 reclaim 반전”을 유지한다.

v4에서는 double_flush lookback 자체를 바꾸지 않는다.

---

## 5. v4 유지/추가 조건

### 5.1 vol_ratio >= 1.45

v1의 기본 거래량 조건은 `vol_ratio >= 1.35`다.

v2, v3에서 추가로 강화한 `vol_ratio >= 1.45`를 v4에서도 유지한다.

의미:

- reclaim이 거래량을 동반했는지 확인한다.
- 거래량 없는 약한 회복을 제거한다.
- v4에서는 ret20 조건과 결합해 “충분히 빠진 뒤 거래량 동반 회복”만 남긴다.

주의:

- vol_ratio를 과하게 높이면 좋은 거래가 제거될 수 있다.
- 현재 기준선 v4는 1.45를 공식값으로 사용한다.

### 5.2 body_atr <= 2.20

v4의 핵심 변경점이다.

v3에서는 `body_atr <= 1.60`을 사용했다.

v4에서는 이를 다음과 같이 완화한다.

```text
body_atr <= 1.60  →  body_atr <= 2.20
```

의미:

- 충분히 빠진 뒤 강한 반전봉이 나오는 거래를 더 허용한다.
- v3의 body guard가 일부 좋은 수익 거래를 막고 있었는지 확인한 결과, v8에서 2.20 완화가 1위를 기록했다.
- ret20 <= -0.08로 충분한 하락 압력을 확인한 상태에서는 body_atr 상한을 더 느슨하게 둬도 성과가 개선되었다.

주의:

- body_atr 상한을 완전히 제거한 것은 아니다.
- 과도한 장대봉 추격 위험은 여전히 존재하므로 2.20 상한은 유지한다.
- v4 이후 개발에서 body_atr 상한을 더 완화하거나 제거할 경우 반드시 v4 exact와 비교해야 한다.

### 5.3 ret20 <= -0.08

v3에서 도입된 핵심 조건이며, v4에서도 유지한다.

의미:

- 최근 20봉 기준 충분히 하락한 상태의 reclaim만 허용한다.
- 덜 빠진 상태에서 발생하는 약한 reclaim을 제거한다.

도입 근거:

- v6 진단에서 손실 거래는 ret20이 덜 빠진 구간에 과대표현되었다.
- v7 실제 백테스트에서 ret20 <= -0.08 계열이 상위권을 장악했다.
- v4에서도 ret20 <= -0.08은 핵심 필터로 유지한다.

주의:

- ret20 <= -0.10은 v3/v4 후보보다 성과가 낮았다.
- ret20 <= -0.12는 너무 강했다.
- 현재 기준선 v4에서는 -0.08을 사용한다.

### 5.4 expected_tp >= 0.003

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

## 6. v4에 없는 조건

### 6.1 close_pos >= 0.77 없음

v2는 v1 raw 조건의 `close_pos > 0.70` 위에 `close_pos >= 0.77`을 추가했다.

v3부터 이 추가 조건은 제거되었고, v4에서도 사용하지 않는다.

이유:

- v6 진단 결과상 손실 과대표현의 핵심은 close_pos보다 ret20 부족이었다.
- 충분한 하락 압력(ret20 <= -0.08)이 확인되면 close_pos를 0.77까지 강제하지 않아도 성과가 더 좋았다.

주의:

- close_pos를 완전히 제거한 것이 아니다.
- v1 raw 조건의 `close_pos > 0.70`은 반드시 유지한다.

---

## 7. 청산 조건

v4는 v3의 청산 구조를 유지한다.

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

## 8. 조건의 역할 요약

| 조건 | 역할 |
|---|---|
| raw_l01_cap_reclaim | v1 기준선 핵심 회복 조건 |
| double_flush_ok | 단일 저점 터치가 아닌 double flush 문맥 확인 |
| vol_ratio >= 1.45 | 거래량 동반 reclaim 확인 |
| body_atr <= 2.20 | 강한 반전봉을 허용하되 과도한 추격은 제한 |
| ret20 <= -0.08 | 충분한 20봉 하락 압력 확인 |
| expected_tp >= 0.003 | 개선안 TP 기대값 규칙 유지 |

---

## 9. 다음 개발 시 주의

v4 기준선을 개발할 때는 다음을 지켜야 한다.

1. `raw_l01_cap_reclaim + double_flush_ok`를 제거하지 않는다.
2. `vol_ratio >= 1.45`, `body_atr <= 2.20`, `ret20 <= -0.08`을 기본값으로 둔다.
3. `close_pos >= 0.77`은 v4 기준선에는 포함하지 않는다.
4. v1 raw의 `close_pos > 0.70`은 반드시 유지한다.
5. 다음 개선안은 v4 기준선 위에 추가하거나 소폭 변형한다.
6. body_atr 상한을 완전히 제거하거나 2.20보다 더 완화할 경우 MDD 증가 여부를 반드시 확인한다.
7. ret20을 -0.12처럼 강하게 조이는 방향은 우선 제외한다.
8. MFE/MAE는 미래 정보이므로 진입 조건에 사용하지 않는다.
