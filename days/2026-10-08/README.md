---
day: 022
date: 2026-10-08
weekday: 목
week: 6
phase: 데이터 분석과 머신러닝/딥러닝
title: 지도 학습 — 분류 · 로지스틱 회귀로 타이타닉 생존 여부 예측
tags: python, pandas, scikit-learn, 머신러닝, 지도학습, 분류, 로지스틱회귀, LogisticRegression, 시그모이드, 결정경계, predict_proba, accuracy_score, 정확도, concat, 결측치, fillna, dropna, pd.cut, 이상치, IQR, clip, get_dummies, stratify, 타이타닉
---

# Day 022 · 2026-10-08 (목)

`데이터 분석과 머신러닝/딥러닝` · 6주차

> **한 줄 요약** — 선형 회귀 점수를 **시그모이드**로 0~1 확률로 바꿔 분류하는 **로지스틱 회귀**를 배우고, 타이타닉 1,309명 데이터를 병합 → 결측치 · 이상치 처리 → 원-핫 인코딩 → 분할 · 표준화까지 전처리해서 생존 여부를 **정확도 85.9%** 로 예측했다.

📂 실습 노트북 → [`lecture/logistic_regression.ipynb`](./lecture/logistic_regression.ipynb) (필기 `Data_Preprocessing03` · `로직스틱회귀실습` + 개념 메모 `notbook03.py` 정리)
📊 실습 데이터 → [`titanic_train.csv`](./lecture/titanic_train.csv) (891행) · [`titanic_test.csv`](./lecture/titanic_test.csv) (418행) · [`titanic_cleaned.csv`](./lecture/titanic_cleaned.csv) (전처리 결과, 1,308행)
📖 교재 `머신러닝` p.47~56 (11. 지도 학습을 이용한 분류)

---

## 1. 로지스틱 회귀 — "이름은 회귀, 목적은 분류"

선형 회귀처럼 직선 점수를 계산하지만, 그 값을 **확률로 바꿔서 분류**한다.

```
z = w1·x1 + w2·x2 + … + b     ← ① 선형 회귀 점수
P = σ(z) = 1 / (1 + e^-z)      ← ② 시그모이드 : 0 ~ 1 확률
P ≥ 0.5 → 1,  P < 0.5 → 0       ← ③ 분류
```

양수/음수만 보면 "A 클래스다" 밖에 모르지만, 확률로 바꾸면 "**A 클래스일 확률이 95%**" 까지 안다. 암 진단 51% 와 99% 는 같은 "양성"이라도 대응이 달라진다.

### 시그모이드 함수

| 입력 z | -∞ 쪽 | **0** | +∞ 쪽 |
|--------|-------|-------|-------|
| 확률 P | 0 에 가까움 | **0.5** | 1 에 가까움 |

- 시그모이드 값 = 1 일 확률 **P**, 0 일 확률은 **1 − P**
- 0 과 1 에 **가까워질 뿐** 정확히 0, 1 은 되지 않는다 (e ≈ 2.718, 자연 상수)

### 결정 경계 = 확률 0.5 = **z = 0**

학습 결과가 **z = −x + y − 1** 이면 결정 경계는 직선 **y = x + 1**. 직선 위쪽(z > 0)은 **Yes**, 아래쪽(z < 0)은 **No**.

### 학습 과정과 장단점

**정답이 1 이면 확률을 1 에, 0 이면 0 에 가깝게** 만드는 최적의 직선을 찾는다(손실 최소화).

| `max_iter` | `coef_` | 장점 | 단점 |
|------------|---------|------|------|
| 기울기 조정 **최대** 반복 횟수 (기본 100) | 최적 직선의 기울기 w1, w2, … | **매우 빠른** 학습 | 경계가 **직선**뿐 → 비선형 데이터에 한계 |

---

## 2. 타이타닉 데이터 전처리

**1,309명** = 학습용 891명 + 평가용 418명. 전처리를 한 번에 하려고 먼저 `concat` 으로 이어 붙였다.

> `concat` 은 같은 컬럼끼리 **위아래로 이어 붙이기**, SQL `JOIN` 같은 `merge` 는 공통 키로 **옆으로 짝 맞추기**다.

| 컬럼 | 누락 | 처리 |
|------|------|------|
| `Cabin` | 1,014 (77%) | **컬럼 삭제** — 대부분 비어 있다 |
| `Age` | 263 | **중앙값 28** 로 채움 → `pd.cut(bins=8)` 로 약 10살 단위 `Age_step` |
| `Embarked` | 2 | **최빈값 `S`** 로 채움 (`mode()[0]`) |
| `Fare` | 1 | **행 삭제** |

**이상치 — `Fare`**

```python
q1, q3 = df2['Fare'].quantile(0.25), df2['Fare'].quantile(0.75)
iqr = q3 - q1
df2['Fare'] = df2['Fare'].clip(lower=q1 - 1.5*iqr, upper=q3 + 1.5*iqr)   # -27.17 ~ 66.34
```

삭제하지 않고 **경계값으로 잘라 붙여서**(`clip`) 행은 살렸다. 66.34 를 넘던 **171명**의 요금이 66.34 로 바뀌었다.

**정리 · 인코딩 · 저장**

```python
df3 = df2.drop(columns=['PassengerId', 'Name', 'Age', 'Ticket'])           # 식별용 값 + Age(→Age_step)
df4 = pd.get_dummies(df3, columns=['Gender', 'Embarked'], dtype=int)       # 문자 → 0/1
df4.to_csv('./titanic_cleaned.csv', index=False)                           # 1,308행 × 11열
```

