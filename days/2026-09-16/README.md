---
day: 009
date: 2026-09-16
weekday: 수
week: 3
phase: 프로그래밍과 데이터 기초
title: SQL 집계와 함수 — GROUP BY · HAVING · 내장 함수, 그리고 JOIN
tags: sql, mysql, world, sakila, COUNT, SUM, AVG, MAX, MIN, GROUP BY, HAVING, INSERT IGNORE, ON DUPLICATE KEY UPDATE, TINYINT, BIGINT, DECIMAL, CHAR, TEXT, 사용자 정의 변수, PREPARE, CAST, CONVERT, 형변환, CONCAT, SUBSTRING, LENGTH, CHAR_LENGTH, REPLACE, NOW, CURDATE, DATEDIFF, DATE_ADD, DATE_FORMAT, IF, IFNULL, CASE WHEN, JOIN, INNER JOIN, LEFT JOIN, RIGHT JOIN
---

# Day 009 · 2026-09-16 (수)

`프로그래밍과 데이터 기초` · 3주차

> **한 줄 요약** — 집계 함수와 `GROUP BY` · `HAVING` 으로 데이터를 요약하고, 형변환 · 문자열 · 날짜 · 제어 흐름 내장 함수로 결과를 가공한 뒤, `JOIN` 으로 나뉜 테이블을 하나로 합쳐 조회했다.

📂 실습 코드 → [`lecture/`](./lecture/) (교재 p.56 ~ p.107, 주제별 `.sql` 15개 + 요약 치트시트)

---

## 0. 오늘 쿼리의 전체 뼈대

어제 `SELECT → FROM → WHERE → ORDER BY → LIMIT` 에 **`JOIN` · `GROUP BY` · `HAVING`** 이 끼어들었다. **적는 순서**와 **DB가 실행하는 순서**가 다르다는 점이 오늘의 핵심이다.

