---
day: 023
date: 2026-10-12
weekday: 월
week: 7
phase: 데이터 분석과 머신러닝/딥러닝
title: 주요 분류 모델 — SVM(SVC · SVR) · 단일 결정 트리(불순도 · CART · 과대적합)
tags: python, pandas, scikit-learn, 머신러닝, 지도학습, 분류, 회귀, SVM, SVC, SVR, 서포트벡터, 마진, 표준화, 결정트리, DecisionTreeClassifier, 불순도, 지니, 엔트로피, CART, plot_tree, predict_proba, max_depth, random_state, 과대적합, iris, 타이타닉, 보스턴주택가격, 당뇨병
---

# Day 023 · 2026-10-12 (월)

`데이터 분석과 머신러닝/딥러닝` · 7주차

> **한 줄 요약** — 클래스 사이의 **마진(안전거리)을 최대화**하는 **SVM** 으로 타이타닉 생존(SVC)과 보스턴 집값(SVR)을 예측하고, 특성의 **임계값으로 데이터를 반복해서 둘로 나누는** **결정 트리**로 붓꽃 품종 · 당뇨병 여부를 분류했다. 트리는 설명하기 쉽지만 끝까지 자라면 **과대적합**된다는 것도 확인했다.

📂 실습 노트북
- [`lecture/svm.ipynb`](./lecture/svm.ipynb) — SVM 개념 · SVC 타이타닉 · SVR 보스턴 · 표준화 비교 (필기 `SVM_분류실습`)
- [`lecture/decision_tree.ipynb`](./lecture/decision_tree.ipynb) — 불순도 · 트리 구조 · 붓꽃 EDA/분류 · 당뇨병 분류 (필기 `붓꽃데이터EDA` · `결정트리분류실습` · `결정트리분류실습02`)

📊 실습 데이터 → [`iris_dataset.csv`](./lecture/iris_dataset.csv) (150행) · [`titanic_cleaned.csv`](./lecture/titanic_cleaned.csv) (1,308행, Day 022 전처리 결과) · [`house_price.csv`](./lecture/house_price.csv) (506행) · [`diabetes_binary_5050split_health_indicators_BRFSS2015.csv`](./lecture/diabetes_binary_5050split_health_indicators_BRFSS2015.csv) (70,692행)
📖 교재 `머신러닝` p.57~81 · 개념 메모 `notbook04.py` 는 확인해서 맞는 내용만 반영

---

## 1. SVM — 마진을 최대화하는 결정 경계

**클래스 간의 안전한 거리(마진)를 최대화해서 성능을 높이는 분류 알고리즘.**

| 용어 | 뜻 |
|------|-----|
| **서포트 벡터** | 결정 경계와 **가장 가까운** 데이터 |
| **마진** | 결정 경계와 서포트 벡터 사이의 **거리** |

학습용 데이터만 보면 한쪽 클래스에 **바짝 붙은** 경계로도 나눌 수 있지만, 평가용 데이터는 위치가 조금씩 달라서 그런 경계는 쉽게 틀린다. 그래서 양쪽에서 **최대한 멀리 떨어진** 경계를 고른다.

| 장점 | 단점 |
|------|------|
| **소규모 데이터**(수십~수백 개)에 강함, 특성이 샘플보다 많아도 안정적 | 데이터가 커지면 학습이 **급격히 느려짐** |

| 용도 | 모델 | 실습 | 결과 |
|------|------|------|------|
| 분류 | `SVC` | 타이타닉 생존 | 정확도 **0.8588** (서포트 벡터 384개) |
| 회귀 | `SVR` | 보스턴 집값 | RMSE **6.34** → `C=100` 이면 **4.19** (선형 회귀 5.46) |

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)        # ← 평가용은 transform 만!

