---
day: 016
date: 2026-09-29
weekday: 화
week: 5
phase: 데이터 분석과 머신러닝/딥러닝
title: Numpy와 Pandas — 배열 연산, DataFrame 인덱싱 · 파생 변수 · value_counts
tags: python, numpy, pandas, ndarray, array, 인덱싱, 슬라이싱, DataFrame, Series, Index, read_csv, loc, 파생변수, CTR, ROAS, value_counts, 데이터분석
---

# Day 016 · 2026-09-29 (화)

`데이터 분석과 머신러닝/딥러닝` · 5주차

> **한 줄 요약** — 숫자 계산용 `numpy` 와 표 계산용 `pandas` 의 기본기를 익히고, 광고 성과 데이터 5,000건으로 인덱싱 · 파생 변수 · 빈도수 세기를 직접 해봤다.

📂 실습 노트북 → [`lecture/numpy_pandas.ipynb`](./lecture/numpy_pandas.ipynb) · 실습 데이터 [`lecture/ad_performance.csv`](./lecture/ad_performance.csv) (5,000행 × 9열)
📖 교재 `데이터분석` p.1~22

---

## 0. 데이터 분석이란

데이터를 **수집 · 정제 · 해석**해 숨겨진 패턴과 인사이트를 찾고, 이를 바탕으로 미래를 예측하고 최적의 의사결정을 내리는 일련의 과정.

| 단계 | 하는 일 |
|------|---------|
| ① 데이터 수집 | 분석에 필요한 데이터 확보 |
| ② 데이터 전처리(preprocessing) | 분석에 적합한 형태로 만들어 신뢰도를 높이는 작업 |
| ③ 데이터 탐색 | 그래프·통계로 데이터의 특징과 패턴 파악 |
| ④ 모델링 | 수학·통계로 관계를 파악해 예측·설명할 규칙(Model)을 만듦 |
| ⑤ 분석 모델 평가 | 만든 모델이 쓸 만한지 확인 |

오늘은 ①~③에 쓰는 도구인 **numpy** 와 **pandas** 를 다뤘다.

---

## 1. Numpy — 숫자 계산용

**수학적 계산을 위한 라이브러리.** 자료형은 다차원 배열 `ndarray` 다.

| | python list | numpy 배열 |
|---|---|---|
| 존재 목적 | 정수·실수·문자열까지 **여러 자료형을 섞어** 담기 | **숫자 한 종류**를 대규모로 묶어 빠르게 처리 |
| 요소별 수학 연산 | **불가능** | **가능** (최대 장점) |
| 처리 방식 | 하나씩 처리 | **동시에** 처리 |

```python
import numpy as np          # 앞으로 np 라는 이름으로 부른다

total = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

arr = np.array(total)       # 리스트 -> 배열
print(arr.ndim, arr.shape, arr.dtype)   # 2 (3, 3) int64
```

차원은 **대괄호가 몇 겹인지**로 정해진다. 1차원은 선, 2차원은 행(가로)×열(세로), 3차원은 깊이×행×열.

### 요소별 연산 — 리스트와 가장 다른 점

```python
list_data1 + list_data2     # [1, 2, 3, 4, 5, 6]  <- 이어 붙이기
arr1 + arr2                 # [5 7 9]             <- 값끼리 더하기

list_data1 * 3              # [1,2,3,1,2,3,1,2,3] <- 세 번 반복
arr1 * 3                    # [3 6 9]             <- 각 값에 3을 곱함
```

`np.mean()` 은 파이썬으로 직접 구한 평균과 값은 같지만 **돌려주는 자료형이 다르다** (`float` vs `numpy.float64`).

### 인덱싱

| 자료형 | 쓰는 법 |
|--------|---------|
| 리스트 | `list_data[행][열]` |
| 배열 | `arr[행][열]` 또는 **`arr[행, 열]`** |

리스트는 대괄호를 두 번 써야 하지만, 배열은 `[행, 열]` 로 한 번에 쓸 수 있다.

### 슬라이싱

