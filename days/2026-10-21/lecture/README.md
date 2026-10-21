# 2026-10-21 수업 실습 — 모델 검증 및 평가 종합 실습 (고객 이탈 · 보스턴 집값)

| 파일 | 내용 |
|---|---|
| `고객이탈예측_1.ipynb` · `회귀 모델 성능 고도화 실습.ipynb` | 수업 필기 원본 |
| [`churn_model_evaluation.ipynb`](./churn_model_evaluation.ipynb) | 정리 · 개선본 — 전처리 → EDA → 인코딩 → 로지스틱 회귀(수렴 경고 · 스케일링 전/후 계수) → `GridSearchCV` (필기 `C`·`max_iter` / 개선 스케일링 + `class_weight`) → 혼동 행렬 → 내장 vs 순열 특성 중요도 → SVM (기본 → 고도화) → 결정 트리 (기본 → 고도화) → 모델 비교. 모델마다 생성 · 학습 · 예측 · 평가 · 고도화를 단계별 코드 · 주석으로 |
| [`regression_model_evaluation.ipynb`](./regression_model_evaluation.ipynb) | 정리 · 개선본 — RMSE → 결정 트리 `GridSearchCV` · `RandomizedSearchCV` → 랜덤 포레스트 `RandomizedSearchCV` (필기 / 기본값 포함) → `RepeatedKFold` → 특성 중요도 검증 |
| `Telco-Customer-Churn.csv` | 통신사 고객 이탈 7,043행 × 21열 ([데이터 설명서](../../2026-10-15/lecture/)) |
| `house_price.csv` | 보스턴 집값 506행 × 14열 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 + 그림 1장 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로 : `./Telco-Customer-Churn.csv`, `./house_price.csv`)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`
- 회귀 노트의 랜덤 포레스트 탐색(600번 학습) · 반복 교차 검증은 2코어 기준 약 3분 (`n_jobs=-1`)
- 이탈 노트의 SVC 탐색(90번 학습) · 결정 트리 탐색(450번) · 순열 중요도는 2코어 기준 약 3분

## 결과 요약
| 실습 | 결과 |
|---|---|
| 로지스틱 회귀 (필기, 스케일링 X) | `ConvergenceWarning` (100번 안에 수렴 실패) · 정확도 0.807 · F1 0.602 |
| `GridSearchCV` 필기 (`C` × `max_iter`, f1) | best `C=100, max_iter=500` · 검증 F1 0.598 (`max_iter` 차이는 수렴 실패 잡음) |
| `GridSearchCV` 개선 (스케일링 + `C` × `class_weight`) | best `C=100, balanced` · 검증 F1 0.628 · 평가 F1 **0.632** · 재현율 0.553 → **0.794** |
| 특성 중요도 검증 | 로지스틱 : `tenure` · `TotalCharges` 내장 = 순열 1 · 2위 (스케일링 X 계수로는 35위 · 45위) / 기본값 트리 : `MonthlyCharges` 내장 0.184 → 순열 0.005 (과대적합) |
| SVM | 스케일링 X : 전부 "유지"(재현율 0) / 스케일링 O : 정확도 0.797 / 고도화 (`C=1`, `balanced`) : 재현율 0.762 · F1 0.614 |
| 결정 트리 | 기본값 : 깊이 27, 학습 0.998 → 평가 0.719 / 고도화 (깊이 7, 리프 50, `balanced`) : 재현율 0.783 · F1 0.625 |
| 결정 트리 회귀 `GridSearchCV` (72가지) | best `max_depth=8, leaf=5` · 검증 RMSE 3.85 · 평가 5.40 |
| 랜덤 포레스트 회귀 | 기본값 평가 **4.07** / 필기 `RandomizedSearchCV` 4.31 (기본값 `leaf=1` 이 탐색 범위에 없음) / 기본값 포함 탐색 검증 3.16 · 평가 4.57 · 반복 교차 검증 **3.26** (기본값 3.44) |
