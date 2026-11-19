# 2026-11-18 수업 실습 — LLM 5일차 : 메타데이터 필터 · BM25 희소 검색 · 하이브리드 검색(RRF)

| 파일 | 내용 |
|---|---|
| `RAG_실습4.ipynb` | 수업 필기 원본 — `manual.txt` 를 `BM25Retriever` 로 검색하려고 MeCab 토큰화 함수를 쓰다가 **`for` 에서 멈춤** |
| `RAG_실습5_1.ipynb` | 수업 필기 원본 — 기술 지원 매뉴얼 하이브리드 RAG 챗봇 : MeCab + BM25 · Chroma · `EnsembleRetriever` · 챗봇 질문 3번의 실행 결과 |
| `RAG_실습6.ipynb` | 수업 필기 원본 — `CSVLoader` 로 챗봇 데이터 30줄 → Chroma → 검색 테스트 |
| [`chroma_filter_csvloader.ipynb`](./chroma_filter_csvloader.ipynb) | 교재 p.51~54 · `RAG_실습6` — `company_policy.json` 으로 연산자(`$eq` ~ `$or`)와 MySQL `WHERE` 비교 → 자주 틀리는 것(키 두 개 · 자료형) → **FAISS 필터의 `fetch_k` 함정** → 문서 5,000개로 속도 · 필터 결과 비교 → `CSVLoader` 와 글자 메타데이터 |
| [`bm25_sparse_search.ipynb`](./bm25_sparse_search.ipynb) | 교재 p.55~61 · `RAG_실습4` 완성 — 정리 자료 `TF-IDF 정리` 다시 계산 → IDF 4가지 → BM25 포화 · 길이 정규화 → 띄어쓰기 vs **MeCab** → **BM25 손계산 = `rank_bm25`** → 코드 · 조항 검색 → 코드를 통째로 남기는 토크나이저 → 0점이어도 k개 |
| [`hybrid_search_rrf.ipynb`](./hybrid_search_rrf.ipynb) | 교재 p.62~64 · `RAG_실습5_1` — `chunk_size=210` 확인 → 희소 · 밀집 · 하이브리드 비교 → **RRF 손계산 = `EnsembleRetriever`** → 연습용 오류 코드 문서로 단일 검색의 문제 → 고쳐 보기 2가지와 그 대가 → RAG 체인 |
| [`manual.txt`](./manual.txt) · [`tech_support_manual.txt`](./tech_support_manual.txt) | 실습 데이터 — 고객 응대 매뉴얼(QA 10쌍, Day 048 과 같은 파일) · 스마트홈 기술 지원 매뉴얼(QA 8쌍 · 오류 코드 · 규정 조항) |
| [`company_policy.json`](./company_policy.json) · [`ChatBotData_sample.csv`](./ChatBotData_sample.csv) | 실습 데이터 — 사내 규정 5개 + 메타데이터(category · department · year) · 챗봇 Q · A 30줄(label 0) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 |

교재 PDF 와 함께 받은 정리 자료 PDF(`TF-IDF 정리`, 4쪽)는 올리지 않았다 — 내용과 계산은 `bm25_sparse_search` 1장에서 다시 확인했다. `.env` 는 올리지 않는다. 올린 필기 3개에는 API 키 값이 없다(확인함).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 옮긴 출력 (CSV 검색 1 · 하이브리드 2) |
| `# ⏳` | API 키가 필요해 **출력이 비어 있는 셀** (하이브리드 1 : OpenAI 임베딩 + `ChatOpenAI` 로 진짜 RAG) |
| `# 🧪` | 밀집 검색을 OpenAI 대신 **로컬 한국어 임베딩**(`jhgan/ko-sroberta-multitask`)으로 돌린 셀, 또는 **가짜 LLM** 으로 체인 흐름만 본 셀 |
| 표시 없음 | 실제로 실행한 셀. **BM25 는 임베딩이 필요 없어서** `bm25_sparse_search` 는 전부 키 없이 수업과 같은 방식으로 실행했다 |

