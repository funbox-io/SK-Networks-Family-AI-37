---
day: 007
date: 2026-09-14
weekday: 월
week: 3
phase: 프로그래밍과 데이터 기초
title: Streamlit — 파이썬만으로 만드는 웹 대시보드
tags: streamlit, st.title, st.write, 위젯, button, checkbox, radio, selectbox, multiselect, text_input, number_input, metric, bar_chart, sidebar, columns, tabs, expander, session_state, CRUD, form, config.toml, theme
---

# Day 007 · 2026-09-14 (월)

`프로그래밍과 데이터 기초` · 3주차

> **한 줄 요약** — HTML·CSS·JS 없이 순수 파이썬만으로 웹 화면을 그리는 Streamlit을 배우고, 텍스트·입력 위젯·차트·레이아웃을 거쳐 세션 상태로 데이터를 기억시키고 폼과 테마까지 붙여 대시보드 한 장을 완성했다.

📂 실습 코드 → [`lecture/`](./lecture/) (`basic_02.py` `basic_03.py` `basic_04.py` `.streamlit/config.toml`, 수업 필기를 주석으로 정리)

---

## 1. Streamlit 개요

복잡한 웹 개발 언어(HTML, CSS, JavaScript)나 백엔드 서버 지식 없이, **순수 파이썬만으로 웹 사이트를 만들어주는 프로그램**이다.
웹 화면 하나를 만들려면 원래 별도의 웹 개발 공부가 필요하지만, Streamlit은 파이썬 변수와 함수 몇 줄로 완성도 높은 대시보드를 만들어 준다.

| 단계 | 명령 | 어디에 |
|------|------|--------|
| 설치 | `pip install streamlit` | 터미널 |
| 임포트 | `import streamlit as st` | 코드 상단 |
| 호출 | `st.func()` | 코드 본문 |
| 실행 | `streamlit run 파일명.py` | 터미널 → 웹 브라우저가 열린다 |

⚠️ `python 파일명.py` 로 실행하면 화면이 뜨지 않는다. **반드시 `streamlit run`** 으로 띄운다.

---

## 2. 텍스트 출력 — `basic_02.py`

웹 화면에 제목, 본문, 안내 문구를 출력하는 기능이다.

| 함수 | 쓰임 |
|------|------|
| `st.title()` | 가장 큰 메인 제목 |
| `st.header()` | 대분류 주제 제목 |
| `st.subheader()` | 중분류 세부 제목 |
| `st.write()` | `print()` 대신 쓰는 **만능 출력** (문자·숫자·딕셔너리 무엇이든) |
| `st.caption()` | 작은 주석, 부연 설명 |
| `st.divider()` | 구분선(가로줄) |

```python
import streamlit as st

st.title("SK네트웍스 Family AI 캠프")
st.divider()
st.header("Python Web 대시보드 만들기")
st.write("Python write() - print() 대신 사용")
st.caption("본 시스템은 순수 파이썬 문법으로 작성되었습니다.")
```

---

## 3. 사용자 입력 위젯 — `basic_02.py`

일방적으로 정보만 보여주는 정적인 페이지가 아니라, **사용자가 누른 값에 따라 다르게 반응하는 동적인 웹 서비스**를 만들기 위해 사용한다.

| 위젯 | 반환값 |
|------|--------|
| `st.button("버튼명")` | 클릭하면 `True`, 아니면 `False` |
| `st.checkbox("문구")` | 체크 여부 `True` / `False` |
| `st.radio("제목", 리스트)` | 고른 **값** 하나 |
| `st.selectbox("제목", 리스트)` | 드롭다운에서 고른 **값** 하나 |
| `st.multiselect("제목", 리스트)` | 고른 값들의 **`list`** |
| `st.text_input("제목")` | 입력한 **문자열** (기본값 `""`) |
| `st.number_input("제목")` | 입력한 **정수/실수** (기본값 `0.0`) |

