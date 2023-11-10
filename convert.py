import json

# JSON 파일을 불러옵니다.
with open('updated_data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 결과를 저장할 새로운 리스트를 초기화합니다.
updated_clinics = []

# 각 클리닉의 데이터를 순회하면서 필터링을 수행합니다.
for clinic in data:
    # "진료시간:" 또는 "영업시간:"을 포함하는 operating_hours 항목만 필터링합니다.
    filtered_hours = [hour for hour in clinic['operating_hours'] if "진료시간:" in hour or "영업시간:" in hour]
    filtered_hours = [hour.replace("닫기", "") for hour in clinic['operating_hours']]
    filtered_hours = [hour.replace("기본 영업시간", "진료시간") for hour in clinic['operating_hours']]
    filtered_hours = [hour.replace("영업시간", "진료시간") for hour in clinic['operating_hours']]
    filtered_hours = [hour.replace("(점심시간 없음)", "") for hour in clinic['operating_hours']]
    filtered_hours = [hour.replace("기본 진료시간", "진료시간") for hour in clinic['operating_hours']]


    # "닫기"라는 단어를 제거합니다.
    filtered_off_days = [off_day.replace("닫기", "") for off_day in clinic['off_days']]

    # 필터링된 결과를 저장합니다.
    updated_clinics.append({
        'name': clinic['name'],
        'address': clinic['address'],
        'operating_hours': filtered_hours,
        'off_days': filtered_off_days
    })

# 결과를 출력합니다.
print(json.dumps(updated_clinics, ensure_ascii=False, indent=2))

# 필요하다면 결과를 새로운 JSON 파일로 저장할 수 있습니다.
with open('updated_data2.json', 'w', encoding='utf-8') as f:
    json.dump(updated_clinics, f, ensure_ascii=False, indent=2)
