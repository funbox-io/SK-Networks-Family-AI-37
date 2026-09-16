/* ===================================================================
   [03] 데이터 그룹화 (GROUP BY)
   교재 : p.65 ~ p.67
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   GROUP BY 절
     1) 특정 컬럼 값이 같은 데이터끼리 묶어서 그룹별 집계(합계, 평균 등)
     2) Pandas 의 df.groupby('컬럼').agg(...) 와 같은 기능

   문법 : SELECT 그룹컬럼, 집계함수(컬럼)
          FROM 테이블
          GROUP BY 그룹컬럼;
   =================================================================== */

USE world;


/* ── 1. 실습 스크립트 (p.66 ~ p.67) ───────────────────────────────────
   대륙(Continent)별 국가 수, 총 인구수, 평균 기대수명
   ------------------------------------------------------------------ */

SELECT
    Continent           AS 대륙,
    COUNT(*)            AS 국가수,
    SUM(Population)     AS 총인구수,
    AVG(LifeExpectancy) AS 평균기대수명
FROM country
GROUP BY Continent
ORDER BY 총인구수 DESC;     -- ORDER BY 에서는 SELECT 의 별칭 사용 가능

-- 결과 : 7개 대륙이 한 행씩 (Asia 가 총인구 1위)
-- ※ Antarctica 는 인구 0, 기대수명 NULL → 평균기대수명도 NULL


/* ── 2. GROUP BY 규칙 ─────────────────────────────────────────────────
   SELECT 에는 ① GROUP BY 에 쓴 컬럼  ② 집계 함수  만 오는 것이 원칙.
   그룹마다 값이 여러 개인 일반 컬럼(Name 등)을 그냥 쓰면
   MySQL 기본 설정(ONLY_FULL_GROUP_BY)에서 에러가 난다.

   -- ✕ 에러 : 대륙 하나에 국가 Name 이 여러 개라 무엇을 보여줄지 모름
   SELECT Continent, Name, COUNT(*) FROM country GROUP BY Continent;
   ------------------------------------------------------------------ */


/* ── 3. 응용 : 두 컬럼으로 그룹화 ─────────────────────────────────────
   대륙 + 지역(Region) 조합별 국가 수
   ------------------------------------------------------------------ */

SELECT Continent AS 대륙, Region AS 지역, COUNT(*) AS 국가수
FROM country
GROUP BY Continent, Region
ORDER BY 대륙, 국가수 DESC;


/* ── 참고 : Pandas 와 비교 ──────────────────────────────────────────
   df.groupby('Continent').agg(
       국가수=('Name', 'count'),
       총인구수=('Population', 'sum'),
       평균기대수명=('LifeExpectancy', 'mean')
   ).sort_values('총인구수', ascending=False)
   ------------------------------------------------------------------ */
