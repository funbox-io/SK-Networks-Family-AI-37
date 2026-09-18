---
day: 010
date: 2026-09-17
weekday: 목
week: 3
phase: 프로그래밍과 데이터 기초
title: JOIN 마무리 · 인덱스 · 뷰 · 백업, 그리고 Python–MySQL 연동
tags: sql, mysql, world, CROSS JOIN, SELF JOIN, 카테시안 곱, GROUP BY, HAVING, 인덱스, index, Full Table Scan, Index Scan, EXPLAIN, 뷰, view, CREATE VIEW, DROP VIEW, 접근 통제, 백업, 복원, Data Export, Data Import, mysqldump, ERROR 1046, conda, 가상환경, PyMySQL, DictCursor, fetchall, streamlit, st.table, st.selectbox, st.form, SQL Injection
---

# Day 010 · 2026-09-17 (목)

`프로그래밍과 데이터 기초` · 3주차

> **한 줄 요약** — `CROSS` · `SELF JOIN` 으로 조인을 마무리하고, 인덱스 · 뷰 · 백업으로 "DB를 관리하는 쪽"의 도구를 훑은 뒤, PyMySQL 로 파이썬에서 `world` DB를 읽어 Streamlit 대시보드에 띄우는 것까지 연결했다. SQL 단원 끝.

📂 실습 코드 → [`lecture/`](./lecture/) (교재 p.107 ~ p.139, `.sql` 7개 + `.py` 3개 + 환경 설정 메모)

---

## 0. 오늘의 위치

지난 3일이 **"SQL 문법"** 이었다면 오늘은 그 문법을 **실제로 쓰는 자리**로 옮겨 가는 날이었다.

```text
Day 008  DDL · CRUD · SELECT 기본
Day 009  집계 · 내장 함수 · JOIN                     ← 조회 문법
Day 010  JOIN 마무리 → 인덱스 · 뷰 · 백업 → Python 연동   ← 관리 + 활용
```

---

## 1. CROSS JOIN · SELF JOIN — `01_CROSS_JOIN_SELF_JOIN.sql`

어제 남겨 둔 두 가지 조인. (어제 질문 해결)

| 조인 | 개념 | 결과 행 수 |
|------|------|-----------|
| `CROSS JOIN` | **`ON` 없이** A의 모든 행 × B의 모든 행 (카테시안 곱) | A × B |
| `SELF JOIN` | **같은 테이블**을 두 번 참조 — 사원-상사, 카테고리-상위카테고리 | 조건에 따라 |

```sql
-- city(4079) × country(239) = 974,881 행. COUNT 로만 확인할 것
SELECT COUNT(*) FROM city AS C CROSS JOIN country AS CO;

-- 조직도 : 사원 → 직속 상사 → 상사의 상사를 한 줄로
SELECT A.emp_name AS 사원, A.mgr_name AS 직속상사, B.mgr_name AS 상사의상사
FROM emp_tree A
INNER JOIN emp_tree B ON A.mgr_name = B.emp_name;   -- 김사원 | 박대리 | 최부장
```

⚠️ SELF JOIN 은 한 테이블을 두 번 읽으므로 **서로 다른 별칭(`A`, `B`)이 필수**다. 같은 이름으로는 어느 쪽 컬럼인지 구분이 안 된다.
💡 `INNER` 를 `LEFT` 로 바꾸면 상사의 상사가 없는 박대리도 `NULL` 로 남는다.
💡 CROSS JOIN 은 실무에서 **더미 데이터 생성 · 성능 테스트**에 쓴다. 국가 3개 × 연도 3개 = 9행 같은 조합표를 만들 때 유용하다.

---

## 2. 종합 실습 — `02_종합실습_SQL기본_조인다지기.sql`

*"대륙별 도시 인구 합계를 구하고, 1억 이상인 대륙만, 합계 내림차순으로."*

대륙은 `country` 에, 도시 인구는 `city` 에 있다 → **JOIN → GROUP BY → HAVING → ORDER BY** 를 한 문장으로 잇는 문제였다.

```sql
SELECT CO.Continent AS 대륙, SUM(C.Population) AS 총도시인구합계
FROM country CO
INNER JOIN city C ON CO.Code = C.CountryCode
GROUP BY CO.Continent
HAVING 총도시인구합계 >= 100000000
ORDER BY 총도시인구합계 DESC;
-- Asia 697,604,103 / Europe 241,942,813 / South America 172,037,859 / North America 168,250,381 / Africa 135,838,579
```

