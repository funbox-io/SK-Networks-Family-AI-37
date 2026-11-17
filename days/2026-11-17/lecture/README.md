# 2026-11-17 수업 실습 — LLM 4일차 : 벡터 저장소 · 검색 도구 · RAG 체인 · PDF 헌법 Q&A

| 파일 | 내용 |
|---|---|
| `RAG_실습07.ipynb` | 수업 필기 원본(내 필기) — 고객 응대 챗봇 : `TextLoader` → 분할(`chunk_size=110`) → `OpenAIEmbeddings` → `Chroma` → `as_retriever(k=1)` → RAG 체인 → `while` 챗봇. 마지막 출력은 `conttext` 오타 오류 |
| `RAG_실습08.ipynb` | 수업 필기 원본(내 필기) — PDF 헌법 Q&A : `PyMuPDFLoader` → 500자 분할 → `Chroma` → 검색 테스트('심각한 질병 순위') → 챗봇(실행 결과 없음) |
| `RAG_실습8_1.ipynb` | 수업 필기 원본(강의본) — 같은 PDF 헌법 Q&A 의 완성본. 검색 테스트 · **챗봇 질문 4번의 실행 결과**가 들어 있다 |
| [`rag_vectorstore_chroma.ipynb`](./rag_vectorstore_chroma.ipynb) | `RAG_실습07` 정리 · 개선본 (교재 p.39~43 · 45~51) — 7단계 → `chunk_size` 110 vs 160 → 임베딩 → **Chroma 폴더 · SQLite 들여다보기** → '폴더가 있으면 불러오기' 함정 → 검색 비교 → 점수 · 데이터 밖 질문 → **FAISS vs Chroma** → **메타데이터 필터** → RAG 체인 · 챗봇 `ask()` |
| [`rag_pdf_constitution.ipynb`](./rag_pdf_constitution.ipynb) | `RAG_실습08` · `RAG_실습8_1` 정리 · 개선본 (교재 p.44) — PDF 불러오기 → 500자 분할의 문제 → **조문(제N조) 단위 청크 + 메타데이터** → 검색 비교(질문 20개) → **점수 기준으로 데이터 밖 질문 거르기** → 수업 기록 분석 → 장(章) 필터 → 출처를 붙인 RAG 체인 |
| [`manual.txt`](./manual.txt) | 실습 데이터 — 고객 응대 매뉴얼 (Day 048 과 같은 파일, QA 10쌍 · 1,399자) |
| `대한민국헌법(헌법)(제00010호)(19880225).pdf` | 실습 데이터 — 국가법령정보센터 헌법 PDF 14쪽 (법령은 저작권 보호 대상이 아니다 · 저작권법 제7조) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 같은 로컬 임베딩으로 계산) |

교재 PDF 는 올리지 않았다. `.env` 는 올리지 않는다(저장소 `.gitignore` 에 포함). 올린 필기 3개에는 API 키 값이 없다(확인함).

## 출력을 읽는 법

| 표시 | 뜻 |
|---|---|
| `# 📼` | **수업 시간에 실제로 실행한 결과**를 필기 원본에서 그대로 옮긴 출력 (매뉴얼 2개 · 헌법 3개) |
| `# ⏳` | API 키가 필요해 **출력이 비어 있는 셀** — 직접 실행 (매뉴얼 2개 · 헌법 1개 : `OpenAIEmbeddings` · `ChatOpenAI` 로 진짜 RAG) |
| `# 🧪` | OpenAI 임베딩 대신 **로컬 한국어 임베딩**(`jhgan/ko-sroberta-multitask`)으로 실제로 검색한 셀, 또는 LLM 대신 **받은 컨텍스트의 첫 줄을 돌려주는 가짜 LLM** 으로 체인 흐름만 돌린 셀. 순위 · 점수는 수업의 `text-embedding-3-small` 과 다를 수 있다 |
| 표시 없음 | 정리 노트북에서 실제로 실행한 셀 (불러오기 · 분할 · DB 파일 들여다보기 · 수업 기록 분석) |

