# Module 02: Advanced Python

## 1. OOP Deep Dive — Classes & Objects

### What is OOP?
Object-Oriented Programming (OOP) organizes code into **objects** — bundles of data (attributes) and behavior (methods). Think of a class as a blueprint (like a form template) and an object as a filled-in form.

### Defining a Class
```python
class Student:
    """Represents a TechPath Institute student."""

    # Class attribute (shared by ALL students)
    institute = "TechPath Institute"

    def __init__(self, name, city, course, fee):
        """Initialize a new student (constructor)."""
        # Instance attributes (unique to each student)
        self.name = name
        self.city = city
        self.course = course
        self.fee = fee
        self._marks = []  # Private by convention (underscore prefix)

    def add_marks(self, marks):
        """Add marks for a subject."""
        self._marks.append(marks)

    def average_marks(self):
        """Calculate average marks."""
        if not self._marks:
            return 0
        return sum(self._marks) / len(self._marks)

    def __str__(self):
        """Human-readable string representation."""
        return f"{self.name} ({self.city}) — {self.course}"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Student(name='{self.name}', city='{self.city}')"


# Creating objects
s1 = Student("Rahul Sharma", "Bhopal", "Python Full Stack", 25000)
s2 = Student("Priya Patel", "Pune", "Web Development", 20000)

s1.add_marks(85)
s1.add_marks(92)
print(s1)                    # Rahul Sharma (Bhopal) — Python Full Stack
print(f"Average: {s1.average_marks()}")  # Average: 88.5
print(s1.institute)          # TechPath Institute (class attribute)
```

### @property — Computed Attributes
Use `@property` when you want attribute-like access but with logic behind it:
```python
class Product:
    def __init__(self, name, base_price):
        self.name = name
        self._base_price = base_price

    @property
    def price(self):
        """Get price with GST."""
        return round(self._base_price * 1.18, 2)

    @price.setter
    def price(self, value):
        """Set base price (before GST)."""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._base_price = value

    @property
    def base_price(self):
        return self._base_price


chai = Product("Masala Chai", 10)
print(f"{chai.name}: ₹{chai.price}")   # Masala Chai: ₹11.8
chai.price = 15                          # Uses the setter
print(f"{chai.name}: ₹{chai.price}")   # Masala Chai: ₹17.7
```

### Dunder (Magic) Methods
Special methods that Python calls automatically:

| Method | When Called | Example |
|--------|-----------|---------|
| `__init__` | Creating an object | `Student("Rahul", ...)` |
| `__str__` | `print(obj)` or `str(obj)` | `print(student)` |
| `__repr__` | Developer display, `repr(obj)` | In REPL or debugging |
| `__len__` | `len(obj)` | `len(classroom)` |
| `__eq__` | `obj1 == obj2` | `s1 == s2` |
| `__lt__` | `obj1 < obj2` | `s1 < s2` (for sorting) |
| `__add__` | `obj1 + obj2` | `cart1 + cart2` |
| `__contains__` | `item in obj` | `"Rahul" in classroom` |
| `__getitem__` | `obj[key]` | `classroom[0]` |

```python
class Classroom:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add(self, student_name):
        self.students.append(student_name)

    def __len__(self):
        return len(self.students)

    def __contains__(self, name):
        return name in self.students

    def __getitem__(self, index):
        return self.students[index]

    def __iter__(self):
        return iter(self.students)


room = Classroom("Batch A")
room.add("Rahul")
room.add("Priya")
room.add("Amit")

print(len(room))            # 3
print("Rahul" in room)      # True
print(room[0])              # Rahul
for student in room:         # Iteration works!
    print(student)
```

---

## 2. Inheritance & MRO

### Single Inheritance
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Hi, I am {self.name}, age {self.age}"


class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)  # Call parent's __init__
        self.course = course

    def introduce(self):
        base = super().introduce()
        return f"{base}, studying {self.course}"


