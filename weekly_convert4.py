import json
import re

def parse_days(day_str):
    print(day_str)
    days_of_week = ["월", "화", "수", "목", "금", "토", "일"]
    day_indices = []

    if isinstance(day_str, list) and len(day_str) == 0:
        # day_str이 빈 리스트인 경우 "정보없음"으로 처리
        return ["정보없음"]
    
    if day_str.strip():
        print("실행?")
        if ',' in day_str:
            days = day_str.split(',')
            for day in days:
                # 요일 문자열이 days_of_week에 없는 경우 "정보없음"으로 처리
                if day.strip() in days_of_week:
                    day_indices.append(days_of_week.index(day.strip()))
                else:
                    day_indices.append("정보없음")
        elif '~' in day_str:
            start_day, end_day = day_str.split('~')
            start_index = days_of_week.index(start_day.strip())
            end_index = days_of_week.index(end_day.strip())
            day_indices = list(range(start_index, end_index + 1))
        elif '매일' in day_str:
            day_indices = list(range(7))
        else:
            # 요일 문자열이 days_of_week에 없는 경우 "정보없음"으로 처리
            if day_str.strip() in days_of_week:
                day_indices.append(days_of_week.index(day_str.strip()))
            else:
                day_indices.append("정보없음")
        # 문자열이 '진료시간:' 또는 '영업시간:'으로 시작하는 경우
        '''if day_str.startswith('진료시간:') or day_str.startswith('영업시간:'):
            day_str = day_str[len('진료시간:' if day_str.startswith('진료시간:') else '영업시간:'):].strip()
            
            if ',' in day_str:
                days = day_str.split(',')
                for day in days:
                    # 요일 문자열이 days_of_week에 없는 경우 "정보없음"으로 처리
                    if day.strip() in days_of_week:
                        day_indices.append(days_of_week.index(day.strip()))
                    else:
                        day_indices.append("정보없음")
            elif '~' in day_str:
                start_day, end_day = day_str.split('~')
                start_index = days_of_week.index(start_day.strip())
                end_index = days_of_week.index(end_day.strip())
                day_indices = list(range(start_index, end_index + 1))
            else:
                # 요일 문자열이 days_of_week에 없는 경우 "정보없음"으로 처리
                if day_str.strip() in days_of_week:
                    day_indices.append(days_of_week.index(day_str.strip()))
                else:
                    day_indices.append("정보없음")
                    '''
        
        #print(day_indices)
    return day_indices

def extract_times(operating_hours):
    weekly_hours = [[] for _ in range(7)]
    #break_times = [[] for _ in range(7)]

    for hours_str in operating_hours:
        # 공백을 기준으로 문자열을 나눕니다.
        parts = hours_str.split(" ")
        #for i in parts:
        
        day_part = parts[1] if len(parts) > 1 else ""
        
        # 시간 정보를 추출합니다.
        hours_part = " ".join(parts[2:]) if len(parts) > 2 else parts[0]

        print(parts)
        print(day_part)
        print(hours_part)
        # 공백이 없는 경우 (시간 정보)
        if ":" in hours_part:
            day_indices = parse_days(day_part)
            print(day_indices)
            hours_part = re.sub(r'[^0-9:~]', '', hours_part).strip()  # 숫자와 시간 관련 문자만 남깁니다.
            for index in day_indices:
                # 요일이 "정보없음"이 아닌 경우에만 처리
                if index != "정보없음":
                    if '매일' in parts[0]:
                        # '매일'이 포함된 경우 모든 요일에 추가
                        weekly_hours[index].append(hours_part)
                    else:
                        # '매일'이 아닌 경우 해당 요일의 운영시간을 저장합니다.
                        weekly_hours[index].append(hours_part)
        # 공백이 있는 경우 (진료시간 또는 휴게시간)
        elif parts[0].endswith(':'):
            
            if '휴게시간' in parts[0]:
                if '매일' in parts[0]:
                    day_indices=list(range(7))
                else:
                    day_indices = parse_days(day_part)
                for index in day_indices:
                    # 요일이 "정보없음"이 아닌 경우에만 처리
                    if index != "정보없음":
                        weekly_hours[index].append(hours_part)  # 해당 요일의 휴게시간을 저장합니다.
        #print(weekly_hours, break_times)
    return weekly_hours

# JSON 파일 읽기
with open('updated_data2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 각 항목에 대해 로직 수행
for item in data:
    operating_hours = item['operating_hours']
    weekly_hours = extract_times(operating_hours)
    item['weekly_hours'] = weekly_hours
    #item['break_times'] = break_times
for item in data:
    if 'break_times' in item:
        del item['break_times']

# 결과를 JSON 파일로 저장
with open('weekly_data5.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)