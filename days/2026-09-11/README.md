---
day: 006
date: 2026-09-11
weekday: 금
week: 2
phase: 프로그래밍과 데이터 기초
title: 클래스와 상속 — 커스텀 자료형 만들기, 그리고 라이브러리 · 모듈
tags: python, class, object, instance, __init__, self, 속성, 메서드, 상속, super, 오버라이딩, library, package, module, random, sample, requests
---

# Day 006 · 2026-09-11 (금)

`프로그래밍과 데이터 기초` · 2주차

> **한 줄 요약** — 클래스로 나만의 자료형(고객 정보)을 만들고, 상속과 오버라이딩으로 VIP 고객을 확장한 뒤, 내장 모듈(`random`)과 외부 라이브러리(`requests`)를 불러 써 봤다.

📂 실습 노트북 → [`lecture/python_class_inheritance_library.ipynb`](./lecture/python_class_inheritance_library.ipynb) (수업 필기를 실행 가능하도록 정리, 총 5장)

---

## 1. 클래스(Class)와 객체(Object)

클래스는 **나만의 커스텀 자료형**이다.
`int` `str` `list` 처럼 파이썬이 미리 만들어 둔 자료형이 있듯이, 내가 다루려는 대상(고객, 상품, 학생 …)을 직접 자료형으로 정의하는 것이다.

| 용어 | 뜻 |
|------|-----|
| **클래스(class)** | 설계도. 어떤 데이터와 기능을 가질지 정의한다 |
| **객체(object) · 인스턴스(instance)** | 설계도로 실제로 찍어낸 것 |
| **속성(attribute)** | 객체가 가지고 있는 **데이터** (`self.name`) |
| **메서드(method)** | 객체가 할 수 있는 **기능** (`purchase()`) |
| **생성자 `__init__()`** | 객체를 만들 때 **자동으로 한 번** 실행되는 초기화 함수 |
| **`self`** | 만들어진 **그 객체 자신**. 모든 메서드의 첫 번째 매개변수 |

이름 규칙 — **클래스명은 대문자로 시작**(`Customer`), **함수·메서드명은 소문자**(`purchase`).

```python
class Customer:
    # 생성자 : 객체를 만들 때 자동으로 실행된다
    def __init__(self, name, age, sex):
        self.name = name      # 넘겨받은 값을 객체의 속성으로 저장
        self.age = age
        self.sex = sex

    # 인스턴스 메서드 : 첫 번째 매개변수는 항상 self
    def purchase(self, price, product_name):
        print(f"[{self.name}] 고객님이 {price:,}원 상당의 {product_name}를 구매하셨습니다.")
```

### 객체 생성과 메서드 호출

`객체 = 클래스이름(값1, 값2, ...)` 형태로 만든다. 이때 넘긴 값이 `__init__` 의 매개변수로 들어간다.

```python
obj1 = Customer(name='문진호', age=20, sex='남성')   # 키워드 인수 -> 순서 바꿔도 됨
obj2 = Customer('지현', 25, '여성')                  # 순서대로 넘겨도 됨

print(obj1.name)                     # 속성 꺼내기
obj1.purchase(20000, "아이패드")       # 메서드 호출
print(type(obj1))                    # <class 'Customer'>
```

> ⚠️ `Customer()` 처럼 값을 빠뜨리면 **TypeError**. `__init__` 이 `name, age, sex` 세 개를 요구한다.

### 사실 내장 자료형도 클래스다

필기에 적은 `[]` 와 `list()` 가 같다는 말이 바로 그 얘기다. `list` 는 파이썬이 미리 만들어 둔 **클래스**이고, `list()` 는 그 클래스로 객체를 만드는 것이다.

```python
print([] == list())          # True

list(10, 20, 30)             # TypeError! 값 여러 개가 아니라
list([10, 20, 30])           # 반복 가능한 것 하나를 받는다
```

---

## 2. 상속(Inheritance)

이미 만든 클래스를 **그대로 물려받아** 새 클래스를 만드는 것이다.

| 용어 | 뜻 |
|------|-----|
| **부모 클래스 (Super Class)** | 물려주는 쪽 |
| **자식 클래스 (Sub Class)** | 물려받는 쪽 |

- **코드 재사용성** — 부모 코드를 다시 쓰지 않아도 된다
- **유지 보수** — 공통 기능은 부모 **한 곳만** 고치면 된다
- **확장성** — 기존 코드를 두고 필요한 것만 추가한다
- 물려받는 방향은 **부모 → 자식** 한쪽뿐이다. 자식이 부모에게 줄 수는 없다

```python
class VIPCustomer(Customer):        # 괄호 안에 부모 클래스를 적는다
    def __init__(self, name, age, sex, discount_rate=0.1):
        super().__init__(name, age, sex)     # 부모의 __init__ 실행 (공통 속성)
        self.discount_rate = discount_rate   # 자식만 갖는 속성 추가

    # 메서드 오버라이딩 : 부모와 이름·매개변수를 맞춰야 바꿔치기가 된다
    def purchase(self, price, product_name):
        discount_price = int(price * (1 - self.discount_rate))
        print(f"[VIP] [{self.name}] 고객님이 "
              f"[{self.discount_rate * 100:.0f}]% 할인받아 "
              f"{discount_price:,}원에 {product_name}를 구매하셨습니다.")
```

- `super().__init__(...)` — 부모의 생성자를 불러 공통 속성을 그대로 초기화한다
- **메서드 오버라이딩** — 부모에게 물려받은 메서드를 **같은 이름으로 다시 정의**해 바꿔 쓰는 것

