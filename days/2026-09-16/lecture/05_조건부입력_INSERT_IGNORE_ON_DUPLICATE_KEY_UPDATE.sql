/* ===================================================================
   [05] 조건부 데이터 입력 및 수정
   교재 : p.71 ~ p.73
   선행 : testdb (Day 008 01번에서 생성, 없으면 아래 CREATE 로 생성)
   -------------------------------------------------------------------
   PK 중복이 발생했을 때
     - 에러를 무시하고 건너뛰고 싶다    → INSERT IGNORE
     - 기존 값을 고치거나 누적하고 싶다  → INSERT … ON DUPLICATE KEY UPDATE

   INSERT IGNORE
     : PK 중복 에러가 나면 에러 대신 경고(Warning)만 남기고 해당 행을 Skip

   ON DUPLICATE KEY UPDATE
     1) PK 가 중복되지 않으면 → 신규 삽입 (INSERT)
     2) PK 가 중복되면       → 지정한 값으로 기존 행 수정 (UPDATE)
   =================================================================== */

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;


/* ── 0. 실습 테이블 준비 (p.72) ───────────────────────────────────── */

-- 반복 실행해도 결과가 같도록 먼저 삭제 후 생성
DROP TABLE IF EXISTS member_point;

CREATE TABLE IF NOT EXISTS member_point (
    user_id   VARCHAR(10) PRIMARY KEY,   -- 중복 판단 기준
    user_name VARCHAR(20),
    point     INT
);


/* ── 1. 일반 INSERT 로 중복 입력 시 → 에러 ───────────────────────── */

INSERT INTO member_point VALUES ('LEE', '이영희', 50);

-- ✕ 아래를 실행하면 Error 1062 : Duplicate entry 'LEE' for key 'PRIMARY'
-- INSERT INTO member_point VALUES ('LEE', '이영희', 999);


/* ── 2. INSERT IGNORE — 중복이면 조용히 건너뜀 (p.71) ───────────────── */

INSERT IGNORE INTO member_point VALUES ('LEE', '이영희', 999);   -- 0 row(s) affected
SHOW WARNINGS;                                                  -- 무시된 중복 경고 확인

SELECT * FROM member_point;   -- LEE 의 point 는 여전히 50


/* ── 3. ON DUPLICATE KEY UPDATE — 없으면 삽입, 있으면 누적 (p.72 ~ p.73) ── */

-- 1회차 : 'KIM' 이 없으므로 INSERT → point = 100
INSERT INTO member_point VALUES ('KIM', '김철수', 100)
ON DUPLICATE KEY UPDATE point = point + 100;

-- 2회차 : 'KIM' 이 이미 있으므로 UPDATE → point = 100 + 100 = 200
INSERT INTO member_point VALUES ('KIM', '김철수', 100)
ON DUPLICATE KEY UPDATE point = point + 100;

SELECT * FROM member_point;   -- KIM 200, LEE 50

-- ※ 이 구문을 한 번 더 실행할 때마다 KIM 의 point 가 100 씩 계속 늘어난다
--   (포인트 적립, 조회수·장바구니 수량 누적 같은 곳에 쓰는 패턴)


/* ── 참고 : 영향받은 행 수(affected rows) 읽는 법 ───────────────────
   ON DUPLICATE KEY UPDATE 실행 결과
     1 row(s) affected  → 새로 INSERT 됨
     2 row(s) affected  → 기존 행이 UPDATE 됨
     0 row(s) affected  → 중복이었지만 값이 이전과 같아 변경 없음
   ------------------------------------------------------------------ */
