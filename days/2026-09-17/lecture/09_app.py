"""
[09] PyMySQL + Streamlit 연동 웹 대시보드 생성 실습  (교재 p.136, 교재 파일명 app.py)

실행 : (db) 가상환경에서  streamlit run 09_app.py

흐름 : PyMySQL 로 world DB 조회 → list[dict] → Streamlit 표(st.table)로 출력
       Day 007 에서 배운 st.title / st.subheader / st.divider / st.table 을 그대로 쓴다
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


def load_korea_top10():
    """한국(KOR) 도시 인구 상위 10개를 list[dict] 로 반환한다."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # SQL 에서 AS 별칭을 한글로 주면 화면 표의 컬럼 제목이 그대로 한글이 된다
            sql = """
                SELECT Name       AS 도시명,
                       District   AS 도_지역,
                       Population AS 인구수
                FROM city
                WHERE CountryCode = 'KOR'
                ORDER BY Population DESC
                LIMIT 10
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()        # 화면이 재실행될 때마다 열리므로 반드시 닫는다


# ---------------------------------------------------------------------
# 화면 구성
# ---------------------------------------------------------------------
st.title("world DB 한국 주요 도시 현황")
st.subheader("한국 상위 10개 도시 목록")
st.divider()

rows = load_korea_top10()

# st.table() : list[dict] 를 넘기면 dict 의 키가 컬럼 제목, 값이 셀이 된다
st.table(rows)

st.caption(f"조회 건수 : {len(rows)}건 · 출처 : MySQL world 샘플 DB (city 테이블)")
