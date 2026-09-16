/* ===================================================================
   [04] 그룹 조건절 HAVING vs WHERE 절의 차이
   교재 : p.68 ~ p.70
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   WHERE 절
     ① 개별 행(Row) 단위의 1차 필터링
     ② 집계 함수 사용 불가
     ③ 그룹으로 묶기 '전'에 거를 때 사용

   HAVING 절
     ① GROUP BY 로 묶인 결과에 대한 2차 필터링
     ② 집계 결과(평균, 합계 등)를 기준으로 거를 때 사용

   작성 순서 : SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
   실행 순서 : FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
   =================================================================== */

USE world;


/* ── 1. 실습 스크립트 (p.69 ~ p.70) ───────────────────────────────────
   총 인구수 5억 명 이상인 대륙만 출력 (HAVING)
   ------------------------------------------------------------------ */

SELECT
    Continent       AS 대륙,
    SUM(Population) AS 총인구수
FROM country
GROUP BY Continent
HAVING 총인구수 >= 500000000      -- 그룹별 합계로 필터링
ORDER BY 총인구수 DESC;

-- 결과 : Asia, Africa, Europe (3건)
-- ※ HAVING 에서 SELECT 별칭을 쓰는 것은 MySQL 이 허용하는 방식.
--   표준 SQL 에서는 HAVING SUM(Population) >= 500000000 으로 적는다.


/* ── 2. 같은 조건을 WHERE 에 쓰면? ────────────────────────────────────
   -- ✕ 에러 : WHERE 는 그룹이 만들어지기 전에 실행되므로 집계 함수 사용 불가
   SELECT Continent, SUM(Population)
   FROM country
   WHERE SUM(Population) >= 500000000
   GROUP BY Continent;
   → Error 1111 : Invalid use of group function
   ------------------------------------------------------------------ */


/* ── 3. WHERE + HAVING 함께 쓰기 ──────────────────────────────────────
   1차(WHERE)  : 인구 100만 이상인 국가만 남기고
   2차(HAVING) : 그런 국가가 20개 이상인 대륙만 출력
   ------------------------------------------------------------------ */

SELECT
    Continent AS 대륙,
    COUNT(*)  AS 인구100만이상_국가수
FROM country
WHERE Population >= 1000000        -- 행 단위 필터 (그룹화 전)
GROUP BY Continent
HAVING COUNT(*) >= 20              -- 그룹 단위 필터 (그룹화 후)
ORDER BY 인구100만이상_국가수 DESC;


/* ── 참고 : 헷갈릴 때 판단 기준 ────────────────────────────────────
   조건에 집계 함수(SUM, AVG, COUNT …)가 들어간다  → HAVING
   조건이 원본 컬럼 값 그대로다                    → WHERE
   (원본 컬럼 조건은 WHERE 에서 먼저 거르는 것이 처리량이 적어 유리)
   ------------------------------------------------------------------ */