Oceania(약 1,390만)는 `HAVING` 에서 걸러지고, 도시가 없는 Antarctica 는 `INNER JOIN` 단계에서 이미 빠진다.

---

## 3. 인덱스(Index) — `03_인덱스_개념_실습.sql`

데이터를 특정 기준으로 **정렬한 뒤 범위별로 묶어 둔 Tree 구조**. 인덱스가 있는 컬럼은 몇 번의 대소 비교만으로 원하는 행을 찾는다.

| | Full Table Scan | Index Scan |
|---|---|---|
| 언제 | 인덱스 **없음** | 인덱스 **있음** |
| 방법 | 첫 행부터 마지막 행까지 전부 읽어 비교 | Tree 를 타고 내려가 해당 행만 추출 |
| 속도 | 데이터가 많을수록 극도로 느려짐 | 검색 속도 극대화 |

교재는 개념까지였는데, `EXPLAIN` 으로 직접 확인해 보니 차이가 눈에 보였다.

```sql
EXPLAIN SELECT * FROM city WHERE Name = 'Seoul';   -- type = ALL,  rows ≈ 4079 (풀 스캔)
CREATE INDEX idx_city_name ON city (Name);
EXPLAIN SELECT * FROM city WHERE Name = 'Seoul';   -- type = ref,  rows = 1    (인덱스 스캔)
```

- `PRIMARY KEY` 를 만들면 인덱스가 **자동으로** 생긴다 (`SHOW INDEX FROM city`).
- `LIKE 'Seo%'` 는 인덱스를 타지만 **`LIKE '%eoul'` 은 다시 풀 스캔**이다. 정렬된 값의 앞부분으로 찾아 내려가는 구조라 시작 글자를 모르면 소용이 없다. (Day 008 질문 해결)
- 인덱스는 공짜가 아니다 — `INSERT` / `UPDATE` / `DELETE` 때마다 함께 갱신되므로 **쓰기 성능과 용량이 비용**이다. `WHERE` · `JOIN` · `ORDER BY` 에 자주 쓰는 컬럼에만 건다.

---

## 4. 뷰(View) — `04_VIEW_개념_보안용뷰_실습.sql`

**SELECT 쿼리 텍스트만 저장해 두는 가상 테이블.** 데이터는 들고 있지 않다.

```text
1) 생성   CREATE VIEW 뷰이름 AS SELECT …   → DBMS 는 SELECT 구문 "자체"만 저장
2) 호출   SELECT * FROM 뷰이름;             → 저장된 SELECT 를 꺼내 원본 테이블을 대신 조회 → 최신 결과 반환
```

| 특징 | 뜻 |
|------|-----|
| 디스크 공간 절약 | 조회 결과가 아니라 **쿼리 정의**만 보관 |
| 실시간 동기화 | 원본이 바뀌면 뷰 조회 결과에도 **즉시 반영** |

**활용 목적 ① 보안(접근 통제)** — 주민번호 · 급여 같은 민감 컬럼을 뺀 뷰를 만들고, 사용자 계정에는 **뷰에 대해서만** `SELECT` 권한을 준다.

```sql
CREATE VIEW v_user_security AS
SELECT user_id, user_name FROM real_user;          -- user_ssn, salary 제외

SELECT * FROM v_user_security;                     -- 안전한 컬럼만 보인다
DROP VIEW v_user_security;                         -- 뷰를 지워도 real_user 데이터는 그대로
```

| 단계 | 할 일 |
|------|-------|
| 1 | 원본 테이블(`real_user`)의 `SELECT` 권한을 사용자 계정에서 **차단** |
| 2 | 민감 컬럼을 제외한 **정제된 뷰** 생성 |
| 3 | 사용자 계정에 **그 뷰에만** `SELECT` 권한 부여 |

이렇게 하면 개발자의 실수든 악의적 쿼리든 원본 접근 권한 자체가 없어(**Access Denied**) 유출이 구조적으로 막히고, 일반 사용자는 평소 SQL 그대로 허용된 데이터에 접근할 수 있다.

---

## 5. 뷰로 JOIN 쿼리 재사용 — `05_VIEW_조인쿼리_재사용_실습.sql`

**활용 목적 ② 코드 재사용성** — 다중 테이블 JOIN · WHERE · GROUP BY 가 섞인 긴 쿼리를 뷰로 한 번 등록해 두고 어디서든 한 줄로 부른다.

