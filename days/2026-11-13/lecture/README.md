# 2026-11-13 수업 실습 — LLM 2일차 : LangChain 체인 · 챗봇 · 도구와 에이전트

| 파일 | 내용 |
|---|---|
| `LangChain_실습1.ipynb` | 수업 필기 원본 — 프롬프트 \| LLM \| 출력 파서 체인, '양자 컴퓨터' 설명 (실행 결과 있음) |
| `LangChain_실습2.ipynb` | 수업 필기 원본 — 고객 리뷰 감성 분석 체인. 프롬프트까지 쓰고 'llm 모델 생성' 빈 셀에서 멈춤 |
| `LangChain_실습3.ipynb` | 수업 필기 원본 — `MessagesPlaceholder` 챗봇, `input()` 반복문으로 3번 대화 (답만 기록됨) |
| `LangChain_실습4.ipynb` | 수업 필기 원본 — `TavilySearch` 도구 이름 · 설명 · 'Tesla 2026년 2분기 실적' 검색 결과 |
| `LangChain_실습5.ipynb` | 수업 필기 원본 — `create_agent` 실시간 검색 에이전트 (메시지 전체 · 최종 답 기록) |
| [`langchain_chain_basics.ipynb`](./langchain_chain_basics.ipynb) | `실습1` · `실습2` 정리 · 개선본 (교재 p.18~24) — 프롬프트 채워 보기 → LLM · 파서 → 체인 → **'100 토큰 이내' 를 지켰는지 세기** → 가짜 LLM 으로 체인 단계 확인 → 감성 분석 체인 완성 → **구조화 출력(Pydantic)** |
| [`langchain_chatbot_memory.ipynb`](./langchain_chatbot_memory.ipynb) | `실습3` 정리 · 개선본 (교재 p.25~26) — `MessagesPlaceholder` 가 실제로 보내는 메시지 → 수업 대화 → **호출마다 늘어나는 입력 토큰** → `trim_messages` → `input()` 대신 `chat()` 함수 |
| [`agent_tools_tavily.ipynb`](./agent_tools_tavily.ipynb) | `실습4` · `실습5` 정리 · 개선본 (교재 p.27~33) — 도구의 이름 · 설명 · **입력 스키마** → `@tool` 내 함수 → 검색 결과 표 · 공식 IR 과 대조 → `create_agent` 흐름(가짜 LLM) · 그래프 → **수업 에이전트 기록 분석** → 답변 ↔ 검색 결과 대조 → 교재의 체인 2개 방식 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (숫자와 글은 수업 실행 결과에서 가져옴) |

교재 PDF 는 올리지 않았다. 데이터 파일은 없다(리뷰 글 · 검색 결과는 노트북 안에 있음). `.env` 는 올리지 않는다(저장소 `.gitignore` 에 포함).

## 출력을 읽는 법 (중요)

정리 노트북은 **API 키가 없는 환경**에서 만들었다(Day 046 과 같은 방식). 셀 첫 줄의 표시로 구분한다.

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 그대로 옮긴 출력 (7개 : 체인 2 · 챗봇 1 · 도구 · 에이전트 4) |
| `# ⏳` | API 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (4개 : 감성 분석 2 · 챗봇 1 · 체인 2개 에이전트 1) |
| `# 🧪` | API 대신 **정해 둔 답을 내는 가짜 LLM**(`GenericFakeChatModel`)으로 체인 · 에이전트의 **흐름만** 실제로 돌린 셀 — 답 내용은 의미 없음 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 (프롬프트 채우기 · 토큰 세기 · 도구 스키마 · 수업 기록 분석) |

`agent_tools_tavily.ipynb` 의 기록 분석 셀은 같은 폴더의 `LangChain_실습4.ipynb` · `LangChain_실습5.ipynb` 를 읽는다.

## 실행 방법
1. **설치** : `pip install langchain langchain-openai langchain-tavily python-dotenv tiktoken pandas` (수업 버전 `langchain 1.5.0` · `langchain-core 1.8.0` · `langchain-openai 1.7.4` · `langchain-tavily 0.2.18` · `langgraph 1.2.21`)
2. **API 키 2개** : 노트북 폴더(또는 상위 폴더)의 `.env` → `OPENAI_API_KEY="sk-…"` · `TAVILY_API_KEY="tvly-…"` ([tavily.com](https://tavily.com) 가입, 무료 월 1,000 크레딧)
3. **실행** : 맨 위부터 **모두 실행**. 인터넷 필요
4. **요금** : `gpt-5-nano` 입력 $0.05 · 출력 $0.40 / 100만 토큰 — 수업 에이전트 1번 ≈ $0.002. Tavily 검색은 `basic` 1크레딧 · `advanced` 2크레딧 (수업 에이전트 1번 = 6크레딧). OpenAI 모델 문서에 `gpt-5-nano` 가 **지원 종료 예정(deprecated)** 으로 표시돼 있다 — 수업 코드 그대로 두었다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 체인 '양자 컴퓨터' (수업 결과) | 266자 · **168토큰** (o200k_base) — 시스템 프롬프트의 '100 토큰 이내' 초과 |
| 체인 구조 | `prompt \| llm \| parser` = `RunnableSequence` 3단계 · 파서를 빼면 `AIMessage` 객체 |
| 감성 분석 | 필기 미완성 → 체인 완성 · `with_structured_output(Sentiment)` (긍정/부정/중립 · 근거 · 키워드) · 형식이 틀린 답은 `OutputParserException` |
| 챗봇 (수업 결과) | 답 3개 = 240 · 1,167 · 134 토큰 → 보내는 입력 ≈ 65 → 335 → **1,532** 토큰 (지난 대화를 매번 다시 보냄) |
| `trim_messages(max_tokens=800)` | 기록 7개 · 1,574토큰 → 3개 · 151토큰 |
| TavilySearch 입력 스키마 | `query`(필수) · `search_depth`(basic · advanced · **fast · ultra-fast**) · `time_range` · `topic` 등 9개 |
| Tesla 2분기 검색 (수업 결과) | 결과 3개 — 블로그 '매출 282억 달러 · EPS 0.33' = 공식 IR PDF `28,236` · `0.33` 일치 / 세 번째(점수 0.55) 신문 기사는 **유료 구독 안내문뿐** |
| 수업 에이전트 기록 | Human → AI(tool_calls **3개 병렬**) → Tool × 3 → AI · LLM 2번 : 입력 1,376 → **5,468** · 출력 713 → 4,174 (추론 576 · 2,816) · 검색어와 `advanced` · `time_range='year'` 는 LLM 이 정함 · 출처 9개 |
| 답변 ↔ 검색 결과 | 숫자 · 이름 11개 모두 검색 결과에 있음 (USD 29.6 billion → 296억 달러 정확) · 그러나 '80% 는 LangChain, 복잡하면 LangGraph 로 직접(*Drop to LangGraph*)' 를 '**LangGraph 로 내려가지 않고도**' 로 **뜻을 거꾸로** 옮김 · `GPT-6 Astra` 는 블로그 1곳 출처 |
| 교재 체인 2개 방식 | `tool_calling_chain` → 도구 실행 → `ToolMessage` → `final_answer_chain` (가짜 LLM 으로 흐름 확인, 도구 1회) vs `create_agent` (반복) |
