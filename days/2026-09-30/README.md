---
day: 017
date: 2026-09-30
weekday: 수
week: 5
phase: 데이터 분석과 머신러닝/딥러닝
title: 데이터 전처리 — 누락 데이터 · groupby · 이상치(IQR)
tags: python, pandas, 전처리, preprocessing, 결측치, NaN, isnull, dropna, fillna, groupby, agg, 이상치, outlier, 사분위수, quantile, IQR, clip, 불리언인덱싱, 논리연산자
---

# Day 017 · 2026-09-30 (수)

`데이터 분석과 머신러닝/딥러닝` · 5주차

> **한 줄 요약** — 분석 전에 데이터를 손보는 세 가지 — 빈 값 채우기·지우기, 중복 값을 그룹으로 묶어 집계하기, IQR로 이상치를 찾아 제거하거나 눌러 주기를 배웠다.

📂 실습 노트북 → [`lecture/data_preprocessing.ipynb`](./lecture/data_preprocessing.ipynb)
📊 실습 데이터 → [`lecture/ad_performance.csv`](./lecture/ad_performance.csv) (5,000행) · [`lecture/weather.csv`](./lecture/weather.csv) (100,000행)
📖 교재 `데이터분석` p.22~33

---

## 0. 데이터 전처리(preprocessing)란

수집한 데이터를 **분석에 적합한 형태로 만들어 신뢰도를 높이는 작업**이다. 오늘 다룬 세 가지는 전처리에서 가장 자주 만나는 문제들이다.

| 문제 | 도구 |
|------|------|
| 값이 **비어 있다** (누락 데이터) | `isnull()` · `dropna()` · `fillna()` |
| 같은 값이 **여러 행에 반복된다** | `groupby()` · `agg()` |
| 유독 **작거나 큰 값**이 섞여 있다 (이상치) | `quantile()` · IQR · `clip()` |

> 표에 빈자리가 남아 있으면 **머신러닝 단계에서 오류가 난다.** 그래서 먼저 손봐야 한다.

---

## 1. 누락 데이터 처리하기

**누락 데이터(missing value)** = 값이 비어 있는 데이터. 부르는 이름이 셋이다.

| 용어 | 쓰이는 곳 |
|------|-----------|
| `NaN` | `read_csv()` 등으로 파일을 DataFrame·Series 로 바꿀 때 **누락을 표현하는 값** |
| `null` · `na` | **함수 이름**에 쓰인다 (`isnull()`, `dropna()`, `fillna()`) |

### 개수 확인 — `df.isnull().sum()`

- `isnull()` : 누락 여부를 **bool** 로 돌려준다 (비었으면 `True`)
- `sum()` : `True` 가 1로 계산되므로 더하면 **개수**가 된다

```python
df.isnull().sum()          # 컬럼별 누락 개수
df.isnull().sum().sum()    # 전체 누락 개수
```

> ⚠️ 반복문으로 하나씩 세면 40만 행 × 13열 = **520만 번** 돌게 된다. 판다스는 이걸 **한 줄로** 해 준다.

### 삭제 — `df.dropna()`

- 행 또는 열에 누락이 **1개만 있어도 그 행을 통째로** 지운다
- `ignore_index=True` : 남은 행의 인덱스를 0부터 다시 매긴다
- `subset=['컬럼1','컬럼2']` : 지정한 컬럼에 누락이 있는 행만 지운다

### 대체 — `df.fillna()`

지우면 데이터가 줄어든다. 그래서 적당한 값으로 채우기도 한다.

```python
df_cleaned = df.fillna("내용 없음")
df_cleaned = df.fillna(0)
df_cleaned = df.fillna({"저자": "저자 미상", "부가기호": 0})   # 컬럼마다 다르게
```

---

## 2. 중복되는 데이터를 그룹별로 모아서 처리하기

`groupby()` 는 **중복된 값을 기준으로 데이터를 그룹으로 나누고**, 그룹마다 따로 계산한다.

```python
df.groupby(by=['컬럼', ...]).func()
```

- `by` : 그룹으로 묶을 컬럼
- `func` : 그룹별로 적용할 함수 — `sum()` `mean()` `count()` …

> SQL 의 `GROUP BY` 와 같은 일을 한다. SQL 은 DB 안에서 집계까지만 하지만, 판다스로 가져오면 그대로 **머신러닝까지** 이어 갈 수 있다.

