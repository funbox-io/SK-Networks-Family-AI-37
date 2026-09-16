/* ===================================================================
   [14] 조인(JOIN)의 개념 및 내부 조인 (INNER JOIN)
   교재 : p.102 ~ p.105
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   조인(JOIN)
     : 중복 방지를 위해 여러 테이블로 나눠 저장한 데이터를
       공통 컬럼(PK - FK)을 매개로 하나로 합쳐 조회하는 기술

   조인의 종류
     1) INNER JOIN        : 두 테이블 모두에 있는 교집합만 결합
     2) LEFT/RIGHT OUTER  : 한쪽 테이블 전체 + 매칭되는 데이터 결합 (15번 파일)
     3) CROSS JOIN        : 모든 경우의 수 조합 (카테시안 곱)
     4) SELF JOIN         : 자기 자신과의 조인 (조직도 등)

   INNER JOIN 기본 구문
     SELECT A.컬럼1, B.컬럼2
     FROM 테이블A AS A
     INNER JOIN 테이블B AS B ON A.조인키 = B.조인키;
   =================================================================== */

USE world;


/* ── 0. 왜 JOIN 이 필요한가 ───────────────────────────────────────────
   city 에는 국가명이 없고 CountryCode 만 있다.
   국가명·대륙은 country 에 있으므로 두 테이블을 이어 붙여야 한다.

   city.CountryCode  ─────→  country.Code (PK)
      'KOR'                     'KOR' → Name 'South Korea', Continent 'Asia'
   ------------------------------------------------------------------ */

SELECT Name, CountryCode FROM city    WHERE CountryCode = 'KOR' LIMIT 3;
SELECT Code, Name, Continent FROM country WHERE Code = 'KOR';


/* ── 1. 실습 스크립트 (p.104 ~ p.105) ─────────────────────────────────
   도시(city) 정보 + 해당 도시가 속한 국가(country) 정보 결합
   아시아 도시 중 인구 상위 5개
   ------------------------------------------------------------------ */

SELECT
    C.Name        AS 도시명,
    CO.Name       AS 국가명,
    CO.Continent  AS 대륙,
    C.Population  AS 도시인구
FROM city AS C                                          -- C  : city 의 별칭
INNER JOIN country AS CO ON C.CountryCode = CO.Code     -- CO : country 의 별칭
WHERE CO.Continent = 'Asia'
ORDER BY C.Population DESC
LIMIT 5;

-- 결과 : Mumbai(India) → Seoul(South Korea) → Shanghai → Jakarta → Karachi
-- ※ 두 테이블에 같은 이름의 컬럼(Name, Population)이 있으므로
--   반드시 '별칭.컬럼' 으로 어느 테이블 것인지 지정해야 한다
--   (안 쓰면 Error 1052 : Column 'Name' in field list is ambiguous)


/* ── 2. INNER 는 생략 가능, AS 도 생략 가능 ───────────────────────── */

SELECT C.Name AS 도시명, CO.Name AS 국가명
FROM city C
JOIN country CO ON C.CountryCode = CO.Code     -- JOIN = INNER JOIN
WHERE CO.Code = 'KOR'
LIMIT 5;


/* ── 3. 응용 : JOIN + GROUP BY ────────────────────────────────────────
   대륙별 '도시' 수와 도시 인구 합계
   (city 에는 대륙 정보가 없으므로 JOIN 후 그룹화)
   ------------------------------------------------------------------ */

SELECT
    CO.Continent       AS 대륙,
    COUNT(*)           AS 도시수,
    SUM(C.Population)  AS 도시인구합계
FROM city C
INNER JOIN country CO ON C.CountryCode = CO.Code
GROUP BY CO.Continent
ORDER BY 도시수 DESC;


/* ── 4. 응용 : 3개 테이블 JOIN ────────────────────────────────────────
   한국의 수도 이름과 공용어
   country.Capital (도시 ID) = city.ID
   country.Code             = countrylanguage.CountryCode
   ------------------------------------------------------------------ */

SELECT
    CO.Name      AS 국가명,
    C.Name       AS 수도,
    CL.Language  AS 공용어
FROM country CO
INNER JOIN city C             ON CO.Capital = C.ID
INNER JOIN countrylanguage CL ON CO.Code    = CL.CountryCode
WHERE CO.Code = 'KOR'
  AND CL.IsOfficial = 'T';


/* ── 참고 : INNER JOIN 은 '양쪽 모두' 있는 행만 나온다 ────────────────
   country 중 city 테이블에 도시가 하나도 없는 국가(무인도 등 7개)는
   위 JOIN 결과에 나타나지 않는다 → 이런 행까지 보려면 LEFT JOIN (15번)
   ------------------------------------------------------------------ */
