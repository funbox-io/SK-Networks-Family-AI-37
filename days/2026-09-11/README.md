---
day: 006
date: 2026-09-11
weekday: 금
week: 2
phase: 프로그래밍과 데이터 기초
title: 예외 처리 · 파일 처리 실습 — try · except · finally 와 with open 직접 써 보기
tags: python, exception, try, except, else, finally, as, NameError, ZeroDivisionError, FileNotFoundError, Exception, file, open, with, encoding, write, read, readline, readlines, raw string
---

# Day 006 · 2026-09-11 (금)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 전날 배운 예외 처리와 파일 처리를 직접 쳐 보면서, `try`/`except`/`finally` 를 쓰는 법과 `with open` 으로 파일을 만들고 읽는 법을 손에 익혔다.

📂 실습 노트북 → [`lecture/python_exception_file_practice.ipynb`](./lecture/python_exception_file_practice.ipynb) (수업 필기를 실행 가능하도록 정리, 총 5장)

---

## 1. 예외 처리

`10 / 0` 처럼 실행할 수 없는 연산을 만나면 `ZeroDivisionError` 가 나면서 **그 줄에서 프로그램이 멈춘다.**
`try` ~ `except` 로 감싸 두면 멈추지 않고 `except` 쪽 코드로 넘어간다.

```python
def divide_ten(number):
    output = 10 / number
    return output

print("정상 호출 :", divide_ten(2))

try:
    print("0 호출 :", divide_ten(0))
except ZeroDivisionError as e:
    print("0 호출 실패 :", e)

print("프로그램은 계속 실행됩니다.")
```

### 반복문 안에서 예외 처리하기

`range(0, 10)` 은 **0부터** 시작하므로 첫 회차에서 `10 / 0` 이 되어 에러가 난다.
반복문 안에 `try` 를 두면 **그 회차만 건너뛰고 반복은 계속된다.**

```python
for loop in range(0, 10):
    try:
        result = 10 / loop          # loop 가 0일 때만 에러
    except ZeroDivisionError:
        print(f"{loop} : 0으로 나눌 수 없습니다.")
    else:
        print(f"{loop} : 10 / {loop} = {result}")
```

### `if / else` 로도 같은 일을 할 수 있다

예외 처리는 조건문과 비슷한 구석이 있다.
**미리 걸러낼 수 있는 조건**(0인지 확인)은 `if` 로, **미리 알 수 없는 상황**은 `try` 로 처리한다.

```python
for num in range(0, 10):
    if num == 0:
        print(f"{num} : 0으로 나눌 수 없습니다.")
    else:
        print(f"{num} : 10 / {num} = {10 / num}")
```

---

## 2. 명시적 예외 처리

`except` 뒤에 에러 이름을 적으면 **그 에러만** 잡는다.

```python
name = "진호"

print(f"나라를 구하는 이름 : {name}")

try:
    print(f"두 번째 이름 : {second_name}")   # 정의한 적 없는 변수
except NameError as e:
    print("NameError :", e)
```

### 에러 여러 개를 한 번에 처리하기

```python
except (ZeroDivisionError, ValueError) as e:   # 1) 괄호로 묶어 튜플로
    ...

except ZeroDivisionError as e:                 # 2) except 절을 나눠서
    ...
except ValueError as e:
    ...
```

> ⚠️ `as` 는 **한 번만** 쓴다. `except A as B as :` 같은 문법은 없다.
> 그리고 `as e` 로 받은 `e` 는 **그 `except` 블록 안에서만** 살아 있다. `finally` 에서 쓰면 `NameError` 가 난다.

```python
for num in range(0, 3):
    try:
        output = 10 / num
    except (ZeroDivisionError, ValueError) as e:
        print(f"{num} : 에러 발생 -", e)
    else:
        print(f"{num} : 결과 {output}")
    finally:
        print(f"{num} : 처리 완료")      # 에러가 있든 없든 항상 실행
```

---

## 3. 포괄적 예외 처리

에러 이름을 **튜플로 묶어** 한 번에 잡거나, `Exception` 으로 전부 잡는다.

```python
error_types = (FileNotFoundError, NameError)

try:
    print("pass :", name)
    print("없는 변수 :", king_name)       # NameError
except error_types as e:
    print("잡힌 에러 :", type(e).__name__, "-", e)
```

```python
try:
    open("없는파일.txt", "r", encoding="utf-8")
except Exception as e:                     # 안전망
    print("모든 에러 잡기 :", type(e).__name__, "-", e)
```

> ⚠️ 변수 이름을 `tuple` 로 쓰면 내장 함수 `tuple()` 을 덮어쓰게 되므로 피한다.

---

## 4. 파일 처리

