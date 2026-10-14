---
day: 025
date: 2026-10-14
weekday: 수
week: 7
phase: 데이터 분석과 머신러닝/딥러닝
title: 앙상블(2) — 부스팅(XGBoost) · 스태킹 + 선형 회귀 · concat 다시 보기
tags: python, pandas, scikit-learn, xgboost, 머신러닝, 지도학습, 회귀, 분류, concat, 선형회귀, LinearRegression, MAE, MSE, RMSE, 표준화, StandardScaler, Lasso, 규제, 앙상블, 배깅, 부스팅, 스태킹, 하드보팅, 소프트보팅, RandomForestClassifier, RandomForestRegressor, XGBClassifier, XGBRegressor, StackingClassifier, StackingRegressor, 메타모델, 보스턴주택가격, 당뇨병
---

# Day 025 · 2026-10-14 (수)

`데이터 분석과 머신러닝/딥러닝` · 7주차

> **한 줄 요약** — 어제의 배깅(랜덤 포레스트)에 이어, **이전 트리의 오차(잔차)를 다음 트리가 깎아 나가는 부스팅(XGBoost)** 과 **여러 모델의 예측값을 메타 모델이 한 번 더 학습하는 스태킹** 을 배웠다. 당뇨병 정확도는 RF **74.0%** → XGBoost **75.0%** · 스태킹 74.8%, 보스턴 RMSE 는 선형 회귀 5.46 → RF **4.07** · 스태킹 4.20 · XGBoost 4.23 — **스태킹이 항상 1등은 아니었다.**

📂 실습 노트북
- [`lecture/01_pd_concat_실습.ipynb`](./lecture/01_pd_concat_실습.ipynb) — `pd.concat()` axis=0 / 1 · `ignore_index` · `join`
- [`lecture/02_선형회귀_LinearRegression_실습.ipynb`](./lecture/02_선형회귀_LinearRegression_실습.ipynb) — 회귀 개념 · MAE / MSE / RMSE · 표준화 · LinearRegression · Lasso (필기 `선형회귀실습` 2개 통합)
- [`lecture/03_앙상블_분류_RF_XGB_Stacking_실습.ipynb`](./lecture/03_앙상블_분류_RF_XGB_Stacking_실습.ipynb) — 당뇨병 RF · XGBoost · 스태킹 분류 (필기 `앙상블분류실습`)
- [`lecture/04_앙상블_회귀_RF_XGB_Stacking_실습.ipynb`](./lecture/04_앙상블_회귀_RF_XGB_Stacking_실습.ipynb) — 보스턴 RF · XGBoost · 스태킹 회귀 (필기 `앙상불회귀실습01`)

📊 실습 데이터 → [Day 024 `lecture/`](../2026-10-13/lecture/) 의 `house_price.csv` (506행) · `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` (70,692행) — 노트북과 같은 폴더에 두고 실행
📖 교재 `머신러닝` p.26~41 (concat · 선형 회귀 다시 보기) · p.92~113 (앙상블 · 부스팅 · 스태킹)

---

## 1. 다시 보기 — `pd.concat()` (p.26~28)

여러 DataFrame 을 **한 개로 병합**한다.

| 옵션 | 동작 |
|---|---|
| `axis=0` (기본값) | **공통 컬럼** 기준으로 **아래로** 이어 붙임 |
| `axis=1` | **공통 행 인덱스** 기준으로 **옆으로** 이어 붙임 (인덱스 다르면 `NaN`) |
| `ignore_index=True` | 인덱스를 버리고 0 부터 새로 매김 |
| `join='inner'` | 컬럼이 다를 때 **공통 컬럼만** 남김 (기본 `outer` 는 합집합) |

```python
df_concat = pd.concat([df1, df2, df3], ignore_index=True) # (12, 4)
```

---

## 2. 다시 보기 — 선형 회귀 (p.29~41)

**회귀** = 처음 보는 데이터의 값을 **연속적인 숫자**로 예측. **선형 회귀** = 데이터 분포를 가장 잘 표현하는 직선 `y = Wx + b` 를 찾는 것.

공부 시간 `[9, 8, 4, 2]` → 성적 `[90, 80, 40, 20]` 으로 학습하면 `W = 10`, `b = 0`, **7시간 → 70점**.

| 지표 | 수식 | 특징 |
|---|---|---|
| **MAE** | $\frac{\sum\|y-\hat{y}\|}{n}$ | 절대값 평균, 이상치에 덜 민감 |
| **MSE** | $\frac{\sum(y-\hat{y})^2}{n}$ | 큰 오차에 큰 벌점, 단위가 제곱 |
| **RMSE** | $\sqrt{MSE}$ | **정답과 같은 단위**로 해석 |

