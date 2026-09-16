/* ===================================================================
   [01] world 데이터베이스 조건별 실전 조회 실습
   교재 : p.56 ~ p.61  (p.56 ~ p.57 ORDER BY · LIMIT 은 Day 008 09번 복습)
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   어제 배운 WHERE + AND + ORDER BY 를 한 쿼리에 조합하는 연습

   작성 순서 : SELECT → FROM → WHERE → ORDER BY → LIMIT
   =================================================================== */

USE world;


/* ── 복습 : 인구 상위 5개 국가 (p.56 ~ p.57) ───────────────────────── */

SELECT Name, Continent, Population
FROM country
ORDER BY Population DESC      -- 인구 내림차순
LIMIT 5;                      -- 상위 5건만


/* ── 문제 1 (p.58 ~ p.60) ─────────────────────────────────────────────
   city 테이블에서 한국(CountryCode = 'KOR') 도시 중 인구 100만 명 이상인
   도시의 Name, Population 을 인구수 내림차순으로 조회
   ------------------------------------------------------------------ */

SELECT Name, Population
FROM city
WHERE CountryCode = 'KOR'          -- 조건 1 : 한국 도시
  AND Population >= 1000000        -- 조건 2 : 인구 100만 이상
ORDER BY Population DESC;

-- 결과 : 7건 (Seoul → Pusan → Inchon → Taegu → Taejon → Kwangju → Ulsan)
-- ※ city 테이블은 국가명이 아니라 '국가코드(CountryCode)'를 가지고 있다
--   → 국가명으로 찾으려면 country 테이블과 JOIN 이 필요 (14번 파일)


/* ── 문제 2 (p.58, p.61) ──────────────────────────────────────────────
   country 테이블에서 기대수명(LifeExpectancy)이 80세 이상인 국가의
   Name, Continent, LifeExpectancy 조회
   ------------------------------------------------------------------ */

SELECT Name, Continent, LifeExpectancy
FROM country
WHERE LifeExpectancy >= 80;

-- 결과 : 5건 (Andorra, Japan, Macao, Singapore, San Marino)
-- ※ LifeExpectancy 가 NULL 인 국가는 비교 결과가 NULL(참 아님)이라 자동 제외


/* ── 응용 : 문제 2 를 기대수명 높은 순으로 정렬 ─────────────────────── */

SELECT Name, Continent, LifeExpectancy
FROM country
WHERE LifeExpectancy >= 80
ORDER BY LifeExpectancy DESC;
