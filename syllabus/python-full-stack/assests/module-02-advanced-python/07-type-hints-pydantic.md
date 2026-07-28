# Type Hints & Pydantic

**Module 02 — Advanced Python | Topic 7**

---

## Why Type Hints?

Python is dynamically typed — you can put any type in any variable. This is flexible but can cause bugs:

```python
def calculate_fee(base, discount):
    return base * (1 - discount)

# This works
calculate_fee(25000, 0.10)    # 22500.0

# But what if someone passes wrong types?
calculate_fee("25000", "10%")    # TypeError at runtime!
```

Type hints let you document what types a function expects. They don't enforce types at runtime but help your editor catch mistakes and make code self-documenting.

```python
def calculate_fee(base: float, discount: float) -> float:
    return base * (1 - discount)
```

---

## Basic Type Hints

### Variable Annotations

```python
name: str = "Rahul"
age: int = 22
fee: float = 25000.0
is_enrolled: bool = True
nothing: None = None
```

### Function Annotations

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_total(prices: list, tax_rate: float = 0.18) -> float:
    subtotal = sum(prices)
    return round(subtotal * (1 + tax_rate), 2)

def print_header() -> None:
    print("TechPath Institute")
```

### Common Types from typing Module

```python
from typing import Optional, Union, Any

# Optional — can be the type OR None
def find_student(name: str) -> Optional[dict]:
    # Returns dict or None
    return None

# Union — can be one of multiple types
def process_id(student_id: Union[int, str]) -> str:
    return str(student_id)

# Any — accepts anything (avoid when possible)
def log(message: Any) -> None:
    print(message)
```

### Collection Types

```python
# Python 3.9+ — use built-in types directly
def process_marks(marks: list[int]) -> float:
    return sum(marks) / len(marks)

def get_student(data: dict[str, str]) -> str:
    return data["name"]

def get_cities(students: list[dict[str, str]]) -> set[str]:
    return {s["city"] for s in students}

# Tuple with specific types
def get_location() -> tuple[float, float]:
    return (23.26, 77.41)    # Bhopal coordinates
```

For Python 3.8 and earlier:

```python
from typing import List, Dict, Set, Tuple

def process_marks(marks: List[int]) -> float:
    return sum(marks) / len(marks)
```

---

## Advanced Type Hints

### Callable — Function Types

```python
from typing import Callable

def apply_discount(price: float, strategy: Callable[[float], float]) -> float:
    return strategy(price)

# Usage
student_discount: Callable[[float], float] = lambda p: p * 0.9
result = apply_discount(25000, student_discount)    # 22500.0
```

### Literal — Specific Values Only

```python
from typing import Literal

def set_role(user_id: int, role: Literal["admin", "student", "instructor"]) -> None:
    print(f"User {user_id} set to {role}")

set_role(1, "admin")       # OK
# set_role(1, "manager")   # mypy error: not a valid literal
```

### TypeAlias — Named Types

```python
from typing import TypeAlias

StudentRecord: TypeAlias = dict[str, str | int | float]
StudentList: TypeAlias = list[StudentRecord]

def process_batch(students: StudentList) -> int:
    return len(students)
```

---

## mypy — Static Type Checker

mypy checks your type hints without running the code.

```bash
pip install mypy
mypy your_file.py
```

```python
# file: student.py
def greet(name: str) -> str:
    return f"Hello, {name}!"

result: int = greet("Rahul")    # mypy catches this!
# error: Incompatible types in assignment
# (expression has type "str", variable has type "int")
```

### mypy Configuration

Create `mypy.ini` or add to `pyproject.toml`:

```ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

---

## dataclasses — Structured Data

`dataclasses` automatically generate `__init__`, `__repr__`, `__eq__`, and more.

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    city: str
    course: str
    fee: float
    marks: list[int] = field(default_factory=list)
    enrolled: bool = True

# Auto-generated __init__ — no need to write it!
s1 = Student("Rahul", "Bhopal", "Python Full Stack", 25000)
s2 = Student("Priya", "Pune", "Web Dev", 20000, [85, 92])

print(s1)
# Student(name='Rahul', city='Bhopal', course='Python Full Stack',
#         fee=25000, marks=[], enrolled=True)

# Auto-generated __eq__
s3 = Student("Rahul", "Bhopal", "Python Full Stack", 25000)
print(s1 == s3)    # True
```

### Frozen Dataclasses (Immutable)

```python
@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float
    city: str

bhopal = Coordinates(23.26, 77.41, "Bhopal")
# bhopal.lat = 0  # FrozenInstanceError!
```

### Post-init Processing

```python
@dataclass
class Student:
    name: str
    marks: list[int]
    average: float = field(init=False)    # Not in __init__

    def __post_init__(self):
        """Runs after __init__ — calculate derived fields."""
        self.average = sum(self.marks) / len(self.marks) if self.marks else 0

s = Student("Rahul", [85, 92, 78])
print(s.average)    # 85.0
```

---

## NamedTuple — Typed Tuples

```python
from typing import NamedTuple