```text
작성 순서 : SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
실행 순서 : FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

`WHERE` 는 `SELECT` 보다 먼저 실행되므로 **SELECT 별칭을 쓸 수 없고**, `ORDER BY` 는 나중이라 별칭을 쓸 수 있다.

---

## 1. world 조건별 실전 조회 — `01_world_조건별_실전조회_실습.sql`

어제 배운 `WHERE` + `AND` + `ORDER BY` 조합 연습.

```sql
-- 한국 도시 중 인구 100만 이상, 인구 내림차순 → 7건 (Seoul, Pusan, Inchon …)
SELECT Name, Population
FROM city
WHERE CountryCode = 'KOR' AND Population >= 1000000
ORDER BY Population DESC;
```

`city` 에는 국가명이 없고 **국가코드만** 있다. 국가명으로 찾으려면 `JOIN` 이 필요하다 (→ 9장).

---

## 2. 집계 함수 — `02_집계함수_COUNT_SUM_AVG_MAX_MIN.sql`

여러 행을 받아 **값 하나**로 요약한다. **NULL은 자동으로 계산에서 빠진다.**

| 함수 | 설명 | NULL 처리 |
|------|------|-----------|
| `COUNT()` | 행 개수 | `COUNT(*)` 는 **포함** / `COUNT(컬럼)` 은 제외 |
| `SUM()` | 합계 | 제외 |
| `AVG()` | 평균 | 제외 |
| `MAX()` / `MIN()` | 최대 / 최소 | 제외 |

```sql
SELECT COUNT(*), COUNT(LifeExpectancy) FROM country;   -- 239 vs 222
```

⚠️ `AVG` 는 NULL을 0으로 치지 않는다. 분모가 `COUNT(*)` 가 아니라 **`COUNT(컬럼)`** 이다.

---

## 3. GROUP BY · HAVING — `03_GROUP_BY_데이터그룹화.sql` · `04_HAVING_vs_WHERE.sql`

`GROUP BY` 는 같은 값끼리 묶어 그룹별로 집계한다. Pandas `groupby` 와 같은 역할이다.

```sql
SELECT Continent AS 대륙, COUNT(*) AS 국가수, SUM(Population) AS 총인구수
FROM country
GROUP BY Continent
HAVING 총인구수 >= 500000000      -- 그룹 결과로 거르기 → Asia, Africa, Europe
ORDER BY 총인구수 DESC;
```

| | `WHERE` | `HAVING` |
|---|---------|----------|
| 거르는 대상 | 개별 **행** | 묶인 **그룹** |
| 실행 시점 | 그룹화 **전** | 그룹화 **후** |
| 집계 함수 | ✕ (Error 1111) | ○ |

⚠️ `SELECT` 에는 **`GROUP BY` 컬럼 + 집계 함수**만 온다. 그룹마다 값이 여러 개인 `Name` 같은 컬럼을 넣으면 `ONLY_FULL_GROUP_BY` 에러가 난다.

---

## 4. 조건부 입력 — `05_조건부입력_INSERT_IGNORE_ON_DUPLICATE_KEY_UPDATE.sql`

PK가 중복될 때의 두 가지 처리 방식.

| 구문 | PK 중복이면 | 용도 |
|------|-------------|------|
| `INSERT IGNORE` | 에러 대신 경고, 해당 행 **Skip** | 중복 데이터 무시 |
| `… ON DUPLICATE KEY UPDATE` | 기존 행을 **UPDATE** | 포인트·수량 누적 (Upsert) |

```sql
-- 1회차: 없으니 INSERT (100) → 2회차: 있으니 UPDATE (200)
INSERT INTO member_point VALUES ('KIM', '김철수', 100)
ON DUPLICATE KEY UPDATE point = point + 100;
```

---

## 5. 데이터 타입 · 사용자 변수 — `07_데이터타입_세부정리.sql` · `08_사용자정의변수.sql`

| 분류 | 타입 | 포인트 |
|------|------|--------|
| 정수 | `TINYINT` `SMALLINT` `INT` `BIGINT` | INT 4B(±21억), BIGINT 8B(대용량 ID·금액) |
| 실수 | `FLOAT` `DOUBLE` `DECIMAL(P,S)` | 금액은 **오차 없는 DECIMAL** |
| 문자 | `CHAR(N)` `VARCHAR(N)` `TEXT` `LONGTEXT` | 고정 / 가변 / 최대 4GB |
| 날짜 | `DATE` `TIME` `DATETIME` | DATETIME은 시분초 포함 |

직접 돌려 보니 `0.1 + 0.2` 는 `0.3` 이지만, `DOUBLE` 로 바꿔 더하면 `0.30000000000000004` 가 나왔다. 금액에 `DECIMAL` 을 쓰는 이유다.

**사용자 정의 변수** — `SET @변수 = 값;` 으로 만들며 **접속(세션)이 끊기기 전까지** 유지된다.

```sql
SET @target_continent = 'Asia';
SELECT Name FROM country WHERE Continent = @target_continent;
```

⚠️ `LIMIT @n` 은 **문법 에러**다. `PREPARE … EXECUTE … USING @n` 으로 우회해야 한다.

---

## 6. 형변환 — `09_형변환_CAST_CONVERT.sql`

| 구분 | 방식 | 예 |
|------|------|-----|
| 명시적 | `CAST(값 AS 타입)` · `CONVERT(값, 타입)` | `CAST('100' AS SIGNED)` |
| 묵시적 | MySQL이 문맥을 보고 자동 변환 | `'100' + '200'` → `300` |

⚠️ 형변환 함수 안에서는 **전용 타입**만 쓴다: 정수 `SIGNED`(INT ✕), 문자 `CHAR`(VARCHAR ✕), 실수 `DECIMAL`.
⚠️ `CAST(123.5 AS SIGNED)` = **124**. 버림이 아니라 **반올림**이다.
⚠️ SQL의 `+` 는 항상 **숫자 덧셈**이다. 문자열을 이어 붙일 때는 `CONCAT` 을 쓴다.

---

## 7. 내장 함수 — 문자열 · 날짜 — `10_…문자열처리.sql` · `11_…날짜시간처리.sql`

| 문자열 함수 | 기능 | 날짜 함수 | 기능 |
|------|------|------|------|
| `CONCAT(a, b…)` | 연결 | `NOW()` · `SYSDATE()` | 현재 날짜+시간 |
| `SUBSTRING(s, p, l)` | p번째(**1부터**)부터 l글자 | `CURDATE()` · `CURTIME()` | 날짜만 / 시간만 |
| `LENGTH(s)` | **바이트** 수 | `DATEDIFF(d1, d2)` | d1 − d2 일수 |
| `CHAR_LENGTH(s)` | **글자** 수 | `DATE_ADD(d, INTERVAL n 단위)` | 기간 더하기 |
| `UPPER` · `LOWER` | 대 / 소문자 | `DATE_FORMAT(d, fmt)` | `'%Y년 %m월 %d일'` 등 |
| `REPLACE(s, f, t)` | f → t 치환 | | |

```sql
SELECT LENGTH('김철수'), CHAR_LENGTH('김철수');   -- 9, 3 (한글 1자 = 3바이트)
```

---

## 8. 내장 함수 — 제어 흐름 · NULL 처리 — `12_…제어흐름_NULL처리.sql` · `13_…리포트생성_실습.sql`

```sql
SELECT Name,
       IF(LifeExpectancy >= 75, '장수국가', '일반국가') AS 국가분류,
       IFNULL(GNPOld, 0)                                AS 이전GNP,
       CASE
           WHEN Population >= 100000000 THEN '초대형 국가'
           WHEN Population >=  30000000 THEN '중대형 국가'
           ELSE '소형 국가'
       END AS 인구규모분류
