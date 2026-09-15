---
day: 008
date: 2026-09-15
weekday: 화
week: 3
phase: 프로그래밍과 데이터 기초
title: SQL 기초 — DDL · 제약조건 · CRUD, 그리고 SELECT 조회 문법
tags: sql, mysql, workbench, DDL, DML, CREATE DATABASE, CREATE TABLE, INT, DECIMAL, VARCHAR, DATETIME, PRIMARY KEY, NOT NULL, AUTO_INCREMENT, FOREIGN KEY, INSERT, SELECT, UPDATE, DELETE, safe mode, WHERE, AND, OR, NOT, BETWEEN, IN, LIKE, 와일드카드, ORDER BY, LIMIT, world
---

# Day 008 · 2026-09-15 (화)

`프로그래밍과 데이터 기초` · 3주차

> **한 줄 요약** — MySQL Workbench로 DB와 테이블을 직접 만들고(DDL), 제약조건으로 데이터 규칙을 건 뒤 CRUD로 데이터를 넣고 고치고 지웠으며, `world` 샘플 DB로 `WHERE` · `BETWEEN` · `IN` · `LIKE` · `ORDER BY` · `LIMIT` 조회 문법까지 훑었다.

📂 실습 코드 → [`lecture/`](./lecture/) (교재 p.19 ~ p.56, 주제별 `.sql` 9개 + 요약 치트시트)

---

## 0. SQL 명령어의 두 갈래

오늘 배운 명령어는 **무엇을 다루는가**로 나뉜다. 이 구분을 잡고 가면 나머지가 정리된다.

| 구분 | 다루는 것 | 명령어 |
|------|-----------|--------|
| **DDL** (Data Definition Language) | **구조** — DB, 테이블, 컬럼 | `CREATE` `DROP` `DESCRIBE` `SHOW` |
| **DML** (Data Manipulation Language) | **데이터** — 행(Row) | `INSERT` `SELECT` `UPDATE` `DELETE` |

---

## 1. 데이터베이스 생성 · 삭제 — `01_데이터베이스_생성삭제.sql`

```sql
SHOW DATABASES;            -- 현재 DB 목록 확인
CREATE DATABASE testdb;    -- 생성
DROP   DATABASE testdb;    -- 삭제 (안의 테이블·데이터가 전부 함께 사라진다)
```

`IF NOT EXISTS` / `IF EXISTS` 를 붙이면 이미 있거나 없는 경우에도 에러 없이 넘어간다. 스크립트를 **여러 번 반복 실행**할 때 유용하다.

```sql
CREATE DATABASE IF NOT EXISTS testdb;
DROP   DATABASE IF EXISTS     testdb;
```

---

## 2. 데이터 유형과 테이블 생성 · 삭제 — `02_데이터유형_테이블생성삭제.sql`

테이블을 만들려면 **컬럼마다 어떤 종류의 값이 들어올지(자료형)** 를 먼저 정해야 한다.

| 유형 | 저장하는 값 | 형식 · 범위 | 주 사용처 |
|------|------------|------------|-----------|
| `INT` | 정수 | -2,147,483,648 ~ 2,147,483,647 | 고유 ID, 수량, 횟수 |
| `DECIMAL(p, s)` | 정밀 십진수 | (전체 자리수, 소수점 이하 자리수) | 가격, 금액, 세율 |
| `VARCHAR(n)` | 가변 길이 문자열 | 최대 n자, 실제 길이만큼만 공간 사용 | 이름, 제목, 주소 |
| `DATETIME` | 날짜 + 시간 | `YYYY-MM-DD HH:MM:SS` | 생성·수정 시간 |

```sql
USE testdb;                -- 이후 모든 명령은 testdb를 대상으로 실행된다

CREATE TABLE test_table (
    col1 INT,
    col2 VARCHAR(50),
    col3 DATETIME
);

SHOW TABLES;               -- 테이블 목록 확인
DROP TABLE test_table;     -- 테이블 삭제
```

⚠️ `USE` 를 빠뜨리면 *"No database selected"* 에러가 난다. **DB를 먼저 고르고 테이블을 다룬다.**

---

## 3. 제약조건 — `03_제약조건.sql`

컬럼에 거는 **데이터 규칙**이다. 잘못된 데이터가 애초에 들어오지 못하게 막아 **무결성(Integrity)** 을 지킨다.

| 제약조건 | 뜻 | 규칙 |
|------|-----|------|
| `PRIMARY KEY` | 각 행을 **유일하게 식별**하는 컬럼 | 테이블당 **1개**, Unique + NOT NULL 자동 보유 |
| `NOT NULL` | NULL(누락) 입력 금지 | 필수 입력값에 건다 |
| `AUTO_INCREMENT` | 새 행마다 번호를 **1씩 자동 증가** | **INT 컬럼에만**, 테이블당 1개, 주로 PK에 |
| `FOREIGN KEY` | 다른 테이블의 **PK를 참조** | 부모-자식 관계 형성, 참조 무결성 보장 |

