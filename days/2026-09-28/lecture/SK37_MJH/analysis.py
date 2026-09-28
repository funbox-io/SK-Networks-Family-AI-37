"""설날 vs 추석 연휴 교통사고 분석 함수 모음.

화면(app.py)과 분리해 두어서 streamlit 없이도 계산 결과를 확인할 수 있습니다.
    python analysis.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "holiday_accidents_2021_2025.csv"
GEO_PATH = DATA_DIR / "sido.geojson"
HOTSPOT_PATH = DATA_DIR / "hotspots_2021_2025.csv"
HOTSPOT_PERIOD = "2021~2025"  # 사고다발지역은 5년 묶음 자료 (연도·명절 구분 없음)

HOLIDAYS = ["설날", "추석"]
METRICS = {"사고": "건", "사망": "명", "부상": "명", "중상": "명"}
METRIC_NAMES = {"사고": "사고 건수", "사망": "사망자", "부상": "부상자", "중상": "중상자"}

# 명절 당일(음력 1월 1일 · 8월 15일). 연휴 일자를 D-1 / D / D+1 로 셀 때 기준입니다.
HOLIDAY_D = {
    (2021, "설날"): "2021-02-12", (2021, "추석"): "2021-09-21",
    (2022, "설날"): "2022-02-01", (2022, "추석"): "2022-09-10",
    (2023, "설날"): "2023-01-22", (2023, "추석"): "2023-09-29",
    (2024, "설날"): "2024-02-10", (2024, "추석"): "2024-09-17",
    (2025, "설날"): "2025-01-29", (2025, "추석"): "2025-10-06",
}
WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]
VALUE_COLS = ["사고", "사망", "중상", "부상"]


def josa(word: str, pair: str = "이가") -> str:
    """받침 유무에 맞는 조사를 붙입니다. pair: '이가', '은는', '을를', '으로로'."""
    code = ord(word[-1]) - 0xAC00
    has_final = 0 <= code <= 11171 and code % 28 != 0
    if pair == "으로로":
        return word + ("으로" if has_final and code % 28 != 8 else "로")
    return word + (pair[0] if has_final else pair[1])


# ---------------------------------------------------------------- 불러오기
def load_data(path: Path | str = CSV_PATH) -> pd.DataFrame:
    """CSV를 읽고 '일차'(연휴 몇째 날)와 '연휴일수' 컬럼을 붙입니다.

    컬럼: 연도, 명절, 날짜, 요일, 시도, 시군구, 사고, 사망, 중상, 부상
    - 시도 == '전국'  : 전국 합계 행
    - 시군구 == '소계': 시도 합계 행
    - 부상에는 중상이 포함되어 있으므로 부상 + 중상을 더하면 안 됩니다.
    """
    return prepare_accidents(pd.read_csv(path, encoding="utf-8-sig"))


def prepare_accidents(df: pd.DataFrame) -> pd.DataFrame:
    """사고통계 표(CSV든 MySQL이든)에 날짜 형식 · 일차 · 연휴일수 · D(명절 당일 기준)를 붙입니다."""
    df = df.copy()
    df["날짜"] = pd.to_datetime(df["날짜"])
    for c in ["연도", *VALUE_COLS]:
        df[c] = pd.to_numeric(df[c]).astype(int)
    days = (
        df[["연도", "명절", "날짜"]]
        .drop_duplicates()
        .sort_values("날짜")
        .assign(일차=lambda d: d.groupby(["연도", "명절"]).cumcount() + 1)
    )
    days["연휴일수"] = days.groupby(["연도", "명절"])["일차"].transform("max")
    dday = pd.to_datetime(pd.Series([HOLIDAY_D.get((y, h)) for y, h in zip(days["연도"], days["명절"])], index=days.index))
    days["D"] = (days["날짜"] - dday).dt.days.astype("Int64")
    return df.merge(days, on=["연도", "명절", "날짜"], how="left")


def d_label(off: int) -> str:
    """0 → 'D', -1 → 'D-1', 2 → 'D+2'."""
    off = int(off)
    return "D" if off == 0 else f"D{off:+d}"


def load_hotspots(path: Path | str = HOTSPOT_PATH) -> pd.DataFrame:
    """연휴기간 사고다발지역 (도로교통공단, 2021~2025 묶음).

    컬럼: 지점명, 시도, 시군구, 사고, 사상자, 사망, 중상, 경상, 부상신고, 경도, 위도
    사고통계는 '용인시'처럼 시 단위, 사고다발지는 '용인시처인구'처럼 구 단위라서
    필터용으로 시 이름만 남긴 '시군구_기준' 컬럼을 붙입니다.
    """
    return prepare_hotspots(pd.read_csv(path, encoding="utf-8-sig"))


def prepare_hotspots(hs: pd.DataFrame) -> pd.DataFrame:
    """사고다발지 표(CSV든 MySQL이든)에 '시군구_기준'을 붙이고 숫자 형식을 맞춥니다."""
    hs = hs.copy()
    for c in ["사고", "사상자", "사망", "중상", "경상", "부상신고"]:
        hs[c] = pd.to_numeric(hs[c]).astype(int)
    hs["경도"], hs["위도"] = pd.to_numeric(hs["경도"]).astype(float), pd.to_numeric(hs["위도"]).astype(float)
    hs["시군구_기준"] = hs["시군구"].str.replace(r"^(.+?시).+구$", r"\1", regex=True)
    return hs


def hotspots_in(hs: pd.DataFrame, sido: str = "전체", sgg: str = "전체") -> pd.DataFrame:
    if sido == "전체":
        return hs
    hs = hs[hs["시도"] == sido]
    return hs if sgg == "전체" else hs[hs["시군구_기준"] == sgg]


def hotspot_values(hs: pd.DataFrame, metric: str) -> pd.Series:
    """사고다발지의 지표별 값. 사고=사고 건수, 부상=사상자−사망(중상+경상+부상신고), 사망=사망자."""
    if metric == "사고":
        return hs["사고"]
    if metric == "부상":
        return hs["사상자"] - hs["사망"]
    if metric == "중상":
        return hs["중상"]
    return hs["사망"]


def hotspot_area_stats(df: pd.DataFrame, hs: pd.DataFrame, year: int | None, metric: str) -> pd.DataFrame:
    """사고다발지 지점마다, 그 지점이 속한 시군구의 선택 연도 연휴 수치(설날·추석)를 붙입니다.

    사고다발지 자료에는 연도 구분이 없어서, 연도 필터는 '소속 시군구'의 연휴 사고통계로 연결합니다.
    (용인시처인구 → 용인시처럼 '시군구_기준'으로 사고통계의 시군구와 맞춥니다.)
    """
    r = filter_years(df[(df["시도"] != "전국") & (df["시군구"] != "소계")], year)
    t = (
        r.pivot_table(index=["시도", "시군구"], columns="명절", values=metric, aggfunc="sum")
        .reindex(columns=HOLIDAYS)
        .fillna(0)
        .rename(columns={"설날": "지역_설날", "추석": "지역_추석"})
        .reset_index()
        .rename(columns={"시군구": "시군구_기준"})
    )
    out = hs.merge(t, on=["시도", "시군구_기준"], how="left")
    out["지역_합계"] = out["지역_설날"] + out["지역_추석"]
    return out


def region_rows(df: pd.DataFrame, sido: str = "전체", sgg: str = "전체") -> pd.DataFrame:
    """선택한 지역의 행만 돌려줍니다 (합계 행을 사용해 이중 집계를 막습니다)."""
    if sido == "전체":
        return df[df["시도"] == "전국"]
    if sgg == "전체":
        return df[(df["시도"] == sido) & (df["시군구"] == "소계")]
    return df[(df["시도"] == sido) & (df["시군구"] == sgg)]


def sido_list(df: pd.DataFrame) -> list[str]:
    return sorted(s for s in df["시도"].unique() if s != "전국")


def sgg_list(df: pd.DataFrame, sido: str) -> list[str]:
    if sido == "전체":
        return []
    return sorted(df.loc[(df["시도"] == sido) & (df["시군구"] != "소계"), "시군구"].unique())


def filter_years(rows: pd.DataFrame, year: int | None) -> pd.DataFrame:
    return rows if year is None else rows[rows["연도"] == year]


# ---------------------------------------------------------------- 요약 지표
def summarize(rows: pd.DataFrame) -> pd.DataFrame:
    """명절별 합계, 연휴 일수, 일평균, 치사율을 계산합니다.

    치사율 = 사망 ÷ 사고 × 100 (사고 100건당 사망자)
    """
    g = rows.groupby("명절")
    out = g[VALUE_COLS].sum()
    out["일수"] = g["날짜"].nunique()  # 날짜에 연도가 들어 있어 여러 해를 합쳐도 겹치지 않음
    for m in METRICS:
        out[f"{m}_일평균"] = out[m] / out["일수"]
    out["치사율"] = (out["사망"] / out["사고"].where(out["사고"] > 0) * 100).fillna(0)
    return out.reindex(HOLIDAYS).fillna(0)


def yearly(rows: pd.DataFrame, metric: str, per_day: bool) -> pd.DataFrame:
    """연도 × 명절 표. per_day=True면 연휴 일수로 나눈 일평균."""
    g = rows.groupby(["연도", "명절"])
    t = g[metric].sum().to_frame("값")
    t["일수"] = g["날짜"].nunique()
    if per_day:
        t["값"] = t["값"] / t["일수"]
    return t.reset_index()


def verdict(summary: pd.DataFrame, metric: str, per_day: bool) -> dict:
    """더 위험한 명절 판정. 두 값이 같으면 winner=None."""
    col = f"{metric}_일평균" if per_day else metric
    a, b = summary.loc["설날", col], summary.loc["추석", col]
    if a == b:
        return {"winner": None, "ratio": 0.0, "설날": a, "추석": b}
    hi, lo = ("추석", "설날") if b > a else ("설날", "추석")
    hv, lv = max(a, b), min(a, b)
    ratio = (hv / lv - 1) * 100 if lv else float("inf")
    return {"winner": hi, "loser": lo, "ratio": ratio, "설날": a, "추석": b}


def previous_year_summary(rows: pd.DataFrame, year: int | None) -> pd.DataFrame | None:
    if year is None or year - 1 not in set(rows["연도"]):
        return None
    return summarize(rows[rows["연도"] == year - 1])


# ---------------------------------------------------------------- 일자별
def day_trend(rows: pd.DataFrame, metric: str) -> pd.DataFrame:
    """연휴 일차별 값. 여러 해가 섞이면 같은 일차끼리 평균을 냅니다."""
    per_day = rows.groupby(["연도", "명절", "일차", "날짜", "요일"])[metric].sum().reset_index()
    t = per_day.groupby(["명절", "일차"]).agg(값=(metric, "mean"), 연도수=("연도", "nunique")).reset_index()
    t["일차명"] = t["일차"].astype(str) + "일차"
    return t


def day_table(rows: pd.DataFrame, year: int, metric: str) -> pd.DataFrame:
    """연도 상세 화면의 일자별 표 (일차 기준으로 설날·추석을 나란히)."""
    r = rows[rows["연도"] == year]
    d = r.groupby(["명절", "일차", "날짜", "요일"])[metric].sum().reset_index()
    d["날짜(요일)"] = d["날짜"].dt.strftime("%m.%d") + " (" + d["요일"] + ")"
    wide = None
    for h in HOLIDAYS:
        part = d[d["명절"] == h][["일차", "날짜(요일)", metric]].rename(
            columns={"날짜(요일)": f"{h} 날짜", metric: f"{h} {metric}"}
        )
        wide = part if wide is None else wide.merge(part, on="일차", how="outer")
    wide = wide.sort_values("일차")
    for h in HOLIDAYS:
        wide[f"{h} {metric}"] = wide[f"{h} {metric}"].astype("Int64")
        wide[f"{h} 날짜"] = wide[f"{h} 날짜"].fillna("–")
    wide["일차"] = wide["일차"].astype(int).astype(str) + "일차"
    return wide.reset_index(drop=True)


# ---------------------------------------------------------------- 지역별
def sido_compare(df: pd.DataFrame, year: int | None, metric: str, per_day: bool) -> pd.DataFrame:
    """시도별 설날·추석 값과 차이(추석 − 설날)."""
    r = filter_years(df[(df["시도"] != "전국") & (df["시군구"] == "소계")], year)
    t = r.pivot_table(index="시도", columns="명절", values=metric, aggfunc="sum").reindex(columns=HOLIDAYS).fillna(0)
    if per_day:
        days = filter_years(df[df["시도"] == "전국"], year).groupby("명절")["날짜"].nunique()
        for h in HOLIDAYS:
            t[h] = t[h] / days.get(h, 1)
    t["차이"] = t["추석"] - t["설날"]
    return t.reset_index().sort_values("차이", ascending=False).reset_index(drop=True)


def sgg_top(df: pd.DataFrame, year: int | None, metric: str, sido: str = "전체", n: int = 10) -> pd.DataFrame:
    """시군구 TOP n (설날+추석 합계 기준)."""
    r = filter_years(df[(df["시도"] != "전국") & (df["시군구"] != "소계")], year)
    if sido != "전체":
        r = r[r["시도"] == sido]
    t = r.pivot_table(index=["시도", "시군구"], columns="명절", values=metric, aggfunc="sum").reindex(columns=HOLIDAYS).fillna(0)
    t["합계"] = t.sum(axis=1)
    t = t.sort_values("합계", ascending=False).head(n).reset_index()
    t["지역"] = t["시도"] + " " + t["시군구"]
    return t


def weekday_compare(rows: pd.DataFrame, metric: str) -> pd.DataFrame:
    """요일별 하루 평균 (요일마다 들어간 날 수가 달라 평균으로 비교)."""
    d = rows.groupby(["명절", "날짜", "요일"])[metric].sum().reset_index()
    t = d.groupby(["명절", "요일"]).agg(값=(metric, "mean"), 일수=("날짜", "nunique")).reset_index()
    t["요일"] = pd.Categorical(t["요일"], WEEKDAYS, ordered=True)
    return t.sort_values(["요일", "명절"])


# ---------------------------------------------------------------- 인사이트
def insights(rows: pd.DataFrame, metric: str) -> list[dict]:
    """인사이트 카드 3장 (보정 효과, 가장 위험한 날, 추세)."""
    unit = METRICS[metric]
    cards = []

    # 1. 총량 vs 일평균: 판정이 뒤집히는 해
    tot = yearly(rows, metric, per_day=False).pivot(index="연도", columns="명절", values="값")
    avg = yearly(rows, metric, per_day=True).pivot(index="연도", columns="명절", values="값")
    win_tot = (tot["추석"] > tot["설날"]).map({True: "추석", False: "설날"})
    win_avg = (avg["추석"] > avg["설날"]).map({True: "추석", False: "설날"})
    flips = [int(y) for y in tot.index if win_tot[y] != win_avg[y]]
    chuseok_years = int((win_avg == "추석").sum())
    body = f"{len(avg)}년 중 {chuseok_years}년은 일평균 {josa(metric)} 추석에 더 많았습니다."
    if flips:
        y = flips[0]
        body += (f" {y}년은 총량으로는 {win_tot[y]}({tot.loc[y, win_tot[y]]:,.0f}{unit})이 많지만 "
                 f"연휴 길이를 보정하면 {josa(win_avg[y])} 더 많습니다.")
    cards.append({"title": "연휴 길이를 보정하면", "body": body})

    # 2. 가장 위험한 하루 (명절 당일 D 기준)
    d = rows.groupby(["연도", "명절", "날짜", "요일", "D"])[metric].sum().reset_index()
    top = d.loc[d[metric].idxmax()]
    by_d = day_trend_d(rows, metric)
    n_years = rows["연도"].nunique()
    common = by_d.groupby("D").filter(lambda t: (t["연도수"] == n_years).all())  # 모든 해에 있는 D만
    peak = common.groupby("D")["값"].mean().idxmax()
    rng = f"{d_label(common['D'].min())}~{d_label(common['D'].max())}"
    cards.append({
        "title": "가장 위험한 하루",
        "body": (f"{top['연도']}년 {top['명절']} {top['날짜']:%m월 %d일}({top['요일']}), "
                 f"명절 {d_label(top['D'])}에 {metric} {josa(f'{top[metric]:,.0f}{unit}')} 나와 가장 많았습니다. "
                 f"모든 해에 있는 {rng}만 평균하면 가장 위험한 날은 {d_label(peak)}입니다."),
    })

    # 3. 추세
    years = sorted(avg.index)
    first, last = years[0], years[-1]
    parts = []
    for h in HOLIDAYS:
        a, b = avg.loc[first, h], avg.loc[last, h]
        parts.append(f"{h} {(b / a - 1) * 100:+.0f}%" if a else f"{h} {first}년 0이라 비교 불가")
    cards.append({
        "title": f"{first} → {last} 추세",
        "body": f"일평균 {metric} 변화: " + ", ".join(parts) + ".",
    })
    return cards


if __name__ == "__main__":
    df = load_data()
    nat = region_rows(df)
    s = summarize(nat)
    print(s[["사고", "사망", "부상", "일수", "사고_일평균", "치사율"]].round(2))
    print(verdict(s, "사고", per_day=True))
    print(yearly(nat, "부상", per_day=True).round(1))
    print(day_table(nat, 2025, "사고"))
    print(sido_compare(df, None, "사고", per_day=True).head())
    print(sgg_top(df, 2025, "사고"))
    print(weekday_compare(nat, "사고"))
    for c in insights(nat, "부상"):
        print("-", c["title"], ":", c["body"])


# ---------------------------------------------------------------- 명절 당일(D) 기준 화면용
def day_trend_d(rows: pd.DataFrame, metric: str) -> pd.DataFrame:
    """명절 당일(D) 기준 일자별 값. 여러 해면 같은 D끼리 평균, 날짜 목록도 함께."""
    per_day = rows.groupby(["연도", "명절", "D", "날짜", "요일"])[metric].sum().reset_index()
    per_day["날짜표시"] = per_day["날짜"].dt.strftime("%m.%d") + "(" + per_day["요일"] + ")"
    t = per_day.groupby(["명절", "D"]).agg(값=(metric, "mean"), 연도수=("연도", "nunique"),
                                         날짜들=("날짜표시", lambda x: ", ".join(x))).reset_index()
    t["라벨"] = t["D"].map(d_label)
    return t.sort_values(["명절", "D"])


def period_text(rows: pd.DataFrame, year: int | None, holiday: str) -> str:
    """KPI 머리글의 기간 표시: [02.11–02.13 · 3일] 또는 [5회 · 17일]."""
    r = filter_years(rows, year)
    r = r[r["명절"] == holiday]
    dates = sorted(r["날짜"].unique())
    if not dates:
        return "[자료 없음]"
    if year is None:
        return f"[{r['연도'].nunique()}회 · {len(dates)}일]"
    return f"[{pd.Timestamp(dates[0]):%m.%d}–{pd.Timestamp(dates[-1]):%m.%d} · {len(dates)}일]"


def day_table_d(rows: pd.DataFrame, year: int, metric: str) -> pd.DataFrame:
    """연도 상세의 일자별 표 (D 기준으로 설날·추석을 나란히)."""
    r = rows[rows["연도"] == year]
    d = r.groupby(["명절", "D", "날짜", "요일"])[metric].sum().reset_index()
    d["날짜표시"] = d["날짜"].dt.strftime("%m.%d") + " (" + d["요일"] + ")"
    out = pd.DataFrame({"D": sorted(d["D"].unique())})
    for h in HOLIDAYS:
        part = d[d["명절"] == h][["D", "날짜표시", metric]].rename(columns={"날짜표시": f"{h}_날짜", metric: f"{h}_값"})
        out = out.merge(part, on="D", how="left")
    out["라벨"] = out["D"].map(d_label)
    return out


def sido_heat(df: pd.DataFrame, year: int, holiday: str, metric: str) -> pd.DataFrame:
    """시·도 × 연휴 일자(D) 히트맵용 표. 행 = 시도(합계 큰 순), 열 = D."""
    r = df[(df["시도"] != "전국") & (df["시군구"] == "소계") & (df["연도"] == year) & (df["명절"] == holiday)]
    t = r.pivot_table(index="시도", columns="D", values=metric, aggfunc="sum").fillna(0)
    t = t.loc[t.sum(axis=1).sort_values(ascending=False).index]
    dates = r.drop_duplicates("D").set_index("D")["날짜"].dt.strftime("%m.%d").to_dict()
    dows = r.drop_duplicates("D").set_index("D")["요일"].to_dict()
    return t, {k: f"{dates[k]}({dows[k]})" for k in dates}


def composition(rows: pd.DataFrame, year: int) -> list[dict]:
    """피해 구성 비교: 일평균 사고, 사고 100건당 부상·중상·사망."""
    r = rows[rows["연도"] == year]
    out = []
    specs = [
        ("일평균 사고", "건 / 일", lambda d: d["사고"].sum() / d["날짜"].nunique(), 1),
        ("100건당 부상자", "명", lambda d: d["부상"].sum() / d["사고"].sum() * 100, 1),
        ("100건당 중상자", "명", lambda d: d["중상"].sum() / d["사고"].sum() * 100, 1),
        ("100건당 사망자", "명 · 치사율", lambda d: d["사망"].sum() / d["사고"].sum() * 100, 2),
    ]
    for label, unit, fn, dp in specs:
        vals = {}
        for h in HOLIDAYS:
            d = r[r["명절"] == h]
            vals[h] = fn(d) if len(d) and d["사고"].sum() else 0.0
        out.append({"라벨": label, "단위": unit, "소수": dp, **vals})
    return out


def sido_diff(df: pd.DataFrame, year: int | None, metric: str, per_day: bool) -> pd.DataFrame:
    """타일 지도 · 순위표용: 시도별 설날, 추석, 차이, 증감률(%)."""
    t = sido_compare(df, year, metric, per_day)
    t["증감률"] = (t["차이"] / t["설날"].where(t["설날"] > 0) * 100)
    return t


# 타일 지도 배치 (열, 행) — 첨부 HTML과 같은 배치
SIDO_TILES = [("인천", 0, 0), ("서울", 1, 0), ("경기", 2, 0), ("강원", 3, 0), ("충남", 0, 1), ("세종", 1, 1),
              ("충북", 2, 1), ("경북", 3, 1), ("전북", 0, 2), ("대전", 1, 2), ("대구", 2, 2), ("울산", 3, 2),
              ("광주", 0, 3), ("전남", 1, 3), ("경남", 2, 3), ("부산", 3, 3), ("제주", 0, 4)]


def year_summary(rows: pd.DataFrame, year: int) -> dict:
    """연도 상세의 한 줄 요약용 수치 (일평균 사고 기준)."""
    r = rows[rows["연도"] == year]
    out = {}
    for h in HOLIDAYS:
        d = r[r["명절"] == h]
        daily = d.groupby(["날짜", "요일"])["사고"].sum().reset_index()
        top = daily.loc[daily["사고"].idxmax()] if len(daily) else None
        out[h] = {
            "일수": d["날짜"].nunique(),
            "일평균": d["사고"].sum() / max(d["날짜"].nunique(), 1),
            "치사율": d["사망"].sum() / d["사고"].sum() * 100 if d["사고"].sum() else 0.0,
            "최다일": f"{top['날짜']:%m.%d}({top['요일']}) {int(top['사고']):,}건" if top is not None else "–",
        }
    prev = rows[rows["연도"] == year - 1]
    for h in HOLIDAYS:
        p = prev[prev["명절"] == h]
        out[h]["전년"] = (out[h]["일평균"] / (p["사고"].sum() / p["날짜"].nunique()) - 1) * 100 if len(p) else None
    return out


def overall_summary(df: pd.DataFrame) -> dict:
    """맨 위 고정 요약: 필터와 상관없이 전국 · 전체 기간 · 사고 기준.

    일평균 사고, 치사율, 최다 사고일, 5년 중 추석이 더 많았던 해 수를 돌려줍니다.
    """
    nat = df[df["시도"] == "전국"]
    years = sorted(nat["연도"].unique())
    out = {"기간": f"{years[0]}–{years[-1]}", "연수": len(years)}
    for h in HOLIDAYS:
        d = nat[nat["명절"] == h]
        daily = d.groupby(["날짜", "요일"])["사고"].sum().reset_index()
        top = daily.loc[daily["사고"].idxmax()]
        out[h] = {
            "일수": d["날짜"].nunique(),
            "일평균": d["사고"].sum() / d["날짜"].nunique(),
            "치사율": d["사망"].sum() / d["사고"].sum() * 100,
            "최다일": f"{top['날짜']:%Y.%m.%d}({top['요일']}) {int(top['사고']):,}건",
        }
    per_year = nat.groupby(["연도", "명절"]).agg(합=("사고", "sum"), 일=("날짜", "nunique"))
    avg = (per_year["합"] / per_year["일"]).unstack()
    out["추석우세연수"] = int((avg["추석"] > avg["설날"]).sum())
    return out


def fixed_insights(df: pd.DataFrame) -> list[dict]:
    """전체 비교의 핵심 인사이트 3장 — 전국 · 2021~2025 전체 · 사고 건수 기준 (필터와 무관).

    1. 추석이 더 위험하다      : 연도별 일평균 사고 비교 + 총량과 일평균 판정이 뒤집힌 해
    2. 가장 위험한 날          : 명절 당일 기준 D별 5년 사고 총계 최댓값
    3. 사고가 가장 많았던 지역 : 시도별 5년 사고 총계 최댓값
    """
    nat = df[df["시도"] == "전국"]
    years = sorted(nat["연도"].unique())
    y0, y1, n = years[0], years[-1], len(years)
    g = nat.groupby(["연도", "명절"]).agg(합=("사고", "sum"), 일=("날짜", "nunique"))
    tot, avg = g["합"].unstack(), (g["합"] / g["일"]).unstack()
    c_years = int((avg["추석"] > avg["설날"]).sum())
    w = "추석" if c_years * 2 >= n else "설날"
    if c_years == n:
        body1 = f"{y0}년부터 {y1}년까지 모든 연도에서 추석 일평균 사고가 더 많았습니다."
    else:
        body1 = f"{y0}년부터 {y1}년까지 {n}년 중 {c_years if w == '추석' else n - c_years}년은 {w} 일평균 사고가 더 많았습니다."
    flips = [y for y in years if (tot.loc[y, "추석"] > tot.loc[y, "설날"]) != (avg.loc[y, "추석"] > avg.loc[y, "설날"])]
    for y in flips:
        big = "설날" if tot.loc[y, "설날"] > tot.loc[y, "추석"] else "추석"
        small = "추석" if big == "설날" else "설날"
        body1 += (f" {y}년은 예외적으로 사고 총량이 {big}({tot.loc[y, big]:,}건)이 많았으나, "
                  f"연휴 길이를 보정할 경우 {small}이 더 위험했습니다.")

    by_d = nat.groupby("D")["사고"].sum()
    top_d = int(by_d.idxmax())
    name = {-1: "명절 전날", 0: "명절 당일", 1: "명절 다음 날"}.get(top_d, d_label(top_d))
    body2 = (f"{y0}년부터 {y1}년까지 총계 데이터에 따르면, 연휴 중 가장 위험한 날은 "
             f"{name}({d_label(top_d)}, {by_d.max():,}건)로 나타났습니다.")

    sido = df[(df["시도"] != "전국") & (df["시군구"] == "소계")].groupby("시도")["사고"].sum()
    top_s = sido.idxmax()
    body3 = f"{n}년간 사고가 가장 많이 발생한 지역은 {top_s}({sido.max():,}건)이었습니다."

    return [
        {"title": f"{w}이 더 위험하다", "body": body1},
        {"title": f"가장 위험한 날은 {name}", "body": body2},
        {"title": f"사고가 가장 많았던 지역은 {top_s}", "body": body3},
    ]


def d_totals(rows: pd.DataFrame, metric: str) -> pd.DataFrame:
    """명절 당일(D) 기준 일자별 5년 총계 (평균이 아니라 합계). 해당 D가 있었던 연도 수와 날짜 목록도 함께."""
    per_day = rows.groupby(["연도", "명절", "D", "날짜", "요일"])[metric].sum().reset_index()
    per_day["날짜표시"] = per_day["연도"].astype(str).str[2:] + "." + per_day["날짜"].dt.strftime("%m.%d")
    t = per_day.groupby(["명절", "D"]).agg(값=(metric, "sum"), 연도수=("연도", "nunique"),
                                         날짜들=("날짜표시", lambda x: ", ".join(x))).reset_index()
    t["라벨"] = t["D"].map(d_label)
    return t.sort_values(["명절", "D"])
