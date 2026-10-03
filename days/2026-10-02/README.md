---
day: 019
date: 2026-10-02
weekday: 금
week: 5
phase: 데이터 분석과 머신러닝/딥러닝
title: plotly 시각화 — 막대 · 원 · 히스토그램 · 박스 플롯 · 산점도 · 히트맵
tags: python, pandas, EDA, 시각화, plotly, px.line, px.bar, px.pie, px.histogram, px.box, px.scatter, px.imshow, groupby, reset_index, rename, value_counts, barmode, 이상치, IQR, 상관관계, 히트맵
---

# Day 019 · 2026-10-02 (금)

`데이터 분석과 머신러닝/딥러닝` · 5주차

> **한 줄 요약** — `tips.csv` 하나로 plotly express 의 7가지 그래프(직선 · 막대 · 원 · 히스토그램 · 박스 플롯 · 산점도 · 히트맵)를 그려 보며, **알고 싶은 질문에 맞는 그래프를 고르는 법**과 그래프용 표를 만드는 `groupby → reset_index → rename` 흐름을 익혔다.

📂 실습 노트북 → [`lecture/plotly_visualization.ipynb`](./lecture/plotly_visualization.ipynb) (필기 `Data_analysis03` 정리 + 교재 p.50~52 예제 추가)
📊 실습 데이터 → [`tips.csv`](./lecture/tips.csv) (244행)
📖 교재 `데이터분석` p.46~52 (EDA 개요와 직선 그래프는 [Day 018](../2026-10-01/) 에서 처음 정리)

---

## 0. 어떤 질문에 어떤 그래프?

| 알고 싶은 것 | 그래프 | plotly express | 교재 |
|-------------|--------|----------------|------|
| 값이 **어떻게 변해 가나** (추세) | 직선 그래프 | `px.line()` | p.46 |
| 범주별 **크기 비교** | 막대 그래프 | `px.bar()` | p.47 |
| 전체 중 **비율** | 원 그래프 | `px.pie()` | p.48 |
| 수치가 **어느 구간에 몰려 있나** (분포) | 히스토그램 | `px.histogram()` | p.49 |
| 분포 **요약 + 이상치** | 박스 플롯 | `px.box()` | p.50 |
| 두 수치 변수의 **관계** | 산점도 | `px.scatter()` | p.51 |
| 여러 변수 사이 **상관을 한눈에** | 히트맵 | `px.imshow()` | p.52 |

그래프를 고를 때는 컬럼이 **수치형**(`total_bill` · `tip` · `size`)인지 **범주형**(`sex` · `smoker` · `day` · `time`)인지가 먼저다.

---

## 1. 직선 그래프 — `px.line()` (p.46)

어제 그린 그래프를 다시 그리고, 이번에는 **HTML 파일로 저장**까지 했다.

```python
df_sorted = df.sort_values(by='total_bill')          # x 축으로 먼저 정렬!
fig1 = px.line(data_frame=df_sorted, x='total_bill', y='tip', color='time')
fig1.show()

fig1.write_html("line.html")                          # 브라우저에서 그대로 열리는 그래프
```

`write_html()` 로 만든 파일은 plotly.js 가 통째로 들어가 **약 4MB** 다. `include_plotlyjs="cdn"` 을 주면 plotly.js 를 인터넷에서 불러와 수 KB 로 줄어든다.

---

## 2. 막대 그래프 — `px.bar()` (p.47)

**범주별 수치 크기를 막대로 표현.**

| | 수직형 (기본) | 수평형 |
|---|---|---|
| `x` | **범주형** | **수치형** |
| `y` | **수치형** | **범주형** |
| `orientation` | `'v'` | `'h'` |

### 그래프용 표 만들기 — `groupby → reset_index → rename`

`px.bar()` 에는 **"요일 | 평균 요금"** 두 컬럼짜리 DataFrame 을 넘기는 게 편하다.

```python
day_mean      = df.groupby(by='day')['total_bill'].mean()     # ① Series (요일이 인덱스)
df_day_mean   = day_mean.reset_index()                         # ② 인덱스 → 컬럼, DataFrame
df_day_mean1  = df_day_mean.rename(columns={'total_bill': 'avg_total_bill'})   # ③ 이름 정리
```

### 순서 · 색 · 값 표시

```python
px.bar(df_day_mean1, x='day', y='avg_total_bill',
       category_orders={'day': ['Thur', 'Fri', 'Sat', 'Sun']},   # x 축 순서 지정
       color='day')                                              # 요일별 색

px.bar(df_day_mean1, x='avg_total_bill', y='day',                # 수평형 : x/y 역할 교체
       orientation='h', text_auto='.2f')                         # 막대에 값 표시
```

