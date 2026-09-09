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

---

## 📚 수업

**주제**  
흐름 제어 — 반복문(for / while) · 조건문(if / elif / else) + 함수 · 메서드 복습

**핵심 키워드**  
`def` `return` `매개변수/인수` `키워드 인수` `lower()` `upper()` `capitalize()` `title()` `strip()` `replace()` `split()` `join()` `append()` `keys()` `values()` `items()` `get()` `for` `range()` `while` `break` `if` `elif` `else` `%` `f-string`

**배운 내용**
- 함수의 기본 구조 — `def 이름(매개변수):` → 실행 코드 → `return 값`. **매개변수**는 정의할 때 약속한 이름, **인수**는 호출할 때 실제로 넘기는 값.
- **키워드 인수** — `subtract(a=10, b=3)` 처럼 이름을 지정해 넘기면 순서를 바꿔도 된다.
- `return` 이 없는 함수는 값을 돌려주지 않고 **`None`** 이 된다. 출력만 하는 함수와 값을 돌려주는 함수는 역할이 다르다.
- 문자열 메서드 — `lower()`/`upper()`, `capitalize()`(첫 글자만), `title()`(단어마다 첫 글자), `strip()`(앞뒤 공백·줄바꿈 제거), `replace(옛것, 새것)`, `split(기준)`(→ 리스트), `구분자.join(리스트)`(→ 문자열).
- 문자열 메서드는 원본을 바꾸지 않고 **새 문자열을 돌려준다** → `text.strip()` 만 하면 아무 일도 일어나지 않고, `text = text.strip()` 처럼 **다시 대입**해야 결과가 남는다.
- 메서드는 `.` 으로 이어 붙여 한 번에 처리할 수 있다 — `text.replace(...).upper().strip()` 은 **왼쪽부터 차례대로** 실행된다.
- 리스트·딕셔너리 메서드 — `append(값)`, `len(자료형)`, `keys()` / `values()` / `items()`, `get(key)`(없으면 `None`).
- 리스트는 **함수 안에서 바꾸면 원본까지 바뀐다** — `target_list.append(value)` 를 함수 안에서 하면 호출한 쪽의 리스트도 함께 늘어난다.
- `for 변수 in 데이터:` — 리스트는 **원소**를, 문자열은 **글자 하나씩**을 꺼낸다. 딕셔너리를 그냥 반복하면 **key** 가 꺼내지고, key·value 를 함께 쓰려면 `for k, v in d.items():`.
- `range()` — `range(끝)` 은 `0`부터 `끝-1`까지, `range(시작, 끝)` 은 `시작`부터 `끝-1`까지. 그대로 출력하면 `range(0, 5)` 라고만 나오므로 **`list()` 로 감싸야** 내용을 볼 수 있다.
- `while 조건식:` — 조건이 참인 동안 계속 반복한다. 파이썬에는 `++count` 같은 **증감 연산자가 없어서** `count += 1` / `count -= 1` 로 써야 하고, 이 줄을 빠뜨리면 **무한 루프**가 된다.
- `while True:` 는 조건이 항상 참이므로 안쪽에 반드시 `break` 로 빠져나갈 길을 만들어 준다. 사용자 입력을 받을 때는 `int(input(...))` 과 함께 쓴다.
- `if ~ else` — 조건식의 결과는 항상 `True` / `False`(bool). 조건식만 따로 출력해 보면 확인할 수 있다.
- `if ~ elif ~ else` — **위에서부터 순서대로** 검사해 처음 참이 되는 곳만 실행하고 빠져나온다. 그래서 **범위가 좁은 조건(큰 값)부터** 써야 하고, 경계값을 놓치지 않으려면 `>=` 를 쓴다.
- 반복문 + 조건문 조합 패턴 — `%` 로 짝수/배수 판별(`number % 2 == 0`, `% 3 == 0`), 조건에 맞는 값만 새 리스트에 `append`, 누적 변수(`total += price`), 첫 값을 임시 최댓값으로 두고 갱신하기.
- 값이 이미 `True` / `False` 면 `if user.get('active') == True` 가 아니라 **`if user.get('active'):`** 로 충분하다.
- 변수 이름 주의 — `sum` 은 내장 함수 이름이라 변수명으로 쓰지 않는다(`total_price` 등으로).

