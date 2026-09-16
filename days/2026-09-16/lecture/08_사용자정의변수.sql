/* ===================================================================
   [08] 사용자 정의 변수 (@변수)
   교재 : p.79 ~ p.81
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   개념 : Workbench 에서 접속을 끊기 전(세션 유지 동안)까지 살아있는 변수
   문법 : SET @변수명 = 값;
          SELECT @변수명;
   =================================================================== */

USE world;


/* ── 1. 실습 스크립트 (p.80 ~ p.81) ───────────────────────────────── */

-- 변수 생성
SET @target_continent = 'Asia';

-- 조건절에 변수 활용
SELECT Name, Continent, Population
FROM country
WHERE Continent = @target_continent
ORDER BY Population DESC
LIMIT 3;

-- 결과 : China, India, Indonesia
-- 변수 값만 'Europe' 으로 바꿔 다시 실행하면 쿼리 수정 없이 결과가 바뀐다


/* ── 2. 변수 값 확인 · 여러 개 선언 ──────────────────────────────── */

SET @min_pop = 100000000, @label = '인구 1억 이상';

SELECT @target_continent, @min_pop, @label;

SELECT @label AS 구분, Name, Population
FROM country
WHERE Population >= @min_pop;


/* ── 3. 조회 결과를 변수에 담기 (SELECT … INTO) ───────────────────── */

SELECT AVG(Population) INTO @avg_pop FROM country;

-- 평균보다 인구가 많은 국가 수
SELECT COUNT(*) AS 평균초과국가수
FROM country
WHERE Population > @avg_pop;


/* ── 4. 주의 : LIMIT 에는 @변수를 직접 쓸 수 없다 ────────────────────
   -- ✕ Error 1064 (문법 에러)
   SET @n = 3;
   SELECT Name FROM country LIMIT @n;

   → PREPARE 문(동적 SQL)으로 우회해야 한다
   ------------------------------------------------------------------ */

SET @n = 3;
PREPARE stmt FROM 'SELECT Name, Population FROM country ORDER BY Population DESC LIMIT ?';
EXECUTE stmt USING @n;          -- ? 자리에 @n 값이 들어감
DEALLOCATE PREPARE stmt;        -- 사용이 끝난 문장 해제


/* ── 참고 ───────────────────────────────────────────────────────────
   - 선언하지 않은 변수를 조회하면 에러가 아니라 NULL 이 나온다
   - 접속(세션)이 끊기면 변수는 사라진다. 다른 접속 창에서는 보이지 않음
   ------------------------------------------------------------------ */
