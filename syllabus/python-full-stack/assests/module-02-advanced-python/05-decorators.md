# Decorators

**Module 02 — Advanced Python | Topic 5**

---

## What is a Decorator?

A decorator is a function that takes another function, adds extra behavior to it, and returns the enhanced version — without modifying the original function.

**Real-world analogy:** Think of a phone case. Your phone works perfectly without it, but a case adds protection (extra behavior) without changing the phone itself. A decorator "wraps" a function with extra functionality.

```python
# Without decorator — manually wrapping
def greet(name):
    return f"Hello, {name}!"

def make_fancy(func):
    def wrapper(*args, **kwargs):
        print("=" * 30)
        result = func(*args, **kwargs)
        print("=" * 30)
        return result
    return wrapper

greet = make_fancy(greet)    # Manually wrap
greet("Rahul")

# With decorator — same thing, cleaner syntax
@make_fancy
def greet(name):
    return f"Hello, {name}!"

greet("Rahul")
```

The `@decorator` syntax is just shorthand for `function = decorator(function)`.

---

## Writing Your First Decorator

### Step-by-Step

```python
import time

def timer(func):
    """Measure how long a function takes to run."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)    # Call the original function
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def process_students(n):
    """Simulate processing n student records."""
    total = sum(range(n))
    return total

result = process_students(1_000_000)
# process_students took 0.0312 seconds
```

### The Pattern

Every decorator follows the same structure:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 1. Do something BEFORE the function
        result = func(*args, **kwargs)
        # 2. Do something AFTER the function
        return result
    return wrapper
```

---

## Practical Decorators

### Logging Decorator

```python
def log_call(func):
    """Log every function call with arguments."""
    def wrapper(*args, **kwargs):
        args_str = ", ".join(
            [repr(a) for a in args] +
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"Calling {func.__name__}({args_str})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_call
def calculate_fee(base, gst_rate=0.18):
    return round(base * (1 + gst_rate), 2)

calculate_fee(25000)
# Calling calculate_fee(25000)
# calculate_fee returned 29500.0
```

### Retry Decorator

```python
import time

def retry(max_attempts=3, delay=1):
    """Retry a function if it raises an exception."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def connect_to_database():
    """Simulate a flaky database connection."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Database not responding")
    return "Connected!"
```

### Validation Decorator

```python
def validate_positive(func):
    """Ensure all numeric arguments are positive."""
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Negative value not allowed: {arg}")
        for key, val in kwargs.items():
            if isinstance(val, (int, float)) and val < 0:
                raise ValueError(f"Negative value for '{key}': {val}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def create_invoice(item, price, quantity=1):
    return f"{item}: ₹{price * quantity:,}"

print(create_invoice("Laptop", 55000, quantity=2))
# Laptop: ₹1,10,000

# create_invoice("Laptop", -5000)
# ValueError: Negative value not allowed: -5000
```

---

## Decorators with Arguments

To pass arguments to a decorator, you need **three levels of nesting**:

```python
def repeat(times):
    """Run a function multiple times."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"

print(greet("Priya"))
# ['Hello, Priya!', 'Hello, Priya!', 'Hello, Priya!']
```

### Role-Based Access Decorator

```python
def require_role(role):
    """Only allow users with the specified role."""
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(
                    f"Access denied. Required role: {role}, "
                    f"your role: {user.get('role')}"
                )
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_role("admin")
def delete_student(user, student_id):
    return f"Student {student_id} deleted by {user['name']}"

admin = {"name": "Sneha", "role": "admin"}
student = {"name": "Rahul", "role": "student"}

print(delete_student(admin, "TP-001"))
# Student TP-001 deleted by Sneha

# delete_student(student, "TP-001")
# PermissionError: Access denied. Required role: admin, your role: student
```

---

## functools.wraps — Preserving Function Identity

Without `@wraps`, the decorated function loses its name and docstring:

```python
from functools import wraps

def timer(func):
    @wraps(func)    # Preserve the original function's identity
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def process_data():
    """Process student data."""
    pass

# Without @wraps:
# print(process_data.__name__)  → "wrapper"
# print(process_data.__doc__)   → None

# With @wraps:
print(process_data.__name__)    # process_data
print(process_data.__doc__)     # Process student data.
```

**Always use `@wraps(func)`** in your decorators.

---

## @staticmethod and @classmethod

### @staticmethod — No Access to Instance or Class

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def factorial(n):
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n - 1)

# Call without creating an object
print(MathUtils.is_even(42))      # True
print(MathUtils.factorial(5))     # 120
```

### @classmethod — Access to Class (not Instance)

```python
class Student:
    total_students = 0

    def __init__(self, name, city):
        self.name = name
        self.city = city
        Student.total_students += 1

    @classmethod
    def from_string(cls, data_string):
        """Create a Student from a comma-separated string."""
        name, city = data_string.split(",")
        return cls(name.strip(), city.strip())

    @classmethod
    def get_count(cls):
        return f"Total students: {cls.total_students}"

# Regular creation
s1 = Student("Rahul", "Bhopal")

# Using class method
s2 = Student.from_string("Priya, Pune")

print(s2.name)                # Priya
print(Student.get_count())    # Total students: 2
```

### Comparison

| Decorator | `self`? | `cls`? | Use Case |
|-----------|---------|--------|----------|
| (none) | Yes | No | Regular method — needs instance data |
| `@staticmethod` | No | No | Utility function — no instance/class needed |
| `@classmethod` | No | Yes | Factory methods, class-level operations |

---

## Stacking Decorators

You can apply multiple decorators to one function. They execute **bottom-up** (closest to function first):

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold        # Applied second (outer)
@italic      # Applied first (inner)
def greet(name):
    return f"Hello, {name}"

print(greet("Rahul"))    # <b><i>Hello, Rahul</i></b>
```

---

## Class-Based Decorators

You can also create decorators using classes with `__call__`:

```python
class CountCalls:
    """Count how many times a function is called."""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}!"

greet("Rahul")    # greet called 1 times
greet("Priya")    # greet called 2 times
print(greet.count)   # 2
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Basic decorator | `@decorator` | Add behavior to functions |
| With arguments | `@decorator(arg)` | Configurable decorators |
| `@wraps(func)` | In wrapper function | Preserve function identity |
| `@staticmethod` | On class method | Utility method (no self/cls) |
| `@classmethod` | On class method | Factory/class-level method |
| Stacking | `@a` then `@b` | Multiple decorators |
| Class decorator | `class Dec: __call__` | Stateful decorators |

---

## Practice Tasks

1. Write a `@timer` decorator that logs how long a function takes
2. Write a `@retry(max_attempts=3)` decorator with configurable retries
3. Write a `@require_role("admin")` decorator for access control
4. Create a `Student` class with a `@classmethod` factory `from_dict()`
5. Stack `@log_call` and `@timer` decorators on a function and observe the order
