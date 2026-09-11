---
day: 003
date: 2026-09-08
weekday: 화
week: 2
phase: 프로그래밍과 데이터 기초
title: 파이썬 함수 — 사용자 정의 함수 · 리스트 · 딕셔너리 · 문자열 전용 함수
tags: python, function, def, return, 기본값, None, append, insert, extend, clear, keys, values, items, get, lower, upper, split, join, replace, strip, immutable
---

# Day 003 · 2026-09-08 (화)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 기능을 이름으로 묶어 재사용하는 함수를 직접 만들어 보고, 리스트·딕셔너리·문자열에 딸린 전용 함수를 정리했다.

📂 실습 노트북 → [`lecture/python_functions.ipynb`](./lecture/python_functions.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 5장)

---

## 1. 함수(function)란?

같은 코드를 여러 번 쓰지 않도록 **하나의 이름으로 묶어 둔 기능 덩어리**다. 재료(입력)를 넣으면 결과(출력)를 돌려주는 자판기라고 생각하면 쉽다.

| 종류 | 설명 | 예 |
|------|------|-----|
| **내장 함수** | 파이썬이 기본으로 갖고 있어 바로 쓸 수 있는 함수 | `print()` `len()` `type()` |
| **전용 함수(메서드)** | 특정 자료형에만 딸려 있는 함수. `변수.함수()` 형태로 부른다 | `리스트.append()` `문자열.split()` |
| **사용자 정의 함수** | 내가 직접 `def` 로 만들어 쓰는 함수 | `def add(x, y):` |

### 함수 정의 — `def`

```python
def 함수이름(매개변수1, 매개변수2):
    실행할 코드
    return 돌려줄 값
```

- **매개변수(parameter)** : 함수를 *정의*할 때 적는 이름 (`x`, `y`)
- **인수(argument)** : 함수를 *호출*할 때 실제로 넣는 값 (`3`, `5`)
- `return` : 결과를 밖으로 돌려준다. 없으면 `None` 을 돌려준다.

정의만 해서는 아무 일도 일어나지 않는다. **`이름(인수)`** 형태로 불러야 실행되고, 한 번 만들면 값만 바꿔 몇 번이든 재사용할 수 있다.

```python
def add(first_number, second_number):
    total = first_number + second_number
    return total

print(add(3, 5))      # 8
print(add(10, 20))    # 30  <- 같은 함수를 값만 바꿔 재사용
```

### 기본값이 있는 매개변수

매개변수에 `= 값` 을 적어 두면, 호출할 때 그 자리를 **생략**할 수 있다.

```python
def price_with_tax(price, tax_rate=0.1):
    return price * (1 + tax_rate)

print(price_with_tax(10000))         # 기본 세율 10%
print(price_with_tax(10000, 0.05))   # 세율 5% 지정
```

### `return` 이 없는 함수

`return` 을 적지 않으면 함수는 **`None`** 을 돌려준다. 화면에 출력만 하는 함수와 값을 돌려주는 함수는 다르다.

```python
def print_greeting(name):
    print(f"안녕하세요, {name}님!")   # 출력만 하고 돌려주는 값은 없다

returned_value = print_greeting("김진호")
print(returned_value)   # None
```

---

## 2. 리스트 전용 함수

리스트 변수 뒤에 점을 찍고 부르는 함수들이다. (`리스트.함수()`)

| 함수 | 하는 일 |
|------|---------|
| `append(값)` | 맨 **뒤에 하나** 추가 |
| `insert(위치, 값)` | 원하는 **위치에 끼워 넣기** |
| `extend(리스트)` | 다른 리스트의 값들을 **모두 이어 붙이기** |
| `clear()` | 전체 비우기 |
| `len(리스트)` | 길이 세기 (내장 함수) |

> ⚠️ `append()` 는 **원본 리스트를 직접 바꾸고, 돌려주는 값은 `None`** 이다.
> 그래서 `새변수 = 리스트.append(값)` 처럼 쓰면 `None` 이 담긴다.

