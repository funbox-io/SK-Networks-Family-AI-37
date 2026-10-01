---
day: 018
date: 2026-10-01
weekday: 목
week: 5
phase: 데이터 분석과 머신러닝/딥러닝
title: 데이터 탐색 — 요약 통계량 · 상관관계 분석 · plotly 직선 그래프(EDA)
tags: python, pandas, 데이터탐색, describe, 요약통계량, mean, median, quantile, std, 표준편차, 상관관계, corr, 피어슨, EDA, 시각화, plotly, px.line, matplotlib, seaborn
---

# Day 018 · 2026-10-01 (목)

`데이터 분석과 머신러닝/딥러닝` · 5주차

> **한 줄 요약** — `describe()` 로 데이터의 중심과 퍼짐을 숫자로 요약하고, `corr()` 로 두 변수가 같이 움직이는지 재고, `plotly` 직선 그래프로 눈으로 확인하는 데이터 탐색의 세 단계를 익혔다.

📂 실습 노트북 → [`lecture/statistics_eda.ipynb`](./lecture/statistics_eda.ipynb) (필기 3개 `Data_analysis02` · `통계분석연습` · `plotly` 를 하나로 정리)
📊 실습 데이터 → [`ad_performance.csv`](./lecture/ad_performance.csv) (5,000행) · [`weather.csv`](./lecture/weather.csv) (100,000행) · [`tips.csv`](./lecture/tips.csv) (244행)
📖 교재 `데이터분석` p.34~46 (p.33 비교/논리 연산자는 [Day 017](../2026-09-30/) 에서 정리)

---

## 0. 데이터 탐색이란

전처리로 데이터를 손봤다면, 이제 **데이터가 어떻게 생겼는지 파악**할 차례다.

| 단계 | 질문 | 도구 |
|------|------|------|
| 통계로 요약하기 | 값들이 **어디에 모여 있고 얼마나 퍼져 있나?** | `describe()` · `mean()` · `std()` … |
| 상관관계 분석 | 두 값이 **같이 움직이나?** | `corr()` |
| 탐색적 데이터 분석(EDA) | **눈으로 보면** 어떤 모양인가? | `plotly.express` |

---

## 1. 통계로 요약하기 — `df.describe()`

**데이터 분포의 특징을 나타내는 통계량.** 전체적인 특징과 분포를 **빠르게** 파악할 때 쓴다.

| 행 이름 | 뜻 |
|---------|-----|
| `count` | 데이터 개수 (**NaN 제외**) |
| `mean` | 평균값 |
| `std` | 표준편차 (데이터가 퍼져 있는 정도) |
| `min` · `max` | 최솟값 · 최댓값 |
| `25%` · `50%` · `75%` | 1 사분위수 · **중앙값** · 3 사분위수 |

`describe()` 의 결과도 **DataFrame** 이라 `df.loc[행, 열]` 로 값 하나를 꺼낼 수 있다. 같은 값을 컬럼 메서드로 바로 구해도 된다.

```python
df_state = df.describe()

df_state.loc['mean', 'Cost']        # 방법 1 : 요약 통계량에서 꺼내기
df['Cost'].mean()                   # 방법 2 : 메서드로 바로
```

| 교재 질문 | 요약 통계량 | 메서드 | 광고 데이터 결과 |
|-----------|-------------|--------|------------------|
| 광고 하나에 평균 얼마를 쓰나? (p.35) | `loc['mean','Cost']` | `mean()` | **173,572.5원** |
| 매출의 최소는? (p.36) | `loc['min','Revenue']` | `min()` | 100,440원 |
| 매출의 최대는? (p.36) | `loc['max','Revenue']` | `max()` | 1,999,273원 |
| 매출의 중앙값은? (p.37) | `loc['50%','Revenue']` | `median()` · `quantile(0.5)` | **1,078,122.5원** |
| 매출의 표준편차는? (p.38) | `loc['std','Revenue']` | `std()` | 544,216.9원 |

매출 평균(1,062,507원)이 중앙값보다 **조금 작다** — 작은 값 쪽으로 꼬리가 살짝 길다는 뜻이다.

### 표준편차 읽는 법

**데이터들이 평균값에서 평균적으로 얼마나 떨어져 있는가?** — 데이터의 일관성(변동성)을 보여 준다.

| 표준편차가 | 뜻 |
|-----------|-----|
| **작다** | 평균 주변에 옹기종기 모여 있다 → 성과가 꾸준하고 **예측 가능** |
| **크다** | 평균에서 멀리 넓게 흩어져 있다 → 성과가 들쭉날쭉하고 **예측하기 힘듦** |

광고 매출의 표준편차는 평균의 **51%** 나 된다. 캠페인마다 매출이 꽤 들쭉날쭉하다.

