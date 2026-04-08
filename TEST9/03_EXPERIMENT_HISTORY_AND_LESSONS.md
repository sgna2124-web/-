실험 역사와 교훈

1단계: timeout_18bars baseline 시대
- 출발점은 timeout_18bars baseline 이었다.
- 이 전략은 오랫동안 기준선 역할을 했다.
- 하지만 MDD가 높았고, 상단 수익도 더 개선 여지가 있었다.

2단계: hybrid stack, confirmation, retrace, exitcraft 탐색
- fail_fast, light quality, confirmation, retrace entry, various trailing/breakeven 등을 시도했다.
- 관찰 결과:
  - confirmation: 기회를 너무 많이 버리는 경향
  - pure retrace: 체결을 많이 놓침
  - trailing / breakeven: 너무 빨리 이익을 잘라 상단 수익 훼손
  - fail_fast: 일부 구간에서는 의미 있었지만 절대 1위 구조는 되지 못함
- 결론: 진입 필터를 더 복잡하게 만드는 것은 주력 해답이 아니었다.

3단계: stopshape 승리
- ema_only_target 계열이 큰 개선을 보였다.
- rr_only_target 도 강했지만, ema_only_target 이 상위가 됐다.
- 여기서 핵심 통찰이 나왔다.
  - 문제는 진입보다 목표가 구조에 있었다.

4단계: ema_only + atr_only + longer timeout
- ema_only target 위에 atr_only stop 을 얹자 성과가 더 올라갔다.
- timeout 을 24, 26, 27 쪽으로 늘리면서 공격형이 강해졌다.
- 여기까지의 결론:
  - stop 구조와 보유 구조가 핵심 변수다.
  - 품질 필터는 보조 변수다.

5단계: attack refine / attack defense
- atr17_t24, atr18_t26 같은 공격형 후보가 올라왔다.
- 여기서 후반 보호 구조를 다시 실험했다.
- 조기 breakeven, prevbar trail, ATR trail 같은 방식은 기대만큼 좋지 않았다.
- 하지만 time_reduce 구조가 대성공했다.

6단계: time_reduce 시대 개막
- time_reduce_b16_r050 이 크게 개선되며 새로운 흐름을 만들었다.
- 이후 더 강하게 줄인 tr_b16_r030 이 다시 1위가 됐다.
- 이후 atr_stop_mult 조정과 timeout 27 결합이 겹치며 성과가 더 올라갔다.

7단계: v3, v4 초미세 조정
- tr_b16_r030_atr19 가 1위가 된 뒤,
  timeout 27 + 17봉 후 25% 축소 + atr 1.9 로 atr19_t27_b17_r025 가 새 1위가 됐다.
- 그 다음 v4 초미세 조정에서 risk_frac 0.20 이 0.25 를 넘어섰다.
- 최종적으로 atr19_t27_b17_r020 이 현재 1위가 됐다.

실패 패턴 요약
- confirmation 계열: 너무 엄격해서 기회 상실
- pure retrace 계열: 체결 상실
- 초기 breakeven / 공격적 trailing: 상단 수익 훼손
- short_light 단독 강화: 보조적 의미는 있지만 핵심 승리 변수는 아님
- long_light: 안정형 후보에는 도움되지만 공격형 절대 1위를 만드는 핵심은 아니었음

성공 패턴 요약
- ema_only target 이 큰 전환점이었다.
- atr_only stop 이 그 위에 추가 개선을 만들었다.
- timeout 연장은 24 -> 26 -> 27 축으로 상단을 밀어올렸다.
- time_reduce 가 가장 중요한 보호 구조로 판명됐다.
- time_reduce 타이밍과 강도 미세 조정이 최근 모든 개선을 주도했다.
- 현재 상단 구조는 timeout 27 + atr 1.9 + time_reduce 17봉 20% 축소 근방이다.

다음 대화창에서 절대 잊지 말 것
- 지금은 진입 필터 싸움이 아니라 risk structure 싸움이다.
- 특히 time_reduce 계열이 가장 중요한 축이다.
- 탐색 우선순위는 timeout 27, atr 1.9 부근, time_reduce 16~18봉, risk_frac 0.18~0.22 부근이다.