### 보스턴 집값 — LinearRegression vs Lasso

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # 학습용: 평균 · 표준편차 계산 + 적용
X_test_scaled = scaler.transform(X_test) # 평가용: 학습용 값 그대로 적용 (데이터 누수 방지)
```

| 모델 | MAE | RMSE |
|---|---|---|
| **LinearRegression** | 3.67 | **5.46** |
| Lasso (`alpha=1.0`) | 3.93 | 5.96 |

Lasso 는 13개 중 **8개 특성**(crim · zn · indus · chas · nox · age · dis · rad)의 기울기를 **0** 으로 만들고 `rm` · `lstat` · `ptratio` · `tax` · `b` 만 남겼다. 모델은 단순해졌지만 이 데이터에선 오차가 오히려 늘었다 → `alpha` 가 너무 컸다.

---

## 3. 앙상블 정리 — 투표 · 평균 (p.92~96)

| 방식 | 학습 | 대표 모델 |
|---|---|---|
| **배깅** | 복원 추출한 서브 데이터로 **병렬** 학습 → 투표 / 평균 | RandomForest |
| **부스팅** | 이전 모델의 오류를 다음 모델이 보완하는 **순차** 학습 | XGBoost |
| **스태킹** | 개별 모델의 예측값을 새 특성으로 → **메타 모델**이 최종 예측 | Stacking |

| 문제 | 모으는 방법 |
|---|---|
| 분류 | **하드 보팅**(레이블 다수결) / **소프트 보팅**(확률 평균, 확신도 반영 → 보통 더 좋음) |
| 회귀 | 연속값이라 투표 불가 → 예측값의 **평균** |

랜덤 포레스트는 [Day 024](../2026-10-13/) 에서 자세히 정리 — 오늘은 같은 분할로 **비교 기준**으로만 썼다.

---

## 4. 부스팅 — XGBoost (p.102~109)

**'조각상 다듬기'**

| 단계 | 하는 일 |
|---|---|
| 초기값 | 큰 덩어리 잡기 — **평균값**으로 예측하고 오차(잔차) 계산 |
| 1단계 | 튀어나온 큰 오차를 깎는다 — 2번째 트리가 **잔차**를 예측 × 학습률 |
| 2단계 | 덜 깎이거나 잘못 깎인 미세한 오차를 또 깎는다 — 3번째 트리 × 학습률 |
| 반복 | 수백 번 반복해 점점 정밀한 모델 |

교재 예시: 몸무게 평균 **64.2** → 1차 잔차 `88 − 64.2 = 23.8` → 다음 트리가 잔차를 예측해 × 학습률 0.1 만큼만 반영 → 2차 잔차 `88 − (64.2 + 0.1 × 23.8) = 21.42`. 잔차가 조금씩 0 으로 다가간다.

```python
# pip install xgboost
from xgboost import XGBClassifier, XGBRegressor # 교재의 XGBClassifer 는 오타

xgb = XGBClassifier(random_state=0)
xgb.fit(X_train, y_train)
accuracy_score(y_test, xgb.predict(X_test)) # 0.7498
```

---

## 5. 스태킹 (p.110~113)

| | 1단계 (Base Models) | 2단계 (Meta Model) |
|---|---|---|
| **학습** | 서로 다른 알고리즘으로 각각 train | 1단계 **예측값 + 정답**으로 메타 모델 train |
| **예측** | 평가용 데이터를 각각 predict | 1단계 **예측값을 입력(X)** 으로 최종 predict |

```python
base_estimators = [
    ('rf', RandomForestClassifier(random_state=0)),
    ('xgb', XGBClassifier(random_state=0)),
    ('dt', DecisionTreeClassifier(random_state=0)),
]
final_meta_learner = LogisticRegression(max_iter=1000, random_state=0) # 회귀는 LinearRegression

