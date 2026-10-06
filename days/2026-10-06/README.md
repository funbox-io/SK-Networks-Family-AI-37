---
day: 020
date: 2026-10-06
weekday: 화
week: 6
phase: 데이터 분석과 머신러닝/딥러닝
title: 머신러닝 기본 개념 + 데이터 전처리(특성 공학) — 인코딩 · 스케일링 · 구간화 · query · concat
tags: python, pandas, scikit-learn, 머신러닝, 지도학습, 비지도학습, 분류, 회귀, train_test_split, 특성공학, 파생변수, 원핫인코딩, get_dummies, 레이블인코딩, replace, map, 스케일링, MinMaxScaler, StandardScaler, 정규화, 표준화, 구간화, pd.cut, query, concat
---

# Day 020 · 2026-10-06 (화)

`데이터 분석과 머신러닝/딥러닝` · 6주차

> **한 줄 요약** — 머신러닝이 무엇이고(지도/비지도, 분류/회귀, 학습/평가 데이터 분할) 모델이 숫자만 이해하기 때문에 필요한 **특성 공학** — 글자는 **인코딩**, 범위가 다른 숫자는 **스케일링**, 숫자를 범주로는 **구간화** — 을 익혔다.

📂 실습 노트북 → [`lecture/ml_preprocessing.ipynb`](./lecture/ml_preprocessing.ipynb) (필기 `Data_Preprocessing01` + 개념 메모 `notbook.py` 를 하나로 정리)
📊 실습 데이터 → [`iris_dataset.csv`](./lecture/iris_dataset.csv) (150행) · [`ad_performance.csv`](./lecture/ad_performance.csv) (5,000행)
📖 새 교재 `머신러닝` p.1~28 (09. 머신 러닝 기본 개념 · 데이터 전처리)

---

## 0. 머신러닝 기본 개념

### 데이터 분석 및 모델링 과정

| 단계 | 하는 일 | 지금까지 |
|------|---------|---------|
| 1) 데이터 수집 | 분석에 필요한 데이터 확보 | |
| 2) 데이터 **전처리** | 분석에 적합한 형태로 만들어 신뢰도를 높이는 작업 | [Day 017](../2026-09-30/) 결측치 · 이상치 → **오늘 특성 공학** |
| 3) 데이터 **탐색** | 그래프 · 통계로 특징과 패턴 파악 | [Day 018](../2026-10-01/) · [Day 019](../2026-10-02/) |
| 4) **모델링** | 데이터 간의 관계를 파악해 **새 데이터의 결과를 예측**하는 규칙 만들기 | 다음 시간 |
| 5) 분석 모델 평가 | 모델이 얼마나 잘 맞히는지 측정 | |

### 인공지능 ⊃ 머신러닝 ⊃ 딥러닝

| 용어 | 뜻 | 예 |
|------|-----|-----|
| **인공지능** | 인간의 지적 능력을 컴퓨터로 구현하는 기술 | 전문가 시스템, 규칙 기반 시스템 |
| **머신러닝** | 컴퓨터가 **데이터를 통해 스스로 학습**해 예측·판단 | 결정 트리, 선형 회귀 |
| **딥러닝** | **깊은 인공신경망**을 쓰는 머신러닝 | CNN, RNN |

머신러닝은 표 형태의 **정형 데이터**, 딥러닝은 이미지·소리·글 같은 **비정형 데이터**에 강하다.

### 특성(X)과 레이블(y)

붓꽃(iris) 데이터에서 꽃받침·꽃잎의 길이와 너비 4개가 **특성(Feature, 독립변수)**, 품종(`setosa` · `versicolor` · `virginica`)이 맞혀야 할 정답 **레이블(Label, 종속변수)** 이다.

### 머신러닝 종류 — 학습 방식 기준

