/* ===================================================================
   [01] 외부 조인 실습 결과 확인 · 상호 조인(CROSS JOIN) · 자체 조인(SELF JOIN)
   교재 : p.107 ~ p.111
   선행 : testdb 존재 (없으면 아래 CREATE DATABASE IF NOT EXISTS 가 만들어 줌)
   -------------------------------------------------------------------
   CROSS JOIN : 조인 조건(ON) 없이 A의 모든 행 × B의 모든 행을 1:1 로 무조건 조합
                → 결과 행 수 = A 행 수 * B 행 수 (카테시안 곱)
   SELF  JOIN : 하나의 테이블을 자기 자신과 조인 (사원-상사, 카테고리-상위카테고리)
                → 같은 테이블을 두 번 참조하므로 서로 다른 별칭(A, B)이 필수
   =================================================================== */

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;


/* ── 0. 어제 만든 외부 조인 실습 결과 재확인 (p.107) ──────────────────
   j_member(회원) 와 j_buy(구매) — 이영희(LEE) 회원은 구매 이력이 없다.
   ※ 반복 실행을 위해 테이블을 지우고 다시 만든다.
   ------------------------------------------------------------------ */
DROP TABLE IF EXISTS j_buy;
DROP TABLE IF EXISTS j_member;

CREATE TABLE j_member (user_id VARCHAR(10) PRIMARY KEY, user_name VARCHAR(10));
CREATE TABLE j_buy   (order_id INT AUTO_INCREMENT PRIMARY KEY,
                      user_id VARCHAR(10), prod_name VARCHAR(20));

INSERT INTO j_member VALUES ('KIM', '김철수'), ('LEE', '이영희');
INSERT INTO j_buy    VALUES (NULL, 'KIM', '노트북');   -- order_id 는 AUTO_INCREMENT → NULL 로 두면 자동 부여

-- LEFT JOIN : 기준(왼쪽) 테이블 j_member 의 모든 행 + 매칭되는 j_buy 데이터
--             구매 이력이 없는 이영희도 출력되고, prod_name 은 NULL 로 채워진다
SELECT M.user_id, M.user_name, B.prod_name
FROM j_member M
LEFT JOIN j_buy B ON M.user_id = B.user_id;
-- 결과 : KIM 김철수 노트북 / LEE 이영희 NULL


/* ── 1. 상호 조인 · CROSS JOIN (p.108) ──────────────────────────────
   문법 : SELECT A.컬럼1, B.컬럼2
          FROM   테이블A AS A
          CROSS JOIN 테이블B AS B;        -- ON 절이 없다!

   용도 : 시스템 성능 테스트, 대량의 더미(Dummy) 데이터 생성
   ------------------------------------------------------------------ */

-- 1) 작은 테이블로 눈으로 확인 : 회원 2명 × 구매 1건 = 2행
SELECT M.user_name, B.prod_name
FROM j_member AS M
CROSS JOIN j_buy AS B;

-- 2) 행 수가 곱으로 불어나는 것 확인 : city(4079) × country(239) = 974,881 행
--    ※ SELECT * 로 실제 출력하면 화면이 멈추다시피 하므로 COUNT 로만 확인
USE world;
SELECT COUNT(*) AS 카테시안_행수
FROM city AS C
CROSS JOIN country AS CO;
-- 결과 : 974881

-- 3) 참고 : 더미 데이터 생성 예 — 국가 3개 × 연도 3개 = 9행의 조합표
SELECT CO.Name AS 국가, Y.yr AS 연도
FROM (SELECT Name FROM country WHERE Code IN ('KOR', 'JPN', 'CHN')) AS CO
CROSS JOIN (SELECT 2024 AS yr UNION SELECT 2025 UNION SELECT 2026) AS Y
ORDER BY 국가, 연도;


/* ── 2. 자체 조인 · SELF JOIN (p.109 ~ p.111) ───────────────────────
   문법 : SELECT E.emp_name AS 사원명, M.emp_name AS 상사명
          FROM  테이블명 AS E                  -- [사원 역할]
          INNER JOIN 테이블명 AS M             -- [상사 역할] 같은 테이블
          ON E.manager_id = M.emp_id;          -- 사원의 상사ID = 상사의 사원ID

   ★ 핵심 주의사항 : 한 테이블을 두 번 참조하므로 반드시 서로 다른 별칭을 준다.
   ------------------------------------------------------------------ */
USE testdb;

-- 자체 조인용 조직도 테이블 생성 (반복 실행용 초기화 포함)
DROP TABLE IF EXISTS emp_tree;
CREATE TABLE emp_tree (emp_name VARCHAR(10), mgr_name VARCHAR(10));
INSERT INTO emp_tree VALUES ('김사원', '박대리'), ('박대리', '최부장');

-- SELF JOIN 실행 : 사원과 직속 상사, 그리고 상사의 상사를 한 줄로 연동
--   A = 사원 역할, B = 상사 역할 (같은 emp_tree 를 두 번 읽는다)
SELECT A.emp_name AS 사원,
       A.mgr_name AS 직속상사,
       B.mgr_name AS 상사의상사
FROM emp_tree A
INNER JOIN emp_tree B ON A.mgr_name = B.emp_name;
-- 결과 : 김사원 | 박대리 | 최부장   (1행)
--   ※ 박대리는 상사(최부장)가 emp_tree 에 사원으로 없어 INNER JOIN 에서 빠진다


/* ── 참고 : INNER 대신 LEFT 로 바꾸면 ─────────────────────────────────
   상사의 상사가 없는 사람(박대리)도 NULL 로 남는다.
   ------------------------------------------------------------------ */
SELECT A.emp_name AS 사원,
       A.mgr_name AS 직속상사,
       B.mgr_name AS 상사의상사
FROM emp_tree A
LEFT JOIN emp_tree B ON A.mgr_name = B.emp_name;
-- 결과 : 김사원 | 박대리 | 최부장
--        박대리 | 최부장 | NULL
