import json

# JSON 파일 읽기
with open('weekly_data5.json', 'r', encoding='utf-8') as file:
    clinics = json.load(file)

# 결과를 저장할 리스트
updated_clinics = []

# 각 클리닉별로 데이터 추출
for clinic in clinics:
    clinic_data = {
        "clinic_name": clinic["name"],
        "address": clinic["address"]
    }

    if "weekly_hours" in clinic and isinstance(clinic["weekly_hours"], list):
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(days):
            if i < len(clinic["weekly_hours"]):
                day_data = clinic["weekly_hours"][i]
                clinic_data[f"{day}_hours"] = day_data[0] if day_data else ""  # 운영 시간
                clinic_data[f"{day}_break"] = day_data[1] if len(day_data) > 1 else ""  # 휴게 시간
            else:
                clinic_data[f"{day}_hours"] = ""
                clinic_data[f"{day}_break"] = ""

        # 각 클리닉 데이터를 리스트에 추가
        updated_clinics.append(clinic_data)
    else:
        print(f"{clinic['name']}에는 'weekly_hours' 키가 없습니다.")

# 결과를 새로운 JSON 파일로 저장
with open('weekly_data6.json', 'w', encoding='utf-8') as file:
    json.dump(updated_clinics, file, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 업데이트되었습니다.")