| 종류 | 정답 | 분야 | 예 |
|------|------|------|-----|
| **지도 학습** | **있다** | **분류** — 어떤 범주에 속할지 | 품종 분류, 종양 양성/악성 |
| | | **회귀** — 숫자 값 | 수량, 가격, 시험 점수 |
| **비지도 학습** | **없다** | **클러스터링** — 비슷한 것끼리 묶기 | 고객 군집 |

같은 "공부 시간" 데이터라도 정답이 **점수**면 회귀, **Pass/Fail** 이면 분류다.

### 데이터 분할과 평가

학습에 데이터를 **100% 다 쓰면 안 된다** — 이미 본 문제로 시험을 보면 점수가 부풀려진다.

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns='label')
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)    # 학습 120 / 평가 30
```

| 데이터 | 비율 | 평가 척도 |
|--------|------|----------|
| Train (학습용) | 60~80% | 분류 — accuracy · recall · precision · f1 score |
| Test (평가용) | 40~20% | 회귀 — MSE · RMSE |

---

## 1. 특성 공학(Feature Engineering)

**분석가의 지식을 데이터에 주입해 모델이 더 똑똑하게 예측하도록 만드는 과정.**

| 작업 | 대상 | 방법 |
|------|------|------|
| **파생 변수** 생성 | 기존 컬럼들 | 조합해 새 의미 만들기 |
| **범주형** 변환 (Encoding) | 성별 · 채널 같은 **글자** | 원-핫 · 레이블 인코딩 |
| **연속형** 변환 (Scaling) | 구매액 · 방문횟수 같은 **숫자** | 표준화 · 정규화 |
| **구간화** (Binning) | 숫자 → 범주 | `pd.cut()` |

**파생 변수 예 — ROAS(광고비 대비 수익률)**

```python
df_ad['ROAS'] = df_ad['Revenue'] / df_ad['Cost']    # 광고비 1원으로 얼마를 벌었나
```

채널별 평균 ROAS 는 Organic 8.06 · Naver 7.91 · Google 7.61 · Facebook 7.50 · Instagram 7.46.

---

## 2. 원-핫 인코딩 — `pd.get_dummies()`

범주의 고유한 값 **n개 → 새 컬럼 n개**, 해당 컬럼에만 1, 나머지는 0.

| id | day | → | day_월 | day_화 | day_수 |
|----|-----|---|--------|--------|--------|
| 0 | 월 | | 1 | 0 | 0 |
| 2 | 화 | | 0 | 1 | 0 |
| 3 | 수 | | 0 | 0 | 1 |

```python
pd.get_dummies(df, dtype=int)                       # 문자열 컬럼 전부
pd.get_dummies(df, columns=['label'], dtype=int)    # 지정한 컬럼만 → iris 5열 → 7열
```

`dtype=int` 를 안 주면 1/0 대신 `True/False` 가 나온다. 결측치(NaN) 행은 모든 컬럼이 0 이 된다.

---

## 3. 레이블 인코딩 — `replace()` / `map()`

범주를 **0 ~ n-1** 숫자로. 컬럼 수는 그대로다.

```python
df_bank[['default', 'housing', 'loan']].replace({'no': 0, 'yes': 1})

df['label'].map({'setosa': 0, 'versicolor': 1, 'virginica': 2})   # 컬럼 하나면 map 이 깔끔
```

| | 원-핫 인코딩 | 레이블 인코딩 |
|---|---|---|
| 장점 | 범주 사이에 **순서가 안 생긴다** | **간결** — 컬럼이 안 늘어난다 |
| 단점 | 범주 수만큼 **컬럼이 늘어난다** | 값을 **직접** 적어야 하고, 0 < 1 < 2 **크기 순서**가 생긴다 |

> ⚠️ `replace()` 로 바꾼 컬럼은 숫자처럼 보여도 자료형이 **`object`** 로 남을 수 있다. `map()` 을 쓰거나 `.astype(int)` 로 바꾼다.

---

## 4. 스케일링 — `MinMaxScaler` · `StandardScaler`

나이(22~45)와 연봉(1,000~6,000)처럼 범위가 다르면 모델은 **숫자가 큰 특성**을 더 중요하게 여길 수 있다. 그래서 범위를 맞춘다.

| 종류 | 결과 | 공식 | 도구 |
|------|------|------|------|
| **정규화** | 범위 0 ~ 1 | (x − min) / (max − min) | `MinMaxScaler` |
| **표준화** | 평균 0, 표준편차 1 | (x − 평균) / 표준편차 | `StandardScaler` |

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

data_minmax = MinMaxScaler().fit_transform(df_dic)       # 결과는 numpy 배열
df_minmax = pd.DataFrame(data_minmax, index=df_dic.index, columns=['나이_정규화', '연봉_정규화'])
```

