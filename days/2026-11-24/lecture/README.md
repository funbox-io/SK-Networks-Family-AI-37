# 2026-11-24 수업 실습 — LLM 9일차 : 비동기 처리(async · await) · 멀티 에이전트 RAG 챗봇 비동기 업그레이드

| 파일 | 내용 |
|---|---|
| `LangGraph_실습5.ipynb` | 수업 필기 원본 — Day 053 에서 멈춰 있던 멀티 에이전트 RAG 챗봇(동기)의 **완성 · 실행본** (진짜 gpt-5-nano 로 3턴 대화) |
| `LangGraph_실습6.ipynb` | 수업 필기 원본 — 같은 챗봇의 **비동기판**. `async def` 노드 3개까지 · 그래프 구성 비어 있음 · `main()` 미완성 |
| `faq_manual.csv` | 실습 데이터 (Day 053 과 같은 FAQ 10개) |
| [`python_asyncio_basics.ipynb`](./python_asyncio_basics.ipynb) | 교재 p.120~124 — 카페 비유를 시간 재기로 · 코루틴 객체 · `asyncio.run` vs Jupyter `await` · `.py` 로 실행 · 막는 호출(`time.sleep`) · `to_thread` · I/O vs CPU |
| [`langgraph_async_multi_agent_rag.ipynb`](./langgraph_async_multi_agent_rag.ipynb) | 교재 p.125~128 · 필기 `실습6` 완성 — 비동기 노드 → 그래프 → `invoke` 하면 `TypeError` → 필기 `main()` 의 무한 반복 → 고친 `main()` → **동기 vs 비동기 시간 재기**(1명 · 5명 · `gather`) |
| [`langgraph_multi_agent_class_run.ipynb`](./langgraph_multi_agent_class_run.ipynb) | 필기 `실습5` 수업 실행 기록 읽기 — 재구성 결과 · 묵은 상태 값 · 할 수 없는 일을 약속한 답변 · 추론 토큰 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (실제로 시간을 잰 기록으로 그림) |

교재 PDF 는 올리지 않았다. `.env` 도 올리지 않는다(저장소 `.gitignore` 에 포함).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 옮긴 출력 (`실습5` 3턴 대화) |
| `# ⏳` | OpenAI 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (`input()` 대화 루프 포함) |
| `# 🧪` | OpenAI 대신 **로컬 임베딩**(`jhgan/ko-sroberta-multitask`) · **0.3초 기다리는 가짜 LLM** 으로 실제로 돌린 셀 — 답변 · 시간은 gpt-5-nano 와 다르지만 비동기 동작(오류 · 순서 · 동시 실행 단축)은 같다 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 — 걸린 시간은 실행마다 조금씩 다르다 |

## 실행 방법
1. **asyncio 노트** : 설치할 것 없음 (표준 라이브러리) — 맨 위부터 실행
2. **비동기 에이전트 노트** : `pip install langgraph langchain-openai langchain-community langchain-chroma python-dotenv` (키 없이 : `+ langchain-huggingface sentence-transformers`) · 같은 폴더에 `faq_manual.csv` · `.env`
3. 필기 `실습6` 첫 셀의 `AsyncSqliteSaver` 는 **`pip install langgraph-checkpoint-sqlite`** 가 있어야 import 된다 (정리 환경 : `langgraph 1.2.21` · `langgraph-checkpoint-sqlite 3.1.3`)
4. Jupyter 에서는 `await main()`, `.py` 파일에서는 `asyncio.run(main())`

## 결과 요약
| 실습 | 결과 |
|---|---|
| 커피 3잔 (0.5초씩) | 동기 1.50초 · 비동기 차례로 `await` **1.50초** · `gather` 0.50초 |
| 코루틴 | `say_hello()` → `<coroutine object …>` (실행 안 됨) · `await` 해야 실행 |
| Jupyter 에서 `asyncio.run(main())` | `RuntimeError: asyncio.run() cannot be called from a running event loop` → `await main()` · `.py` 로 실행하면 정상 |
| `async def` 안의 `time.sleep` | `gather` 해도 1.50초 (루프가 막힘) · `asyncio.to_thread` 로 보내면 0.50초 |
| CPU 계산 | 동기 0.45초 · `gather` 0.46초 — 비동기는 I/O 기다림만 겹친다 |
| 비동기 노드 그래프 `invoke` | `TypeError: No synchronous function provided to "rephrase_node"` → `ainvoke` |
| 필기 `main()` | `ainvoke()` 입력 없음 → `TypeError: … missing 1 required positional argument: 'input'` · `except` 가 잡고 `while True` 로 **무한 반복** |
| 시간 (🧪 LLM 0.3초) | 1명 : 동기 0.67초 = 비동기 0.67초 · 5명 : 차례로 3.35초 → **`gather` 0.94초** · 동기 노드 그래프도 `ainvoke` + `gather` 0.95초 (스레드) |
| `실습5` 수업 기록 | 2턴 '그거 전액 …' → '수강한 강의를 전액 환불받으려면 …' 으로 재구성 → 환불 FAQ ✅ · 추론 토큰 88% · 84% · 없는 기능(고객센터 전달) 약속 |
