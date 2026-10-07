---
day: 021
date: 2026-10-07
weekday: 수
week: 6
phase: 데이터 분석과 머신러닝/딥러닝
title: 지도 학습 — 회귀(1) · 선형 회귀 · MAE/MSE/RMSE · Lasso/Ridge 규제
tags: python, scikit-learn, 머신러닝, 지도학습, 회귀, 선형회귀, LinearRegression, 다중선형회귀, train_test_split, StandardScaler, MAE, MSE, RMSE, 과대적합, 규제, L1, L2, Lasso, Ridge, alpha, 보스턴주택가격
---

# Day 021 · 2026-10-07 (수)

`데이터 분석과 머신러닝/딥러닝` · 6주차

> **한 줄 요약** — 보스턴 주택 가격 데이터로 **선형 회귀** 모델을 처음 만들었다. 특성/정답 → 학습/평가로 나누고, 학습용 기준으로 표준화해서 학습하고 예측한 뒤 **RMSE 5.46** 으로 평가했다. 이어서 가중치를 줄여 과대적합을 막는 **Lasso(L1) · Ridge(L2) 규제**를 비교했다.

📂 실습 노트북 → [`lecture/linear_regression.ipynb`](./lecture/linear_regression.ipynb) (필기 `Data_Preprocessing02` + 개념 메모 `notbook02.py` 정리 · 메모의 틀린 부분 수정)
📊 실습 데이터 → [`house_price.csv`](./lecture/house_price.csv) (보스턴 주택 가격, 506행 × 14열)
📖 교재 `머신러닝` p.29~46 (10. 지도 학습을 이용한 회귀(1))

---

## 1. 회귀와 선형 회귀

**회귀** — 학습 데이터로 특성과 정답의 관계를 파악해, 처음 보는 데이터의 **연속적인 숫자 값**을 예측하는 것.

**선형 회귀** — 입력과 출력의 관계를 **직선** $y = Wx + b$ 로 나타내고 그 직선으로 예측한다. 할 일은 **"어떤 직선이 데이터를 가장 잘 표현하는가?"** 를 찾는 것이다.

| 공부 시간 x | 9 | 8 | 4 | 2 | **7** |
|---|---|---|---|---|---|
| 성적 y | 90 | 80 | 40 | 20 | **?** |

```python
model = LinearRegression().fit([[9], [8], [4], [2]], [90, 80, 40, 20])
model.coef_, model.intercept_      # W = 10, b = 0
model.predict([[7]])               # → 70점
```

특성이 여러 개면 특성마다 가중치가 붙는 **다중 선형 회귀** $y = w_1x_1 + w_2x_2 + \cdots + w_px_p + b$ 가 된다. 보스턴 데이터는 특성 13개 → 가중치 13개 + 절편 1개.

---

## 2. 평가 지표 — 오차를 하나의 숫자로

**오차 = 정답 − 예측** ($y - \hat{y}$). 작을수록 좋은 모델이다.

| 지표 | 공식 | 특징 |
|------|------|------|
| **MAE** 평균 절대값 오차 | $\sum \lvert y - \hat{y} \rvert / n$ | 오차의 절댓값 평균 |
| **MSE** 평균 제곱 오차 | $\sum (y - \hat{y})^2 / n$ | 큰 오차를 더 크게 벌함. 단위가 **제곱** |
| **RMSE** 평균 제곱근 오차 | $\sqrt{\text{MSE}}$ | 루트로 **정답과 같은 단위**로 되돌림 |

절댓값이나 제곱을 하는 이유는 +3 과 −3 을 그냥 더하면 0 이 되어 "오차가 없다"로 보이기 때문이다.

---

## 3. 보스턴 주택 가격 예측 — 전체 흐름

```python
# ① 열 나누기 : 특성 / 정답
X_data = df.drop(columns=['medv'])
y_data = df['medv']

# ② 행 나누기 : 학습용 75% / 평가용 25%
X_train, X_test, y_train, y_test = train_test_split(
    X_data, y_data, test_size=0.25, random_state=0)

# ③ 표준화 : 기준은 학습용에서만 계산, 평가용은 그 기준으로 변환만
scaler = StandardScaler()
X_train_scal = scaler.fit_transform(X_train)
X_test_scal  = scaler.transform(X_test)

# ④ 학습 → ⑤ 예측 → ⑥ 평가
lireg = LinearRegression()
lireg.fit(X_train_scal, y_train)
y_pred = lireg.predict(X_test_scal)
rmse(y_test, y_pred)                 # 5.46
```

| 지표 | 값 | 해석 |
|------|-----|------|
| MAE | 3.67 | |
| MSE | 29.78 | |
| **RMSE** | **5.46** | 평균 약 **5,460달러** 틀림 (집값 평균 약 22,500달러) |

**가중치 읽기** — 표준화한 데이터라 크기끼리 비교할 수 있다. `lstat`(저소득층 비율) **−3.59**, `dis`(고용 시설까지 거리) −3.00 이 집값을 가장 크게 낮추고, `rm`(방 개수) **+2.61** 이 가장 크게 올린다. 절편 22.61 은 학습용 집값의 평균이다.

> 기본 선형 회귀는 표준화를 해도 **예측이 똑같다** (표준화 안 해도 RMSE 5.46). 표준화의 이점은 가중치 크기를 비교할 수 있게 되는 것, 그리고 다음의 Lasso · Ridge 처럼 **가중치 크기에 벌점을 주는 모델**에서 결과가 달라진다는 것이다.

---

## 4. 모델 정규화(Regularization) = 규제

**과대적합**(학습 데이터에만 너무 맞춰져 새 데이터에 틀리는 것)을 막기 위해 **가중치 W 를 0 이나 0 에 가까운 작은 값으로** 줄여 모델을 단순하게 만든다.