| 나이 | 연봉 | 나이_정규화 | 연봉_정규화 | 나이_표준화 | 연봉_표준화 |
|------|------|------------|------------|------------|------------|
| 22 | 1000 | 0.00 | 0.00 | -1.11 | -1.74 |
| 24 | 3500 | 0.09 | 0.50 | -0.88 | -0.29 |
| 45 | 6000 | 1.00 | 1.00 | 1.54 | 1.16 |
| 38 | 4300 | 0.70 | 0.66 | 0.74 | 0.17 |
| 29 | 5200 | 0.30 | 0.84 | -0.30 | 0.70 |

공식으로 직접 계산해 scikit-learn 결과와 **같은지 확인**했다. `StandardScaler` 는 표준편차를 **ddof=0**(모집단)으로 계산한다 — pandas `std()` 기본값(ddof=1)과 다르다.

**알고리즘별 가이드** — 선형·로지스틱 회귀, SVM, PCA 는 `StandardScaler`, K-Means 는 이상치를 자른 뒤 `StandardScaler`/`RobustScaler`, **트리 기반 모델(결정 트리, 랜덤 포레스트, XGBoost)은 스케일링이 필요 없다.**

---

## 5. 구간화 — `pd.cut(x, bins, labels)`

```python
age_bins  = [0, 12, 19, 49, 70, 100]                   # 경계값 6개 → 구간 5개
age_label = ['어린이', '청소년', '청년', '중년', '노년']
df_age['age_step'] = pd.cut(x=df_age['age'], bins=age_bins, labels=age_label)
```

구간은 `(0, 12]` 처럼 **왼쪽 열림, 오른쪽 닫힘**이다. 그래서 나이 **0** 은 어느 구간에도 들지 않아 NaN — 포함하려면 `include_lowest=True`. 15명 중 청년이 8명으로 가장 많다.

---

## 6. `df.query()` — 조건으로 행 추출

조건을 **문자열**로 써서 SQL 의 `WHERE` 처럼 읽힌다.

```python
df_emp.query("Age >= 28")
df_emp.query("Dept == 'IT'")                        # 문자열 값은 안쪽 따옴표
df_emp.query("Age >= 25 & Salary >= 6000")          # and 로 써도 된다
df_emp.query("Dept == 'HR' | Salary >= 7000")       # or
df_emp.query("not Dept == 'IT'")                    # not / ~
df_emp.query("Salary >= @min_salary")               # 파이썬 변수는 @
```

**컬럼 이름은 대소문자를 구분**한다 — `age` 로 쓰면 `Age` 를 못 찾는다.

---

## 7. `pd.concat()` — 데이터프레임 병합

```python
pd.concat([df1, df2, df3], ignore_index=True)    # axis=0 : 공통 컬럼 기준으로 아래로
```

`ignore_index=True` 는 인덱스를 0 부터 새로 매긴다. 광고 데이터에서 조건 결과 3개(Facebook · 매출 150만 초과 · Google & 매출 150만 초과)를 합쳤더니 3,213행 중 **789행이 중복**이었다 — 두 조건에 동시에 걸린 행이 두 번 들어간 것. `drop_duplicates()` 로 제거하면 2,424행.

---

## 🔁 복습

