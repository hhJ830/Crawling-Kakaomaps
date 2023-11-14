import json
import pandas as pd

# JSON 파일 읽기
with open('operating_hours.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# JSON 데이터를 Pandas DataFrame으로 변환
df = pd.DataFrame(data)

# DataFrame을 Excel 파일로 저장
df.to_excel('operating_data.xlsx', index=False)