stack = StackingClassifier(estimators=base_estimators, final_estimator=final_meta_learner)
stack.fit(X_train, y_train)
```

`StackingClassifier` 는 내부에서 **교차 검증(cv=5)** 으로 1단계 예측값을 만든다 — 학습에 쓴 데이터를 그대로 예측하면 메타 모델이 '이미 외운 답'을 보고 배우기 때문.

---

## 6. 결과 비교 (모두 `random_state=0`, 같은 분할)

### 분류 — 당뇨병 여부 (정확도 ↑)

| 모델 | 평가용 정확도 |
|---|---|
| **XGBoost** | **75.0%** |
| Stacking (RF + XGB + DT → LogisticRegression) | 74.8% |
| RandomForest | 74.0% |

### 회귀 — 보스턴 집값 (RMSE ↓)

| 모델 | 평가용 RMSE |
|---|---|
| **RandomForestRegressor** | **4.07** |
| Stacking (DT + RF + XGB → LinearRegression) | 4.20 |
| XGBRegressor | 4.23 |
| LinearRegression | 5.46 |
| Lasso (`alpha=1.0`) | 5.96 |

회귀 스태킹의 메타 모델 가중치는 **xgb 0.854** · rf 0.098 · dt 0.079 — XGBoost 예측을 가장 믿었지만, 최종 성능은 단일 랜덤 포레스트가 가장 좋았다. 스태킹은 **기본 모델들이 서로 다른 실수**를 할 때 효과가 크다.

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `앙상불회귀실습01` 의 부스팅 모델이 `XGBRFRegressor` → 이건 XGBoost 로 만든 **랜덤 포레스트**(배깅)라 부스팅 실습이 아니다. 교재대로 **`XGBRegressor`** 로 교체
- [x] 같은 노트북 `train_test_split` 에 `random_state` 가 없어 필기의 RMSE 2.68 · 2.72 는 다시 만들 수 없는 값 → `random_state=0` 으로 고정
- [x] 회귀 문제에 `accuracy_score` 임포트, `"예상 값:"` · `"예측 값:"` 으로 RMSE · 정확도 출력 → 회귀는 RMSE, 문구는 무엇을 출력하는지 맞게
- [x] `final_mate_learmer` 오타 → `final_meta_learner`
- [x] `print("평가용 데이터:", y_train.index)` → `y_train` 은 **학습용** 정답
- [x] 결과를 `print(acc_rf)` `print(acc_xgb)` … 숫자만 나열 → 모델별 비교표로
- [x] `선형회귀실습` 노트북 2개(경로만 다름) + Lasso 버전을 하나로 합치고, LinearRegression vs Lasso 기울기 비교 추가
- [x] 경로 `C:\Users\…` → `./`

**직접 해본 것**
- 공부 시간 4개 데이터로 `W = 10`, `b = 0`, 7시간 → 70점이 나오는지 확인
- MAE · MSE · RMSE 를 numpy 로 직접 계산해 sklearn 함수와 같은 값인지 비교
- Lasso 가 0 으로 만든 특성 목록 뽑기
- stratify 로 원본 / 학습용 / 평가용의 정답 비율이 같은지 확인
- 스태킹 메타 모델의 `coef_` 로 기본 모델별 가중치 확인
- 참고로 같은 분할에서 `XGBRFRegressor(random_state=0)` 은 RMSE **3.98** — 이 데이터에선 배깅 계열이 부스팅 기본값보다 나았다 (단, 최신 xgboost 에서 `XGBRFRegressor` 는 deprecated 경고가 뜬다)

**막혔던 부분 / 질문**
- [ ] XGBoost 기본값(`n_estimators=100`, `learning_rate=0.3`, `max_depth=6`)이 보스턴처럼 작은 데이터에서 과대적합인지 — 학습률 · 깊이를 낮춰 비교해 보기
- [ ] Lasso `alpha` 를 0.1 · 0.01 로 줄이면 LinearRegression 보다 나아지는지, Ridge 와 비교
- [ ] 스태킹에서 `passthrough=True`(원본 특성도 메타 모델에 같이 넣기)를 쓰면 좋아지는지
- [ ] LightGBM · CatBoost 는 XGBoost 와 무엇이 다른지
- [ ] 하이퍼파라미터를 평가용이 아니라 교차 검증(`GridSearchCV`)으로 고르는 방법

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [pandas — `concat` 문서](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
- [scikit-learn — Linear Models: Ordinary Least Squares · Lasso](https://scikit-learn.org/stable/modules/linear_model.html)
- [scikit-learn — Regression metrics (MAE · MSE · RMSE)](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)
- [scikit-learn — Ensembles: Stacked generalization](https://scikit-learn.org/stable/modules/ensemble.html#stacked-generalization)
- [`StackingClassifier` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html) · [`StackingRegressor` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingRegressor.html)
- [XGBoost — Python API (`XGBClassifier` · `XGBRegressor`)](https://xgboost.readthedocs.io/en/stable/python/python_api.html)
- [XGBoost — Introduction to Boosted Trees](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)
