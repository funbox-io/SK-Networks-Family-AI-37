/* ===================================================================
   [07] MySQL 주요 데이터 타입 세부 정리
   교재 : p.78
   선행 : testdb
   -------------------------------------------------------------------
   분류        데이터 타입                        설명 및 범위
   정수형      TINYINT, SMALLINT, INT, BIGINT    INT    (4 Byte, 약 -21억 ~ 21억)
                                                 BIGINT (8 Byte, 대용량 ID / 금액)
   실수형      FLOAT, DOUBLE, DECIMAL            DECIMAL(P, S) : 오차 없는 정확한 실수
   문자형      CHAR(N), VARCHAR(N),              CHAR (고정 길이), VARCHAR (가변 길이)
               TEXT, LONGTEXT                    LONGTEXT (최대 4GB 대용량 텍스트)
   날짜/시간형 DATE, TIME, DATETIME              DATE (YYYY-MM-DD)
                                                 DATETIME (시분초 포함)
   =================================================================== */

USE testdb;


/* ── 1. 정수형 크기 비교 ─────────────────────────────────────────────
   TINYINT   1 Byte   -128 ~ 127                  (나이, 상태코드, 0/1 플래그)
   SMALLINT  2 Byte   -32,768 ~ 32,767
   INT       4 Byte   약 -21억 ~ 21억             (일반 ID, 수량)
   BIGINT    8 Byte   약 ±922경                   (대용량 로그 ID, 큰 금액)
   → 값 범위에 맞는 가장 작은 타입을 고르면 저장 공간이 절약된다
   ------------------------------------------------------------------ */


/* ── 2. 타입을 골고루 쓴 예시 테이블 ─────────────────────────────── */

DROP TABLE IF EXISTS type_sample;

CREATE TABLE type_sample (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,  -- 대용량 ID
    age        TINYINT,                            -- 0 ~ 127 이면 충분
    price      DECIMAL(10, 2),                     -- 금액 : 오차 없이 소수 2자리
    rate       FLOAT,                              -- 근사값 (과학 계산, 센서 값 등)
    country_cd CHAR(3),                            -- 항상 3글자 → 고정 길이
    name       VARCHAR(50),                        -- 길이가 제각각 → 가변 길이
    memo       TEXT,                               -- 긴 본문
    birth      DATE,                               -- 날짜만
    created_at DATETIME                            -- 날짜 + 시분초
);

INSERT INTO type_sample (age, price, rate, country_cd, name, memo, birth, created_at)
VALUES (27, 19900.50, 0.1, 'KOR', '김철수', '긴 메모 …', '1999-03-15', NOW());

SELECT * FROM type_sample;
DESCRIBE type_sample;


/* ── 3. 범위를 넘으면? ───────────────────────────────────────────────
   -- ✕ TINYINT 최대값(127) 초과 → Error 1264 : Out of range value
   INSERT INTO type_sample (age) VALUES (200);
   ------------------------------------------------------------------ */


/* ── 4. FLOAT vs DECIMAL — 왜 금액은 DECIMAL 인가 ────────────────────
   FLOAT/DOUBLE 은 2진수 근사값이라 0.1 같은 수를 정확히 담지 못한다.
   합계를 여러 번 내면 미세한 오차가 쌓일 수 있으므로
   돈 계산처럼 1원도 틀리면 안 되는 값은 DECIMAL 을 쓴다.
   ------------------------------------------------------------------ */

SELECT
    0.1 + 0.2                                 AS DECIMAL연산,   -- 0.3 (정확)
    CAST(0.1 AS DOUBLE) + CAST(0.2 AS DOUBLE) AS DOUBLE연산;    -- 0.30000000000000004
