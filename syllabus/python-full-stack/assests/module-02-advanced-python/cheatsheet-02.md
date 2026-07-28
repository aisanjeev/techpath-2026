# Cheat Sheet — Advanced Python

**Module 02 | Quick Reference Card**

---

## OOP Basics

```python
class Student:
    institute = "TechPath"           # Class attribute (shared)

    def __init__(self, name, fee):   # Constructor
        self.name = name             # Instance attribute (per-object)
        self.fee = fee

    def __str__(self):               # print(obj) / str(obj)
        return f"{self.name}: ₹{self.fee}"

    def __repr__(self):              # repr(obj) / REPL
        return f"Student('{self.name}', {self.fee})"

    @property                        # Computed attribute
    def fee_with_gst(self):
        return round(self.fee * 1.18, 2)

    @fee_with_gst.setter             # Setter
    def fee_with_gst(self, val):
        self.fee = round(val / 1.18, 2)

    @staticmethod                    # No self/cls
    def is_valid_fee(fee):
        return fee > 0

    @classmethod                     # Factory method
    def from_dict(cls, data):
        return cls(data["name"], data["fee"])
```

---

## Inheritance

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):               # Single inheritance
    def __init__(self, name, course):
        super().__init__(name)        # Call parent
        self.course = course

class Staff(Person, JsonMixin):       # Multiple inheritance
    pass

# Check
isinstance(obj, Student)             # True if Student or subclass
issubclass(Student, Person)           # True
Student.__mro__                       # Method Resolution Order
```

---

## Abstract Classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...     # Child MUST implement

    def describe(self):               # Concrete method — inherited
        return f"Area = {self.area()}"
```

---

## Dunder Methods

| Method | Trigger | Example |
|--------|---------|---------|
| `__init__` | `Cls()` | Constructor |
| `__str__` | `print()`, `str()` | Human string |
| `__repr__` | `repr()`, REPL | Dev string |
| `__eq__` | `==` | Equality |
| `__lt__` | `<` (enables `sort`) | Less than |
| `__add__` | `+` | Addition |
| `__len__` | `len()` | Length |
| `__getitem__` | `obj[k]` | Index/key access |
| `__contains__` | `in` | Membership |
| `__call__` | `obj()` | Callable object |
| `__bool__` | `bool()` / `if obj` | Truthiness |

---

## Functional Programming

```python
# map — transform every item
list(map(func, items))
list(map(lambda x: x * 2, [1, 2, 3]))        # [2, 4, 6]

# filter — keep matching items
list(filter(func, items))
list(filter(lambda x: x > 2, [1, 2, 3, 4]))  # [3, 4]

# reduce — combine into one
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])     # 10

# sorted with key
sorted(students, key=lambda s: s["marks"], reverse=True)
```

---

## itertools

```python
import itertools as it

it.chain(a, b)                    # Concatenate iterables
it.product(a, b)                  # Cartesian product
it.permutations(a, r)             # Order matters
it.combinations(a, r)             # Order doesn't matter
it.groupby(data, key=func)        # Group consecutive items
it.islice(iterable, stop)         # Slice any iterable
it.accumulate(data)               # Running totals
it.count(start, step)             # Infinite counter
it.cycle(iterable)                # Infinite repeat
it.repeat(val, times)             # Repeat value
```

---

## functools

```python
from functools import partial, lru_cache, wraps, total_ordering

calc_gst = partial(calc_fee, gst=0.18)       # Pre-fill args

@lru_cache(maxsize=128)                        # Memoize
def fib(n): ...

@wraps(func)                                   # In decorators
def wrapper(*a, **kw): ...

@total_ordering                                 # Auto-gen comparisons
class X:
    def __eq__: ...
    def __lt__: ...
```

---

## Generators

```python
# Generator function
def gen():
    yield 1
    yield 2

# Generator expression
g = (x**2 for x in range(10))

# Consume
next(g)                           # One value
list(g)                           # All remaining
for x in gen(): ...               # Loop

# yield from — delegate
def combined():
    yield from gen_a()
    yield from gen_b()
```

---

## Decorators

```python
# Basic decorator
def my_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

@my_dec
def f(): ...

# Decorator with arguments
def my_dec(arg):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

@my_dec(arg="value")
def f(): ...

# Stacking (bottom → up)
@dec_a       # Applied second
@dec_b       # Applied first
def f(): ...
```

---

## Async

```python
import asyncio

async def fetch(url):                          # Coroutine
    await asyncio.sleep(1)                     # Non-blocking wait
    return "data"

async def main():
    # Sequential
    r1 = await fetch("url1")
    r2 = await fetch("url2")

    # Concurrent
    r1, r2 = await asyncio.gather(
        fetch("url1"), fetch("url2")
    )

    # Fire-and-forget
    task = asyncio.create_task(fetch("url3"))

asyncio.run(main())                            # Start event loop
```

---

## Type Hints

```python
# Variables
name: str = "Rahul"
marks: list[int] = [85, 92]
info: dict[str, str] = {"city": "Bhopal"}

# Functions
def greet(name: str) -> str: ...
def find(id: int) -> Optional[dict]: ...       # dict | None
def process(x: Union[int, str]) -> None: ...   # int or str
def log(msg: Any) -> None: ...                 # anything

# Collections (3.9+)
list[int]    dict[str, int]    tuple[str, int]    set[str]

# Advanced
Callable[[int, str], bool]                     # Function type
Literal["admin", "student"]                    # Specific values
TypeAlias = dict[str, list[int]]               # Named type
```

---

## dataclass / NamedTuple / Pydantic

```python
# dataclass
from dataclasses import dataclass, field
@dataclass
class Student:
    name: str
    marks: list[int] = field(default_factory=list)

# NamedTuple (immutable)
from typing import NamedTuple
class Point(NamedTuple):
    x: float
    y: float

# Pydantic (validates + converts)
from pydantic import BaseModel, Field
class Student(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=16, le=60)

s = Student(name="Rahul", age="22")     # age auto-converted to int
s.model_dump()                           # → dict
s.model_dump_json()                      # → JSON string
Student.model_validate(dict_data)        # dict → model
```

---

## pytest

```bash
pytest                                   # Run all
pytest tests/test_x.py                   # Run file
pytest tests/test_x.py::test_func        # Run one test
pytest -v                                # Verbose
pytest -x                                # Stop on first fail
pytest -k "grade"                        # By keyword
pytest --cov=app                         # Coverage
```

```python
# Basic test
def test_add():
    assert add(2, 3) == 5

# Test exceptions
def test_error():
    with pytest.raises(ValueError, match="negative"):
        func(-1)

# Fixture
@pytest.fixture
def student():
    return {"name": "Rahul", "marks": [85]}

def test_name(student):
    assert student["name"] == "Rahul"

# Parametrize
@pytest.mark.parametrize("input,expected", [
    (90, "A+"), (80, "A"), (59, "F"),
])
def test_grade(input, expected):
    assert get_grade(input) == expected

# Mock
from unittest.mock import patch, MagicMock
@patch("module.requests.get")
def test_api(mock_get):
    mock_get.return_value.json.return_value = {"name": "Rahul"}
    result = fetch_student(1)
    assert result["name"] == "Rahul"
```
