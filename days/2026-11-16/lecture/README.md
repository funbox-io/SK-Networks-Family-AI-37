# 2026-11-16 수업 실습 — LLM 3일차 : RAG 개념 · 데이터 불러오기 · 텍스트 분할

| 파일 | 내용 |
|---|---|
| `RAG_실습06.ipynb` | 수업 필기 원본(내 필기) — 환경 설정 → `TextLoader` → QA 쌍 길이 계산 → 분할 도구 생성. **출력에 찍혀 있던 API 키 2개의 값만 `…(가림)` 으로 바꿨다**(그 밖의 코드 · 출력은 그대로) |
| `1RAG_실습1.ipynb` | 수업 필기 원본(강의본) — 같은 흐름의 완성본. 각 QA 쌍 글자 수 `[133, 142, 146, 123, 157, 119, 116, 149, 149, 147]` · 최대 157자 |
| [`rag_overview_flow.ipynb`](./rag_overview_flow.ipynb) | 교재 p.34~38 정리 — 빛과 그림자 → RAG 5단계 → 실습 개요(그림 ↔ LangChain 클래스) → **키 없이 준비 → 검색 → 증강 한 바퀴**(대체 임베딩 + `FAISS`) → `chunk_size` 별 검색 결과 → 대체 임베딩의 한계 → 다음 수업용 RAG 체인 코드 |
| [`rag_loader_text_splitter.ipynb`](./rag_loader_text_splitter.ipynb) | `RAG_실습06` · `1RAG_실습1` 정리 · 개선본 — `TextLoader` → `Document` → **`.env` 를 잘못 읽은 실수 재현** → 줄바꿈(`\r\n`) 함정 → QA 쌍 글자 · 토큰 수 → `max(qa_pairs)` 오류 재현 → `RecursiveCharacterTextSplitter` → `split_documents` 검증 → **`chunk_size` 20 ~ 420 실험** → `chunk_overlap` → 글자 vs 토큰 → QA 쌍으로 직접 `Document` 만들기 |
| [`manual.txt`](./manual.txt) | 실습 데이터 — 코드크래프터스 아카데미 고객 응대 매뉴얼. 질문/답변 10쌍 · 1,399자(줄바꿈 `\r\n`, UTF-8) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 같은 분할 도구 · 같은 대체 임베딩으로 계산) |

교재 PDF 는 올리지 않았다. `.env` 는 올리지 않는다(저장소 `.gitignore` 에 포함 — 단, **노트북 출력에 찍힌 키**는 `.gitignore` 가 막아 주지 못한다).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 🧪` | 진짜 임베딩 모델 대신 **글자 2~3개 묶음의 겹침(TF-IDF)으로 벡터를 만드는 대체 임베딩**으로 흐름만 실제로 돌린 셀 (`rag_overview_flow` 7개). 순위 · 점수는 `OpenAIEmbeddings` 결과와 다르다 |
| `# ⏳` | API 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (`rag_overview_flow` 2개 : 증강 프롬프트로 답 생성 · `OpenAIEmbeddings` RAG 체인) |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀. `rag_loader_text_splitter` 는 전부 여기에 해당한다 |

## 실행 방법
1. **설치** : `pip install langchain-community langchain-text-splitters langchain-openai faiss-cpu python-dotenv tiktoken scikit-learn pandas matplotlib` (정리 환경 : `langchain-community 0.4.2` · `langchain-text-splitters 1.1.3` · `langchain-core 1.8.1` · `faiss-cpu 1.16.0`)
2. **데이터** : `manual.txt` 를 노트북과 **같은 폴더**에 둔다
3. **실행** : 맨 위부터 **모두 실행**. 불러오기 · 분할 · 대체 임베딩 검색은 API 키 · 인터넷 없이 돌아간다(tiktoken 은 처음 한 번 토크나이저 파일을 내려받는다)
4. **`# ⏳` 셀** : 노트북 폴더(또는 상위 폴더)의 `.env` 에 `OPENAI_API_KEY="sk-…"` 가 있어야 한다
5. `chunk_size` 경계(159 · 238)는 `langchain-text-splitters 1.1.3` 에서 확인한 값이다. 버전이 다르면 `rag_loader_text_splitter` 5장 셀로 다시 확인한다

## 결과 요약
| 실습 | 결과 |
|---|---|
| `TextLoader` | `[Document]` 1개 · `page_content` 1,399자 · `metadata={'source': 'manual.txt'}` · `load()` 는 `BaseLoader` 의 공통 함수 |
| 줄바꿈 | 파일은 `\r\n`(28개). 변환 없이 읽으면 1,427자 · `split('\n\n')` 조각 1개 / 텍스트 모드 · `TextLoader` 는 1,399자 · 10개 |
| QA 쌍 길이 | 글자 `[133, 142, 146, 123, 157, 119, 116, 149, 149, 147]` · 토큰(`cl100k_base`) `[123, 140, 125, 117, 159, 109, 105, 145, 142, 126]` · 전체 **1,291 토큰**(임베딩 제한 8,192 의 15.8%) |
| `max(qa_pairs)` (필기) | 사전 순 최댓값 = 8번째 '코딩 실습…' 149자 ↔ `max(…, key=len)` = 5번째 **157자** |
| `for out in string_txt: qa_pairs.append(out)` (필기) | 리스트 10개 → **157개**(글자 147개 추가) |
| `RecursiveCharacterTextSplitter(160, 0)` | 청크 **10개** = QA 10쌍 (모두 `청크 == QA 쌍`) · `split_documents` 는 `TextSplitter` 의 공통 함수 |
| `chunk_size` 실험 | 100 → 27개 · 150 → 13개 · **157 · 158 → 11개** · **159 ~ 238 → 10개** · 239 → 9개 · 300 → 5개 · 1399 이상 → 1개 |
| 경계가 159 인 이유 | `keep_separator=True`(기본) : 구분자 `\n\n` 2글자가 조각 앞에 붙어 157 + 2 = 159. `keep_separator=False` 면 157 부터 10개 |
| `chunk_overlap` | `chunk_size=160` 에서 0 · 20 · 40 모두 겹침 0군데 / `chunk_size=80, overlap=20` 은 10군데(14 ~ 19자) |
| 토큰 기준 분할 | `from_tiktoken_encoder(chunk_size=160)` → 11개 / `200` → 10개 |
| 🧪 검색 (대체 임베딩) | '환불 받으려면 어떻게 해야 하나요?' → 1등 **2번 청크**(코사인 0.205) · 2등 1번(0.117) |
| 🧪 `chunk_size` 별 1등 청크 | 100 → 가입 **질문 줄만** 28자(답 없음) / 160 → 환불 QA 142자 / 300 → 가입 + 환불 277자 / 4000 → 전체 1,399자 |
| 증강 프롬프트 크기 | 검색된 청크 2개 ≈ **225 토큰** / 매뉴얼 전체 ≈ 857 토큰 (`o200k_base`, 3.8배) |
| 🧪 대체 임베딩의 한계 | 매뉴얼과 낱말이 겹치는 질문 6/6 · 뜻만 같은 질문(`돈 돌려줘` · `핸드폰 지원돼?` · `자격증 나와요?` 등) **0/6** |
