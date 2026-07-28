# Variables & Data Types

**Module 01 — Python Core: Language Fundamentals | Topic 2**

---

## What is a Variable?

A variable is a name that stores a value. Think of it as a **labelled box** — the label is the variable name and the content inside is the value.

```python
student_name = "Priya"
age = 21
fee = 15999.50
is_enrolled = True
```

Python is **dynamically typed** — you do not need to declare the type. Python figures it out automatically.

```python
x = 10        # Python knows this is an int
x = "hello"   # Now x is a str — Python allows this
```

### Variable Naming Rules

| Rule | Valid | Invalid |
|------|-------|---------|
| Must start with a letter or underscore | `name`, `_count` | `1name`, `@data` |
| Can contain letters, digits, underscores | `student_1`, `total_fee` | `student-1`, `total fee` |
| Case-sensitive | `Name` and `name` are different | — |
| Cannot use Python keywords | `my_class` | `class`, `for`, `if` |

### Python Naming Conventions

| Style | Used For | Example |
|-------|----------|---------|
| `snake_case` | Variables, functions | `student_name`, `calculate_fee()` |
| `PascalCase` | Classes | `Student`, `CourseEnrollment` |
| `UPPER_CASE` | Constants | `MAX_STUDENTS`, `GST_RATE` |

---

## Core Data Types

Python has four fundamental data types:

### 1. int — Whole Numbers

```python
age = 22
batch_size = 30
negative = -5
big_number = 1_00_000    # Underscores for readability (₹1,00,000)

print(type(age))    # <class 'int'>
```

Python integers have **no size limit** — they can be as large as your memory allows:

```python
huge = 10 ** 100    # 1 followed by 100 zeros — no problem!
```

### 2. float — Decimal Numbers

```python
fee = 15999.50
gst_rate = 0.18
pi = 3.14159
temperature = -2.5

print(type(fee))    # <class 'float'>
```

**Warning — Float Precision:**

```python
>>> 0.1 + 0.2
0.30000000000000004    # Not exactly 0.3!
```

This happens because computers store decimals in binary. For financial calculations, use the `decimal` module:

```python
from decimal import Decimal
price = Decimal("0.1") + Decimal("0.2")
print(price)    # 0.3 (exact)
```

### 3. str — Text (Strings)

```python
name = "Rahul Sharma"
city = 'Bhopal'
greeting = "Hello, World!"
empty = ""

print(type(name))    # <class 'str'>
```

Strings can use single quotes `'...'` or double quotes `"..."` — both are the same.

**Multi-line strings** use triple quotes:

```python
address = """TechPath Institute
MP Nagar, Bhopal
Madhya Pradesh - 462011"""
```

### 4. bool — True or False

```python
is_student = True
has_paid = False

print(type(is_student))    # <class 'bool'>
```

Booleans are used in conditions:

```python
if has_paid:
    print("Access granted")
else:
    print("Please pay your fee")
```

---

## Type Checking and Casting

### Checking Types

```python
x = 42
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
print(isinstance(x, str))   # False
```

### Type Casting (Conversion)

| Function | Converts To | Example |
|----------|------------|---------|
| `int()` | Integer | `int("42")` → `42` |
| `float()` | Float | `float("3.14")` → `3.14` |
| `str()` | String | `str(42)` → `"42"` |
| `bool()` | Boolean | `bool(1)` → `True` |

```python
# String to number
age_str = "22"
age = int(age_str)
print(age + 1)    # 23

# Number to string
fee = 15999
message = "Fee is ₹" + str(fee)
print(message)    # Fee is ₹15999

# Float to int (truncates, does not round)
marks = 88.7
print(int(marks))    # 88 (not 89!)
```

### What Converts to True / False?

```python
# Falsy values (become False)
bool(0)        # False
bool(0.0)      # False
bool("")       # False (empty string)
bool([])       # False (empty list)
bool(None)     # False

# Truthy values (become True)
bool(1)        # True
bool(-5)       # True (any non-zero number)
bool("hello")  # True (any non-empty string)
bool([1, 2])   # True (any non-empty list)
```

---

## Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `10 + 3` | `13` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `10 * 3` | `30` |
| `/` | Division | `10 / 3` | `3.333...` |
| `//` | Floor Division | `10 // 3` | `3` |
| `%` | Modulus (Remainder) | `10 % 3` | `1` |
| `**` | Power | `2 ** 10` | `1024` |

