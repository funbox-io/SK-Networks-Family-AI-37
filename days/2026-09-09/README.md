---
day: 004
date: 2026-09-09
weekday: 수
week: 2
phase: 프로그래밍과 데이터 기초
title: 파이썬 반복문과 조건문 — for · while · if, 그리고 함수 · 메서드 복습
tags: python, function, return, method, for, while, range, break, if, elif, else, split, join, strip, replace
---

# Day 004 · 2026-09-09 (수)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 함수와 자료형 메서드를 문제로 복습하고, 반복문(for · while)과 조건문(if · elif · else)으로 코드의 흐름을 제어하는 법을 배웠다.

📂 실습 노트북 → [`lecture/python_loops_conditions.ipynb`](./lecture/python_loops_conditions.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 5장 · 문제 43문항)

---

## 1. 함수 복습

```python
def 함수이름(매개변수1, 매개변수2):
    실행할 코드
    return 돌려줄 값
```

- **매개변수(parameter)** : 함수를 정의할 때 받기로 약속한 값
- **인수(argument)** : 함수를 호출할 때 실제로 넘기는 값
- **키워드 인수** : `subtract(a=10, b=3)` 처럼 이름을 지정해 넘기면 **순서를 바꿔도 된다.**
- `return` 이 없는 함수는 값을 돌려주지 않고 **`None`** 이 된다. 출력만 하는 함수와 값을 돌려주는 함수는 역할이 다르다.

```python
def subtract(a, b):
    return a - b

print(subtract(a=10, b=3))   # 키워드 인수 -> 순서를 바꿔 써도 된다
```

---

## 2. 자료형별 메서드

### 문자열 메서드

| 메서드 | 하는 일 |
|--------|---------|
| `lower()` / `upper()` | 전부 소문자 / 대문자로 |
| `capitalize()` | 첫 글자만 대문자 |
| `title()` | 단어마다 첫 글자를 대문자 |
| `strip()` | 앞뒤 공백·줄바꿈 제거 |
| `replace(옛것, 새것)` | 문자열 바꾸기 |
| `split(기준)` | 기준으로 잘라 **리스트**로 |
| `구분자.join(리스트)` | 리스트를 이어 붙여 **문자열**로 |

> 문자열 메서드는 원본을 바꾸지 않고 **새 문자열을 돌려준다.**
> 그래서 `text.strip()` 처럼 호출만 하면 아무 일도 일어나지 않고, `text = text.strip()` 처럼 **다시 대입해야** 결과가 남는다.

메서드는 `.` 으로 이어 붙여 한 번에 처리할 수 있고, **왼쪽부터 차례대로** 실행된다.

```python
text = "\n  i like java  \n"
print(text.replace("java", "python").strip().title())   # I Like Python
```

### 리스트 · 딕셔너리 메서드

| 메서드 | 하는 일 |
|--------|---------|
| `리스트.append(값)` | 리스트 맨 뒤에 값 추가 |
| `len(자료형)` | 원소 개수 |
| `딕셔너리.keys()` | key 모음 |
| `딕셔너리.values()` | value 모음 |
| `딕셔너리.items()` | (key, value) 쌍 모음 |
| `딕셔너리.get(key)` | value 가져오기 (없으면 `None`) |

리스트는 **함수 안에서 바꾸면 원본까지 바뀐다.** 함수 안에서 `target_list.append(value)` 를 하면 호출한 쪽의 리스트도 함께 늘어난다.

```python
def add_and_count(target_list, value):
    target_list.append(value)    # 원본이 바뀐다
    return target_list

my_list = [1, 2, 3]
add_and_count(my_list, 4)
print(my_list)                   # [1, 2, 3, 4]
```

---

## 3. 반복문 (for / while)

### for 문 — 정해진 데이터를 하나씩 꺼내기

```python
for 변수 in 반복할_데이터:
    반복할 코드
```

리스트는 **원소**를, 문자열은 **글자 하나씩**을 꺼낸다. 딕셔너리를 그냥 반복하면 **key** 가 꺼내지고, key·value 를 함께 쓰려면 `items()` 를 쓴다.

```python
menu_price = {'햄버거': 6000, '피자': 15000}

for menu_name in menu_price:                  # key 가 꺼내진다
    print(menu_name, ":", menu_price[menu_name], "원")

for menu_name, price in menu_price.items():   # key, value 를 한 번에
    print(f"{menu_name}의 가격은 {price}원입니다.")
```

### range() — 숫자를 자동으로 만들어 주기

- `range(끝)` → `0` 부터 `끝-1` 까지
- `range(시작, 끝)` → `시작` 부터 `끝-1` 까지
- `range()` 자체를 출력하면 숫자가 아니라 `range(0, 5)` 라고만 나온다 → **`list()` 로 감싸야** 내용을 볼 수 있다.

```python
print(range(0, 5))         # range(0, 5)
print(list(range(0, 5)))   # [0, 1, 2, 3, 4]
```

### while 문 — 조건이 참인 동안 계속 반복

```python
while 조건식:
    반복할 코드
    변수 변경          # 이걸 빠뜨리면 무한 루프!
```

> ⚠️ 파이썬에는 `++count` 같은 **증감 연산자가 없다.** `count += 1` / `count -= 1` 처럼 써야 값이 실제로 바뀐다.

```python
count = 3

while count > 0:
    print(f"Hello World (남은 횟수 {count})")
    count -= 1                   # 반드시 값을 줄여야 반복이 끝난다
```