class Student(NamedTuple):
    name: str
    city: str
    marks: int

s = Student("Rahul", "Bhopal", 85)
print(s.name)      # Rahul
print(s[0])        # Rahul (still works as tuple)
print(s)           # Student(name='Rahul', city='Bhopal', marks=85)

# Immutable — cannot modify
# s.name = "Priya"    # AttributeError!

# Can be used as dict key (tuples are hashable)
scores = {s: "Pass"}
```

---

## Pydantic — Data Validation

Pydantic is the most popular library for data validation in Python. Unlike dataclasses (which just structure data), Pydantic **validates and converts** data.

```bash
pip install pydantic
```

### Basic Model

```python
from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    name: str
    city: str
    age: int
    fee: float
    email: Optional[str] = None

# Valid data
s1 = Student(name="Rahul", city="Bhopal", age=22, fee=25000)
print(s1)
# name='Rahul' city='Bhopal' age=22 fee=25000.0 email=None

# Automatic type conversion
s2 = Student(name="Priya", city="Pune", age="21", fee="20000")
print(s2.age)     # 21 (converted from str to int!)
print(s2.fee)     # 20000.0 (converted from str to float!)

# Invalid data — raises ValidationError
try:
    Student(name="Amit", city="Delhi", age="not-a-number", fee=15000)
except Exception as e:
    print(e)
    # validation error for Student
    # age: Input should be a valid integer
```

### Field Validation

```python
from pydantic import BaseModel, Field, field_validator

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=16, le=60, description="Student age (16-60)")
    fee: float = Field(gt=0, description="Course fee in INR")
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")

    @field_validator("name")
    @classmethod
    def name_must_be_title_case(cls, v):
        if not v[0].isupper():
            raise ValueError("Name must start with uppercase")
        return v

# Valid
s = Student(name="Rahul", age=22, fee=25000, email="rahul@techpath.com")

# Invalid — clear error messages
try:
    Student(name="r", age=15, fee=-100, email="bad")
except Exception as e:
    print(e)
    # Multiple validation errors with clear messages
```

### Model Methods

```python
class Student(BaseModel):
    name: str
    city: str
    fee: float

s = Student(name="Rahul", city="Bhopal", fee=25000)

# To dictionary
d = s.model_dump()
print(d)    # {'name': 'Rahul', 'city': 'Bhopal', 'fee': 25000.0}

# To JSON string
j = s.model_dump_json()
print(j)    # '{"name":"Rahul","city":"Bhopal","fee":25000.0}'

# From dictionary
s2 = Student.model_validate({"name": "Priya", "city": "Pune", "fee": 20000})

# From JSON
s3 = Student.model_validate_json('{"name":"Amit","city":"Delhi","fee":15000}')

# Partial update (only update provided fields)
data = {"fee": 22000}
s4 = s.model_copy(update=data)
print(s4.fee)    # 22000.0 (updated)
print(s4.name)   # Rahul (unchanged)
```

### Nested Models

```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    pincode: str

class Student(BaseModel):
    name: str
    age: int
    address: Address
    courses: list[str]

# Nested validation works automatically
s = Student(
    name="Rahul",
    age=22,
    address={"street": "MP Nagar", "city": "Bhopal", "pincode": "462011"},
    courses=["Python Full Stack", "Data Science"],
)

print(s.address.city)       # Bhopal
print(s.address.pincode)    # 462011
```

### ConfigDict — Model Settings

```python
from pydantic import BaseModel, ConfigDict

class Student(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,    # Allow creating from ORM objects
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,   # Validate on attribute change
    )

    name: str
    city: str
    fee: float

s = Student(name="  Rahul  ", city="  Bhopal  ", fee=25000)
print(s.name)    # "Rahul" (whitespace stripped!)
```

---

## Comparison: dataclass vs Pydantic vs NamedTuple

| Feature | dataclass | Pydantic | NamedTuple |
|---------|-----------|----------|------------|
| Validation | No | Yes | No |
| Type conversion | No | Yes | No |
| Mutable | Yes (default) | Yes (default) | No |
| JSON support | Manual | Built-in | Manual |
| Performance | Fastest | Slower (validates) | Fastest |
| Use case | Internal data | API data, forms | Immutable records |

---

## Summary

| Concept | What It Does | Use When |
|---------|-------------|----------|
| Type hints | Document expected types | Always (good practice) |
| mypy | Check types statically | CI/CD, large projects |
| dataclass | Auto-generate __init__, __repr__ | Internal data structures |
| NamedTuple | Immutable typed tuples | Fixed records, dict keys |
| Pydantic | Validate and convert data | API input, config, forms |
| Field | Add constraints | Min/max, patterns, descriptions |

---

## Practice Tasks

1. Add type hints to 5 existing functions in your code
2. Create a `Student` dataclass with auto-calculated `grade` in `__post_init__`
3. Create a Pydantic model for a course enrollment form with validation
4. Run mypy on a file and fix any type errors
5. Build a nested Pydantic model (Student with Address and list of Courses)