FROM country;
```

- `IF` — 조건이 **NULL이면 거짓 값**을 돌려준다. 기대수명이 NULL인 나라도 '일반국가'로 분류된다.
- `IFNULL` — `숫자 + NULL = NULL` 인 계산 오류를 막는다.
- `CASE` — **위에서부터** 평가한다. 작은 기준을 먼저 쓰면 China도 '중대형'에서 끝난다. `ELSE` 를 생략하면 NULL이 나오고, 끝에는 `END` 가 필수다.

---

## 9. JOIN — `14_JOIN_개념_INNER_JOIN.sql` · `15_OUTER_JOIN_LEFT_RIGHT.sql`

중복을 막으려고 나눠 둔 테이블을 **공통 컬럼(PK–FK)** 으로 다시 합친다.

| 종류 | 결과 |
|------|------|
| `INNER JOIN` | 양쪽 모두 있는 행만 (**교집합**) |
| `LEFT JOIN` | 왼쪽 전체 + 매칭 (없으면 **NULL**) |
| `RIGHT JOIN` | 오른쪽 전체 + 매칭 (없으면 NULL) |
| `CROSS JOIN` | 모든 조합 (카테시안 곱) |
| `SELF JOIN` | 자기 자신과 조인 (조직도 등) |

```sql
-- 아시아 도시 인구 Top 5 + 국가명 (Mumbai, Seoul, Shanghai …)
SELECT C.Name AS 도시명, CO.Name AS 국가명, C.Population
FROM city AS C
INNER JOIN country AS CO ON C.CountryCode = CO.Code
WHERE CO.Continent = 'Asia'
ORDER BY C.Population DESC
LIMIT 5;