### Real-World Examples

```python
# Calculate GST on a laptop
laptop_price = 55000
gst = laptop_price * 18 / 100
total = laptop_price + gst
print(f"Price: ₹{laptop_price}, GST: ₹{gst}, Total: ₹{total}")
# Price: ₹55000, GST: ₹9900.0, Total: ₹64900.0

# Split a bill equally among 4 friends
total_bill = 2400
per_person = total_bill / 4
print(f"Each person pays: ₹{per_person}")    # ₹600.0

# Check if a number is even or odd
number = 17
if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")    # 17 is odd
```

---

## Comparison & Logical Operators

### Comparison Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `10 > 5` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>=` | Greater or equal | `5 >= 5` | `True` |
| `<=` | Less or equal | `3 <= 5` | `True` |

### Logical Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `and` | Both must be True | `True and False` | `False` |
| `or` | At least one True | `True or False` | `True` |
| `not` | Opposite | `not True` | `False` |

```python
age = 22
has_id = True

# Can vote?
if age >= 18 and has_id:
    print("You can vote!")    # This prints

# Eligible for discount?
is_student = True
is_senior = False
if is_student or is_senior:
    print("Discount applied!")    # This prints
```

---

## f-Strings (Formatted String Literals)

f-strings are the modern way to put variables inside strings. Add an `f` before the string and use `{variable}` inside.

```python
name = "Ananya"
course = "Python Full Stack"
fee = 25000

# f-string
print(f"Student: {name}")
print(f"Course: {course}")
print(f"Fee: ₹{fee}")
```

### Formatting Numbers

```python
price = 1599.5
pi = 3.14159265

# Two decimal places
print(f"Price: ₹{price:.2f}")       # ₹1599.50

# Thousands separator
big = 1500000
print(f"Salary: ₹{big:,}")          # ₹1,500,000

# Indian style (manual)
print(f"Salary: ₹{big:,.0f}")       # ₹1,500,000

# Percentage
score = 0.875
print(f"Score: {score:.1%}")         # 87.5%

# Padding
for i in range(1, 6):
    print(f"Day {i:02d}")            # Day 01, Day 02, ...
```

### Expressions Inside f-strings

```python
a = 10
b = 3

print(f"{a} + {b} = {a + b}")       # 10 + 3 = 13
print(f"{a} > {b}? {a > b}")        # 10 > 3? True
print(f"{'PASS' if a > 5 else 'FAIL'}")  # PASS
```

---

## Special Values

### None

`None` represents "no value" or "nothing". It is not `0`, not `""`, not `False` — it is the absence of a value.

```python
result = None

if result is None:
    print("No result yet")

# Common use: optional function parameters
def greet(name=None):
    if name is None:
        print("Hello, stranger!")
    else:
        print(f"Hello, {name}!")

greet()           # Hello, stranger!
greet("Sneha")    # Hello, Sneha!
```

### Multiple Assignment

```python
# Assign multiple variables at once
x, y, z = 10, 20, 30

# Swap two variables
a, b = 5, 10
a, b = b, a
print(a, b)    # 10 5

# Same value to multiple variables
x = y = z = 0
```

---

## input() — Getting User Input

```python
name = input("Enter your name: ")
print(f"Hello, {name}!")

# input() ALWAYS returns a string
age = input("Enter your age: ")     # "22" (string!)
age = int(input("Enter your age: "))  # 22 (integer)

# Complete example
name = input("Student name: ")
marks = float(input("Enter marks: "))
print(f"{name} scored {marks} marks")
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Variables | Named storage — Python auto-detects type |
| `int` | Whole numbers, unlimited size |
| `float` | Decimal numbers, beware of precision |
| `str` | Text in quotes — single or double |
| `bool` | `True` or `False` |
| Type Casting | `int()`, `float()`, `str()`, `bool()` |
| f-strings | `f"text {variable}"` — best way to format strings |
| `None` | Represents "no value" |
| `input()` | Get user input (always returns string) |

---

## Practice Tasks

1. Create variables for a student: name, age, city, fee, is_enrolled
2. Calculate the total fee with 18% GST using variables
3. Use f-strings to print: "Rahul (age 22) from Bhopal enrolled for ₹25,000"
4. Take user input for two numbers and print their sum
5. Check if a number entered by the user is even or odd