`groupby` 결과는 **알파벳 순**(Fri · Sat · Sun · Thur)이라 요일 순서로 보려면 `category_orders` 가 필요하다.

| 요일 | Thur | Fri | Sat | Sun |
|------|------|-----|-----|-----|
| 평균 요금 | 17.68 | 17.15 | 20.44 | **21.41** |

주말 손님이 더 많이 쓴다.

---

## 3. 원 그래프 — `px.pie()` (p.48)

**범주형 데이터의 비율을 부채꼴 조각으로.** `names` = 조각 이름(범주형), `values` = 조각 크기(수치형), `hole` = 가운데 구멍(0~1, 주면 **도넛**).

```python
sex_ratio    = df['sex'].value_counts(normalize=True)    # 개수 대신 비율
df_sex_ratio = sex_ratio.reset_index()                   # 컬럼 : sex | proportion

px.pie(df_sex_ratio, names='sex', values='proportion', hole=0.4)
```

남성 **64.3%** · 여성 **35.7%**. `proportion` 이라는 컬럼 이름은 **pandas 2.0 부터**라 버전이 낮으면 에러가 난다. `px.pie()` 는 개수를 넣어도 알아서 퍼센트로 그려 준다.

---

## 4. 히스토그램 — `px.histogram()` (p.49)

**수치형 데이터의 분포를 구간(bin)별 빈도 막대로.** 막대 그래프의 x 축은 **범주**, 히스토그램의 x 축은 **수치 구간**이라 막대가 서로 붙어 있다.

```python
px.histogram(df, x='total_bill')                  # 구간 개수 자동
px.histogram(df, x='total_bill', nbins=50)        # 구간 50개
px.histogram(df, y='tip')                         # y 에 주면 수평 히스토그램

fig.update_traces(marker_line_color='black', marker_line_width=1)   # 막대 경계선 일괄 추가
```

`color='time'` 으로 점심/저녁을 나누면, 두 그룹을 **어떻게 놓을지** `barmode` 로 고른다.

| `barmode` | 배치 | 언제 |
|-----------|------|------|
| `'relative'` (기본) | 위로 **쌓기** | 전체 분포 + 그룹 구성 |
| `'overlay'` + `opacity` | **겹치기** (반투명) | 두 분포의 **모양** 비교 |
| `'group'` | 구간마다 **나란히** | 구간별 개수 직접 비교 |

계산 금액은 **10~20달러에 가장 많이** 몰려 있고 고액 쪽으로 꼬리가 길다.

---

## 5. 박스 플롯 — `px.box()` (p.50)

**최솟값 · Q1 · 중앙값 · Q3 · 최댓값으로 분포를 요약하고 이상치를 찾는** 그래프. Day 018 `describe()` 의 `25%` · `50%` · `75%` 를 그림으로 그린 것이다.

```python
px.box(df, x='day', y='total_bill', color='time')     # 수직 : x 범주, y 수치
px.box(df, x='tip', y='smoker')                       # 수평 : 역할 교체
```

- **박스 길이 = IQR (Q3 − Q1)** — 가운데 50% 가 퍼진 정도
- 수염은 **IQR × 1.5** 까지. 그 밖은 **점(이상치)** 으로 찍힌다

그래프의 점이 정말 이상치인지 pandas 로 직접 계산해 봤다.

```python
q1, q3 = df['total_bill'].quantile(0.25), df['total_bill'].quantile(0.75)
iqr = q3 - q1
upper = q3 + 1.5 * iqr                  # 40.30
df[df['total_bill'] > upper]            # 9건
```

요일별 **중앙값**(일 19.63 > 토 18.24 > 목 16.20 > 금 15.38)이 평균보다 조금씩 작다 — 고액 손님 몇 명이 **평균을 위로 끌어올린** 것이다.

---

## 6. 산점도 — `px.scatter()` (p.51)

**두 변수 간의 상관관계를 점으로.** 행 하나가 점 하나다.

```python
px.scatter(df, x='total_bill', y='tip', color='time')
```

점이 오른쪽 위로 모인다 → **양의 상관(0.68)**.
직선 그래프는 같은 금액에 팁이 여러 개라 선이 위아래로 튀었는데, **두 수치 변수의 관계**는 순서를 잇지 않는 산점도가 맞는 도구다. 정렬도 필요 없다.

---

