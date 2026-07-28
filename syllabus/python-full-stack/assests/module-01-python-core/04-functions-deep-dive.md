# Functions Deep Dive

**Module 01 — Python Core: Language Fundamentals | Topic 4**

---

## What is a Function?

A function is a reusable block of code that performs a specific task. Instead of writing the same code again and again, you write it once inside a function and call it whenever needed.

**Real-world analogy:** A function is like a recipe. You write the recipe once. Every time you want to make that dish, you follow the same recipe — you don't reinvent it.

```python
# Without function — repeating code
print("=" * 40)
print("TechPath Institute")
print("=" * 40)

# ... later in code ...
print("=" * 40)
print("TechPath Institute")
print("=" * 40)

# With function — write once, use many times
def print_header():
    print("=" * 40)
    print("TechPath Institute")
    print("=" * 40)

print_header()    # Call it whenever needed
print_header()
```

---

## Defining and Calling Functions

### Basic Syntax

```python
def function_name(parameters):
    """Docstring — describes what the function does."""
    # Function body
    return result
```

### Example

```python
def greet(name):
    """Greet a student by name."""
    return f"Hello, {name}! Welcome to TechPath."

# Calling the function
message = greet("Rahul")
print(message)    # Hello, Rahul! Welcome to TechPath.
```

### Functions with Multiple Parameters

```python
def calculate_fee(base_price, gst_rate=0.18):
    """Calculate total fee including GST."""
    gst = base_price * gst_rate
    total = base_price + gst
    return total

# Call with both arguments
print(calculate_fee(25000, 0.18))    # 29500.0

# Call with default GST rate
print(calculate_fee(25000))          # 29500.0 (uses default 0.18)
```

---

## Return Values

### Returning a Single Value

```python
def square(n):
    return n ** 2

result = square(5)
print(result)    # 25
```

### Returning Multiple Values

Python functions can return multiple values as a tuple:

```python
def get_student_info(name):
    """Return student details."""
    city = "Bhopal"
    marks = 85
    return name, city, marks    # Returns a tuple

# Unpack the returned values
name, city, marks = get_student_info("Priya")
print(f"{name} from {city} scored {marks}")
```

### Functions Without return

If a function has no `return` statement, it returns `None`:

```python
def say_hello(name):
    print(f"Hello, {name}!")    # No return

result = say_hello("Amit")
print(result)    # None
```

### Early Return

Use `return` to exit a function early:

```python
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero!"    # Exit early
    return a / b

print(divide(10, 3))     # 3.333...
print(divide(10, 0))     # Cannot divide by zero!
```

---

## Default Arguments

Default arguments have a preset value. If the caller does not provide that argument, the default is used.

```python
def enroll_student(name, course="Python Full Stack", city="Bhopal"):
    print(f"Enrolled {name} in {course} at {city}")

enroll_student("Rahul")
# Enrolled Rahul in Python Full Stack at Bhopal

enroll_student("Priya", "Web Development")
# Enrolled Priya in Web Development at Bhopal

enroll_student("Amit", city="Delhi")
# Enrolled Amit in Python Full Stack at Delhi
```

**Rule:** Default arguments must come after non-default arguments:

```python
# Correct
def func(a, b, c=10):
    pass

# Wrong — SyntaxError
def func(a, b=10, c):
    pass
```

### Mutable Default Argument Trap

Never use a mutable object (list, dict) as a default argument:

```python
# WRONG — the list is shared across all calls!
def add_student(name, students=[]):
    students.append(name)
    return students

print(add_student("Rahul"))     # ['Rahul']
print(add_student("Priya"))     # ['Rahul', 'Priya']  ← Unexpected!

# CORRECT — use None as default
def add_student(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students

print(add_student("Rahul"))     # ['Rahul']
print(add_student("Priya"))     # ['Priya']  ← Correct!
```

---

## *args — Variable Positional Arguments

`*args` lets a function accept any number of positional arguments. They are collected into a tuple.

```python
def total_marks(*marks):
    """Calculate total of any number of marks."""
    return sum(marks)

print(total_marks(85, 92, 78))         # 255
print(total_marks(90, 88, 95, 82))     # 355
print(total_marks(100))                 # 100
```

### Real-World Example

```python
def print_receipt(shop_name, *items):
    """Print a receipt with any number of items."""
    print(f"\n{'=' * 35}")
    print(f"  {shop_name}")
    print(f"{'=' * 35}")
    
    total = 0
    for name, price in items:
        print(f"  {name:<20} ₹{price:>8.2f}")
        total += price
    
    print(f"{'—' * 35}")
    print(f"  {'Total':<20} ₹{total:>8.2f}")
    print(f"{'=' * 35}")

print_receipt(
    "TechPath Bookstore",
    ("Python Crash Course", 599),
    ("Clean Code", 499),
    ("Flask Web Dev", 399),
)
```

---

## **kwargs — Variable Keyword Arguments

`**kwargs` lets a function accept any number of keyword arguments. They are collected into a dictionary.

```python
def create_profile(**details):
    """Create a student profile from keyword arguments."""
    print("Student Profile:")
    for key, value in details.items():
        print(f"  {key}: {value}")

create_profile(name="Sneha", city="Pune", course="Python Full Stack", batch=2026)
# Student Profile:
#   name: Sneha
#   city: Pune
#   course: Python Full Stack
#   batch: 2026
```