```python
number_list = [0, 1, 2, 3, 4]

number_list.append(10)              # 원본이 바뀐다
wrong_result = number_list.append(20)
print(wrong_result)                 # None  <- 흔한 실수
print(number_list)                  # 원본은 바뀌어 있다
```

`insert(위치, 값)` 은 그 위치부터 뒤의 값들이 한 칸씩 밀린다.

```python
waiting_line = ['김진호', '이지현', '박서준']
waiting_line.insert(0, '최유리')      # 맨 앞에 새치기
waiting_line.insert(2, '정민수')      # 2번 자리에 끼워 넣기
```

### `extend()` 와 `+` — 리스트 합치기

| 방법 | 원본 | 결과 |
|------|------|------|
| `A.extend(B)` | **A가 직접 바뀐다** | 돌려주는 값 없음(`None`) |
| `A + B` | 원본은 그대로 | **합쳐진 새 리스트**를 돌려준다 |

```python
basket = ['계란']
basket.extend(['사과', '두부'])        # basket 자체가 늘어난다

first_list = ['계란', '우유']
merged_list = first_list + ['사과']    # first_list 는 그대로, 새 리스트가 생긴다
```

---

## 3. 딕셔너리 전용 함수

| 함수 | 하는 일 | 돌려주는 값 |
|------|---------|------------|
| `keys()` | key 전체 | `dict_keys([...])` |
| `values()` | value 전체 | `dict_values([...])` |
| `items()` | key와 value 쌍 전체 | `dict_items([(k, v), ...])` |
| `get(key)` | 값 하나 꺼내기 | 없으면 **`None`** (에러 없음) |
| `clear()` | 전체 비우기 | 없음 |

`keys()` 가 돌려주는 값은 리스트가 아니라 `dict_keys` 라는 전용 자료형이다. 리스트처럼 쓰고 싶으면 `list()` 로 바꿔 준다.

```python
member = {'name': '이지현', 'age': 20, 'phone': '010-2000-0000'}

key_data = member.keys()
print(type(key_data))       # <class 'dict_keys'>
print(list(key_data))       # ['name', 'age', 'phone']
```

`items()` 는 `(key, value)` 튜플들의 묶음을 돌려준다. 반복문에서 특히 많이 쓴다.

```python
actor = {'name': '박보검', 'age': 31}

for key, value in actor.items():
    print(f"{key} : {value}")
```

### `get()` — 에러 없이 값 꺼내기

| 방법 | 없는 key를 찾으면 |
|------|------------------|
| `딕셔너리[key]` | **KeyError** 발생 |
| `딕셔너리.get(key)` | `None` 반환 (에러 없음) |

`get()` 은 값을 *읽기만* 한다. 없는 key 를 만들어 주지는 않는다.

```python
print(actor.get('address'))                 # None
print(actor.get('address', '정보 없음'))     # 기본값 지정도 가능

try:
    print(actor['address'])                 # 대괄호는 에러
except KeyError as error:
    print("KeyError 발생 :", error)
```

---

## 4. 문자열 전용 함수

| 함수 | 하는 일 |
|------|---------|
| `lower()` / `upper()` | 소문자 / 대문자로 바꾸기 |
| `split(기준)` | 기준으로 **잘라서 리스트**로 만들기 |
| `기준.join(리스트)` | 리스트를 기준으로 **이어 붙여 문자열**로 만들기 |
| `replace(찾을값, 바꿀값)` | 바꿔치기 |
| `strip()` | 앞뒤 공백·줄바꿈 지우기 |

> ⚠️ 문자열은 **immutable(변경 불가)** 이라서, 이 함수들은 원본을 바꾸지 않고 **새 문자열을 돌려준다.**
> 그래서 결과를 꼭 변수에 담아야 한다.

```python
language_name = "PYTHON"

lower_name = language_name.lower()
print(lower_name)        # python
print(language_name)     # PYTHON  <- 원본은 그대로
```

`split()` 은 기준을 적지 않으면 **공백**을 기준으로 자르고, 결과는 **리스트**다. `join()` 은 그 반대 기능으로, **이어 붙일 기준 문자열**에 점을 찍고 부른다.

