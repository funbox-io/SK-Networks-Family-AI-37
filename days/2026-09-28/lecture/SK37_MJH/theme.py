"""버전 B4 — 「명절의 밤」 디자인 · 전체 흰색 (가독성 개선)

배치 · 달 모티프 · 세리프 제목은 그대로 두고 모든 면을 흰색 계열로 바꾼 버전.
    설날 = 하늘색 #3B8BEB (글자는 #1D5FB8), 추석 = 호박색 #D4801A (글자는 #9A5B00)
    흰 바탕에서 호박색 글자는 흐려 보여서, 막대·점 같은 면에는 밝은 색을, 글자에는 진한 색을 씁니다.
    제목 Noto Serif KR · 본문 Pretendard · 숫자 Space Grotesk
색을 바꾸려면 아래 상수만 고치면 됩니다.
"""
from __future__ import annotations

import html

NAME = "day"
BASE = "light"

# ---------------------------------------------------------------- 색 (모두 흰 바탕 기준, 글자 대비 4.5:1 이상)
BG, SURFACE, SURFACE2 = "#FFFFFF", "#FFFFFF", "#FAFBFD"
INK, INK2, MUTED = "#0F172A", "#374151", "#5B6472"
INK_ON_LIGHT = "#0F172A"
LINE, LINE2, WASH = "#DDE3EC", "#EDF0F5", "#F1F4F9"
S, C = "#3B8BEB", "#D4801A"                      # 막대 · 점 · 선 (흰 바탕 도형 대비 3:1 이상)
S_BG, C_BG, S_INK, C_INK = "#EAF3FF", "#FFF3DC", "#1D5FB8", "#9A5B00"   # 옅은 바탕 · 글자
S_SOFT = "#DCEBFF"          # 값이 0인 사고다발지 점
SEL_FILL = "#DCE8FA"        # 지도에서 선택한 시도
UP = "#D93B3B"              # 전년 대비 증가
COLORS = {"설날": S, "추석": C}
TINTS = {"설날": (S_BG, S_INK), "추석": (C_BG, C_INK)}

SANS = "Pretendard, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
SERIF = "'Noto Serif KR', 'Nanum Myeongjo', serif"
NUM = "'Space Grotesk', Pretendard, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, Menlo, monospace"
FONT = SANS
SHADOW = "0 1px 2px rgba(15,23,42,.04), 0 8px 24px rgba(15,23,42,.06)"
MOON = "radial-gradient(circle at 38% 38%,#FFE9B8 0%,#FFD27A 45%,#F2A12B 100%)"

CSS = f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap');
:root {{--bg:{BG};--surface:{SURFACE};--surface2:{SURFACE2};--ink:{INK};--ink2:{INK2};--muted:{MUTED};--line:{LINE};--line2:{LINE2};
  --wash:{WASH};--s:{S};--c:{C};--sBg:{S_BG};--cBg:{C_BG};--sInk:{S_INK};--cInk:{C_INK};--up:{UP}}}
.stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp li, .stApp button, .stApp input, .stApp table, .stApp td, .stApp th,
section[data-testid="stSidebar"] * {{font-family:{SANS}}}
.stApp [data-testid="stIconMaterial"] {{font-family:'Material Symbols Rounded' !important}}
.stApp .mono {{font-family:{MONO} !important;font-size:.92em}}
.stApp {{background:var(--bg);color:var(--ink);font-size:15px}}
[data-testid="stMainBlockContainer"], .block-container {{max-width:1380px;padding-top:2rem;padding-bottom:5rem}}
[data-testid="stHeader"] {{background:transparent}}
section[data-testid="stSidebar"] {{background:{SURFACE2};border-right:1px solid var(--line)}}