-- 구매 이력이 없는 회원도 포함 (이영희 → prod_name NULL)
SELECT M.user_id, M.user_name, B.prod_name
FROM j_member M
LEFT JOIN j_buy B ON M.user_id = B.user_id;
```

⚠️ 두 테이블에 같은 이름의 컬럼(`Name`)이 있으면 **`별칭.컬럼`** 으로 구분해야 한다. 안 쓰면 Error 1052 *ambiguous* 가 난다.
💡 `LEFT JOIN … WHERE B.키 IS NULL` 로 **한쪽에만 있는 행(차집합)** 을 찾을 수 있다.

📄 오늘 명령어 전체 요약 → [`lecture/16_명령어_요약정리.sql`](./lecture/16_명령어_요약정리.sql) (시험 대비용 치트시트)

---

## 🔁 복습

**다시 정리한 것**
- [x] **작성 순서 ≠ 실행 순서**. 이것 하나로 "WHERE에서 별칭이 안 되는 이유"가 설명된다
- [x] `COUNT(*)` 는 NULL 포함, `COUNT(컬럼)` 은 NULL 제외. `AVG` 의 분모도 NULL을 뺀 개수다
- [x] 집계 조건이면 `HAVING`, 원본 컬럼 조건이면 `WHERE`. 원본 조건은 WHERE에서 먼저 거르는 편이 유리하다
- [x] `INSERT IGNORE`(Skip) vs `ON DUPLICATE KEY UPDATE`(Upsert)
- [x] `CAST` 안에는 `INT` · `VARCHAR` 대신 `SIGNED` · `CHAR` 를 쓴다
- [x] 실수 → 정수 `CAST` 는 **반올림**이다 (123.5 → 124)
- [x] `LENGTH` 는 바이트, `CHAR_LENGTH` 는 글자 수. 한글에서 3배 차이가 난다
- [x] `IF` 는 조건이 NULL이면 거짓 쪽으로 간다. NULL을 따로 구분하려면 `CASE WHEN … IS NULL` 을 쓴다
- [x] `CASE` 는 **큰 기준부터** 적는다
- [x] NULL은 `= NULL` 이 아니라 `IS NULL` 로 찾는다. NULL과 비교한 결과는 참도 거짓도 아닌 NULL이기 때문이다 (어제 질문 해결)

**막혔던 부분 / 질문**
- [ ] `LIMIT @변수` 가 안 되는 이유와, `PREPARE` 말고 다른 방법이 있는지
- [ ] `NOW()` 와 `SYSDATE()` 의 차이(쿼리 시작 시각 vs 호출 시각)가 실무에서 문제가 되는 경우
- [ ] `FULL OUTER JOIN` 을 MySQL에서는 `UNION` 으로 구현한다는데, 정확한 작성법
- [ ] `SELF JOIN` · `CROSS JOIN` 실습 (교재 p.108 이후로 예상)
- [ ] `JOIN` 할 테이블이 커지면 성능은 어떻게 되는지 (인덱스와의 관계)
- [ ] `HAVING` 에 SELECT 별칭을 쓰는 것은 MySQL 확장 문법이라는데, 다른 DB(PostgreSQL 등)에서는 어떻게 되는지

**직접 해본 것**
- [x] 교재 p.56 ~ p.107 실습을 주제별 `.sql` 파일로 나눠 정리하고 `lecture/` 에 업로드
- [x] 교재 스크립트에 **반복 실행용 초기화**(`DROP TABLE IF EXISTS`)와 **응용 쿼리**(NULL 처리 CASE, 차집합 LEFT JOIN, 3개 테이블 JOIN 등)를 추가
- [x] MySQL 8.0 + `world` · `sakila` 환경에서 16개 파일 전체를 실행해 에러 없음과 주석의 결과값을 확인
- [ ] `sakila` 의 `customer` 와 `payment` 를 JOIN해 고객 **이름**별 총 결제 금액 리포트 만들기
- [ ] Pandas `groupby` · `merge` 로 같은 결과를 내서 SQL과 비교해 보기

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [집계 함수 — Aggregate Functions](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html)
- [GROUP BY 처리 (ONLY_FULL_GROUP_BY)](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)
- [INSERT … ON DUPLICATE KEY UPDATE](https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html)
- [사용자 정의 변수](https://dev.mysql.com/doc/refman/8.0/en/user-variables.html)
- [형변환 — Cast Functions](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html)
- [문자열 함수](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html) · [날짜 · 시간 함수](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html) · [제어 흐름 함수](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html)
- [JOIN 구문](https://dev.mysql.com/doc/refman/8.0/en/join.html)
- [sakila 샘플 데이터베이스](https://dev.mysql.com/doc/sakila/en/)
