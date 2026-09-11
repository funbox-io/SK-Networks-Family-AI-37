---
day: 005
date: 2026-09-10
weekday: 목
week: 2
phase: 프로그래밍과 데이터 기초
title: 파이썬 예외 처리와 파일 처리 — try · except · else · finally, open · with
tags: python, exception, try, except, else, finally, ValueError, TypeError, ZeroDivisionError, IndexError, KeyError, FileNotFoundError, file, open, with, encoding, read, readline, readlines, write, writelines, close
---

# Day 005 · 2026-09-10 (목)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 에러가 나도 프로그램이 멈추지 않게 하는 예외 처리(`try` / `except` / `else` / `finally`)를 배우고, 파일을 읽고 쓰는 `open` · `with` 사용법을 익혔다.

📂 실습 노트북 → [`lecture/python_exception_file.ipynb`](./lecture/python_exception_file.ipynb) (`개념 설명 → 예제 코드 → 연습 문제` 구성, 총 3장 · 문제 15문항)

---

## 1. 예외 처리 (Exception Handling)

파이썬은 위에서 아래로 한 줄씩 순차 실행된다. 중간에 에러가 나면 **그 즉시 프로그램이 멈추고 아래 코드는 실행되지 않는다.**

예외 처리를 쓰면 에러가 나도 프로그램이 죽지 않고, 대신 준비해둔 코드로 넘어가서 계속 실행된다.

```python
try:
    # 에러가 날 수 있는 코드
    num = int(input("숫자 입력: "))
    print(10 / num)
except:
    # 에러가 났을 때 대신 실행되는 코드
    print("잘못된 입력입니다.")

print("프로그램은 계속 실행됩니다.")  # 에러가 나도 이 줄은 실행됨
```

흐름은 이렇다.

> `try` 안에서 에러 발생 → 남은 `try` 코드는 건너뜀 → `except` 실행 → 그 아래 코드 정상 진행

---

## 2. 명시적 예외 처리 (에러 종류를 지정)

`except` 뒤에 에러 이름을 적어두면 **그 에러만** 잡는다. 다른 종류의 에러가 나면 잡지 못하고 프로그램이 멈춘다. 대신 "무슨 에러인지 정확히 알고 대응"할 수 있다는 게 장점이다.

```python
try:
    num = int(input("숫자 입력: "))
    print(10 / num)
except ValueError:          # 숫자가 아닌 걸 입력했을 때
    print("숫자만 입력하세요.")
except ZeroDivisionError:   # 0으로 나눴을 때
    print("0으로 나눌 수 없습니다.")
```

**자주 쓰는 에러 종류**

| 에러 이름 | 언제 발생하나 |
|-----------|---------------|
| `ValueError` | 값의 형태가 잘못됨 (`int("가나다")`) |
| `TypeError` | 자료형이 안 맞음 (`"3" + 5`) |
| `ZeroDivisionError` | 0으로 나눔 |
| `IndexError` | 리스트 범위를 벗어난 인덱스 |
| `KeyError` | 딕셔너리에 없는 키 |
| `FileNotFoundError` | 파일이 존재하지 않음 |

---

## 3. 포괄적 예외 처리 (모든 에러를 한 번에)

에러 이름을 안 적거나 `Exception` 을 쓰면 **모든 에러**를 잡는다.

```python
try:
    ...
except Exception as e:   # as e → 에러 내용을 변수 e에 담음
    print("에러 발생:", e)
```

- **명시적** : 정확하지만 예상 못 한 에러는 놓침
- **포괄적** : 안전망 역할이지만 무슨 에러인지 뭉개져서 디버깅이 어려움

실무에서는 **명시적으로 먼저 쓰고, 맨 마지막에 포괄적으로 마무리**하는 방식을 쓴다.

```python
try:
    ...
except ValueError:
    print("값 오류")
except Exception as e:   # 위에서 못 잡은 나머지 전부
    print("기타 오류:", e)
else:
    print("에러가 없을 때만 실행")
finally:
    print("에러가 있든 없든 무조건 실행")   # 파일 닫기 등 마무리 작업
```

| 절 | 언제 실행되나 |
|----|---------------|
| `try` | 먼저 실행되는 코드 |
| `except` | `try` 에서 에러가 났을 때 |
| `else` | **에러가 없을 때만** |
| `finally` | **에러가 있든 없든 무조건** |

---

## 4. 파일 처리

**인코딩(encoding)** 이란 사람이 읽는 텍스트(문자)를 컴퓨터가 저장하는 숫자로 바꾸는 규칙이다. 한글은 `utf-8` 을 지정하지 않으면 깨질 수 있으므로 항상 `encoding="utf-8"` 을 붙이는 습관을 들이자.

**모드**

