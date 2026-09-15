/* ===================================================================
   [03] 주요 제약조건 (PRIMARY KEY / NOT NULL / AUTO_INCREMENT / FK)
   교재 : p.28 ~ p.32
   선행 : 02번 파일 실행 (testdb 존재)
   =================================================================== */

USE testdb;


/* ── 1. PRIMARY KEY & NOT NULL (p.28) ──────────────────────────────
   PRIMARY KEY (기본 키)
     1) 테이블 내의 각 행(Row)을 유일하게 식별하는 컬럼 (테이블당 단 1개)
     2) Unique(중복 불가) + NOT NULL(누락 불가) 특성을 자동 보유
   NOT NULL
     1) 해당 컬럼에 NULL(누락) 상태가 들어오는 것을 금지하는 제약조건
     2) 데이터 누락을 방지하고 데이터 무결성(Integrity)을 보장
   ------------------------------------------------------------------ */
CREATE TABLE users (
    user_id  INT PRIMARY KEY,        -- 기본키 : 중복 X, NULL X
    username VARCHAR(50) NOT NULL,   -- 필수 입력값
    email    VARCHAR(100)            -- NULL 허용
);


/* ── 2. AUTO_INCREMENT (p.29) ──────────────────────────────────────
   1) 주로 PRIMARY KEY 정수형 컬럼(고유 ID)에 사용
   2) 새로운 행이 추가될 때마다 고유한 정수 번호가 1씩 자동 증가하여 할당
   3) 특징
      ① 개발자가 직접 번호를 부여할 필요가 없어 관리가 용이 (고유 ID 자동 생성)
      ② 정수형(INT) 컬럼에만 지정 가능, 테이블당 단 1개 컬럼만 설정 가능
   ------------------------------------------------------------------ */
DROP TABLE users;

CREATE TABLE users (
    user_id  INT PRIMARY KEY AUTO_INCREMENT,   -- 1, 2, 3 … 자동 부여
    username VARCHAR(50) NOT NULL,
    email    VARCHAR(100)
);


/* ── 3. FOREIGN KEY · 외래 키 (p.30) ───────────────────────────────
   1) 한 테이블의 컬럼이 다른 테이블의 PRIMARY KEY 컬럼을 참조하도록
      설정하는 키
   2) 테이블 간의 부모-자식 관계를 형성

   참조 무결성 (Referential Integrity)
     : 부모 테이블에 존재하지 않는 임의의 값을 자식 테이블에 넣을 수 없도록
       엄격히 제한함.
       "자식 테이블의 컬럼에 들어가는 값은 반드시 부모 테이블의 PK에
        실제로 존재하는 값 중에서만 가져오겠다"고 보증하는 행위

   ※ 교재에는 도식만 있어 아래는 개념을 코드로 옮긴 참고 예시
   ------------------------------------------------------------------ */
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id  INT,                                     -- 부모(users)의 PK를 참조
    FOREIGN KEY (user_id) REFERENCES users(user_id)   -- 외래키 설정
);

-- 참고 예시 정리 (다음 실습에 영향 없도록 삭제)
-- ※ 자식(orders)을 먼저 지워야 부모(users)를 지울 수 있음
DROP TABLE orders;
DROP TABLE users;


/* ── 4. 제약조건 종합 적용 테이블 생성 실습 (p.31 ~ p.32) ─────────── */
USE testdb;

-- 기존 테이블이 있으면 삭제 후, 제약조건이 포함된 테이블 생성
DROP TABLE IF EXISTS test_table;

CREATE TABLE test_table (
    col1 INT PRIMARY KEY AUTO_INCREMENT,   -- 기본키 + 자동 증가
    col2 VARCHAR(50) NOT NULL,             -- 필수 입력
    col3 DATETIME
);

-- 생성된 테이블 목록 및 구조 확인
SHOW TABLES;
DESCRIBE test_table;   -- 컬럼명 / 타입 / NULL 허용 여부 / 키 / 기본값 확인
