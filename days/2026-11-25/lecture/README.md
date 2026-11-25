# 2026-11-25 수업 실습 — LLM 10일차 : 체크포인팅(AsyncSqliteSaver · AIOMySQLSaver · thread_id) · 조건부 분기 + 비동기 + 체크포인팅 RAG 챗봇

| 파일 | 내용 |
|---|---|
| `LangGraph_실습6.ipynb` | 수업 필기 원본 — 멀티 에이전트 RAG 챗봇(비동기)에 **`AsyncSqliteSaver` 체크포인터**를 붙인 완성 · 실행본 (2턴 대화) |
| `LangGraph_실습7.ipynb` | 수업 필기 원본 — 같은 챗봇을 **MySQL `AIOMySQLSaver`** 로 (aiomysql 오류 방지 패치 포함 · 실행 출력 없음). **DB 비밀번호 부분만 `****` 로 가렸다** |
| `LangGraph_실습8.ipynb` | 수업 필기 원본 — **조건부 분기 + 비동기 + 체크포인팅**. 체인 4개 · 상태 · 분류 노드까지, 검색 노드 중간에서 멈춤 |
| `faq_manual.csv` | 실습 데이터 (Day 053 과 같은 FAQ 10개) |
| [`chroma_db_multi/`](./chroma_db_multi/) | 수업 벡터 저장소 — `chroma.sqlite3` + HNSW 색인 폴더 (OpenAI `text-embedding-3-small` 1536차원 · 10개). 0바이트 `link_lists.bin` 은 GitHub 웹 업로드가 받지 않아 빠짐 (없어도 읽기 · 검색됨) |
| [`langgraph_checkpoint_sqlite.ipynb`](./langgraph_checkpoint_sqlite.ipynb) | 교재 p.130~137 · 필기 `실습6` — 용어 → 작은 그래프로 저장 · 복원 · 체크포인트 목록 → `thread_id` 분리 · config 없음 · `async with` 밖 · 다시 켜기 → **리듀서 없는 항목이 남는 문제** → 오류 뒤 이어 가기 → 핵심 변화 3가지를 RAG 챗봇에 → 📼 수업 실행 → 부록 : `chroma_db_multi` 구조 |
| [`langgraph_checkpoint_mysql.ipynb`](./langgraph_checkpoint_mysql.ipynb) | 필기 `실습7` — **aiomysql 패치가 왜 필요한지 재현** → 접속 정보를 `.env` 로 → `AIOMySQLSaver` + `setup()` 으로 2턴 · 테이블 확인 → 패치 없이 실행하면 → SQLite vs MySQL 표 |
| [`langgraph_rag_router_async_checkpoint.ipynb`](./langgraph_rag_router_async_checkpoint.ipynb) | 필기 `실습8` 완성 — 체인 4개 → 분류(대화 기록 포함) · 검색(재구성) · 매뉴얼 답변 · 일반 답변 노드 → 조건부 그래프 → 한 대화방 4턴 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (실제로 체크포인터를 돌린 기록으로 그림) |

교재 PDF · `.env` · 실행하며 생기는 체크포인트 DB(`*.sqlite`)는 올리지 않았다.

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 옮긴 출력 (`실습6` 2턴 대화) |
| `# ⏳` | OpenAI 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (`input()` 대화 루프 포함) |
| `# 🧪` | OpenAI 대신 **로컬 임베딩**(`jhgan/ko-sroberta-multitask`) · **가짜 LLM**(규칙 분류 · 앞 질문 이어 붙이기 재구성)으로 실제로 돌린 셀 — 체크포인트 저장 · 복원 · 오류는 진짜와 같다 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 — **MySQL 노트는 정리 환경에 MariaDB 10.11 서버를 띄워 실제로 실행** |

## 실행 방법
1. **SQLite 체크포인터** : `pip install langgraph-checkpoint-sqlite aiosqlite` (+ Day 053~054 패키지)
2. **MySQL 체크포인터** : MySQL(또는 MariaDB) 실행 → `CREATE DATABASE langgraph_db;` → `pip install langgraph-checkpoint-mysql aiomysql` → `.env` 에 `MYSQL_USER` · `MYSQL_PASSWORD` · `MYSQL_HOST` · `MYSQL_PORT` · `MYSQL_DB`
3. 같은 폴더에 `faq_manual.csv` · `.env`(`OPENAI_API_KEY`) — 키가 있으면 `# ⏳`, 없으면 `# 🧪` 셀
4. 정리 환경 : `langgraph 1.2.21` · `langgraph-checkpoint 4.3.1` · `langgraph-checkpoint-sqlite 3.1.3` · `aiosqlite 0.22.1` · `langgraph-checkpoint-mysql 3.0.0` · `aiomysql 0.3.2` · `PyMySQL 1.2.4`

## 결과 요약
| 실습 | 결과 |
|---|---|
| 2턴째에 새 질문만 넣기 | 노드가 받은 messages 3개 — 체크포인터가 1턴 기록을 복원해 합침 |
| 체크포인트 수 | 한 턴에 4개 (입력 · 시작 · 노드 a 직후 · 노드 b 직후) — 2턴 8개 |
| 다른 `thread_id` | 기록이 섞이지 않음 |
| config 없이 `ainvoke` | `ValueError: Checkpointer requires … thread_id …` |
| `async with` 블록 밖에서 사용 | `ValueError: no active connection` |
| 다시 연결 | 파일의 기록에 이어서 계속 (같은 thread_id) |
| 리듀서 없는 `context` | 노드가 안 쓰면 **앞 턴 값이 남음** → 분류 노드가 매 턴 `''` 로 비우도록 고침 |
| 노드 오류 뒤 `ainvoke(None, config)` | 실패한 노드부터 이어서 성공 (앞 노드 다시 안 함) |
| aiomysql 패치 | PyMySQL 의 `escape_bytes_prefixed` 가 문자열 `'DO NOT IMPORT THIS!!!'` → 패치 없으면 첫 저장에서 `TypeError: 'str' object is not callable` · 패치 후 `X'…'` 로 저장 |
| MySQL 테이블 | `checkpoints` · `checkpoint_blobs` · `checkpoint_writes` · `checkpoint_migrations` (SQLite 는 `checkpoints` · `writes`) |
| `실습8` 4턴 | 안녕(일반) → 환불(검색 FAQ-002) → 그거 전액(재구성 → FAQ-002) → 고마워(일반 · context 0자) |
| `실습6` 수업 기록 | 2턴 '그거 전액 …' → '수강 신청한 강의를 전액 환불받으려면 어떤 조건이 필요하나요?' 로 재구성 → 조건 2가지 FAQ 와 일치 |
| `chroma_db_multi` | 10개 · 1536차원 · 환불 벡터의 이웃 : 수료증(0.899) · 수강 기간(1.094) |