```python
print("Arithmetic,Value,Type".split(','))   # ['Arithmetic', 'Value', 'Type']
print("Life is too short".split())          # ['Life', 'is', 'too', 'short']

colors = ['red', 'blue', 'yellow']
print(','.join(colors))     # red,blue,yellow
print(' '.join(colors))     # red blue yellow
```

```python
sentence = "Life is too short"
print(sentence.replace("Life", "My leg"))   # My leg is too short

messy_text = "\n\n  BaseExceptionGroup  \n"
print(f"[{messy_text.strip()}]")            # 앞뒤 공백·줄바꿈 제거
```

---

## 5. 오늘 정리

- 함수는 **기능을 이름으로 묶어 재사용**하는 도구다. `def` 로 만들고 `return` 으로 결과를 돌려준다.
- `append()`, `extend()`, `clear()` 처럼 **원본을 직접 바꾸는 함수**는 돌려주는 값이 `None` 이다. → `새변수 = 리스트.append(값)` 은 흔한 실수.
- `split()`, `join()`, `replace()`, `strip()` 처럼 **새 값을 돌려주는 함수**는 결과를 변수에 담아야 한다. → 문자열은 immutable 이라 원본이 바뀌지 않는다.
- 없는 key 가 있을 수 있으면 `딕셔너리[key]` 대신 `딕셔너리.get(key)` 를 쓴다.

---

## 🔁 복습

**직접 해본 것**
- `add()` 함수를 만들어 여러 값으로 반복 호출하고, 기본값 매개변수(`tax_rate=0.1`)로 세율 계산 함수 작성
- `return` 없는 함수의 반환값이 `None` 인 것을 직접 출력해서 확인
- 빈 리스트에 `append()` 로 하나씩 담고, `insert()` 로 중간에 끼워 넣어 인덱스가 밀리는 것 확인
- `extend()` 로 합친 결과와 `+` 로 합친 결과에서 원본이 어떻게 달라지는지 비교
- `keys()`, `values()`, `items()` 의 자료형을 `type()` 으로 확인하고 `list()` 로 변환
- 없는 key 를 `[]` 와 `.get()` 으로 각각 꺼내 KeyError / None 차이 확인 (`try/except KeyError`)
- `split()` → `join()` 왕복, `replace()` 로 문장 바꾸기, `strip()` 전후 길이 비교
- 변수 이름을 **데이터가 무엇인지 드러나게** 다시 지음 (`output1`, `clist2`, `data` → `sum_result`, `shopping_list`, `word_list`)
- 단원별 연습 문제 풀이 — 곱셈·평균·짝수 판별 함수, 과일 리스트 조작, 상품 딕셔너리 순회, 이메일 분리

**막혔던 부분 / 질문**
- [ ] `output = list_data.append(10)` 이 왜 `None` 이 되는지 — 원본을 바꾸는 함수와 새 값을 돌려주는 함수의 구분
- [ ] `extend()` 와 `+` 중 언제 무엇을 써야 하는지 (원본을 바꿔도 되는 상황인지)
- [ ] `keys()` 가 돌려주는 `dict_keys` 는 리스트와 뭐가 다른지, 언제 `list()` 로 바꿔야 하는지
- [ ] 문자열 함수를 썼는데 원본이 그대로인 이유 — immutable 개념
- [ ] `split()` 에 기준을 넣을 때와 비워 둘 때의 결과 차이
- [ ] `return` 을 쓰는 함수와 `print()` 만 하는 함수를 언제 나눠 만들어야 하는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 함수 정의하기](https://docs.python.org/ko/3/tutorial/controlflow.html#defining-functions)
- [내장 함수 목록](https://docs.python.org/ko/3/library/functions.html)
- [문자열 메서드 문서 (`split`, `join`, `replace`, `strip`)](https://docs.python.org/ko/3/library/stdtypes.html#string-methods)
- [딕셔너리 메서드 문서 (`keys`, `values`, `items`, `get`)](https://docs.python.org/ko/3/library/stdtypes.html#mapping-types-dict)

