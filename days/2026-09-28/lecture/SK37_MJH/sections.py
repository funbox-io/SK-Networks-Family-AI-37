"""대시보드 화면 영역(카드)들. 색·글꼴은 theme.py(T)에서 받아서 그립니다.

두 디자인 버전(첨부 HTML 디자인 / 새 디자인)이 이 파일을 똑같이 쓰고, theme.py만 다릅니다.
화면 순서 (첨부 HTML 기준)
    [전체 비교]  필터 → 설날 VS 추석 → 연도별 비교 · 치사율 → 일자별 추이(D 기준)
                → 지역별 차이 지도 · 시·도 순위 → 사고다발지점 · Top 6 · 데이터 메모
                → 사고다발지 목록 · 핵심 인사이트 (지금까지 만든 내용)
    [연도 상세]  일자별 상세표 · 시·도 × 일자 히트맵 → 피해 구성 비교 · 한 줄 요약
                → 시군구 TOP 10 · 요일별 하루 평균 (지금까지 만든 내용)
"""
from __future__ import annotations

import html

import pandas as pd
import plotly.graph_objects as go

from analysis import (
    HOLIDAYS,
    HOTSPOT_PERIOD,
    METRIC_NAMES,
    METRICS,
    SIDO_TILES,
    WEEKDAYS,
    composition,
    d_label,
    day_table_d,
    day_trend_d,
    hotspot_area_stats,
    hotspot_values,
    hotspots_in,
    d_totals,
    filter_years,
    fixed_insights,
    insights,
    overall_summary,
    previous_year_summary,
    region_rows,
    summarize,
    period_text,
    sgg_top,
    sido_diff,
    sido_heat,
    weekday_compare,
    year_summary,
    yearly,
)

esc = html.escape


# ---------------------------------------------------------------- 작은 도구
def md(text: str) -> str:
    """마크다운으로 그려지는 곳(st.caption 등)에서 '2021~2025'가 취소선이 되지 않게 합니다."""
    return text.replace("~", r"\~")


def fmt(v, dp: int = 0) -> str:
    if v is None or pd.isna(v):
        return "—"
    return f"{v:,.{dp}f}"


def pct(a, b):
    return (a - b) / b * 100 if b else None


def mix(c1: str, c2: str, p: float) -> str:
    """c1 → c2 사이 색 (p = 0~100, c2 쪽 비율)."""
    p = max(0.0, min(100.0, float(p))) / 100
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * p):02X}" for x, y in zip(a, b))


