"""대한민국 명절 교통사고 데이터 — 설날 vs 추석, 어떤 연휴가 더 위험할까?

실행 (이 폴더 안에서):
    pip install -r requirements.txt
    streamlit run app.py

데이터: MySQL holiday_db (db/holiday_db.sql로 생성) · 접속 정보는 db_config.py (평문)
        연결이 안 되면 data/ 폴더의 CSV로 대신 표시하고 사이드바에 알려 줍니다.
구성
    app.py         페이지 뼈대 (사이트 제목 · 사이드바 메뉴/지표/일평균 · 탭)
    data_source.py MySQL → 표 (실패 시 CSV)
    sections.py    화면 카드들 · theme.py 디자인 · analysis.py 계산 · faq.py 보험 FAQ
"""
from __future__ import annotations

import streamlit as st

import data_source
import db_config
import sections
import theme as T
from analysis import sgg_list, sido_list
from faq import render_faq

st.set_page_config(page_title="대한민국 명절 교통사고 데이터", layout="wide")
st.markdown(T.CSS, unsafe_allow_html=True)


@st.cache_data(ttl=600, show_spinner="데이터를 불러오는 중…")
def get_bundle(cfg: dict | None) -> data_source.Bundle:
    return data_source.load(cfg)


def mysql_config() -> dict:
    """접속 정보는 db_config.py에서 읽습니다 (secrets.toml 불필요)."""
    return dict(db_config.MYSQL)


data = get_bundle(mysql_config())
df = data.df
YEARS = sorted(int(y) for y in df["연도"].unique())
ctx = {
    "df": df,
    "geo": data.geo,
    "hotspots": data.hotspots,
    "YEARS": YEARS,
    "PERIOD": f"{YEARS[0]}~{YEARS[-1]}",
    "sido_list": sido_list(df),
    "sgg_list": lambda s: sgg_list(df, s),
}

# ---------------------------------------------------------------- 사이트 제목
sections.site_header(st, T)

# ---------------------------------------------------------------- 사이드바 1) 메뉴 (버튼 형식)
PAGES = ["명절 교통사고 대시보드", "보험 FAQ"]
st.session_state.setdefault("page", PAGES[0])


def _go(p: str) -> None:
    st.session_state["page"] = p


with st.sidebar:
    st.markdown("<div class='menu-h'>메뉴</div>", unsafe_allow_html=True)
    for i, p in enumerate(PAGES):
        st.button(p, key=f"menu_{i}", type="primary" if st.session_state["page"] == p else "secondary",
                  use_container_width=True, on_click=_go, args=(p,))
page = st.session_state["page"]


def data_note() -> None:
    with st.sidebar:
        if data.source == "mysql":
            st.markdown("<div class='src-note'>데이터: MySQL holiday_db</div>", unsafe_allow_html=True)
        else:
            st.warning(data.note, icon="⚠️")


if page == "보험 FAQ":
    data_note()
    render_faq(st, css=T.FAQ_CSS, muted=T.MUTED, data=data.faq)
    st.stop()

# ---------------------------------------------------------------- 사이드바 2) 지표 · 3) 일평균 보정
ctx.update(sections.filters_sidebar(st, T, ctx))
data_note()

# ---------------------------------------------------------------- 본문
tab_o, tab_d, tab_h = st.tabs(["전체 비교", "연도 상세", "사고다발지점"])
with tab_o:
    sections.overview(st, T, ctx)     # 5년 합계만
with tab_d:
    sections.detail(st, T, ctx)       # 연도 선택은 이 탭 안에
with tab_h:
    sections.hotspots(st, T, ctx)     # 시도 · 시군구 선택은 이 탭 안에

st.caption(sections.md("출처: 도로교통공단, 설날·추석 연휴기간 사고통계(2021~2025), 연휴기간 사고다발지역(2021~2025). "
                       "※ 인용 표기는 팀 DataFact 데이터 인용 가이드 형식에 맞춰 수정하세요."))
