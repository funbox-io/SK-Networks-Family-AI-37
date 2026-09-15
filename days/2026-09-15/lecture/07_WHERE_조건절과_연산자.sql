/* ===================================================================
   [07] WHERE 조건절과 비교 / 논리 연산자
   교재 : p.48 ~ p.50
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   WHERE 절
     : 테이블 전체 데이터 중 특정 조건에 맞는 행(Row)만 필터링할 때 사용

   주요 연산자
     1) 비교 연산자 : =, !=, >, <, >=, <=
     2) 논리 연산자 : AND (둘 다 참), OR (하나라도 참), NOT (조건 부정)
   =================================================================== */

USE world;


-- 1) 인구가 1억 명 이상인 국가 조회
SELECT Name, Continent, Population
FROM country
WHERE Population >= 100000000;


-- 2) 대륙이 'Asia'이면서 인구가 5,000만 명 이상인 국가 조회 (AND)
--    ※ 문자열 비교는 작은따옴표로 감쌈
SELECT Name, Continent, Population
FROM country
WHERE Continent = 'Asia' AND Population >= 50000000;


/* ── 참고 : OR / NOT 사용 형태 ──────────────────────────────────────
   -- 대륙이 Asia 이거나 Europe 인 국가 (OR)
   SELECT Name, Continent FROM country
   WHERE Continent = 'Asia' OR Continent = 'Europe';

   -- 대륙이 Asia가 아닌 국가 (NOT)
   SELECT Name, Continent FROM country
   WHERE NOT Continent = 'Asia';
   ------------------------------------------------------------------ */
