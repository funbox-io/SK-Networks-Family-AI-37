# 2026-11-02 수업 실습 — 2차 팀 프로젝트 발표 : 이커머스 고객 이탈 예측 (ShopInsight)

| 파일 | 내용 |
|---|---|
| [`team_project/`](./team_project/) | [팀 저장소 `SKN37-2ST-2TEAM`](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN37-2ST-2TEAM) 원본 그대로 — `app.py`(Streamlit 대시보드) · `requirements.txt` · `.streamlit/config.toml` · `data/` · `models/` |
| `team_project/data/[2nd] customer_churn_ecommerce_cleaned.csv` | 정제 데이터 36,992명 × 23열 (정답 `churn_risk_score` 0/1, 이탈 54.1%) |
| `team_project/models/mlp_churn_4features.pth` · `mlp_churn_preprocessor.pkl` | 팀 MLP 가중치(11 → 32 → 16 → 1) · 전처리기(scikit-learn 1.6.1) |
| [`churn_project_eda.ipynb`](./churn_project_eda.ipynb) | EDA 다시 보기 — 데이터 품질(중앙값 대체 697.62 · 음수 포인트) → 멤버십 / 피드백별 이탈률 → 수치형 분포 · 포인트 계단 → 규칙으로 고객 3그룹 → 상관 |
| [`churn_project_mlp.ipynb`](./churn_project_mlp.ipynb) | 같은 전처리 · 같은 MLP 다시 학습 → 팀 `.pth` 직접 평가 → 규칙 / 로지스틱 / 결정 트리 비교 → 결정 경계 → 변수 추가 실험 → 순열 중요도 → 임계값 → 대시보드 입력 점검 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 같은 시드로 직접 만든 것) |

## 실행 방법
- 노트북은 `team_project/` 폴더와 **같은 위치**에서 실행 (데이터 · 모델을 `team_project/data/`, `team_project/models/` 에서 읽음)
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `torch` — `churn_project_mlp.ipynb` 는 MLP 를 여러 번 학습해 CPU 로 2~3분
- 팀 모델은 `torch.load(..., weights_only=True)` 로 가중치만 읽는다. 전처리기 `.pkl` 은 열지 않고 같은 분할로 다시 fit
- 대시보드 실행 : `cd team_project && pip install -r requirements.txt && python -m streamlit run app.py`

## 결과 요약
| 실습 | 결과 |
|---|---|
| 데이터 품질 | 포인트 697.62(중앙값 대체) 3,446명 · 음수 포인트 136명 |
| 이탈률 | Platinum·Premium 0% · No·Basic 97% · 긍정 피드백 0% · 거래 5만 초과 0% (2,874명 전원 앞 조건과 겹침) |
| 고객 3그룹 | 확실한 유지 29.8% · 거의 이탈 41.7% · 애매한 고객 28.5% (이탈률 0.481) |
| 포인트 기준 | 애매한 고객에 '포인트 ≤ 700 → 이탈' 규칙 정확도 0.796 (최고) |
| 팀 모델 다시 평가 | 정확도 0.935 · 정밀도 0.946 · 재현율 0.933 · F1 0.940 · AUC 0.977 (README 0.938 · 0.945 · 0.940 · 0.942 · 0.976) |
| 다시 학습한 MLP | 정확도 0.934 · F1 0.940 · AUC 0.975, 검증 손실 0.167 에서 평평 |
| 단순 모델 | 규칙 3줄 0.931 · 결정 트리 깊이 4 0.931 · 로지스틱 0.914 · 전부 이탈 0.541 |
| 변수 추가 | 멤버십 0.855 → + 포인트 0.926 → + 피드백 0.930 → + 거래 금액 0.932 |
| 순열 중요도 | 멤버십 0.249 · 포인트 0.089 · 피드백 0.076 · 거래 금액 0.001 |
| 임계값 | 0.5 : FN 176 · FP 316 / 0.3 : FN 89 · FP 451 / 0.2 : FN 29 · FP 510 |
