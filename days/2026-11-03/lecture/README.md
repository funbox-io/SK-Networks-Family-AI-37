# 2026-11-03 수업 실습 — 자연어 처리 1일차 : 전처리 · 토큰화 · 서브워드(BPE · WordPiece) 단어 사전

| 파일 | 내용 |
|---|---|
| `11_03메모.txt` | 수업 메모 원본 (자연어 처리 과정 · 불용어 · 형태소 · NLTK · OOV · BPE) |
| `11_03메모_수정본.txt` | 메모 수정본 (불용어 정의 · 텍스트 구조 · 형식 형태소 · 접속사 · NLTK · BPE 빈도 · 바이그램 오타) |
| `단어사전.ipynb` | 수업 필기 원본 (Colab — `BertWordPieceTokenizer` 사전 생성 · `BertTokenizerFast` 토큰화) |
| `vocab.txt` | 필기에서 만든 단어 사전 원본 (3만 개, 리뷰 id 숫자 토큰 5,778개 포함) |
| [`nlp_preprocessing_tokenization.ipynb`](./nlp_preprocessing_tokenization.ipynb) | 메모 정리 · 개선본 — 자연어 처리 5단계 → 텍스트 구조 → 특수문자 · 불용어 제거 → 형태소(`kiwipiepy`) → 영어 / 한글 불용어 → NLTK `sent_tokenize` · `word_tokenize` → 어절 사전 OOV |
| [`bpe_subword_tokenization.ipynb`](./bpe_subword_tokenization.ipynb) | 교재 BPE 예시 직접 구현 → 바이그램 빈도 → 병합 4단계 → 새 단어 토큰화 → `tokenizers` BPE 대조 → BPE vs WordPiece 병합 기준 |
| [`wordpiece_vocab_nsmc.ipynb`](./wordpiece_vocab_nsmc.ipynb) | 필기 `단어사전` 정리 · 개선본 — 리뷰만 뽑은 말뭉치 → `BertWordPieceTokenizer` 학습 · 원본 방식 비교 → `vocab.txt` 저장 → `BertTokenizerFast` (`do_lower_case` · `strip_accents` 함정) → id → `[CLS]`/`[SEP]` · `attention_mask` · 패딩 → 복원 규칙 → OOV 비교 · `limit_alphabet` · 사전 크기 |
| `ratings_train.zip` · `ratings_test.txt` | 네이버 영화 리뷰 NSMC 15만 · 5만 행 (탭 구분 `id · document · label`, 리뷰 결측 8개) — `ratings_train.txt` 는 14.6MB 라 zip 으로 올림 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 (노트북과 같은 데이터 · 토크나이저로 직접 만든 것) |

## 실행 방법
- `ratings_train.zip` · `ratings_test.txt` (· 비교용 `vocab.txt`)를 노트북과 **같은 폴더**에 두고 실행 (Colab 은 왼쪽 📁 에 업로드). 노트북 첫 데이터 셀이 zip 을 풀고, 파일이 아예 없으면 [NSMC 저장소](https://github.com/e9t/nsmc)에서 내려받는다
- 필요 패키지 : `pandas`, `nltk`, `kiwipiepy`, `tokenizers`, `transformers` — Colab 은 `!pip install kiwipiepy` 만 추가
- NLTK 데이터 : `nltk.download('punkt_tab')` · `nltk.download('stopwords')` (노트북 안에서 실행)
- `wordpiece_vocab_nsmc.ipynb` 는 사전을 여러 번 학습해서 1 ~ 2분 걸린다. 학습이 여러 스레드로 돌아 실행마다 id 가 조금 달라질 수 있다

## 결과 요약
| 실습 | 결과 |
|---|---|
| NLTK | `sent_tokenize('Hello Mr. Smith. How are you?')` → 2문장 (`split('. ')` 은 3조각) · `word_tokenize("Don't …")` → `Do / n't / … / .` |
| 불용어 | 영어 198개, 예문 33 단어 → 14 단어 (빈도 1~3위 the · was · and 가 모두 불용어) · 한글 `꽃밭에 꽃이 많이 피었다` → 꽃밭 · 꽃 · 많이 · 피 |
| 어절 사전 OOV | 학습 어절 357,862종 중 3만 개 사전 → 테스트 어절 **36.1%** OOV, `재미…` 어절만 2,362종 |
| BPE (교재 예시) | ug(20) → un(16) → hug(15) → pun(12), 최종 사전 11개 — 직접 구현 = `tokenizers` = 교재 |
| BPE vs WordPiece | 첫 병합 BPE `(u, g)` 빈도 20 / WordPiece `(g, s)` 점수 0.050 |
| WordPiece 사전 | 리뷰만 학습 : 숫자 토큰 154개 · `##` 조각 29.6% / 원본 파일 학습 : 숫자 토큰 5,778개(19.3%) |
| `BertTokenizerFast` 옵션 | `lowercase=False` 무시(`Marvel` → `m ##ar …`) · `strip_accents` 없으면 한글 전부 `[UNK]` |
| `[UNK]` 비율 (사전 3만) | 어절 36.1% → WordPiece 1.3% → `limit_alphabet=6000` **0.04%** |
| 사전 크기 | 리뷰당 평균 토큰 1,000개 28.0 · 5,000개 18.1 · 30,000개 14.1 |
