# 2026-10-28 수업 실습 — 경사하강법 · 오차역전파 · 최적화 · PyTorch MLP 분류 / 회귀

| 파일 | 내용 |
|---|---|
| `MLP_타이타닉_생존자_예측.ipynb` | 수업 필기 원본 (직접 작성, 학습 → 평가 → `classification_report`) |
| `경사하강법.pdf` · `다중_분류_손실.pdf` | 수업 메모 원본 |
| `딥러닝_메모_수정본.txt` | 위 두 메모를 고친 정리본 (부호 · 용어 · 번호) |
| [`mlp_titanic_binary.ipynb`](./mlp_titanic_binary.ipynb) | 필기 정리 · 개선본 — 분할 → 표준화 → 텐서 · DataLoader → MLP → `BCEWithLogitsLoss` · Adam → 학습 5 단계 → 평가(정확도 · `classification_report` · 혼동 행렬) → 로지스틱 회귀 · 학습률 · 배치 · 에포크 비교 → 자주 하는 실수 |
| [`gradient_descent_backprop.ipynb`](./gradient_descent_backprop.ipynb) | 새로 작성 — 배치 vs 미니배치 → 편미분 · 기울기 → 경사하강법(메모 포물선) · 학습률 → 행렬 모양 → 다중 분류 손실(메모) → 계산 그래프 · 역전파 → 퍼셉트론 기울기 검산 → SGD / Momentum / AdaGrad / Adam |
| [`mlp_diabetes_iris.ipynb`](./mlp_diabetes_iris.ipynb) | 새로 작성 — 당뇨 이진 분류 → 붓꽃 다중 분류(`CrossEntropyLoss`, 정답 형식 실험, 결정 경계) → 붓꽃 회귀(`MSELoss`, 모양 실수) |
| `titanic_cleaned.csv` | 1,308 행 × 11 열 — 타이타닉 생존(0/1) + 특성 10 |
| `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | 70,692 행 × 22 열 — 당뇨 여부(50 : 50) + 설문 특성 21 |
| `iris_dataset.csv` | 150 행 × 5 열 — 붓꽃 측정값 4 + 품종 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 같은 폴더에 두고 실행 (Colab 이면 드라이브 마운트 후 경로만 바꾸기)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `torch` (CPU 로 충분, 당뇨 학습 약 6 초)

## 결과 요약
| 실습 | 결과 |
|---|---|
| 미니배치 (교재 p.46~48) | N = 1046, n = 32 → 1 에포크 **33 번** 업데이트 (마지막 묶음 22 개) |
| 편미분 (교재 p.55) | $x_0^2 + x_1^2$ 의 (3, 4) 기울기 = **(6, 8)** |
| 경사하강법 (메모) | $L = (1-w)^2$, w = 3 · lr 0.1 → 20 걸음 뒤 **w = 1.0231**, lr 1.1 은 발산 |
| 역전파 (교재 p.62) | 사과 220원 → ∂사과값 **2.2** · ∂개수 110 · ∂소비세 200 (PyTorch 와 같음) |
| 퍼셉트론 기울기 | 역전파 · 수치 미분 · PyTorch 모두 **−0.6636** = (a − t)x |
| 최적화 | w = 3.5 출발 : SGD · AdaGrad · Adam(0.3) 가짜 골짜기 1.86, **Momentum(0.02) 진짜 골짜기 −2.12** |
| 타이타닉 MLP | 평가 정확도 **0.8779** (필기 실행 0.8740 · 로지스틱 0.8588), 생존 재현율 0.798, 200 에포크면 0.8397 (과대적합) |
| 당뇨 MLP | **0.7565** (로지스틱 0.7485) |
| 붓꽃 다중 분류 | **30 / 30** (로지스틱 0.9667), 꽃잎 2 특성만 0.9667 |
| 붓꽃 회귀 | RMSE **0.229 cm** (선형 회귀 0.228), 정답 (N,) 실수 시 MSE 19 배 |