### 경로 쓰는 법

윈도우 경로의 역슬래시는 escape 문자로 해석된다. `"C:\Users\..."` 는 `\U` 때문에 **SyntaxError** 가 나므로 아래 셋 중 하나로 쓴다.

```python
path = r"C:\Users\Jinho\miniconda3\work\테스트.txt"    # r 을 붙이거나
path = "C:/Users/Jinho/miniconda3/work/테스트.txt"     # / 를 쓰거나
path = "C:\\Users\\Jinho\\miniconda3\\work\\테스트.txt" # \\ 로 두 번 쓰거나
```

### `with` 로 쓰기

`with open(...) as f:` 를 쓰면 블록이 끝날 때 **자동으로 닫힌다.** 한글이 깨지지 않도록 `encoding="utf-8"` 을 붙인다.

```python
file_path = "테스트.txt"

with open(file=file_path, mode='w', encoding="utf-8") as f:
    for num in range(1, 11):
        data = f"{num}번째 줄입니다.\n"     # 줄바꿈은 \n 을 직접 붙인다
        f.write(data)
# with 블록을 벗어나면 자동으로 close()

print("파일이 닫혔는가? :", f.closed)     # True
```

### 읽기 — `read()` / `readline()` / `readlines()`

| 메서드 | 결과 |
|--------|------|
| `read()` | 파일 전체를 **하나의 문자열**로 |
| `readline()` | **한 줄만** 문자열로 |
| `readlines()` | 전체를 **줄 단위 리스트**로 |

```python
with open(file=file_path, mode='r', encoding="utf-8") as f:
    lines = f.readlines()

print("줄 수 :", len(lines))
```

### 파일 처리 + 예외 처리

```python
def read_file(path):
    try:
        with open(file=path, mode='r', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"{path} 파일이 없습니다."
```

---

## 🔁 복습

**필기에서 고친 부분**
- [x] 함수 이름 `die_tem` → `divide_ten`, 매개변수 `e` → `number` — `e` 는 보통 `except ... as e` 의 에러 객체에 쓰는 이름이라 헷갈린다
- [x] `loop = 10/loop` → 반복 변수에 결과를 덮어쓰지 않도록 `result` 로 분리
- [x] 성공했을 때 `print("Error")` 가 찍히던 것 — 성공은 `else`, 실패는 `except`
- [x] `except:` (전부 잡기) → `except ZeroDivisionError:` (무슨 에러인지 분명하게)
- [x] `NameError` 예제 — 변수를 정의해 두고 "없는 변수 호출"이라 적어 실제로는 에러가 안 났던 것
- [x] `except ZeroDivisionError as FileNotFoundError as :` → `except (ZeroDivisionError, ValueError) as e:`
- [x] `finally` 안의 `print(e)` — `e` 는 `except` 블록을 벗어나면 사라진다
- [x] 변수명 `tuple` → `error_types` (내장 이름 피하기)
- [x] `"C:\Users\..."` 경로가 `SyntaxError` 나던 것 → `r"..."` 또는 `/`
- [x] `with open() as f` — 인자와 콜론(`:`) 누락
- [x] `with` 블록 안의 불필요한 `f.close()` 제거
- [x] `print("길이:", num)` — `num` 은 길이가 아니라 마지막 반복 번호. 줄 수는 `len(readlines())`
- [x] 오타 `ouput` → `output`

**막혔던 부분 / 질문**
- [ ] `else` 에 쓸 코드와 `try` 맨 끝에 둘 코드의 차이
- [ ] `except (A, B) as e` 와 `except A` / `except B` 를 나눠 쓰는 것 중 언제 무엇을 고르는지
- [ ] `mode='w'` 로 열면 기존 내용이 지워지는데, 이어 쓰려면 `'a'` — 실수로 `'w'` 를 쓰면 복구할 방법이 있는지
- [ ] `encoding="utf-8"` 을 빼면 실제로 어떤 환경에서 한글이 깨지는지
- [ ] `with` 를 중첩해서 파일 두 개를 동시에 열 수 있는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 에러와 예외 (`try`, `except`, `else`, `finally`)](https://docs.python.org/ko/3/tutorial/errors.html)
- [내장 예외 목록 (`NameError`, `ZeroDivisionError`, `FileNotFoundError` 등)](https://docs.python.org/ko/3/library/exceptions.html)
- [파이썬 공식 튜토리얼 — 파일 읽고 쓰기 (`open`, `with`)](https://docs.python.org/ko/3/tutorial/inputoutput.html#reading-and-writing-files)
- [문자열 리터럴 — raw string (`r"..."`)](https://docs.python.org/ko/3/reference/lexical_analysis.html#string-and-bytes-literals)
