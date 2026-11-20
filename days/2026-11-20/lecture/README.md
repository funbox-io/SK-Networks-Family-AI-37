# 2026-11-20 수업 실습 — LLM 7일차 : LangGraph 조건부 엣지 · 검색 필요 여부로 분기하는 에이전트

| 파일 | 내용 |
|---|---|
| `LangGraph_실습3.ipynb` | 수업 필기 원본 — 상태(`BaseModel`) · 노드 3개(분류 · Tavily 검색 · 답변)까지. **'라우팅 함수 정의' 에서 멈춤** (그래프 구성 · 실행 없음, 출력 없음) |
| [`langgraph_conditional_edges.ipynb`](./langgraph_conditional_edges.ipynb) | 교재 p.96~99 — 일반 엣지 vs 조건부 엣지 → **3단계 매핑**(교재 p.99 `should_continue` 실행) → 매핑 dict / 없음 / `Literal` 의 그림 차이 → 없는 이름을 돌려주면 → 되돌아가는 엣지와 `recursion_limit` |
| [`langgraph_search_router_agent.ipynb`](./langgraph_search_router_agent.ipynb) | 교재 p.100~102 · 필기 `LangGraph_실습3` 완성 — API 키 로드 → `AgentState` → 분류 · 검색 · 답변 노드(📝 고친 부분) → `route_by_search_need` → 그래프 구성 · Mermaid → 질문 3개의 실행 경로 · 최종 상태 · 검색 실패 → ⏳ 진짜 gpt-5-nano + Tavily |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 그래프를 실제로 실행한 기록으로 그림) |

교재 PDF 는 올리지 않았다. `.env` 도 올리지 않는다(저장소 `.gitignore` 에 포함).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# ⏳` | OpenAI · Tavily 키가 필요해 **출력이 비어 있는 셀** (2개) — 직접 실행 |
| `# 🧪` | 진짜 LLM · 검색 대신 **가짜 LLM(키워드 규칙) · 가짜 검색 도구**로 실제로 돌린 셀 — 답변 문장은 다르지만 **그래프가 고르는 길 · 상태 변화 · 오류는 진짜와 같다** |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 |

필기 원본에는 실행 출력이 없어 `# 📼`(수업 출력 옮김) 셀은 없다.

## 실행 방법
1. **설치** : `pip install langgraph langchain-openai langchain-tavily python-dotenv` (정리 환경 : `langgraph 1.2.21` · `langchain-core 1.8.0` · `langchain-openai 1.7.4` · `langchain-tavily 0.2.18` · `pydantic 2.14.3`)
2. **조건부 엣지 노트** : 맨 위부터 모두 실행 — API 키 · 인터넷 필요 없음
3. **검색 에이전트 노트** : `.env` 에 `OPENAI_API_KEY` · `TAVILY_API_KEY` 를 적고 실행. 키가 없으면 `# ⏳` 셀을 건너뛰고 `# 🧪` 셀로 끝까지 실행된다. 그래프 그림은 `draw_mermaid()` 글자 — **점선(`-.->`) = 조건부 엣지**

## 결과 요약
| 실습 | 결과 |
|---|---|
| 교재 p.99 `should_continue` | `n` 0 → 1 → 2 → 3 에서 `'end'` → `{'n': 3}` · Mermaid 점선 위에 `continue` / `end` 글자 |
| 매핑 3가지 | 실행은 모두 같음. **매핑 없음 · 힌트 없음** 은 그림이 `classifier_node --> __end__` 로 **틀리게** 그려짐 · 매핑 dict 나 `-> Literal[...]` 이면 바르게 |
| 오타 이름 `'searchnode'` | 매핑 있음 → `KeyError: 'searchnode'` / 매핑 없음 → **경고만 남기고 `classifier_node` 에서 끝** (답변 노드를 건너뜀) |
| 끝나지 않는 반복 | `recursion_limit=5` → `GraphRecursionError` · **기본값은 10007** (langgraph 1.2.21 — 25 가 아님) |
| 키 없이 `TavilySearch()` | `ValidationError … Did not find tavily_api_key` — 필기는 `load_dotenv()` 를 부르지 않았다 |
| 분류 결과 비교 | `== 'SEARCH'` 는 `'SEARCH'`(따옴표) · `Search.` 를 놓침 / `'SEARCH' in` 은 `NO_SEARCH` 도 True / 앞뒤 기호를 뗀 `parse_decision` 만 5개 모두 맞음 |
| 필기 검색 노드 | 검색 결과 0개(`ToolException`) → `except` 뒤 **`UnboundLocalError: … 'combined_results'`** |
| 실행 경로 | '2026년 엔비디아 2분기 실적' → `classifier → search → answer` / '리스트 컴프리헨션' · '안녕하세요' → `classifier → answer` |
| `invoke()` 결과 | dict · 검색을 건너뛰면 **`search_results` 키가 없음** (쓰인 항목만 들어옴) |
| 검색 실패 | 고친 노드는 오류 글을 `search_results` 에 남기고 끝까지 진행 — 단 답변 노드는 그 글도 '검색 결과' 로 넣는다 |