## 실행 방법
1. **설치** : `pip install langchain-community langchain-classic langchain-chroma faiss-cpu rank_bm25 python-mecab-ko langchain-huggingface sentence-transformers langchain-openai python-dotenv scikit-learn pandas matplotlib` (정리 환경 : `langchain-core 1.8.0` · `langchain-classic 1.0.8` · `langchain-chroma 1.1.0` · `chromadb 1.5.9` · `rank-bm25 0.2.2` · `python-mecab-ko 1.3.7`)
2. **MeCab** : Windows · Mac · Colab 은 `pip install python-mecab-ko` 로 사전까지 설치된다. 리눅스 · 새 파이썬에서 빌드 오류가 나면 `apt-get install mecab libmecab-dev` 를 먼저(정리 환경이 그랬다)
3. **데이터** : 위 데이터 파일 4개를 노트북과 **같은 폴더**에
4. **실행** : 맨 위부터 모두 실행. 🧪 로컬 임베딩은 처음 한 번 모델(약 440MB)을 받는다. `# ⏳` 셀은 `.env` 의 `OPENAI_API_KEY` 가 필요하다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 교재 p.51 필터 '비밀번호 규정 알려줘' | `$and`(보안 · 2026) → 사내 보안 규정 제5조 |
| 연산자 7가지 | `$eq` · `$ne` · `$gt` · `$lt` · `$in` · `$and` · `$or` 모두 MySQL `WHERE` 로 쓴 조건대로 걸렀다 (5개 규정의 메타데이터와 대조) |
| 자주 틀리는 것 | 키 두 개를 `$and` 없이 → `ValueError` · `year` 를 글자 `'2026'` 으로 → 0개 · CSV `label` 은 글자 `'0'` (숫자 `0` → 0개) |
| FAISS 필터 | `$and` · `$in` 등은 되지만 '다르다' 는 **`$neq`**(`$ne` 는 오류) · `fetch_k=1` 이면 빈 결과 |
| 문서 5,000개 | 저장 FAISS 0.45초 · Chroma 2.94초 / 검색 0.44ms · 1.57ms / 조건에 맞는 문서 178개에 k=4 → **FAISS 1개 · Chroma 4개** (FAISS 는 `fetch_k=5000` 이어야 4개) |
| `CSVLoader` | 30줄 → Document 30개 · 본문 `Q: … \nA: …` · 🧪 '가족 여행 갈거야…' → row 23 · 28 (**수업과 같음**) |
| 정리 자료 `TF-IDF 정리` | TF · DF · `3 ÷ 1 = 3.0` · `2 × 3.0 = 6.0` 표는 **모두 맞다** · 단 IDF 는 실제로 로그를 씌운다 |
| BM25 IDF (`rank_bm25`) | 절반 넘는 문서에 나오면 음수 → 0.25 × 평균 IDF 로 바꿈 (매뉴얼의 `질문` · `답변` · `:` → −3.045 → 0.371) |
| 교재 p.58 예시 | 1,000단어 중 5번 **1.663** < 50단어 중 3번 **2.154** (avgdl 525) — 교재 말대로 |
| 띄어쓰기 vs MeCab | 질문 5개 중 띄어쓰기 3개(질문을 매뉴얼과 똑같이 쓴 것만) · MeCab **5개** |
| BM25 손계산 | `rank_bm25.get_scores` 와 일치 ('환불하고 싶어요' → 2번 문서 5.102) |
| MeCab 과 코드 | `ERR-502` → `ERR` · `-` · `502`, `SH-M200X` → 5조각 → 매뉴얼에 없는 `ERR-503` 질문에도 ERR-502 문서가 1등 |
| 점수 0 | '프린터 용지가 걸렸어요' → 8문서 모두 0점인데도 2개 반환 |
| `chunk_size=210` | 최대 QA 208자 + 구분자 2 = 딱 맞는 최솟값 (208 · 209 → 9개) |
| 🧪 기술 지원 매뉴얼 10문항 | 희소 · 밀집 · 하이브리드 **모두** 1등이 정답 (문서 8개라 차이가 안 남) |
| RRF | 손계산 = `EnsembleRetriever`($c=60$) · 교재 p.64 순서 예시 0.03252 > 0.03227 > 0.03200 |
| 🧪 연습용 오류 코드 6문서 | 밀집 : 'X-2202' → X-2201 · 'X-2210' → X-2202 (틀림) / 희소 : '컴퓨터 화면이 안 켜져요' → 0점 / 하이브리드 4/5 |
| 고쳐 보기 (15문항) | 수업 방식 · 0점 제외 · 코드 토큰 + 0점 제외 **모두 14/15** — 각각 고친 질문과 새로 틀린 질문이 있다 |
| 수업 챗봇 기록 | 질문 3개(ERR-502 · 강제 재부팅 · DL-900 초기화) — 매번 3개 문서를 모아 넘겼고 답은 모두 근거와 맞음 |