핵심은 **위젯이 값을 돌려준다**는 것이다. 버튼은 `True`/`False` 를 돌려주므로 항상 `if` 와 짝을 이룬다.

```python
if st.button("버튼: 인사하기"):
    st.write("== 반가워요. ==")
else:
    st.write("== 버튼: 대기 ==")

cont_types = ['일반 고객', 'VIP 고객', '가입 고객']
radio_value = st.radio("분석할 고객 유형:", cont_types)   # 하나만
multi_value = st.multiselect("고객 유형 다중 선택:", cont_types)  # list 로 반환
```

---

## 4. 데이터 표출 & 차트 — `basic_03.py`

파이썬 딕셔너리(dict)나 리스트(list)를 **숫자 카드 · 표 · 그래프**로 바꿔 출력하는 기능이다. 복잡한 숫자를 직관적으로 전달하기 위해 쓴다.

| 함수 | 쓰임 |
|------|------|
| `st.metric(label, value, delta)` | 매출·회원 수 같은 **핵심 지표(KPI)** 와 변화량(Delta)을 크게 강조 |
| `st.table()` | `[{"이름": "김철수", "나이": 25}, …]` 구조를 깔끔한 웹 표로 |
| `st.bar_chart()` `st.line_chart()` | **Pandas 없이** 딕셔너리만 넘겨도 즉시 막대·선 그래프 |

```python
data_value = {'1명': 120, '2명': 190, '3명': 260, '4명': 310}

st.metric(label="오늘의 총매출", value="8,000원", delta="+158")
st.bar_chart(data=data_value, color="green", horizontal=True)  # horizontal=True → 수평 막대
```

---

## 5. 레이아웃 & 컨테이너 — `basic_03.py`

입력창과 글자가 위에서 아래로만 길게 쌓이면 화면이 지저분해진다. 화면 공간을 나눠 **깔끔한 UI를 만드는 '화면 정리 정돈' 기능**이다.

| 함수 | 쓰임 |
|------|------|
| `st.sidebar` | 화면 왼쪽에 메뉴·설정창 공간 |
| `st.columns(2)` | 화면을 가로로 원하는 비율만큼 분할 |
| `st.tabs([...])` | 한 화면에서 탭을 눌러 내용 전환 |
| `st.expander()` | 접어두었다가 클릭할 때만 펼치기 |

넷 다 **`with` 구문**과 함께 쓴다. `with` 는 "여기 안쪽에 붙여라"는 **부착**의 의미다. 들여쓰기 안에 쓴 요소가 모두 그 구역으로 들어간다.

```python
with st.sidebar:                 # 사이드바에 붙는다
    st.header("메뉴판")
    menu = st.radio("이동", ['홈', '상세보기'])

col1, col2 = st.columns(2)       # 반환된 객체를 변수에 받아서
with col1:                       # 각 구역에 부착
    st.subheader("왼쪽 구역")
    with st.expander("원본 데이터"):
        st.write(data_value)

tab1, tab2, tab3 = st.tabs(['차트 보기', '데이터 보기', '정보 보기'])
with tab1:
    st.bar_chart(data=data_value, color='red', horizontal=True)
```

---

## 6. 세션 상태 `st.session_state` — `basic_04.py`

**웹 브라우저가 열려 있는 동안 파이썬 변수 값을 기억해 두는 메모리** 역할의 도구다.

- Streamlit은 버튼 하나만 눌러도 **스크립트 전체를 처음부터 끝까지 다시 실행**한다.
- 그래서 일반 변수(`a = 10`)는 매번 초기화되어 데이터가 소실된다.
- 새로고침이 일어나도 값이 유지되게 하려면 **반드시 `st.session_state` 에 저장**해야 한다.

사용법은 파이썬 **딕셔너리(dict)와 동일**하다. 다만 없는 키를 부르면 에러가 나므로, `if 'key' not in st.session_state:` 로 **존재 여부를 먼저 검사하는 것이 필수 규칙**이다.

