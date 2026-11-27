# 2026-11-27 수업 실습 — LLM 12일차 : PydanticAI 구조화 출력 · 서울시 상권 분석 멀티 에이전트 1~2단계 (데이터 파이프라인 · NL2SQL 분석 에이전트)

| 파일 | 내용 |
|---|---|
| `pydantic_agent.ipynb` | 수업 필기 원본 — 자재 재고 분석 · 자동 발주 : 텍스트 파싱 실패 시나리오 → PydanticAI `Agent(output_type=…)` 성공 시나리오 (실행본) |
| `seoul_commercial_sales_db.ipynb` | 수업 필기 원본 — 상권 추정매출 CSV(128,053행) → 영문 컬럼 → MySQL `seoul_commercial`. **DB 비밀번호만 `****` 로 가렸다** |
| `data_analysis_agent.ipynb` | 수업 필기 원본 — 분석 에이전트. 출력 자료형 3개 · 상태 · 도구 함수 2개까지, **노드 함수는 주석만**. **DB 비밀번호만 `****` 로 가렸다** |
| `download.txt` | 수업 자료 — 한글 → 영문 컬럼 매핑 `column_mapping` (55개) |
| [`pydantic_ai_structured_output.ipynb`](./pydantic_ai_structured_output.ipynb) | 교재 p.139~144 — 실패 시나리오 재현 → `output_type` → **가짜 모델로 '검사 → 재시도' 확인** → 재시도 초과 · `'15'` 자동 변환 · `TestModel` → LangGraph 노드 안에서 → 📼 수업 실행 |
| [`seoul_commercial_db_pipeline.ipynb`](./seoul_commercial_db_pipeline.ipynb) | 교재 p.145~147 — 매핑 55개 확인 → 📼 수업 CSV 기록 · 🧪 모의 데이터 → **매핑 검사를 양쪽으로** → `to_sql` → 자료형 · 인덱스 확인 |
| [`seoul_commercial_analysis_agent.ipynb`](./seoul_commercial_analysis_agent.ipynb) | 교재 p.148~149 · 필기 `data_analysis_agent` 완성 — 도구 함수(연결 닫기 · **SQL 검사 · 읽기 전용 계정**) → Agent 4개 · 노드 5개 · 조건부 그래프 → `AIOMySQLSaver` 로 4턴 (교재 예시 질문 포함) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (실제 실행 기록으로 그림) |

교재 PDF · `.env` · 수업 데이터 `seoul_data.csv`(받지 못함)는 올리지 않았다.

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 옮긴 출력 |
| `# ⏳` | OpenAI 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 |
| `# 🧪` | OpenAI 대신 PydanticAI **`FunctionModel`**(정해 둔 규칙으로 답하는 가짜 모델) · **모의 데이터 72행**(같은 55개 컬럼 · 2025년 1분기 ~ 2026년 2분기 · **숫자는 실제 서울시 데이터가 아님**)으로 실제로 돌린 셀 — 검사 · 재시도 · 노드 흐름 · SQL 실행은 진짜와 같지만 **가짜 모델의 SQL 은 정해 둔 질문 꼴에만 맞다** |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 — MySQL 은 정리 환경에 띄운 **MariaDB 10.11** |

## 실행 방법
1. **설치** : `pip install "pydantic-ai-slim[openai]" langgraph langgraph-checkpoint-mysql aiomysql pandas sqlalchemy pymysql python-dotenv` (정리 환경 : `pydantic-ai-slim 2.76.0` · `langgraph 1.2.21` · `pandas 3.0.5` · `SQLAlchemy 2.1.9` · `PyMySQL 1.2.4` · `aiomysql 0.3.2`)
2. **MySQL** : `CREATE DATABASE langgraph_db;` · (권장) `CREATE USER reader …; GRANT SELECT ON langgraph_db.* TO reader;`
3. **`.env`** : `OPENAI_API_KEY` · `MYSQL_USER` · `MYSQL_PASSWORD` · `MYSQL_HOST` · `MYSQL_PORT` · `MYSQL_DB` · `MYSQL_RO_USER` · `MYSQL_RO_PASSWORD`
4. 순서 : 파이프라인 노트(테이블 만들기) → 분석 에이전트 노트. 같은 폴더에 `download.txt`
5. ⚠️ **`gpt-5-nano` 는 2026-12-11 지원 종료 예정** — 이후에는 `MODEL_NAME` 을 바꿔야 실행된다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 실패 시나리오 | 땜질 파싱 후 `int('수량 부족 (재고 15개)')` → `ValueError` |
| PydanticAI (🧪 첫 답 틀림) | `int_parsing` 오류를 LLM 에 돌려줌 → 2번째 답 `15` → `InventoryAnalysis(…, current_stock=15)` · 요청 2번 |
| 끝까지 틀리면 | `UnexpectedModelBehavior: Exceeded maximum output retries (1)` |
| `'15'` (글자) | Pydantic 이 int 15 로 바꿔 받음 (재시도 없음) |
| 키 없이 `Agent('openai:…')` | `UserError: Set the OPENAI_API_KEY …` |
| 📼 수업 PydanticAI | 한 번에 `current_stock=15` → 발주 85개 · **`DeprecatedModelWarning` : gpt-5-nano 2026-12-11 종료** |
| 컬럼 매핑 | 55개 = 기타 7 + 금액 24 + 건수 24 · 영문 중복 없음 |
| 매핑 검사 | 필기 검사는 **빠진 열**을 못 잡음(열 하나 지워도 통과) → 반대 방향 검사 추가 |
| `to_sql` 결과 | `BIGINT` · `TEXT` 열 · **인덱스 없음** · `replace` 는 테이블을 지우고 새로 만듦 |
| SQL 안전장치 | `DROP` → 검사에서 거부 · 읽기 전용 계정의 `DELETE` → `1142 DELETE command denied` |
| 집계 결과 | `SUM` → `Decimal` → `to_number` 로 int |
| 분석 4턴 (🧪) | 성수동 2025 여성 매출 → '거기와 흑리단길 · 2024' 재구성 성공이지만 **0행 (2024년 데이터 없음)** → 2026 비교 2행 → '고마워요' 일반 답 |
| 체크포인터 경고 | `Deserializing unregistered type __main__.ReportResult` — 상태에 직접 만든 Pydantic 클래스 → 앞으로 차단 예정 |