```sql
CREATE VIEW v_asia_city_info AS
SELECT C.Name AS city_name, CO.Name AS country_name, C.Population AS city_population
FROM city AS C
INNER JOIN country AS CO ON C.CountryCode = CO.Code
WHERE CO.Continent = 'Asia';

-- 긴 JOIN 문 대신 한 줄
SELECT * FROM v_asia_city_info WHERE city_population >= 5000000 ORDER BY city_population DESC;
-- Mumbai 10,500,000 / Seoul 9,981,619 / Shanghai 9,696,300 / Jakarta 9,604,900 / Karachi 9,269,265 …
```

`SHOW CREATE VIEW v_asia_city_info;` 로 저장된 것이 데이터가 아니라 **쿼리 텍스트**임을 눈으로 확인했다. 이름 앞에 `v_` 를 붙이면 `SHOW TABLES` 에서 테이블과 뷰가 바로 구분된다.

---

## 6. 백업과 복원 — `06_백업복원_ERROR1046_해결.sql`

시스템 장애 · 악성코드 · 개발자 실수로 데이터가 사라졌을 때 되돌리기 위한 필수 작업.

| 종류 | 방식 |
|------|------|
| **논리적 백업** (SQL Dump) | 구조(DDL) + 데이터(DML)를 `.sql` 텍스트 파일로 저장 ← 실습 방식 |
| 물리적 백업 | DB가 실제 저장되는 디스크 파일(Data File, Log File) 자체를 복사 |

Workbench 상단 메뉴 **Server → Data Export**(백업) / **Data Import**(복원). Export 는 *Export to Self-Contained File* 로 경로를 정해 `testdb_dump.sql` 하나로 뽑고, Import 는 그 파일을 *Import from Self-Contained File* 로 지정한다.

⚠️ **ERROR 1046 (3D000) No database selected** — 복원할 때 자주 만나는 에러. 덤프 파일 안에 `CREATE DATABASE` / `USE` 가 없어서 MySQL 이 *"이 테이블을 어느 DB에 넣지?"* 를 모르는 상태다.

| 해결 | 방법 |
|------|------|
| ① GUI (추천) | Data Import 화면의 **Default Target Schema** 드롭다운에서 대상 DB 선택 (없으면 New… 로 생성) |
| ② 파일 수정 | 덤프 파일 첫 줄에 `CREATE DATABASE IF NOT EXISTS testdb; USE testdb;` 추가 |

💡 터미널에서는 `mysqldump -u root -p --databases testdb > testdb_dump.sql` — `--databases` 를 붙이면 덤프에 `CREATE DATABASE` / `USE` 가 자동으로 들어가 이 에러가 아예 생기지 않는다.

---

## 7. 실습 환경 — `07_실습환경설정_conda_PyMySQL.md`

```bash
conda create -n db python=3.12      # 가상환경 생성
conda activate db                   # (base) → (db)
pip install PyMySQL streamlit       # 반드시 (db) 가 붙은 뒤에
```

이후 miniconda3 폴더에 `work1` 을 만들어 VS Code 로 열고, `Ctrl+Shift+P` → *Python: Select Interpreter* → `db`.

| 라이브러리 | 역할 |
|------------|------|
| **PyMySQL** | 파이썬 ↔ MySQL 사이의 **통신** |
| **Streamlit** | 조회 결과를 **웹 대시보드**로 (Day 007) |

---

## 8. PyMySQL 로 DB 접속 — `08_pymysql_study.py`

파이썬에서 DB를 읽는 절차는 **4단계**로 고정이다.

| 단계 | 코드 | 뜻 |
|------|------|-----|
| 1 | `conn = pymysql.connect(host, user, password, database, charset, cursorclass)` | 파이썬과 MySQL 을 잇는 **전용 통로** |
| 2 | `cursor = conn.cursor()` | 명령을 내리고 결과를 받아오는 **조작 도구** |
| 3 | `cursor.execute(sql)` | SQL 실행 |
| 4 | `rows = cursor.fetchall()` | 결과 전체를 **한 번에** 파이썬으로 |

```python
DB_CONFIG = {
    "host": "localhost", "user": "root", "password": "1234",
    "database": "world", "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,     # 결과를 list[dict] 로
}
conn = pymysql.connect(**DB_CONFIG)
try:
    cursor = conn.cursor()
    cursor.execute("SELECT Name, District, Population FROM city WHERE CountryCode='KOR' ORDER BY Population DESC LIMIT 5")
    rows = cursor.fetchall()     # [{'Name': 'Seoul', 'District': 'Seoul', 'Population': 9981619}, …]
    for row in rows:
        print(f"- 도시명: {row['Name']} | 지역: {row['District']} | 인구수: {row['Population']:,}명")
finally:
    conn.close()
```

