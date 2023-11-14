import csv
import json

# CSV 파일을 JSON 형태로 변환 (파일 저장 없이 메모리 상에만 저장)
def csv_to_json(csv_file):
    data = []
    with open(csv_file, encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

# Hospital과 OperatingHours 데이터 분리
def split_data(data):
    hospital_data = []
    operating_hours_data = []

    id_counter = 1

    for entry in data:
        # Hospital 데이터 추출 (키가 없는 경우 None을 반환)
        hospital_entry = {key: entry.get(key, None) for key in ['business_id', 'business_name', 'department', 'address', 'phone_number', 'open_date']}
        hospital_data.append(hospital_entry)

        # OperatingHours 데이터 추출 (키가 없는 경우 None을 반환)
        for day in ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']:
            operating_hours_entry = {
                'hours_id': id_counter,
                'business_id': entry.get('business_id', None),
                'day_of_week': day,
                'opening_hours': entry.get(f'{day} 운영시간', None),
                'break_time': entry.get(f'{day} 휴게시간', None)
            }
            operating_hours_data.append(operating_hours_entry)
            id_counter += 1
    return hospital_data, operating_hours_data

# JSON 파일로 저장
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 실행
csv_file = 'C:\crawling\crawling_time\병원 데이터(최종3).csv'
hospital_json_file = 'hospital_info.json'
operating_hours_json_file = 'operating_hours.json'

data = csv_to_json(csv_file)
hospital_data, operating_hours_data = split_data(data)

save_to_json(hospital_data, hospital_json_file)
save_to_json(operating_hours_data, operating_hours_json_file)

with open(csv_file, encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)
    print(headers)