svc = SVC().fit(X_train_scaled, y_train)
accuracy_score(y_test, svc.predict(X_test_scaled))
```

**SVM 은 거리 기반이라 표준화가 필수다.**

| | 표준화 O | 표준화 X |
|---|---|---|
| SVC 정확도 | **85.9%** | 67.6% (기준선 62.2% 수준) |
| SVR RMSE | **6.34** | 8.65 |

> 필기에서는 평가용에 `fit_transform` 을 써서 정확도가 **0.8626** 으로 나왔다. 평가용이 자기 기준으로 다시 표준화된 **잘못된 방법**이라, 올바르게 고친 **0.8588** 이 실제 성능이다.

---

## 2. 단일 결정 트리 — IF-THEN 스무고개

**특성 하나의 임계값으로 데이터를 반복해서 둘로 나눠, 영역 안의 불순도를 최소화하는 비선형 알고리즘.**

```
꽃잎 너비 <= 0.8 ?
├─ 예  → setosa (불순도 0)
└─ 아니오 → 꽃잎 너비 <= 1.75 ? → …
```

"AI 가 setosa 라고 했어요" 가 아니라 "**꽃잎 너비가 0.8cm 이하라서** setosa 입니다" 라고 설명할 수 있다(**해석 가능성**). 한 특성 안에서 자르기만 하니 **표준화가 필요 없다.**

### 불순도 — 서로 다른 데이터가 섞인 정도

| 지표 | 공식 | 순수 | 2클래스 반반 | 3클래스 1:1:1 |
|------|------|------|------------|---------------|
| **지니** (기본값) | $1 - \sum p^2$ | 0 | **0.5** | 0.667 |
| **엔트로피** | $-\sum p \log_2 p$ | 0 | **1.0** | 1.585 |

### 트리 구성 · 클래스 확률 · CART

| 구성 | 뜻 |
|------|-----|
| 루트 노드 | 맨 위 첫 분할 |
| 리프 노드 | **자식이 없는** 맨 아래, 최종 예측 |
| 노드 정보 | 분할 조건(Threshold) · `gini` · `samples` · `value`(클래스별 수) |

- **클래스 확률** = 도착한 리프의 학습 데이터 클래스 비율 $N_{L,k} / N_L$ → `predict_proba`
- **CART** — scikit-learn 의 트리 알고리즘. **항상 둘로** 나누고, `max_depth` 에 닿거나 더 줄일 불순도가 없으면 멈춘다

---

## 3. 붓꽃 품종 분류

EDA 에서 **꽃잎(petal)** 크기가 품종별로 뚜렷이 나뉘는 걸 먼저 확인했다 (setosa 꽃잎 너비 0.1~0.6 vs 나머지 1.0 이상).

```python
dt = DecisionTreeClassifier(random_state=0)
dt.fit(X_train, y_train)
plot_tree(dt, feature_names=X_train.columns,
          class_names=['setosa', 'versicolor', 'virginica'], filled=True)