> ⚠️ 규제의 **정규화(Regularization)** 는 [Day 020](../2026-10-06/) 스케일링의 **정규화(Normalization, MinMaxScaler)** 와 다른 개념이다.

| | **L1 규제 → `Lasso`** | **L2 규제 → `Ridge`** |
|---|---|---|
| 줄이는 방식 | 모든 W 를 **같은 크기**만큼 | 모든 W 를 **같은 비율**로 |
| 효과 | 작은 가중치가 **0** → 특성 **제거** | 전체가 0 에 **가까워짐** |
| 강도 | `alpha` (클수록 강함) | `alpha` |

```python
lasso = Lasso(alpha=1.0, random_state=0).fit(X_train_scal, y_train)
ridge = Ridge(alpha=1.0, random_state=0).fit(X_train_scal, y_train)
```

| 모델 (alpha=1) | 0 이 된 가중치 | 평가용 RMSE |
|------|---------------|------------|
| LinearRegression | 0 | 5.46 |
| Ridge (L2) | 0 | 5.46 |
| Lasso (L1) | **8** | 5.96 |

Lasso 는 13개 중 `rm` · `tax` · `ptratio` · `b` · `lstat` **5개만 남겼다.** `alpha=10` 이면 13개를 전부 0 으로 만들어 평균값만 예측하는 모델이 되고 RMSE 가 9.04 로 나빠진다 — 규제가 **너무 세면 과소적합**이다.

---

## 🔁 복습

**메모(`notbook02.py`) · 필기에서 고친 부분**
- [x] "**REMSE**", "평균제곱 오차 **MASS**" → **RMSE**, **MSE**
- [x] "정답 ± 평균 오차를 계산 후 (예측 데이터)" → 예측은 **학습한 직선** $Wx + b$ 로 하고, 평균 오차는 **평가 지표**다
- [x] "MSE 숫자가 너무 크기 때문에 RMSE" → 핵심은 제곱으로 바뀐 **단위를 원래대로** 되돌리는 것
- [x] "학습할 때**만** 표준화를 적용한다" → 기준 계산(`fit`)은 학습용에서만, 변환(`transform`)은 학습용 · 평가용 **둘 다**
- [x] `X_data` 에 "#학습용", `y_data` 에 "#평가용" → 이 단계는 **특성 / 정답** 나누기. 학습용/평가용은 `train_test_split` 에서
- [x] `random_state=0 # 0번째 값 출력` → 무작위로 섞는 방식(**시드**)을 고정하는 값
- [x] `print(y_train.index) # 평가용(정답)` → `y_train` 은 **학습용 정답**
- [x] "lireg 변수에 대입하지 않으면 에러" → `fit()` 은 모델 **자기 자신을** 학습시킨다. 대입 안 해도 된다
- [x] `coef_` = "학습용 최소 기울기", `intercept_` = "모델 절연" → 특성별 **가중치 W**, **절편 b**
- [x] "선이 하나면 Y = wx + b" → 특성 13개짜리 **다중 선형 회귀**
- [x] (보류) 로지스틱 회귀 메모 — "Y = X+1", "X^+2 (3^2=9)" 는 섞여 적힌 것이라 빼고, **시그모이드 · 자연 상수 e · 0.5 결정 경계**만 예고로 정리
- [x] 오타 — `X_trarin`, `prad`, `편균`, `절연`, `mean_mse29.78`(콜론 빠짐)
- [x] 절대 경로 → `./house_price.csv`, 앞 셀 출력이 잘못 붙어 있던 표준화 셀 출력 제거
- [x] 교재 예제 추가 — 공부 시간 회귀(p.30~31), MAE(p.35), Lasso · Ridge(p.42~46)

**직접 해본 것**
- 작은 예시로 MAE · MSE · RMSE 를 numpy 로 직접 계산해 공식 확인
- `X_train.index == y_train.index` 로 문제와 정답이 짝을 유지한 채 섞였는지 확인
- 표준화 후 평가용 평균이 정확히 0 이 아닌 것 확인 (기준이 학습용이라서)
- 표준화 안 한 선형 회귀와 RMSE 비교 → 같음
- 정답 · 예측 · 오차를 나란히 놓고 가장 크게 틀린 집 찾기 (정답 50.0 → 예측 23.6)
- `alpha` 0.01 ~ 10 에서 Lasso · Ridge 의 0 인 가중치 수와 RMSE 비교

**막혔던 부분 / 질문**
- [ ] 정답이 50.0 으로 딱 잘린 집들(상한값)이 크게 틀리는데, 이런 값은 빼고 학습해야 하는지
- [ ] 적당한 `alpha` 는 평가용 점수를 보고 고르면 안 된다는데 — 교차 검증(`LassoCV`, `RidgeCV`)
- [ ] L1 과 L2 를 섞은 `ElasticNet` 은 언제 쓰는지
- [ ] `model.score()` 가 돌려주는 **R²(결정계수)** 와 RMSE 의 차이
- [ ] 과대적합을 실제로 확인하려면 학습용 RMSE(4.43)와 평가용 RMSE(5.46)를 어떻게 비교해야 하는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [scikit-learn — Linear Models (OLS · Ridge · Lasso)](https://scikit-learn.org/stable/modules/linear_model.html)
- [`LinearRegression` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [`Lasso` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html) · [`Ridge` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html)
- [scikit-learn — Regression metrics (MAE · MSE · RMSE)](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)
- [`train_test_split` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
- [scikit-learn — Common pitfalls (데이터 누수)](https://scikit-learn.org/stable/common_pitfalls.html)
