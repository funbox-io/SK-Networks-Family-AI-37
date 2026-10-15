# 2026-10-15 수업 실습 — 고객 이탈 예측 (로지스틱 회귀 · SVM · 결정 트리)

| 파일 | 내용 |
|---|---|
| `고객이탈예측.ipynb` | 수업 필기 원본 |
| [`churn_classification.ipynb`](./churn_classification.ipynb) | 정리 · 개선본 — 전처리 → EDA → 인코딩 → 로지스틱 회귀 · SVM(스케일링 전/후) · 결정 트리(깊이) → 임계값 → 모델 비교 |
| `Telco-Customer-Churn.csv` | 실습 데이터 (7,043행 × 21열) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 4개 + EDA · 모델 비교 그림 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로: `./Telco-Customer-Churn.csv`)
- 필요 패키지: `pandas`, `plotly`, `matplotlib`, `scikit-learn`
- `SAVE_GIF = False` 로 바꾸면 GIF 를 다시 만들지 않아 빨리 끝난다
- 수업 EDA 그래프는 plotly 라 GitHub 미리보기에서는 안 보임 → 같은 내용을 `images/00_eda.png` 로도 저장

## 결과 요약 (`random_state=0`, 평가용 1,407명)
| 모델 | 정확도 | 재현율(이탈) | F1 |
|---|---|---|---|
| 기준선 (전부 "유지") | 0.734 | 0 | 0 |
| **LogisticRegression** (스케일링) | **0.808** | 0.554 | 0.605 |
| SVC (스케일링 X — 필기 그대로) | 0.734 | 0 | 0 |
| SVC (스케일링 O) | 0.797 | 0.471 | 0.553 |
| DecisionTree (기본값 — 필기 그대로) | 0.719 | 0.476 | 0.474 |
| DecisionTree (`max_depth=3`) | 0.795 | 0.390 | 0.503 |
| LogisticRegression (임계값 0.3) | 0.772 | **0.765** | **0.641** |