```python
vip_data = VIPCustomer("jinho", 30, "male", discount_rate=0.1)

print(vip_data.name)                  # 부모에게서 물려받은 속성
vip_data.purchase(20000, "아이패드")    # 오버라이딩한 메서드가 대신 실행된다
# [VIP] [jinho] 고객님이 [10]% 할인받아 18,000원에 아이패드를 구매하셨습니다.
```

---

## 3. 라이브러리 · 패키지 · 모듈

셋은 **크기 순서**로 이해하면 쉽다.

| 용어 | 단위 | 예 |
|------|------|-----|
| **모듈(module)** | 파이썬 파일 하나 (`.py`) | `random`, `os` |
| **패키지(package)** | 모듈 여러 개를 담은 폴더 | `urllib`, `matplotlib.pyplot` |
| **라이브러리(library)** | 패키지·모듈을 묶어 배포하는 단위 | `requests`, `pandas` |

- **내장(built-in)** — 파이썬을 깔면 이미 들어 있다 (`random`, `os`, `datetime`)
- **외부(external)** — `pip install` 로 따로 설치해야 한다 (`requests`, `pandas`)

```python
import random                  # 모듈 전체 -> random.sample(...) 처럼 모듈명을 붙여 쓴다
from random import sample      # 함수 하나만 -> sample(...) 로 바로 쓴다
```

| 분야 | 대표 라이브러리 |
|------|-----------|
| 시각화 | `matplotlib` `seaborn` `plotly` |
| 데이터 분석 | `pandas` |
| 웹 요청 | `requests` |

### 내장 모듈 `random` — 로또 번호 뽑기

`sample(대상, 개수)` 는 **중복 없이** 원하는 개수를 뽑아 리스트로 돌려준다.

```python
from random import sample

numbers = range(1, 46)          # 1 ~ 45 (46은 포함되지 않는다)

list_data = []
for loop in range(0, 5):        # 5줄짜리 로또 한 장
    info = sample(numbers, 6)   # 중복 없이 6개
    info.sort()
    list_data.append(info)
```

---

## 4. 외부 라이브러리 `requests` — 웹 페이지 HTML 가져오기

`pip install requests` 로 설치한 뒤 쓴다. `requests.get(주소)` 가 서버에 요청을 보내고, `.text` 에 응답 본문(HTML)이 들어 있다.

| 속성 | 뜻 |
|------|-----|
| `.status_code` | 응답 코드 (`200` 이면 정상) |
| `.text` | 본문을 문자열로 |
| `.content` | 본문을 바이트로 |

```python
import requests

url = "https://www.google.com"
output = requests.get(url, timeout=5)

print(output.status_code)      # 200
print(output.text[:300])       # 전체를 찍으면 수만 자가 쏟아진다
```

---

## 🔁 복습

**필기에서 고친 부분**
- [x] `seif` → **`self`** (오타)
- [x] "속성: 여러 기능 종류" → 속성은 **데이터**, 기능은 **메서드**. 둘을 나눠 정리
- [x] `test = Customer()` 는 **TypeError** — `__init__` 이 요구하는 값을 빠뜨릴 수 없다
- [x] `list(10, 20, 30)` 은 **TypeError** — `list([10, 20, 30])` 처럼 반복 가능한 것 하나를 넘긴다
- [x] `화장성` → **확장성**, `부모 콛드` → **부모 코드** (오타)
- [x] 클래스명 `VIPCUStomer` → **`VIPCustomer`**, `"mele"` → `"male"` (오타)
- [x] `vip_data = ...` 가 주석 처리된 채 `vip_data.purchase(...)` 를 불러 **NameError** 나던 것
- [x] `self.discount_price` → **지역 변수**. 그 순간 계산해 쓰고 마는 값이라 속성으로 남길 이유가 없다
- [x] 로또 주석 "중복 없이 6까지 숫자 선택" → 실제로는 **1~45 중 6개**. `for` 문은 **줄 수**를 정하는 것
- [x] `print(output.text)` 로 HTML 전체를 쏟아내던 것 → **앞부분 300자만**, `status_code` 확인 추가

**막혔던 부분 / 질문**
- [ ] `self` 를 매개변수에 적는데 호출할 때는 왜 안 넘기는지
- [ ] `super().__init__()` 을 빼먹으면 어떻게 되는지 (부모 속성이 아예 안 생기는지)
- [ ] 오버라이딩할 때 매개변수를 부모와 다르게 쓰면 어떤 문제가 생기는지
- [ ] 객체 속성(`self.x`)과 메서드 안 지역 변수의 수명 차이
- [ ] `import 모듈` 과 `from 모듈 import 함수` 중 언제 무엇을 고르는지
- [ ] `requests.get()` 이 실패하는 경우(네트워크, 404)를 어떻게 다뤄야 하는지

📂 [수업 자료 폴더](./lecture/) · [복습 자료 폴더](./review/)

---

## 🔗 참고 링크

- [파이썬 공식 튜토리얼 — 클래스](https://docs.python.org/ko/3/tutorial/classes.html)
- [파이썬 공식 튜토리얼 — 상속](https://docs.python.org/ko/3/tutorial/classes.html#inheritance)
- [파이썬 공식 튜토리얼 — 모듈과 패키지](https://docs.python.org/ko/3/tutorial/modules.html)
- [`random` 모듈 문서 (`sample`)](https://docs.python.org/ko/3/library/random.html#random.sample)
- [requests 공식 문서](https://requests.readthedocs.io/en/latest/)