- `cursorclass=DictCursor` 가 핵심이다. 이걸 빼면 결과가 **튜플**로 와서 `row[0]` 처럼 번호로 꺼내야 한다. `DictCursor` 면 `row['Name']` 처럼 **컬럼명**으로 꺼낸다.
- `finally: conn.close()` — 에러가 나도 연결은 반드시 닫는다. (Day 005 예외 처리)
- 교재는 `db=` 로 적지만 최신 PyMySQL 은 `database=` 를 권장한다. `db=` 도 동작하지만 경고가 뜬다.

---

## 9. PyMySQL + Streamlit 대시보드 — `09_app.py` · `10_app_search.py`

`fetchall()` 이 돌려주는 `list[dict]` 를 **그대로 `st.table()` 에 넣으면** dict 의 키가 컬럼 제목이 된다. SQL 에서 `AS 도시명` 처럼 한글 별칭을 주면 화면 표 제목도 한글이 된다.

```python
# 09_app.py — 한국 상위 10개 도시
st.title("world DB 한국 주요 도시 현황")
rows = load_korea_top10()        # SELECT Name AS 도시명, District AS 도_지역, Population AS 인구수 …
st.table(rows)
```

`10_app_search.py` 는 Day 007 의 위젯을 DB 조건과 연결한 것이다.

```python
with st.sidebar:
    continent = st.selectbox("대륙 선택", continents)            # 선택지도 DISTINCT 로 DB에서

with st.form(key="search_form"):
    min_pop = st.number_input("최소 인구수를 입력하세요", value=9_500_000)
    submitted = st.form_submit_button("DB 검색 실행")

if submitted:
    sql = """SELECT C.Name AS 도시명, CO.Name AS 국가명, C.Population AS 인구수
             FROM city AS C INNER JOIN country AS CO ON C.CountryCode = CO.Code
             WHERE CO.Continent = %s AND C.Population >= %s
             ORDER BY C.Population DESC"""
    rows = run_query(sql, (continent, int(min_pop)))              # ← 값은 튜플로 따로
    st.success(f"{continent} 대륙 / {int(min_pop):,}명 이상 도시 검색 완료!")
    st.table(rows)                                                # Mumbai / Seoul / Shanghai / Jakarta
```

⚠️ 사용자 입력값을 `f"... WHERE Continent = '{continent}'"` 처럼 **문자열에 직접 붙이면 안 된다**. `%s` 자리표시자를 두고 `execute(sql, (값, 값))` 으로 넘기면 PyMySQL 이 값을 안전하게 감싸 준다 — **SQL Injection** 을 막는 기본기다.
💡 `st.form` 덕분에 숫자를 고칠 때마다 DB에 쿼리가 날아가지 않고, [DB 검색 실행] 을 누를 때만 한 번 조회된다.

📄 오늘 명령어 전체 요약 → [`lecture/11_명령어_요약정리.sql`](./lecture/11_명령어_요약정리.sql) (시험 대비용 치트시트)

---

## 🔁 복습

**다시 정리한 것**
- [x] `CROSS JOIN` 은 `ON` 이 없다. 행 수가 A × B 로 불어나므로 큰 테이블끼리는 `COUNT(*)` 로만 확인
- [x] `SELF JOIN` 은 같은 테이블에 **다른 별칭** 두 개. 별칭이 곧 "역할"(사원 / 상사)이다
- [x] 종합 실습 한 문장 = `JOIN → GROUP BY → HAVING → ORDER BY`. 어제 정리한 작성 순서가 그대로 쓰였다
- [x] PK 는 자동 인덱스. `EXPLAIN` 의 `type` 이 `ALL` 이면 풀 스캔, `ref` / `const` / `range` 면 인덱스 사용
- [x] 앞에 `%` 가 붙은 `LIKE` 는 인덱스를 못 쓴다 — 정렬된 앞글자로 찾아가는 구조라서 (Day 008 질문 해결)
- [x] 뷰는 데이터가 아니라 **쿼리 텍스트**를 저장한다. 그래서 공간을 안 쓰고, 원본 변경이 즉시 반영되고, 지워도 원본은 무사하다
- [x] 뷰의 두 목적 — **보안**(민감 컬럼 제외 + 뷰에만 권한) · **재사용**(긴 JOIN 을 한 줄로)
- [x] ERROR 1046 은 "어느 DB 에 넣을지 모름". Default Target Schema 를 고르거나 덤프 첫 줄에 `USE` 를 넣는다
- [x] PyMySQL 4단계 `connect → cursor → execute → fetchall`, 그리고 `DictCursor` 로 `list[dict]`
- [x] `fetchall()` 결과를 `st.table()` 에 바로 넣을 수 있다. SQL 별칭이 표 제목이 된다
- [x] 입력값은 `%s` + 튜플로 — 문자열 결합으로 SQL 을 만들지 않는다
- [x] 어제 남긴 "SELF JOIN · CROSS JOIN 실습" · "JOIN 성능과 인덱스" 두 질문 해결

