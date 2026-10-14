# 2026-10-14 수업 실습 (머신러닝교재 v5 · 26-41p, 92-113p)

| 노트북 | 교재 | 내용 | 데이터 |
|---|---|---|---|
| `01_pd_concat_실습.ipynb` | 26~28p | `pd.concat()` axis=0/1, `ignore_index`, `join` | 직접 생성 |
| `02_선형회귀_LinearRegression_실습.ipynb` | 29~41p | 회귀 개념, MAE·MSE·RMSE, 표준화, LinearRegression, Lasso | `house_price.csv` |
| `03_앙상블_분류_RF_XGB_Stacking_실습.ipynb` | 92~113p | Bagging·Boosting·Stacking 분류 | `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` |
| `04_앙상블_회귀_RF_XGB_Stacking_실습.ipynb` | 92~113p | Bagging·Boosting·Stacking 회귀 | `house_price.csv` |

## 실행 방법
- CSV 파일을 노트북과 **같은 폴더**에 두고 실행 (경로: `./파일명.csv`)
- 필요 패키지: `pandas`, `scikit-learn`(1.4 이상, `root_mean_squared_error` 사용), `xgboost`

## 결과 요약 (`random_state=0`)
| 문제 | 모델 | 성능 |
|---|---|---|
| 보스턴 집값 (RMSE ↓) | LinearRegression | 5.457 |
| | Lasso (alpha=1.0) | 5.957 |
| | RandomForest | 4.072 |
| | XGBoost | 4.230 |
| | Stacking (메타: LinearRegression) | 4.195 |
| 당뇨병 분류 (정확도 ↑) | RandomForest | 0.740 |
| | XGBoost | 0.750 |
| | Stacking (메타: LogisticRegression) | 0.748 |

## 원본 코드 대비 수정한 부분
- 하드코딩된 절대경로(`C:\Users\...`) → 상대경로 `./파일명.csv`
- 회귀 앙상블: `XGBRFRegressor`(XGBoost 랜덤 포레스트) → **`XGBRegressor`**(부스팅)로 교체
- 회귀 앙상블: `train_test_split`에 `random_state=0` 추가 (모델 간 공정 비교·재현성)
- 회귀에 쓰지 않는 `accuracy_score` import 제거, 회귀는 RMSE로 평가
- 변수명 오타 `final_mate_learmer` → `final_meta_learner`, "예측 값" 출력 문구 → "정확도"로 정정
- 학습용 확인 셀에서 `y_train.index`를 "평가용"으로 출력하던 라벨 오류 수정
- stratify 효과(정답 비율) 확인 셀, 모델별 결과 비교표, 정리(✅) 섹션 추가
- 선형회귀 노트북 2개(경로만 다름) + Lasso 버전을 하나로 통합, LinearRegression vs Lasso 기울기 비교 추가
