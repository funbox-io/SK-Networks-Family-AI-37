# 2026-11-05 수업 실습 — 자연어 처리 3일차 : 임베딩 · BoW(Count · TF-IDF) · 코사인 유사도 · 영화 추천

| 파일 | 내용 |
|---|---|
| `nlp_실습6.ipynb` | 수업 필기 원본 — `movies_metadata.csv` 줄거리 → `CountVectorizer` → 코사인 유사도 → 영화 추천 (앞 9,999편) |
| `TF-IDF_정리.md` · `유클리드_거리_정리.md` · `PCA_차원축소_정리.md` · `tokenization-vectorization-embedding.md` · `예시코드_토큰화_벡터화_임베딩.md` | 함께 받은 정리 노트 원본 (영상 「토큰화, 벡터화, 임베딩 무슨 차이일까?」 정리 · 손계산 예제) — 숫자는 아래 노트북에서 다시 실행해 확인 |
| [`bow_count_tfidf.ipynb`](./bow_count_tfidf.ipynb) | 교재 p.46~58 — 설치 · 실행 방법 → 임베딩 · 희소/밀집 → `CountVectorizer` 단어 사전 · 빈도 벡터 → `token_pattern`(한 글자 버림) · OOV → 문서 빈도(DF) 표 → IDF 손계산 = `idf_` → TF×IDF ÷ 길이(l2) → `TF-IDF_정리.md` · `예시코드` 파트 2 확인 |
| [`text_similarity_cosine.ipynb`](./text_similarity_cosine.ipynb) | 교재 p.59~62 · 66 — 설치 · 실행 방법 → 코사인 손계산 vs `cosine_similarity` → Count / TF-IDF 유사도 행렬 → BoW 각도 0~90° → 챗봇 예문 (어절 vs Kiwi 형태소) → 유클리드 vs 코사인 → tiktoken · Kiwi 확인 → 문장 임베딩(768차원) vs TF-IDF → PCA |
| [`movie_recommendation.ipynb`](./movie_recommendation.ipynb) | `nlp_실습6` 정리 · 개선본 (교재 p.63~65) — 설치 · 실행 방법 → 데이터 점검(깨진 행 · 중복 · 2017년 이후) → 결측 · 자리표시 줄거리 제거 → **희소 행렬 그대로** → 추천 함수(자기 자신 · 같은 제목 · 없는 제목 처리) → 원본 결과 재현 → Count vs TF-IDF |
| [`data/movies_overview.csv.gz`](./data/) | Kaggle The Movies Dataset `movies_metadata.csv`(34MB)에서 `id · title · overview · release_date · status` 5개 열만 뽑아 압축 (7MB, 45,466행) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 예문 · 데이터로 직접 만든 것) |

## 실행 방법
1. **설치** : `pip install scikit-learn pandas kiwipiepy sentence-transformers tiktoken`
   - `scikit-learn` · `pandas` 는 Colab 기본 포함 — `bow_count_tfidf` · `movie_recommendation` 은 **추가 설치 없이** 돈다
   - `text_similarity_cosine` 의 밀집 임베딩은 `sentence-transformers` 가 Hugging Face 에서 한국어 모델 `jhgan/ko-sroberta-multitask`(약 440MB)를 처음 한 번 받는다 → **인터넷 필요**, GPU 는 필요 없음
2. **데이터** : 영화 추천 노트북은 노트북과 같은 폴더의 `movies_metadata.csv`(Kaggle 원본) 또는 `data/movies_overview.csv.gz` 를 자동으로 찾는다. 나머지 두 노트북은 받을 파일 없음
3. **실행** : 노트북을 열고 맨 위부터 **[런타임] → [모두 실행]**. 각 노트북 0절에 Colab 용 설치 셀(주석 처리)이 있다
4. 순서 : `bow_count_tfidf` → `text_similarity_cosine` → `movie_recommendation`

## 결과 요약
| 실습 | 결과 |
|---|---|
| 교재 단어 사전 (4문장) | `{'고프다':0, '공부':1, '공부해야지':2, '나는':3, …, '해야겠다':9}` · `'나는 배가 고프다'` → `[[1 0 0 1 0 0 0 1 0 0]]` (교재와 같음) |
| IDF (`smooth_idf`) | df 1 → **1.916** · df 2(`내일` · `점심`) → **1.511** · 손계산 = `idf_` |
| TF-IDF 값 | 교재 공식 TF×IDF(1.916 …) ÷ 문장 벡터 길이 = `toarray()` 값(0.577 · 0.618 …) |
| 문장2 · 4 유사도 | Count **0.333** → TF-IDF **0.256** (`점심` 의 무게가 줄어서) |
| 챗봇 예문 (같은 뜻) | 어절 Count **0.289** → Kiwi 형태소 **0.721** |
| 같은 문장 × 2 | 코사인 1.0 · 유클리드 1.732 (= 다른 문장 `내일 공부` 와 같은 거리) |
| 토큰 수 `모두의 한국어 텍스트 분석 with 파이썬` (23글자) | r50k 43 · cl100k 22 · **o200k 14** |
| 도서 제목 7개 | 딥러닝 1 ↔ 2 : TF-IDF 1.0 (한 글자 `1` `2` 버림) · 한 글자 포함 0.653 · 임베딩 0.90 |
| 검색 `신경망 처음 배우는 책` | TF-IDF 전부 0 · 임베딩 1위 `밑바닥부터 시작하는 딥러닝 1` (0.441) |
| 영화 데이터 | 45,466행 = 깨진 행 3 · 중복 id 30 · 2017-08 이후 40 포함 → 결측(954 · 6) · 자리표시 줄거리 149 제거 → **44,357편** |
| 행렬 크기 | 44,357 × 75,827 — `.toarray()` 26.9GB vs 희소 행렬 14.7MB · 전체 유사도 표 15.7GB |
| 원본 재현 (앞 9,999편) | `Toy Story 2 0.412393` · `The Champ 0.245402` (원본과 같음) |
| `Toy Story` 추천 (전체) | Count : Toy Story 3 0.436 · Toy Story 2 0.412 / TF-IDF : 0.532 · 0.472 · 이름(Andy · Woody)만 같은 영화도 섞임 |
| Count vs TF-IDF 상위 10편 겹침 | Toy Story 9 · GoldenEye 6 · The Dark Knight 5 · Titanic 5 · Finding Nemo 1 |