```python
# 1. 세션 상태 안전 초기화 (처음 들어왔을 때 1번만)
if 'count' not in st.session_state:
    st.session_state['count'] = 0

# 2. 버튼을 누르면 세션 상태 내부 값을 1 증가
if st.button("숫자 1 증가"):
    st.session_state['count'] += 1

# 3. 화면이 재실행되어도 유지되는 값 출력
st.write(f"현재 누적 카운트: **{st.session_state['count']}**")
```

---

## 7. 데이터 CRUD — `basic_04.py`

Streamlit은 **데이터가 변하는 흐름을 화면에 실시간으로 동기화**해 준다. 복잡한 화면 구현 코드를 짜지 않아도 Create·Update·Delete 결과가 알아서 화면에 반영된다.
파이썬 기본 자료형(list, dict)만으로 구현한다 — 입력 위젯에서 받은 값을 `dict` 로 묶어 세션 리스트에 `.append()` 하고, 그 리스트를 출력하면 그대로 조회가 된다.

```python
if "customer_list" not in st.session_state:
    st.session_state["customer_list"] = []

# C (Create)
new_name = st.text_input("고객 이름:")
if st.button("고객 추가"):
    if new_name == "":
        st.warning("고객 이름을 입력해 주세요.")     # 빈 값 방어
    else:
        st.session_state["customer_list"].append({"name": new_name})
        st.success(f"{new_name} 고객이 등록되었습니다.")

# R (Read)
st.write("현재 등록된 고객 리스트:", st.session_state["customer_list"])
```

| 피드백 함수 | 색 |
|------|-----|
| `st.success()` | 초록 — 성공 |
| `st.warning()` | 노랑 — 경고 |
| `st.error()` | 빨강 — 오류 |

---

## 8. 입력 폼 `st.form` — `basic_04.py`

여러 입력 위젯을 하나로 묶어, **오직 [제출] 버튼을 누르는 순간에만** 데이터가 전송되고 화면이 새로고침되게 하는 기능이다.
입력창이 5개면 글자를 칠 때마다 화면이 5번 새로고침되며 연산이 반복되는데, `st.form` 이 이를 차단해 **앱이 버벅거리는 현상을 막아준다**.

```python
with st.form(key="user_info_form"):
    name = st.text_input("Name:")
    user_age = st.text_input("Age:")
    submitted = st.form_submit_button("제출")   # 폼 전용 제출 버튼

if submitted:                                   # 제출을 눌렀을 때만 실행
    try:
        user_age = int(user_age)
        st.success(f"성공! {name} 님의 나이 {user_age}세가 확인되었습니다.")
    except ValueError:
        st.error("경고! 나이는 숫자로 입력해 주세요.")
```

- 폼 안에서는 `st.button()` 이 아니라 **`st.form_submit_button()`** 을 써야 한다.
- 값 검증은 `try ~ except ValueError` 로 — Day 005에서 배운 예외 처리가 그대로 쓰인다.

---

## 9. 환경(색상·폰트) 설정 — `.streamlit/config.toml`

웹 앱의 글꼴·배경색·강조 색상 등 **전체 디자인 테마를 한곳에서 관리하는 설정 파일**이다.
파이썬 코드를 일일이 고치지 않고 **설정 파일 하나만 수정해 사이트 전체에 브랜드 색상을 일괄 적용**할 수 있다.

**저장 위치 (중요 규칙)** — 실습 폴더 최상단에 `.streamlit` 폴더를 만들고 그 안에 `config.toml` 로 두어야 Streamlit이 자동으로 인식한다.

```text
my_dashboard/
├── .streamlit/
│   └── config.toml   <-- 테마 설정 파일
└── app.py            <-- 테마 확인용 파이썬 코드
```

