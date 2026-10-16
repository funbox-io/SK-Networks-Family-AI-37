# 2026-10-16 수업 실습 — 차원 축소(PCA) · AutoML(AutoGluon) · 비지도 학습(K-Means)

| 파일 | 내용 |
|---|---|
| `PCA실습.ipynb` · `AutoGluon.ipynb` · `비지도학습_K_Means.ipynb` · `1일_비지도학습_K_Means.txt` | 수업 필기 원본 |
| [`pca_dimensionality_reduction.ipynb`](./pca_dimensionality_reduction.ipynb) | 정리 · 개선본 — 차원의 저주 → PCA 원리 → 3차원 PC1 · PC2 · PC3 → 손글씨 64→2 · 3차원 · 95% → 복원 → PCA + KNN |
| [`automl_autogluon.ipynb`](./automl_autogluon.ipynb) | 정리 · 개선본 — AutoML 개념 → `TabularPredictor` → `fit` → 리더보드 → `evaluate` → 저장 모델 → 어제 모델과 비교 |
| [`kmeans_clustering.ipynb`](./kmeans_clustering.ipynb) | 정리 · 개선본 — 비지도 학습 → K-Means 직접 구현 → `KMeans` k=2 / 3 → 정답 비교 → 엘보우 |
| `iris_dataset.csv` | 붓꽃 150송이 (K-Means) |
| `Telco-Customer-Churn.csv` | 통신사 고객 이탈 7,043행 × 21열 (AutoGluon) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 7개 + 그림 2장 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로 : `./iris_dataset.csv`, `./Telco-Customer-Churn.csv`)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`
- AutoGluon : `pip install -U "autogluon.tabular[all]>=1.6.0"` — 학습에 약 5분, 모델 폴더 `AutoGluon_Model/` 은 수백 MB 라 GitHub 에 올리지 않음
- 손글씨 숫자 데이터는 `sklearn.datasets.load_digits()` 내장

## 결과 요약
| 실습 | 결과 |
|---|---|
| PCA (손글씨 64차원) | 2개 = 정보 28.5% · 3개(PC3 추가) = 40.3%, KNN 0.617 → 0.747 · **29개 = 95%** · KNN 정확도 64개 0.978 → 29개 0.975 |
| AutoGluon (고객 이탈) | best `WeightedEnsemble_L3` — 평가용 정확도 **0.803**(수업) / **0.814**(다시 실행) vs 로지스틱 회귀 0.808 |
| K-Means (붓꽃 꽃잎) | k=3 → 품종과 **96%** 일치 · 엘보우 k=3 (SSE 550.9 → 86.4 → 31.4) |