## 7. 히트맵 — `px.imshow()` (p.52)

**상관계수 크기를 색 농도로.** 변수가 많아도 어떤 쌍이 강하게 연결돼 있는지 한눈에 보인다.

```python
corr_matrix = df.corr(numeric_only=True)        # ① 상관 행렬

px.imshow(corr_matrix,
          text_auto='.2f',                      # 칸 안에 값 (소수 둘째 자리)
          color_continuous_scale='RdBu_r',      # 음수 파랑 ↔ 양수 빨강
          zmin=-1, zmax=1)                      # 색 범위를 -1 ~ 1 로 고정
```

|  | total_bill | tip | size |
|---|---|---|---|
| **total_bill** | 1.00 | **0.68** | 0.60 |
| **tip** | **0.68** | 1.00 | 0.49 |
| **size** | 0.60 | 0.49 | 1.00 |

> `zmin` · `zmax` 를 안 주면 색이 **데이터 값 범위**(0.49 ~ 1.0)에 맞춰 늘어나, 0.49 가 진한 파랑 — 마치 강한 음의 상관처럼 — 으로 보인다.

---

## 🔁 복습

**필기에서 고친 부분**
- [x] 절대 경로 `C:/Users/playdata2/work/tips.csv` → 상대 경로 `./tips.csv`
- [x] `warnings.filterwarnings('ignore')` 로 **모든 경고를 끄던 셀** 제거 — 문제가 생겨도 원인을 놓친다
- [x] `display(df)` · `display(df_sorted)` 로 244행을 다 찍던 것 → `head()`
- [x] 그래프 여러 개를 한 셀에서 연달아 그리던 것 → **한 셀에 그래프 하나**로 나눠 차이가 바로 보이게
- [x] `text_auto=True` → `text_auto='.2f'` (`17.682741935483875` → `17.68`)
- [x] 주석 "금액 구간별 **누적** 빈도수" → **빈도수**. 진짜 누적 히스토그램은 `cumulative=True` 가 따로 있다
- [x] `# nbins=50` 주석 처리돼 있던 것 → 따로 그려 자동 구간과 비교
- [x] `barmode` 기본값(`'relative'`, 쌓기) 설명, `proportion` 컬럼 이름의 pandas 버전 주의 추가
- [x] 교재 p.49 **수평 히스토그램**, p.50~52 **박스 플롯 · 산점도 · 히트맵** 예제가 필기에 없어 추가

**직접 해본 것**
- 같은 데이터로 `barmode` 세 가지(쌓기 · 겹치기 · 나란히)를 그려 비교
- 박스 플롯의 이상치를 `quantile()` 로 계산해 그래프의 점 개수(9개)와 맞춰 보기
- 요일별 평균(막대)과 중앙값(박스)을 비교해 이상치가 평균에 주는 영향 확인
- [Day 018](../2026-10-01/) 질문 "이런 데이터에는 산점도가 더 맞지 않은지" → 같은 데이터를 산점도로 그려 확인 ✔
- 히트맵에서 `zmin` · `zmax` 를 줄 때와 안 줄 때 색이 어떻게 달라지는지

**막혔던 부분 / 질문**
- [ ] `nbins` 를 몇으로 잡아야 분포가 제일 잘 보이는지 — 구간 개수를 정하는 기준(스터지스 공식 등)
- [ ] 박스 플롯의 IQR × 1.5 기준으로 걸린 값을 **지워야 하는지, 남겨야 하는지**
- [ ] `px.pie()` 는 범주가 많아지면 읽기 어려운데, 몇 개까지가 적당한지
- [ ] 산점도에 추세선을 같이 그리는 `trendline='ols'` 옵션 (statsmodels 필요)
- [ ] `write_html()` 파일과 `fig.write_image()` (PNG) 저장의 차이 — kaleido 설치

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [Plotly Express — Bar charts](https://plotly.com/python/bar-charts/)
- [Plotly Express — Pie charts](https://plotly.com/python/pie-charts/)
- [Plotly Express — Histograms](https://plotly.com/python/histograms/)
- [Plotly Express — Box plots](https://plotly.com/python/box-plots/)
- [Plotly Express — Scatter plots](https://plotly.com/python/line-and-scatter/)
- [Plotly — Heatmaps (`px.imshow`)](https://plotly.com/python/heatmaps/)
- [Plotly — Interactive HTML export (`write_html`)](https://plotly.com/python/interactive-html-export/)
- [`DataFrame.groupby()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)
- [`Series.value_counts()` 문서 — `normalize`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