**1차원** — `배열[start : stop]` → start 부터 **stop 바로 앞까지** (`start <= x < stop`)
**2차원** — `배열[행 start : 행 stop, 열 start : 열 stop]`

```python
arr_data2[0, 2:5]      # 0번 행의 2~4번 값
arr_data2[0:2, 0:3]    # 0~1번 행 x 0~2번 열
```

> ⚠️ **콤마(`,`)가 행과 열을 나누는 기호**다.
> `arr_data2[:4:9]` 처럼 콜론을 두 번 쓰면 `[start:stop:step]` 으로 읽혀 **행만** 잘린다.

---

## 2. Pandas — 표 계산용

**행(Row)과 열(Column)로 된 표 형식 데이터** 를 다루는 라이브러리. CSV · Excel · DB 테이블을 쉽게 불러오고 정제할 수 있다.

| 자료형 | 구성 |
|--------|------|
| **Series** | 행 + **1개의 열** → 1차원 |
| **DataFrame** | 행 + 열, 각 열이 Series → 2차원 (가장 많이 쓴다) |
| **Index** | 행이나 열을 식별하는 정수 또는 문자열 |

> MySQL 의 Table 과 달리 DataFrame 의 행 인덱스는 **0번부터** 시작한다.

```python
import pandas as pd

df = pd.read_csv("./ad_performance.csv")
df.shape        # (5000, 9)
```

### 실습 데이터

가상의 이커머스 회사가 **2025년 1월 1일 ~ 6월 30일** 집행한 디지털 광고의 일별 성과다.

| 컬럼 | 뜻 |
|------|-----|
| `Date` | 광고 성과가 기록된 날짜 |
| `Channel` | 광고가 집행된 마케팅 채널 또는 유입 경로 |
| `Age_Group` | 타겟 고객의 연령대 그룹 |
| `Gender` | 타겟 고객의 성별 |
| `Impressions` | 광고가 잠재 고객에게 노출된 총 횟수 |
| `Clicks` | 노출된 광고를 클릭한 총 횟수 |
| `Cost` | 광고 집행에 지출된 총 비용(원) |
| `Conversions` | 광고를 통해 발생한 실제 목표 달성 횟수 (구매·가입·설치 등) |
| `Revenue` | 전환으로부터 얻은 총 매출액(원) |

### DataFrame 분해

**DataFrame = 행 인덱스 + 컬럼 인덱스 + 값**

| 속성 | 돌려주는 것 |
|------|------------|
| `df.index` | 행 인덱스 |
| `df.columns` | 컬럼 인덱스 |
| `df.values` | 값 → **넘파이 2차원 배열** |

### 인덱싱

| 하고 싶은 것 | 쓰는 법 | 결과 |
|--------------|---------|------|
| 컬럼 1개 | `df['컬럼명']` | **Series** |
| 컬럼 여러 개 (fancy 인덱싱) | `df[['컬럼1', '컬럼2']]` | **DataFrame** |
| 특정 행 + 컬럼 | `df.loc[행 인덱스, '컬럼명']` | 값 하나 |
| 여러 행 + 여러 컬럼 | `df.loc[[행1, 행2], ['컬럼1', '컬럼2']]` | DataFrame |

> 대괄호가 **한 겹이면 Series, 두 겹이면 DataFrame** 이다.

### 파생 변수 만들기

없던 컬럼에 값을 대입하면 **새 컬럼이 생긴다.**

| 지표 | 뜻 | 계산식 |
|------|-----|--------|
| **CTR** (Click-Through Rate) | 클릭률 — 노출 대비 얼마나 눌렸나 | `Clicks / Impressions * 100` |
| **ROAS** (Return On Ad Spend) | 광고 수익률 — 쓴 돈 대비 얼마나 벌었나 | `Revenue / Cost * 100` |

```python
df['CTR'] = df['Clicks'] / df['Impressions'] * 100
df['ROAS'] = df['Revenue'] / df['Cost'] * 100

df = df.drop('ROAS', axis=1)    # axis=1 이 열, axis=0 이 행
```