## 실행 방법
1. **설치** : `pip install langchain-community langchain-text-splitters langchain-chroma faiss-cpu pymupdf langchain-openai langchain-huggingface sentence-transformers python-dotenv pandas` (정리 환경 : `langchain-core 1.8.0` · `langchain-chroma 1.1.0` · `chromadb 1.5.9` · `langchain-community 0.4.2` · `faiss-cpu 1.16.0` · `pymupdf 2.1`)
2. **데이터** : `manual.txt` · 헌법 PDF 를 노트북과 **같은 폴더**에. 헌법 노트의 기록 분석은 같은 폴더의 `RAG_실습8_1.ipynb` 를 읽는다
3. **실행** : 맨 위부터 **모두 실행**. 🧪 로컬 임베딩은 처음 한 번 Hugging Face 에서 모델(약 440MB)을 받으므로 인터넷이 필요하고, 그다음부터는 키 없이 돈다(CPU 로 노트북마다 1 ~ 2분)
4. **`# ⏳` 셀** : `.env` 에 `OPENAI_API_KEY="sk-…"`. 임베딩 요금은 매뉴얼 · 헌법 전체를 넣어도 1센트 미만
5. 노트북 폴더에 연습용 DB 폴더(`chroma_db_*` · `faiss_manual`)가 생긴다. 노트북 첫 셀이 매번 지우고 새로 만든다

## 결과 요약
| 실습 | 결과 |
|---|---|
| `chunk_size=110` (수업) | 청크 **25개** = 질문만 10 · 답변 10(그중 끝이 잘린 것 5) · 꼬리 조각 5(`드립니다.` · `수 있습니다.` …) / 160 → 10개 = QA 10쌍 |
| 🧪 `k=1` 검색 '환불 해줘' | 110 → 1등 **`드립니다.`**(꼬리 조각, 답 없음) · 160 → 환불 QA 한 쌍 / 수업 챗봇 기록도 1등이 **질문 줄 하나** |
| Chroma 폴더 | `chroma.sqlite3`(249,856 bytes · 테이블 21개) + UUID 폴더(`data_level0.bin` 321,200 bytes = HNSW 벡터 인덱스) |
| SQLite 안 | `embedding_metadata` = 원문(`chroma:document`) + `source` / `embeddings_queue` = 쓰기 기록, 한 줄에 벡터 3,072 bytes(768 × 4) |
| '폴더가 있으면 불러오기' | 110 으로 만든 뒤 160 으로 고쳐 다시 실행 → **그대로 25개** (옛날 DB) |
| 🧪 점수 (코사인) | 환불 해줘 0.493 · 돈 돌려줘 0.404 · 수료증 0.592 / 매뉴얼에 없는 '회사 주소' 0.338 · '주차' 0.279 — 검색 도구는 항상 k개를 돌려준다 |
| FAISS vs Chroma | 같은 상위 3개 · FAISS 는 `save_local` → `index.faiss` + `index.pkl`, 불러올 때 `allow_dangerous_deserialization=True` 필요 |
| 메타데이터 필터 | `{'category': '결제'}` → 결제 QA 2개만 · `$and` · `$gte` · `$in` 동작 / 조건 두 개를 `$and` 없이 넣으면 Chroma `ValueError` |
| 수업 챗봇 오류 | `conttext` 오타 (코드는 고쳤지만 다시 실행 안 함) · 고쳐도 `response` 를 출력하지 않음 · 종료 확인보다 검색이 먼저 |
| 헌법 PDF | 14쪽 · 20,881자 · `page` 는 0부터 / 500자 분할 52개 중 **27개가 조문 중간에서 시작**(500자 한도 20 · 페이지 경계 7) · 머리글 14개 |
| 조문 단위 | **137개** = 전문 1 + 제1 ~ 130조 + 부칙 6 · 메타데이터 `article` · `chapter` · `part` |
| 🧪 헌법 질문 20개 | 정답 조문이 1등 : 500자 **12** → 조문 **15** / 2등 안 : **13 → 19** |
| 🧪 점수 기준 | 헌법 질문 1등 0.450 ~ 0.726 · 헌법 밖 10개 0.166 ~ 0.262 → 기준 0.30 이면 20/20 통과 · 10/10 걸러짐 |
| 수업 기록 (강의본) | 질문 1 : 1등 청크(제46 ~ 50조)에 답이 없고 **2등**에 제42조 → `k=2` 라서 맞힘 · 답은 모두 조 번호를 밝힘 · 질문 4 는 질문 글자가 기록에 없음 |
| 🧪 장(章) 필터 '임기는 몇 년이야?' | 법원 → 제105조 · 헌법재판소 → 제112조 맞힘 / 국회 · 정부는 2등 안에 제42조 · 제70조 없음 — 필터는 범위만 보장 |
