/* ===================================================================
   [11] 오늘 배운 명령어 한눈에 보기 (p.107 ~ p.139 요약)
   용도 : 복습 / 시험 대비용 치트시트
   =================================================================== */


/* ── JOIN 마무리 ────────────────────────────────────────────────────
   CROSS JOIN   : ON 없이 A × B 모든 조합 (행 수 = A행 * B행) — 더미 데이터 · 성능 테스트
     SELECT A.c1, B.c2 FROM 테이블A AS A CROSS JOIN 테이블B AS B;

   SELF JOIN    : 같은 테이블을 두 번 참조 — 조직도(사원-상사), 카테고리 계층
     SELECT E.emp_name AS 사원, M.emp_name AS 상사
     FROM emp AS E INNER JOIN emp AS M ON E.manager_id = M.emp_id;
     ※ 반드시 서로 다른 별칭(E, M)을 지정

   종합 : JOIN → GROUP BY → HAVING → ORDER BY
     SELECT CO.Continent, SUM(C.Population) AS 합계
     FROM country CO INNER JOIN city C ON CO.Code = C.CountryCode
     GROUP BY CO.Continent HAVING 합계 >= 100000000 ORDER BY 합계 DESC;
   ------------------------------------------------------------------ */


/* ── 인덱스 (Index) ─────────────────────────────────────────────────
   개념 : 특정 기준으로 정렬 + 범위 그룹으로 묶은 Tree 구조 → 몇 번의 비교로 즉시 탐색
   Full Table Scan : 인덱스 없음, 첫 행~마지막 행 전부 읽음 (느림)
   Index Scan      : 인덱스 있음, Tree 를 타고 내려가 해당 행만 추출 (빠름)

   SHOW INDEX FROM 테이블;                      -- 인덱스 목록
   EXPLAIN SELECT … ;                           -- 실행 계획 (type: ALL=풀스캔, ref/const=인덱스)
   CREATE INDEX 인덱스명 ON 테이블 (컬럼);
   DROP   INDEX 인덱스명 ON 테이블;
   ※ PK 는 자동 인덱스 / LIKE '%…' 는 인덱스 못 씀 / 쓰기 성능·용량은 비용
   ------------------------------------------------------------------ */


/* ── 뷰 (View) ──────────────────────────────────────────────────────
   정의 : 데이터가 아니라 SELECT 쿼리 텍스트만 저장하는 가상 테이블
   특징 : 디스크 공간 절약 · 원본 변경 시 실시간 동기화
   목적 : ① 보안(민감 컬럼 제외한 뷰에만 권한 부여)  ② 복잡한 JOIN 쿼리 재사용

   CREATE VIEW 뷰이름 AS SELECT 컬럼… FROM 테이블 WHERE 조건;
   SELECT * FROM 뷰이름;                        -- 일반 테이블처럼 조회
   DROP VIEW 뷰이름;                            -- 뷰만 삭제, 원본 데이터는 유지
   SHOW CREATE VIEW 뷰이름;                     -- 저장된 정의 확인
   ------------------------------------------------------------------ */


/* ── 백업 · 복원 ────────────────────────────────────────────────────
   논리적 백업(SQL Dump) : 구조(DDL) + 데이터(DML) 를 .sql 파일로   ← 실습 방식
   물리적 백업           : 디스크 파일(Data/Log File) 자체 복사

   Workbench : Server → Data Export (백업) / Data Import (복원)
   CLI       : mysqldump -u root -p --databases testdb > testdb_dump.sql
               mysql -u root -p < testdb_dump.sql

   ERROR 1046 No database selected
     원인 : 덤프 파일에 CREATE DATABASE / USE 가 없음
     해결 ① Data Import 의 Default Target Schema 에서 대상 DB 선택 (추천)
     해결 ② 덤프 파일 첫 줄에  CREATE DATABASE IF NOT EXISTS testdb; USE testdb;  추가
   ------------------------------------------------------------------ */


/* ── Python ↔ MySQL 연동 (PyMySQL) ──────────────────────────────────
   환경 : conda create -n db python=3.12 → conda activate db → pip install PyMySQL streamlit

   conn   = pymysql.connect(host, user, password, db, charset, cursorclass=DictCursor)
   cursor = conn.cursor()
   cursor.execute(sql, params)      -- params : %s 자리표시자에 넣을 튜플 (SQL Injection 방지)
   rows   = cursor.fetchall()       -- list[dict]  예) [{'Name': 'Seoul', 'Population': 9981619}, …]
   conn.close()

   Streamlit 연동 : rows 를 st.table(rows) 에 넘기면 dict 키 = 컬럼 제목
     - 09_app.py        : 조회 결과를 표로
     - 10_app_search.py : st.selectbox(대륙) + st.form(최소 인구수) → 조건을 SQL 로 전달
   ------------------------------------------------------------------ */