```sql
CREATE TABLE users (
    user_id  INT PRIMARY KEY AUTO_INCREMENT,   -- 1, 2, 3 … 자동 부여
    username VARCHAR(50) NOT NULL,             -- 필수 입력
    email    VARCHAR(100)                      -- NULL 허용
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id  INT,                                     -- 부모(users)의 PK를 참조
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

**참조 무결성** — *"자식 테이블에 들어가는 값은 반드시 부모 테이블 PK에 **실제로 존재하는 값**이어야 한다"* 고 DB가 보증하는 것. 그래서 지울 때도 순서가 있다 — **자식(`orders`)을 먼저 지워야 부모(`users`)를 지울 수 있다.**

```sql
DESCRIBE test_table;   -- 컬럼명 / 타입 / NULL 허용 / 키 / 기본값 한눈에 확인
```

---

## 4. CRUD — `04_CRUD_INSERT_SELECT_UPDATE_DELETE.sql`

| | 명령 | 문법 |
|---|------|------|
| **C** | `INSERT` | `INSERT INTO 테이블 (컬럼…) VALUES (값…);` |
| **R** | `SELECT` | `SELECT 컬럼… FROM 테이블;` · `SELECT * FROM 테이블;` |
| **U** | `UPDATE` | `UPDATE 테이블 SET 컬럼 = 값 WHERE 조건;` |
| **D** | `DELETE` | `DELETE FROM 테이블 WHERE 조건;` |

```sql
-- AUTO_INCREMENT 컬럼(col1)은 생략 → 자동으로 1, 2, 3 부여
INSERT INTO test_table (col2, col3) VALUES ('데이터입력1', '2025-01-01');

-- 다중 행 입력 : VALUES 뒤를 콤마로 이어 쓴다
INSERT INTO test_table (col2, col3) VALUES
    ('데이터입력2', '2025-01-02'),
    ('데이터입력3', '2025-01-03');

UPDATE test_table SET col2 = '데이터 수정' WHERE col1 = 3;
DELETE FROM test_table WHERE col1 = 2;
```

⚠️ **Safe Mode** — Workbench는 `WHERE` 없이, 또는 **PK가 아닌 조건**으로 `UPDATE` / `DELETE` 하는 것을 기본적으로 막는다. 실수로 전체 데이터를 날리는 사고를 막는 안전장치다.

```sql
SET sql_safe_updates = 0;   -- 해제
```

⚠️ `WHERE` 없는 `DELETE FROM 테이블;` 은 **테이블 구조는 남고 데이터만 전부** 사라진다. `DROP TABLE`(구조까지 삭제)과 헷갈리지 말 것.

---

## 5. SELECT 기본 구조 · `world` 샘플 DB — `06_SELECT기본_world샘플DB.sql`

여기서부터는 Workbench에 미리 설치된 **`world` 샘플 DB**로 조회 연습을 한다.

| 테이블 | 담긴 정보 |
|--------|-----------|
| `country` | 세계 각국 정보 (국가코드, 국가명, 대륙, 인구, GDP …) |
| `city` | 세계 주요 도시 정보 (도시ID, 도시명, 국가코드, 인구) |
| `countrylanguage` | 국가별 사용 언어 정보 |

```sql
USE world;

SELECT * FROM country;                          -- 전체 컬럼 (*)
SELECT Name, Continent, Population FROM country; -- 필요한 컬럼만
```

`*` 은 편하지만, 실무에서는 **필요한 컬럼만 지정**하는 편이 성능·가독성에 유리하다.

---

## 6. WHERE 조건절 — `07_WHERE_조건절과_연산자.sql`

전체 데이터 중 **조건에 맞는 행(Row)만 필터링**한다.

| 종류 | 연산자 |
|------|--------|
| 비교 | `=` `!=` `>` `<` `>=` `<=` |
| 논리 | `AND`(둘 다 참) · `OR`(하나라도 참) · `NOT`(부정) |

```sql
-- 대륙이 Asia 이면서 인구 5,000만 이상
SELECT Name, Continent, Population
FROM country
WHERE Continent = 'Asia' AND Population >= 50000000;
```

문자열 비교는 **작은따옴표**로 감싼다. 파이썬과 달리 SQL에서 `=` 는 **비교** 연산자다(대입이 아니다).

---

## 7. 범위 · 목록 · 패턴 검색 — `08_BETWEEN_IN_LIKE.sql`

| 연산자 | 쓰임 |
|--------|------|
| `BETWEEN A AND B` | 연속된 **범위** (A 이상 B 이하, **경계값 포함**) |
| `IN (값1, 값2 …)` | 지정한 **목록** 중 하나라도 일치 (`OR` 반복을 대체) |
| `LIKE '패턴'` | 문자열 **부분 일치** 패턴 검색 |

**와일드카드** — 정확히 일치하지 않는 검색을 위해 `LIKE` 와 함께 쓰는 특수 문자.

| 기호 | 규칙 | 예 |
|------|------|-----|
| `%` | 글자 수 **제한 없이** 어떤 문자가 와도 허용 | `'김%'` 김철수·김민준 / `'%김%'` 서울김치 / `'%김'` 허균김 |
| `_` | 언더바 **개수만큼 글자 자리를 강제** | `'김_'` 김민·김수(2글자, 김철수는 ✕) / `'김__'` 김철수(3글자) |

```sql
SELECT Name, Population FROM country
WHERE Population BETWEEN 10000000 AND 20000000;