> ⚠️ **행 개수 세기 함정** — `len(df.describe())` 는 **8** 이다. describe 표의 통계량 8가지를 센 것이다.
> 실제 데이터 행 수는 `len(df)` (5,000), NaN 을 뺀 개수는 `describe().loc['count', '컬럼']` 이다.

---

## 2. 연습 — 날씨 데이터 (`통계분석연습`)

기상청 날씨 데이터 100,000행으로 같은 방법을 반복했다. 각 문제를 방법 1·2로 풀어 결과가 같은지 확인했다.

```python
w_state.loc['mean', 'temp']   == df_w['temp'].mean()      # 16.9
w_state.loc['min',  'hum']    == df_w['hum'].min()        # 17
w_state.loc['max',  'hum']    == df_w['hum'].max()        # 100
w_state.loc['50%',  'atm']    == df_w['atm'].median()     # 1006.0
w_state.loc['std',  'speed']  == df_w['speed'].std()      # 1.92
```

---

## 3. 상관관계 분석

**두 변수 사이에 연관성이 있는지, 있다면 얼마나 강한지** 측정하는 분석 방법. 예) 광고비 지출이 매출액 증가에 어느 정도 영향이 있는지.

**상관계수(피어슨)** — 두 변수 사이의 **선형 관계 정도**를 **-1 ~ +1** 로 나타낸 것.

| 상관계수 | 뜻 |
|---------|-----|
| **+1 에 가까움** | 양의 상관 — 한쪽이 오르면 다른 쪽도 **오른다** |
| **0 에 가까움** | 선형 관계가 거의 없다 |
| **-1 에 가까움** | 음의 상관 — 한쪽이 오르면 다른 쪽은 **내린다** |

> ⚠️ **상관관계 ≠ 인과관계.** 상관은 "같이 움직이는가"만 볼 뿐 "**왜**"는 말해 주지 않는다.
> 아이스크림 판매량과 익사 사고는 상관이 높지만, 원인은 둘 다 늘린 **더운 날씨**다.

```python
df.corr(numeric_only=True)              # 상관 행렬 (숫자 컬럼끼리 전부)

df.corr(numeric_only=True).loc['Cost', 'Revenue']   # 두 변수만 꺼내기
df[['Cost', 'Revenue']].corr()                      # 두 컬럼만 골라 2x2 표
df['Cost'].corr(df['Revenue'])                      # Series 끼리 바로
```

**광고 데이터** — 모든 상관계수가 **0 근처**(최대 0.10). `Cost`-`Revenue` 는 **0.0098**. 이 데이터에서는 "광고비를 많이 쓰면 매출이 오른다"는 선형 관계가 보이지 않는다(실습용 무작위 데이터).

**날씨 데이터** — 뚜렷한 관계가 보인다.

|       | temp | hum | atm | speed |
|-------|------|-----|-----|-------|
| **temp** | 1.00 | **-0.46** | 0.18 | -0.07 |
| **hum** | **-0.46** | 1.00 | **-0.50** | -0.18 |
| **atm** | 0.18 | **-0.50** | 1.00 | -0.33 |
| **speed** | -0.07 | -0.18 | -0.33 | 1.00 |

기온이 높을수록 습도가 낮고(-0.46), 습도가 높을수록 기압이 낮다(-0.50). **음수도 뚜렷한 관계**다.

---

## 4. 탐색적 데이터 분석 — EDA

**EDA(Exploratory Data Analysis)** — **시각화를 통해** 데이터의 특징과 패턴을 이해하는 것. 시각화하면 특징을 **쉽게** 파악하고, 결과를 상대에게 **효과적으로** 전달할 수 있다.

| 라이브러리 | 특징 | 불러오기 |
|-----------|------|---------|
| **matplotlib** | 파이썬의 대표적인 시각화 라이브러리 | `import matplotlib.pyplot as plt` |
| **seaborn** | matplotlib 기반, **통계 데이터** 시각화 | `import seaborn as sns` |
| **plotly** | **웹 기반 인터랙티브** — 툴팁, 드래그 확대·축소, 범례 클릭 필터링 | `import plotly.express as px` |

주로 쓰는 도구 — 직선 그래프 · 막대 그래프 · 원 그래프 · 히스토그램 · 박스 플롯 · 산점도 · 히트맵

### 직선 그래프 — `px.line(data_frame, x, y, color)`

두 개 이상의 데이터 포인트를 **직선으로 연결**해 연속적인 변화와 추세를 보여 준다. `color` 에 컬럼을 넣으면 그 값으로 **색을 나눠** 그린다.

