/* ===================================================================
   [15] 외부 조인 (LEFT / RIGHT OUTER JOIN)
   교재 : p.106 ~ p.107
   선행 : testdb (world 응용 예시는 world 샘플 DB 필요)
   -------------------------------------------------------------------
   LEFT OUTER JOIN
     : 왼쪽(기준) 테이블의 모든 행 출력,
       오른쪽에 매칭되는 데이터가 없으면 NULL 로 채움
       SELECT A.컬럼1, B.컬럼2
       FROM 테이블A(기준) AS A
       LEFT OUTER JOIN 테이블B(상대) AS B ON A.조인키 = B.조인키;

   RIGHT OUTER JOIN
     : 오른쪽(기준) 테이블의 모든 행 출력,
       왼쪽에 매칭되는 데이터가 없으면 NULL 로 채움
       SELECT A.컬럼1, B.컬럼2
       FROM 테이블A(상대) AS A
       RIGHT OUTER JOIN 테이블B(기준) AS B ON A.조인키 = B.조인키;

   ※ OUTER 는 생략 가능 : LEFT JOIN / RIGHT JOIN
   =================================================================== */

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;


/* ── 0. 실습 준비 (p.107) ─────────────────────────────────────────────
   회원(j_member) 2명 중 이영희는 구매 이력(j_buy)이 없다
   ------------------------------------------------------------------ */

-- 반복 실행용 초기화
DROP TABLE IF EXISTS j_buy;
DROP TABLE IF EXISTS j_member;

CREATE TABLE j_member (
    user_id   VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(10)
);

CREATE TABLE j_buy (
    order_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id   VARCHAR(10),        -- j_member.user_id 를 가리키는 조인키
    prod_name VARCHAR(20)
);

INSERT INTO j_member VALUES ('KIM', '김철수'), ('LEE', '이영희');
INSERT INTO j_buy    VALUES (NULL, 'KIM', '노트북');   -- NULL → AUTO_INCREMENT 가 1 부여


/* ── 1. INNER JOIN 과 비교 (교집합만) ─────────────────────────────── */

SELECT M.user_id, M.user_name, B.prod_name
FROM j_member M
INNER JOIN j_buy B ON M.user_id = B.user_id;

-- 결과 : KIM 1건만 (이영희는 j_buy 에 없어서 빠짐)


/* ── 2. LEFT JOIN 실행 (p.107) ────────────────────────────────────────
   구매 이력이 없는 이영희 회원도 포함되어 출력됨
   ------------------------------------------------------------------ */

SELECT M.user_id, M.user_name, B.prod_name
FROM j_member M                                -- 왼쪽 = 기준 (전체 출력)
LEFT JOIN j_buy B ON M.user_id = B.user_id;

-- 결과
-- user_id | user_name | prod_name
-- KIM     | 김철수    | 노트북
-- LEE     | 이영희    | NULL       ← 매칭 없음 → NULL


/* ── 3. RIGHT JOIN — 기준을 오른쪽으로 ────────────────────────────────
   테이블 순서를 바꾸면 LEFT JOIN 과 같은 결과를 RIGHT JOIN 으로 낼 수 있다
   ------------------------------------------------------------------ */

SELECT M.user_id, M.user_name, B.prod_name
FROM j_buy B
RIGHT JOIN j_member M ON B.user_id = M.user_id;   -- 오른쪽(j_member) = 기준

-- 실무에서는 읽기 쉬운 LEFT JOIN 으로 통일하는 경우가 많다


/* ── 4. 응용 : 한 번도 구매하지 않은 회원 찾기 ───────────────────────
   LEFT JOIN 후 오른쪽 값이 NULL 인 행만 남긴다 (차집합)
   ------------------------------------------------------------------ */

SELECT M.user_id, M.user_name
FROM j_member M
LEFT JOIN j_buy B ON M.user_id = B.user_id
WHERE B.user_id IS NULL;          -- 결과 : LEE 이영희


/* ── 5. 응용 : IFNULL 로 NULL 을 보기 좋게 ─────────────────────────── */

SELECT
    M.user_name                    AS 회원명,
    IFNULL(B.prod_name, '구매없음') AS 구매상품
FROM j_member M
LEFT JOIN j_buy B ON M.user_id = B.user_id;


/* ── 6. 응용 : world — 도시 정보가 없는 국가 ──────────────────────── */

USE world;

SELECT CO.Code, CO.Name, CO.Population
FROM country CO
LEFT JOIN city C ON CO.Code = C.CountryCode
WHERE C.ID IS NULL;               -- 결과 : 7건 (Antarctica 등 무인 지역)


/* ── 참고 : 벤 다이어그램으로 정리 ────────────────────────────────────
   INNER JOIN               A ∩ B
   LEFT JOIN                A 전체 (B 없으면 NULL)
   LEFT JOIN + B IS NULL    A - B
   RIGHT JOIN               B 전체 (A 없으면 NULL)
   ※ MySQL 은 FULL OUTER JOIN 을 지원하지 않음 → LEFT ∪ RIGHT 를 UNION 으로 구현
   ------------------------------------------------------------------ */
