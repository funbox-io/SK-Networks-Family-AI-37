"""
[10] PyMySQL + Streamlit 위젯(st.selectbox, st.form) 동적 연동 실습
     (교재 p.137, 교재 파일명 app_search.py)

실행 : (db) 가상환경에서  streamlit run 10_app_search.py

흐름 : 사이드바 selectbox 로 대륙 선택 → 폼에서 최소 인구수 입력 → [DB 검색 실행]
       → 입력값을 SQL 조건으로 넘겨 city + country JOIN 조회 → 표로 출력

★ 핵심 : 사용자 입력값을 SQL 문자열에 직접 붙이지 않고 %s 자리표시자 + 튜플로 넘긴다.
         (SQL Injection 방지 — PyMySQL 이 값을 안전하게 감싸 준다)
"""

import pymysql
import streamlit as st

# ---------------------------------------------------------------------
# DB 접속 정보 — 본인 환경에 맞게 password 를 수정한다
# ---------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",            # ★ 본인 MySQL root 비밀번호로 변경
    "database": "world",           # 교재의 db= 와 같음 (최신 PyMySQL 권장 표기)
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def run_query(sql, params=None):
    """SQL 을 실행하고 결과를 list[dict] 로 반환하는 공용 함수."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)      # params 가 있으면 %s 자리에 안전하게 치환
            return cursor.fetchall()
    finally:
        conn.close()


# ---------------------------------------------------------------------
# 1. 사이드바 — 대륙 선택 (st.selectbox)
#    선택지도 DB 에서 가져온다 (DISTINCT 로 중복 없는 대륙 목록)
# ---------------------------------------------------------------------
continents = [row["Continent"] for row in
              run_query("SELECT DISTINCT Continent FROM country ORDER BY Continent")]

with st.sidebar:
    continent = st.selectbox("대륙 선택", continents,
                             index=continents.index("Asia"))   # 기본값 Asia


# ---------------------------------------------------------------------
# 2. 메인 화면 — 입력 폼 (st.form)
#    폼 안의 위젯은 [DB 검색 실행] 을 누르는 순간에만 값이 전송된다
# ---------------------------------------------------------------------
st.title("대륙 및 인구수 조건별 도시 검색")
st.divider()

with st.form(key="search_form"):
    min_pop = st.number_input("최소 인구수를 입력하세요",
                              min_value=0, value=9_500_000, step=100_000)
    submitted = st.form_submit_button("DB 검색 실행")


# ---------------------------------------------------------------------
# 3. 제출됐을 때만 DB 조회 → 결과 출력
# ---------------------------------------------------------------------
if submitted:
    sql = """
        SELECT C.Name       AS 도시명,
               CO.Name      AS 국가명,
               C.Population AS 인구수
        FROM city AS C
        INNER JOIN country AS CO ON C.CountryCode = CO.Code
        WHERE CO.Continent = %s          -- 선택한 대륙
          AND C.Population >= %s         -- 입력한 최소 인구수
        ORDER BY C.Population DESC
    """
    rows = run_query(sql, (continent, int(min_pop)))

    if rows:
        st.success(f"{continent} 대륙 / {int(min_pop):,}명 이상 도시 검색 완료!")
        st.table(rows)
    else:
        st.warning(f"{continent} 대륙에는 인구 {int(min_pop):,}명 이상인 도시가 없습니다.")
