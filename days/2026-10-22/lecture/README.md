# 2026-10-22 수업 실습 — 딥러닝 시작 (퍼셉트론 · XOR · MLP) · 고객 이탈 순열 특성 중요도

| 파일 | 내용 |
|---|---|
| `고객이탈예측 2.ipynb` | 수업 필기 원본 |
| `딥러닝_1일.txt` | 수업 메모 — 틀린 내용을 고친 판 (고친 줄 끝에 `[수정]`) |
| [`perceptron_logic_gates.ipynb`](./perceptron_logic_gates.ipynb) | 정리 · 개선본 — 딥러닝 개요 → 퍼셉트론 수식 · 계단 함수 → AND / OR / NAND → 퍼셉트론 학습 규칙 → XOR 실패 → MLP 로 XOR → sklearn `Perceptron` · `MLPClassifier` |
| [`churn_permutation_importance.ipynb`](./churn_permutation_importance.ipynb) | 정리 · 개선본 — `permutation_importance` 매개변수 → `Bunch` 키 2가지 → 중요도 Top 10 → `n_repeats` → 학습용 vs 평가용 비교 |
| `Telco-Customer-Churn.csv` | 통신사 고객 이탈 7,043행 × 21열 ([데이터 설명서](../../2026-10-15/lecture/)) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 + 그림 1장 (노트북 코드로 직접 만든 것) |

## 실행 방법
- CSV 를 노트북과 **같은 폴더**에 두고 실행 (경로 : `./Telco-Customer-Churn.csv`)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn` (TensorFlow · PyTorch 없이 퍼셉트론을 numpy 로 구현)

## 결과 요약
| 실습 | 결과 |
|---|---|
| 퍼셉트론 게이트 (w = 0.5, 0.5) | b = −0.7 → AND, b = −0.2 → OR, (−0.5, −0.5, +0.7) → NAND |
| 퍼셉트론 학습 규칙 (η = 0.25) | AND 6 epoch · OR 4 epoch · NAND 6 epoch 만에 4개 모두 정답 |
| XOR (단층) | 학습 규칙 실패 · 가중치/편향 9,261가지 중 최고 3 / 4 · sklearn `Perceptron` 0.5 |
| XOR (다층) | NAND · OR → AND 로 4 / 4 · `MLPClassifier(4,)` 1.0 (뉴런 2개는 5번 중 2번 성공) |
| 순열 특성 중요도 (평가용, F1) | `tenure` 0.252 > 월 단위 계약 0.070 > 2년 계약 0.041 > 광랜 0.030 > 총 요금 0.025 |
| 학습용 vs 평가용 | 순열끼리 비교하면 상위 5개 순위 동일 (필기의 계수 비교는 스케일링 착시 — `tenure` 37위) |
