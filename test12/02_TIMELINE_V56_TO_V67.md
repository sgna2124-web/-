V56~V67 타임라인 및 결론

v56
- 숏 전용 hybrid guards and entry modes
- 목적: behavioral guard + diverse entry mode를 한 엔진에서 동시에 보기
- 결론: 숏 메인형 기준선 정립에 큰 의미. dd_brake, dense30 계열이 핵심 축으로 부상

v57
- 롱 전용 hybrid guards and entry modes
- 목적: 롱에서도 behavioral guard + entry mode 결합 검증
- 결론: 롱 메인 철학의 기반 형성. 이후 long_hybrid_symbol1_dd_confirmation 계열로 이어짐

v58
- 숏 전용 session and cadence hybrid
- 결론: baseline 교체 실패. session/cadence 제약이 수익을 너무 많이 깎음

v59
- 롱 전용 session and cadence hybrid
- 결론: baseline drift 발생. 일부 힌트는 있었으나, 롱 저MDD 메인 교체 실패

v60
- 숏 전용 confirmation weird mix
- 결론: 사실상 완패. reclaim/followthrough/no_chase 계열이 숏에서는 유효하지 않았음

v61
- 롱 전용 confirmation weird mix
- 결론: 역시 실패. 롱에서 standalone weird confirmation은 MDD만 커지고 실전성 부족

v62a
- 숏 전용 multimethod architectures
- 결론: 구조 힌트는 일부 있었지만 메인형 교체 실패. short_multi_reclaim 정도만 약한 힌트

v62b
- 숏 전용 split architectures
- 결론: 강한 공격형 후보 발굴. pure_atr050_2bar, pure_atr025_1bar, pure_wick075_2bar가 고수익 구조 후보로 등장. 다만 max_conc가 지나치게 높음

v63a
- 롱 전용 multimethod architectures
- 결론: 실패. 롱에서 multimethod 필터 계열은 수익성/실전성 모두 약함

v63b
- 롱 전용 split architectures
- 결론: wick 부분 진입 힌트 확보. pure retrace보다 wick partial entry가 더 낫다는 방향성만 남김

v64
- 숏 전용 guarded split hybrid
- 결론: 너무 방어적으로 기울어 수익이 크게 죽음. 초방어형 후보는 남았지만 메인 교체 실패

v65
- 롱 전용 guarded wick split hybrid
- 결론: 극저MDD형 후보군 형성. 다만 수익이 너무 낮아 메인형으로 쓰기 어려움

v66
- 숏 전용 balanced split bridge hybrid
- 목적: v62 공격형과 v64 방어형 사이의 중간지대 찾기
- 결론: short_balanced_bridge_atr050_prior1_24, short_balanced_bridge_wick075_dense30, short_balanced_bridge_wick075_prior1_24가 MDD 5% 미만 + cd_value 기준으로 의미 있는 bridge 후보로 등장

v67
- 롱 전용 hybrid wick bridge
- 목적: 과거 롱 메인 철학과 v65 wick 부분 진입 저MDD 힌트를 결합
- 결론: long_hybrid_wick_bridge_halfhalf, quiet48, us_max40이 현재 롱 cd_value 기준 상위권. 롱 수익 엔진 강화의 첫 실마리

큰 흐름 요약
1. 숏
- behavioral guard + dense skip 철학이 가장 강력했다.
- split 공격형은 엄청난 수익을 주지만 max_conc가 너무 높았다.
- 최근 방향은 공격형과 방어형의 중간지대를 찾는 것

2. 롱
- standalone weird/confirmation/multimethod는 계속 실패했다.
- wick 부분 진입과 quiet/us_only 같은 운영 필터가 그나마 유효했다.
- 최근 방향은 기존 저MDD 메인형 철학에 wick 부분 진입을 bridge처럼 접목하는 것

현재 타임라인상 가장 중요한 구간
- v56/v57: hybrid 기반 형성
- v62/v63: split/multimethod 대탐색
- v64/v65: guarded family 실험
- v66/v67: bridge family 등장 및 cd_value 포함 결과 정렬 가능화
