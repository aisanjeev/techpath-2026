# Python — Getting Started

**Module 10 — Python Programming | Topic 1**

---

## What is Python?

**Python** is one of the most popular programming languages in the world. It's known for being simple to read and write — almost like English.

| Feature | Detail |
|---------|--------|
| **Created by** | Guido van Rossum (1991) |
| **Used for** | Web development, AI/ML, data science, automation, scripting |
| **Used by** | Google, Netflix, Instagram, NASA, Spotify |
| **Why popular** | Easy to learn, huge library ecosystem, versatile |

> **Python reads like English:**
> ```python
> if age >= 18:
>     print("You can vote")
> ```

---

## Installing Python

1. Go to **python.org** → Download latest version
2. During install, **check "Add Python to PATH"** (very important!)
3. Open Terminal/Command Prompt → type `python --version`
4. If it shows version number, Python is installed

### Writing Python Code

| Method | How |
|--------|-----|
| **Terminal** | Type `python` → write code line by line |
| **VS Code** | Install Python extension → create `.py` file |
| **Online** | replit.com, Google Colab (no install needed) |

---

## Your First Python Program

```python
print("Hello, World!")
```

Save as `hello.py`, run with: `python hello.py`

---

## Variables

```python
# Variables - no need to declare type
name = "Rahul"          # String (text)
age = 20                # Integer (whole number)
height = 5.8            # Float (decimal number)
is_student = True       # Boolean (True/False)

print(name)             # Rahul
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
```

### Naming Rules

| Rule | Good | Bad |
|------|------|-----|
| Use lowercase + underscores | `student_name` | `StudentName` |
| Start with letter or _ | `_count`, `name` | `2name`, `my-var` |
| No spaces | `first_name` | `first name` |
| Descriptive names | `total_marks` | `x`, `t` |

---

## Data Types

| Type | Example | Check Type |
|------|---------|-----------|
| `str` | `"Hello"`, `'World'` | `type("Hello")` |
| `int` | `42`, `-5`, `0` | `type(42)` |
| `float` | `3.14`, `-0.5` | `type(3.14)` |
| `bool` | `True`, `False` | `type(True)` |
| `list` | `[1, 2, 3]` | `type([1,2])` |
| `tuple` | `(1, 2, 3)` | `type((1,2))` |
| `dict` | `{"name": "R"}` | `type({})` |
| `set` | `{1, 2, 3}` | `type({1,2})` |
| `None` | `None` | `type(None)` |

### Type Conversion

```python
# String to number
age = int("20")         # 20
price = float("9.99")   # 9.99

# Number to string
text = str(42)           # "42"

# User input is always string
name = input("Enter name: ")
age = int(input("Enter age: "))
```

---

## Strings

```python
name = "TechPath"

# String operations
print(len(name))           # 8 (length)
print(name.upper())        # TECHPATH
print(name.lower())        # techpath
print(name[0])             # T (first character)
print(name[-1])            # h (last character)
print(name[0:4])           # Tech (slice)
print(name.replace("Path", "World"))  # TechWorld

# f-strings (formatted strings)
age = 20
print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")

# Multi-line string
message = """
Hello,
This is a multi-line
string in Python.
"""
```

### Useful String Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `.upper()` | ALL CAPS | `"hello".upper()` → `"HELLO"` |
| `.lower()` | all lowercase | `"HELLO".lower()` → `"hello"` |
| `.strip()` | Remove spaces from ends | `" hi ".strip()` → `"hi"` |
| `.split()` | Split into list | `"a,b,c".split(",")` → `["a","b","c"]` |
| `.join()` | Join list into string | `",".join(["a","b"])` → `"a,b"` |
| `.replace()` | Replace text | `"hello".replace("l","L")` → `"heLLo"` |
| `.startswith()` | Check start | `"hello".startswith("he")` → `True` |
| `.count()` | Count occurrences | `"hello".count("l")` → `2` |
| `.find()` | Find position | `"hello".find("l")` → `2` |

---

## Operators

### Math

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Add | `5 + 3` | `8` |
| `-` | Subtract | `10 - 4` | `6` |
| `*` | Multiply | `3 * 4` | `12` |
| `/` | Divide (float) | `10 / 3` | `3.333` |
| `//` | Divide (integer) | `10 // 3` | `3` |
| `%` | Remainder | `10 % 3` | `1` |
| `**` | Power | `2 ** 3` | `8` |

### Comparison

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `>`, `<` | Greater, Less |
| `>=`, `<=` | Greater/equal, Less/equal |

### Logical

| Operator | Meaning | Example |
|----------|---------|---------|
| `and` | Both true | `True and False` → `False` |
| `or` | At least one true | `True or False` → `True` |
| `not` | Opposite | `not True` → `False` |

---

## Conditionals

```python
marks = 75

if marks >= 90:
    print("Grade: A")
elif marks >= 75:
    print("Grade: B")
elif marks >= 60:
    print("Grade: C")
else:
    print("Grade: F")

# One-line if (ternary)
status = "Pass" if marks >= 40 else "Fail"
```

---

## Loops

### for loop

```python
# Loop through range
for i in range(1, 6):
    print(i)    # 1, 2, 3, 4, 5

# Loop through list
fruits = ["Apple", "Banana", "Mango"]
for fruit in fruits:
    print(fruit)

# Loop with index
for i, fruit in enumerate(fruits):
    print(f"{i+1}. {fruit}")
```

### while loop

```python
count = 1
while count <= 5:
    print(count)
    count += 1
```

### Loop Control

```python
# break - exit loop early
for i in range(10):
    if i == 5:
        break
    print(i)    # 0, 1, 2, 3, 4

# continue - skip current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)    # 0, 1, 3, 4
```

---

## Functions

```python
# Define a function
def greet(name):
    return f"Hello, {name}!"

# Call it
print(greet("Rahul"))    # Hello, Rahul!

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Priya"))             # Hello, Priya!
print(greet("Priya", "Hi"))       # Hi, Priya!

# Multiple return values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, avg = get_stats([85, 90, 78, 92])
print(f"Low: {low}, High: {high}, Avg: {avg:.1f}")
```

### Lambda (one-line function)

```python
square = lambda x: x ** 2
print(square(5))    # 25

add = lambda a, b: a + b
print(add(3, 7))    # 10
```

---

## Summary

- **Python** is easy to learn, reads like English
- No type declaration needed — Python figures it out
- **f-strings** for easy formatting: `f"Hello {name}"`
- Use `//` for integer division, `/` for float division
- **Indentation matters** — Python uses 4 spaces (not curly braces)
- `for` loops with `range()` or iterate over lists directly
- Functions defined with `def`, can have default parameters
- User input with `input()` — always returns a string, convert with `int()`/`float()`