def text_on(bg: str, light: str, dark: str) -> str:
    """배경색 밝기에 맞는 글자색."""
    r, g, b = (int(bg[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return dark if (0.2126 * r + 0.7152 * g + 0.0722 * b) > 0.55 else light


def delta_html(p, T) -> str:
    if p is None:
        return "—"
    a = f"{abs(p):.1f}%"
    return f"<span class='up'>▲</span> {a}" if p > 0 else (f"▼ {a}" if p < 0 else "— 0.0%")


def card(st, name: str):
    return st.container(key=f"card-{name}")


def head(st, T, title: str, meta: str = "", sub: str = "", swatch: str | None = None, meta_html: bool = False):
    st.markdown(T.card_head(title, meta if meta_html else esc(meta), sub, swatch), unsafe_allow_html=True)


def legend_html(T, items: list[tuple[str, str]], right: str = "") -> str:
    """items = [(스와치 HTML, 라벨)]"""
    spans = "".join(f"<span>{sw}{esc(lab)}</span>" for sw, lab in items)
    return f"<div class='foot'><div class='legend'>{spans}</div><span class='meta'>{esc(right)}</span></div>"


def sw_box(color):  # 네모 스와치
    return f"<i class='sw' style='background:{color};color:{color}'></i>"


def sw_line(color, dashed=False):
    style = f"border-top:3px {'dashed' if dashed else 'solid'} {color};height:0;width:22px;border-radius:0;background:none;box-shadow:none"
    return f"<i class='sw' style='{style}'></i>"


# ================================================================= 필터
def filters(st, T, ctx) -> dict:
    """상단 필터 카드. 선택값을 dict로 돌려줍니다."""
    YEARS, df = ctx["YEARS"], ctx["df"]
    with card(st, "filters"):
        c = st.columns([3.1, 3.1, 2.2, 1.3, 1.3, 1.2], vertical_alignment="center")
        y = c[0].segmented_control("연도", ["전체", *map(str, YEARS)], default="전체", key="f_year") or "전체"
        m = c[1].segmented_control("지표", list(METRICS), default="사고", key="f_metric",
                                   format_func=lambda k: METRIC_NAMES[k]) or "사고"
        avg = c[2].checkbox("일평균으로 보정 (연휴 길이 차이 반영)", value=False, key="f_avg")
        sido = c[3].selectbox("시도", ["전체"] + ctx["sido_list"], key="f_sido")
        sgg = c[4].selectbox("시군구", ["전체"] + ctx["sgg_list"](sido), disabled=sido == "전체", key="f_sgg")
        dmin, dmax = df["날짜"].min(), df["날짜"].max()
        c[5].markdown(f"<div class='asof'>자료 범위<br>{dmin:%Y.%m} – {dmax:%Y.%m}</div>", unsafe_allow_html=True)
    return {"year": None if y == "전체" else int(y), "metric": m, "per_day": avg, "sido": sido, "sgg": sgg}


def filters_sidebar(st, T, ctx) -> dict:
    """사이드바 필터: 지표 · 일평균 보정만 (연도는 연도 상세 탭, 지역은 사고다발지점 탭에 있습니다)."""
    with st.sidebar:
        st.markdown("<div class='side-h'>조건</div>", unsafe_allow_html=True)
        m = st.segmented_control("지표", list(METRICS), default="사고", key="f_metric",
                                 format_func=lambda k: METRIC_NAMES[k]) or "사고"
        avg = st.toggle("일평균 보정 (연휴 길이 차이 반영)", value=False, key="f_avg")
        dmin, dmax = ctx["df"]["날짜"].min(), ctx["df"]["날짜"].max()
        st.markdown(f"<div class='asof' style='text-align:left;margin-top:6px'>자료 범위 {dmin:%Y.%m} – {dmax:%Y.%m}</div>",
                    unsafe_allow_html=True)
    return {"metric": m, "per_day": avg}


def site_header(st, T):
    """사이트 최상단 제목."""
    st.markdown("<div class='site-head'><h1>대한민국 명절 교통사고 데이터</h1>"
                "<p>설날 vs 추석, 어떤 연휴가 더 위험할까?</p></div>", unsafe_allow_html=True)


def with_scope(ctx: dict, year=None, sido: str = "전체", sgg: str = "전체") -> dict:
    """탭마다 쓰는 범위(연도 · 지역)로 ctx를 새로 만듭니다."""
    c = dict(ctx, year=year, sido=sido, sgg=sgg)
    c["where"] = "전국" if sido == "전체" else (sido if sgg == "전체" else f"{sido} {sgg}")
    c["rows"] = region_rows(ctx["df"], sido, sgg)
    c["cur"] = filter_years(c["rows"], year)
    c["summary"] = summarize(c["cur"])
    c["prev"] = previous_year_summary(c["rows"], year)
    return c


# ================================================================= 전체 비교
def fixed_summary_card(st, T, ctx):
    """맨 위 요약. 필터와 상관없이 항상 전국 · 전체 기간 · 사고 기준으로 같은 결과를 보여 줍니다."""
    o = overall_summary(ctx["df"])
    S, C = o["설날"], o["추석"]
    w = "추석" if C["일평균"] >= S["일평균"] else "설날"
    p = pct(max(S["일평균"], C["일평균"]), min(S["일평균"], C["일평균"]))
    fw = "추석" if C["치사율"] > S["치사율"] else "설날"
    body = (f"<div class='kicker'>전체 기간 요약 · {o['기간']} · 전국 · 사고 기준</div>"
            f"<h3>{o['기간']} 5년간은 <em>{w}</em>이 일평균 사고 기준 <em>{p:.1f}%</em> 더 위험했다</h3><ul>"
            f"<li>일평균 사고 설날 <b>{S['일평균']:.1f}</b>건 vs 추석 <b>{C['일평균']:.1f}</b>건 (연휴 {S['일수']}일 · {C['일수']}일)</li>"
            f"<li>치사율 설날 {S['치사율']:.2f} vs 추석 {C['치사율']:.2f} — {fw}이 사고당 더 치명적</li>"
            f"<li>최다 사고일: 설 {S['최다일']} · 추석 {C['최다일']}</li>"
            f"<li>{o['연수']}년 중 <b>{o['추석우세연수']}</b>년은 추석의 일평균 사고가 더 많았습니다</li></ul>")
    with card(st, "fixed-summary"):
        st.markdown(f"<div class='summary big'>{body}</div>"
                    "<div class='meta' style='margin-top:10px'>이 요약은 사이드바 필터와 연동되지 않는 고정 결과입니다. "
                    "아래 카드들은 선택한 조건에 따라 바뀝니다.</div>", unsafe_allow_html=True)


def kpi_panel(st, T, ctx, h: str):
    s, prev, year, m, avg = ctx["summary"], ctx["prev"], ctx["year"], ctx["metric"], ctx["per_day"]
    dp = 1 if avg else 0
    tiles = []
    for key in ["사고", "사망", "부상"]:
        v = s.loc[h, f"{key}_일평균" if avg else key]
        if prev is not None:
            pv = prev.loc[h, f"{key}_일평균" if avg else key]
            d = f"전년 대비 {delta_html(pct(v, pv), T)}"
        else:
            d = f"{len(ctx['YEARS'])}년 합산{' · 일평균' if avg else ''}" if year is None else "전년 자료 없음"
        tiles.append(f"<div class='kpi'><div class='l'>{METRIC_NAMES[key]}</div>"
                     f"<div class='v'>{fmt(v, dp)}<small>{METRICS[key]}</small></div><div class='d'>{d}</div></div>")
    da = s.loc[h, f"{m}_일평균"]
    dd = f"{METRICS[m]} / 일"
    if prev is not None:
        dd += f"<br>전년 {delta_html(pct(da, prev.loc[h, f'{m}_일평균']), T)}"
    bg, ink = T.TINTS[h]
    tiles.append(f"<div class='kpi hl' style='background:{bg}'><div class='l'>일평균 {METRIC_NAMES[m].replace(' 건수', '')}</div>"
                 f"<div class='v' style='color:{ink}'>{fmt(da, 1)}</div><div class='d'>{dd}</div></div>")
    with card(st, f"kpi-{h}"):
        head(st, T, f"{h} 연휴", meta=f"<span class='mono'>{esc(period_text(ctx['rows'], year, h))}</span>",
             swatch=T.COLORS[h], meta_html=True)
        st.markdown(f"<div class='kpi-wrap'><div class='kpis'>{''.join(tiles)}</div></div>", unsafe_allow_html=True)


def vs_center(st, T, ctx):
    s, m = ctx["summary"], ctx["metric"]
    a, b = s.loc["설날", f"{m}_일평균"], s.loc["추석", f"{m}_일평균"]
    if a == b:
        verdict = "<div class='verdict'>같음</div>"
    else:
        w = "추석" if b > a else "설날"
        p = pct(max(a, b), min(a, b))
        bg, ink = T.TINTS[w]
        txt = f"{w} +{p:.1f}%" if p is not None else f"{w} (상대 0)"
        verdict = f"<div class='verdict' style='background:{bg};color:{ink}'>{txt}</div>"
    st.markdown(
        f"<div class='vs-center'><div class='vsdot'>VS</div><div class='meta'>더 위험한 명절</div>{verdict}"
        f"<div class='meta'>{METRIC_NAMES[m]} · 일평균 기준<br><span class='mono'>{fmt(a, 1)} vs {fmt(b, 1)}</span></div></div>",
        unsafe_allow_html=True,
    )


def years_card(st, T, ctx):
    m, avg, year = ctx["metric"], ctx["per_day"], ctx["year"]
    yt = yearly(ctx["rows"], m, avg)
    dp = 1 if avg else 0
    with card(st, "years"):
        head(st, T, "연도별 비교", meta=f"묶음 막대 · {METRIC_NAMES[m]}{' · 일평균' if avg else ''}")
        fig = go.Figure()
        for h in HOLIDAYS:
            t = yt[yt["명절"] == h].reset_index(drop=True)
            prev = t["값"].shift(1)
            chg = [("—" if pd.isna(p) or not p else f"{(v - p) / p * 100:+.1f}%") for v, p in zip(t["값"], prev)]
            fig.add_bar(
                name=h, x=t["연도"].astype(str), y=t["값"], marker_color=T.COLORS[h],
                marker_opacity=[1 if (year is None or y == year) else 0.28 for y in t["연도"]],
                text=[fmt(v, dp) if (year is None or y == year) else "" for v, y in zip(t["값"], t["연도"])],
                textposition="outside", textfont=dict(color=T.INK2, size=11), cliponaxis=False,
                customdata=list(zip(t["일수"], chg)),
                hovertemplate=f"<b>%{{x}} {h}</b><br>{METRIC_NAMES[m]} %{{y:,.{dp}f}}{' /일' if avg else ''}"
                              "<br>전년 대비 %{customdata[1]}<br>연휴 %{customdata[0]}일<extra></extra>",
            )
        fig.update_layout(barmode="group", bargap=0.45, bargroupgap=0.08)
        st.plotly_chart(T.plotly_style(fig, 300, legend=False), use_container_width=True)
        st.markdown(legend_html(T, [(sw_box(T.COLORS["설날"]), "설날"), (sw_box(T.COLORS["추석"]), "추석")],
                                "막대에 마우스를 올리면 값 · 전년 대비 증감"), unsafe_allow_html=True)


def holiday_main_card(st, T, ctx):
    """연도별 비교를 설날 · 추석이 주인공이 되도록: 왼쪽 설날 / 오른쪽 추석 두 묶음, 안에 연도 막대."""
    from plotly.subplots import make_subplots
    m, avg, year = ctx["metric"], ctx["per_day"], ctx["year"]
    yt = yearly(ctx["rows"], m, avg)
    dp = 1 if avg else 0
    ymax = max(yt["값"].max(), 1e-9) * 1.18
    with card(st, "holiday-main"):
        head(st, T, "설날 vs 추석 · 연도별 비교", meta=f"{METRIC_NAMES[m]}{' · 일평균' if avg else ' · 합계'} · 점선 = 5년 평균")
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06, subplot_titles=HOLIDAYS)
        for i, h in enumerate(HOLIDAYS, start=1):
            t = yt[yt["명절"] == h].reset_index(drop=True)
            prev = t["값"].shift(1)
            chg = [("—" if pd.isna(p) or not p else f"{(v - p) / p * 100:+.1f}%") for v, p in zip(t["값"], prev)]
            shades = [mix(T.WASH, T.COLORS[h], 45 + 55 * k / max(len(t) - 1, 1)) for k in range(len(t))]
            fig.add_bar(
                x=t["연도"].astype(str), y=t["값"], name=h, marker_color=shades,
                marker_opacity=[1 if (year is None or y == year) else 0.3 for y in t["연도"]],
                text=[fmt(v, dp) for v in t["값"]], textposition="outside", cliponaxis=False,
                textfont=dict(color=T.INK, size=12),
                customdata=list(zip(t["일수"], chg)),
                hovertemplate=f"<b>%{{x}} {h}</b><br>{METRIC_NAMES[m]} %{{y:,.{dp}f}}{' /일' if avg else ''}"
                              "<br>전년 대비 %{customdata[1]}<br>연휴 %{customdata[0]}일<extra></extra>",
                row=1, col=i, showlegend=False,
            )
            mean = t["값"].mean()
            fig.add_hline(y=mean, line_dash="dot", line_color=T.COLORS[h], line_width=1.5, row=1, col=i,
                          annotation_text=f"평균 {fmt(mean, dp)}", annotation_position="top left",
                          annotation_font=dict(color=T.TINTS[h][1], size=12))
        fig.update_layout(bargap=0.35)
        fig.update_yaxes(range=[0, ymax])
        for a in fig.layout.annotations:
            if a.text in HOLIDAYS:
                a.font = dict(size=15, color=T.TINTS[a.text][1])
        st.plotly_chart(T.plotly_style(fig, 340, legend=False), use_container_width=True)
        s, c = yt[yt["명절"] == "설날"]["값"].mean(), yt[yt["명절"] == "추석"]["값"].mean()
        w = "추석" if c >= s else "설날"
        st.markdown(legend_html(T, [(sw_box(T.COLORS["설날"]), "설날"), (sw_box(T.COLORS["추석"]), "추석")],
                                f"5년 평균은 {w}이 {abs(pct(max(s, c), min(s, c)) or 0):.0f}% 많음 · 진할수록 최근 연도"),
                    unsafe_allow_html=True)


def rate_card(st, T, ctx):
    s, year = ctx["summary"], ctx["year"]
    S, C = s.loc["설날", "치사율"], s.loc["추석", "치사율"]
    mx = max(S, C, 0.01) * 1.25
    bars = "".join(
        f"<div><div class='row'><span>{h}</span><b>{v:.2f}</b></div>"
        f"<div class='track'><div class='fill' style='width:{v / mx * 100:.1f}%;background:{T.COLORS[h]};color:{T.COLORS[h]}'></div></div>"
        f"<div class='rsub'>사망 {int(s.loc[h, '사망']):,}명 ÷ 사고 {int(s.loc[h, '사고']):,}건 × 100</div></div>"
        for h, v in (("설날", S), ("추석", C))
    )
    scope = f"{len(ctx['YEARS'])}년 합산" if year is None else f"{year}년"
    notes = []
    if S and C and S != C:
        hi, lo = ("추석", "설날") if C > S else ("설날", "추석")
        notes.append(f"사고 100건당 사망자는 {hi}이 {lo}보다 <b>{abs(pct(max(S, C), min(S, C))):.0f}%</b> 많습니다 ({scope}).")
    zero = [h for h in HOLIDAYS if s.loc[h, "사망"] == 0 and s.loc[h, "사고"] > 0]
    if zero:
        notes.append(f"{'·'.join(zero)} 연휴는 이 조건에서 사망자가 0명이라 치사율이 0입니다.")
    if 0 < s["사망"].min() < 5 or zero:
        notes.append("사망자가 적으면 한두 명 차이로 크게 흔들리니 전국·전체 기간과 함께 보세요.")
    notes.append("건수는 적어도 더 치명적인 명절이 있는지 보여주는 보조 지표 · 연도 필터와 연동.")
    with card(st, "rate"):
        head(st, T, "치사율 비교", meta="사망자 ÷ 사고 × 100")
        st.markdown(f"<div class='rate'>{bars}</div><div class='note'>{' '.join(notes)}</div>", unsafe_allow_html=True)


def trend_card(st, T, ctx):
    m, year = ctx["metric"], ctx["year"]
    dt = day_trend_d(ctx["cur"], m)
    offs = sorted(dt["D"].unique())
    labels = [d_label(o) if o else "D (당일)" for o in offs]
    lab_of = dict(zip(offs, labels))
    with card(st, "trend"):
        head(st, T, "연휴 일자별 추이", sub="— 귀성일과 귀경일, 언제 더 위험한가", meta="꺾은선 · 명절 당일 = D")
        fig = go.Figure()
        if 0 in offs:
            i = offs.index(0)
            fig.add_shape(type="rect", xref="x", yref="paper", x0=i - 0.5, x1=i + 0.5, y0=0, y1=1,
                          fillcolor=T.WASH, opacity=0.8, line_width=0, layer="below")
        dp = 1 if year is None else 0
        for h in HOLIDAYS:
            t = dt[dt["명절"] == h]
            if t.empty:
                continue
            x = [lab_of[o] for o in t["D"]]
            top = t.loc[t["값"].idxmax()]
            fig.add_scatter(
                name=h, x=x, y=t["값"], mode="lines+markers",
                line=dict(color=T.COLORS[h], width=2.8, dash="solid" if h == "설날" else "dash"),
                marker=dict(size=[12 if v == top["값"] else 8 for v in t["값"]], color=T.COLORS[h],
                            line=dict(color=T.SURFACE, width=2)),
                customdata=list(zip(t["연도수"], t["날짜들"])),
                hovertemplate=f"<b>{h} %{{x}}</b><br>"
                              + ("%{customdata[0]}개년 평균 " if year is None else "")
                              + f"{METRIC_NAMES[m]} %{{y:,.{dp}f}}{METRICS[m]}<br>%{{customdata[1]}}<extra></extra>",
            )
            fig.add_annotation(x=lab_of[top["D"]], y=top["값"], text=f"{h} 최다 {d_label(top['D'])} · {fmt(top['값'], dp)}",
                               showarrow=False, yshift=18, xshift=-40 if h == "설날" else 40,
                               font=dict(color=T.TINTS[h][1], size=12))
        fig.update_xaxes(categoryorder="array", categoryarray=labels)
        st.plotly_chart(T.plotly_style(fig, 280, legend=False), use_container_width=True)
        note = "전체 = 같은 D끼리 연도 평균 · 연휴 길이가 다른 해는 D 기준 정렬" if year is None else "연휴 길이가 다른 해는 D 기준 정렬 · 점 호버 → 날짜"
        st.markdown(legend_html(T, [(sw_line(T.COLORS["설날"]), "설날"), (sw_line(T.COLORS["추석"], True), "추석"),
                                    ("", "음영 = 명절 당일")], note), unsafe_allow_html=True)


def tiles_card(st, T, ctx):
    m, avg, year = ctx["metric"], ctx["per_day"], ctx["year"]
    t = sido_diff(ctx["df"], year, m, avg).set_index("시도")
    dp = 1 if avg else 0
    with card(st, "tiles"):
        c1, c2 = st.columns([1, 1.3], vertical_alignment="center")
        c1.markdown(T.card_head("지역별 차이 지도"), unsafe_allow_html=True)
        mode = c2.segmented_control("지도", ["추석 − 설", "설날", "추석"], default="추석 − 설", key="f_tile",
                                    label_visibility="collapsed") or "추석 − 설"
        if mode == "추석 − 설":
            lim = t["증감률"].abs().clip(upper=100).max()
            lim = max(10, int(-(-lim // 10) * 10)) if pd.notna(lim) else 10
        else:
            lim = max(t[mode].max(), 1e-9)
        cells = []
        for name, col, row in SIDO_TILES:
            o = t.loc[name] if name in t.index else None
            if o is None:
                continue
            if mode == "추석 − 설":
                q = 0 if pd.isna(o["증감률"]) else max(-1, min(1, o["증감률"] / lim))
                bg = mix(T.WASH, T.COLORS["추석" if q > 0 else "설날"], abs(q) * 78)
                lab = "—" if pd.isna(o["증감률"]) else f"{o['증감률']:+.0f}%"
            else:
                bg = mix(T.WASH, T.COLORS[mode], o[mode] / lim * 80)
                lab = fmt(o[mode], dp)
            fg = text_on(bg, "#FFFFFF", T.INK_ON_LIGHT)
            sel = " sel" if ctx["sido"] == name else ""
            tip = (f"{name} · 설날 {fmt(o['설날'], dp)} · 추석 {fmt(o['추석'], dp)} · 차이 {o['차이']:+,.{dp}f}"
                   + ("" if pd.isna(o["증감률"]) else f" ({o['증감률']:+.1f}%)"))
            cells.append(f"<div class='tile{sel}' title='{esc(tip)}' style='grid-column:{col + 1};grid-row:{row + 1};"
                         f"background:{bg};color:{fg}'>{name}<small>{lab}</small></div>")
        if mode == "추석 − 설":
            ramp = (f"<span>설 많음 −{lim}%</span><i style='background:linear-gradient(90deg,{mix(T.WASH, T.COLORS['설날'], 78)},"
                    f"{T.WASH},{mix(T.WASH, T.COLORS['추석'], 78)})'></i><span>추석 많음 +{lim}%</span>")
        else:
            ramp = (f"<span>0</span><i style='background:linear-gradient(90deg,{T.WASH},{mix(T.WASH, T.COLORS[mode], 80)})'></i>"
                    f"<span>{fmt(lim, dp)} {METRICS[m]}</span>")
        st.markdown(f"<div class='tiles'>{''.join(cells)}</div><div class='ramp'>{ramp}</div>", unsafe_allow_html=True)
        st.caption(md(f"{'전체 기간' if year is None else f'{year}년'} · {METRIC_NAMES[m]}{' 일평균' if avg else ''} · 칸에 마우스를 올리면 값"))


def rank_card(st, T, ctx):
    m, avg = ctx["metric"], ctx["per_day"]
    t = sido_diff(ctx["df"], ctx["year"], m, avg)
    dp = 1 if avg else 0
    with card(st, "rank"):
        c1, c2 = st.columns([1, 1.4], vertical_alignment="center")
        c1.markdown(T.card_head("시·도 순위"), unsafe_allow_html=True)
        key = c2.segmented_control("정렬", ["차이", "%", "설날", "추석", "시·도"], default="차이", key="f_rank_sort",
                                   label_visibility="collapsed") or "차이"
        col = {"차이": "차이", "%": "증감률", "설날": "설날", "추석": "추석", "시·도": "시도"}[key]
        t = t.sort_values(col, ascending=(col == "시도"), na_position="last").reset_index(drop=True)
        expand = st.session_state.get("f_rank_all", False)
        vis = (t if expand else t.head(6)).copy()
        vis["pct_txt"] = vis["증감률"].map(lambda v: "—" if pd.isna(v) else f"{v:+.0f}%")
        body = "".join(
            f"<tr class='{'sel' if r['시도'] == ctx['sido'] else ''}'><td class='rk'>{i + 1}</td><td>{r['시도']}</td>"
            f"<td class='r'>{fmt(r['설날'], dp)}</td><td class='r'>{fmt(r['추석'], dp)}</td>"
            f"<td class='r' style='font-weight:600'>{r['차이']:+,.{dp}f}</td>"
            f"<td class='r' style='color:{T.INK2}'>{r['pct_txt']}</td></tr>"
            for i, r in vis.iterrows()
        )
        arrow = lambda k: " ↓" if k == key and key != "시·도" else (" ↑" if k == key else "")
        st.markdown(
            f"<div class='tw'><table class='tbl'><thead><tr><th>#</th><th>시·도{arrow('시·도')}</th><th class='r'>설날{arrow('설날')}</th>"
            f"<th class='r'>추석{arrow('추석')}</th><th class='r'>차이{arrow('차이')}</th><th class='r'>%{arrow('%')}</th></tr></thead>"
            f"<tbody>{body}</tbody></table></div>", unsafe_allow_html=True)
        st.toggle("17개 시·도 전체 보기", key="f_rank_all")


def hotspot_scatter_card(st, T, ctx):
    m, year = ctx["metric"], ctx["year"]
    hs_view = hotspots_in(ctx["hotspots"], ctx["sido"], ctx["sgg"])
    with card(st, "hs-map"):
        head(st, T, "명절 사고다발지점", meta=f"{HOTSPOT_PERIOD.replace('~', '–')} 연휴 합산 · {len(hs_view)}곳")
        fig = go.Figure()
        feats = [f["properties"]["n"] for f in ctx["geo"]["features"]]
        fig.add_trace(go.Choropleth(
            geojson=ctx["geo"], locations=feats, z=[1] * len(feats), featureidkey="properties.n",
            colorscale=[[0, T.WASH], [1, T.WASH]], showscale=False, hoverinfo="skip",
            marker_line_color=T.LINE, marker_line_width=1,
        ))
        if ctx["sido"] != "전체":
            fig.add_trace(go.Choropleth(
                geojson=ctx["geo"], locations=[ctx["sido"]], z=[1], featureidkey="properties.n",
                colorscale=[[0, T.SEL_FILL], [1, T.SEL_FILL]], showscale=False, hoverinfo="skip",
                marker_line_color=T.INK2, marker_line_width=1.5,
            ))
        if not hs_view.empty:
            hv = hotspot_area_stats(ctx["df"], hs_view, year, m).assign(
                값=hotspot_values(hs_view, m).to_numpy(), 부상자=hotspot_values(hs_view, "부상").to_numpy())
            hv = hv.sort_values("값", ascending=False)
            vmax = max(hotspot_values(ctx["hotspots"], m).max(), 1)
            has = hv["값"] > 0
            area = f"{year}년" if year else ctx["PERIOD"]
            fig.add_trace(go.Scattergeo(
                lon=hv["경도"], lat=hv["위도"], mode="markers",
                marker=dict(size=5 + 15 * (hv["값"] / vmax) ** 0.5,
                            color=[T.COLORS["설날"] if x else T.S_SOFT for x in has], opacity=0.9,
                            line=dict(color=[T.SURFACE if x else T.COLORS["설날"] for x in has], width=1.3)),
                customdata=hv[["지점명", "값", "사고", "사상자", "사망", "중상", "경상", "부상신고", "시군구_기준", "지역_설날", "지역_추석"]],
                hovertemplate=(
                    f"<b>%{{customdata[0]}}</b><br><b>{METRIC_NAMES[m]} %{{customdata[1]:,}}{METRICS[m]}</b>"
                    "<br>발생 %{customdata[2]}건 · 사상자 %{customdata[3]}명"
                    "<br>사망 %{customdata[4]} · 중상 %{customdata[5]} · 경상 %{customdata[6]} · 부상신고 %{customdata[7]}"
                    f"<br>── 소속 %{{customdata[8]}} {area} 연휴 {METRIC_NAMES[m]} ──"
                    f"<br>설날 %{{customdata[9]:,.0f}} · 추석 %{{customdata[10]:,.0f}}<extra></extra>"),
                showlegend=False,
            ))
        fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(T.plotly_style(fig, 600, legend=False), use_container_width=True)
        st.markdown(f"<div class='meta'>원 크기 = 선택 지표({esc(METRIC_NAMES[m])}) · 진한 점 = 발생 · 옅은 점 = 0 · "
                    "툴팁 아래쪽은 소속 시군구의 선택 연도 수치</div>", unsafe_allow_html=True)


def hotspot_top_card(st, T, ctx):
    hs = hotspots_in(ctx["hotspots"], ctx["sido"], ctx["sgg"]).sort_values(["사상자", "사고"], ascending=False).head(6)
    items = "".join(
        f"<li><span class='k'>{i}</span><span>{esc(r['지점명'].split(' ', 1)[1] if ' ' in r['지점명'] else r['지점명'])}"
        f"<small>발생 {r['사고']}건 · 중상 {r['중상']} · 경상 {r['경상']}</small></span><b>{r['사상자']}명</b></li>"
        for i, (_, r) in enumerate(hs.iterrows(), start=1)
    ) or f"<li><span></span><span class='meta'>{esc(ctx['where'])}에는 사고다발지가 없습니다.</span></li>"
    with card(st, "hs-top"):
        head(st, T, "다발지점 Top 6", meta="사상자 순")
        st.markdown(f"<div class='hs'><ol>{items}</ol></div>", unsafe_allow_html=True)


def memo_card(st, T, ctx):
    with card(st, "memo"):
        head(st, T, "데이터 메모")
        st.markdown(
            "<div class='src'>"
            "<p>연휴 기간은 자료에 수록된 날짜 기준이며 해마다 3~5일로 다릅니다. 길이 차이를 지우려면 <b>일평균 보정</b>을 켜세요.</p>"
            "<p>D는 음력 1월 1일·8월 15일 당일. 2023년 추석 D+3(10.2)은 임시공휴일, 2025년 추석은 수록된 4일(10.5–10.8)만 반영.</p>"
            f"<p>다발지점 자료는 {HOTSPOT_PERIOD} 명절 연휴를 합산한 값이라 연도·설·추석 구분이 없습니다. "
            "연도를 고르면 툴팁·목록에 소속 시군구의 그해 연휴 수치가 함께 나옵니다.</p>"
            "<p>부상자 수에는 중상자가 포함됩니다. 군위군은 2023년 7월 경북에서 대구로 편입되었습니다.</p>"
            "<p class='meta'>자료: 도로교통공단(KoROAD) 설날·추석 연휴기간 사고통계 · 연휴기간 사고다발지역</p></div>",
            unsafe_allow_html=True,
        )


def hotspot_table_card(st, T, ctx):
    m, year = ctx["metric"], ctx["year"]
    hs = hotspots_in(ctx["hotspots"], ctx["sido"], ctx["sgg"])
    with card(st, "hs-table"):
        head(st, T, "연휴 사고다발지 전체 목록", meta=f"{ctx['where']} · {len(hs)}곳 · {METRIC_NAMES[m]} 순")
        with st.expander("목록 펼치기"):
            if hs.empty:
                st.info(f"{ctx['where']}에는 연휴 사고다발지가 없습니다.")
                return
            t = hotspot_area_stats(ctx["df"], hs, year, m).assign(_v=hotspot_values(hs, m).to_numpy())
            t = t.sort_values(["_v", "사고", "사상자"], ascending=False)
            yr = f"{year}년" if year else ctx["PERIOD"]
            cs, cc = f"소속 시군구 {yr} 설날", f"소속 시군구 {yr} 추석"
            st.dataframe(
                t.assign(지역=t["시도"] + " " + t["시군구"]).rename(columns={"지역_설날": cs, "지역_추석": cc})[
                    ["지점명", "지역", "사고", "사상자", "사망", "중상", "경상", "부상신고", cs, cc]],
                hide_index=True, use_container_width=True,
            )
            st.caption(md(f"사고~부상신고는 {HOTSPOT_PERIOD} 합계(연도 구분 없음), 오른쪽 두 열({METRIC_NAMES[m]})은 선택 연도에 따라 바뀝니다."))


def insights_row(st, T, ctx):
    """핵심 인사이트 3장 — 전국 · 전체 기간 · 사고 건수 기준 고정 (analysis.fixed_insights)."""
    st.markdown(T.card_head("핵심 인사이트", meta=esc(f"전국 · {ctx['PERIOD'].replace('~', '–')} 전체 기준 · 사고 건수")),
                unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (col, item) in enumerate(zip(cols, fixed_insights(ctx["df"])), start=1):
        with col:
            with card(st, f"insight-{i}"):
                st.markdown(f"<div class='tag'>INSIGHT {i}</div><div class='ins-t'>{esc(item['title'])}</div>"
                            f"<div class='ins-b'>{esc(item['body'])}</div>", unsafe_allow_html=True)


def trend_totals_card(st, T, ctx):
    """연휴 일자별 2021~2025년 총계 (명절 당일 D 기준, 5년 합계)."""
    m = ctx["metric"]
    dt = d_totals(ctx["rows"], m)
    offs = sorted(dt["D"].unique())
    labels = [d_label(o) if o else "D (당일)" for o in offs]
    lab_of = dict(zip(offs, labels))
    period = ctx["PERIOD"]
    period_html = period.replace("~", "&#126;")   # 제목은 HTML — 물결표가 취소선이 되지 않게
    with card(st, "trend-total"):
        head(st, T, f"연휴 일자별 {period_html}년 {METRIC_NAMES[m].replace(' 건수', '')} 총계", meta="5년 합계 · 명절 당일 = D")
        fig = go.Figure()
        if 0 in offs:
            i = offs.index(0)
            fig.add_shape(type="rect", xref="x", yref="paper", x0=i - 0.5, x1=i + 0.5, y0=0, y1=1,
                          fillcolor=T.WASH, opacity=0.9, line_width=0, layer="below")
        for h in HOLIDAYS:
            t = dt[dt["명절"] == h]
            fig.add_bar(
                name=h, x=[lab_of[o] for o in t["D"]], y=t["값"], marker_color=T.COLORS[h],
                text=[fmt(v) for v in t["값"]], textposition="outside", cliponaxis=False, textfont=dict(color=T.INK, size=12),
                customdata=list(zip(t["연도수"], t["날짜들"])),
                hovertemplate=f"<b>{h} %{{x}}</b><br>{period} 총계 %{{y:,}}{METRICS[m]}"
                              "<br>%{customdata[0]}개 연도 · %{customdata[1]}<extra></extra>",
            )
        fig.update_layout(barmode="group", bargap=0.3, bargroupgap=0.08)
        fig.update_xaxes(categoryorder="array", categoryarray=labels)
        st.plotly_chart(T.plotly_style(fig, 320, legend=False), use_container_width=True)
        tot = dt.groupby("D")["값"].sum()
        top = int(tot.idxmax())
        st.markdown(legend_html(T, [(sw_box(T.COLORS["설날"]), "설날"), (sw_box(T.COLORS["추석"]), "추석"), ("", "음영 = 명절 당일")],
                                f"두 명절 합계 최다: {d_label(top)} {fmt(tot.max())}{METRICS[m]} · D+2·D+3은 연휴가 길었던 해만 포함"),
                    unsafe_allow_html=True)


# ================================================================= 연도 상세
def detail_header(st, T, ctx) -> int:
    YEARS = ctx["YEARS"]
    c1, c2 = st.columns([3, 2], vertical_alignment="bottom")
    dy = c2.segmented_control("상세 연도", list(map(str, YEARS)), default=str(ctx["year"] or 2023), key="f_detail_year",
                              label_visibility="collapsed") or str(ctx["year"] or 2023)
    dy = int(dy)
    c1.markdown(f"<div class='dtitle'><div class='meta'>연도 상세 · {esc(ctx['where'])} · {esc(METRIC_NAMES[ctx['metric']])}</div>"
                f"<h2>{dy}년 설날 vs 추석</h2></div>", unsafe_allow_html=True)
    return dy


def day_table_card(st, T, ctx, dy: int):
    m = ctx["metric"]
    t = day_table_d(ctx["rows"], dy, m)
    mxS, mxC = t["설날_값"].max(), t["추석_값"].max()
    nS, nC = t["설날_값"].notna().sum(), t["추석_값"].notna().sum()
    sS, sC = t["설날_값"].sum(), t["추석_값"].sum()

    def cell(v, mx):
        if pd.isna(v):
            return "<td class='r'>—</td>"
        return f"<td class='r'{' style=font-weight:700' if v == mx else ''}>{fmt(v)}</td>"

    body = "".join(
        f"<tr><td class='mono'>{r['라벨']}</td><td class='dim'>{r['설날_날짜'] if pd.notna(r['설날_날짜']) else '—'}</td>{cell(r['설날_값'], mxS)}"
        f"<td class='dim'>{r['추석_날짜'] if pd.notna(r['추석_날짜']) else '—'}</td>{cell(r['추석_값'], mxC)}</tr>"
        for _, r in t.iterrows()
    )
    body += (f"<tr class='tot'><td>합계</td><td class='meta'>{nS}일</td><td class='r'>{fmt(sS)}</td>"
             f"<td class='meta'>{nC}일</td><td class='r'>{fmt(sC)}</td></tr>"
             f"<tr class='tot'><td>일평균</td><td></td><td class='r'>{fmt(sS / max(nS, 1), 1)}</td>"
             f"<td></td><td class='r'>{fmt(sC / max(nC, 1), 1)}</td></tr>")
    u = METRIC_NAMES[m].replace(" 건수", "")
    with card(st, "d-table"):
        c1, c2 = st.columns([2, 1], vertical_alignment="center")
        c1.markdown(T.card_head("일자별 상세표"), unsafe_allow_html=True)
        csv = t.rename(columns={"라벨": "일자", "설날_날짜": "설날 날짜", "설날_값": f"설날 {u}", "추석_날짜": "추석 날짜", "추석_값": f"추석 {u}"})
        c2.download_button("CSV 내보내기", csv[["일자", "설날 날짜", f"설날 {u}", "추석 날짜", f"추석 {u}"]].to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"{dy}_설날_추석_{u}_{ctx['where']}.csv", mime="text/csv", use_container_width=True)
        st.markdown(
            f"<div class='tw'><table class='tbl'><thead><tr><th>연휴 일자</th><th>설 날짜(요일)</th><th class='r'>설 {u}</th>"
            f"<th>추석 날짜(요일)</th><th class='r'>추석 {u}</th></tr></thead><tbody>{body}</tbody></table></div>"
            "<div class='meta' style='margin-top:10px'>굵은 숫자 = 해당 명절 최다일 · D = 명절 당일</div>",
            unsafe_allow_html=True)


def heat_card(st, T, ctx, dy: int):
    m = ctx["metric"]
    with card(st, "d-heat"):
        c1, c2 = st.columns([2, 1], vertical_alignment="center")
        c1.markdown(T.card_head("시·도 × 연휴 일자 히트맵"), unsafe_allow_html=True)
        h = c2.segmented_control("명절", HOLIDAYS, default="설날", key="f_heat", label_visibility="collapsed") or "설날"
        t, dl = sido_heat(ctx["df"], dy, h, m)
        cols = list(t.columns)
        head_row = "<div></div>" + "".join(f"<div class='hl'>{d_label(c)}</div>" for c in cols)
        rows_html = ""
        for name, r in t.iterrows():
            mx = r.max() or 1
            rows_html += f"<div class='rl'>{name}</div>"
            for c in cols:
                bg = mix(T.WASH, T.COLORS[h], r[c] / mx * 72)
                fg = text_on(bg, "#FFFFFF", T.INK_ON_LIGHT)
                rows_html += (f"<div class='c' title='{esc(f'{name} · {dl[c]} · {METRIC_NAMES[m]} {int(r[c])}{METRICS[m]}')}' "
                              f"style='background:{bg};color:{fg}'>{int(r[c])}</div>")
        st.markdown(f"<div class='tw'><div class='heat' style='grid-template-columns:52px repeat({len(cols)},minmax(46px,1fr))'>"
                    f"{head_row}{rows_html}</div></div>"
                    "<div class='meta' style='margin-top:12px'>행마다 가장 많은 날이 가장 진함 · 칸 숫자 = 선택 지표 · 호버 → 날짜 · 시·도 전체 기준</div>",
                    unsafe_allow_html=True)
        st.markdown("<span class='flag'>시간대 컬럼 없음 → 시·도로 대체</span>", unsafe_allow_html=True)


def composition_card(st, T, ctx, dy: int):
    rows = composition(ctx["rows"], dy)
    html_rows = ""
    for r in rows:
        mx = max(r["설날"], r["추석"], 1e-9) * 1.12
        html_rows += (f"<div class='crow'><div class='lab'>{r['라벨']}<small>{r['단위']}</small></div><div class='bars'>"
                      f"<div class='b'><div class='bar' style='width:{r['설날'] / mx * 85:.1f}%;background:{T.COLORS['설날']}'></div>{r['설날']:.{r['소수']}f}</div>"
                      f"<div class='b'><div class='bar' style='width:{r['추석'] / mx * 85:.1f}%;background:{T.COLORS['추석']}'></div>{r['추석']:.{r['소수']}f}</div>"
                      "</div></div>")
    with card(st, "d-comp"):
        head(st, T, "피해 구성 비교")
        st.markdown(f"<div class='cmp'>{html_rows}</div>"
                    "<div class='meta' style='margin-top:16px'>위 막대 = 설날 · 아래 막대 = 추석 · 행마다 큰 값 기준 길이</div>"
                    "<span class='flag' style='display:inline-block;margin-top:10px'>사고 유형 컬럼 없음 → 피해 정도로 대체</span>",
                    unsafe_allow_html=True)


def summary_card(st, T, ctx, dy: int):
    ys = year_summary(ctx["rows"], dy)
    S, C = ys["설날"], ys["추석"]
    w = "추석" if C["일평균"] >= S["일평균"] else "설날"
    p = pct(max(S["일평균"], C["일평균"]), min(S["일평균"], C["일평균"]))
    sg = lambda v: "—" if v is None or pd.isna(v) else f"{v:+.1f}%"
    fw = "추석" if C["치사율"] > S["치사율"] else "설날"
    body = (f"<h3>{dy}년은 <em>{w}</em>이 일평균 사고 기준 <em>{'—' if p is None else f'{p:.1f}%'}</em> 더 위험했다</h3><ul>"
            f"<li>일평균 사고 설날 <b>{S['일평균']:.1f}</b>건 vs 추석 <b>{C['일평균']:.1f}</b>건 (연휴 {S['일수']}일 · {C['일수']}일)</li>"
            f"<li>치사율 설날 {S['치사율']:.2f} vs 추석 {C['치사율']:.2f} — {fw}이 사고당 더 치명적</li>"
            f"<li>최다 사고일: 설 {S['최다일']} · 추석 {C['최다일']}</li>"
            f"<li>전년 대비 일평균 사고: 설날 {sg(S['전년'])} · 추석 {sg(C['전년'])}</li></ul>")
    with card(st, "d-summary"):
        head(st, T, "이 해의 한 줄 요약", meta=ctx["where"])
        st.markdown(f"<div class='summary'>{body}</div>"
                    "<div class='meta' style='margin-top:14px'>자료: 도로교통공단(KoROAD) 설날·추석 연휴기간 사고통계</div>",
                    unsafe_allow_html=True)


def sgg_top_card(st, T, ctx, dy: int | None = None):
    m = ctx["metric"]
    dy = ctx["year"] if dy is None else dy
    top = sgg_top(ctx["df"], dy, m, ctx["sido"])
    scope = "전국" if ctx["sido"] == "전체" else ctx["sido"]
    with card(st, "d-sgg"):
        head(st, T, "시군구 TOP 10", meta=f"{scope} · {ctx['PERIOD'].replace('~', '–') if dy is None else f'{dy}년'} · 설날+추석 합계 순")
        if top.empty or top["합계"].sum() == 0:
            st.info("이 조건에는 자료가 없습니다.")
            return
        fig = go.Figure()
        for h in HOLIDAYS:
            fig.add_bar(name=h, y=top["지역"], x=top[h], orientation="h", marker_color=T.COLORS[h],
                        hovertemplate=f"%{{y}}<br>{h} {METRIC_NAMES[m]} %{{x:,}}{METRICS[m]}<extra></extra>")
        fig.add_scatter(x=top["합계"], y=top["지역"], mode="text", text=[fmt(v) for v in top["합계"]],
                        textposition="middle right", textfont=dict(color=T.INK, size=12), showlegend=False, hoverinfo="skip")
        fig.update_layout(barmode="stack", bargap=0.35, legend=dict(traceorder="normal"))
        fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color=T.INK, size=13, family=T.FONT))
        fig.update_xaxes(showgrid=True, range=[0, top["합계"].max() * 1.12])
        st.plotly_chart(T.plotly_style(fig, 380, legend=True), use_container_width=True)


def weekday_card(st, T, ctx):
    m = ctx["metric"]
    wk = weekday_compare(ctx["rows"], m)
    with card(st, "d-week"):
        head(st, T, "요일별 하루 평균", meta=f"{ctx['PERIOD'].replace('~', '–')} 전체 기준")
        fig = go.Figure()
        for h in HOLIDAYS:
            t = wk[wk["명절"] == h]
            fig.add_bar(name=h, x=t["요일"].astype(str), y=t["값"], marker_color=T.COLORS[h], customdata=t["일수"],
                        hovertemplate=f"{h} %{{x}}요일<br>하루 평균 {METRIC_NAMES[m]} %{{y:,.1f}}<br>%{{customdata}}일 평균<extra></extra>")
        fig.update_layout(barmode="group", bargap=0.4)
        fig.update_xaxes(categoryorder="array", categoryarray=WEEKDAYS)
        st.plotly_chart(T.plotly_style(fig, 300, legend=True), use_container_width=True)
        st.caption(md("한 해의 연휴는 3~5일뿐이라 요일 비교는 5년을 합쳐서 봅니다. 요일마다 들어간 날 수가 달라 하루 평균으로 비교합니다."))


# ================================================================= 페이지 조립 (PDF 배치)
def overview(st, T, ctx):
    """전체 비교 (5년 합계만): 고정 요약 → 설날 VS 추석 → 연휴 일자별 5년 총계 → 핵심 인사이트."""
    c = with_scope(ctx, year=None)
    fixed_summary_card(st, T, c)
    left, mid, right = st.columns([5, 1.35, 5], vertical_alignment="center")
    with left:
        kpi_panel(st, T, c, "설날")
    with mid:
        vs_center(st, T, c)
    with right:
        kpi_panel(st, T, c, "추석")
    trend_totals_card(st, T, c)
    insights_row(st, T, c)


def detail(st, T, ctx):
    """연도 상세: (연도 선택) → 설날 vs 추석 연도별 비교 · 치사율 → 시군구 TOP 10."""
    YEARS = ctx["YEARS"]
    with card(st, "detail-filter"):
        y = st.segmented_control("연도", ["전체", *map(str, YEARS)], default="전체", key="f_year") or "전체"
    c = with_scope(ctx, year=None if y == "전체" else int(y))
    c1, c2 = st.columns([2.1, 1])
    with c1:
        holiday_main_card(st, T, c)
    with c2:
        rate_card(st, T, c)
    sgg_top_card(st, T, c)


def hotspots(st, T, ctx):
    """사고다발지점: (시도 · 시군구 선택) → 지도 · Top 6 → 전체 목록."""
    with card(st, "hs-filter"):
        f1, f2, _ = st.columns([1, 1, 2])
        sido = f1.selectbox("시도", ["전체"] + ctx["sido_list"], key="f_sido")
        sgg = f2.selectbox("시군구", ["전체"] + ctx["sgg_list"](sido), disabled=sido == "전체", key="f_sgg")
    c = with_scope(ctx, year=None, sido=sido, sgg=sgg)
    c1, c2 = st.columns([1.6, 1])
    with c1:
        hotspot_scatter_card(st, T, c)
    with c2:
        hotspot_top_card(st, T, c)
    hotspot_table_card(st, T, c)


# PDF에 없어 이번 배치에서 뺀 카드들 (코드는 남겨 두었습니다. 다시 쓰려면 위 함수에 넣으면 됩니다):
#   tiles_card(지역별 차이 타일 지도) · rank_card(시·도 순위) · memo_card(데이터 메모)
#   day_table_card(일자별 상세표) · heat_card(히트맵) · composition_card(피해 구성) · summary_card(연도 요약) · weekday_card(요일별)
