# [07] 실습 환경 설정 — conda 가상환경 + PyMySQL + Streamlit

교재 : p.131 ~ p.133
선행 : Anaconda(또는 miniconda3) · Visual Studio Code 설치, MySQL 서버 실행 중

> 이 파일은 SQL 이 아니라 **터미널 명령**이므로 Anaconda Prompt 에서 한 줄씩 실행한다.

---

## 1. 가상환경 만들기 (p.131 ~ p.132)

| 순서 | 할 일 | 명령 / 조작 |
|------|-------|-------------|
| 1 | Anaconda Prompt 실행 | 윈도우 시작(또는 찾기) → `anaconda` 입력 → **Anaconda Prompt** |
| 2 | 가상환경 생성 | `conda create -n db python=3.12` → `Proceed ([y]/n)?` 에 `y` |
| 3 | 가상환경 활성화 | `conda activate db` → 프롬프트 앞이 `(base)` 에서 **`(db)`** 로 바뀐다 |
| 4 | 라이브러리 설치 | `pip install PyMySQL streamlit` |
| 5 | 작업 폴더 생성 | miniconda3 설치 폴더 → 새 폴더 **`work1`** |
| 6 | VS Code 에서 폴더 열기 | File → Open Folder → `work1` |
| 7 | 인터프리터 지정 | `Ctrl + Shift + P` → **Python: Select Interpreter** → `db` 선택 |

```bash
conda create -n db python=3.12
conda activate db
pip install PyMySQL streamlit
```

⚠️ 4번을 `(base)` 상태에서 실행하면 base 환경에 설치된다. **반드시 `(db)` 가 붙은 뒤에** `pip install` 한다.

---

## 2. Python 에서 DB 를 연동하는 이유 (p.133)

데이터베이스에 저장된 데이터를 파이썬으로 가져와 **가공 · 분석**하고, 이를 **웹 화면(Streamlit)에 시각적으로 구현**하기 위함.

| 라이브러리 | 역할 |
|------------|------|
| **PyMySQL** | 파이썬과 MySQL 데이터베이스 사이의 **통신**을 담당 |
| **Streamlit** | 조회한 데이터를 **웹 대시보드**로 출력 (Day 007) |

---

## 3. 설치 확인

```bash
python -c "import pymysql, streamlit; print(pymysql.__version__, streamlit.__version__)"
```

버전 두 개가 에러 없이 출력되면 준비 완료. 이어서 `08_pymysql_study.py` 를 실행한다.

```bash
python 08_pymysql_study.py          # 콘솔 출력
streamlit run 09_app.py             # 웹 대시보드
streamlit run 10_app_search.py      # 위젯 연동 검색
```
