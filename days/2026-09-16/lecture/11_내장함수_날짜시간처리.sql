/* ===================================================================
   [11] 주요 내장 함수 ② : 날짜 및 시간 처리 함수
   교재 : p.90 ~ p.92
   선행 : 없음 (sakila 응용 예시는 sakila 샘플 DB 필요)
   -------------------------------------------------------------------
   함수명                        기능
   NOW() / SYSDATE()             현재 날짜 + 시간 (YYYY-MM-DD HH:MM:SS)
   CURDATE() / CURTIME()         현재 날짜만 / 현재 시간만
   DATEDIFF(date1, date2)        두 날짜의 일수 차이 (date1 - date2)
   DATE_ADD(date, INTERVAL …)    날짜에 특정 기간을 더함
   DATE_FORMAT(date, fmt)        날짜를 지정한 형식의 문자열로 변환
   =================================================================== */


/* ── 1. 실습 스크립트 (p.91 ~ p.92) ───────────────────────────────── */

SELECT
    NOW()                                     AS 현재시간,
    DATE_ADD(NOW(), INTERVAL 7 DAY)           AS 일주일후,
    DATEDIFF('2026-12-31', CURDATE())         AS 남은일수,   -- 2026-09-16 기준 106
    DATE_FORMAT(NOW(), '%Y년 %m월 %d일 %H시') AS 포맷변환;   -- 2026년 09월 16일 21시


/* ── 2. CURDATE / CURTIME ─────────────────────────────────────────── */

SELECT CURDATE() AS 오늘날짜, CURTIME() AS 현재시각;


/* ── 3. DATE_ADD · DATE_SUB — INTERVAL 단위 ──────────────────────────
   단위 : SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR
   빼기 : DATE_SUB 를 쓰거나 DATE_ADD 에 음수를 넣는다
   ------------------------------------------------------------------ */

SELECT
    DATE_ADD(CURDATE(), INTERVAL 1 MONTH)  AS 한달후,
    DATE_ADD(CURDATE(), INTERVAL -3 DAY)   AS 사흘전_ADD,
    DATE_SUB(CURDATE(), INTERVAL 3 DAY)    AS 사흘전_SUB,
    DATE_ADD(NOW(), INTERVAL 90 MINUTE)    AS 구십분후;


/* ── 4. DATEDIFF 순서 주의 ────────────────────────────────────────── */

SELECT
    DATEDIFF('2026-12-31', '2026-09-16') AS 앞이미래,   --  106
    DATEDIFF('2026-09-16', '2026-12-31') AS 앞이과거;   -- -106


/* ── 5. DATE_FORMAT 주요 서식 ─────────────────────────────────────────
   %Y 4자리 연도   %y 2자리 연도
   %m 월(01~12)    %d 일(01~31)
   %H 시(00~23)    %i 분(00~59)    %s 초
   %W 요일(영문)   %p AM/PM
   ------------------------------------------------------------------ */

SELECT
    DATE_FORMAT(NOW(), '%Y-%m-%d')          AS 날짜만,
    DATE_FORMAT(NOW(), '%H:%i:%s')          AS 시간만,
    DATE_FORMAT(NOW(), '%y.%m.%d (%W)')     AS 요일포함;


/* ── 6. 응용 : sakila 대여 기간 계산 ─────────────────────────────────
   rental 테이블 : rental_date(대여일), return_date(반납일)
   ------------------------------------------------------------------ */

USE sakila;

SELECT
    rental_id,
    DATE_FORMAT(rental_date, '%Y-%m-%d') AS 대여일,
    DATE_FORMAT(return_date, '%Y-%m-%d') AS 반납일,
    DATEDIFF(return_date, rental_date)   AS 대여일수     -- 미반납이면 NULL
FROM rental
LIMIT 5;


/* ── 참고 : NOW() vs SYSDATE() ──────────────────────────────────────
   NOW()     : 쿼리가 '시작된' 시각으로 고정 (한 쿼리 안에서 여러 번 불러도 같음)
   SYSDATE() : 함수가 '호출되는' 순간의 시각
   SELECT NOW(), SLEEP(2), NOW();          -- 두 값 동일
   SELECT SYSDATE(), SLEEP(2), SYSDATE();  -- 2초 차이
   ------------------------------------------------------------------ */
