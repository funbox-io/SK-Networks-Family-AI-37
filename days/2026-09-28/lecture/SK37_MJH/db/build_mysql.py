"""data 폴더 → MySQL용 SQL 스크립트(holiday_db.sql) 만들기

사용법 (프로젝트 폴더에서):
    python db/build_mysql.py              → db/holiday_db.sql 생성
그다음 MySQL Workbench에서 File > Open SQL Script… 로 holiday_db.sql 을 열고 번개(⚡) 버튼으로 실행하면
holiday_db 데이터베이스 · 테이블 · 데이터 · 뷰가 한 번에 만들어집니다.

만들어지는 테이블
    accident_daily   연휴 날짜 × 지역별 사고통계 (전국 / 시도 소계 / 시군구)   8,901행
    holiday_dates    연도 · 명절별 명절 당일(D)                               10행
    hotspot          연휴기간 사고다발지역 (2021~2025 합산, 좌표 포함)          81행
    sido_boundary    시도 경계 GeoJSON (지도용)                              17행
    faq              보험 FAQ (항목 · 질문 · 답변 · 출처)                      348행
뷰
    v_holiday_totals  연도 · 명절별 전국 합계 · 일평균 · 치사율
    v_sido_totals     연도 · 명절 · 시도별 합계
    v_daily_d         전국 일자별 수치 + 명절 당일 기준 D(−1, 0, +1 …)
"""
from __future__ import annotations

import json
import re
import html
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent / "holiday_db.sql"
DB = "holiday_db"
BATCH = 500

HOLIDAY_D = {
    (2021, "설날"): "2021-02-12", (2021, "추석"): "2021-09-21",
    (2022, "설날"): "2022-02-01", (2022, "추석"): "2022-09-10",
    (2023, "설날"): "2023-01-22", (2023, "추석"): "2023-09-29",
    (2024, "설날"): "2024-02-10", (2024, "추석"): "2024-09-17",
    (2025, "설날"): "2025-01-29", (2025, "추석"): "2025-10-06",
}


def q(v) -> str:
    """SQL 값 표기. 문자열은 작은따옴표를 두 번 써서 이스케이프 (역슬래시는 데이터에 없음을 확인)."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "NULL"
    if isinstance(v, (int,)) or (hasattr(v, "dtype") and str(getattr(v, "dtype", "")).startswith("int")):
        return str(int(v))
    if isinstance(v, float):
        return repr(v)
    s = str(v)
    if "\\" in s:
        s = s.replace("\\", "\\\\")
    return "'" + s.replace("'", "''") + "'"


def inserts(table: str, cols: list[str], rows: list[tuple]) -> str:
    out = []
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        vals = ",\n".join("(" + ", ".join(q(v) for v in r) + ")" for r in chunk)
        out.append(f"INSERT INTO `{table}` ({', '.join(f'`{c}`' for c in cols)}) VALUES\n{vals};")
    return "\n\n".join(out)


def level_of(sido: str, sgg: str) -> str:
    if sido == "전국":
        return "전국"
    return "시도" if sgg == "소계" else "시군구"


def build() -> str:
    acc = pd.read_csv(DATA / "holiday_accidents_2021_2025.csv", encoding="utf-8-sig")
    hs = pd.read_csv(DATA / "hotspots_2021_2025.csv", encoding="utf-8-sig")
    geo = json.load(open(DATA / "sido.geojson", encoding="utf-8"))
    faq = pd.read_csv(DATA / "faq" / "insurance_faq.csv", encoding="utf-8-sig")

    # ---- FAQ: 답변 끝의 '(출처 : …)'를 source 컬럼으로 분리 (화면의 faq.py와 같은 규칙)
    src_re = r"\s*\(출처\s*:\s*([^)]+)\)\s*\"?\s*$"
    faq["source"] = faq["답변"].str.extract(src_re)[0].fillna("").str.strip()
    faq["answer"] = (faq["답변"].str.replace(src_re, "", regex=True).str.strip().str.strip('"').str.strip()
                     .map(lambda s: html.unescape(s.replace("& #", "&#"))))

    acc_rows = [
        (int(r.연도), r.명절, r.날짜, r.요일, level_of(r.시도, r.시군구), r.시도, r.시군구,
         int(r.사고), int(r.사망), int(r.중상), int(r.부상))
        for r in acc.itertuples(index=False)
    ]
    hs_rows = [
        (r.지점명, r.시도, r.시군구, re.sub(r"^(.+?시).+구$", r"\1", r.시군구),
         int(r.사고), int(r.사상자), int(r.사망), int(r.중상), int(r.경상), int(r.부상신고), float(r.경도), float(r.위도))
        for r in hs.itertuples(index=False)
    ]
    geo_rows = [(f["properties"]["n"], json.dumps(f, ensure_ascii=False, separators=(",", ":"))) for f in geo["features"]]
    faq_rows = [(r.항목.strip(), r.질문.strip(), r.answer, r.source) for r in faq.itertuples(index=False)]
    d_rows = [(y, h, d) for (y, h), d in sorted(HOLIDAY_D.items())]

    parts = [f"""-- =====================================================================