---

## 3. 학습 · 예측 · 평가

```python
X_train, X_test, y_train, y_test = train_test_split(
    X_data, y_data, test_size=0.2, random_state=0,
    stratify=y_data)                       # 사망 62% : 생존 38% 비율 유지

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

logistic = LogisticRegression()
logistic.fit(X_train_scaled, y_train)
pred_test  = logistic.predict(X_test_scaled)         # 0 / 1
proba_test = logistic.predict_proba(X_test_scaled)   # [사망 확률, 생존 확률]
accuracy_score(y_test, pred_test)                    # 0.8588
```

| 결과 | 값 |
|------|-----|
| 정확도 | **85.9%** (평가용 262명 중 **225명** 맞힘) |
| 기준선 — 전부 "사망" 으로 찍기 | 62.2% |
| 살았는데 사망으로 예측 / 사망했는데 생존으로 예측 | 21명 / 16명 |

`predict_proba()` 의 생존 확률이 `decision_function()` 으로 구한 z 를 **시그모이드에 직접 넣은 값과 똑같은 것**도 확인했다.

**가중치 읽기** — 양수면 생존 확률 ↑, 음수면 ↓

| 특성 | 가중치 | 해석 |
|------|-------|------|
| `Gender_female` / `Gender_male` | **+0.88** / **−0.88** | 여성 생존율 83%, 남성 13% |
| `Pclass` | −0.69 | 3등석일수록 생존 확률 낮음 |
| `Fare` | +0.26 | 요금이 높을수록 생존 확률 높음 |

`Gender_female` 과 `Gender_male` 은 부호만 반대인 **같은 정보**다. `get_dummies(..., drop_first=True)` 로 하나만 남길 수 있다.

---

## 🔁 복습

**메모(`notbook03.py`) · 필기에서 고친 부분**
- [x] 결정 경계 · 시그모이드 · e · "0 과 1 에 수렴" · "정답 1 → 확률 1, 정답 0 → 확률 0" → **맞는 내용**이라 그대로 정리
- [x] "Y = X + 1 이 결정 경계" → **z = −x + y − 1 일 때** 라는 조건 추가 (z = 0 인 곳이 경계)
- [x] "정확도를 1 에 가깝게 만드는 게 학습" → 학습이 줄이는 건 **손실(log loss)**, 정확도는 **평가 지표**
- [x] "**Max_irer**: 학습 횟수", "**선영** 회귀 직선" → `max_iter` 는 **최대** 반복 횟수 (이번엔 10번 만에 수렴), 선형
- [x] `df_del` 로 `Cabin` 을 지워 놓고 `df_tot` 에 계속 작업해서 **`Cabin` 이 끝까지 남던 것** → 한 줄기로 정리
- [x] `Fare02 = dropna(...)` 결과를 안 써서 **Fare 누락 1행이 남던 것** → 그대로면 모델 학습에서 NaN 에러
- [x] 변수 이름 `sum` → 파이썬 내장 함수를 덮어쓴다 → `num_nulls`
- [x] `get_dummies` 에 `dtype=int` 누락 (True/False 로 나옴)
- [x] 경로 `C:\Users\Jinho\…`, `'C:./titanic_train.csv'` → `./`, `warnings.filterwarnings('ignore')` 제거
- [x] 오타 — `marge`, `숭선`, `Embared`, `평간`, 주석 `#85.8%` → 실제 **85.9%**
- [x] 교재 p.49 확률 정보 → `predict_proba()` 와 시그모이드 직접 검증 코드 추가

**직접 해본 것**
- 시그모이드 함수를 numpy 로 만들어 z = −10 ~ 10 에서 확률 확인
- 메모의 결정 경계 예시(z = −x + y − 1)에 점 3개를 넣어 Yes/No 확인
- `pd.cut(bins=8)` 의 실제 구간 범위 출력 → 약 10살 단위
- `stratify` 로 학습용 · 평가용 정답 비율이 원본과 같은지 확인 (0.622 : 0.378)
- 정확도를 "전부 사망" 기준선(62.2%)과 비교, 틀린 유형 나눠 세기
- 노트북으로 다시 만든 `titanic_cleaned.csv` 가 수업 때 저장한 파일과 같은지 비교 → 같음

**막혔던 부분 / 질문**
- [ ] `Age` 중앙값 · `Fare` IQR 경계를 **학습용 · 평가용을 합친 전체**로 계산했는데, 평가용 정보가 섞이는 데이터 누수는 아닌지
- [ ] 원래 891 / 418 로 나뉜 데이터를 합쳤다가 80:20 으로 다시 나눈 이유
- [ ] 정확도 말고 생존자를 얼마나 놓쳤는지 보는 **재현율 · 정밀도 · 혼동 행렬**
- [ ] 분류 기준 0.5 를 0.3 이나 0.7 로 바꾸면 결과가 어떻게 달라지는지
- [ ] `Name` 의 호칭(Mr, Mrs, Miss, Master)으로 새 특성을 만들면 성능이 오르는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [`LogisticRegression` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [scikit-learn — Logistic regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [`accuracy_score` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
- [`Series.clip()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.Series.clip.html)
- [`DataFrame.dropna()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html)
- [`pd.get_dummies()` 문서 — `drop_first`](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html)
