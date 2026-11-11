# 2026-11-10 수업 실습 — 자연어 처리 6일차 : GPT · BERT · 사전 학습 / 전이 학습 / 추론 · `pipeline()` · NSMC 미세 조정

| 파일 | 내용 |
|---|---|
| `nlp_실습9.ipynb` | 수업 필기 원본 — `pipeline('text-classification')` 영어 · 금융(영어 · 한국어) · 영화 리뷰 감성 분석 |
| `nlp_실습10_전이학습.ipynb` | 수업 필기 원본 — NSMC 로 다국어 BERT · KLUE BERT 미세 조정 (`Trainer`, Colab GPU · 전체 데이터) |
| [`bert_mlm_nsp.ipynb`](./bert_mlm_nsp.ipynb) | 교재 p.97~107 — 설치 · 실행 방법 → GPT vs BERT · 크기 → `[CLS] A [SEP] B [SEP]` · 세 임베딩 → MLM 빈칸 맞히기 · 양방향 · 15% 가리기 규칙 → NSP → 같은 단어 '배' 의 문맥 벡터 |
| [`pipeline_inference.ipynb`](./pipeline_inference.ipynb) | `nlp_실습9` 정리 · 개선본 (교재 p.109~111 · 114) — 설치 · 실행 방법 → 영어 감성 → FinBERT · KR-FinBert → 영화 리뷰 `LABEL_0/1` 의 뜻 → **마켓컬리 갈비탕 리뷰 200개** 적용 → KoGPT2 문장 생성 |
| [`nsmc_finetune_bert.ipynb`](./nsmc_finetune_bert.ipynb) | `nlp_실습10_전이학습` 정리 · 개선본 (교재 p.108 · 112~113) — 설치 · 실행 방법 → 데이터 나누기 → 토크나이저 비교([UNK]) → `max_length` → Dataset → 미세 조정 전 · 후 → 저장 · 불러오기 → 추론 · 컬리 리뷰 |
| [`data/kurly_reviews.csv`](./data/) | 마켓컬리 `[사미헌] 갈비탕` 리뷰 200개 (상품명 · 날짜 · 리뷰, 2025-11 ~ 2026-09 · 교재 p.45 수집 과제) |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 모델 · 데이터로 직접 만든 것) |

네이버 영화 리뷰(NSMC) `ratings_train.txt` · `ratings_test.txt` 는 [Day 039 폴더](../../2026-11-03/lecture/)에 이미 있어 다시 올리지 않았다(노트북은 없으면 [e9t/nsmc](https://github.com/e9t/nsmc) 에서 바로 읽는다). 교재 PDF · BERT 논문 PDF 는 올리지 않았다 — 논문은 [arXiv 1810.04805](https://arxiv.org/abs/1810.04805).

## 실행 방법
1. **설치** : `pip install transformers accelerate torch scikit-learn pandas` (Colab 은 모두 기본 포함)
   - `Trainer` 는 **`accelerate`** 가 없으면 `ImportError` — 로컬에서는 꼭 함께 설치
2. **모델** : 첫 실행 때 Hugging Face 에서 자동으로 받는다 → **인터넷 필요** (세 노트북 합쳐 약 3.5GB)
3. **데이터** : `kurly_reviews.csv` 는 노트북 폴더 또는 `data/` 에 · NSMC 는 자동
4. **실행** : 노트북을 열고 맨 위부터 **[런타임] → [모두 실행]**. 각 노트북 0절에 설치 셀(주석 처리)이 있다
5. **시간**
   - `bert_mlm_nsp` · `pipeline_inference` : 예측만 — CPU 로 몇 분 (다운로드 제외)
   - `nsmc_finetune_bert` : **GPU 면 전체 데이터**(원본과 같게, 모델당 약 15~20분) · **CPU 면 학습 3,000 · 평가 2,000 개만** 뽑아 모델당 약 8~10분 — 저장된 결과는 CPU 실행

## 결과 요약
| 실습 | 결과 |
|---|---|
| klue/bert-base 크기 | 본체 110,026,752개 · 12층 · 768 · 12 head · 사전 32,000 |
| 특수 토큰 번호 | klue `[CLS] 2 · [SEP] 3 · [MASK] 4` (교재 p.101 과 같음) · 영어 BERT `101 · 102 · 103` |
| MLM 교재 예문 `공항을 가는데 [MASK] 너무 막혀서` | 1위 `길이` 0.61 · 2위 `차가` 0.30 |
| 양방향 (`오늘 [MASK]가 너무 ~`) | 막혀서 → `비행기` · 아파서 → `아침` `하루` `머리` · 고파서 → `배` 0.85 |
| 15% 가리기 | 가려진 비율 14.9% → [MASK] 80.5% · 무작위 9.6% · 그대로 9.9% (논문 80 · 10 · 10) |
| NSP | 이어지는 쌍 IsNext 1.000 · 엉뚱한 쌍 NotNext 0.985~0.997 |
| 같은 '배' 의 문맥 벡터 | 타는 배끼리 0.83 · 먹는 배끼리 0.69 · 다른 뜻 0.46~0.66 |
| 영어 감성 (SST-2 모델) | awesome POSITIVE 0.9999 · awful NEGATIVE 0.9997 |
| KR-FinBert-SC | '사상 첫 6,600선' neutral 0.909 — '사상 최고치' · '큰 폭 상승' 으로 바꿔도 neutral |
| 컬리 리뷰 200개 (영화 리뷰 모델) | 긍정 196 · 부정 4 — 부정 4개는 모두 먹는 방법 · 제안 문장(확신도 0.51~0.65, 오분류) |
| KoGPT2 | 가중치 125,164,032개 · `PreTrainedTokenizerFast` 에 특수 토큰을 지정해야 글자가 깨지지 않음 |
| 토큰화 (NSMC 2만 개) | 90% 분위수 다국어 51 · KLUE 43 · 평균 24.1 · 20.4 · **[UNK] 가 있는 리뷰 다국어 29.2% · KLUE 5.1%** |
| 미세 조정 전 (분류층 무작위) | KLUE 평가 정확도 0.576 |
| 미세 조정 후 (CPU · 학습 3,000 · 1 에폭) | 다국어 **0.697** (10.2분) · KLUE **0.843** (7.8분) — 원본(GPU · 학습 12만) 0.848 · 0.898 |
| 저장 → 불러오기 | 정확도 0.843 그대로 · 레이블 `{0: 'negative', 1: 'positive'}` |
| 컬리 리뷰 — 내 모델 vs 공개 모델 | 두 모델 일치율 98.0% (내 모델 긍정 198 · 부정 2) |
