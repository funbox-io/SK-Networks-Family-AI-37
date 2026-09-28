"""데이터 불러오기 — MySQL(holiday_db)에서 읽고, 연결이 안 되면 data/ 폴더의 CSV로 대신합니다.

접속 정보: db_config.py 의 MYSQL (host · port · user · password · database)

DB는 db/holiday_db.sql 을 MySQL Workbench에서 실행해 만듭니다 (db/README.md).
두 경로 모두 analysis.prepare_* 를 거치므로 화면에 들어가는 표 모양은 똑같습니다.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd

import analysis
import faq as faq_mod

# 테이블 컬럼 → 화면 코드가 쓰는 한글 컬럼
ACC_SQL = ("SELECT year, holiday, acc_date, weekday, sido, sigungu, accidents, deaths, serious, injuries "
           "FROM accident_daily ORDER BY acc_date, holiday, sido, sigungu")
ACC_COLS = {"year": "연도", "holiday": "명절", "acc_date": "날짜", "weekday": "요일", "sido": "시도", "sigungu": "시군구",
            "accidents": "사고", "deaths": "사망", "serious": "중상", "injuries": "부상"}
HS_SQL = ("SELECT name, sido, sigungu, accidents, casualties, deaths, serious, minor, reported, lon, lat "
          "FROM hotspot ORDER BY id")
HS_COLS = {"name": "지점명", "sido": "시도", "sigungu": "시군구", "accidents": "사고", "casualties": "사상자", "deaths": "사망",
           "serious": "중상", "minor": "경상", "reported": "부상신고", "lon": "경도", "lat": "위도"}
GEO_SQL = "SELECT sido, geojson FROM sido_boundary ORDER BY sido"
FAQ_SQL = "SELECT category, question, answer, source FROM faq ORDER BY id"
FAQ_COLS = {"category": "항목", "question": "질문", "answer": "답변", "source": "출처"}
DAYS_SQL = "SELECT year, holiday, d_day FROM holiday_dates"


@dataclass
class Bundle:
    df: pd.DataFrame          # 사고통계 (analysis.prepare_accidents 적용)
    hotspots: pd.DataFrame    # 사고다발지 (analysis.prepare_hotspots 적용)
    geo: dict                 # 시도 경계 GeoJSON FeatureCollection
    faq: pd.DataFrame         # 보험 FAQ (항목 · 질문 · 답변 · 출처)
    source: str               # "mysql" 또는 "csv"
    note: str = ""            # CSV로 대신했을 때 이유


def _query(conn, sql: str) -> pd.DataFrame:
    """DB-API 커넥션(pymysql 등)으로 SELECT 결과를 DataFrame으로."""
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return pd.DataFrame(list(cur.fetchall()), columns=cols)
    finally:
        cur.close()


def connect_mysql(cfg: dict):
    import pymysql  # requirements.txt: pymysql

    return pymysql.connect(
        host=cfg.get("host", "localhost"), port=int(cfg.get("port", 3306)),
        user=cfg.get("user", "root"), password=cfg.get("password", ""),
        database=cfg.get("database", "holiday_db"), charset="utf8mb4", connect_timeout=5,
    )


def load_from_db(conn) -> Bundle:
    """열린 DB 커넥션에서 네 테이블을 읽어 화면용 표로 바꿉니다."""
    days = _query(conn, DAYS_SQL)
    if len(days):   # 명절 당일(D) 기준일도 DB 값을 씁니다
        analysis.HOLIDAY_D.update({(int(r.year), r.holiday): str(r.d_day)[:10] for r in days.itertuples()})
    df = analysis.prepare_accidents(_query(conn, ACC_SQL).rename(columns=ACC_COLS))
    hs = analysis.prepare_hotspots(_query(conn, HS_SQL).rename(columns=HS_COLS))
    g = _query(conn, GEO_SQL)
    geo = {"type": "FeatureCollection",
           "features": [json.loads(x) if isinstance(x, (str, bytes)) else x for x in g["geojson"]]}
    faq = _query(conn, FAQ_SQL).rename(columns=FAQ_COLS).fillna("")
    return Bundle(df=df, hotspots=hs, geo=geo, faq=faq[["항목", "질문", "답변", "출처"]], source="mysql")


def load_from_csv(note: str = "") -> Bundle:
    with open(analysis.GEO_PATH, encoding="utf-8") as f:
        geo = json.load(f)
    return Bundle(df=analysis.load_data(), hotspots=analysis.load_hotspots(), geo=geo,
                  faq=faq_mod.load_faq(), source="csv", note=note)


def load(cfg: dict | None) -> Bundle:
    """MySQL을 먼저 시도하고, 설정이 없거나 연결에 실패하면 CSV로 대신합니다."""
    if not cfg:
        return load_from_csv("db_config.py에 MySQL 접속 정보가 없어 CSV로 표시합니다.")
    try:
        conn = connect_mysql(cfg)
    except Exception as e:  # 드라이버 없음 · 접속 실패 등
        return load_from_csv(f"MySQL에 연결하지 못해 CSV로 표시합니다. db_config.py의 비밀번호와 MySQL 실행 여부를 확인하세요. ({type(e).__name__}: {e})")
    try:
        return load_from_db(conn)
    except Exception as e:  # 테이블 없음 등
        return load_from_csv(f"holiday_db를 읽지 못해 CSV로 표시합니다 ({type(e).__name__}: {e}). "
                             "db/holiday_db.sql을 먼저 실행했는지 확인하세요.")
    finally:
        conn.close()
