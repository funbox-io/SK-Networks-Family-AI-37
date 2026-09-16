/* ===================================================================
   [02] 주요 집계 함수 (COUNT, SUM, AVG, MAX, MIN)
   교재 : p.62 ~ p.64
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   집계 함수 (Aggregate Function)
     1) 여러 행의 데이터를 입력받아 '단 하나'의 요약 결과값을 계산
     2) NULL 값은 자동으로 계산 대상에서 제외됨

   함수      설명                    NULL 처리
   COUNT()   행(레코드)의 개수        COUNT(*) 는 NULL 포함
   SUM()     컬럼 값들의 총합         제외
   AVG()     컬럼 값들의 평균         제외
   MAX()     컬럼 값 중 최대값        제외
   MIN()     컬럼 값 중 최소값        제외
   =================================================================== */

USE world;


/* ── 1. 실습 스크립트 (p.63 ~ p.64) ───────────────────────────────── */

SELECT
    COUNT(*)        AS 전체국가수,       -- 239
    SUM(Population) AS 전세계총인구,
    AVG(Population) AS 국가별평균인구,   -- 소수점 포함 결과
    MAX(Population) AS 최고인구수,
    MIN(Population) AS 최저인구수        -- 0 (무인도 등 인구 0인 지역)
FROM country;

-- AS 별칭 : 결과 컬럼 이름을 바꿔 보여준다 (한글 별칭도 가능)


/* ── 2. COUNT(*) vs COUNT(컬럼) — NULL 처리 차이 확인 ─────────────── */

SELECT
    COUNT(*)              AS 전체행수,        -- 239 : NULL 여부와 무관하게 행 수
    COUNT(LifeExpectancy) AS 기대수명있는행,   -- 222 : NULL 17건 제외
    COUNT(IndepYear)      AS 독립연도있는행    -- 192 : NULL 47건 제외
FROM country;


/* ── 3. AVG 는 NULL 을 '0' 이 아니라 '없는 값'으로 본다 ─────────────
   AVG(LifeExpectancy) = SUM(LifeExpectancy) / COUNT(LifeExpectancy)
   → 분모가 239 가 아니라 222
   ------------------------------------------------------------------ */

SELECT
    AVG(LifeExpectancy)                         AS AVG결과,
    SUM(LifeExpectancy) / COUNT(LifeExpectancy) AS 직접계산_NULL제외,
    SUM(LifeExpectancy) / COUNT(*)              AS 직접계산_NULL포함   -- 값이 다름
FROM country;


/* ── 참고 : 소수점 정리 ─────────────────────────────────────────────
   ROUND(값, n) : 소수점 n 자리까지 반올림

   SELECT ROUND(AVG(Population), 0) AS 평균인구 FROM country;
   ------------------------------------------------------------------ */