### Combining *args and **kwargs

```python
def log_event(event_type, *tags, **metadata):
    print(f"Event: {event_type}")
    print(f"Tags: {tags}")
    print(f"Metadata: {metadata}")

log_event("enrollment", "new", "python", student="Rahul", fee=25000)
# Event: enrollment
# Tags: ('new', 'python')
# Metadata: {'student': 'Rahul', 'fee': 25000}
```

**Parameter order rule:** `def func(normal, *args, **kwargs)`

---

## Lambda Functions

A lambda is a small, anonymous (unnamed) function defined in one line.

```python
# Regular function
def square(x):
    return x ** 2

# Lambda equivalent
square = lambda x: x ** 2

print(square(5))    # 25
```

### When to Use Lambda

Lambdas are useful when you need a quick function for sorting, filtering, or mapping:

```python
students = [
    {"name": "Rahul", "marks": 78},
    {"name": "Priya", "marks": 92},
    {"name": "Amit", "marks": 85},
]

# Sort by marks (descending)
students.sort(key=lambda s: s["marks"], reverse=True)
print(students[0]["name"])    # Priya (highest marks)

# Filter: only passing students
passing = list(filter(lambda s: s["marks"] >= 60, students))

# Transform: get just the names
names = list(map(lambda s: s["name"], students))
```

### Lambda vs Regular Function

| Feature | Lambda | Regular Function |
|---------|--------|-----------------|
| Lines | One line only | Multiple lines |
| Name | Anonymous (optional) | Named |
| `return` | Implicit | Explicit |
| Readability | Low for complex logic | High |
| Use case | Quick throwaway | Reusable logic |

---

## Scope — Where Variables Live (LEGB Rule)

Python looks for variables in this order: **L → E → G → B**

| Level | Name | Example |
|-------|------|---------|
| **L** | Local | Variables inside the current function |
| **E** | Enclosing | Variables in the outer function (for nested functions) |
| **G** | Global | Variables at the module (file) level |
| **B** | Built-in | Python's built-in names (`print`, `len`, `int`) |

### Local Scope

```python
def greet():
    message = "Hello"    # Local variable
    print(message)

greet()
# print(message)    # NameError! 'message' is not accessible here
```

### Global Scope

```python
institute = "TechPath"    # Global variable

def show():
    print(institute)    # Can READ global variables

show()    # TechPath
```

### Modifying Global Variables

```python
count = 0

def increment():
    global count    # Declare that we want to modify the global
    count += 1

increment()
increment()
print(count)    # 2
```

**Best practice:** Avoid using `global`. Instead, pass values as arguments and return results.

### Enclosing Scope (Closures)

```python
def outer():
    greeting = "Hello"    # Enclosing variable
    
    def inner(name):
        print(f"{greeting}, {name}!")    # Accesses enclosing variable
    
    return inner

greet = outer()
greet("Rahul")    # Hello, Rahul!
```

---

## Docstrings — Documenting Functions

Always add a docstring to explain what your function does:

```python
def calculate_gst(amount, rate=0.18):
    """
    Calculate GST for a given amount.
    
    Args:
        amount: Base amount in INR
        rate: GST rate (default 18%)
    
    Returns:
        Tuple of (gst_amount, total_amount)
    
    Example:
        >>> calculate_gst(1000)
        (180.0, 1180.0)
    """
    gst = amount * rate
    total = amount + gst
    return gst, total

# Access the docstring
print(calculate_gst.__doc__)
help(calculate_gst)
```

---

## Higher-Order Functions

A higher-order function takes another function as an argument or returns a function.

### map() — Apply a Function to Every Item

```python
prices = [100, 200, 300, 400]

# Add 18% GST to all prices
with_gst = list(map(lambda p: p * 1.18, prices))
print(with_gst)    # [118.0, 236.0, 354.0, 472.0]
```

### filter() — Keep Items That Match

```python
marks = [85, 42, 91, 58, 73, 36, 88]

# Keep only passing marks
passing = list(filter(lambda m: m >= 60, marks))
print(passing)    # [85, 91, 73, 88]
```

### sorted() with key

```python
students = ["sneha", "Rahul", "priya", "Amit"]

# Case-insensitive sort
sorted_students = sorted(students, key=str.lower)
print(sorted_students)    # ['Amit', 'priya', 'Rahul', 'sneha']
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Function | `def name(params):` | Reusable block of code |
| Return | `return value` | Send result back |
| Default args | `def f(x=10):` | Preset parameter values |
| `*args` | `def f(*args):` | Accept any number of positional args |
| `**kwargs` | `def f(**kwargs):` | Accept any number of keyword args |
| Lambda | `lambda x: x ** 2` | Quick one-line function |
| Scope (LEGB) | Local > Enclosing > Global > Built-in | Variable lookup order |
| Docstring | `"""Description"""` | Document your function |

---

## Practice Tasks

1. Write a function `calculate_bmi(weight, height)` that returns the BMI and category
2. Write a function using `*args` that returns the average of any number of marks
3. Write a function using `**kwargs` that prints a student's profile card
4. Sort a list of dictionaries by a specific key using a lambda
5. Write a function that returns another function (closure) for creating greetings
