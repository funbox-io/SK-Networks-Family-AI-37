"""보험 FAQ — data/faq/insurance_faq.csv 내용만으로 만든 화면.

CSV 컬럼: 항목, 질문, 답변 (답변 끝에 '(출처 : 보험사)')
화면: 제목 → 항목 버튼(전체 + CSV의 항목) → 질문 목록(누르면 답변과 출처가 펼쳐짐) → 페이지 넘김
데이터 확인:  python faq.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import pandas as pd

FAQ_FILE = Path(__file__).parent / "data" / "faq" / "insurance_faq.csv"
ALL = "전체"
PAGE_SIZE = 15
SOURCE_RE = r"\s*\(출처\s*:\s*([^)]+)\)\s*\"?\s*$"


# ---------------------------------------------------------------- 데이터
def load_faq(path: Path | str = FAQ_FILE) -> pd.DataFrame:
    """CSV를 그대로 읽고, 답변 끝의 '(출처 : …)'만 따로 떼어 '출처' 컬럼으로 둡니다."""
    d = pd.read_csv(path, encoding="utf-8-sig")[["항목", "질문", "답변"]].fillna("")
    d["출처"] = d["답변"].str.extract(SOURCE_RE)[0].fillna("").str.strip()
    body = d["답변"].str.replace(SOURCE_RE, "", regex=True).str.strip().str.strip('"').str.strip()
    d["답변"] = body.map(lambda s: html.unescape(s.replace("& #", "&#")))   # '& #39;' 같은 깨진 문자만 복원
    d["항목"] = d["항목"].str.strip()
    d["질문"] = d["질문"].str.strip()
    return d


def categories(faq: pd.DataFrame) -> list[str]:
    """CSV의 항목 (질문이 많은 순)."""
    return faq["항목"].value_counts().index.tolist()


def md_escape(text: str) -> str:
    """펼침 목록 제목처럼 마크다운으로 그려지는 곳의 특수문자 이스케이프."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!|~$>])", r"\\\1", text)


# ---------------------------------------------------------------- 화면
CSS = """
<style>
.faq-hero {border-radius:22px;padding:28px 32px;margin:4px 0 20px;background:#F6F8FC;border:1px solid #DDE3EC}
.faq-hero h1 {margin:0;padding:0;font-size:32px;line-height:1.3;color:#0F172A}
.faq-hero p {margin:8px 0 0;font-size:14.5px;color:#374151}
.faq-sec {font-size:17px;font-weight:700;color:#0F172A;margin:20px 0 10px}
.faq-sec small {font-size:13px;font-weight:400;color:#5B6472;margin-left:6px}
.faq-a {font-size:15.5px;line-height:1.9;color:#0F172A;word-break:keep-all}
.faq-src {display:inline-block;margin-top:12px;font-size:12.5px;color:#1D5FB8;background:#EAF3FF;border-radius:999px;padding:3px 10px}
</style>
"""


def render_faq(st, css: str | None = None, muted: str = "#5B6472", data: pd.DataFrame | None = None) -> None:
    """보험 FAQ 화면. app.py에서 render_faq(st, css=테마의 FAQ_CSS, data=DB에서 읽은 FAQ 표)로 부릅니다.
    data를 주지 않으면 CSV(data/faq/insurance_faq.csv)를 읽습니다."""
    faq = data if data is not None else _load_cached(st)
    ss = st.session_state
    ss.setdefault("faq_category", ALL)
    ss.setdefault("faq_page", 1)

    def pick(v):
        ss.faq_category, ss.faq_page = v, 1

    st.markdown(css or CSS, unsafe_allow_html=True)
    st.markdown(
        "<div class='faq-hero'><h1>보험 FAQ</h1>"
        f"<p>자동차·운전자 보험 자주 묻는 질문 {len(faq):,}개 · 항목을 누르면 해당 질문만 모아 봅니다.</p></div>",
        unsafe_allow_html=True,
    )

    # --- 항목 버튼 (CSV의 '항목' 컬럼)
    cats = categories(faq)
    counts = {ALL: len(faq), **faq["항목"].value_counts().to_dict()}
    st.markdown(f"<div class='faq-sec'>항목<small>{len(cats)}개</small></div>", unsafe_allow_html=True)
    labels = [ALL, *cats]
    per_row = 5
    for start in range(0, len(labels), per_row):
        cols = st.columns(per_row)
        for col, lab in zip(cols, labels[start:start + per_row]):
            col.button(f"{lab} · {counts.get(lab, 0)}", key=f"faq_cat_{lab}",
                       type="primary" if lab == ss.faq_category else "secondary",
                       use_container_width=True, on_click=pick, args=(lab,))

    # --- 질문 목록
    rows = faq if ss.faq_category == ALL else faq[faq["항목"] == ss.faq_category]
    st.markdown(f"<div class='faq-sec'>{html.escape(ss.faq_category)} 질문<small>{len(rows):,}개</small></div>",
                unsafe_allow_html=True)
    pages = max((len(rows) - 1) // PAGE_SIZE + 1, 1)
    ss.faq_page = min(max(ss.faq_page, 1), pages)
    view = rows.iloc[(ss.faq_page - 1) * PAGE_SIZE: ss.faq_page * PAGE_SIZE]
    for _, r in view.iterrows():
        label = f"[{r['항목']}] {r['질문']}" if ss.faq_category == ALL else r["질문"]
        with st.expander(md_escape(label)):
            src = f"<div class='faq-src'>출처 · {html.escape(r['출처'])}</div>" if r["출처"] else ""
            st.markdown(f"<div class='faq-a'>{html.escape(r['답변'])}</div>{src}", unsafe_allow_html=True)

    if pages > 1:
        c1, c2, c3 = st.columns([1, 2, 1])

        def go(step):
            ss.faq_page += step

        c1.button("◀ 이전", disabled=ss.faq_page <= 1, on_click=go, args=(-1,), use_container_width=True, key="faq_prev")
        c2.markdown(f"<div style='text-align:center;padding-top:8px;color:{muted}'>{ss.faq_page} / {pages} 페이지</div>",
                    unsafe_allow_html=True)
        c3.button("다음 ▶", disabled=ss.faq_page >= pages, on_click=go, args=(1,), use_container_width=True, key="faq_next")


def _load_cached(st) -> pd.DataFrame:
    @st.cache_data
    def _load() -> pd.DataFrame:
        return load_faq()

    return _load()


if __name__ == "__main__":
    faq = load_faq()
    print(faq.shape)
    print(faq["항목"].value_counts())
    print(faq["출처"].value_counts())
    print(faq.iloc[0].to_dict())
