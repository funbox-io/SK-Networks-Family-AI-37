# 2026-11-26 수업 실습 — LLM 11일차 : 수업 흐름도(RAG.png)대로 `실습8` 완성 · 하나의 answer_node · 비동기 · 체크포인팅

오늘 받은 필기 3개(`실습6_1` · `실습7` · `실습8`)는 **Day 055 에 올린 파일과 바이트 단위로 같다**. 그래서 이 노트들의 정리는 [Day 055 수업 자료](../../2026-11-25/lecture/)를 보면 되고, 여기서는 새로 받은 **흐름도 `RAG.png` 의 설계를 그대로 코드로 옮겨** 실행 · 비교했다.

| 파일 | 내용 |
|---|---|
| [`langgraph_rag_flowchart_single_answer.ipynb`](./langgraph_rag_flowchart_single_answer.ipynb) | 교재 p.138 · 흐름도 `RAG.png` 구현 — 상태 · 노드(분류 · 검색 · **하나의 `answer_node`**) → `exit` 까지 대화 루프 · 턴마다 체크포인트 수 → 블록 밖 · 다시 연결 → 기록이 길어지는 문제 → 답변 노드 1개 vs 2개(Day 055) 비교 |
| `RAG.png` | 수업 흐름도 원본 (입력 → exit 판단 → 1. 상태 복원 → 2. 비동기 워크플로우 → 3. 상태 저장 → 출력) |
| `LangGraph_실습6_1.ipynb` | 수업 필기 원본 — Day 055 `LangGraph_실습6.ipynb` 와 같음 (`AsyncSqliteSaver` 체크포인터 · 2턴 실행본) |
| `LangGraph_실습7.ipynb` | 수업 필기 원본 — Day 055 와 같음 (MySQL `AIOMySQLSaver`). **DB 비밀번호 부분만 `****` 로 가렸다** |
| `LangGraph_실습8.ipynb` | 수업 필기 원본 — Day 055 와 같음 (조건부 분기 + 비동기 + 체크포인팅 · 검색 노드에서 멈춤) |
| `faq_manual.csv` | 실습 데이터 (Day 053 과 같은 FAQ 10개) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (정리 노트를 실제로 실행한 출력으로 그림) |

교재 PDF · `.env` · 실행하며 생기는 체크포인트 DB(`*.sqlite`)는 올리지 않았다.

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# ⏳` | OpenAI 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (`input()` 대화 루프 포함) |
| `# 🧪` | OpenAI 대신 **로컬 임베딩**(`jhgan/ko-sroberta-multitask`) · **가짜 LLM**(규칙 분류 · 앞 질문 이어 붙이기 재구성 · 고정 답변)으로 실제로 돌린 셀 — 그래프 경로 · 체크포인트 저장 · 복원 · 오류는 진짜와 같다 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 |

## 실행 방법
1. `pip install langgraph langgraph-checkpoint-sqlite aiosqlite langchain-openai langchain-community langchain-chroma python-dotenv` (키 없이 : `+ langchain-huggingface sentence-transformers`)
2. 같은 폴더에 `faq_manual.csv` · `.env`(`OPENAI_API_KEY`) — 키가 있으면 `# ⏳`, 없으면 `# 🧪` 셀
3. 정리 환경 : `langgraph 1.2.21` · `langgraph-checkpoint 4.3.1` · `langgraph-checkpoint-sqlite 3.1.3` · `aiosqlite 0.22.1`

## 결과 요약
| 실습 | 결과 |
|---|---|
| 그래프 | `classifier_node` → (`retriever_node`) → `answer_node` — 흐름도에 두 번 그려진 `answer_node` 는 **노드 하나** |
| 4턴 + `exit` | 안녕(NO_RAG) → 환불(RAG · FAQ-002) → 그거 전액(재구성 → FAQ-002) → 고마워(NO_RAG) → `exit` 로 종료 |
| 턴마다 체크포인트 | NO_RAG 턴 **4개** · RAG 턴 **5개** (입력 · 시작 · 거친 노드마다) — 흐름도의 '3. 상태 저장' 은 끝에 한 번이 아니다 |
| messages | 턴마다 2개씩 (2 → 4 → 6 → 8) — 흐름도의 `add_messages` 병합 설명은 정확 |
| `context` | 마지막 NO_RAG 턴 뒤 `''` — 분류 노드가 매 턴 비운 덕분 (흐름도 Node 1 `context=""`) |
| `exit` 뒤 같은 `agent` 사용 | `ValueError: no active connection` → 다시 연결하면 messages 8개 · `needs_rag False` 복원 |
| 기록 길이 | 다음 턴 `chat_history` 2개 · 46자 → 6턴 뒤 12개 · 277자 — 분류 · 재구성 · 답변 체인 세 곳에 매번 들어감 |
| 답변 노드 1개 vs 2개 | 같은 답 · 노드 3개 vs 4개 · 분기 판단 두 곳(라우터 + `if`) vs 한 곳 |
