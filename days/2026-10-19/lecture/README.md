# 2026-10-19 수업 실습 — K-Means 군집 평가 · 교차 검증 · GridSearchCV

| 파일 | 내용 |
|---|---|
| `비지도학습_K_Means.ipynb` · `분류모델고도화실습.ipynb` · `2일_비지도학습_K_Means.txt` | 수업 필기 원본 |
| [`kmeans_cluster_evaluation.ipynb`](./kmeans_cluster_evaluation.ipynb) | 정리 · 개선본 — 군집별 데이터 수(`np.unique` · 교차표) → SSE = `inertia_` → 엘보우 → 실루엣 |
| [`cross_validation_gridsearch.ipynb`](./cross_validation_gridsearch.ipynb) | 정리 · 개선본 — hold-out 의 운 → 학습/검증/평가 → K-fold → `cross_val_score` → `GridSearchCV` → `cv_results_` → 깊이 곡선 |
| [`gridsearch_regression.ipynb`](./gridsearch_regression.ipynb) | 교재 p.141 회귀 실습 (새로 작성) — `neg_root_mean_squared_error` · 분할 20번 비교 |
| `iris_dataset.csv` | 붓꽃 150송이 (K-Means) |
| `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | 당뇨병 건강 지표 70,692행 × 22열 (분류 GridSearchCV) |
| `house_price.csv` | 보스턴 집값 506행 × 14열 (회귀 GridSearchCV) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 + 그림 1장 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로 : `./iris_dataset.csv` 등)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`
- `GridSearchCV` 셀은 160번 학습이라 수십 초 걸린다

## 결과 요약
| 실습 | 결과 |
|---|---|
| K-Means (붓꽃 꽃잎, k=3) | 품종과 **96%** 일치 (144 / 150) · 엘보우 k=3 · 실루엣 최고 k=2 (0.765) |
| hold-out 30번 반복 | 500명 : 0.54 ~ 0.76 / 70,692명 : 0.733 ~ 0.748 |
| 5-fold 교차 검증 (깊이 7 트리) | 0.7418 · 0.7467 · 0.7426 · 0.7405 · 0.7377 → 평균 **0.7419** |
| GridSearchCV (당뇨병, 32조합) | best `max_depth=7`, `min_samples_leaf=5` — 검증 0.7419 · 평가 **0.7411** (기본값 트리 0.6545) |
| GridSearchCV (보스턴 회귀) | best `max_depth=8`, `min_samples_leaf=5` — 검증 RMSE 3.85 · 평가 5.40 · 분할 20번 평균 4.82 → **4.64** |