| 모드 | 의미 |
|------|------|
| `"w"` | 쓰기 — 파일이 없으면 새로 만들고, 있으면 기존 내용 전부 삭제 |
| `"a"` | 추가 — 기존 내용 뒤에 이어서 씀 |
| `"r"` | 읽기 — 파일이 없으면 `FileNotFoundError` |

**쓰기 메서드**

| 쓰기 | 설명 |
|------|------|
| `write("문자열")` | 문자열 하나를 씀 (줄바꿈은 `\n` 을 직접 넣어야 함) |
| `writelines(리스트)` | 리스트에 든 문자열들을 이어서 씀 |

**읽기 메서드**

| 읽기 | 결과 |
|------|------|
| `read()` | 파일 전체를 하나의 문자열로 |
| `readline()` | 한 줄만 문자열로 |
| `readlines()` | 전체를 줄 단위 리스트로 (`['1줄\n', '2줄\n']`) |

### 기본 방식 — 반드시 `close()` 로 닫아야 저장이 완료된다

```python
f = open("test.txt", "w", encoding="utf-8")
f.write("안녕하세요!")
f.close()   # 안 닫으면 내용이 저장 안 될 수 있음
```

### with 방식 (권장)

블록이 끝나면 자동으로 닫아준다. 중간에 에러가 나도 닫히기 때문에 훨씬 안전하다.

```python
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("반갑습니다.")
# 여기서 자동으로 close()
```

### 읽기 + 예외 처리를 합친 실전 형태

```python
try:
    with open("test.txt", "r", encoding="utf-8") as f:
        for line in f:          # 줄 단위로 하나씩 읽기 (메모리 효율적)
            print(line.strip()) # strip() → 줄 끝의 \n 제거
except FileNotFoundError:
    print("파일이 없습니다.")
```

---

## 🔁 복습

**직접 해본 것**
- 에러 6종(`ValueError` `TypeError` `ZeroDivisionError` `IndexError` `KeyError` `FileNotFoundError`)을 하나씩 일부러 일으켜 `as e` 로 메시지 확인
- 같은 입력값 묶음(`"5"` / `"0"` / `"가나다"`)을 포괄적 `except` 와 명시적 `except` 두 방식으로 처리해 결과 비교
- 정상 / `ValueError` / `ZeroDivisionError` 세 경우에 `else` 와 `finally` 가 각각 실행되는지 확인
- `"w"` 로 쓰고 `"a"` 로 덧붙인 뒤 `read()` · `readline()` · `readlines()` 결과 형태 비교
- `with` 블록을 벗어난 뒤 `f.closed` 가 `True` 인지 확인
- 없는 파일을 `"r"` 로 열어 `FileNotFoundError` 를 잡고, 그 뒤 코드가 계속 실행되는지 확인
- 연습 15문항 — 정수 변환 실패 시 기본값 돌려주기, 안전한 나눗셈, 인덱스·키 에러 처리(`get()` 과 비교), 에러 이름과 메시지 출력, `continue` 로 에러 건너뛰며 합계 내기, 리스트를 파일로 저장 후 다시 리스트로 되돌리기, `a` 모드로 덧붙이기, 줄 수·글자 수 세기, 점수 파일 평균 내기, 로그 파일 기록 함수, 에러를 로그로 남기고 계속 진행하기, 특정 단어가 든 줄만 골라내기

**막혔던 부분 / 질문**
- [ ] `except:` 만 쓰는 것과 `except Exception as e:` 는 실제로 잡는 범위가 같은가
- [ ] `else` 는 `try` 맨 끝에 코드를 두는 것과 무엇이 다른가 — 왜 굳이 나눠 쓰는지
- [ ] `finally` 가 있는데도 `with` 를 권하는 이유
- [ ] `"w"` 모드로 열기만 하고 아무것도 안 쓰면 기존 내용이 지워지는지
- [ ] `readline()` 을 여러 번 부르면 어디서부터 읽히는지 (파일 위치 개념)
- [ ] `for line in f:` 와 `readlines()` 는 결과가 같은데 왜 메모리 차이가 나는지

📂 [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 에러와 예외 (`try`, `except`, `else`, `finally`)](https://docs.python.org/ko/3/tutorial/errors.html)
- [내장 예외 목록 (`ValueError`, `KeyError`, `FileNotFoundError` 등)](https://docs.python.org/ko/3/library/exceptions.html)
- [파이썬 공식 튜토리얼 — 파일 읽고 쓰기 (`open`, `with`, `read`, `readline`)](https://docs.python.org/ko/3/tutorial/inputoutput.html#reading-and-writing-files)
- [`open()` 내장 함수 문서 — 모드와 encoding](https://docs.python.org/ko/3/library/functions.html#open)
