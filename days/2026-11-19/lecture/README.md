# 2026-11-19 수업 실습 — LLM 6일차 : LangGraph 입문 · 상태(State) · TypedDict · Pydantic BaseModel

| 파일 | 내용 |
|---|---|
| `LangGraph_실습1.ipynb` | 수업 필기 원본 — TypedDict 연습 → `AgentState` → 노드 3개 → 그래프 만들기까지. **컴파일 · 실행 전에 멈춤** (`call_llm` 이 `id` 없는 `tool_calls` 를 만들어 실행하면 오류) |
| `LangGraph_실습1_1.ipynb` | 수업 필기 원본 — 같은 실습의 **실행 완료본** (`compile` → `invoke` → 최종 상태 출력) |
| [`langgraph_typeddict_state.ipynb`](./langgraph_typeddict_state.ipynb) | 교재 p.72~87 · 92~93 — 체인 vs 그래프 → 타입 힌트 → `TypedDict` → **리듀서(`add_messages`) 있음 / 없음** → 교재 · 필기의 메시지 오류 재현 → 짝이 맞는 노드 → 그래프 · 컴파일 · Mermaid → `invoke` · `stream` → 빠진 키 `KeyError` |
| [`langgraph_pydantic_state.ipynb`](./langgraph_pydantic_state.ipynb) | 교재 p.88~91 · 94~95 — `BaseModel` 검사 · `Field` 제약 · JSON 스키마 → BaseModel 상태로 같은 그래프 → `state.messages` · `invoke` 결과는 dict → **검사 시점 3가지** → TypedDict vs BaseModel 표 다시 정리 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 그래프를 실제로 실행한 기록으로 그림) |

교재 PDF 는 올리지 않았다. 오늘 실습은 LLM 을 부르지 않는 **모의 노드**라 데이터 · API 키가 필요 없다.

## 출력을 읽는 법

모든 셀을 **실제로 실행**했다. `# 📼` 셀(TypedDict 노트 1개)만 수업 시간 출력을 옮긴 것이다 — 메시지 `id` 는 실행할 때마다 달라진다.

## 실행 방법
1. **설치** : `pip install langgraph` (정리 환경 : `langgraph 1.2.21` · `langchain-core 1.8.0` · `pydantic 2.14.3`)
2. **실행** : 맨 위부터 모두 실행. 인터넷 · API 키 필요 없음. 그래프 그림은 `draw_mermaid()` 글자로 출력한다(Mermaid 를 지원하는 편집기 · GitHub 에 붙이면 그림이 된다)

## 결과 요약
| 실습 | 결과 |
|---|---|
| 타입 힌트 | `agent_node('세 번', 123)` 도 그대로 실행 — 힌트는 `__annotations__` 에 기록만 된다 |
| `TypedDict` | 결과는 평범한 `dict` · 틀린 자료형 · 빠진 키도 오류 없이 만들어짐 |
| 리듀서 | 리듀서 없는 `list[BaseMessage]` → 질문이 사라지고 AI 답 1개만 / `add_messages` → `[Human, AI]` 로 덧붙임 · 같은 `id` 면 교체 · 글자도 `HumanMessage` 로 |
| 교재 p.87 · p.91 코드 | `ToolMessage(content=…)` → **`KeyError: 'tool_call_id'`** |
| 필기 `LangGraph_실습1` | `tool_calls=[{'name', 'args'}]` → **`TypeError: tool_call() missing … 'id'`** |
| 그래프 | `StateGraph` → `compile()` → `CompiledStateGraph` · Mermaid `__start__ → call_llm_node → call_tool_node → summarize_node → __end__` |
| `stream(stream_mode='updates')` | 노드마다 바꾼 항목 : llm → `messages`(AI) / tool → `messages`(Tool) + `tool_output` / summarize → `messages`(AI) |
| TypedDict 빠진 키 | 도구 노드 없이 요약 노드만 → `KeyError: 'tool_output'` |
| `BaseModel` | `id='2'` → 2 로 바꿔 받음 · `id='삼'` · 빠진 `id` → `ValidationError` · `Field(ge=1, le=10, min_length=2)` 동작 |
| BaseModel 상태 | 노드가 받는 것은 `AgentState` 객체(`state['messages']` → `TypeError: not subscriptable`) · **`invoke()` 결과는 dict** |
| 검사 시점 | ① 입력 값 → 오류 ② 노드 출력 → **다음 노드가 받을 때** 오류 ③ 마지막 노드 출력 → **검사 안 됨**(123 그대로) |
