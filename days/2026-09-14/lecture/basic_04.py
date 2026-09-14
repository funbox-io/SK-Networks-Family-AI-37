"""
basic_04.py
교재 p.133~139 : streamlit 기능
  - 세션 상태(st.session_state)를 이용한 메모리
  - 데이터 CRUD
  - 버벅임 없는 데이터 전송, 입력 폼(st.form)

실행 방법 : 터미널에서  streamlit run basic_04.py
"""

# 라이브러리 임포트
import streamlit as st


# =====================================================================
# 1. 세션 상태(st.session_state) (교재 p.133~134)
#    - Streamlit은 버튼 하나만 눌러도 스크립트 전체를 처음부터 다시 실행한다.
#    - 일반 변수는 그때마다 초기화되어 값이 사라지므로,
#      유지해야 하는 값은 반드시 st.session_state 에 저장한다.
#    - 사용법은 파이썬 딕셔너리(dict)와 동일하다.
#    - 없는 키를 부르면 에러가 나므로 'key' not in st.session_state 로
#      존재 여부를 먼저 검사하는 것이 필수 규칙이다.
# =====================================================================

# 세션 상태 안전 초기화 (처음 웹에 들어왔을 때 1번만 실행)
if 'count' not in st.session_state:
    st.session_state['count'] = 0  # 초기값 0 세팅

# 버튼을 누르면 세션 상태 내부의 값을 1 증가
# (st.button() 은 True/False 를 반환하므로 if 조건문과 함께 사용)
if st.button("숫자 1 증가"):
    st.session_state['count'] += 1

# 화면이 재실행되어도 유지되는 값 출력
st.write(f"현재 누적 카운트: **{st.session_state['count']}**")

st.divider()


# =====================================================================
# 2. 데이터 CRUD (교재 p.136~137)
#    파이썬 기본 자료형(list, dict)을 활용해 데이터를 추가/조회한다.
#    데이터가 바뀌면 Streamlit이 화면을 자동으로 동기화해 준다.
# =====================================================================

# 세션 상태에 고객 리스트 초기화
if "customer_list" not in st.session_state:
    st.session_state["customer_list"] = []

# --- C (Create) : 데이터 추가 ---
new_name = st.text_input("고객 이름:")

if st.button("고객 추가"):
    if new_name == "":
        # 입력값이 비어 있으면 경고만 출력하고 추가하지 않는다.
        st.warning("고객 이름을 입력해 주세요.")
    else:
        # 입력받은 값을 dict 로 묶어 세션 리스트에 append
        st.session_state["customer_list"].append({"name": new_name})
        # 등록 성공 메시지(초록색)
        st.success(f"{new_name} 고객이 등록되었습니다.")

# --- R (Read) : 데이터 조회 ---
st.write("현재 등록된 고객 리스트:", st.session_state["customer_list"])

st.divider()


# =====================================================================
# 3. 입력 폼 (st.form) (교재 p.138)
#    - 여러 입력 위젯을 하나로 묶어, [제출] 버튼을 누르는 순간에만
#      데이터가 전송되고 화면이 새로고침되도록 제어한다.
#    - 입력창을 칠 때마다 화면이 새로고침되어 버벅이는 현상을 막아준다.
# =====================================================================

with st.form(key="user_info_form"):
    name = st.text_input("Name:")
    user_age = st.text_input("Age:")

    # st.form_submit_button() : 폼 내부 데이터를 한 번에 전송하는 전용 제출 버튼
    submitted = st.form_submit_button("제출")

# 제출 버튼이 눌렸을 때만 실행
if submitted:
    try:
        # 문자열로 받은 나이를 정수로 변환 (숫자가 아니면 ValueError 발생)
        user_age = int(user_age)
        st.success(f"성공! {name} 님의 나이 {user_age}세가 확인되었습니다.")
    except ValueError:
        # 변환 실패 시 빨간색 에러 메시지 출력
        st.error("경고! 나이는 숫자로 입력해 주세요.")
