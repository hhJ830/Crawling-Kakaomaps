import csv
import pymysql

# MySQL 데이터베이스에 연결
connection = pymysql.connect(host='localhost', user='root', password='root', db='db')

# CSV 파일 읽기 및 데이터 삽입
def import_csv_to_mysql(csv_file_path, connection):
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 첫 번째 줄(헤더)을 건너뜁니다. 필요하지 않은 경우 이 줄을 제거하세요.

        with connection.cursor() as cursor:
            for row in csv_reader:
                 # 데이터 타입 변환 (예: 첫 번째 필드가 'id'이고 정수형이어야 한다면)
                row[0] = int(row[0])  # 'id' 필드를 정수로 변환
                sql = "INSERT INTO operatinghours (id, business_id, day_of_week, opening_hours, break_time) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, tuple(row))

        connection.commit()

# 실행
csv_file_path = 'C:/Users/jhh88/OneDrive/문서/데베프/operating_data(최종1).csv'
import_csv_to_mysql(csv_file_path, connection)

# 데이터베이스 연결 종료
connection.close()
