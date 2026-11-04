# 2026-10-30 수업 실습 — 2차 팀 프로젝트 개발 : Streamlit 대시보드 (ShopInsight)

| 파일 | 내용 |
|---|---|
| `team_project/app.py` | 대시보드 **최종본** (967줄) — 핵심 지표 · 고객 이탈 예측 · 이탈 원인 분석 · 모델 성능 |
| `team_project/app_v1.py` | 대시보드 **초기본** (919줄) — 요약 · 데이터 분석 페이지, 금액을 원 단위로 입력 |
| `team_project/requirements.txt` · `.streamlit/config.toml` | 패키지 목록 · 테마(라이트, 주 색 `#2f62f0`) |
| `team_project/data/[2nd] customer_churn_ecommerce_cleaned.csv` | 정제 데이터 36,992명 × 23열 |
| `team_project/models/mlp_churn_4features.pth` · `mlp_churn_preprocessor.pkl` | MLP 가중치(11 → 32 → 16 → 1) · 전처리기(scikit-learn 1.6.1) |
| [`streamlit_dashboard_logic.ipynb`](./streamlit_dashboard_logic.ipynb) | 앱 구조 · Streamlit 기능 → KPI → `create_analysis_tables` 재현 → 4분위 동점 문제 → `ChurnMLP` NumPy 변환 검증 → 입력 폼 계산 → `evaluate_mlp` · ROC |
| [`app_version_changes.ipynb`](./app_version_changes.ipynb) | `difflib` 비교 → 변경 분류 → 금액 단위 검증 → 계산 함수 동일 확인 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 같은 모델로 직접 만든 것) |

## 실행 방법
- 노트북은 `team_project/` 폴더와 **같은 위치**에서 실행
- 필요 패키지 : `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `torch` (노트북은 Streamlit 없이 돈다)
- 팀 모델은 `torch.load(..., weights_only=True)` 로 가중치만 읽고, 전처리기 `.pkl` 은 열지 않고 같은 분할로 다시 fit
- 대시보드 실행 : `cd team_project && pip install -r requirements.txt streamlit && python -m streamlit run app.py`

## 결과 요약
| 실습 | 결과 |
|---|---|
| KPI | 36,992명 · 이탈 라벨 54.1% · 특성 22개 · 결측 0 |
| 회원 등급 · 피드백 | No 97.1% · Basic 96.8% · Silver 42.8% · Gold 37.0% · Platinum · Premium 0% / 긍정 피드백 0% |
| 로그인 간격 | 1–4일 5.3% · 5–8일 51.0% · 9–14일 51.3% · 15일 이상 58.2% |
| 4분위 동점 | 포인트 697.62 3,446명 → 중하위 1,724 · 중상위 1,722 로 갈림, 행 순서를 섞으면 88.6 → 88.1% · 26.6 → 27.1% |
| NumPy 변환 | scikit-learn `ColumnTransformer` 와 `allclose = True` (7,399 × 11) |
| 입력 폼 | Gold · 거래 25,000 · 부정 : 포인트 720 → 7.7% / 650 → 96.5%, 판정이 420 · 560 · 700 · 830 · 1,110점에서 바뀜 |
| 모델 성능 | 정확도 93.50% · 정밀도 94.60% · 재현율 93.31% · F1 93.95% · AUC 97.65% |
| 버전 비교 | 919 → 967줄, 변경 23군데(추가 91 · 삭제 43줄), 계산 함수 5개 동일 |