실제로 계산해 보니 평균 CTR 은 **4.77%**, 평균 ROAS 는 **766.43%** 였다.

### `value_counts()`

컬럼이 **범주형 데이터**일 때 **항목별 개수(빈도수)** 를 세어 준다.

```python
df['Channel'].value_counts()
# Google 1506 · Facebook 1479 · Naver 1023 · Instagram 537 · Organic 455
```

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `3차열` → **3차원**, `ouput1` `ouput3` → **`output1`** `output3` (오타)
- [x] `np.array(list(lis))` → `np.array(lis)` — `lis` 는 이미 리스트라 `list()` 로 다시 감쌀 필요가 없다
- [x] 주석으로 막아 둔 반복문이 `num2` 를 만들기 전에 써서 **NameError** 가 나던 것 → 인덱싱 예제로 다시 정리
- [x] `arr_data2[:4:9]` 는 `[start:stop:step]` 으로 읽혀 **0번 행 하나만** 나온다 → 교재 p.12 의 `arr_data2[0:4, 0:9]` (콤마) 형태와 나란히 비교
- [x] `df['New_Data'] = 0 #df['Clicks'] / df['Impressions']*10` — 계산식이 주석으로 막혀 0만 들어가 있었고, CTR 은 `* 100` (원본은 `* 10`)
- [x] 주석 `# 루아스 계산식` 이 **CTR 식 옆에** 붙어 있던 것 — ROAS 는 `Revenue / Cost`, CTR 은 `Clicks / Impressions` 로 서로 다른 지표
- [x] 컬럼명 `Ross` → **`ROAS`**
- [x] `pd.DataFrame` 만 적은 줄은 클래스를 가리키기만 할 뿐 아무 일도 하지 않아 제거
- [x] `display(df)` 는 주피터 전용이고 5,000행을 다 찍는다 → `df.head()`
- [x] `df['Date'].value_counts()` 는 날짜가 180일이라 결과가 길기만 하다 → 범주형(`Channel`·`Age_Group`·`Gender`)으로 교체

**직접 해본 것**
- 같은 데이터를 리스트와 배열로 각각 만들어 `+` `*` 결과 비교 (이어 붙이기 vs 요소별 연산)
- `ndim` · `shape` · `dtype` 으로 차원과 모양 확인
- `sum()/len()` 평균과 `np.mean()` 평균의 **자료형 차이** 확인
- `arr[행][열]` 과 `arr[행, 열]` 두 방식으로 같은 값 꺼내기
- 콜론 두 번(`[:4:9]`)과 콤마(`[0:4, 0:9]`)의 결과를 나란히 출력해 차이 확인
- 광고 데이터 5,000건에서 `df.loc` 로 행·열 골라내기, CTR·ROAS 파생 변수 만들고 지우기
- `Channel` · `Age_Group` · `Gender` 빈도수 세기

**막혔던 부분 / 질문**
- [ ] `arr[0][0]` 과 `arr[0, 0]` 은 결과가 같은데 왜 넘파이는 콤마 방식을 권할까 (성능 차이가 있는지)
- [ ] `df.values` 가 넘파이 배열이면, 문자열 컬럼과 숫자 컬럼이 섞이면 자료형이 어떻게 되는지
- [ ] `df['컬럼']` 과 `df.loc[:, '컬럼']` 의 차이
- [ ] 파생 변수를 만들 때 0으로 나누는 행(`Impressions`가 0)이 있으면 어떻게 처리해야 하는지
- [ ] `drop()` 이 새 DataFrame 을 돌려주는데 `inplace=True` 는 언제 쓰는지
- [ ] 평균 ROAS 766% 는 너무 높아 보이는데, 이상치를 빼고 봐야 하는 건 아닌지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [NumPy 공식 문서 — 배열 기초](https://numpy.org/doc/stable/user/basics.creation.html)
- [NumPy 공식 문서 — 인덱싱과 슬라이싱](https://numpy.org/doc/stable/user/basics.indexing.html)
- [pandas 공식 문서 — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas 공식 문서 — 인덱싱과 선택 (`loc`)](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [`value_counts()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
