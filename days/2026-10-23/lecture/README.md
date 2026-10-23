# 2026-10-23 수업 실습 — 퍼셉트론 실습 · 활성화 함수 · 행렬 곱 신경망 · 출력층 설계

| 파일 | 내용 |
|---|---|
| `퍼셉트론.ipynb` · `퍼셉트론_2.ipynb` | 수업 필기 원본 (직접 작성 · 강의 코드) |
| `딥러닝_1일_수정본.txt` | 1 · 2일차 수업 메모 정리본 |
| [`activation_functions.ipynb`](./activation_functions.ipynb) | 정리 · 개선본 — numpy 기초 → 논리 게이트(계단 함수) → 활성화 함수가 필요한 이유 → 계단 / 시그모이드 / ReLU 와 기울기 → 기울기 소실 |
| [`neural_network_forward.ipynb`](./neural_network_forward.ipynb) | 정리 · 개선본 — 행렬 곱 → 층 = X·W + B → 3층 순전파 → 항등 / 시그모이드 / 소프트맥스 → 출력 뉴런 수 → sklearn MLP 순전파 직접 계산 |
| `iris_dataset.csv` · `house_price.csv` | 출력층 설계 실습 (붓꽃 다중 · 이진 분류, 보스턴 집값 회귀) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn` (TensorFlow · PyTorch 없이 numpy 로 구현)

## 결과 요약
| 실습 | 결과 |
|---|---|
| 논리 게이트 (계단 함수) | AND [0 0 0 1] · NAND [1 1 1 0] · OR [0 1 1 1] · XOR [0 1 1 0] |
| 활성화 함수 없는 2층 | 직선 1개(W = W1·W2, B = b1·W2 + b2)와 결과가 완전히 같다 |
| ReLU 곡선 근사 | 뉴런 1개 RMSE 0.443 → 12개 0.006 |
| 기울기 소실 | 시그모이드 최대 기울기 0.25ⁿ — 10층 9.5e-07, ReLU 는 1 |
| 행렬 곱 | 교재 예시 [[2, 1], [13, 5]] · (1,2)×(2,3)+(3,) = (1,3) |
| 소프트맥스 | [0.3, 2.9, 4.0] → [0.018, 0.245, 0.737], 합 1 · [1010, 1000, 990] 도 최댓값 빼면 계산 가능 |
| sklearn MLP 출력층 | 다중 분류 softmax · 3개 / 이진 분류 logistic · 1개 / 회귀 identity · 1개, 직접 계산 = `predict_proba` |
