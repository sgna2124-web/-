실험 타임라인 v41 ~ v55

이 문서는 최근 대화창에서 진행된 핵심 실험 흐름을 빠르게 복기하기 위한 타임라인이다.
각 버전은 무엇을 검증하려고 했는지, 무엇을 배웠는지를 중심으로 기록한다.

v41 structural gate exploration
- 목적: 파라미터 조정이 아니라 구조 조건 탐색으로 전환.
- 철학: burst 차단, dominant side 차단, active freeze, conflict 처리 같은 구조적 진입 차단 정책 실험.
- 결론: 기존 고수익 구조와 강한 진입 억제 정책은 상성이 나빴다. 수익을 크게 훼손하는 경우가 많았다.

v42 rr60_t200_short_only leverage10
- 목적: MDD 10% 미만 후보 중 유력한 short_only에 레버리지 10배를 얹어보기.
- 문제: position_fraction 0.10으로 처리해 총노출 왜곡. 현실형 10배 모델로 보기 어려움.
- 결론: 참조는 가능했지만 실전형 모델로는 부적절. 수정 필요.

v43 rr60_t200_short_only split300 leverage10
- 목적: 300분할 기준으로 레버리지 10배 모델 정정.
- 결론: v42보다 훨씬 현실적이었지만, 여전히 레버리지 고배수는 MDD 부담이 컸다.
- 학습: 레버리지는 저MDD 전략에 얹을 때가 훨씬 낫다는 결론 강화.

v44 short_only structural gates
- 목적: 숏 전용 기준선에 구조 게이트 부착.
- 결론: baseline이 여전히 1위였지만, defense_combo / dominant_short 계열이 방어형 후보로 의미가 있었다.
- 학습: 숏 전용은 이미 baseline 구조가 강하며, 구조 게이트는 방어형 서브 전략으로는 의미가 있다.

v45 long_only architecture exploration
- 목적: 롱 전용 아키텍처 탐색 시작.
- 결론: 실패에 가까움. MDD가 여전히 너무 컸다.
- 학습: 롱은 숏의 대칭으로 풀 수 없고, 별도 철학이 필요하다.

v46 short_only low MDD exploration
- 목적: 숏 전용 저MDD 탐색을 본격화.
- 성과: short_lowmdd_asym_short_s22, short_lowmdd_rr30_t40_defense 등 유의미한 숏 저MDD 후보군 형성.
- 학습: 숏은 신호 품질 강화 + 보수적 청산 구조에서 저MDD 후보가 잘 나온다.

v47 long_only low MDD exploration
- 목적: 롱 전용도 저MDD를 향해 구조적으로 압축.
- 성과: 롱 MDD를 40%대에서 15%대로 끌어내리는 데 성공.
- 한계: 아직 10% 미만은 못 만듦.

v48 short_only hybrid low MDD
- 목적: 46의 균형형 후보와 방어형 후보를 교배.
- 성과: 숏 전용 메인형 / 극방어형 분화가 더욱 선명해짐.
- 학습: 숏은 이미 전략군이 형성되기 시작했음.

v49 long_only hybrid low MDD
- 목적: 47의 방어형 롱 후보를 기준으로, 더 짧은 timeout/더 낮은 RR/더 강한 defense 조합 실험.
- 성과: 롱 전용이 MDD 10% 직전까지 접근.
- 학습: 롱은 rr 0.8~1.0, timeout 10~12, 강한 block 계열이 저MDD에 유효.

v50 short_only next low MDD
- 목적: 숏 전용 s22 계열을 더 보수적으로 재구성.
- 성과: short_next_baseline_s22, short_next_rr30_t40_s22 등으로 숏 메인형 / 보수형 / 극방어형 구조가 더 선명해짐.
- 학습: 숏은 MDD 3%대까지도 충분히 내려갈 수 있음.

v51 long_only push under10
- 목적: 롱 전용 MDD 10% 미만 직접 돌파.
- 성과: long_push_u10_rr08_t10_ema_rr_more_block, long_push_u10_ema_rr_more_block 등 MDD 10% 미만 후보를 처음 확보.
- 학습: 롱도 구조적 압축을 통해 10% 미만 전략이 가능함.

v52 short_only behavioral guards
- 목적: 파라미터가 아니라 행동 규칙(브레이크 시스템) 자체를 바꾸기.
- 규칙: loss streak freeze, drawdown brake, max active cap, per-symbol cap 등.
- 성과: short_beh_dd_brake, short_beh_conservative_combo 등 유의미한 행동 규칙형 후보 등장.
- 학습: 숏은 dd_brake가 매우 실전적이며, conservative combo는 극방어형으로 강력.

v53 long_only behavioral guards
- 목적: 롱 전용에도 behavioral guards 적용.
- 성과: long_beh_max50_plus_lossbrake, long_beh_conservative_combo 등 매우 강한 롱 저MDD 후보 등장.
- 학습: 롱은 behavioral guard가 특히 강하게 먹힘.
- 주의: baseline 해석 시 direct lineage를 주의해야 함.

v54 short_only diverse entry modes
- 목적: 진입 방식 자체를 바꾸는 실험.
- 규칙: confirmation24, first_after_quiet48, reentry_gap48, us/asia hours only, dense_skip30 등.
- 성과: short_div_dense_skip30, short_div_first_after_quiet48, short_div_reentry_gap48 등 새로운 숏 전용 후보 다수 확보.
- 학습: 숏은 과밀 시점 회피, 고요 후 첫 신호, 재진입 금지 같은 entry mode 변경이 매우 잘 먹힘.

v55 long_only diverse entry modes
- 목적: 롱 전용에도 diverse entry modes 적용.
- 성과: long_div_confirmation_plus_reentry, long_div_dense_skip30_confirm 등 새로운 롱 전용 후보 확보.
- 학습: 롱은 반복 확인 + 재진입 금지, 밀집 회피 + 확인형이 유망.
- 주의: v55 러너는 max_active_cap/loss_streak 계열을 직접 사용하지 않으므로 baseline_lossbrake 이름을 문자 그대로 해석하면 안 됨.

타임라인 총평
1. 프로젝트는 cd_value 중심에서 MDD 우선 체계로 전환했다.
2. 양방향 전략 하나로 해결하려던 흐름에서, 롱 전용 / 숏 전용 분리 개발 체계로 전환했다.
3. 숏 전용은 이미 전략군이 형성되었다.
4. 롱 전용은 v51~v55 구간에서 드디어 실질적인 저MDD 전략군이 생기기 시작했다.
5. 최근 가장 중요한 성과는 behavioral guard와 diverse entry mode라는 두 개의 새로운 철학이 실제로 유효했다는 점이다.
