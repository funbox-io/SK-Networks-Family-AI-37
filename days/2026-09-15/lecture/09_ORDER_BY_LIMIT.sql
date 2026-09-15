/* ===================================================================
   [09] 조회 결과 정렬(ORDER BY) 및 개수 제한(LIMIT)
   교재 : p.56  ← 오늘 수업 마지막 페이지
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   ORDER BY 절
     : 조회된 결과를 특정 컬럼 기준으로 정렬
       ASC  = 오름차순 (기본값, 생략 가능)
       DESC = 내림차순
   LIMIT 절
     : 출력할 결과의 개수를 제한 (Top-N 추출)
   =================================================================== */

USE world;


-- 인구수가 가장 많은 상위 5개 국가 조회 (내림차순 정렬 + LIMIT)
SELECT Name, Continent, Population
FROM country
ORDER BY Population DESC
LIMIT 5;


/* ── 참고 : 작성 순서 ───────────────────────────────────────────────
   SELECT  →  FROM  →  WHERE  →  ORDER BY  →  LIMIT
   순서를 바꾸면 문법 에러가 나므로 이 흐름을 그대로 외워둘 것.

   예) 아시아 국가 중 인구 상위 3개
   SELECT Name, Population
   FROM country
   WHERE Continent = 'Asia'
   ORDER BY Population DESC
   LIMIT 3;
   ------------------------------------------------------------------ */
