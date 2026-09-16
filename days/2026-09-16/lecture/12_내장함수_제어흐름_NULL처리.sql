/* ===================================================================
   [12] 주요 내장 함수 ③ : 제어 흐름 및 NULL 처리 함수
   교재 : p.93 ~ p.98
   선행 : world 샘플 DB
   -------------------------------------------------------------------
   IF(조건식, 참일 때 값, 거짓일 때 값)
     - 조건이 TRUE 면 두 번째 값, FALSE 또는 NULL 이면 세 번째 값
     - 합격/불합격처럼 '둘 중 하나'로 나눌 때

   IFNULL(검사할 값, 대체 값)
     - 값이 NULL 이 아니면 그대로, NULL 이면 대체 값 반환
     - 숫자 + NULL = NULL 같은 계산 오류 방지에 필수

   CASE (다중 조건문)
     CASE
         WHEN 조건식1 THEN 결과1
         WHEN 조건식2 THEN 결과2
         ELSE 기본값
     END
     ① WHEN 은 위에서부터 순서대로 평가, 처음 참이 되는 THEN 을 반환하고 종료
     ② ELSE 생략 시 아무 조건도 안 맞으면 NULL → ELSE 는 명시할 것
     ③ 끝에 END 필수
   =================================================================== */

USE world;


/* ── 1. IF 및 IFNULL 활용 (p.95, p.97) ────────────────────────────── */

SELECT
    Name,
    LifeExpectancy,
    IF(LifeExpectancy >= 75, '장수국가', '일반국가') AS 국가분류,
    IFNULL(GNPOld, 0)                                AS 이전GNP
FROM country
LIMIT 5;

-- ※ LifeExpectancy 가 NULL 이면 조건 결과도 NULL → '일반국가' 로 분류된다
--   (Antarctica 등). NULL 을 따로 구분하려면 CASE 로 먼저 걸러야 함


/* ── 2. CASE WHEN 활용 (p.96, p.98) ────────────────────────────────── */

SELECT
    Name,
    Population,
    CASE
        WHEN Population >= 100000000 THEN '초대형 국가'   -- 1억 이상
        WHEN Population >=  30000000 THEN '중대형 국가'   -- 3천만 이상 ~ 1억 미만
        ELSE '소형 국가'
    END AS 인구규모분류
FROM country
LIMIT 5;


/* ── 3. CASE 는 순서가 중요하다 ───────────────────────────────────────
   작은 기준을 먼저 쓰면 1억 넘는 나라도 첫 WHEN 에서 걸려 버린다
   ------------------------------------------------------------------ */

SELECT
    Name,
    Population,
    CASE
        WHEN Population >=  30000000 THEN '중대형 국가'   -- ✕ China 도 여기서 끝
        WHEN Population >= 100000000 THEN '초대형 국가'   -- 절대 도달하지 않음
        ELSE '소형 국가'
    END AS 잘못된분류
FROM country
WHERE Code IN ('CHN', 'KOR', 'ISL');


/* ── 4. IFNULL 이 필요한 이유 : NULL 이 섞인 계산 ──────────────────── */

SELECT
    Name,
    GNP,
    GNPOld,
    GNP - GNPOld            AS 증감_그대로,    -- GNPOld 가 NULL 이면 결과도 NULL
    GNP - IFNULL(GNPOld, 0) AS 증감_IFNULL     -- NULL 을 0 으로 보고 계산
FROM country
WHERE GNPOld IS NULL        -- NULL 은 = 가 아니라 IS NULL 로 찾는다
LIMIT 5;


/* ── 5. 응용 : NULL 까지 구분하는 CASE ────────────────────────────── */

SELECT
    Name,
    LifeExpectancy,
    CASE
        WHEN LifeExpectancy IS NULL THEN '정보없음'
        WHEN LifeExpectancy >= 75   THEN '장수국가'
        ELSE '일반국가'
    END AS 국가분류
FROM country
WHERE Continent = 'Antarctica' OR Code IN ('KOR', 'AFG');


/* ── 6. 응용 : CASE + GROUP BY — 분류별 국가 수 집계 ──────────────── */

SELECT
    CASE
        WHEN Population >= 100000000 THEN '초대형 국가'
        WHEN Population >=  30000000 THEN '중대형 국가'
        ELSE '소형 국가'
    END      AS 인구규모분류,
    COUNT(*) AS 국가수
FROM country
GROUP BY 인구규모분류
ORDER BY 국가수;