```

| 결과 | 값 |
|------|-----|
| 정확도 | **0.9667** (30개 중 29개) |
| 트리 | 깊이 4, 리프 8개 — 루트 `petal width <= 0.8` 로 setosa 40개를 한 번에 분리 |
| 특성 중요도 | 꽃잎 너비 **0.955** |
| `max_depth=2` 의 확률 | versicolor 리프 `[0, 39, 3]` → **[0, 0.929, 0.071]** |

**`random_state`** — 똑같이 좋은 분할이 여러 개면 그중 하나를 고르는 데 영향을 준다. `random_state=0` 은 루트가 `petal width <= 0.8`, `42` 는 `petal length <= 2.45` (교재 p.81 의 두 그림). 재현하려면 **고정**한다.

---

## 4. 당뇨병 여부 분류 — 과대적합 확인

CDC 건강 설문(BRFSS 2015) **70,692명**, 특성 21개, 정상 : 당뇨 = 50 : 50.

| `max_depth` | 리프 수 | 학습용 | 평가용 |
|-------------|--------|--------|--------|
| 3 | 8 | 71.0% | 71.3% |
| 7 | 127 | 74.8% | **74.1%** |
| 9 | 460 | 76.0% | **74.3%** |
| 12 | 1,995 | 79.4% | 72.8% |
| 제한 없음 | **16,192** | **99.5%** | **65.5%** |

끝까지 자란 트리는 학습용을 거의 다 외워서(99.5%) 처음 보는 데이터에는 오히려 약하다(65.5%) — **과대적합**. 깊이를 7~9 로 제한하면 학습용 · 평가용이 비슷해진다. 중요한 특성은 **고혈압(0.45)**, **전반적 건강 상태(0.28)**, BMI, 나이 순.

---

## 🔁 복습

**메모(`notbook04.py`) · 필기에서 고친 부분**
- [x] "평가용에서는 경계가 다르다 → 여유 있게 떨어질 필요(안전거리)" → **맞는 내용** (마진 최대화 이유)
- [x] "서포트 **팩터**" → 서포트 **벡터** = 경계와 가장 가까운 데이터. 안전거리 자체는 **마진**
- [x] "마진 : 결정 경계 **사이의** 거리" → 결정 경계와 **서포트 벡터 사이**
- [x] "SVM : 데이터가 **많을 때** 유리" → 반대. **적은 데이터에 강하고** 많으면 느리다
- [x] "분류 SVC, 회귀 **SVM**" → 회귀는 **SVR**
- [x] "**1/N 데이터 개수만큼 자른다**" → 특성 하나의 **임계값**으로 **항상 둘로** (CART)
- [x] "루트(**부모**) / 리프(**자식**)" → 부모 · 자식은 위아래 관계. 리프는 **자식이 없는** 노드
- [x] "1:1 보다 1:1:1 이 불순도 낮다" → 반대. 고르게 섞인 클래스가 많을수록 **높다** (0.5 → 0.667)
- [x] 끊겨 있던 "클래스 확률 추정 …" 문장 → 교재 공식으로 완성
- [x] `X_test_scaled = scaler.fit_transform(X_test)` → **`transform`** (데이터 누수 버그)
- [x] `train_test_split(` 빈 괄호로 `NameError` 난 셀, 불러오기만 하고 끝난 당뇨병 실습 → 완성
- [x] 주석 "X 학습용, y **평가용**", "**평가용** 데이터 개수 확인 `print(y_train.index)`" → 둘 다 **학습용**
- [x] 쓰지 않는 `LinearRegression` 임포트 · 주석 처리된 코드 제거, `DecisionTreeClassifier()` 중복 생성 정리
- [x] 붓꽃 EDA 히스토그램 8셀 복사 → `for` 반복문 한 셀
- [x] 오타 — `random_sate`, `strafity`, `붗꽃`, `커럼`, `변호한`, `cout`, `꽃잎이 길이`, `단일 일정 트리`
- [x] 교재 p.77 `PhysHlth` 설명의 "**정신** 건강" → **신체** 건강, 교재 `Gender` → 실제 파일은 `Sex`

**직접 해본 것**
- 지니 · 엔트로피 함수를 numpy 로 만들어 붓꽃 루트 노드의 `gini = 0.667` 을 직접 계산
- 평가용을 `fit_transform` / `transform` 했을 때 정확도 비교 (0.8626 vs 0.8588)
- 표준화 유무에 따른 SVC · SVR 성능 비교
- SVR 의 `C` 를 1 · 10 · 100 으로 바꿔 RMSE 비교
- `random_state` 0 과 42 의 루트 분할 조건 비교
- 당뇨병 트리를 `max_depth` 3 ~ 제한 없음까지 바꿔 학습용 / 평가용 정확도 표 만들기

**막혔던 부분 / 질문**
- [ ] SVC 의 `kernel='rbf'`(기본값)는 어떻게 직선이 아닌 경계를 만드는지 — 커널 트릭
- [ ] SVC · SVR 의 `C` · `gamma` 를 평가용이 아니라 **교차 검증**(`GridSearchCV`)으로 고르는 방법
- [ ] 결정 트리 여러 개를 합친 **랜덤 포레스트**는 과대적합을 어떻게 줄이는지
- [ ] `max_depth` 말고 `min_samples_leaf` · `min_samples_split` 같은 다른 가지치기 매개변수
- [ ] 당뇨병처럼 **놓치면 안 되는** 문제에서는 정확도 대신 재현율을 봐야 하지 않는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [scikit-learn — Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)
- [`SVC` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) · [`SVR` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html)
- [scikit-learn — Decision Trees](https://scikit-learn.org/stable/modules/tree.html)
- [`DecisionTreeClassifier` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
- [`plot_tree` 문서](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html)
- [CDC Diabetes Health Indicators (UCI Machine Learning Repository)](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)
