# 2026-11-09 수업 실습 — 자연어 처리 5일차 : RNN 의 한계 · seq2seq · Transformer · self-attention

| 파일 | 내용 |
|---|---|
| `nlp_실습8.ipynb` | 수업 필기 원본 — 임베딩 (3, 512) · 가중치 (512, 1536) → Q · K · V → score → scaling → softmax → output |
| [`rnn_limits_seq2seq.ipynb`](./rnn_limits_seq2seq.ipynb) | 교재 p.79~89 — 설치 · 실행 방법 → BPTT 연쇄 법칙 · 기울기 소멸 / 폭주 실측 → 병렬 처리(기다리는 단계 수) → seq2seq 문맥 벡터 vs 어텐션 (숫자 뒤집기, 길이 5~30) → 교재 p.85 분류 코드의 `Sigmoid` · 손실 짝 → `TransformerEncoderLayer` 구조 |
| [`self_attention_scratch.ipynb`](./self_attention_scratch.ipynb) | `nlp_실습8` 정리 · 개선본 (교재 p.90~96) — 설치 · 실행 방법 → WordPiece 토큰 번호 → 임베딩 + 위치(학습형 · sin/cos) → Q · K · V → score → √d_k 로 나누는 이유 → softmax(`dim=-1`) → weight × V → `F.scaled_dot_product_attention` 확인 → 위치 정보가 없으면? → 같은 단어 · 다른 문맥 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 계산 · 같은 시드로 직접 만든 것) |

## 실행 방법
1. **설치** : `pip install torch transformers` (Colab 은 기본 포함)
   - `transformers` 는 `self_attention_scratch` §1 에서 BERT WordPiece 토크나이저(사전 30,522개, 약 0.5MB)를 받는 데만 쓴다 → **인터넷 필요**
2. **데이터** : 받을 파일 없음 (`rnn_limits_seq2seq` 의 숫자 뒤집기 데이터는 코드가 만든다)
3. **실행** : 노트북을 열고 맨 위부터 **[런타임] → [모두 실행]**. 각 노트북 0절에 설치 셀(주석 처리)이 있다
4. **시간** : `self_attention_scratch` 몇 초 · `rnn_limits_seq2seq` CPU 로 약 4~5분 (seq2seq 8번 학습). 다른 무거운 작업과 동시에 돌리면 크게 느려진다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 기울기 소멸 (무작위 RNN, 59칸 거슬러) | W_h × 0.5 : 9.2e-21 · × 1.0 : 1.7e-5 · × 3.0 : **1.0e+5 (폭주)** |
| 선형 RNN 30칸 | W_h × 0.5 : 1.9e-9 · × 1.0 : 2.1 · × 1.5 : 4.0e+5 |
| seq2seq 숫자 뒤집기 (같은 GRU 64 · 1,500번 학습) | 길이 5 : 0.982 → 어텐션 0.999 · 10 : 0.832 → 0.908 · **20 : 0.468 → 0.688** · 30 : 0.324 → 0.394 |
| 교재 p.85 코드 (`Sigmoid` 출력) | `BCELoss(확률)` = `BCEWithLogitsLoss(logit)` = 0.7619 · `BCEWithLogitsLoss(확률)` 0.7477 (틀림) |
| `TransformerEncoderLayer(512, 8 head)` | 가중치 3,152,384개 · 입력 · 출력 모양 (1, 3, 512) 그대로 |
| `I love you` (BERT WordPiece) | `['i', 'love', 'you']` → `[1045, 2293, 2017]` |
| 내적 크기 | d = 4 · 64 · 512 → 표준편차 2.0 · 7.9 · 22.7 (≈ √d) → ÷√d 후 ≈ 1.0 |
| attention weight (시드 0, 학습 전) | I : `[0.06, 0.03, 0.91]` · love : `[0.16, 0.05, 0.79]` · you : `[0.15, 0.02, 0.82]` (행 합 1) |
| 손계산 vs `F.scaled_dot_product_attention` | 같음 |
| 위치 정보 없이 순서 바꾸기 | 결과도 줄만 바뀜 (내용 같음) — 위치를 더하면 달라짐 |
| `I love you` · `you love me` 의 `love` | 입력 벡터는 같은데 self-attention 뒤 코사인 0.609 (문맥 반영) |
