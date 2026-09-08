---
day: 003
date: 2026-09-08
weekday: 화
week: 2
phase: 프로그래밍과 데이터 기초
title: 파이썬 함수 — 사용자 정의 함수 · 리스트 · 딕셔너리 · 문자열 전용 함수
tags: python, function, def, return, append, extend, insert, keys, values, items, get, split, join, replace, strip
---

# Day 003 · 2026-09-08 (화)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 기능을 이름으로 묶어 재사용하는 함수를 직접 만들어 보고, 리스트·딕셔너리·문자열에 딸린 전용 함수를 정리했다.

---

## 📚 수업

**주제**  
함수(Function) — 내장 함수 · 전용 함수(메서드) · 사용자 정의 함수

**핵심 키워드**  
`def` `return` `매개변수/인수` `기본값` `None` `append()` `insert()` `extend()` `clear()` `len()` `keys()` `values()` `items()` `get()` `lower()` `split()` `join()` `replace()` `strip()` `immutable`

**배운 내용**
- 함수는 **같은 코드를 여러 번 쓰지 않도록 기능을 이름으로 묶어 둔 것**. 재료(인수)를 넣으면 결과를 돌려주는 자판기와 같다.
- 함수의 세 종류 — 파이썬이 기본 제공하는 **내장 함수**(`print()`, `len()`, `type()`), 특정 자료형에만 딸린 **전용 함수(메서드)**(`리스트.append()`), 내가 만드는 **사용자 정의 함수**(`def`).
- 정의는 `def 이름(매개변수):` → 실행 코드 → `return 값`. **매개변수**는 정의할 때 적는 이름, **인수**는 호출할 때 넣는 실제 값.
- 정의만 해서는 실행되지 않는다. **`이름(인수)` 로 호출**해야 동작하고, 한 번 만들면 값만 바꿔 몇 번이든 재사용할 수 있다.
- 매개변수에 `= 값` 을 적어 두면 **기본값**이 되어 호출할 때 그 자리를 생략할 수 있다.
- `return` 이 없는 함수는 **`None`** 을 돌려준다. 출력만 하는 함수와 값을 돌려주는 함수는 다르다.
- 리스트 전용 함수 — `append(값)` 은 맨 뒤에 하나, `insert(위치, 값)` 은 원하는 자리에 끼워 넣기, `extend(리스트)` 는 다른 리스트를 통째로 이어 붙이기.
- **원본을 직접 바꾸는 함수는 돌려주는 값이 `None`** — `output = list_data.append(10)` 처럼 쓰면 `output` 에는 `None` 이 담긴다. 원본만 바뀐다.
- `A.extend(B)` 는 A 자체가 늘어나고, `A + B` 는 원본을 두고 **합쳐진 새 리스트**를 돌려준다.
- 딕셔너리 전용 함수 — `keys()` / `values()` / `items()` 는 각각 key, value, (key, value) 쌍을 돌려준다. 리스트가 아니라 `dict_keys` 같은 전용 자료형이라 `list()` 로 바꿔 쓰기도 한다.
- `get(key)` 는 없는 key 여도 에러 없이 `None` 을 돌려준다. `get(key, 기본값)` 으로 대체값도 지정할 수 있다. 값을 **읽기만** 할 뿐 없는 key 를 만들어 주지는 않는다.
- 문자열 전용 함수 — `lower()`/`upper()`, `split(기준)`(잘라서 **리스트**로), `기준.join(리스트)`(이어 붙여 **문자열**로), `replace(찾을값, 바꿀값)`, `strip()`(앞뒤 공백·줄바꿈 제거).
- 문자열은 **immutable** 이라 이 함수들은 원본을 바꾸지 않고 **새 문자열을 돌려준다** → 결과를 반드시 변수에 담아야 한다.
- `split()` 은 기준을 적지 않으면 **공백**을 기준으로 자른다. `join()` 은 `split()` 의 반대 기능.

📂 [수업 자료 폴더](./lecture/) — 실습 노트북 [`lecture/python_functions.ipynb`](./lecture/python_functions.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 5장)

---

## 🔁 복습

**다시 정리한 것**
- 수업 시간에 만든 실습 노트북을 개념별로 다시 정리 → [`lecture/python_functions.ipynb`](./lecture/python_functions.ipynb)
- 표로 정리한 것: 함수 세 종류 비교, 리스트 전용 함수 정리, 딕셔너리 전용 함수와 돌려주는 값, 문자열 전용 함수 정리, `extend()` vs `+` 차이, `[key]` vs `.get()` 차이
- 변수 이름을 **데이터가 무엇인지 드러나게** 다시 지음 (`output1`, `clist2`, `data` → `sum_result`, `shopping_list`, `word_list`)
- 예제를 실생활 상황으로 바꿔서 정리 — 장바구니(리스트 추가), 대기 줄(insert), 회원·배우 정보(딕셔너리), 이메일 주소 분리(split), 입력값 정리(strip)

**막혔던 부분 / 질문**
- [ ] `output = list_data.append(10)` 이 왜 `None` 이 되는지 — 원본을 바꾸는 함수와 새 값을 돌려주는 함수의 구분
- [ ] `extend()` 와 `+` 중 언제 무엇을 써야 하는지 (원본을 바꿔도 되는 상황인지)
- [ ] `keys()` 가 돌려주는 `dict_keys` 는 리스트와 뭐가 다른지, 언제 `list()` 로 바꿔야 하는지
- [ ] 문자열 함수를 썼는데 원본이 그대로인 이유 — immutable 개념
- [ ] `split()` 에 기준을 넣을 때와 비워 둘 때의 결과 차이
- [ ] `return` 을 쓰는 함수와 `print()` 만 하는 함수를 언제 나눠 만들어야 하는지

**직접 해본 것**
- `add()` 함수를 만들어 여러 값으로 반복 호출하고, 기본값 매개변수(`tax_rate=0.1`)로 세율 계산 함수 작성
- `return` 없는 함수의 반환값이 `None` 인 것을 직접 출력해서 확인
- 빈 리스트에 `append()` 로 하나씩 담고, `insert()` 로 중간에 끼워 넣어 인덱스가 밀리는 것 확인
- `extend()` 로 합친 결과와 `+` 로 합친 결과에서 원본이 어떻게 달라지는지 비교
- `keys()`, `values()`, `items()` 의 자료형을 `type()` 으로 확인하고 `list()` 로 변환
- 없는 key 를 `[]` 와 `.get()` 으로 각각 꺼내 KeyError / None 차이 확인 (`try/except KeyError`)
- `split()` → `join()` 왕복, `replace()` 로 문장 바꾸기, `strip()` 전후 길이 비교
- 단원별 연습 문제 풀이 — 곱셈·평균·짝수 판별 함수, 과일 리스트 조작, 상품 딕셔너리 순회, 이메일 분리

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 함수 정의하기](https://docs.python.org/ko/3/tutorial/controlflow.html#defining-functions)
- [내장 함수 목록](https://docs.python.org/ko/3/library/functions.html)
- [문자열 메서드 문서 (`split`, `join`, `replace`, `strip`)](https://docs.python.org/ko/3/library/stdtypes.html#string-methods)
- [딕셔너리 메서드 문서 (`keys`, `values`, `items`, `get`)](https://docs.python.org/ko/3/library/stdtypes.html#mapping-types-dict)
