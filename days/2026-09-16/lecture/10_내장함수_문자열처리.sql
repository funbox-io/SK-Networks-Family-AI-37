/* ===================================================================
   [10] 주요 내장 함수 ① : 문자열 처리 함수
   교재 : p.87 ~ p.89
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   함수명                기능
   CONCAT(str1, …)       여러 문자열을 하나로 연결
   SUBSTRING(s, p, l)    문자열 s 의 p 번째 위치부터 l 개만큼 추출
   LENGTH(str)           문자열의 '바이트' 수 (CHAR_LENGTH 는 '글자' 수)
   LOWER() / UPPER()     소문자 / 대문자로 변환
   REPLACE(s, f, t)      문자열 s 안의 f 를 t 로 치환
   =================================================================== */

USE world;


/* ── 1. 실습 스크립트 (p.88 ~ p.89) ───────────────────────────────────
   국가명 + 대륙 결합, 국가명 대문자 변환, 앞 3글자 약어
   ------------------------------------------------------------------ */

SELECT
    CONCAT(Name, ' (', Continent, ')') AS 국가정보,      -- Aruba (North America)
    UPPER(Name)                        AS 대문자국가명,  -- ARUBA
    SUBSTRING(Name, 1, 3)              AS 약어           -- Aru
FROM country
LIMIT 5;

-- ※ SQL 의 문자열 위치는 1 부터 시작 (파이썬 인덱스 0 과 다름)
--   SUBSTRING(Name, 1, 3)  ≒  파이썬 Name[0:3]


/* ── 2. LENGTH vs CHAR_LENGTH — 한글에서 차이가 난다 ──────────────────
   utf8mb4 에서 영문 1글자 = 1 Byte, 한글 1글자 = 3 Byte
   ------------------------------------------------------------------ */

SELECT
    LENGTH('SQL')          AS 영문바이트,   -- 3
    CHAR_LENGTH('SQL')     AS 영문글자수,   -- 3
    LENGTH('김철수')        AS 한글바이트,   -- 9
    CHAR_LENGTH('김철수')   AS 한글글자수;   -- 3

-- → "글자 수 제한" 검사에는 CHAR_LENGTH 를 써야 한다
--   (VARCHAR(n) 의 n 도 바이트가 아니라 글자 수 기준)


/* ── 3. LOWER / REPLACE ───────────────────────────────────────────── */

SELECT
    LOWER(Name)                          AS 소문자,
    REPLACE(Name, ' ', '_')              AS 공백치환,   -- South Korea → South_Korea
    REPLACE(Continent, 'America', 'Am.') AS 대륙약칭
FROM country
WHERE Name LIKE 'South%';


/* ── 4. 응용 : 함수 중첩 ─────────────────────────────────────────────
   국가코드 + 국가명 앞 3글자 대문자 → 'KOR-SOU'
   ------------------------------------------------------------------ */

SELECT
    Name,
    CONCAT(Code, '-', UPPER(SUBSTRING(Name, 1, 3))) AS 식별코드,
    CHAR_LENGTH(Name)                               AS 이름길이
FROM country
ORDER BY 이름길이 DESC
LIMIT 5;


/* ── 참고 : 자주 함께 쓰는 문자열 함수 ─────────────────────────────
   TRIM(s)            앞뒤 공백 제거
   LEFT(s, n)         왼쪽에서 n 글자      RIGHT(s, n)  오른쪽에서 n 글자
   CONCAT_WS(sep, …)  구분자를 끼워 연결    예) CONCAT_WS('-', '2026', '09', '16')
   ------------------------------------------------------------------ */