class Trainer(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def introduce(self):
        base = super().introduce()
        return f"{base}, teaching {self.subject}"


s = Student("Rahul", 22, "Python")
t = Trainer("Vikram Sir", 35, "Python")
print(s.introduce())  # Hi, I am Rahul, age 22, studying Python
print(t.introduce())  # Hi, I am Vikram Sir, age 35, teaching Python
```

### Multiple Inheritance & MRO
```python
class Printable:
    def print_info(self):
        print(f"[PRINT] {self}")

class Exportable:
    def export(self):
        return {"type": self.__class__.__name__, "data": str(self)}

class Report(Printable, Exportable):
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"{self.title}: {self.content}"


r = Report("Fee Report", "Total collected: ₹5,00,000")
r.print_info()              # [PRINT] Fee Report: Total collected: ₹5,00,000
print(r.export())            # {'type': 'Report', 'data': '...'}

# Check MRO (Method Resolution Order)
print(Report.__mro__)
# Report → Printable → Exportable → object
```

### Abstract Base Classes (ABC)
Force subclasses to implement specific methods:
```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount):
        """Subclasses MUST implement this."""
        pass

    @abstractmethod
    def refund(self, transaction_id):
        pass

    def generate_receipt(self, amount):
        """Concrete method — shared by all subclasses."""
        return f"Receipt for ₹{amount:,.2f}"


class UPIPayment(PaymentGateway):
    def process_payment(self, amount):
        return f"UPI payment of ₹{amount} processed"

    def refund(self, transaction_id):
        return f"UPI refund for {transaction_id} initiated"


# gateway = PaymentGateway()  # ERROR! Cannot instantiate abstract class
upi = UPIPayment()
print(upi.process_payment(5000))
print(upi.generate_receipt(5000))
```

---

## 3. Functional Python

### map, filter, reduce
```python
from functools import reduce

fees = [15000, 20000, 25000, 30000, 18000]

# map — apply a function to every item
with_gst = list(map(lambda f: round(f * 1.18), fees))
# [17700, 23600, 29500, 35400, 21240]

# filter — keep items that match a condition
above_20k = list(filter(lambda f: f > 20000, fees))
# [25000, 30000]

# reduce — combine all items into one value
total = reduce(lambda a, b: a + b, fees)
# 108000
```

### itertools — Useful Iteration Tools
```python
import itertools

# chain — combine multiple iterables
batch_a = ["Rahul", "Priya"]
batch_b = ["Amit", "Sneha"]
all_students = list(itertools.chain(batch_a, batch_b))
# ["Rahul", "Priya", "Amit", "Sneha"]

# product — all combinations (like nested loops)
sizes = ["S", "M", "L"]
colors = ["Red", "Blue"]
combos = list(itertools.product(sizes, colors))
# [('S', 'Red'), ('S', 'Blue'), ('M', 'Red'), ...]

# groupby — group consecutive items
data = [("Bhopal", "Rahul"), ("Bhopal", "Priya"), ("Delhi", "Amit"), ("Delhi", "Neha")]
for city, students in itertools.groupby(data, key=lambda x: x[0]):
    names = [s[1] for s in students]
    print(f"{city}: {names}")
```

### Closures
A closure is a function that remembers the variables from its enclosing scope:
```python
def fee_calculator(gst_rate):
    """Returns a function that adds GST at the given rate."""
    def calculate(base_price):
        return round(base_price * (1 + gst_rate / 100), 2)
    return calculate

add_gst_18 = fee_calculator(18)
add_gst_5 = fee_calculator(5)

print(add_gst_18(1000))  # 1180.0
print(add_gst_5(1000))   # 1050.0
```

---

## 4. Generators & Iterators

### What is a Generator?
A generator is a function that produces values one at a time using `yield`, instead of returning them all at once. This saves memory.

```python
# Regular function — stores ALL items in memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator — produces one item at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2

