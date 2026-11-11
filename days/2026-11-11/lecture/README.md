# 2026-11-11 수업 실습 — 자연어 처리 7일차 : SentenceTransformer · 문장 유사도 · 영화 추천 · 챗봇

| 파일 | 내용 |
|---|---|
| `nlp_실습11.ipynb` | 수업 필기 원본 — SentenceTransformer 로 영어 · 한국어 · 4개 언어 문장 유사도 |
| `nlp_실습12.ipynb` | 수업 필기 원본 — ChatBotData 예상 질문 임베딩 → 코사인 유사도 → 답변 고르는 챗봇 |
| `nlp_실습6_영화추천서비스.ipynb` | 수업 필기 원본 — CountVectorizer 영화 추천 수정본 (`[0:10000]`, 정리는 [Day 041](../../2026-11-05/lecture/movie_recommendation.ipynb)) |
| [`sentence_similarity_sbert.ipynb`](./sentence_similarity_sbert.ipynb) | `nlp_실습11` 정리 · 개선본 (교재 p.115~117) — 설치 · 실행 방법 → 영어 유사도 → **평균 풀링 손계산 = `encode()`** → 다국어 vs 한국어 모델 → 4개 언어(e5) · 점수 범위 → 문장 학습 안 한 BERT 평균과 비교 |
| [`movie_recommendation_sbert.ipynb`](./movie_recommendation_sbert.ipynb) | `nlp_실습6_영화추천서비스` 정리 + 교재 p.117 '문장 유사도를 이용한 추천' — CountVectorizer vs SentenceTransformer · 상위 10편 겹침 · 줄거리로 직접 검색 |
| [`chatbot_similarity.ipynb`](./chatbot_similarity.ipynb) | `nlp_실습12` 정리 · 개선본 (교재 p.119~120) — 설치 · 실행 방법 → 데이터 · label 뜻 · 중복 질문 → **배치 임베딩** → 행렬 곱 한 번으로 유사도 → 상위 5 → 챗봇 함수(기준값 미만이면 되묻기) → 기준값 정하기 |
| [`data/ChatBotData.csv`](./data/) | 한국어 챗봇 데이터 Q · A · label 11,823줄 ([songys/Chatbot_data](https://github.com/songys/Chatbot_data), MIT 라이선스) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 모델 · 데이터로 직접 만든 것) |

영화 데이터는 [Day 041 폴더의 `data/movies_overview.csv.gz`](../../2026-11-05/lecture/data/)를 그대로 읽는다(다시 올리지 않음). 교재 PDF 는 올리지 않았다.

## 실행 방법
1. **설치** : `pip install sentence-transformers scikit-learn pandas` (Colab 은 기본 포함)
2. **모델** : 첫 실행 때 Hugging Face 에서 자동 다운로드 → **인터넷 필요** — `all-MiniLM-L12-v2`(133MB) · `paraphrase-multilingual-MiniLM-L12-v2`(471MB) · `ddobokki/klue-roberta-base-nli-sts`(442MB) · `intfloat/multilingual-e5-large-instruct`(1.1GB) · `jhgan/ko-sroberta-multitask`(442MB) · `klue/bert-base`(비교용)
3. **데이터** : `ChatBotData.csv` 는 노트북 폴더 또는 `data/` (없으면 원 저장소에서 읽음) · 영화 데이터는 Day 041 폴더에서 자동으로
4. **실행** : 노트북을 열고 맨 위부터 **[런타임] → [모두 실행]**. 각 노트북 0절에 설치 셀(주석 처리)이 있다
5. **시간 (CPU)** : 문장 유사도 1~2분 · 챗봇 질문 11,823개 임베딩 약 2분(이 노트 실행 124초, 다음부터는 저장한 `.npy` 를 불러옴) · 영화 줄거리 1만 개 약 3~4분(203초). Colab GPU 면 각각 수십 초

## 결과 요약
| 실습 | 결과 |
|---|---|
| 영어 (all-MiniLM-L12-v2) | 과학자 두 문장 **0.896** (원본과 같음) · 항공권 문장과 0.07 |
| 평균 풀링 손계산 | 토큰 벡터 (12, 384) → 패딩 빼고 평균 → 정규화 = `encode()` 결과와 같음 |
| 한국어 퇴사 질문 쌍 | 다국어 MiniLM 0.918 / 무관 −0.140 · 한국어 KLUE-RoBERTa 0.961 / 무관 −0.061 |
| 4개 언어 같은 뜻 (e5-large-instruct) | 0.926~0.957 · 무관한 한국어 문장도 0.69~0.75 → 점수는 같은 모델 안에서 순위로 |
| 문장 학습 안 한 klue/bert-base 평균 | 같은 뜻 0.905 · 무관 **0.47** (구분 약함) vs 문장 학습 모델 0.961 · −0.06 |
| 영화 `Toy Story` (1만 편) | Count : Toy Story 2 0.412 · The Champ 0.245 / 문장 임베딩 : Toy Story 2 **0.786** · Elf · Pinocchio |
| 두 방법 상위 10편 겹침 | GoldenEye 6편 (둘 다 007) · Jumanji 0편 |
| 줄거리로 검색 `A group of toys come to life …` | 문장 임베딩 : Dolls · Toy Story · Pinocchio · Toy Story 2 / Count : 관계없는 영화 |
| 챗봇 데이터 | 11,823줄 · label 0 일상 5,290 · 1 이별 3,570 · 2 사랑 2,963 · 같은 질문 161줄 |
| `배가 고파요` | 1위 `배가 너무 고파`(0.934) → `뭐 좀 챙겨드세요.` (원본과 같음) |
| 기준값 0.5 | 일상 질문 10/10 답함 · 데이터 밖 질문 8/10 되물음 (`비트코인 채굴 원리` 0.78 · `서울에서 부산까지 거리` 0.65 는 통과) |
