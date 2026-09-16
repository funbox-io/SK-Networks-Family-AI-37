/* ===================================================================
   [13] 내장 함수를 활용한 리포트 생성 실습
   교재 : p.99 ~ p.101
   선행 : sakila 샘플 DB
   -------------------------------------------------------------------
   문제
     sakila.film 에서 영화 제목(title), 대여 기간(rental_duration),
     대여료(rental_rate)를 조회하되
       1) 영화 제목은 대문자로 출력
       2) 대여료 3.0 이상이면 '프리미엄', 아니면 '일반' (IF 함수)
       3) 상위 10개만 조회
   =================================================================== */

USE sakila;


/* ── 정답 스크립트 (p.100 ~ p.101) ───────────────────────────────── */

SELECT
    UPPER(title)                               AS 영화제목,
    rental_duration                            AS 대여기간,
    rental_rate                                AS 대여료,
    IF(rental_rate >= 3.0, '프리미엄', '일반') AS 요금등급
FROM film
LIMIT 10;

-- ※ sakila 의 title 은 원래 대문자로 저장되어 있어 UPPER 전후가 같아 보인다
--   LOWER(title) 로 바꿔 보면 함수가 적용되는 것을 확인할 수 있음
-- ※ rental_rate 값은 0.99 / 2.99 / 4.99 세 종류 → 4.99 만 '프리미엄'


/* ── 응용 1 : 요금등급별 영화 수 · 평균 대여기간 ─────────────────── */

SELECT
    IF(rental_rate >= 3.0, '프리미엄', '일반') AS 요금등급,
    COUNT(*)                                   AS 영화수,          -- 프리미엄 336
    ROUND(AVG(rental_duration), 1)             AS 평균대여기간
FROM film
GROUP BY 요금등급;


/* ── 응용 2 : 여러 함수를 조합한 리포트 ─────────────────────────────
   - 제목은 첫 글자만 대문자로 (CONCAT + SUBSTRING + LOWER)
   - 대여료 3단계 분류 (CASE)
   - 하루당 요금 계산 후 소수 2자리 반올림 (ROUND)
   ------------------------------------------------------------------ */

SELECT
    CONCAT(UPPER(SUBSTRING(title, 1, 1)),
           LOWER(SUBSTRING(title, 2)))          AS 영화제목,
    rental_rate                                 AS 대여료,
    CASE
        WHEN rental_rate >= 4.0 THEN '프리미엄'
        WHEN rental_rate >= 2.0 THEN '스탠다드'
        ELSE '이코노미'
    END                                         AS 요금등급,
    ROUND(rental_rate / rental_duration, 2)     AS 하루요금
FROM film
ORDER BY 하루요금 DESC
LIMIT 10;

-- SUBSTRING(title, 2) : 길이를 생략하면 2번째 글자부터 끝까지