```python
# "어떤 채널의 평균 매출이 가장 높은가?"
channel_rev = df.groupby(by='Channel')['Revenue'].mean()
# Naver 1,084,622 > Organic 1,069,937 > Instagram 1,060,048 > Facebook > Google
```

### `agg()` — 그룹별로 여러 함수를 한 번에

```python
channel_sum = df.groupby('Channel').agg(
    total_cost      = ('Cost', 'sum'),
    average_cost    = ('Cost', 'mean'),
    total_revenue   = ('Revenue', 'sum'),
    average_revenue = ('Revenue', 'mean'),
)
```

| Channel | total_cost | average_cost | total_revenue | average_revenue |
|---------|-----------|--------------|---------------|-----------------|
| Facebook | 256,579,035 | 173,481.4 | 1,560,665,319 | 1,055,216.6 |
| Google | 261,593,751 | 173,701.0 | 1,586,236,276 | 1,053,277.7 |
| Instagram | 93,910,784 | 174,880.4 | 569,245,784 | 1,060,048.0 |
| Naver | 177,725,667 | 173,729.9 | 1,109,568,326 | 1,084,622.0 |
| Organic | 78,053,282 | 171,545.7 | 486,821,439 | 1,069,937.2 |

---

## 3. 이상치(outlier) 처리하기

**이상치** = 수집된 데이터 중 아주 작거나 매우 큰 값.

### 사분위수와 IQR

순서대로 정렬된 데이터를 **4구간으로 균등하게 나눌 때 기준이 되는 수**가 사분위수다.

| 이름 | 위치 | 뜻 |
|------|------|-----|
| **Q1** | 25% | 아래에서 1/4 지점 |
| **Q2** | 50% | 가운데 값 (중앙값 · 미디언) |
| **Q3** | 75% | 아래에서 3/4 지점 |

- **IQR** = `Q3 - Q1` — 가운데 절반이 퍼져 있는 폭
- 정상 범위 **최솟값** = `Q1 - (1.5 * IQR)`
- 정상 범위 **최댓값** = `Q3 + (1.5 * IQR)`
- **이 범위를 벗어난 값이 이상치**

```python
q1 = df.quantile(q=0.25)
q3 = df.quantile(q=0.75)
iqr = q3 - q1
min_val = q1 - (1.5 * iqr)
max_val = q3 + (1.5 * iqr)
```

날씨 데이터(100,000행)로 계산한 결과

| 컬럼 | Q1 | Q3 | IQR | 정상 최소 | 정상 최대 |
|------|----|----|-----|-----------|-----------|
| `temp` 기온 | 15.0 | 19.0 | 4.0 | 9.00 | 25.00 |
| `hum` 습도 | 66.0 | 93.0 | 27.0 | 25.50 | 133.50 |
| `atm` 기압 | 1002.0 | 1007.0 | 5.0 | 994.50 | 1014.50 |
| `speed` 풍속 | 1.5 | 4.6 | 3.1 | -3.15 | 9.25 |

### 비교 연산자와 논리 연산자

| 판다스 | 뜻 | 파이썬 |
|--------|-----|--------|
| `&` | 논리곱 (둘 다 참) | `and` |
| `\|` | 논리합 (하나라도 참) | `or` |
| `~` | 논리부정 (참↔거짓 뒤집기) | `not` |

> ⚠️ Series·DataFrame 에는 **`and` `or` `not` 을 쓸 수 없다.** 값이 여러 개라 참/거짓을 하나로 정할 수 없어서 `ValueError: The truth value of a DataFrame is ambiguous` 가 난다.
> 반드시 `&` `|` `~` 를 쓰고 조건마다 **괄호**로 묶는다.

### 이상치 제거

```python
outlier = (df < min_val) | (df > max_val)   # ③ 불리언 DataFrame
has_outlier = outlier.any(axis=1)           # ④ 행에 하나라도 있나
normal_rows = ~has_outlier                  # ⑤ 뒤집어서 정상인 행만
df_clean = df[normal_rows].reset_index(drop=True)
```

`axis=1` 은 **행 방향으로 훑는다**는 뜻이다. 100,000행 중 **이상치가 있는 행 8,249개**를 빼고 **91,751행**이 남았다.

### 이상치 대체 — `clip()`

제거하면 행이 줄어든다. 줄이고 싶지 않을 때는 **범위 밖의 값을 경계값으로 눌러 준다.**