```python
import plotly.express as px

df_sorted = df_tips.sort_values(by="total_bill")     # ← 먼저 정렬!

fig = px.line(df_sorted, x="total_bill", y="tip", color="time",
              title="점심 / 저녁으로 나눠 보기")
fig.show()
```

> **직선 그래프는 먼저 정렬해야 한다.** `px.line()` 은 **행 순서대로** 점을 잇기 때문에, x 값이 뒤죽박죽이면 선이 왔다 갔다 엉킨다.

식당 손님 244명의 `tips.csv` 로 그려 보면 계산 금액이 클수록 팁도 커지는 흐름이 보인다. 상관계수로도 **0.68** — 뚜렷한 양의 상관이다.

> plotly 그래프는 **노트북을 직접 실행해야** 보인다. GitHub 미리보기는 plotly 출력을 그리지 않는다.

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `row = len(df_state['Revenue'])` 에 **"행의 개수 확인 (추천!)"** 주석 — 결과는 **8**(describe 통계량 개수). 데이터 행 수는 `len(df)` = 5,000
- [x] `df_state['Revenue'].count()` 도 같은 이유로 8 — 데이터 개수는 `df_state.loc['count', 'Revenue']`
- [x] `df.corr(['temp', 'hum'])` → **ValueError**. 첫 번째 자리는 계산 방법(`method`)이라 컬럼 목록을 넣으면 안 된다 → `df[['temp','hum']].corr()` / `df['temp'].corr(df['hum'])`
- [x] `df.corr.loc['Cost', 'Revenue']` → **AttributeError**. `corr` 는 메서드라 **괄호로 먼저 호출** → `df.corr(numeric_only=True).loc[...]`
- [x] 주석 버전 `df['Cost','Revenue']` — 여러 컬럼은 대괄호 **두 겹**
- [x] "**오른쪽 하향하는 계수는 의미가 없다**" → 틀린 설명. 오른쪽 아래로 내려가는 것은 **음의 상관**이고 의미가 있다. 의미가 없는 건 **0 근처**
- [x] 제목은 "**atm** 컬럼 중간값" 인데 코드는 `speed` 를 구하던 것 → `atm` 으로
- [x] `avg_cost` 를 계산만 하고 `#printt(...)` 로 막혀 있던 것 → 오타 고쳐 살림
- [x] `warnings.filterwarnings("ignore")` 로 **모든 경고를 끄던 것** 제거 — 문제가 생겨도 원인을 놓친다
- [x] 교재 p.46 `color` 하이퍼파라미터 예제 추가, 그래프에 `title` 추가
- [x] 오타 — `medien_rev2`, `요약 통계망`, `상관 행열`, `임포틑`, `tmep`, `printt`
- [x] 절대 경로 `C:\Users\Jinho\work\...` → 상대 경로 `./`
- [x] `Data_analysis01` 은 [Day 017](../2026-09-30/) 의 필기와 **내용이 완전히 같아** 다시 올리지 않았다

**직접 해본 것**
- 같은 통계량을 `describe().loc[...]` 와 메서드 두 방법으로 구해 결과가 같은지 확인 (광고 · 날씨 데이터 둘 다)
- 중앙값을 `loc['50%']` · `median()` · `quantile(0.5)` 세 방법으로 비교
- 매출의 평균과 중앙값을 비교해 분포의 치우침 짐작하기
- `len(df_state)` · `len(df)` · `loc['count']` 를 나란히 찍어 "행 개수"가 무엇을 세는지 확인
- 광고 데이터(상관 거의 없음)와 날씨 데이터(뚜렷한 음의 상관) 상관 행렬 비교
- `tips.csv` 를 정렬하고 `px.line()` 으로 그린 뒤 `color="time"` 으로 점심/저녁 나누기

**막혔던 부분 / 질문**
- [ ] 피어슨 상관계수는 **선형** 관계만 잡는다는데, 곡선 관계는 어떻게 찾는지 (`spearman` 과의 차이)
- [ ] 상관계수 0.68 이 "강하다"고 말할 수 있는 기준이 분야마다 다른지
- [ ] `tips` 직선 그래프는 같은 `total_bill` 에 점이 여러 개라 선이 위아래로 튀는데, 이런 데이터에는 산점도가 더 맞지 않은지
- [ ] 표준편차가 평균의 51% 면 큰 편인지 — 변동계수를 해석하는 기준
- [ ] `describe()` 에 `include='all'` 을 주면 문자열 컬럼은 어떤 통계량이 나오는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [`DataFrame.describe()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
- [`DataFrame.corr()` 문서 — `method` · `numeric_only`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html)
- [`Series.corr()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.Series.corr.html)
- [Plotly Express — Line charts](https://plotly.com/python/line-charts/)
- [Plotly Express 개요](https://plotly.com/python/plotly-express/)
