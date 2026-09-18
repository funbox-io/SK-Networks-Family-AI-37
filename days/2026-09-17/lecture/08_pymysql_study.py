"""
[08] PyMySQL 을 이용한 DB 접속 실습  (교재 p.134 ~ p.135, 교재 파일명 pymysql_study.py)

실행 : (db) 가상환경에서  python 08_pymysql_study.py

PyMySQL 접속 및 데이터 로드 절차 (p.134)
  1) conn = pymysql.connect(매개변수)
       ① 파이썬 프로그램과 MySQL 데이터베이스를 안전하게 연결해 주는 전용 통로
       ② 매개변수 : host, user, password, db(=database), charset, cursorclass
       ③ cursorclass : MySQL 로부터 조회 결과를 받아올 때 결과값의 형식(자료형)을 결정
            - pymysql.cursors.DictCursor → 조회된 전체 행을 list[dict] 형식으로 수신
            - 예 : [{'id': 1, 'name': '홍길동'}, {'id': 2, 'name': '이순신'}]
  2) cursor = conn.cursor()   : 파이썬 코드로 MySQL 에 명령을 내리고 결과를 받아오는 조작 도구
  3) cursor.execute(sql)      : SQL 쿼리 실행
  4) cursor.fetchall()        : 조회 결과 전체를 한 번에 파이썬으로 가져오는 함수
                                반환 구조 : [{'col1': 값1, 'col2': 값2}, {'col1': 값3, 'col2': 값4}, …]
"""

import pymysql

# ---------------------------------------------------------------------
# DB 접속 정보 — 본인 환경에 맞게 password 를 수정한다
# ---------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",           # MySQL 서버 주소 (내 PC 에 설치했으면 localhost)
    "user": "root",                # 접속 계정
    "password": "1234",            # ★ 본인 MySQL root 비밀번호로 변경
    "database": "world",           # 사용할 데이터베이스 (USE world; 와 같은 역할)
                                   #   ※ 교재 p.134 는 db= 로 표기. 최신 PyMySQL 은 database= 권장 (db 도 동작하나 경고)
    "charset": "utf8mb4",          # 한글 깨짐 방지
    "cursorclass": pymysql.cursors.DictCursor,   # 결과를 list[dict] 로 받는다
}


# 1) DB 연결 — 파이썬과 MySQL 사이의 통로 열기
conn = pymysql.connect(**DB_CONFIG)

try:
    # 2) 커서 생성 — 명령을 내리고 결과를 받아오는 도구
    cursor = conn.cursor()

    # 3) SQL 실행 — 한국(KOR) 도시 중 인구 상위 5개
    #    (Workbench 에서 돌리던 SELECT 문을 문자열로 그대로 넘긴다)
    sql = """
        SELECT Name, District, Population
        FROM city
        WHERE CountryCode = 'KOR'
        ORDER BY Population DESC
        LIMIT 5
    """
    cursor.execute(sql)

    # 4) 결과 전체 가져오기 — DictCursor 이므로 list[dict] 구조
    rows = cursor.fetchall()

    print("조회된 데이터 (파이썬 list[dict] 구조):")
    print(rows)
    print("-" * 80)

    # 5) 파이썬 for 문 + dict 키 추출로 한 줄씩 가공 출력
    #    각 row 는 딕셔너리이므로 row['컬럼명'] 으로 값을 꺼낸다
    print("파이썬 for문 및 dict 키 추출을 이용한 데이터 출력:")
    for row in rows:
        print(f"- 도시명: {row['Name']} | 지역: {row['District']} | 인구수: {row['Population']:,}명")

finally:
    # 6) 연결 종료 — 에러가 나더라도 반드시 닫는다 (finally)
    conn.close()


# ---------------------------------------------------------------------
# 참고 : with 구문을 쓰면 close() 를 직접 부르지 않아도 된다
# ---------------------------------------------------------------------
# with pymysql.connect(**DB_CONFIG) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT COUNT(*) AS cnt FROM city")
#         print(cursor.fetchone())        # 한 행만 → {'cnt': 4079}
