# 03_TIMELINE_AND_RESULTS

이 파일은 이번 대화에서 실제로 시도한 흐름을 시간순으로 정리한 것이다. 일부 과거 플러스 결과는 뒤에서 설명하는 엔진 문제로 무효 처리되었다.

## A. 초기 대량 전략 폭격
- 20개 전략을 10종목(2021년 이후)으로 테스트
- 결과: 전부 음수 또는 거래 0건
- 관찰: 링크(LINK)에서 대부분 최악, 일부 소형 종목(BOB/SENT/IRYS)만 약간 버티는 경우 존재

## B. 원시 사건 30개 스캔
상위권
- VOLREV_L
- SWP4_L / SWP4_S
- DPROBE_L
- SHRK_L
- NR2_L

전략화 후
- NR5_S, NR1_S, IR1_S 등 숏 편향 후보 테스트
- 결과: 전부 음수, 다만 숏 승률이 롱보다 높은 구간 관찰

## C. NR5 계열
- NR5-B, NR5-D, NR5-F 등이 일시적으로 플러스처럼 보이는 결과가 있었으나, 이후 엔진 재검증에서 재현되지 않거나 일관성 부족
- 결론: 약한 힌트는 있었으나 실전 카드 아님

## D. VOLREV 계열
- VOLREV, VOLREV-10, EXH, STALL 등에서 플러스처럼 보이는 결과 보고
- 이후 개선안(combo/wick/collapse/noextend/tfail) 전부 실패
- 엔진 불일치 문제 때문에 초기 플러스 결과 자체도 신뢰도 하락

## E. CLX / DEAD / EXH 재스캔 루프
- CLX_exhaustion_L, OPEN_retake_S, INSIDE_impulse_flip_S 전략화
- 결과: CLX_exhaustion_L는 거의 보합(-0.25%)이었으나 Peak도 거의 없어서 채택 보류
- DEAD_OPEN, DEAD_MID, EXH_OPEN, EXH_TWOBAR, EXH_MID 전략화
- 결과: 전부 음수, DEAD_OPEN만 -0.26%로 가장 덜 나쁨
- DEAD_OPEN 변형 5개(wick/mid/inside/twobar/cluster) -> 전부 폐기

## F. ACC3 계열
- 원시 사건 재스캔에서 ACC3_fail_break, RANGE3_dead, INSIDE3_fail, WICK_cluster_flip, BODY_stall_break가 상위권으로 관측됨
- 전략화 백테스트에서 ACC3_fail_break가 +4.92% / Peak +5.63% / MDD -2.11% 로 가장 좋아 보였으나,
- 변형 5개(ACC3_combo, rng, mid, wick, base) 재테스트에서 전부 음수로 붕괴
- 결론: 초기 결과 신뢰 불가, 구조 안정성 부족

## G. noextend_5_2.0_mid
- 한 차례 +6.56%, Peak +7.47%, MDD -0.85% 로 보고됨
- 이후 RR x 이벤트강도 그리드 재테스트에서 전 조합 음수
- 코드/결과 무결성 문제로 이전 양수 결과 무효 처리
- 결론: 전략 축 자체 폐기 권고

## H. 최근 재스캔 후보
- NOEXTEND_BREAK_S
- WICK_TRAP_S
- REVERSAL_ENGULF_S
전략화 후 전부 큰 폭 음수

## 종합 결론
- 현재까지 신뢰 가능한 최종 채택 전략은 없음
- 플러스처럼 보였던 일부 전략은 엔진 불일치/버그 가능성 때문에 무효 처리
- 남아 있는 유효한 교훈은 "비정상 확장 -> 전달 실패 -> 중심값 복귀" 구조가 반복적으로 후보로 떠올랐다는 정도