### break — 반복 도중에 빠져나오기

`while True:` 는 조건이 항상 참이라 영원히 도는 반복문이다. 이때는 반드시 안쪽에 `break` 로 빠져나갈 길을 만들어 준다.

```python
count = 3

while True:
    print(f"카운트 : {count}")
    if count == 0:               # 종료 조건
        print("발사!")
        break
    count -= 1
```

---

## 4. 조건문 (if / elif / else)

```python
if 조건식:
    조건이 참일 때 실행
else:
    조건이 거짓일 때 실행
```

조건식의 결과는 항상 `True` / `False`(bool)다. 조건식만 따로 출력해 보면 확인할 수 있다.

```python
money = 1500
print(money >= 1000)   # True
```

조건이 3개 이상일 때는 `elif` 를 쓴다. **위에서부터 순서대로** 검사해 처음 참이 되는 곳만 실행하고 빠져나온다. 그래서 **범위가 좁은 조건(큰 값)부터** 써야 하고, 경계값을 놓치지 않으려면 `>=` 를 쓴다.

```python
money = 100

if money >= 10000:
    print("택시를 탄다!")
elif money >= 1300:
    print("버스를 탄다!")
else:
    print("걸어간다!")
```

값이 이미 `True` / `False` 면 `if user.get('active') == True` 가 아니라 **`if user.get('active'):`** 로 충분하다.

---

## 5. 반복문 + 조건문 조합 패턴

- `%` 로 짝수/배수 판별 — `number % 2 == 0`, `number % 3 == 0`
- 조건에 맞는 값만 새 리스트에 `append`
- 누적 변수로 합계 내기 — `total += price`
- 첫 값을 임시 최댓값으로 두고 갱신하기

```python
numbers = [12, 7, 19, 24, 30, 15]
even_numbers = []
odd_numbers = []

# range(len(...)) 는 '번호'를 꺼내므로, 값을 쓰려면 리스트를 직접 반복한다
for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)
    else:
        odd_numbers.append(number)
```

> ⚠️ `sum` 은 내장 함수 이름이라 변수명으로 쓰지 않는다. (`total_price` 등으로)

---

## 🔁 복습

**직접 해본 것**
- 곱셈·뺄셈(키워드 인수)·제곱·문자열 연결 함수를 만들고, `return` 없는 함수도 만들어 비교
- `lower / upper / capitalize / title / strip / replace / split / join` 을 하나씩 실행해 결과 비교
- `split(',')` 로 자른 리스트를 `" ".join(...)` 으로 되돌려 보기
- 딕셔너리를 `keys()` `values()` `items()` `get()` 으로 각각 꺼내 출력 형태 확인
- 리스트·딕셔너리·문자열을 `for` 로 각각 반복해 꺼내지는 값이 무엇인지 확인
- `range(0, 5)` 를 그대로 / `list()` 로 감싸서 출력 비교
- `count -= 1` 로 끝나는 `while` 과 `while True` + `break` 로 카운트다운 두 가지 방식 구현
- 필기에서 헷갈렸던 부분을 주석으로 바로잡음 — f-string 안에서는 중괄호 `{}`(대괄호 `[]` 는 글자로 출력), `strip()` 결과를 다시 대입하지 않아 원본이 그대로였던 것, `range(len(...))` 은 값이 아니라 번호를 꺼낸다는 것, `== True` 는 불필요하다는 것
- 종합 응용 15문항 — 짝수·홀수 분리, `.csv` 파일만 골라내기, 10,000원 이상 상품에만 할인율 적용, 글자 수 기준 단어 필터, 3의 배수 합계, 로그인 3회 실패 시 계정 잠금, 학생별 평균 계산 후 합격/불합격 판정, 반복문으로 최댓값 찾기, 장바구니 총액, 이메일 도메인 추출

**막혔던 부분 / 질문**
- [ ] 파이썬에 `++` 가 없어서 `count += 1` 을 빠뜨리면 무한 루프 — while 문을 쓸 때마다 종료 조건 먼저 확인하기
- [ ] `if` / `elif` 순서를 바꾸면 결과가 달라지는 이유 (범위가 넓은 조건을 위에 두면 아래 조건이 실행되지 않음)
- [ ] 문자열 메서드는 새 값을 돌려주는데 `리스트.append()` 는 원본을 바꾸는 차이 (immutable vs mutable)
- [ ] 함수에 리스트를 넘기면 원본이 바뀌는 이유 — 값이 아니라 무엇이 전달되는 걸까
- [ ] `range()` 를 그대로 출력하면 왜 숫자가 안 보이는지, `list()` 로 감싸야 하는 이유
- [ ] `while True` + `break` 와 조건식을 직접 쓰는 `while` 중 언제 무엇을 고르는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 흐름 제어 (`if`, `for`, `range`, `break`)](https://docs.python.org/ko/3/tutorial/controlflow.html)
- [문자열 메서드 문서 (`split`, `join`, `replace`, `strip`, `title`)](https://docs.python.org/ko/3/library/stdtypes.html#string-methods)
- [딕셔너리 메서드 문서 (`keys`, `values`, `items`, `get`)](https://docs.python.org/ko/3/library/stdtypes.html#mapping-types-dict)
- [`range` 자료형 문서](https://docs.python.org/ko/3/library/stdtypes.html#range)

