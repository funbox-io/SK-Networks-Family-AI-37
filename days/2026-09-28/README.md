---
day: 015
date: 2026-09-28
weekday: 월
week: 5
phase: 데이터 분석과 머신러닝/딥러닝
title: 명절 교통사고 데이터 대시보드 — Streamlit · MySQL · Plotly 미니 프로젝트
tags: python, streamlit, mysql, pymysql, pandas, plotly, geojson, dashboard, 데이터분석, 교통사고, 도로교통공단, 캐싱, 폴백
---

# Day 015 · 2026-09-28 (월)

`데이터 분석과 머신러닝/딥러닝` · 5주차

> **한 줄 요약** — 도로교통공단 연휴 사고통계(2021~2025)를 MySQL에 적재하고, Streamlit으로 「설날 vs 추석, 어떤 연휴가 더 위험할까?」를 보여 주는 대시보드를 만들었다.

📂 실습 자료 → [`lecture/SK37_MJH/`](./lecture/SK37_MJH/) (Streamlit 앱 전체) · [`lecture/demo/`](./lecture/demo/) (시연 영상 2편)

---

## 1. 무엇을 만들었나

**대한민국 명절 교통사고 데이터** — 설날과 추석 연휴의 사고를 나란히 놓고 비교하는 대시보드다.

- **전체 비교** — 5년(2021~2025) 합계로 설날 vs 추석, 연휴 일자별 추이, 핵심 인사이트 3개
- **연도 상세** — 연도를 골라 설날/추석 비교와 치사율, 시군구 TOP 10
- **사고다발지점** — 시도·시군구를 골라 지도와 Top 6, 전체 목록(81곳)
- **보험 FAQ** — 보험 관련 질문 348개를 항목별로 찾아보는 화면

연휴 길이가 3~5일로 달라서 총합만 비교하면 긴 연휴가 불리하다. 그래서 **일평균 보정** 스위치를 두고 켜고 끌 수 있게 했다.

---

## 2. 폴더 구성

| 파일 | 하는 일 |
|------|---------|
| `app.py` | 페이지 뼈대 — 사이트 제목 · 사이드바(메뉴/지표/일평균 보정) · 세 개 탭 |
| `data_source.py` | 데이터 불러오기 — **MySQL 우선, 실패하면 CSV** |
| `db_config.py` | MySQL 접속 정보 (host · port · user · password · database) |
| `analysis.py` | 계산 — 명절 당일(D) 기준 일자, 히트맵, 피해 구성, 사고다발지 연도 연결 |
| `sections.py` | 화면 카드들 |
| `theme.py` | 색 · 글꼴 · CSS · 머리글 — **디자인은 이 파일만 고치면 된다** |
| `faq.py` | 보험 FAQ 화면 |
| `db/` | `holiday_db.sql` (스키마 + 데이터), 생성 스크립트, Workbench 안내 |
| `data/` | 연휴 사고통계 2021~2025, 사고다발지 81곳, 시도 경계(geojson), 보험 FAQ |

역할별로 파일을 나눠 두면 **고칠 곳이 한 군데로 모인다.** 색을 바꾸고 싶으면 `theme.py`, 계산식을 바꾸고 싶으면 `analysis.py` 만 열면 된다.

---

## 3. 실행

```bash
pip install -r requirements.txt
streamlit run app.py      # 반드시 이 폴더 안에서 실행 (.streamlit/config.toml 테마 적용)
```

MySQL에서 읽으려면

1. `db/README.md` 순서대로 MySQL Workbench에서 `db/holiday_db.sql` 을 실행해 `holiday_db` 를 만든다
2. `db_config.py` 의 `password` 를 내 MySQL root 비밀번호로 바꾼다
3. `streamlit run app.py` — 사이드바 아래에 **데이터: MySQL holiday_db** 가 보이면 DB에서 읽은 것

| 테이블 | 행 수 |
|--------|------|
| `accident_daily` | 8,901 |
| `holiday_dates` | 10 |
| `hotspot` | 81 |
| `sido_boundary` | 17 |
| `faq` | 348 |

---

## 4. 배운 점

**MySQL → 실패하면 CSV (폴백)**
DB 접속 정보가 없거나 연결에 실패해도 앱이 죽지 않는다. `data/` 폴더의 CSV로 대신 표시하고, 사이드바에 노란 경고로 이유를 알려 준다. 어디서 읽었는지는 `data.source` 로 화면에 표시한다.

**캐싱**
`@st.cache_data(ttl=600)` — 같은 조건이면 10분 동안 다시 읽지 않는다. 데이터를 바꿨다면 오른쪽 위 메뉴 → **Clear cache**.

**`st.session_state` 로 메뉴 상태 기억하기**
사이드바 버튼을 누르면 `st.session_state["page"]` 가 바뀌고, 그 값에 따라 대시보드/FAQ 화면을 고른다. Streamlit은 버튼을 누를 때마다 스크립트를 **처음부터 다시 실행**하기 때문에, 기억해야 하는 값은 `session_state` 에 둬야 한다.

**공개 저장소에 올릴 때**
`db_config.py` 에 비밀번호가 **평문으로** 적힌다. 저장소에 올린 버전은 `password` 를 **비워 두었다.** 내려받아 쓸 때 본인 비밀번호를 적으면 된다.

---

## 5. 시연 영상

| 파일 | 내용 |
|------|------|
| [`lecture/demo/intro.mp4`](./lecture/demo/intro.mp4) | 소개 영상 (약 1분 · 1280×720) |
| [`lecture/demo/screen.mp4`](./lecture/demo/screen.mp4) | 화면 녹화 (약 11초 · 1910×862) |

---

## 🔁 복습

**직접 해본 것**
- CSV 5개(연휴 사고통계 · 사고다발지 · 시도 경계 · 보험 FAQ)를 MySQL 테이블로 적재하고 `holiday_db.sql` 로 내보내기
- `pymysql` 로 읽어 온 결과를 `pandas` DataFrame 으로 변환, 실패 시 CSV 로 떨어지는 폴백 경로 구현
- `plotly` 로 막대·선 그래프와 `geojson` 기반 지도 그리기
- `theme.py` 에 색·글꼴·CSS 를 몰아 두고 화면 코드와 분리
- 연휴 길이가 달라 생기는 왜곡을 **일평균 보정** 스위치로 해결
- 공개 전 `db_config.py` 의 비밀번호 제거

**막혔던 부분 / 질문**
- [ ] `@st.cache_data` 의 인자가 dict 일 때 해시가 어떻게 계산되는지 (접속 정보를 바꾸면 캐시가 새로 도는지)
- [ ] Streamlit이 매번 스크립트를 처음부터 다시 실행한다는 것 — 무거운 계산은 어디까지 캐시해야 하는지
- [ ] 치사율(사망 ÷ 사고 × 100)을 연휴 길이로 보정해야 할까, 아니면 비율이라 그대로 둬도 될까
- [ ] 사고다발지는 2021~2025 합산이라 연도별 비교가 안 되는데, 연도별로 쪼갤 방법이 있는지
- [ ] `db_config.py` 대신 환경변수나 `.streamlit/secrets.toml` 을 쓰는 방식과의 차이

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [Streamlit 공식 문서 — 캐싱 (`st.cache_data`)](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [Streamlit 공식 문서 — Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [PyMySQL 문서](https://pymysql.readthedocs.io/en/latest/)
- [Plotly for Python — Choropleth 지도](https://plotly.com/python/choropleth-maps/)
- [도로교통공단 교통사고분석시스템(TAAS)](https://taas.koroad.or.kr/)