/* 히어로 */
.hero {{position:relative;overflow:hidden;border-radius:26px;padding:34px 38px 30px;margin-bottom:6px;
  background:linear-gradient(135deg,#EEF5FF 0%,#F8FAFF 55%,#FFF6E6 100%);border:1px solid var(--line)}}
.hero .moon {{position:absolute;right:48px;top:-40px;width:210px;height:210px;border-radius:50%;background:{MOON};
  box-shadow:0 0 70px 10px rgba(242,161,43,.22);opacity:.85}}
.hero .snow {{display:none}}
.hero .kicker {{font-family:{MONO};font-size:12.5px;letter-spacing:.16em;color:var(--sInk)}}
.hero h1 {{font-family:{SERIF} !important;font-weight:900;font-size:clamp(34px,4.2vw,56px);letter-spacing:-.02em;margin:10px 0 6px;padding:0;line-height:1.12;color:var(--ink)}}
.hero h1 .s {{color:var(--sInk)}} .hero h1 .c {{color:var(--cInk)}} .hero h1 .vs {{font-size:.55em;color:var(--muted);margin:0 .25em;vertical-align:.25em}}
.hero .sub {{color:var(--ink2);font-size:15.5px;max-width:52ch;line-height:1.6}}
.hero .chips {{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}}
.hero .chip {{background:#FFFFFF;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:13.5px;color:var(--ink2)}}
.hero .chip b {{font-family:{NUM};color:var(--ink);font-weight:600}}
.hero .chip.win {{background:var(--cBg);border-color:transparent;color:var(--cInk)}}
.hero .chip.win.S {{background:var(--sBg);color:var(--sInk)}}
.dtitle h2 {{font-family:{SERIF} !important;font-size:clamp(24px,2.6vw,34px);font-weight:900;margin:4px 0 0;padding:0;color:var(--ink)}}

/* 카드 */
div[class*="st-key-card-"] {{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:22px 24px;gap:.6rem;box-shadow:{SHADOW}}}
div[class*="st-key-card-filters"] {{padding:12px 18px;border-radius:999px}}
.ch {{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:8px}}
.ch h2 {{font-size:17px;font-weight:700;letter-spacing:-.01em;margin:0;padding:0;display:flex;align-items:center;gap:10px;color:var(--ink)}}
.ch h2 small {{font-size:13.5px;color:var(--muted);font-weight:400}}
.meta {{color:var(--muted);font-size:13px;line-height:1.6}}
.asof {{color:var(--muted);font-size:12px;line-height:1.4;text-align:right;font-family:{MONO}}}
.flag {{background:var(--cBg);color:var(--cInk);border-radius:999px;padding:4px 11px;font-size:12.5px;font-weight:500}}
.sw {{width:11px;height:11px;border-radius:50%;display:inline-block;flex:none}}
.foot {{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}}
.legend {{display:flex;gap:20px;align-items:center;flex-wrap:wrap;font-size:14px;color:var(--ink2)}}
.legend span {{display:inline-flex;align-items:center;gap:8px}}
[data-testid="stCaptionContainer"] {{color:var(--muted)}}

/* 위젯 */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{background:#EEF2F7;border-radius:999px;padding:4px;gap:2px;width:fit-content}}
[data-testid="stTabs"] [data-baseweb="tab"] {{border-radius:999px;padding:7px 20px;height:auto;color:var(--ink2);background:transparent;font-weight:500}}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {{background:var(--ink);color:#FFFFFF}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] {{display:none}}
[data-testid="stButtonGroup"] [data-baseweb="button-group"] {{background:#EEF2F7;border-radius:999px;padding:3px;gap:2px;width:fit-content;flex-wrap:wrap}}
button[data-testid^="stBaseButton-segmented_control"] {{border:0 !important;border-radius:999px !important;background:transparent;color:var(--ink2);
  margin:0 !important;padding:5px 13px;min-height:0;font-weight:500}}
button[data-testid="stBaseButton-segmented_controlActive"] {{background:var(--c) !important;color:#1A1204 !important;font-weight:700}}
[data-testid="stWidgetLabel"] p {{font-size:13px;color:var(--ink2);font-weight:500}}
.stButton button, .stDownloadButton button {{border-radius:999px;font-size:13.5px}}
.stButton button[data-testid="stBaseButton-primary"] {{background:var(--c);border:1px solid var(--c);color:#1A1204;font-weight:700}}
.stButton button[data-testid="stBaseButton-secondary"] {{background:#FFFFFF;border:1px solid var(--line);color:var(--ink2)}}
.stButton button[data-testid="stBaseButton-secondary"]:hover {{border-color:var(--c);color:var(--ink)}}
/* 사이드바 메뉴 버튼 */
.menu-h {{font-size:13px;color:var(--muted);font-weight:600;margin:4px 0 2px}}
section[data-testid="stSidebar"] .stButton button {{border-radius:12px;min-height:44px;font-size:15px;justify-content:flex-start;padding-left:16px}}
[data-testid="stExpander"] details {{border:1px solid var(--line) !important;background:#FFFFFF;border-radius:14px}}

/* KPI · VS */
.kpi-wrap {{container-type:inline-size}}
.kpis {{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}}
@container (max-width:470px) {{.kpis {{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.kpi {{border-radius:16px;background:#F6F8FC;border:1px solid var(--line2);padding:14px 14px 12px;min-width:0}}
.kpi .l {{font-size:13px;color:var(--ink2);font-weight:500}}
.kpi .v {{font-family:{NUM} !important;font-weight:600;letter-spacing:-.02em;white-space:nowrap;font-size:clamp(21px,1.9vw,30px);margin:8px 0 6px;line-height:1.1;color:var(--ink)}}
.kpi .v small {{font-family:{SANS};font-size:12.5px;color:var(--muted);font-weight:400;margin-left:3px}}
.kpi .d {{font-size:12.5px;color:var(--muted);line-height:1.45}}
.kpi.hl {{border-color:transparent}}
.up {{color:var(--up);font-weight:600}}
.vs-center {{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px;min-height:180px}}
.vsdot {{width:74px;height:74px;border-radius:50%;display:grid;place-items:center;font-family:{SERIF} !important;font-weight:900;font-size:24px;color:#FFFFFF;
  background:conic-gradient(from 200deg,var(--s),var(--c),var(--s));box-shadow:0 8px 24px rgba(59,139,235,.25);text-shadow:0 1px 2px rgba(0,0,0,.25)}}
.verdict {{border-radius:999px;padding:8px 16px;font-weight:700;font-size:17px;font-family:{NUM};background:var(--wash)}}

/* 치사율 */
.rate {{display:flex;flex-direction:column;gap:22px;margin-top:6px}}
.rate .row {{display:flex;justify-content:space-between;font-size:15px;margin-bottom:8px;color:var(--ink2)}}
.rate .row b {{font-family:{NUM};font-size:22px;color:var(--ink);font-weight:600}}
.track {{height:10px;border-radius:999px;background:var(--wash);overflow:hidden}}
.fill {{height:100%;border-radius:999px}}
.rsub {{font-size:12.5px;color:var(--muted);margin-top:6px}}
.note {{border-top:1px solid var(--line2);margin-top:20px;padding-top:14px;color:var(--ink2);font-size:14px;line-height:1.75}}
.note b {{color:var(--ink)}}

/* 타일 지도 */
.tiles {{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;width:100%;max-width:460px;margin:6px auto 0}}
.tile {{aspect-ratio:1.35;border-radius:12px;display:flex;flex-direction:column;justify-content:center;align-items:center;
  font-size:13.5px;font-weight:600;line-height:1.25;border:1px solid var(--line2)}}
.tile small {{font-family:{NUM};font-weight:500;font-size:12px;opacity:.9}}
.tile.sel {{outline:2px solid var(--ink);outline-offset:2px}}
.ramp {{display:flex;align-items:center;gap:10px;justify-content:center;margin-top:18px;font-size:12.5px;color:var(--ink2)}}
.ramp i {{display:block;width:140px;height:8px;border-radius:999px}}

/* 표 */
.tw {{overflow-x:auto}}
table.tbl {{border-collapse:collapse;width:100%;font-size:14.5px}}
table.tbl th {{text-align:left;font-weight:600;color:var(--muted);font-size:12.5px;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}}
table.tbl td {{padding:11px 12px;border-bottom:1px solid var(--line2);white-space:nowrap;color:var(--ink)}}
table.tbl .r {{text-align:right;font-family:{NUM}}}
table.tbl td.rk {{color:var(--muted);width:44px;font-family:{NUM}}}
table.tbl td.dim {{color:var(--ink2)}}
table.tbl tr.tot td {{font-weight:700;border-bottom:0}}
table.tbl tr.sel td {{background:var(--sBg)}}
table.tbl tbody tr:hover td {{background:#F8FAFD}}

/* 사고다발지 Top · 메모 */
.hs ol {{list-style:none;margin:0;padding:0}}
.hs li {{display:grid;grid-template-columns:26px 1fr auto;gap:10px;padding:11px 0;border-bottom:1px solid var(--line2);font-size:14px;align-items:start;color:var(--ink)}}
.hs .k {{width:26px;height:26px;border-radius:50%;background:var(--sBg);color:var(--sInk);display:grid;place-items:center;font-size:12.5px;font-family:{NUM};font-weight:700}}
.hs li:first-child .k {{background:var(--c);color:#1A1204}}
.hs small {{color:var(--muted);display:block;font-size:12.5px;margin-top:2px}}
.hs b {{font-family:{NUM};font-weight:700;color:var(--ink)}}
.src {{color:var(--ink2);font-size:14px;line-height:1.75}}
.src p {{margin:0 0 10px}} .src b {{color:var(--ink)}}

/* 인사이트 */
.tag {{font-family:{MONO};font-size:12px;color:var(--cInk);letter-spacing:.12em;font-weight:500}}
.ins-t {{font-family:{SERIF} !important;font-size:19px;font-weight:700;margin:10px 0 8px;color:var(--ink)}}
.ins-b {{font-size:14.5px;color:var(--ink2);line-height:1.8}}

/* 연도 상세 · 요약 */
.heat {{display:grid;gap:4px;font-size:12.5px}}
.heat .c {{border-radius:8px;height:30px;display:grid;place-items:center;font-size:12.5px;font-family:{NUM};font-weight:600}}
.heat .hl {{color:var(--muted);text-align:center;padding-bottom:4px;font-family:{MONO}}}
.heat .rl {{color:var(--ink2);font-size:13.5px;display:flex;align-items:center}}
.cmp {{display:flex;flex-direction:column;gap:22px}}
.crow {{display:grid;grid-template-columns:150px 1fr;gap:16px;align-items:center}}
.crow .lab {{font-size:14.5px;color:var(--ink)}}
.crow .lab small {{display:block;color:var(--muted);font-size:12.5px}}
.crow .bars {{display:flex;flex-direction:column;gap:6px}}
.crow .b {{display:flex;align-items:center;gap:8px;font-size:13px;font-family:{NUM};color:var(--ink2)}}
.crow .bar {{height:10px;border-radius:999px}}
.summary {{border-radius:18px;padding:28px;background:linear-gradient(135deg,#EEF5FF,#FFF6E6);border:1px solid var(--line)}}
.summary h3 {{font-family:{SERIF} !important;font-weight:700;font-size:clamp(20px,2vw,27px);margin:0 0 14px;line-height:1.45;color:var(--ink)}}
.summary h3 em {{font-style:normal;color:var(--cInk)}}
.summary ul {{list-style:none;padding:0;margin:4px 0 0;font-size:14.5px;color:var(--ink2);display:flex;flex-direction:column;gap:9px;line-height:1.6}}
.summary b {{font-family:{NUM};color:var(--ink)}}
.summary.big {{padding:30px 34px;position:relative;overflow:hidden}}
.summary.big::after {{content:"";position:absolute;right:-30px;top:-60px;width:180px;height:180px;border-radius:50%;background:{MOON};opacity:.35}}
.summary .kicker {{font-family:{MONO};font-size:12px;letter-spacing:.12em;color:var(--sInk);margin-bottom:10px;position:relative;z-index:1}}
.summary.big h3, .summary.big ul {{position:relative;z-index:1}}
.summary.big h3 {{font-size:clamp(24px,2.6vw,34px)}}

/* 사이트 제목 */
.site-head {{padding:4px 0 18px;margin-bottom:6px;border-bottom:1px solid var(--line2)}}
.site-head h1 {{font-family:{SERIF} !important;font-weight:900;font-size:clamp(28px,3.2vw,42px);letter-spacing:-.02em;margin:0;padding:0;color:var(--ink);line-height:1.2}}
.site-head p {{margin:8px 0 0;font-size:16px;color:var(--ink2)}}
div[class*="st-key-card-detail-filter"], div[class*="st-key-card-hs-filter"] {{padding:12px 20px;border-radius:16px}}
.src-note {{font-size:12px;color:var(--muted);line-height:1.5;margin-top:8px}}

/* 사이드바 */
.side-h {{font-family:{SERIF} !important;font-weight:900;font-size:20px;color:var(--ink);margin:6px 0 2px}}
/* 사이드바 지표 선택: 2 × 2 격자 (칸 크기 · 글자 위치를 똑같이) */
section[data-testid="stSidebar"] [data-testid="stButtonGroup"] {{width:100%}}
section[data-testid="stSidebar"] [data-testid="stButtonGroup"] [data-baseweb="button-group"] {{
  display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;width:100%;
  background:transparent;padding:0;border-radius:0}}
section[data-testid="stSidebar"] button[data-testid^="stBaseButton-segmented_control"] {{
  width:100%;min-height:44px;padding:8px 6px;justify-content:center;text-align:center;
  border:1px solid var(--line) !important;border-radius:12px !important;background:#FFFFFF;
  color:var(--ink2);font-size:14.5px;font-weight:500;box-shadow:0 1px 2px rgba(15,23,42,.04);
  transition:border-color .15s, background .15s}}
section[data-testid="stSidebar"] button[data-testid^="stBaseButton-segmented_control"] p {{margin:0;white-space:nowrap}}
section[data-testid="stSidebar"] button[data-testid="stBaseButton-segmented_control"]:hover {{border-color:var(--c) !important;color:var(--ink)}}
section[data-testid="stSidebar"] button[data-testid="stBaseButton-segmented_controlActive"] {{
  background:var(--c) !important;border-color:var(--c) !important;color:#1A1204 !important;font-weight:700;
  box-shadow:0 2px 6px rgba(212,128,26,.28)}}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{font-size:13px;font-weight:600;color:var(--ink2);margin-bottom:2px}}

@media (max-width:900px) {{.hero .moon {{width:130px;height:130px;right:-20px}}}}
@media (max-width:640px) {{div[class*="st-key-card-"] {{padding:18px 16px}} .crow {{grid-template-columns:1fr}}}}
</style>
"""

FAQ_CSS = f"""
<style>
.faq-hero {{position:relative;overflow:hidden;border-radius:24px;padding:30px 36px;margin:4px 0 20px;
  background:linear-gradient(135deg,#EEF5FF,#F8FAFF 60%,#FFF6E6);border:1px solid {LINE}}}
.faq-hero::after {{content:"";position:absolute;right:40px;top:-50px;width:150px;height:150px;border-radius:50%;background:{MOON};opacity:.8}}
.faq-hero h1 {{font-family:{SERIF} !important;margin:0;padding:0;font-size:clamp(28px,3vw,38px);line-height:1.25;color:{INK};font-weight:900;position:relative;z-index:1}}
.faq-hero p {{margin:8px 0 0;font-size:14.5px;color:{INK2};position:relative;z-index:1}}
.faq-sec {{font-size:17px;font-weight:700;color:{INK};margin:22px 0 10px}}
.faq-sec small {{font-size:13px;font-weight:400;color:{MUTED};margin-left:6px}}
.faq-a {{font-size:15.5px;line-height:1.9;color:{INK};word-break:keep-all}}
.faq-src {{display:inline-block;margin-top:12px;font-size:12.5px;color:{S_INK};background:{S_BG};border-radius:999px;padding:3px 10px}}
[data-testid="stExpander"] details {{background:#FFFFFF;border:1px solid {LINE} !important;border-radius:16px;box-shadow:0 1px 2px rgba(15,23,42,.04)}}
[data-testid="stExpander"] summary p {{font-size:15px;color:{INK}}}
</style>
"""


def card_head(title: str, meta: str = "", sub: str = "", swatch: str | None = None) -> str:
    sw = f"<i class='sw' style='background:{swatch}'></i>" if swatch else ""
    small = f" <small>{sub}</small>" if sub else ""
    return f"<div class='ch'><h2>{sw}{title}{small}</h2><span class='meta'>{meta}</span></div>"


def hero(st, ctx) -> None:
    """달이 뜬 머리글 배너 (이 버전의 대시보드에서는 쓰지 않지만, 필요하면 app.py에서 T.hero(st, ctx)로 부르면 됩니다)."""
    s, m = ctx["summary"], ctx["metric"]
    from analysis import METRIC_NAMES
    a, b = s.loc["설날", f"{m}_일평균"], s.loc["추석", f"{m}_일평균"]
    period = ctx["PERIOD"].replace("~", "–") if ctx["year"] is None else f"{ctx['year']}년"
    if a != b and min(a, b) > 0:
        w = "추석" if b > a else "설날"
        win = (f"<span class='chip win {'S' if w == '설날' else ''}'>더 위험한 명절 <b>{w}</b> · "
               f"일평균 {METRIC_NAMES[m]} +{(max(a, b) / min(a, b) - 1) * 100:.0f}%</span>")
    else:
        win = "<span class='chip'>두 명절 비슷</span>"
    st.markdown(
        "<div class='hero'><div class='moon'></div>"
        f"<div class='kicker'>HOLIDAY ROAD REPORT · {html.escape(period)}</div>"
        "<h1><span class='s'>설날</span><span class='vs'>vs</span><span class='c'>추석</span></h1>"
        "<div class='sub'>고향 가는 길, 어느 명절 연휴가 더 위험했을까요? 연휴 길이를 맞춰 공정하게 비교합니다.</div>"
        f"<div class='chips'>{win}<span class='chip'>{html.escape(ctx['where'])}</span></div></div>",
        unsafe_allow_html=True,
    )


def plotly_style(fig, height: int = 320, legend: bool = True):
    fig.update_layout(
        height=height, margin=dict(l=6, r=6, t=10, b=6),
        font=dict(family=SANS, size=13.5, color=INK2),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None, font=dict(color=INK, size=13.5)),
        hoverlabel=dict(font_family=SANS, font_size=13, bgcolor=INK, font_color="#FFFFFF", bordercolor=INK),
        barcornerradius=6,
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE, tickfont=dict(color=INK2, size=13.5, family=SANS))
    fig.update_yaxes(gridcolor="#E9EDF3", zeroline=False, tickfont=dict(color=INK2, size=12.5, family=SANS), tickformat=",")
    return fig
