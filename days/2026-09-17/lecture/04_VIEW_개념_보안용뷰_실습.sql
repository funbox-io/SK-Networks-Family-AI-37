/* ===================================================================
   [04] 뷰(View)의 개념 · 동작 원리 · 보안용 뷰 실습
   교재 : p.116 ~ p.123
   선행 : testdb 존재
   -------------------------------------------------------------------
   뷰(View)의 정의
     : 자주 사용하는 조회 결과를 위해 별도의 테이블을 만들어 디스크에 저장하지 않고,
       SELECT 쿼리문 텍스트 자체만 DB 에 (키-값 형태로) 보관한 뒤, 사용자가 호출할 때
       일반 테이블과 동일하게 조회 기능을 제공하는 "가상 테이블"

   뷰의 내부 동작 과정
     1) 뷰 생성  : CREATE VIEW 뷰이름 AS SELECT …   구문 실행
     2) 정의 저장: DBMS 가 데이터가 아니라 SELECT 구문 자체만 저장
     3) 뷰 호출  : SELECT * FROM 뷰이름;
     4) 쿼리 실행: 저장된 SELECT 를 꺼내 원본 테이블(Base Table)을 대신 조회 → 최신 결과 반환

   뷰의 핵심 기술적 특징
     1) 디스크 공간 절약 : 조회 결과가 아닌 쿼리 정의만 보관
     2) 실시간 동기화   : 원본 데이터가 바뀌면 뷰 조회 결과에도 즉시 반영

   문법 : CREATE VIEW [뷰이름] AS SELECT [컬럼…] FROM [테이블명] WHERE [조건];
          DROP VIEW [뷰이름];
   =================================================================== */

USE testdb;


/* ── 1. 실습용 원본 테이블 준비 (p.121) ──────────────────────────────
   민감 컬럼(주민번호, 급여)이 섞여 있는 테이블.
   ※ 반복 실행을 위해 뷰 → 테이블 순서로 지우고 다시 만든다.
   ------------------------------------------------------------------ */
DROP VIEW  IF EXISTS v_user_security;
DROP TABLE IF EXISTS real_user;

CREATE TABLE real_user (
    user_id   VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL,
    user_ssn  VARCHAR(14),        -- 주민번호 (민감정보)
    salary    INT                 -- 급여     (민감정보)
);

INSERT INTO real_user VALUES
('KIM', '김철수', '950101-1234567', 4000000),
('LEE', '이영희', '980202-2345678', 3500000);


/* ── 2. 보안용 뷰 생성 (p.122) — 주민번호와 급여를 제외 ─────────────
   [뷰를 통한 강제적 접근 통제 3단계]  (p.119)
     1단계 원본 테이블 차단 : 민감 정보가 든 real_user 의 SELECT 권한을 사용자 계정에서 차단
     2단계 정제된 뷰 생성   : 민감 컬럼을 제외한 안전한 컬럼만 추출하여 뷰 생성   ← 지금 이 단계
     3단계 뷰 접근 권한 부여: 사용자 계정에 오직 이 뷰에 대해서만 SELECT 권한 부여
   ------------------------------------------------------------------ */
CREATE VIEW v_user_security AS
SELECT user_id, user_name
FROM real_user;


/* ── 3. 뷰 조회 테스트 — 안전한 정보만 출력된다 ──────────────────────── */
SELECT * FROM v_user_security;
-- 결과 : KIM 김철수 / LEE 이영희   (user_ssn, salary 컬럼 자체가 보이지 않음)

-- 뷰는 일반 테이블처럼 WHERE · ORDER BY 를 붙여 쓸 수 있다
SELECT * FROM v_user_security WHERE user_id = 'LEE';


/* ── 4. 실시간 동기화 확인 — 원본에 넣으면 뷰에도 바로 보인다 ────────── */
INSERT INTO real_user VALUES ('PARK', '박민수', '000303-3456789', 3000000);
SELECT * FROM v_user_security;
-- 결과 : KIM / LEE / PARK  — 뷰를 다시 만들지 않아도 새 행이 즉시 반영된다


/* ── 5. 뷰 삭제 (p.122) — 뷰를 지워도 원본 real_user 데이터는 안전하게 유지 ── */
DROP VIEW v_user_security;
SELECT * FROM real_user;
-- 결과 : 3행 모두 그대로 (주민번호·급여 포함). 뷰는 "창문"일 뿐 데이터를 들고 있지 않다


/* ── 참고 : 3단계(권한 부여)를 실제로 해 보면 ─────────────────────────
   DBA 권한이 있을 때만 실행된다. 개념 확인용.

   CREATE USER 'staff'@'localhost' IDENTIFIED BY 'staff1234';
   GRANT SELECT ON testdb.v_user_security TO 'staff'@'localhost';   -- 뷰에만 권한
   -- staff 계정으로 접속해서
   --   SELECT * FROM v_user_security;   → 성공
   --   SELECT * FROM real_user;         → ERROR 1142 SELECT command denied (Access Denied)
   DROP USER 'staff'@'localhost';
   ------------------------------------------------------------------ */
