/* ===================================================================
   [02] 종합 실습 — SQL 기본 및 조인 다지기
   교재 : p.112 ~ p.114
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   과제 : world 데이터베이스를 활용하여 다음 결과를 출력하는 단일 SQL 문을 작성
     1. 대륙(Continent)별로 도시 인구(city.Population)의 합계를 구하시오.
     2. 도시 인구 합계가 1억 명 이상인 대륙만 필터링하시오.
     3. 결과를 도시 인구 합계 내림차순으로 정렬하시오.
   =================================================================== */

USE world;


/* ── 1. 문제 풀이 순서대로 뜯어보기 ──────────────────────────────────
   대륙은 country 에, 도시 인구는 city 에 있다 → 두 테이블을 JOIN 해야 한다.
     country.Code (PK)  =  city.CountryCode (FK)
   ------------------------------------------------------------------ */

-- 1단계) 도시와 국가를 붙여서 대륙별로 묶고 합계 (GROUP BY + SUM)
SELECT CO.Continent AS 대륙, SUM(C.Population) AS 총도시인구합계
FROM country CO
INNER JOIN city C ON CO.Code = C.CountryCode
GROUP BY CO.Continent;

-- 2단계) 그룹 결과(합계)로 거르기 → 집계 조건이므로 WHERE 가 아니라 HAVING
-- 3단계) 합계 기준 내림차순 정렬


/* ── 2. 종합 실습 정답 스크립트 (p.113) ─────────────────────────────── */
SELECT
    CO.Continent      AS 대륙,
    SUM(C.Population) AS 총도시인구합계
FROM country CO
INNER JOIN city C ON CO.Code = C.CountryCode
GROUP BY CO.Continent
HAVING 총도시인구합계 >= 100000000       -- 1억 이상 대륙만 (SELECT 별칭 사용 가능 — MySQL 확장)
ORDER BY 총도시인구합계 DESC;

/* 결과 (p.114)
   Asia           697604103
   Europe         241942813
   South America  172037859
   North America  168250381
   Africa         135838579
   ※ Oceania(약 1,390만) 는 HAVING 에서 걸러지고, 도시가 없는 Antarctica 는 INNER JOIN 단계에서 이미 빠진다.
*/


/* ── 참고 : 별칭 없이 쓰면 ────────────────────────────────────────────
   HAVING 과 ORDER BY 에 집계식을 그대로 다시 적어도 된다. 다른 DB 로 옮길 때는
   이쪽이 안전하다 (표준 SQL 은 HAVING 에서 SELECT 별칭을 보장하지 않음).
   ------------------------------------------------------------------ */
SELECT CO.Continent, SUM(C.Population)
FROM country CO
INNER JOIN city C ON CO.Code = C.CountryCode
GROUP BY CO.Continent
HAVING SUM(C.Population) >= 100000000
ORDER BY SUM(C.Population) DESC;


/* ── 응용 : 대륙별 도시 수 · 최대 도시 인구까지 한 번에 ─────────────── */
SELECT
    CO.Continent      AS 대륙,
    COUNT(*)          AS 도시수,
    SUM(C.Population) AS 총도시인구합계,
    MAX(C.Population) AS 최대도시인구
FROM country CO
INNER JOIN city C ON CO.Code = C.CountryCode
GROUP BY CO.Continent
ORDER BY 총도시인구합계 DESC;