**필기에서 고친 부분**
- [x] 절대 경로 `C:\Users\Jinho\work\...` → 상대 경로 `./`, `display(...)` → `head()` / `print()`
- [x] 메모 "지도 학습(**딥러닝**)" → 지도 학습은 **정답이 있는 학습 방식**이지 딥러닝이 아니다
- [x] 메모 "분류(**문자열**) / 회귀(**정수**)" → 분류는 **범주**, 회귀는 **연속적인 숫자**(소수 포함)
- [x] 원-핫 결과를 `#display(df_onhot)` 로 막아 둔 것 → 결과 출력, 오타 `df_onhot` → `df_onehot`
- [x] `df.replace(...)` 결과 `label` 이 **object 자료형**으로 남는 문제 → `map()` 추가
- [x] 길이가 안 맞는 딕셔너리(5개 / 4개)를 만들었다 덮어쓰던 코드 제거 — 그대로 쓰면 `ValueError`
- [x] 컬럼 이름 `연령(인원)` ↔ 결과 `연봉_정규화` 불일치 → `연봉` 으로 통일, 표준화 결과 `나이_정규화` → `나이_표준화`
- [x] 메모 "bins(구간 **크기**) … **균등하게**" → `bins` 는 구간의 **경계값**, 리스트로 주면 균등하지 않아도 된다
- [x] query 예제에서 원본 변수를 결과로 덮어쓰고 매번 DataFrame 을 다시 만들던 것 → 원본 하나 + 결과만 출력
- [x] 광고 데이터 `Revenue > 150000` → 매출 최솟값이 약 10만 원이라 거의 모든 행이 걸려 조건이 의미가 없어, 바로 위 조건과 같은 `1500000` 으로 맞춤
- [x] `pd.concat()` 결과의 **중복 행** 확인 · 제거 추가
- [x] 오타 — `Scling`, `매걔변수`, `매깨변수`, `df_cunt`
- [x] 교재 예제 추가 — 데이터 분할(p.10), ROAS 파생 변수(p.12), 요일·과일 원-핫(p.13~14), 은행 yes/no(p.16), A0~D11 concat(p.26~27), `and`/`or`/`not`(p.24)

**직접 해본 것**
- `train_test_split(stratify=y)` 로 나눈 평가용 데이터에 세 품종이 10개씩 똑같이 들어가는지 확인
- 정규화 · 표준화를 **공식으로 직접 계산**해 scikit-learn 결과와 비교 (`np.allclose` → True)
- `replace()` 와 `map()` 으로 각각 인코딩한 뒤 자료형(`object` vs `int64`) 비교
- 결측치가 있는 컬럼을 원-핫 인코딩하면 어떻게 되는지 (모두 0)
- `concat` 결과에서 `duplicated().sum()` 으로 중복 개수 세기

**막혔던 부분 / 질문**
- [ ] 스케일러를 **학습용 데이터로만 `fit`** 하고 평가용에는 `transform` 만 해야 한다는데, 전체로 `fit` 하면 무엇이 문제인지 (데이터 누수)
- [ ] 레이블 인코딩의 크기 순서 문제 — 그럼 레이블(정답) 컬럼은 레이블 인코딩, 특성 컬럼은 원-핫으로 나누면 되는지
- [ ] scikit-learn 의 `LabelEncoder` · `OneHotEncoder` 와 pandas `replace` · `get_dummies` 의 차이
- [ ] 범주가 수백 개인 컬럼(예: 우편번호)을 원-핫 인코딩하면 컬럼이 너무 많아지는데, 이럴 땐 어떻게 하는지
- [ ] `RobustScaler` 는 어떤 공식인지 (중앙값 · IQR 기준?)

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [scikit-learn — `train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
- [scikit-learn — Preprocessing data (스케일링 · 인코딩)](https://scikit-learn.org/stable/modules/preprocessing.html)
- [scikit-learn — `MinMaxScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) · [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
- [`pd.get_dummies()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html)
- [`Series.map()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html)
- [`pd.cut()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)
- [`DataFrame.query()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html)
- [`pd.concat()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
