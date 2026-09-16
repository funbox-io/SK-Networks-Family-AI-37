/* ===================================================================
   [06] world & sakila 집계 분석 실습
   교재 : p.74 ~ p.77
   선행 : world, sakila 샘플 DB
   -------------------------------------------------------------------
   sakila : MySQL 이 제공하는 DVD 대여점 샘플 DB
            (film 영화, customer 고객, rental 대여, payment 결제 …)
   =================================================================== */


/* ── 문제 1 (p.74 ~ p.76) ─────────────────────────────────────────────
   world.city 에서 국가코드별 도시 개수를 구하고,
   도시가 10개 이상인 국가코드와 도시 수를 도시 수 내림차순으로 조회
   ------------------------------------------------------------------ */

USE world;

SELECT CountryCode, COUNT(*) AS 도시수
FROM city
GROUP BY CountryCode        -- 국가코드별로 묶고
HAVING 도시수 >= 10         -- 집계 결과(도시 수)로 거르므로 HAVING
ORDER BY 도시수 DESC;

-- 결과 : 57건 (CHN 363 → IND 341 → USA 274 …)


/* ── 문제 2 (p.74 ~ p.75, p.77) ───────────────────────────────────────
   sakila.payment 에서 고객(customer_id)별 총 결제 금액(amount)을 구해
   총 결제 금액 내림차순으로 조회
   ------------------------------------------------------------------ */

USE sakila;

SELECT customer_id, SUM(amount) AS 총결제금액
FROM payment
GROUP BY customer_id
ORDER BY 총결제금액 DESC;

-- 결과 : 599건 (1위 customer_id 526 → 221.55)


/* ── 응용 : 문제 2 를 '상위 5명 + 결제 횟수 · 평균 결제액'까지 ────── */

SELECT
    customer_id,
    COUNT(*)              AS 결제횟수,
    SUM(amount)           AS 총결제금액,
    ROUND(AVG(amount), 2) AS 평균결제금액
FROM payment
GROUP BY customer_id
ORDER BY 총결제금액 DESC
LIMIT 5;

-- ※ 고객 '이름'까지 보려면 customer 테이블과 JOIN 필요 (14번 파일)
