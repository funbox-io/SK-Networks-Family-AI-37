/* ===================================================================
   [04] 데이터 조작 CRUD — INSERT / SELECT / UPDATE / DELETE   ※ DML
   교재 : p.33 ~ p.41
   선행 : 03번 파일 실행 (testdb.test_table 이 제약조건 포함 상태로 존재)
   =================================================================== */

USE testdb;


/* ── 1. 데이터 저장 · INSERT (p.33 ~ p.34) ──────────────────────────
   문법 : INSERT INTO 테이블명 (컬럼1, 컬럼2, …) VALUES (값1, 값2, …);
   ------------------------------------------------------------------ */

-- 1) 단일 행 데이터 입력 (AUTO_INCREMENT인 col1은 생략 → 자동으로 1 부여)
INSERT INTO test_table (col2, col3) VALUES ('데이터입력1', '2025-01-01');

-- 2) 다중 행 데이터 동시 입력 : VALUES 뒤를 콤마로 이어서 작성
INSERT INTO test_table (col2, col3) VALUES
    ('데이터입력2', '2025-01-02'),
    ('데이터입력3', '2025-01-03');


/* ── 2. 데이터 조회 · SELECT (p.35 ~ p.36) ──────────────────────────
   문법 : SELECT 컬럼1, 컬럼2 FROM 테이블명;   -- 특정 컬럼 조회
          SELECT * FROM 테이블명;              -- 전체 컬럼 조회
   ------------------------------------------------------------------ */

-- test_table의 모든 데이터 조회 (col1에 1, 2, 3이 자동 부여된 것 확인)
SELECT * FROM test_table;

-- 특정 컬럼만 조회
SELECT col2, col3 FROM test_table;


/* ── 3. 데이터 수정 · UPDATE & Safe Mode (p.37 ~ p.38) ──────────────
   문법 : UPDATE 테이블명 SET 컬럼명 = 변경할값 WHERE 조건절;

   ★ 주의사항
     1) WHERE절 없이 UPDATE/DELETE를 실행하거나, PK가 아닌 조건으로
        수정 시 Workbench Safe Mode에서 에러 발생
     2) 해제 명령 : SET sql_safe_updates = 0;
   ------------------------------------------------------------------ */

-- 1) 특정 데이터만 수정 (col1이 3인 데이터) — PK 조건이라 Safe Mode에서도 동작
UPDATE test_table SET col2 = '데이터 수정' WHERE col1 = 3;
SELECT * FROM test_table;

-- 2) Safe Mode 해제 후 WHERE 없이 전체 데이터 수정
SET sql_safe_updates = 0;
UPDATE test_table SET col2 = '전체 데이터 수정';

-- 3) 결과 확인 (세 행의 col2가 모두 동일하게 변경됨)
SELECT * FROM test_table;


/* ── 4. 데이터 삭제 · DELETE (p.39 ~ p.41) ──────────────────────────
   문법 : DELETE FROM 테이블명 WHERE 조건절;
   ------------------------------------------------------------------ */

-- 1) 조건에 맞는 특정 행 삭제 (col1이 2인 행 삭제)
DELETE FROM test_table WHERE col1 = 2;
SELECT * FROM test_table;

-- 2) 테이블 내 전체 데이터 삭제 (WHERE 없음 → 주의!)
--    ※ 테이블 구조는 남고 데이터만 전부 사라짐
DELETE FROM test_table;
SELECT * FROM test_table;
