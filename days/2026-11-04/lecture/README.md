# 2026-11-04 수업 실습 — 자연어 처리 2일차 : 한글 형태소 분석기 · 단어 빈도 · 워드클라우드

| 파일 | 내용 |
|---|---|
| `단어사전02.ipynb` | 수업 필기 원본 — Okt · Mecab `morphs` / `pos` / `nouns`, `RegexpTokenizer` |
| `문서_마이닝.ipynb` | 수업 필기 원본 — 헌법 명사 추출 · `Counter` · 워드클라우드 |
| `단어사전01.ipynb` | 수업 필기 원본 — WordPiece 단어 사전 (11-03 `단어사전` 과 같은 내용, 정리는 [Day 039](../../2026-11-03/lecture/wordpiece_vocab_nsmc.ipynb)) |
| [`korean_morph_analyzers.ipynb`](./korean_morph_analyzers.ipynb) | `단어사전02` 정리 · 개선본 — 설치 · 실행 방법 → 토큰화 4가지 비교 → Okt(`norm` · `stem` · 품사표) → Mecab(세종 품사) → 틀린 문장 · 불규칙 활용 → 속도 → `RegexpTokenizer` · Kiwi |
| [`constitution_word_frequency.ipynb`](./constitution_word_frequency.ipynb) | `문서_마이닝` 정리 · 개선본 — 설치 · 실행 방법 → 헌법 불러오기 → 명사 → 한 글자 걸러내기 → `Counter` → Okt vs Mecab → 불용어 → `find` 세기 바로잡기 → 워드클라우드 |
| [`images/`](./images/) | 🎬 시뮬레이션 애니메이션(GIF) 5개 · 워드클라우드 2장 (노트북과 같은 분석기 · 데이터로 직접 만든 것) |

## 실행 방법
1. **설치** : `pip install konlpy python-mecab-ko kiwipiepy nltk wordcloud`
   - Okt(`konlpy`)는 **Java(JDK)** 가 필요하다 — Colab 은 기본 포함, Windows · Mac 은 JDK 설치 후 `JAVA_HOME` 설정
   - `python-mecab-ko` 의 미리 만든 설치 파일이 없는 환경(예 : Python 3.13)은 직접 빌드 → 리눅스 · Colab 에서 `apt-get install mecab libmecab-dev` 를 먼저
   - 워드클라우드에는 **한글 폰트**가 필요 (Colab : `apt-get install fonts-nanum`) — 노트북이 설치된 한글 폰트를 찾아 쓴다
2. **실행** : 노트북을 열고 맨 위부터 **[런타임] → [모두 실행]**. 각 노트북 0절에 Colab 용 설치 셀(주석 처리)이 있다
3. **데이터** : 헌법 전문은 KoNLPy 에 들어 있어(`kolaw.open('constitution.txt')`) 따로 받을 파일이 없다

## 결과 요약
| 실습 | 결과 |
|---|---|
| 토큰 수 (같은 문장) | `split` 7 · `word_tokenize` 9 · Okt 14 · Mecab 16 |
| 불규칙 활용 `고와야` | Okt · Mecab : `고 + 와야` (틀림) · Kiwi : `곱 + 어야` (맞음) |
| 속도 (헌법 명사 추출) | Okt 가 Mecab 보다 3.1배 · Kiwi 보다 4.0배 느림 (실행마다 조금씩 다름) |
| Okt 명사 | 3,880개 → 두 글자 이상 3,011개 · 종류 850 → 불용어 제거 826 |
| 상위 명사 | Okt : 법률 127 · 대통령 83 · 국가 73 / Mecab : 법률 121 · 대통령 84 · 국가 73 |
| 한 글자 명사 상위 | 제 175 · 정 89 · 수 88 · 관 58 · 때 55 |
| '법률' 세기 | 필기 코드 129 → 글자열 128 (`법률안` 9 포함) → 명사 Okt 127 · Mecab 121 |