SELECT Name, Continent FROM country
WHERE Continent IN ('Asia', 'Europe', 'North America');

SELECT Name FROM country
WHERE Name LIKE 'South%';
```

---

## 8. 정렬과 개수 제한 — `09_ORDER_BY_LIMIT.sql`

| 절 | 쓰임 |
|----|------|
| `ORDER BY 컬럼 ASC\|DESC` | 정렬 (`ASC` 오름차순이 **기본값**, 생략 가능) |
| `LIMIT n` | 출력 개수 제한 (Top-N 추출) |

```sql
-- 인구 상위 5개 국가
SELECT Name, Continent, Population
FROM country
ORDER BY Population DESC
LIMIT 5;
```

**작성 순서는 고정이다.** 바꾸면 문법 에러가 나므로 흐름째로 외운다.

```text
SELECT  →  FROM  →  WHERE  →  ORDER BY  →  LIMIT
```

📄 오늘 명령어 전체 요약 → [`lecture/10_명령어_요약정리.sql`](./lecture/10_명령어_요약정리.sql) (시험 대비용 치트시트)

---

## 🔁 복습

**다시 정리한 것**
- [x] 명령어를 **DDL(구조) / DML(데이터)** 두 갈래로 먼저 나눠 놓으니 나머지가 제자리를 찾았다
- [x] `DROP TABLE`(구조까지 삭제) vs `DELETE FROM`(데이터만 삭제) — 이름이 비슷해 헷갈리던 것
- [x] `PRIMARY KEY` 는 `UNIQUE` + `NOT NULL` 을 **이미 포함**한다. 따로 또 적을 필요 없음
- [x] `AUTO_INCREMENT` 제약 — **INT 컬럼에만**, **테이블당 1개**
- [x] FK가 걸린 테이블은 **자식 → 부모** 순서로 지워야 한다 (`orders` 먼저, `users` 나중)
- [x] Safe Mode 에러는 문법 오류가 아니라 **Workbench의 안전장치**. `SET sql_safe_updates = 0;`
- [x] `INSERT` 시 `AUTO_INCREMENT` 컬럼은 컬럼 목록에서 **빼는 것이 정석**
- [x] `%` 와 `_` 의 차이 — `_` 는 **글자 수까지 강제**한다는 점을 예시로 다시 정리
- [x] 절 작성 순서 `SELECT → FROM → WHERE → ORDER BY → LIMIT` 를 통째로 암기

**막혔던 부분 / 질문**
- [ ] `VARCHAR` vs `CHAR` — 가변/고정 차이인데 실제로 언제 `CHAR` 를 쓰는지
- [ ] `DECIMAL` 을 두고 `FLOAT` 를 쓰면 금액에서 정확히 무엇이 틀어지는지
- [ ] `DELETE` 후에도 `AUTO_INCREMENT` 번호는 이어지는데, 번호를 되돌리는 방법이 있는지
- [ ] FK 설정 시 `ON DELETE CASCADE` 같은 옵션은 어떤 상황에서 쓰는지
- [ ] `NULL` 은 `= NULL` 로 못 찾고 `IS NULL` 을 쓴다던데, 왜 비교 연산자가 안 먹는지
- [ ] `LIKE '%김%'` 처럼 앞에 `%` 가 붙으면 느려진다는데 그 이유(인덱스와의 관계)
- [ ] 어제 배운 Streamlit 화면에 이 조회 결과를 어떻게 연결하는지 (파이썬 ↔ DB 연동)

**직접 해본 것**
- [x] 교재 p.19 ~ p.56 실습을 주제별 `.sql` 파일로 나눠 정리하고 `lecture/` 에 업로드
- [x] 파일 상단에 **교재 페이지 · 선행 조건**을 적어 순서대로 실행하면 재현되도록 구성
- [ ] `world` DB의 `city` · `countrylanguage` 테이블로 같은 조회 문법 응용해 보기
- [ ] 어제 만든 Streamlit 대시보드에 DB 조회 결과 붙여 보기

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [데이터 유형 — Data Types](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)
- [SELECT 구문](https://dev.mysql.com/doc/refman/8.0/en/select.html)
- [패턴 매칭 (LIKE, 와일드카드)](https://dev.mysql.com/doc/refman/8.0/en/pattern-matching.html)
- [world 샘플 데이터베이스](https://dev.mysql.com/doc/world-setup/en/)
