현재 최상위 후보군 요약

기준
- 아래 후보군은 최근 실험 라운드(v50~v55 및 관련 직전 라운드) 기준으로 현재 가장 중요하다고 판단되는 전용 전략들이다.
- 분류는 다음과 같다.
  1. 메인형: 수익과 MDD의 균형이 좋은 후보
  2. 극방어형: MDD를 아주 낮게 만든 후보
  3. 새로운 진입 철학형: 행동 브레이크 또는 diverse entry mode 기반 후보

숏 전용 현재 핵심 후보군

A. short_next_baseline_s22
- 출처: v50
- 성격: 숏 전용 메인형 기준선
- 최대 수익률: 319.0419%
- MDD: -5.0169%
- 최대 보유 포지션: 286
- 승률: 15.0864%
- PF: 1.4503
- 해석: 현재 숏 전용 메인형 기준선. 수익과 MDD의 균형이 가장 좋다.

B. short_beh_dd_brake
- 출처: v52
- 성격: 행동 브레이크 기반 메인형 개선 후보
- 최대 수익률: 311.5456%
- MDD: -4.7589%
- 최대 보유 포지션: 286
- 승률: 15.0623%
- PF: 1.4457
- 해석: baseline 대비 수익 감소는 작고 MDD 개선이 있는 실전적 후보. 숏 메인형 업데이트 후보.

C. short_div_dense_skip30
- 출처: v54
- 성격: 밀집 타임스탬프 회피형
- 최대 수익률: 251.3963%
- MDD: -3.6805%
- 최대 보유 포지션: 55
- 승률: 14.5801%
- PF: 1.4013
- 해석: “한 시점에 후보가 너무 많으면 그 시점을 통째로 건너뛴다”는 철학이 먹힌 사례. 수익과 MDD를 동시에 낮춘 새 진입 모드형.

D. short_next_rr30_t40_s22
- 출처: v50
- 성격: 숏 전용 극방어형(보수적 청산형)
- 최대 수익률: 141.7084%
- MDD: -3.0599%
- 최대 보유 포지션: 286
- 승률: 25.0689%
- PF: 1.2609
- 해석: 극방어형이지만 수익도 아주 낮지는 않다. 전통적인 보수형 숏 후보.

E. short_beh_conservative_combo
- 출처: v52
- 성격: behavioral guard 극방어형
- 최대 수익률: 144.8252%
- MDD: -2.5182%
- 최대 보유 포지션: 60
- 승률: 14.8562%
- PF: 1.4883
- 해석: MDD 2%대까지 내려간 매우 강한 극방어 후보. PF도 높다.

F. short_div_first_after_quiet48
- 출처: v54
- 성격: 고요 후 첫 신호형
- 최대 수익률: 47.4925%
- MDD: -1.6902%
- 최대 보유 포지션: 130
- 승률: 16.8119%
- PF: 1.4897
- 해석: “한동안 신호가 없다가 나온 첫 신호만 받는다”는 철학이 숏에서 극강 방어 효과를 냄.

G. short_div_reentry_gap48
- 출처: v54
- 성격: 청산 후 재진입 금지형
- 최대 수익률: 53.1100%
- MDD: -1.7075%
- 최대 보유 포지션: 151
- 승률: 16.6208%
- PF: 1.4744
- 해석: 실전적인 극방어 후보. 고요 후 첫 신호형보다 설명이 단순하고 재현성도 좋다.

숏 전용 현재 정리
- 메인형 1순위: short_beh_dd_brake 또는 short_next_baseline_s22
- 메인형 2순위: short_div_dense_skip30
- 극방어형 1순위: short_beh_conservative_combo
- 극방어형 2순위: short_next_rr30_t40_s22
- 초극방어형 실험 후보: short_div_first_after_quiet48, short_div_reentry_gap48

롱 전용 현재 핵심 후보군

A. long_push_u10_ema_rr_more_block
- 출처: v51
- 성격: 롱 전용 MDD 10% 미만 첫 메인형 후보군
- 최대 수익률: 97.0750%
- MDD: -9.4159%
- 최대 보유 포지션: 78
- 승률: 46.9012%
- PF: 1.2243
- 해석: 롱 전용이 처음으로 의미 있게 10% 미만을 유지한 메인형 후보 중 하나.

B. long_push_u10_rr08_t10_ema_rr_more_block
- 출처: v51
- 성격: 롱 전용 최저MDD 근접형
- 최대 수익률: 80.6681%
- MDD: -9.2294%
- 최대 보유 포지션: 87
- 승률: 53.6263%
- PF: 1.2047
- 해석: v51 시점에서 롱 전용 최저MDD 후보.

C. long_beh_max50_plus_lossbrake
- 출처: v53
- 성격: behavioral guard 기반 롱 메인형
- 최대 수익률: 81.0411%
- MDD: -7.0753%
- 최대 보유 포지션: 50
- 승률: 50.3251%
- PF: 1.3424
- 해석: behavioral guard 계열에서 가장 균형이 좋은 롱 메인형 후보. 현재 롱 전용 핵심 후보 중 하나.

D. long_beh_conservative_combo
- 출처: v53
- 성격: behavioral guard 극방어형
- 최대 수익률: 59.5996%
- MDD: -6.0715%
- 최대 보유 포지션: 40
- 승률: 50.4477%
- PF: 1.3040
- 해석: 롱 전용에서 매우 강한 극방어형.

E. long_div_confirmation_plus_reentry
- 출처: v55
- 성격: 반복 확인 + 재진입 금지형
- 최대 수익률: 51.4272%
- MDD: -7.2922%
- 최대 보유 포지션: 156
- 승률: 51.2903%
- PF: 1.5749
- 해석: diverse entry mode 계열에서 가장 유망한 롱 후보. PF가 매우 높다.

F. long_div_dense_skip30_confirm
- 출처: v55
- 성격: 밀집 회피 + 반복 확인형
- 최대 수익률: 49.3508%
- MDD: -6.8402%
- 최대 보유 포지션: 141
- 승률: 49.0309%
- PF: 1.1820
- 해석: 롱 전용 diverse entry mode 중 최저 MDD 후보.

롱 전용 현재 정리
- 메인형 1순위: long_beh_max50_plus_lossbrake
- 메인형 2순위: long_push_u10_ema_rr_more_block
- 새 진입 철학형 1순위: long_div_confirmation_plus_reentry
- 극방어형 1순위: long_beh_conservative_combo
- 극방어형 2순위: long_div_dense_skip30_confirm

현재 판단 요약
- 숏 전용은 이미 전략군이 많이 생겼다. 메인형 / 보수형 / 극방어형 / 초극방어형으로 분화가 끝난 상태다.
- 롱 전용은 늦게 출발했지만, 현재는 behavioral guard와 diverse entry mode 덕분에 MDD 10% 미만 전략군이 형성되기 시작했다.
- 다음 단계는 이 후보들을 서로 교배하거나, 완전히 다른 진입 철학(예: 지연 진입형)을 더 붙여 확장하는 것이다.

나중에 cd_value 정리 시 후보군 우선 포함 대상
- 숏: short_beh_dd_brake, short_div_dense_skip30, short_beh_conservative_combo, short_next_rr30_t40_s22, short_div_reentry_gap48
- 롱: long_beh_max50_plus_lossbrake, long_beh_conservative_combo, long_div_confirmation_plus_reentry, long_div_dense_skip30_confirm, long_push_u10_ema_rr_more_block