📂 [수업 자료 폴더](./lecture/) — 실습 노트북 [`lecture/python_loops_conditions.ipynb`](./lecture/python_loops_conditions.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 5장 · 문제 43문항)

---

## 🔁 복습

**다시 정리한 것**
- 수업 내용을 실행 가능한 노트북으로 다시 작성 → [`lecture/python_loops_conditions.ipynb`](./lecture/python_loops_conditions.ipynb)
- 표로 정리한 것: 문자열 메서드 7종, 리스트·딕셔너리 메서드 6종
- 단원 구성 — ① 함수(1~5번) ② 자료형별 메서드(6~22번) ③ 반복문 ④ 조건문(연습 1~6번) ⑤ 종합 응용(1~15번)
- 필기에서 헷갈렸던 부분을 주석으로 바로잡음
  - f-string 안에서 변수를 넣을 때는 **중괄호 `{}`** — `[]` 를 쓰면 그냥 글자로 출력된다
  - `strip()` 결과를 다시 대입하지 않아 원본이 그대로였던 것
  - `range(len(...))` 은 값이 아니라 **번호**를 꺼낸다 → 값을 쓰려면 리스트를 직접 반복
  - `== True` 는 불필요, `sum` 을 변수명으로 쓰지 않기

**막혔던 부분 / 질문**
- [ ] 파이썬에 `++` 가 없어서 `count += 1` 을 빠뜨리면 무한 루프 — while 문을 쓸 때마다 종료 조건 먼저 확인하기
- [ ] `if` / `elif` 순서를 바꾸면 결과가 달라지는 이유 (범위가 넓은 조건을 위에 두면 아래 조건이 실행되지 않음)
- [ ] 문자열 메서드는 새 값을 돌려주는데 `리스트.append()` 는 원본을 바꾸는 차이 (immutable vs mutable)
- [ ] 함수에 리스트를 넘기면 원본이 바뀌는 이유 — 값이 아니라 무엇이 전달되는 걸까
- [ ] `range()` 를 그대로 출력하면 왜 숫자가 안 보이는지, `list()` 로 감싸야 하는 이유
- [ ] `while True` + `break` 와 조건식을 직접 쓰는 `while` 중 언제 무엇을 고르는지

**직접 해본 것**
- 곱셈·뺄셈(키워드 인수)·제곱·문자열 연결 함수를 만들고, `return` 없는 함수도 만들어 비교
- `lower / upper / capitalize / title / strip / replace / split / join` 을 하나씩 실행해 결과 비교
- `split(',')` 로 자른 리스트를 `" ".join(...)` 으로 되돌려 보기
- 딕셔너리를 `keys()` `values()` `items()` `get()` 으로 각각 꺼내 출력 형태 확인
- 리스트·딕셔너리·문자열을 `for` 로 각각 반복해 꺼내지는 값이 무엇인지 확인
- `range(0, 5)` 를 그대로 / `list()` 로 감싸서 출력 비교
- `count -= 1` 로 끝나는 `while` 과 `while True` + `break` 로 카운트다운 두 가지 방식 구현
- 종합 응용 15문항 — 짝수·홀수 분리, `.csv` 파일만 골라내기, 10,000원 이상 상품에만 할인율 적용, 글자 수 기준 단어 필터, 3의 배수 합계, 로그인 3회 실패 시 계정 잠금, 학생별 평균 계산 후 합격/불합격 판정, 반복문으로 최댓값 찾기, 장바구니 총액, 이메일 도메인 추출

📂 [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 흐름 제어 (`if`, `for`, `range`, `break`)](https://docs.python.org/ko/3/tutorial/controlflow.html)
- [문자열 메서드 문서 (`split`, `join`, `replace`, `strip`, `title`)](https://docs.python.org/ko/3/library/stdtypes.html#string-methods)
- [딕셔너리 메서드 문서 (`keys`, `values`, `items`, `get`)](https://docs.python.org/ko/3/library/stdtypes.html#mapping-types-dict)
- [`range` 자료형 문서](https://docs.python.org/ko/3/library/stdtypes.html#range)
