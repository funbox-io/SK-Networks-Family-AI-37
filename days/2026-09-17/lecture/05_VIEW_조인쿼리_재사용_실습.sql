/* ===================================================================
   [05] 복잡한 조인(JOIN) 쿼리를 재사용하는 뷰 작성 실습
   교재 : p.120, p.124 ~ p.126
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   코드의 재사용성 (p.120)
     : 다중 테이블 JOIN, WHERE 조건절, GROUP BY 등이 포함된 복잡한 쿼리를 매번
       중복 작성할 필요 없이, 뷰로 한 번 등록해 두고 프로그램이나 쿼리에서
       자유롭게 재사용 가능
   =================================================================== */

USE world;


/* ── 1. 도시(city) + 국가(country) 를 조인하여 대륙이 'Asia' 인 데이터만
        추출하는 뷰 생성 (p.124) ──────────────────────────────────── */
DROP VIEW IF EXISTS v_asia_city_info;      -- 반복 실행용

CREATE VIEW v_asia_city_info AS
SELECT
    C.Name        AS city_name,
    CO.Name       AS country_name,
    C.Population  AS city_population
FROM city AS C
INNER JOIN country AS CO ON C.CountryCode = CO.Code
WHERE CO.Continent = 'Asia';


/* ── 2. 축약된 뷰를 일반 테이블처럼 조회 (p.125) ──────────────────────
   긴 INNER JOIN 문을 매번 쓰지 않고, 한 줄 SELECT 로 정제된 결과를 즉시 획득
   ------------------------------------------------------------------ */
SELECT * FROM v_asia_city_info
WHERE city_population >= 5000000
ORDER BY city_population DESC;
/* 결과 (p.126)
   Mumbai (Bombay)  India        10500000
   Seoul            South Korea   9981619
   Shanghai         China         9696300
   Jakarta          Indonesia     9604900
   Karachi          Pakistan      9269265
   …
*/

-- 뷰 위에 집계를 얹어도 된다 : 아시아 국가별 도시 수 Top 5
SELECT country_name, COUNT(*) AS 도시수, SUM(city_population) AS 도시인구합
FROM v_asia_city_info
GROUP BY country_name
ORDER BY 도시수 DESC
LIMIT 5;


/* ── 3. 뷰의 정의(저장된 SELECT 문) 들여다보기 ──────────────────────
   뷰는 데이터가 아니라 "쿼리 텍스트"만 저장한다는 것을 직접 확인
   ------------------------------------------------------------------ */
SHOW CREATE VIEW v_asia_city_info;

-- 현재 DB 의 뷰 목록 (SHOW TABLES 에도 뷰가 함께 나온다)
SHOW FULL TABLES WHERE Table_type = 'VIEW';


/* ── 4. 실습용 뷰 정리 ───────────────────────────────────────────── */
DROP VIEW v_asia_city_info;


/* ── 참고 : 뷰 이름 규칙 ─────────────────────────────────────────────
   교재처럼 v_ 접두어를 붙여 두면 SHOW TABLES 에서 테이블과 뷰가 한눈에 구분된다.
   ------------------------------------------------------------------ */
