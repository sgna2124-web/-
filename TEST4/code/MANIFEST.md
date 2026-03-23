# TEST4 code manifest

복원 대상 원본 파일
- 5m Immediate_Climax_Reversal 1.py
- 5m_Climax_Failure_Reclaim_E16L10.py
- raw_event_scan_50.py
- raw_event_scan_50_results.csv

조각 파일 구성
- 5m_Immediate_Climax_Reversal_1.py.part01.txt ~ part08.txt
- 5m_Climax_Failure_Reclaim_E16L10.py.part01.txt ~ part08.txt

복원 방법
- 각 part 파일을 번호 순서대로 이어붙여 원본 .py 파일로 복원
- raw_event_scan_50_results.csv는 그대로 사용

비고
- GitHub 도구 안전 제한 때문에 긴 코드 파일은 분할 업로드 방식으로 저장
- 원본 대용량 OHLCV CSV는 TEST4/04_data_inventory.csv 인벤토리로만 보관