# Usage is the same
for sq in get_squares_gen(5):
    print(sq)  # 0, 1, 4, 9, 16

# But generators use almost no memory for large data
import sys
big_list = get_squares_list(10000)
big_gen = get_squares_gen(10000)
print(f"List size: {sys.getsizeof(big_list)} bytes")  # ~87,000 bytes
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")  # ~200 bytes
```

### Generator Expressions
Like list comprehensions, but with parentheses:
```python
# List comprehension — creates entire list in memory
squares_list = [x ** 2 for x in range(1000000)]

# Generator expression — lazy, memory efficient
squares_gen = (x ** 2 for x in range(1000000))

# Useful with sum, max, min, etc.
total = sum(x ** 2 for x in range(1000000))
```

### Practical Generator — Reading Large Files
```python
def read_large_csv(filename):
    """Read a large CSV file one row at a time."""
    with open(filename, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        for line in f:
            values = line.strip().split(",")
            yield dict(zip(header, values))

# Process millions of rows without running out of memory
for row in read_large_csv("students.csv"):
    if int(row["Marks"]) > 90:
        print(f"Topper: {row['Name']}")
```

---

## 5. Decorators

### What is a Decorator?
A decorator is a function that wraps another function to add extra behavior.

```python
import time

def timer(func):
    """Decorator that measures execution time."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    """Simulate a slow operation."""
    total = sum(i ** 2 for i in range(1_000_000))
    return total

result = slow_function()  # slow_function took 0.0823 seconds
```

### Writing Your Own Decorators
```python
def require_auth(func):
    """Decorator that checks if user is logged in."""
    def wrapper(user, *args, **kwargs):
        if not user.get("logged_in"):
            print(f"Access denied! Please log in first.")
            return None
        return func(user, *args, **kwargs)
    return wrapper

@require_auth
def view_dashboard(user):
    print(f"Welcome to dashboard, {user['name']}!")

view_dashboard({"name": "Rahul", "logged_in": True})   # Works
view_dashboard({"name": "Priya", "logged_in": False})   # Access denied!
```

### @staticmethod and @classmethod
```python
class Student:
    count = 0

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        Student.count += 1

    @staticmethod
    def is_passing(marks):
        """Does not need self or cls — just a utility."""
        return marks >= 40

    @classmethod
    def from_string(cls, data_string):
        """Alternative constructor from a string like 'Rahul,85'."""
        name, marks = data_string.split(",")
        return cls(name.strip(), int(marks.strip()))

    @classmethod
    def total_enrolled(cls):
        return cls.count


s1 = Student("Rahul", 85)
s2 = Student.from_string("Priya, 92")    # classmethod as factory
print(Student.is_passing(35))              # False (staticmethod)
print(Student.total_enrolled())            # 2 (classmethod)
```

### Stacking Decorators
```python
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}"

print(greet("Rahul"))  # <b><i>Hello, Rahul</i></b>
# Decorators apply bottom-up: italic first, then bold wraps it
```

---

## 6. Async Python

### Why Async?
When your program waits for something (API call, file read, database query), async lets other code run during that wait instead of blocking.

```python
import asyncio

async def fetch_student(name, delay):
    """Simulate fetching student data from an API."""
    print(f"Fetching {name}...")
    await asyncio.sleep(delay)  # Simulates network delay
    print(f"Got {name}!")
    return {"name": name, "status": "active"}

async def main():
    # Sequential — takes 1 + 2 + 1.5 = 4.5 seconds
    # await fetch_student("Rahul", 1)
    # await fetch_student("Priya", 2)
    # await fetch_student("Amit", 1.5)

    # Concurrent — takes only 2 seconds (longest task)
    results = await asyncio.gather(
        fetch_student("Rahul", 1),
        fetch_student("Priya", 2),
        fetch_student("Amit", 1.5),
    )
    print(f"\nAll done! Got {len(results)} results")

asyncio.run(main())
```

### async/await Rules
- `async def` makes a function a **coroutine**
- `await` pauses the coroutine until the awaited thing completes
- You can only use `await` inside an `async def`
- `asyncio.run()` starts the event loop from synchronous code
- `asyncio.gather()` runs multiple coroutines concurrently

---

## 7. Type Hints & Data Validation

### Basic Type Hints
```python
def calculate_fee(base: float, discount: float = 0) -> float:
    """Type hints tell you (and your editor) what types to expect."""
    return base * (1 - discount / 100)

name: str = "Rahul"
age: int = 22
courses: list[str] = ["Python", "Web Dev"]
student: dict[str, str] = {"name": "Rahul", "city": "Bhopal"}
```

### dataclasses
A shortcut for classes that mainly hold data:
```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    city: str
    course: str
    fee: float
    marks: list[int] = field(default_factory=list)

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks) if self.marks else 0

s = Student("Rahul", "Bhopal", "Python", 25000, [85, 92, 78])
print(s)            # Student(name='Rahul', city='Bhopal', ...)
print(s.average)    # 85.0
# __init__, __repr__, __eq__ are auto-generated!
```

### Pydantic for Validation
```python
from pydantic import BaseModel, Field, field_validator

class StudentForm(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=16, le=60)
    email: str
    fee: float = Field(gt=0)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()

# Valid data
s = StudentForm(name="Rahul", age=22, email="Rahul@Email.com", fee=25000)
print(s.email)  # rahul@email.com (auto-lowercased)

# Invalid data — raises ValidationError
try:
    bad = StudentForm(name="R", age=10, email="invalid", fee=-100)
except Exception as e:
    print(e)  # Shows all validation errors
```

---

## 8. Testing with pytest

### Writing Tests
```python
# file: calculator.py
def add(a, b):
    return a + b

def calculate_fee(base, discount=0, gst=18):
    discounted = base * (1 - discount / 100)
    return round(discounted * (1 + gst / 100), 2)

# file: test_calculator.py
from calculator import add, calculate_fee

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_calculate_fee_no_discount():
    assert calculate_fee(1000) == 1180.0

def test_calculate_fee_with_discount():
    assert calculate_fee(1000, discount=10) == 1062.0

def test_calculate_fee_zero_base():
    assert calculate_fee(0) == 0
```

### Running Tests
```bash
pip install pytest
pytest                       # Run all tests
pytest -v                    # Verbose output
pytest test_calculator.py    # Specific file
pytest -k "test_add"         # Run tests matching name
```

### Fixtures
```python
import pytest

@pytest.fixture
def sample_students():
    """Provide test data for multiple tests."""
    return [
        {"name": "Rahul", "marks": 85},
        {"name": "Priya", "marks": 92},
        {"name": "Amit", "marks": 78},
    ]

def test_topper(sample_students):
    topper = max(sample_students, key=lambda s: s["marks"])
    assert topper["name"] == "Priya"

def test_average(sample_students):
    avg = sum(s["marks"] for s in sample_students) / len(sample_students)
    assert avg == 85.0
```

### Parametrize — Test Multiple Inputs
```python
@pytest.mark.parametrize("marks,expected", [
    (95, "A+"),
    (80, "A"),
    (65, "B"),
    (45, "C"),
    (30, "Fail"),
])
def test_grade(marks, expected):
    grade = get_grade(marks)
    assert grade == expected
```

### Mocking
```python
from unittest.mock import patch, MagicMock

def fetch_student_from_api(student_id):
    """In real code, this would call an API."""
    import requests
    response = requests.get(f"https://api.techpath.biz/students/{student_id}")
    return response.json()

@patch("requests.get")
def test_fetch_student(mock_get):
    mock_get.return_value = MagicMock(
        json=lambda: {"name": "Rahul", "city": "Bhopal"}
    )
    result = fetch_student_from_api(1)
    assert result["name"] == "Rahul"
    mock_get.assert_called_once()
```
