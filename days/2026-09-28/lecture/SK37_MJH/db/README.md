# MySQL 데이터베이스 만들기 (MySQL Workbench)

## 1. 실행
1. MySQL Workbench에서 로컬 MySQL 연결(예: `Local instance MySQL80`)을 엽니다.
2. **File → Open SQL Script…** 로 `db/holiday_db.sql`을 엽니다.
3. 번개 모양 **⚡ Execute** 버튼(전체 실행)을 누릅니다. 1분 안에 끝납니다.
4. 왼쪽 **Schemas** 패널에서 새로고침(↻)하면 `holiday_db`가 보입니다.

마지막 확인 쿼리 결과가 아래와 같으면 정상입니다.

| tbl | n |
|---|---|
| accident_daily | 8901 |
| holiday_dates | 10 |
| hotspot | 81 |
| sido_boundary | 17 |
| faq | 348 |

- MySQL 5.7 이상이 필요합니다(JSON 형식). 8.0을 권장합니다.
- 여러 번 실행해도 됩니다. 테이블을 지우고 새로 만듭니다.
- `LOAD DATA LOCAL INFILE`을 쓰지 않고 데이터를 SQL 안에 넣었기 때문에, Workbench의 로컬 파일 권한 설정은 필요 없습니다.

## 2. 테이블

| 테이블 | 내용 | 원본 |
|---|---|---|
| accident_daily | 연휴 날짜 × 지역별 사고·사망·중상·부상. `level`: 전국 / 시도(소계) / 시군구 | data/holiday_accidents_2021_2025.csv |
| holiday_dates | 연도·명절별 명절 당일(D) | analysis.py의 HOLIDAY_D |
| hotspot | 사고다발지 81곳 (2021~2025 합산, 좌표 포함). `sigungu_base`는 사고통계와 맞춘 시군구 이름 | data/hotspots_2021_2025.csv |
| sido_boundary | 시도 경계 GeoJSON (JSON 컬럼) | data/sido.geojson |
| faq | 보험 FAQ (항목 · 질문 · 답변 · 출처) | data/faq/insurance_faq.csv |

뷰: `v_holiday_totals`(연도·명절별 전국 합계·일평균·치사율), `v_sido_totals`(시도별 합계), `v_daily_d`(전국 일자별 + D 기준 일자)

주의: `injuries`(부상자)에는 `serious`(중상자)가 포함되어 있어 두 값을 더하면 안 됩니다.
전국 합계는 `level='전국'`, 시도 합계는 `level='시도'` 행으로 구하세요. 섞어서 더하면 두 번 셉니다.

## 3. 앱에서 읽기
프로젝트 폴더의 `db_config.py`에서 `password`를 내 비밀번호로 바꾼 뒤 `streamlit run app.py`.
앱은 `data_source.py`에서 pymysql로 accident_daily · holiday_dates · hotspot · sido_boundary · faq 다섯 테이블을 읽습니다.

## 4. 다시 만들기
data 폴더의 CSV가 바뀌면 프로젝트 폴더에서 아래를 실행해 SQL을 새로 뽑습니다.
```bash
python db/build_mysql.py
```
