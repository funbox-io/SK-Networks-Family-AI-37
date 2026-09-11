---
day: 002
date: 2026-09-07
weekday: 월
week: 2
phase: 프로그래밍과 데이터 기초
title: 파이썬 자료형 — 리스트 · 딕셔너리 · 튜플 · 숫자형 · 문자열 · 불
tags: python, list, dict, tuple, 자료형, 인덱싱, 슬라이싱, mutable, immutable, get, del, clear, 연산자, bool
---

# Day 002 · 2026-09-07 (월)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 값을 담는 여섯 가지 그릇(리스트·딕셔너리·튜플·숫자형·문자열·불)의 성질과 꺼내 쓰는 법을 정리했다.

📂 실습 노트북 → [`lecture/python_datatypes.ipynb`](./lecture/python_datatypes.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 7장 · 종합 문제 23문항)

---

## 1. 리스트 (list)

- **인덱싱** : 값 하나를 꺼낸다. `리스트[번호]`
- **슬라이싱** : 범위를 잘라 **리스트**로 꺼낸다. `리스트[시작:끝]` (끝 번호는 포함하지 않음)
- 리스트 안에 리스트를 넣으면 **중첩 리스트**가 되고, `[i][j]` 처럼 두 번 인덱싱한다.

```python
student_names = ["김진호", "이지현", "박서준"]
student_scores = [88, 95.5, 72]

score_table = [student_names, student_scores]   # 중첩 리스트

print(score_table[0][0])   # '김진호'  <- 0번 리스트(이름)의 0번 값
print(score_table[:-1])    # 마지막 리스트(점수)를 뺀 나머지
```

리스트는 **변경 가능(mutable)** 한 자료형이라 인덱스로 값을 덮어쓸 수 있다.

```python
weekly_sales = [120, 250, 310, 400]
weekly_sales[3] = 500      # 목요일 판매량 정정
```

---

## 2. 딕셔너리 (dict)

**매핑(mapping)** 자료형으로, `key` 와 `value` 가 **1:1로 대응**한다.

- 형태 : `{key: value, key: value, ...}`
- `key` 는 **중복 불가**, `value` 는 **중복 가능**
- 리스트가 *순서(번호)* 로 값을 찾는다면, 딕셔너리는 *이름(key)* 으로 찾는다.

```python
address_book = {}                                   # 빈 딕셔너리
member = {'name': '이지현', 'age': 20}               # key = 문자열
member_by_id = {1: '김진호', 2: '이지현'}             # key = 숫자도 가능
member_group = {'name': ['김진호', '이지현'], 'age': [30, 20]}   # value 에 리스트
```

### 값(value) 가져오기

| 방법 | 형태 | 없는 key를 찾으면 |
|------|------|------------------|
| 대괄호 | `딕셔너리[key]` | **에러(KeyError)** 발생 |
| get() | `딕셔너리.get(key)` | `None` 반환 (에러 없음) |

```python
customer = {'name': '김진호', 'age': 30, 'phone': '010-1234-5678'}

print(customer['name'])          # 김진호
print(customer.get('phone'))     # 010-1234-5678
print(customer.get('address'))   # None  <- 없는 key 여도 에러가 나지 않는다
```

### 추가 / 수정 / 삭제

추가와 수정은 문법이 같다. `딕셔너리[key] = value` 가 **없는 key 면 추가, 있는 key 면 덮어쓰기**다.

```python
customer['birth'] = '08/09'   # 없던 key -> 새로 추가
customer['age'] = 31          # 있는 key -> 값이 덮어써짐

del customer['birth']         # key 하나 삭제
customer.clear()              # 전체 삭제 (빈 딕셔너리가 됨)
```

---

## 3. 튜플 (tuple)

|  | 리스트 | 튜플 |
|---|--------|------|
| 표기 | `['우유', '빵']` | `(1999, 1, 1)` |
| 인덱싱·슬라이싱 | 가능 | 가능 |
| 값 변경 | **가능**(mutable) | **불가능**(immutable) |

둘 다 여러 값을 담는 묶음 자료형이다. **바뀔 수 있는 값은 리스트(장바구니), 바뀌면 안 되는 값은 튜플(생년월일)** 에 담는다고 생각하면 쉽다.

```python
shopping_list = ['우유', '빵', '계란']    # 언제든 바뀔 수 있는 장바구니
birth_date = (1999, 1, 1)               # 절대 바뀌면 안 되는 생년월일

shopping_list[0] = '두유'                # 리스트는 변경 성공

try:
    birth_date[0] = 2000                # 튜플은 TypeError
except TypeError as error:
    print("튜플 변경 실패 :", error)
```

---

## 4. 숫자형과 연산자

- **정수형(int)** : 소수점이 없는 수 → 사람 수, 개수
- **실수형(float)** : 소수점이 있는 수 → 평균, 키, 몸무게
- `type()` 함수로 자료형을 확인한다.

