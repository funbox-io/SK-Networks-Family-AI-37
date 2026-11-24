# 2026-11-23 수업 실습 — LLM 8일차 : 싱글 에이전트 RAG 챗봇 · 멀티 에이전트 RAG (질문 재구성 → 검색 → 답변)

| 파일 | 내용 |
|---|---|
| `LangGraph_실습3_1.ipynb` | 수업 필기 원본 — Day 052 `LangGraph_실습3` 의 **완성 · 실행본** (라우팅 함수 · 그래프 · 진짜 gpt-5-nano + Tavily 실행 2건) |
| `LangGraph_실습4.ipynb` | 수업 필기 원본 — FAQ CSV → Chroma → RAG 체인 → `rag_node` 하나짜리 **싱글 에이전트** · `while` + `input()` 대화 루프 |
| `LangGraph_실습5.ipynb` | 수업 필기 원본 — 멀티 에이전트. **질문 재구성 체인까지 만들고 멈춤** |
| `faq_manual.csv` | 실습 데이터 — 가상의 '코드크래프터스 아카데미' FAQ 10개 (`faq_id` · `category` · `question` · `answer`) |
| [`langgraph_single_agent_rag_chatbot.ipynb`](./langgraph_single_agent_rag_chatbot.ipynb) | 교재 p.103~106 · 필기 `실습4` — CSV 로드(`metadata_columns`) → 저장소 중복 · 묵은 DB 함정 → k=1 검색기 확인 → RAG 체인 → `rag_node` 그래프 → 대화 루프(기억 없음 확인) → **교재 p.105 조건부 분기판**(classifier → retriever → answer) |
| [`langgraph_multi_agent_rag.ipynb`](./langgraph_multi_agent_rag.ipynb) | 교재 p.107~119 · 필기 `실습5` 완성 — 싱글 vs 멀티 · 전용 체인 2개(`MessagesPlaceholder`) → 상태 확장(`rephrased_query` · `context` · `next`) → 노드 3개 · `router` → 두 번 이어서 묻기 → 재구성 규칙의 한계 → ⏳ 진짜 실행 |
| [`langgraph_search_router_class_run.ipynb`](./langgraph_search_router_class_run.ipynb) | 필기 `실습3_1` 의 수업 실행 기록 읽기 — 실행 경로 · 분류 비용(reasoning 토큰) · **NVIDIA 실적 답변을 보도자료와 대조** |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 그래프를 실제로 실행한 기록으로 그림) |

교재 PDF 는 올리지 않았다. `.env` 도 올리지 않는다(저장소 `.gitignore` 에 포함).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 옮긴 출력 (`실습3_1` 기록 노트 2개) |
| `# ⏳` | OpenAI 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (`input()` 대화 루프 포함) |
| `# 🧪` | OpenAI 대신 **로컬 임베딩**(`jhgan/ko-sroberta-multitask`) · **가짜 LLM** 으로 실제로 돌린 셀 — 검색 순위 · 거리는 `text-embedding-3-small` 과 다를 수 있고, 답변은 '컨텍스트의 첫 문장' 이다. 가짜 질문 재구성은 '앞 질문 + 지금 질문 이어 붙이기' 규칙 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 |

## 실행 방법
1. **설치** : `pip install langgraph langchain-openai langchain-community langchain-chroma python-dotenv` (키 없이 : `+ langchain-huggingface sentence-transformers`) — 정리 환경 : `langgraph 1.2.21` · `langchain-core 1.8.0` · `langchain-community 0.4.2` · `langchain-chroma 1.1.0` · `langchain-openai 1.7.4`
2. 노트북과 같은 폴더에 `faq_manual.csv` · `.env`(`OPENAI_API_KEY`)
3. 키가 있으면 `# ⏳` 셀, 없으면 `# 🧪` 셀을 실행 — 어느 쪽이든 끝까지 실행된다

## 결과 요약
| 실습 | 결과 |
|---|---|
| `CSVLoader(content_columns=…)` | 메타데이터는 `source` · `row` 뿐 → `metadata_columns=['faq_id', 'category']` 로 번호 · 분류 보존 |
| `Chroma.from_documents` 두 번 | 같은 폴더에 **20개(중복)** · 필기의 '있으면 불러오기' 는 중복은 막지만 CSV 를 바꿔도 **옛 벡터**를 쓴다 |
| k=1 검색 (🧪 로컬) | 환불 → FAQ-002 · 수료증 → FAQ-003 · 영상 → FAQ-005 ✅ / '그거 전액 …' → FAQ-003 ✗ · '안녕하세요' → FAQ-008 · '오늘 날씨' → FAQ-010 (관계없어도 1개를 꼭 돌려줌) |
| 싱글 에이전트 2턴 | 질문마다 새 상태(`messages` 2개) → '그거 전액 …' 이 **수료증 FAQ** 로 |
| 교재 p.105 분기판 | '안녕하세요' `classifier → answer` (검색 건너뜀) · '환불은 어떻게?' `classifier → retriever → answer` |
| 멀티 에이전트 2턴 | 앞 `messages` 를 이어 넣고 재구성 → **FAQ-002 (환불)** ✅ |
| 재구성 품질 | 이어 붙이기 : 환불 ✅ · '앱에서도 돼?' 는 앞 주제(FAQ-005)에 끌려감 ✗ / 한 문장으로 다시 쓰기 : 둘 다 ✅ (거리 0.447 · 0.371) |
| `next` + `router` | 매핑 dict 로 점선 3개 · 지금 구조에서는 `add_edge` 와 결과 같음 |
| `실습3_1` 수업 기록 | 분류 `NO_SEARCH` / `SEARCH` 로 분기 정상 · 분류 한 단어에 reasoning 토큰 64 · 256개 · NVIDIA FY27 Q2 숫자 **모두 보도자료와 일치** |
