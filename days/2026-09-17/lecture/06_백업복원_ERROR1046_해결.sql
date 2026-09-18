/* ===================================================================
   [06] 데이터베이스 백업(Backup)과 복원(Restore) · 복원 에러(ERROR 1046) 해결
   교재 : p.127 ~ p.130
   선행 : testdb 에 실습 테이블이 몇 개 들어 있는 상태
   -------------------------------------------------------------------
   백업과 복원의 필요성
     : 시스템 장애, 악성코드 감염, 개발자의 실수로 인한 데이터 삭제 시 원상 복구를 위해 필수

   백업의 종류
     1) 논리적 백업 (SQL Dump)     : DB 의 구조(DDL)와 데이터(DML)를 .sql 텍스트 파일로 저장 ← 본 실습
     2) 물리적 백업 (Physical)     : DB 가 실제 저장되는 디스크 파일(Data File, Log File)을 그대로 복사

   MySQL Workbench 도구 : 상단 메뉴 Server → Data Export(백업) / Data Import(복원)
   =================================================================== */


/* ── 1. 데이터 백업 (Data Export) 단계 — Workbench GUI (p.128) ────────
   1) Workbench 상단 메뉴 Server → Data Export
   2) 좌측 Tables to Export 패널에서 백업 대상 DB(testdb) 체크
   3) Export Options
        ① Export to Self-Contained File 선택
        ② 저장 경로 지정 (예: C:\Users\User\public\testdb_dump.sql)
   4) 우측 하단 Start Export → Export Completed 확인
   ------------------------------------------------------------------ */

-- 백업 전에 무엇이 들어 있는지 확인해 두면, 복원 후 비교할 수 있다
USE testdb;
SHOW TABLES;
SELECT COUNT(*) AS emp_tree_rows  FROM emp_tree;
SELECT COUNT(*) AS real_user_rows FROM real_user;


/* ── 2. 데이터 복원 (Data Import) 단계 — Workbench GUI (p.128) ────────
   1) 복원 테스트를 위해 기존 testdb 삭제
   2) Workbench 상단 메뉴 Server → Data Import
   3) Import from Self-Contained File 선택 → 저장했던 testdb_dump.sql 지정
   4) 우측 하단 Start Import
   ------------------------------------------------------------------ */

-- 1) 복원 테스트용 삭제  ★ 백업(Export Completed)을 확인한 뒤에만 실행할 것
-- DROP DATABASE testdb;


/* ── 3. 복원 에러 ERROR 1046 분석 및 해결 (p.129 ~ p.130) ────────────
   대표 에러 현상
     ERROR 1046 (3D000) at line 22: No database selected
     Operation failed with exitcode 1

   원인
     1) 백업 파일(testdb_dump.sql) 안에 CREATE DATABASE 또는 USE 구문이 생략되어 있을 때 발생
     2) 복원 시 MySQL 서버가 "이 테이블과 데이터를 어느 DB 에 넣어야 하는가?" 를 알지 못해 중단

   해결 — 가장 확실한 대안 2가지 (선택 적용)
     대안 ① GUI 방식 (가장 추천)
        ① Data Import 화면 중간의 Default Target Schema 드롭다운 클릭
        ② 복원될 대상 DB 선택 (없다면 New… 버튼으로 testdb 생성 후 선택)
        ③ Start Import → 에러 없이 복원 완료
     대안 ② SQL 파일 수정 방식
        ① 백업된 .sql 파일을 메모장으로 열고 최상단 첫 줄에 아래 두 줄을 추가 후 저장
        ② 다시 Import
   ------------------------------------------------------------------ */

-- 대안 ② 에서 덤프 파일 첫 줄에 추가할 코드 (이 두 줄이 "어느 DB 에 넣을지" 를 알려준다)
CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;


/* ── 4. 복원 확인 ─────────────────────────────────────────────────── */
SHOW DATABASES;               -- testdb 가 다시 보이는지
USE testdb;
SHOW TABLES;                  -- 백업 전 목록과 같은지
SELECT * FROM emp_tree;


/* ── 참고 : 터미널(CLI) 로 같은 작업 하기 ─────────────────────────────
   Workbench 의 Data Export / Import 는 내부적으로 아래 명령을 대신 실행해 준다.
   (SQL 이 아니라 터미널 명령이므로 Workbench 쿼리창에서는 실행되지 않는다)

   백업 :  mysqldump -u root -p --databases testdb > testdb_dump.sql
           ※ --databases 를 붙이면 덤프 파일에 CREATE DATABASE / USE 가 자동으로 들어가
              ERROR 1046 이 원천적으로 생기지 않는다
   복원 :  mysql -u root -p < testdb_dump.sql
   ------------------------------------------------------------------ */