-- 설날 vs 추석 명절 교통사고 대시보드 · MySQL 데이터베이스
-- 생성: db/build_mysql.py  (data 폴더가 바뀌면 다시 생성하세요)
-- 실행: MySQL Workbench > File > Open SQL Script… > ⚡(Execute) · MySQL 5.7 이상 (JSON 형식 사용)
-- 다시 실행해도 됩니다: 테이블을 지우고 새로 만듭니다.
-- =====================================================================
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS `{DB}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `{DB}`;

DROP VIEW IF EXISTS v_daily_d;
DROP VIEW IF EXISTS v_sido_totals;
DROP VIEW IF EXISTS v_holiday_totals;
DROP TABLE IF EXISTS accident_daily;
DROP TABLE IF EXISTS holiday_dates;
DROP TABLE IF EXISTS hotspot;
DROP TABLE IF EXISTS sido_boundary;
DROP TABLE IF EXISTS faq;

-- ---------------------------------------------------------------------
-- 1) 연휴 날짜 × 지역별 사고통계  (원본: data/holiday_accidents_2021_2025.csv)
--    level: 전국(합계 행) / 시도(시도 소계 행) / 시군구
--    ※ 부상자(injuries)에는 중상자(serious)가 포함됩니다. 두 값을 더하지 마세요.
-- ---------------------------------------------------------------------
CREATE TABLE accident_daily (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  year         SMALLINT     NOT NULL COMMENT '연도',
  holiday      ENUM('설날','추석') NOT NULL COMMENT '명절',
  acc_date     DATE         NOT NULL COMMENT '날짜',
  weekday      CHAR(1)      NOT NULL COMMENT '요일',
  level        ENUM('전국','시도','시군구') NOT NULL COMMENT '집계 단위',
  sido         VARCHAR(10)  NOT NULL COMMENT '시도 (전국 합계 행은 전국)',
  sigungu      VARCHAR(20)  NOT NULL COMMENT '시군구 (시도 합계 행은 소계)',
  accidents    INT          NOT NULL DEFAULT 0 COMMENT '사고 건수',
  deaths       INT          NOT NULL DEFAULT 0 COMMENT '사망자',
  serious      INT          NOT NULL DEFAULT 0 COMMENT '중상자',
  injuries     INT          NOT NULL DEFAULT 0 COMMENT '부상자 (중상 포함)',
  PRIMARY KEY (id),
  UNIQUE KEY uq_day_region (acc_date, holiday, sido, sigungu),
  KEY ix_year_holiday (year, holiday, level),
  KEY ix_region (sido, sigungu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='설날·추석 연휴기간 사고통계 2021~2025 (도로교통공단)';

-- ---------------------------------------------------------------------
-- 2) 명절 당일(D) — 연휴 일자를 D-1 / D / D+1 로 셀 때 기준
-- ---------------------------------------------------------------------
CREATE TABLE holiday_dates (
  year     SMALLINT NOT NULL COMMENT '연도',
  holiday  ENUM('설날','추석') NOT NULL COMMENT '명절',
  d_day    DATE NOT NULL COMMENT '명절 당일 (음력 1/1, 8/15)',
  PRIMARY KEY (year, holiday)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 3) 연휴기간 사고다발지역  (원본: data/hotspots_2021_2025.csv · 2021~2025 합산, 연도 구분 없음)
--    sigungu_base: '용인시처인구' → '용인시' 처럼 사고통계의 시군구와 맞춘 이름
-- ---------------------------------------------------------------------
CREATE TABLE hotspot (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name          VARCHAR(100) NOT NULL COMMENT '지점명',
  sido          VARCHAR(10)  NOT NULL COMMENT '시도',
  sigungu       VARCHAR(20)  NOT NULL COMMENT '시군구 (원본)',
  sigungu_base  VARCHAR(20)  NOT NULL COMMENT '시군구 (사고통계와 맞춘 이름)',
  accidents     INT NOT NULL COMMENT '사고 건수',
  casualties    INT NOT NULL COMMENT '사상자',
  deaths        INT NOT NULL COMMENT '사망',
  serious       INT NOT NULL COMMENT '중상',
  minor         INT NOT NULL COMMENT '경상',
  reported      INT NOT NULL COMMENT '부상신고',
  lon           DECIMAL(9,5) NOT NULL COMMENT '경도',
  lat           DECIMAL(8,5) NOT NULL COMMENT '위도',
  PRIMARY KEY (id),
  KEY ix_region (sido, sigungu_base)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='연휴기간 사고다발지역 2021~2025 (도로교통공단)';

-- ---------------------------------------------------------------------
-- 4) 시도 경계 (지도용 GeoJSON Feature)
-- ---------------------------------------------------------------------
CREATE TABLE sido_boundary (
  sido     VARCHAR(10) NOT NULL COMMENT '시도',
  geojson  JSON        NOT NULL COMMENT 'GeoJSON Feature',
  PRIMARY KEY (sido)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 5) 보험 FAQ  (원본: data/faq/insurance_faq.csv · 답변 끝 '(출처 : …)'는 source로 분리)
-- ---------------------------------------------------------------------
CREATE TABLE faq (
  id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
  category  VARCHAR(30)  NOT NULL COMMENT '항목',
  question  VARCHAR(255) NOT NULL COMMENT '질문',
  answer    TEXT         NOT NULL COMMENT '답변',
  source    VARCHAR(30)  NOT NULL DEFAULT '' COMMENT '출처 (보험사)',
  PRIMARY KEY (id),
  KEY ix_category (category),
  KEY ix_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='보험 FAQ';
"""]
    parts.append("-- ===== 데이터 =====")
    parts.append(inserts("accident_daily",
                         ["year", "holiday", "acc_date", "weekday", "level", "sido", "sigungu",
                          "accidents", "deaths", "serious", "injuries"], acc_rows))
    parts.append(inserts("holiday_dates", ["year", "holiday", "d_day"], d_rows))
    parts.append(inserts("hotspot", ["name", "sido", "sigungu", "sigungu_base", "accidents", "casualties",
                                     "deaths", "serious", "minor", "reported", "lon", "lat"], hs_rows))
    parts.append(inserts("sido_boundary", ["sido", "geojson"], geo_rows))
    parts.append(inserts("faq", ["category", "question", "answer", "source"], faq_rows))

    parts.append("""-- ===== 뷰 =====
-- 연도 · 명절별 전국 합계 · 일평균 · 치사율(사고 100건당 사망자)
CREATE VIEW v_holiday_totals AS
SELECT year, holiday,
       COUNT(*)                                   AS days,
       SUM(accidents)                             AS accidents,
       SUM(deaths)                                AS deaths,
       SUM(serious)                               AS serious,
       SUM(injuries)                              AS injuries,
       ROUND(SUM(accidents) / COUNT(*), 1)        AS accidents_per_day,
       ROUND(SUM(deaths) / SUM(accidents) * 100, 2) AS fatality_rate
FROM accident_daily
WHERE level = '전국'
GROUP BY year, holiday;

-- 연도 · 명절 · 시도별 합계 (시도 소계 행 기준)
CREATE VIEW v_sido_totals AS
SELECT year, holiday, sido,
       COUNT(*) AS days, SUM(accidents) AS accidents, SUM(deaths) AS deaths,
       SUM(serious) AS serious, SUM(injuries) AS injuries
FROM accident_daily
WHERE level = '시도'
GROUP BY year, holiday, sido;

-- 전국 일자별 + 명절 당일 기준 D (0 = 당일, -1 = 전날, +1 = 다음날)
CREATE VIEW v_daily_d AS
SELECT a.year, a.holiday, a.acc_date, a.weekday,
       DATEDIFF(a.acc_date, h.d_day) AS d_offset,
       a.accidents, a.deaths, a.serious, a.injuries
FROM accident_daily a
JOIN holiday_dates h ON h.year = a.year AND h.holiday = a.holiday
WHERE a.level = '전국';

-- ===== 확인용 (실행 결과가 아래 숫자와 같으면 정상) =====
SELECT 'accident_daily' AS tbl, COUNT(*) AS n FROM accident_daily   -- 8901
UNION ALL SELECT 'holiday_dates', COUNT(*) FROM holiday_dates        -- 10
UNION ALL SELECT 'hotspot', COUNT(*) FROM hotspot                    -- 81
UNION ALL SELECT 'sido_boundary', COUNT(*) FROM sido_boundary        -- 17
UNION ALL SELECT 'faq', COUNT(*) FROM faq;                           -- 348

-- ===== 예시 쿼리 =====
-- 5년 전체: 설날 vs 추석 일평균 사고 (설날 314.2 / 추석 400.4)
-- SELECT holiday, ROUND(SUM(accidents)/SUM(days),1) AS per_day FROM v_holiday_totals GROUP BY holiday;
-- 2023년 시도별 추석 − 설날 차이
-- SELECT sido, SUM(CASE WHEN holiday='추석' THEN accidents ELSE -accidents END) AS diff
--   FROM v_sido_totals WHERE year=2023 GROUP BY sido ORDER BY diff DESC;
-- 사고다발지 Top 6 (사상자 순)
-- SELECT name, accidents, casualties FROM hotspot ORDER BY casualties DESC, accidents DESC LIMIT 6;
-- FAQ 항목별 개수
-- SELECT category, COUNT(*) FROM faq GROUP BY category ORDER BY 2 DESC;
""")
    return "\n\n".join(parts) + "\n"


if __name__ == "__main__":
    sql = build()
    OUT.write_text(sql, encoding="utf-8")
    print(f"생성 완료: {OUT}  ({OUT.stat().st_size / 1024:,.0f} KB)")
