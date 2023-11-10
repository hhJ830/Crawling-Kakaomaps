import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import pandas as pd


# Chrome driver 설정
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 카카오맵 접속
driver.get('https://m.map.kakao.com/actions/index')

# 정보를 저장할 리스트 초기화
clinic_info_list = []

# 검색어 설정
#search_queries = ['천안오케이내과의원', '천안플러스이비인후과의원', '휴먼피부과의원', '평택365연합의원']  # 예시로 몇 가지 검색어를 리스트로 만들었습니다.

# Excel 파일 경로 지정
file_path = 'C:/crawling/병원 검색어 목록.xlsx'
print("가져왔니")

# Excel 파일 읽기, 열 이름 없음을 가정
df = pd.read_excel(file_path, header=None)
# 검색어 목록 추출
# 첫 번째 열의 데이터 추출
search_queries = df[0].tolist()


# 예시: 첫 번째 열을 위치로 참조
#search_queries = df.iloc[0, :].tolist()

# 각 검색어에 대해서 검색 실행
for search_query in search_queries:
    # 검색창 선택 후 검색어 입력, 엔터 키 입력
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.tf_keyword')))
    search_box.clear()  # 이전 검색어를 지웁니다
    search_box.send_keys(search_query + Keys.ENTER)

    # 결과 로딩 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result_place_body')))

    # ... 기존 코드 ...

    # 첫 번째 결과의 이름 가져오기
    try:
        first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result_place_body .info_result')))
        clinic_name = first_result.find_element(By.CSS_SELECTOR, '.info_result .tit_g').text
        clinic_name = ' '.join(clinic_name.split())  # 공백 및 줄바꿈 제거

        # 상세 페이지로 이동
        first_result.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kakaoContent')))
        detail_html = driver.page_source
        detail_soup = BeautifulSoup(detail_html, 'html.parser')

        # 주소 가져오기
        address = detail_soup.select_one('.location_detail .txt_address').get_text().strip()
        address = ' '.join(address.split())

        # 영업시간 정보 가져오기
        try:
            # '영업시간 상세' 버튼 클릭
            detail_time_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ico_comm.ico_more'))
            )
            detail_time_button.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.period_wrap')))
            
            # 상세 정보 다시 로드
            hours_detail_html = driver.page_source
            hours_detail_soup = BeautifulSoup(hours_detail_html, 'html.parser')

            # 영업시간 및 휴무일 정보 추출
            period_lists = hours_detail_soup.select('.displayPeriodList')
            offday_lists = hours_detail_soup.select('.displayOffdayList')

            ing_list = []
            for period_list in period_lists:
                title_elements = period_list.find_all('strong', class_='tit_period')
                for title_element in title_elements:
                    title = ' '.join(title_element.get_text().strip().split())
                    operations = period_list.select('.txt_operation')
                    for operation in operations:
                        clean_operation = ' '.join(operation.get_text().strip().split())
                        ing_list.append(f"{title}: {clean_operation}")

            try:
                off_list = []
                for offday_list in offday_lists:
                    title_elements = offday_list.find_all('strong', class_='tit_period')
                    for title_element in title_elements:
                        title = ' '.join(title_element.get_text().strip().split())
                        operations = offday_list.select('.txt_operation')
                        for operation in operations:
                            clean_operation = ' '.join(operation.get_text().strip().split())
                            off_list.append(f"{title}: {clean_operation}")
            except TimeoutException:
                off_list = ['휴무일 정보 없음']

        except TimeoutException:
            # '.ico_comm.ico_more'가 없거나 클릭할 수 없는 경우, 기본 영업시간 정보 사용
            operations = detail_soup.select('.displayPeriodList .txt_operation')
            ing_list = ['기본 영업시간: ' + ' '.join(op.get_text().split()) for op in operations]

            off_operations = detail_soup.select('.displayOffdayList .txt_operation')
            off_list = ['휴무일: ' + ' '.join(op.get_text().split()) for op in off_operations]

        # 정보 추가
        clinic_info_list.append({
            'name': clinic_name,
            'address': address,
            'operating_hours': ing_list,
            'off_days': off_list
        })

        # 뒤로 가기
        driver.back()

    except TimeoutException as e:
        print(f"TimeoutException for search query '{search_query}': {e}")
        continue



    # 결과 출력 및 JSON 파일 저장
    # ...

    '''# 첫 번째 결과의 이름 가져오기
    try:
        first_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_result_place_body .info_result')))
        clinic_name = first_result.find_element(By.CSS_SELECTOR, '.info_result .tit_g').text
        clinic_name = ' '.join(clinic_name.split()) #깔끔하게 만들기 불필요한 공백, 줄바꿈 제거

        # 상세 페이지로 이동
        first_result.click()

        # 상세 정보 로딩 대기
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kakaoContent')))
        detail_html = driver.page_source
        detail_soup = BeautifulSoup(detail_html, 'html.parser')
        
        # 상세 페이지에서 주소 가져오기
        address = detail_soup.select_one('.location_detail .txt_address').get_text()
        address = address.replace('\n','').replace('\r', '').strip()
        address = ' '.join(address.split()) #깔끔하게 만들기 불필요한 공백, 줄바꿈 제거

        # 상세 페이지에서 영업시간 가져오기 시도
        try:
            # '영업시간 상세' 버튼 클릭 대기
            detail_time_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ico_comm.ico_more'))
            )
            detail_time_button.click()
            # 영업시간 상세 정보 로딩 대기
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.period_wrap')))
            
            # 상세 페이지에서 영업시간 리스트 가져오기
            hours_detail_html = driver.page_source
            hours_detail_soup = BeautifulSoup(hours_detail_html, 'html.parser')

            
            # 영업시간 리스트
            ing_titles = [title.get_text().strip().replace('\n', '').replace('\r', '') for title in hours_detail_soup.select('.period_wrap .displayPeriodList .tit_period')]
            ing_elements = [elem.get_text().strip().replace('\n', '').replace('\r', '') for elem in hours_detail_soup.select('.displayPeriodList .txt_operation')]
            ing_list = [f"{title}: {' '.join(elem.split())}" for title, elem in zip(ing_titles, ing_elements)]

            try:
                off_titles = [title.get_text().strip().replace('\n', '').replace('\r', '') for title in hours_detail_soup.select('.period_wrap .displayOffdayList .tit_period')]
                off_elements = [elem.get_text().strip().replace('\n', '').replace('\r', '') for elem in hours_detail_soup.select('.displayOffdayList .txt_operation')]
                off_list = [f"{title}: {' '.join(elem.split())}" for title, elem in zip(off_titles, off_elements)]
            
            except Exception as e:
                print(f"An exception occurred: {e}")
                #ing_list = ["진료시간 정보가 없습니다."]
                off_list = ['휴무일 정보 없음']
        
        except TimeoutException:
            # 버튼이 없거나 클릭할 수 없으면, 페이지에서 바로 영업시간 가져오기
            # 영업시간 리스트
            ing_titles = [title.get_text().strip().replace('\n', '').replace('\r', '') for title in hours_detail_soup.select('.period_wrap .displayPeriodList .tit_period')]
            ing_elements = [elem.get_text().strip().replace('\n', '').replace('\r', '') for elem in hours_detail_soup.select('.displayPeriodList .txt_operation')]
            ing_list = [f"{title}: {' '.join(elem.split())}" for title, elem in zip(ing_titles, ing_elements)]
            print('버튼없음')

            
            try:
                # 휴무일 리스트
                off_titles = [title.get_text().strip().replace('\n', '').replace('\r', '') for title in hours_detail_soup.select('.period_wrap .displayOffdayList .tit_period')]
                off_elements = [elem.get_text().strip().replace('\n', '').replace('\r', '') for elem in hours_detail_soup.select('.displayOffdayList .txt_operation')]
                off_list = [f"{title}: {' '.join(elem.split())}" for title, elem in zip(off_titles, off_elements)]
            
            
            except Exception as e:
                print(f"An exception occurred: {e}")
                #ing_list = ["진료시간 정보가 없습니다."]
                off_list = ['휴무일 정보 없음']
        
        # 정보 추가
        clinic_info_list.append({
            'name': clinic_name,              
            'address': address,
            'PeriodList': ing_list,  # 수정된 부분: 리스트
            'OffdayList': off_list  # 수정된 부분: 리스트
        })


        # 뒤로 가기
        driver.back()

    except TimeoutException as e:
        print(f"TimeoutException for search query '{search_query}': {e}")            
        continue'''


# 드라이버 종료
driver.quit()


# 결과 출력
print(json.dumps(clinic_info_list, ensure_ascii=False, indent=2))

# JSON 파일로 저장
with open('clinic_data.json', 'w', encoding='utf-8') as f:
    json.dump(clinic_info_list, f, ensure_ascii=False, indent=2)
