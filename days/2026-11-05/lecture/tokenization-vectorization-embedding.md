# 토큰화 · 벡터화 · 임베딩, 무슨 차이일까?

> NLP와 LLM 텍스트 데이터 기초 용어를 실습으로 이해하는 튜토리얼
> 출처 영상: [오늘코드 todaycode – 토큰화, 벡터화, 임베딩 무슨 차이일까?](https://youtu.be/9rbm29bCjaQ) (33분)

---

## 목차

1. [왜 텍스트를 숫자로 바꿔야 할까?](#1-왜-텍스트를-숫자로-바꿔야-할까)
2. [한눈에 보는 세 개념](#2-한눈에-보는-세-개념)
3. [토큰화 (Tokenization)](#3-토큰화-tokenization)
4. [실습 준비 (Google Colab)](#4-실습-준비-google-colab)
5. [벡터화 (Vectorization) – BoW와 TF-IDF](#5-벡터화-vectorization--bow와-tf-idf)
6. [임베딩 (Embedding) – OpenAI API로 만들기](#6-임베딩-embedding--openai-api로-만들기)
7. [유사도 측정 – 코사인 vs 유클리드](#7-유사도-측정--코사인-vs-유클리드)
8. [차원 축소와 시각화](#8-차원-축소와-시각화)
9. [TensorFlow Embedding Projector로 3D 탐색](#9-tensorflow-embedding-projector로-3d-탐색)
10. [임베딩 모델의 종류](#10-임베딩-모델의-종류)
11. [임베딩 결과는 어디에? – 벡터 DB](#11-임베딩-결과는-어디에--벡터-db)
12. [최종 정리](#12-최종-정리)

---

## 1. 왜 텍스트를 숫자로 바꿔야 할까?

컴퓨터는 본질적으로 **숫자 연산 장치**입니다. 텍스트 자체로는 계산하거나 패턴을 찾을 수 없어요.

- ChatGPT 같은 생성형 AI에 글로 질문해도, 내부에서는 전부 **숫자로 변환되어 처리**됩니다.
- 그래서 사람의 언어를 컴퓨터가 **계산·비교·학습**할 수 있는 숫자(주로 벡터) 형태로 바꿔야 합니다.
- 이렇게 변환된 데이터가 머신러닝(딥러닝 포함) 모델의 **입력**이 됩니다.

> 💡 참고: 딥러닝은 머신러닝의 한 종류로, 신경망(Neural Network) 모델을 쓰는 방식을 따로 부르는 이름입니다.

---

## 2. 한눈에 보는 세 개념

텍스트 → 숫자 변환은 보통 아래 순서로 **점진적으로 발전**합니다.

```
"오늘 날씨가 좋아요"
        │
        ▼  ① 토큰화: 의미 있는 최소 단위로 쪼개기
["오늘", "날씨", "가", "좋아요"]
        │
        ▼  ② 벡터화: 쪼갠 단위를 숫자 벡터로 표현
[0, 1, 1, 0, 1, 0, 0, ...]   ← 0이 많은 희소 벡터
        │
        ▼  ③ 임베딩: 문맥적 의미까지 담은 저차원 밀집 벡터
[0.021, -0.113, 0.087, ...]   ← 값이 빼곡한 밀집 벡터
```

| 구분 | 하는 일 | 대표 기법 | 결과물 특징 |
|---|---|---|---|
| **토큰화** | 텍스트를 단어·형태소·서브워드 단위로 **분해** | 공백 분리, 형태소 분석, BPE, WordPiece | 토큰 리스트 |
| **벡터화** | 토큰을 **숫자 벡터**로 표현 | Bag of Words, TF-IDF | 고차원 **희소(Sparse)** 벡터, 의미 정보 약함 |
| **임베딩** | 단어·문장의 **문맥적 의미와 유사도**까지 반영 | Word2Vec, GloVe, BERT, text-embedding-3-small | 저차원 **밀집(Dense)** 벡터, 의미가 가까우면 공간상 가까움 |

> 🧱 비유: 토큰화는 **레고 건물을 개별 블록으로 분해**하는 것, 벡터화는 각 블록에 **번호표**를 붙이는 것, 임베딩은 블록들을 **비슷한 것끼리 가까이 놓이도록 공간에 배치(심기)** 하는 것입니다.

---

## 3. 토큰화 (Tokenization)

### 3-1. 정의

> 주어진 텍스트를 **분석 목적에 맞게 의미 있는 단위(토큰)로 나누는 과정**

기계가 처리할 수 있는 **기본 단위**를 만드는 단계로, 이후 벡터화·임베딩의 출발점입니다. 단어 단위, 의미 단위, 빈도 단위 등 **어떻게 나누느냐에 따라 방법이 다양**합니다.

### 3-2. 토큰화 시 고려 사항

- 구두점(.,!?) 처리
- 대소문자 정규화 (`Python` → `python`)
- 불용어(stopwords, 의미 없는 단어) 제거
- 형태소 분석

### 3-3. 토큰화 방식

**① 공백·구두점 기준 토큰화**

가장 단순한 방법. 띄어쓰기와 특수문자로 분리합니다. 영어에선 잘 동작하지만 한국어는 조사·어미가 붙어 있어 한계가 있어요.

```python
text = "모두의 한국어 텍스트 분석 with 파이썬"
tokens = text.split()
# ['모두의', '한국어', '텍스트', '분석', 'with', '파이썬']
```

**② 형태소 분석 기반 토큰화 (한국어에 중요!)**

한국어는 조사·어미를 고려해야 의미를 제대로 살릴 수 있습니다.

> "아버지가 방에 들어가신다" ↔ "아버지 가방에 들어가신다"
> 띄어쓰기·형태소를 잘못 처리하면 의미가 완전히 달라집니다.

대표 한국어 형태소 분석기: **Okt(KoNLPy)**, **Mecab**, **Kiwi** 등

```python
# 예시: Kiwi 형태소 분석기
# !pip install kiwipiepy
from kiwipiepy import Kiwi
kiwi = Kiwi()
print([t.form for t in kiwi.tokenize("아버지가 방에 들어가신다")])
# ['아버지', '가', '방', '에', '들어가', '시', 'ㄴ다']
```

**③ 서브워드(Subword) 토큰화 – LLM이 쓰는 방식**

단어를 더 작은 조각으로 나누고, **자주 등장하는 글자 시퀀스**를 하나의 토큰으로 묶습니다.

- 대표 알고리즘: **BPE(Byte Pair Encoding)**, **WordPiece**, **SentencePiece**
- 트랜스포머 계열 모델(GPT, BERT 등)이 사용
- 장점: 사전에 없는 단어(**OOV, Out-Of-Vocabulary**)도 서브워드 조합으로 표현 가능 → 희귀 단어나 형태 정보 반영에 유리
- 트랜스포머 토크나이저는 **공백도 토큰에 포함**해서 처리하기도 합니다.

### 3-4. 직접 확인해 보기 – OpenAI Tokenizer

[OpenAI Tokenizer](https://platform.openai.com/tokenizer) 페이지에서 로그인 없이 토큰화를 체험할 수 있습니다.

- 영상 예시: `모두의 한국어 텍스트 분석 with 파이썬` → **26글자, 11토큰** (GPT-4o 계열 기준)
- **모델마다 토큰화 방식이 다릅니다.** 구형 GPT-3 / GPT-3.5 토크나이저에서는 한글이 깨져(�) 보이고 잘게 쪼개지는 반면, GPT-4o 계열에서는 훨씬 깔끔하게 토큰화됩니다.
- 영어 단어(`Python`, `with`)는 대체로 한 단어가 하나의 토큰으로 잘 묶입니다.

코드로는 `tiktoken` 라이브러리로 같은 결과를 볼 수 있어요.

```python
# !pip install tiktoken
import tiktoken
enc = tiktoken.get_encoding("o200k_base")  # GPT-4o 계열 인코딩
ids = enc.encode("모두의 한국어 텍스트 분석 with 파이썬")
print(len(ids), [enc.decode([i]) for i in ids])
```

---

## 4. 실습 준비 (Google Colab)

영상의 실습은 Google Colab에서 진행합니다. (영상 설명란에 시연 Colab 링크가 있어요.)

### 4-1. 라이브러리 설치

```python
!pip install openai koreanize-matplotlib
```

> 💡 **koreanize-matplotlib**: matplotlib 시각화에서 한글 폰트가 깨지는 문제를 import 한 줄로 해결해 주는 라이브러리. (일본어용 japanize-matplotlib를 한국어로 만든 것) 영상 제작자 강추 👍

### 4-2. 라이브러리 로드 & API 키

```python
import openai, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
from google.colab import userdata

# Colab 왼쪽 🔑 '보안 비밀'에 OPENAI_API_KEY 등록해 두고 불러오기
client = openai.OpenAI(api_key=userdata.get("OPENAI_API_KEY"))
```

> ⚠️ API 키를 코드에 직접 적지 말고 Colab **보안 비밀(Secrets)** 기능을 쓰세요.

### 4-3. 실습 데이터

영상에서는 한빛미디어 최근 출간 **도서 제목 50개**를 사용합니다. 목표는 *"제목만으로도 의미가 비슷한 책끼리 가까이 위치하는가?"* 를 확인하는 것.

```python
texts = [
    "NLP와 LLM 실전 가이드",
    "밑바닥부터 시작하는 딥러닝 1",
    "밑바닥부터 시작하는 딥러닝 5",
    "AI를 위한 필수 수학",
    "개발자를 위한 필수 수학",
    "혼자 공부하는 머신러닝+딥러닝",
    # ... 총 50개
]
len(texts)  # 50
```

---

## 5. 벡터화 (Vectorization) – BoW와 TF-IDF

### 5-1. Bag of Words (단어 가방)

가장 단순한 벡터화 방법입니다.

1. 문서를 토큰화(띄어쓰기 단위)
2. 전체 문서에 등장한 모든 단어로 **어휘 사전(vocabulary)** 생성
3. 각 문서에 사전의 단어가 **등장하는지/몇 번 등장하는지**를 숫자로 기록

```python
from sklearn.feature_extraction.text import CountVectorizer

corpus = ["코로나 확진자 증가", "지하철 승강장 혼잡", "코로나 지하철 방역"]
cv = CountVectorizer()
bow = cv.fit_transform(corpus)
pd.DataFrame(bow.toarray(), columns=cv.get_feature_names_out())
```

- **N-gram**: 토큰을 2개, 3개씩 묶어서 쓰는 방식. 단어 단위로도, 글자(character) 단위로도 묶을 수 있습니다. (`ngram_range=(1, 2)`)
- 불용어 제거 옵션도 줄 수 있어요.

### 5-2. TF-IDF (가중치 적용)

BoW는 "등장했다/안 했다"만 보지만, TF-IDF는 **그 단어가 얼마나 중요한지**를 가중치로 반영합니다.

- **TF (Term Frequency)**: 이 문서에서 단어가 얼마나 자주 나오는가
- **IDF (Inverse Document Frequency)**: 전체 문서에서 얼마나 드물게 나오는가

> 예) "코로나"라는 단어가 **다른 문서엔 거의 없고 이 문서에만 자주** 나온다면 → 이 문서를 대표하는 **중요한 단어** → 높은 가중치
> 반대로 모든 문서에 흔하게 나오는 단어는 → 낮은 가중치

같은 "한 번 등장"이라도, **어디서 등장했느냐**에 따라 값이 달라진다는 것이 BoW와의 차이입니다.

### 5-3. 도서 제목 TF-IDF 벡터화 실습

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()          # 내부에서 토큰화(띄어쓰기) + 벡터화 + TF-IDF 가중치까지 한 번에
X = tfidf.fit_transform(texts)

df = pd.DataFrame(X.toarray(), columns=tfidf.get_feature_names_out())
df.style.background_gradient()     # 값이 클수록 진하게 표시
```

결과를 보면 각 행(책 50권)마다 어휘 사전 크기만큼의 열이 생기고, 대부분이 **0**이며 일부만 `0.39`, `0.26` 같은 값을 가집니다.

> ✅ 정리: **토큰화**는 띄어쓰기로 나눈 것, **벡터화**는 그걸 숫자로 바꾼 것.
> ⚠️ 한계: 0이 너무 많은 **희소 벡터**라 문서 간 관계(의미적 유사성)를 파악하기 어렵습니다.

---

## 6. 임베딩 (Embedding) – OpenAI API로 만들기

### 6-1. 정의

> 단어·문장의 **문맥적 의미와 유사도**를 반영해 **저차원의 연속적인 밀집 벡터**로 표현하는 것

- 의미가 비슷한 텍스트는 벡터 공간에서 **가까운 위치에 매핑**됩니다.
- 단순 빈도를 넘어 텍스트의 **잠재적 의미(Latent Semantics)** 를 벡터 공간에 투영합니다.
- "임베딩(embedding)" = 말 그대로 **고차원 공간에 단어를 '심어 주는' 것**.

### 6-2. 희소 벡터 vs 밀집 벡터

| | 희소 벡터 (Sparse) | 밀집 벡터 (Dense) |
|---|---|---|
| 예 | BoW, TF-IDF | 임베딩 |
| 값 | 대부분 0 | 0 없이 값이 빼곡함 |
| 차원 | 어휘 사전 크기만큼 (매우 큼) | 고정된 크기 (예: 1,536) |
| 의미 관계 | 파악 어려움 | 파악 쉬움 |

### 6-3. OpenAI `text-embedding-3-small`로 임베딩 생성

```python
resp = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts,
)
embeddings = np.array([d.embedding for d in resp.data])
embeddings.shape   # (50, 1536)  → 책 50권 × 1,536차원
```

### 6-4. Embedding Projector용 TSV 저장

임베딩 값과 메타데이터(책 제목)를 **탭(\t)으로 구분**한 TSV 파일 두 개로 저장합니다.

```python
# 임베딩 벡터
with open("embedding.tsv", "w") as f:
    for vec in embeddings:
        f.write("\t".join(map(str, vec)) + "\n")

# 메타데이터 (각 줄이 embedding.tsv의 같은 줄과 대응)
with open("metadata.tsv", "w") as f:
    for t in texts:
        f.write(t + "\n")
```

Colab 왼쪽 📁 파일 탭에 `embedding.tsv`, `metadata.tsv`가 생기면 다운로드해 둡니다.

### 6-5. 히트맵으로 들여다보기

```python
plt.figure(figsize=(12, 6))
sns.heatmap(embeddings, cmap="viridis")   # 밝을수록 큰 값, 어두울수록 작은 값
```

TF-IDF와 달리 **빈칸 없이 빽빽하게** 채워진 것을 볼 수 있습니다. 하지만 숫자만 봐서는 의미를 알기 어렵죠 → 그래서 **유사도 계산**과 **차원 축소 시각화**를 합니다.

> 🎓 참고: 영상에서 소개한 **RNN Explainer**는 영어 문장을 임베딩한 뒤 LSTM으로 감성(긍정/부정)을 분석하는 과정을 시각적으로 보여 줍니다. 여기서도 임베딩은 밀집 벡터로 표현됩니다.

---

## 7. 유사도 측정 – 코사인 vs 유클리드

벡터 공간에 심어진 단어들 사이의 **거리나 각도**를 구하면 의미가 비슷한지 알 수 있습니다.

| 방법 | 기준 | 특징 |
|---|---|---|
| **유클리드 거리** | 두 점 사이의 **직선 거리** | 고차원에서는 어느 각도에서 보느냐에 따라 가깝고 먼 정도가 왜곡될 수 있음 |
| **코사인 유사도** | 두 벡터 사이의 **각도(방향)** | 같은 방향인지를 보므로 의미 유사도 비교에 더 적합 → **가장 많이 사용** |

- 코사인 유사도는 **1에 가까울수록 유사**합니다.
- GPT 같은 트랜스포머 기반 모델 생태계에서도 단어/문장 간 유사도를 계산할 때 코사인 방식을 널리 사용합니다.

```python
from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(embeddings)        # (50, 50) 유사도 행렬
plt.figure(figsize=(14, 12))
sns.heatmap(sim, xticklabels=texts, yticklabels=texts, cmap="coolwarm")
```

**영상 실습 결과 (제목만으로 계산!)**

- `밑바닥부터 시작하는 딥러닝 1 ~ 5` 시리즈끼리 → **0.84 ~ 0.89**로 매우 높은 유사도
- `AI를 위한 필수 수학` ↔ `개발자를 위한 필수 수학` → 높은 유사도
- `NLP와 LLM 실전 가이드` → 이번 50권 안에서는 특별히 유사도가 높은 책이 없음

> 💡 TF-IDF 벡터로도 코사인 유사도를 구할 수 있지만, 임베딩을 쓰면 **더 의미 있는 유사도**를 얻을 수 있습니다.

---

## 8. 차원 축소와 시각화

1,536차원은 눈으로 볼 수 없으니 **2차원/3차원으로 축소**해서 그립니다.

```python
from sklearn.decomposition import PCA

xy = PCA(n_components=2).fit_transform(embeddings)

plt.figure(figsize=(12, 10))
plt.scatter(xy[:, 0], xy[:, 1])
for (x, y), t in zip(xy, texts):
    plt.annotate(t, (x, y), fontsize=8)
plt.show()
```

**관찰 결과**

- `밑바닥부터 시작하는 딥러닝 1~5`가 한곳에 **몰려 있음**
- `NLP와 LLM 실전 가이드` 근처에는 `AI 시대의 프로그래머`, `GPT API를 이용한 인공지능 앱 개발`, `엑셀 대신 파이썬으로 업무 자동화` 등이 위치
- `AI를 위한 필수 수학`, `개발자를 위한 필수 수학`도 서로 가까움

> ⚠️ 차원 축소는 **어느 각도에서 압축하느냐에 따라 전혀 다른 그림**이 나올 수 있습니다. 2D보다 3D가 더 잘 보이니 다음 단계로!

차원 축소 기법: **PCA**, **t-SNE**, 토픽 모델링에서 쓰는 **잠재 의미 분석(LSA)** 등

---

## 9. TensorFlow Embedding Projector로 3D 탐색

[TensorFlow Embedding Projector](https://projector.tensorflow.org/)는 웹에서 바로 쓸 수 있는 임베딩 3D 시각화 도구입니다.

### 사용 방법

1. 사이트 접속 (기본으로 IMDb 데이터를 Word2Vec으로 벡터화한 예시가 떠 있음)
2. 왼쪽 패널의 **Load** 클릭
3. `embedding.tsv` 업로드 (벡터)
4. `metadata.tsv` 업로드 (라벨)
5. 내 데이터로 바뀐 3D 공간에서 점을 클릭해 탐색

### 확인 포인트

- 화면 정보: **Points 50, Dimension 1536** → PCA로 X·Y·Z 3축으로 줄여 표시
- `밑바닥부터 시작하는 딥러닝 1` 클릭 → 2·3·4·5권이 가장 가깝게 나열되고, 그다음 `혼자 공부하는 머신러닝+딥러닝` 등이 이어짐
- 오른쪽 패널에서 **코사인 / 유클리드** 거리 기준을 바꿔 볼 수 있음 (이 예시는 둘 다 비슷한 결과)

> 🌌 이게 바로 임베딩입니다: 의미를 살려 공간에 심어 두었기 때문에 **가까움 = 의미가 비슷함**을 눈으로 확인할 수 있어요.

---

## 10. 임베딩 모델의 종류

| 분류 | 예시 | 특징 |
|---|---|---|
| **정적 단어 임베딩** | Word2Vec (CBOW, Skip-gram), GloVe | 단어마다 고정된 벡터 1개 |
| **문맥적 임베딩** | ELMo, BERT 등 트랜스포머 계열 | 같은 단어라도 문맥에 따라 벡터가 달라짐 |
| **API형 임베딩 모델** | OpenAI `text-embedding-3-small` | 호출만 하면 바로 사용 (유료) |

더 많은 모델은 [Hugging Face](https://huggingface.co/models)에서 태스크별로 찾을 수 있어요. 예를 들어 **"Korean embedding"** 으로 검색하면 한국어 특화 임베딩 모델들이 나옵니다.

> 💡 토큰화 방식과 임베딩만 잘 골라도 자연어 처리에서 훨씬 더 좋은 결과를 얻을 수 있습니다.

### 임베딩 활용처

감성 분석 · 유사도 분석 · 검색 · 군집화(클러스터링) · 추천 등

---

## 11. 임베딩 결과는 어디에? – 벡터 DB

- OpenAI 임베딩 API는 **무료가 아니라 과금**됩니다.
- 매번 임베딩할 수 없으니 결과를 어딘가에 **저장**해 둬야 하죠 → 이것이 **벡터 데이터베이스(Vector DB)** 입니다.
- 질문이 들어오면 벡터 DB에서 **유사도 검색**으로 관련 문서를 찾아 LLM 요청에 함께 넣어 → 요약, FAQ 생성 등 다양하게 활용 (이것이 **RAG**의 핵심 흐름)

```
문서 ──임베딩──▶ 벡터 DB 저장
질문 ──임베딩──▶ 유사도 검색 ──▶ 관련 문서 + 질문 ──▶ LLM ──▶ 답변
```

---

## 12. 최종 정리

| 단계 | 한 줄 정의 | 키워드 |
|---|---|---|
| 🔪 **토큰화** | 텍스트를 의미 있는 최소 단위로 **분해** | 공백, 형태소, 서브워드(BPE), OOV |
| 🔢 **벡터화** | 토큰을 **숫자 벡터**로 표현 | BoW(빈도), TF-IDF(가중치), 희소 벡터 |
| 🌌 **임베딩** | 의미·문맥을 보존해 **고차원 공간에 심기** | 저차원 밀집 벡터, 코사인 유사도, 벡터 DB |

**예시 한 문장으로 흐름 따라가기**

```
"오늘 날씨가 좋아요, 산책하기 좋은 날"
 → 토큰화: 형태소/서브워드 단위로 나누기
 → 벡터화: 간단한 분석·키워드 추출엔 TF-IDF
 → 임베딩: 저차원 밀집 벡터 생성 → 감성 분석, 유사도, 검색, 군집화에 활용
```

> 세 용어는 비슷하게 쓰이지만 **분명히 다른 의미**를 가집니다. 이 차이를 알고 있으면 LLM을 훨씬 더 잘 활용할 수 있습니다.

---

### ✅ 셀프 체크

- [ ] 토큰화·벡터화·임베딩의 차이를 한 문장씩 설명할 수 있다
- [ ] 한국어 토큰화에서 형태소 분석이 왜 중요한지 예를 들 수 있다
- [ ] BoW와 TF-IDF의 차이를 "코로나" 예시로 설명할 수 있다
- [ ] 희소 벡터와 밀집 벡터의 차이를 안다
- [ ] 유사도 계산에 코사인을 더 많이 쓰는 이유를 안다
- [ ] Embedding Projector에 내 임베딩을 올려 볼 수 있다

### 🔗 참고 링크

- 영상: https://youtu.be/9rbm29bCjaQ
- OpenAI Tokenizer: https://platform.openai.com/tokenizer
- TensorFlow Embedding Projector: https://projector.tensorflow.org/
- Hugging Face Models: https://huggingface.co/models

> 📝 본문의 코드는 영상 시연 흐름을 따라 재구성한 예시입니다. 원본 실습 코드는 영상 설명란의 Colab 링크를 참고하세요.
