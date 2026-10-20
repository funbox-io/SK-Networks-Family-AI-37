# 2026-10-20 수업 실습 — 랜덤 포레스트 · XGBoost 튜닝 · RandomizedSearchCV · 스태킹 · 평가 지표

| 파일 | 내용 |
|---|---|
| `분류 모델 성능 고도화 실습 1.ipynb` | 수업 필기 원본 |
| [`hyperparameter_search_rf_xgb.ipynb`](./hyperparameter_search_rf_xgb.ipynb) | 정리 · 개선본 — 랜덤 포레스트 `GridSearchCV` 80조합 → `RandomizedSearchCV` 30/240 (accuracy · f1 함께) → Grid vs Random 1,000번 흉내 → XGBoost `GridSearchCV` (`min_samples_leaf` 무시 확인) → 결과 비교 → `joblib` 저장 |
| [`stacking_classifier.ipynb`](./stacking_classifier.ipynb) | 정리 · 개선본 — `StackingClassifier` → out-of-fold 예측 직접 구현 · 메타 모델 계수 → out-of-fold 를 안 하면? → 기본 모델 상관 → 교재 p.111 버전 |
| [`classification_evaluation.ipynb`](./classification_evaluation.ipynb) | 교재 `모델검증및평가` 18장 실습 (새로 작성) — 혼동 행렬 · 정확도 · 재현율 · 정밀도 · F1 직접 계산 → 불균형 데이터 → 임계값 → 내장 vs 순열 특성 중요도 |
| `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | 당뇨병 건강 지표 70,692행 × 22열 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 + 그림 3장 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로 : `./diabetes_...csv`)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `xgboost`, `joblib`
- `hyperparameter_search_rf_xgb.ipynb` 를 **먼저** 실행 — 탐색 때문에 약 30분(2코어). 튜닝한 모델을 `./models/*.pkl` 로 저장하고, 나머지 두 노트가 불러 쓴다 (없으면 찾은 조합으로 바로 학습)
- `models/` 의 `.pkl` 은 최대 75 MB 라 저장소에 올리지 않았다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 랜덤 포레스트 `GridSearchCV` (80조합, 13.5분) | best `n_estimators=400, max_depth=9, min_samples_leaf=2` — 검증 0.7511 · 평가 **0.7519** (기본값 0.7402) |
| 랜덤 포레스트 `RandomizedSearchCV` (30/240, 12.3분) | best `800, 10, 4` — 검증 **F1 0.7617** / 정확도 0.7512 · 평가 0.7520 |
| Grid vs Random 1,000번 흉내 | 20개만 뽑아도 1등과 평균 0.0005 차이, 30개면 84% 확률로 상위 5% |
| XGBoost `GridSearchCV` (36조합, 1.1분) | best `learning_rate=0.05, max_depth=4, n_estimators=200` — 검증 0.7537 · 평가 **0.7544** (기본값 0.7498) |
| 스태킹 (튜닝 3개 + 로지스틱) | 평가 정확도 0.7548 · F1 0.7605 — 메타 계수 xgb 3.90 · rf 1.61 · dt −0.15 |
| out-of-fold 없이 메타 학습 | 기본값 트리 계수 13.9 → 평가 0.652 (XGBoost 혼자 0.754 보다 나쁨) |
| XGBoost 평가 지표 | 재현율 0.790 · 정밀도 0.737 · F1 0.763 · 임계값 0.4 에서 F1 최고 0.778 |
| 불균형(당뇨 5%) | "전부 정상" 정확도 0.95 · F1 0 / XGBoost 정확도 0.725 · 재현율 0.85 |