| 연산자 | 의미 |
|--------|------|
| `+` `-` `*` `/` | 더하기 · 빼기 · 곱하기 · 나누기 |
| `**` | 제곱 |
| `//` | 몫(정수 나눗셈) |
| `%` | 나머지 |

`/` 는 결과가 항상 실수(`float`)다.

```python
total_pages = 7
pages_per_day = 3

print(total_pages // pages_per_day)   # 2일  <- 몫
print(total_pages % pages_per_day)    # 1쪽  <- 나머지
```

**2로 나눈 나머지가 `0` 이면 짝수, `1` 이면 홀수**다.

```python
locker_number = 2
print(locker_number % 2)   # 0 -> 짝수
```

---

## 5. 문자열 (string)

따옴표 3개(`'''` 또는 `"""`)로 감싸면 줄바꿈이 포함된 **여러 줄 문자열**을 만들 수 있다. `len()` 은 **줄바꿈(`\n`)도 한 글자로** 센다.

```python
address = '''서울특별시 강남구
테헤란로 123
파이썬빌딩 5층'''

print(len(address))   # 줄바꿈도 세어진다
```

인덱스는 앞에서 **0번부터**, 뒤에서 **-1번부터**. `문자열[시작:끝]` 은 **끝 번호 직전까지** 잘라낸다.

```python
lesson_text = "문자열은 인덱싱과 슬라이싱이 가능하다."

print(lesson_text[0])      # 첫 글자
print(lesson_text[-1])     # 마지막 글자
print(lesson_text[0:5])    # 0번 ~ 4번 글자
```

문자열 연산은 `+` 가 **연결**, `*` 가 **반복**이다.

```python
greeting = 'Good' + " " + 'Morning'
print(greeting * 3)
print("=" * 20)            # 구분선을 만들 때 자주 쓰는 방법
```

---

## 6. 불 (bool)

비교 연산(`>` `<` `==` `!=`)의 결과는 항상 `True` 또는 `False` 다.

```python
my_money = 8000
item_price = 10000

can_buy = my_money > item_price       # False
is_odd = (7 % 2 == 1)                 # True
```

`True` 는 숫자 `1`, `False` 는 숫자 `0` 처럼 계산된다 → **개수를 셀 때** 유용하다.

```python
print(can_buy + is_odd)   # False(0) + True(1) = 1

attended = [True, True, False]
print(attended[0] + attended[1] + attended[2])   # 출석 일수 2
```

---

## 🔁 복습

**직접 해본 것**
- 중첩 리스트 `score_table` 을 만들어 `[0][0]` 인덱싱과 `[:-1]` 슬라이싱 결과 비교
- 딕셔너리에 없는 key 를 `[]` 와 `.get()` 으로 각각 꺼내 보고 KeyError / None 차이 확인
- `song_info` 를 빈 상태에서 시작해 가수·장르·발매일을 하나씩 추가하고, `del` → `.clear()` 로 되돌려 보기
- 튜플 값 변경을 `try/except TypeError` 로 감싸 실제 에러 메시지 출력
- `total_pages // pages_per_day`, `% 2` 로 몫·나머지와 짝수/홀수 판별 실습
- 변수 이름을 **데이터가 무엇인지 드러나게** 다시 지음 (`data1`, `swap` → `student_names`, `first_item`, `weekly_sales`)
- 예제를 실생활 상황으로 바꿔서 정리 — 성적표(중첩 리스트), 주소록·고객 정보(딕셔너리), 장바구니 vs 생년월일(리스트/튜플), 사물함 번호(짝·홀 판별)
- 종합 복습 문제 23문항 풀이 — 주민번호 앞/뒤 자리 분리, 피타고라스 계산, 중첩 리스트 + 문자열 슬라이싱 조합 등

**막혔던 부분 / 질문**
- [ ] 딕셔너리에서 `d[key]` 와 `d.get(key)` 를 언제 골라 써야 하는지 — 없는 key 가 정상 상황이면 `get()`, 반드시 있어야 하면 대괄호?
- [ ] 튜플은 왜 값을 못 바꾸게 만들었는지 (immutable 의 장점)
- [ ] 슬라이싱에서 끝 번호가 제외되는 규칙 — `lesson_text[5:-6]` 처럼 음수 인덱스와 섞이면 결과 예측이 어려움
- [ ] `//` 로 평균을 구하면 소수점이 버려짐 — 정확한 평균을 원할 때는 `/` 를 써야 한다는 점
- [ ] `del` 과 `.clear()` 처럼 원본을 직접 바꾸는 연산과, 새 값을 돌려주는 연산의 구분

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 자료구조 (리스트 · 튜플 · 딕셔너리)](https://docs.python.org/ko/3/tutorial/datastructures.html)
- [내장 자료형 문서 (`dict`, `tuple`, `str`, `bool`)](https://docs.python.org/ko/3/library/stdtypes.html)
- [문자열 메서드와 시퀀스 슬라이싱](https://docs.python.org/ko/3/library/stdtypes.html#text-sequence-type-str)