```python
df_clipped = df.clip(lower=min_val, upper=max_val, axis=1)
```

행 개수는 그대로 100,000행. `temp` 의 최댓값 27 은 정상 최대 25 로, `hum` 의 최솟값 17 은 정상 최소 25.5 로 눌렸다.

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `for` 문을 두 겹으로 돌려 NaN 을 하나씩 세던 것 → **`df.isnull().sum()`** 한 줄 (교재 p.24). 401,682행 × 13열이면 **520만 번** 돈다
- [x] 변수명 `dfbool` — 담기는 값이 bool 이 아니라 **개수**라 이름이 맞지 않았다 → `na_count` 개념으로 정리
- [x] `display(df.isnull())` 이 401,682행을 전부 찍던 것 → `.head()`
- [x] `read_csv` 의 `DtypeWarning` → `low_memory=False` 로 해결
- [x] `groupby(by='Gender')['Cost'].mean()` 을 계산만 하고 출력을 주석으로 막아 둬서 결과가 안 보이던 것 → 살림
- [x] 주석 오타 `SQL cunt` → **`count`**
- [x] 마크다운 필기의 `(Q1 - (1.5-IQR))` · `(Q3 + (1.5+IQR))` → **곱하기(`*`)** 가 맞다 (교재 p.30)
- [x] `q1` `q3` `iqr` `min_val` `max_val` 을 따로 찍고 대부분 주석 처리해 **IQR 하나만** 보이던 것 → 다섯 값을 한 표로
- [x] 변수명 오타 — `hax_outlier` → **`has_outlier`**, `noml_bool` → **`normal_rows`**
- [x] `print(f"논리 부정{hax_outlier}")` 가 **뒤집기 전** 값을 "논리 부정"이라는 이름으로 찍던 것 → 전후를 개수로 비교
- [x] `arr = output.values` — `.values` 로 바꾸지 않아도 **Series 그대로 불리언 인덱싱**이 된다
- [x] 교재 p.32 의 마지막 단계 **`reset_index(drop=True)`** 가 빠져 있어 추가
- [x] 주석으로 남아 있던 `or` 버전은 지우지 않고 **실제 `ValueError` 를 띄워** 왜 안 되는지 보이게 함
- [x] 교재 p.32 의 **대체(`clip`) 방법이 필기에 없어서** 새로 추가

**직접 해본 것**
- 작은 표를 만들어 `isnull()` · `dropna()` · `fillna()` 를 차례로 적용하고 행 수 변화 확인
- `dropna()` 전체 삭제와 `subset=` 삭제의 결과 비교
- 채널별 평균 매출, 성별 평균 비용을 `groupby` 로 집계하고 `agg()` 로 네 가지 지표 한 번에 뽑기
- 날씨 데이터 100,000행에서 컬럼별 Q1 · Q3 · IQR · 정상 범위를 한 표로 계산
- `or` 를 써서 실제로 `ValueError` 가 나는 것을 확인한 뒤 `|` 로 고치기
- 이상치 제거(91,751행 남음)와 `clip()` 대체(100,000행 유지) 두 방법을 나란히 실행해 비교

**막혔던 부분 / 질문**
- [ ] `dropna()` 로 지울지 `fillna()` 로 채울지 판단 기준 — 누락 비율이 몇 %를 넘으면 컬럼을 통째로 버리는지
- [ ] `fillna()` 에 평균·중앙값을 넣는 방법과, 그게 분포를 왜곡하지는 않는지
- [ ] `speed` 의 정상 최소가 **-3.15** 로 음수가 나왔다 — 풍속은 음수가 될 수 없는데 이럴 때 IQR 기준을 그대로 써도 되는지
- [ ] 1.5배라는 숫자는 어디서 온 것인지 (3배를 쓰는 경우도 있다고 들음)
- [ ] 이상치를 지우면 8,249행이 사라지는데, 이게 실제로 "잘못된 값"인지 "드물지만 진짜 값"인지 어떻게 구분하는지
- [ ] `groupby().agg()` 에서 `'sum'` 같은 문자열 대신 직접 만든 함수를 넣을 수 있는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [pandas 공식 문서 — 결측 데이터 다루기](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [pandas 공식 문서 — Group by (split-apply-combine)](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [`DataFrame.quantile()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.quantile.html)
- [`DataFrame.clip()` 문서](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.clip.html)
- [pandas 공식 문서 — 불리언 인덱싱](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing)