**막혔던 부분 / 질문**
- [ ] 인덱스를 **두 컬럼 이상**에 걸면(복합 인덱스) 컬럼 순서가 왜 중요한지
- [ ] `EXPLAIN` 의 `rows` 가 실제 행 수(4079)와 조금 다르게(4046) 나오는 이유 — 통계 추정치인지
- [ ] 뷰에 `INSERT` / `UPDATE` 가 되는 경우와 안 되는 경우(JOIN · GROUP BY 가 든 뷰)
- [ ] `GRANT` 로 뷰에만 권한을 주는 실습을 실제 계정으로 해 보기 (DBA 권한 필요)
- [ ] 물리적 백업은 실무에서 어떤 도구로 하는지 (MySQL Enterprise Backup, Percona XtraBackup?)
- [ ] `pymysql.connect()` 를 화면이 재실행될 때마다 여는데, 접속을 **재사용**하려면 (`st.cache_resource`?)
- [ ] `st.table` 과 `st.dataframe` 의 차이 — 정렬 · 스크롤이 필요하면 어느 쪽인지
- [ ] Pandas 를 쓰면 `pd.read_sql(sql, conn)` 한 줄로 끝난다는데, `fetchall()` 과 언제 무엇을 쓰는지

**직접 해본 것**
- [x] 교재 p.107 ~ p.139 실습을 주제별 `.sql` 7개 · `.py` 3개 · 환경 설정 `.md` 로 나눠 정리하고 `lecture/` 에 업로드
- [x] 교재 스크립트에 **반복 실행용 초기화**(`DROP … IF EXISTS`)와 **응용 쿼리**(CROSS JOIN 조합표, SELF JOIN 의 LEFT 버전, 뷰 위 집계, 뷰 실시간 동기화 확인)를 추가
- [x] 교재에 개념만 있던 **인덱스**를 `EXPLAIN` + `CREATE INDEX` 로 실습 파일로 만듦 (풀 스캔 → 인덱스 스캔 전환 확인)
- [x] MariaDB 10.11(MySQL 호환) + `world` 환경에서 SQL 6개 파일 전체 실행 → 에러 없음, 주석의 결과값 확인 (종합 실습 5개 대륙 수치 일치)
- [x] `08_pymysql_study.py` 실행 → 교재 p.135 화면과 동일한 출력 확인. `09` · `10` 은 Streamlit `AppTest` 로 돌려 표 10행 · 검색 결과 4행(Mumbai / Seoul / Shanghai / Jakarta) 확인
- [x] 교재 스크린샷에만 있던 `app.py` · `app_search.py` 는 화면을 보고 코드로 복원 (`%s` 파라미터 바인딩 적용)
- [ ] `10_app_search.py` 에 `st.bar_chart` 를 붙여 검색 결과를 그래프로도 보여주기
- [ ] Day 007 의 세션 상태(`st.session_state`)로 검색 이력 남기기

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [JOIN 구문 (CROSS JOIN 포함)](https://dev.mysql.com/doc/refman/8.0/en/join.html)
- [인덱스 최적화 — How MySQL Uses Indexes](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html) · [EXPLAIN 출력 읽기](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)
- [CREATE VIEW](https://dev.mysql.com/doc/refman/8.0/en/create-view.html) · [뷰의 갱신 가능 조건](https://dev.mysql.com/doc/refman/8.0/en/view-updatability.html)
- [mysqldump — 논리적 백업](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [PyMySQL 문서](https://pymysql.readthedocs.io/en/latest/) · [PyMySQL 예제 (DictCursor)](https://pymysql.readthedocs.io/en/latest/user/examples.html)
- [Streamlit — st.table](https://docs.streamlit.io/develop/api-reference/data/st.table) · [st.form](https://docs.streamlit.io/develop/concepts/architecture/forms)