| 항목 | 지정하는 것 |
|------|------|
| `primaryColor` | 버튼·선택된 탭·슬라이더 등 포인트 색상 |
| `backgroundColor` | 메인 화면 기본 배경색 |
| `secondaryBackgroundColor` | 사이드바·입력 상자 보조 배경색 |
| `textColor` | 기본 글자 색상 |
| `font` | 글꼴 (`sans serif` / `serif` / `monospace`) |

```toml
[theme]
primaryColor = "#2563EB"              # 인디고 블루
backgroundColor = "#F8FAFC"           # 소프트 오프화이트
secondaryBackgroundColor = "#EFF6FF"  # 연한 블루 톤 사이드바
textColor = "#1E293B"                 # 딥 차콜
font = "sans serif"
```

실무 권장 테마 2가지 — **타입 A 모던 화이트(Modern Light Pro)** 는 기업용 깔끔한 스타일, **타입 B 프리미엄 다크(Premium Dark)** 는 그래프가 돋보여 데이터 분석가가 선호하는 스타일이다. (타입 B 값은 `config.toml` 하단에 주석으로 남겨 뒀다)

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `if bin:` → **`if submitted:`** — `bin` 은 파이썬 **내장 함수**라 항상 참. 제출을 안 눌러도 에러 메시지가 떴다
- [x] 폼 제출 변수명 `btn` → `submitted` (무엇을 담은 값인지 이름으로 드러나게)
- [x] 고객 추가 실패 시 `del new_name` → **`st.warning()`** 안내로 교체. 변수를 지우면 다음 실행에서 `NameError` 위험
- [x] `basic_03.py` 에서 `data_value` 를 **4번 중복 정의**하던 것 → 상단 한 곳으로 통합
- [x] 의미 없이 남아 있던 `None` 한 줄 삭제, 탭 사이에 끼어 있던 `st.divider()` 위치 정리
- [x] 변수명 `Tval` `fx` `selct` `muit` → `is_checked` `radio_value` `select_value` `multi_value`
- [x] 오타 — `라이브 러이` → 라이브러리, `SK네트윅스` → **SK네트웍스**, `곡객` → 고객, `헌재` → 현재, `시독성` → 시인성
- [x] `st.number_input` 반환값이 **`0.0`(실수)** 이라 `if int_data:` 는 0일 때 걸러진다는 점 확인

**막혔던 부분 / 질문**
- [ ] `st.session_state` 에 넣지 않은 일반 변수는 정확히 언제 초기화되는지 (재실행 단위)
- [ ] 위젯의 `key` 인자는 언제 꼭 필요한지 (같은 위젯을 두 번 그릴 때 발생하는 중복 ID 에러)
- [ ] `st.form` 안에서는 `st.button()` 이 왜 막혀 있는지
- [ ] `st.bar_chart` 에 딕셔너리 말고 **Pandas DataFrame** 을 넘기면 무엇이 달라지는지
- [ ] 세션 상태는 브라우저 탭을 닫으면 사라지는데, 진짜 저장은 파일/DB로 어떻게 잇는지 (CRUD 의 U·D 구현)
- [ ] `config.toml` 을 고쳤는데 반영이 안 될 때 — 서버 재시작이 필요한 항목이 따로 있는지

**직접 해본 것**
- [x] 수업 실습 파일 3개 + 테마 설정 파일을 주석 정리해 `lecture/` 에 업로드
- [ ] 위젯 → 세션 상태 → 차트를 한 파일로 묶어 **나만의 미니 대시보드** 만들어 보기

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [API 레퍼런스 — 전체 함수 목록](https://docs.streamlit.io/develop/api-reference)
- [세션 상태(st.session_state) 가이드](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [입력 폼(st.form) 가이드](https://docs.streamlit.io/develop/concepts/architecture/forms)
- [테마 설정(config.toml)](https://docs.streamlit.io/develop/concepts/configuration/theming)
