# Module 01: Python Core — Language Fundamentals

## 1. Python Setup & Environment

### Installing Python
- Download Python 3.12+ from [python.org](https://www.python.org/downloads/)
- During installation on Windows, **check "Add Python to PATH"**
- Verify installation:
```bash
python --version
pip --version
```

### The Python REPL
REPL stands for **Read-Eval-Print-Loop** — an interactive Python shell.
```bash
python
>>> 2 + 3
5
>>> print("Welcome to TechPath Institute!")
Welcome to TechPath Institute!
>>> exit()
```

### VS Code Setup
1. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com)
2. Install the **Python extension** by Microsoft
3. Open a folder → Create a file `hello.py` → Write `print("Hello!")` → Run with `Ctrl+Shift+P` → "Run Python File"

### Virtual Environments
A virtual environment keeps your project's packages isolated from other projects.

```bash
# Create a virtual environment
python -m venv myenv

# Activate it
# Windows:
myenv\Scripts\activate
# Mac/Linux:
source myenv/bin/activate

# Install packages inside it
pip install requests

# Deactivate when done
deactivate
```

### pip — Python Package Manager
```bash
pip install package_name       # Install a package
pip install package==1.2.3     # Install specific version
pip list                       # List installed packages
pip freeze > requirements.txt  # Save dependencies
pip install -r requirements.txt  # Install from file
pip uninstall package_name     # Remove a package
```

---

## 2. Variables, Data Types & Operators

### Variables
Variables store data. Python figures out the type automatically (dynamic typing).
```python
name = "Rahul"           # str (text)
age = 22                 # int (whole number)
fee = 15999.50           # float (decimal number)
is_enrolled = True       # bool (True/False)

print(type(name))   # <class 'str'>
print(type(age))    # <class 'int'>
```

### Data Types Summary

| Type    | Example              | Description              |
|---------|----------------------|--------------------------|
| `int`   | `42`, `-7`, `0`      | Whole numbers            |
| `float` | `3.14`, `-0.5`       | Decimal numbers          |
| `str`   | `"hello"`, `'world'` | Text (in quotes)         |
| `bool`  | `True`, `False`      | Yes/No values            |
| `None`  | `None`               | Empty/no value           |

### Type Casting
Converting one type to another:
```python
x = "100"
y = int(x)       # str → int: 100
z = float(x)     # str → float: 100.0
w = str(42)      # int → str: "42"
a = bool(0)      # int → bool: False (0 is False, everything else is True)
```

### Operators

**Arithmetic Operators:**
```python
10 + 3    # 13  (addition)
10 - 3    # 7   (subtraction)
10 * 3    # 30  (multiplication)
10 / 3    # 3.333... (division — always returns float)
10 // 3   # 3   (floor division — whole number only)
10 % 3    # 1   (modulo — remainder)
10 ** 3   # 1000 (power)
```

**Comparison Operators:**
```python
5 == 5    # True  (equal to)
5 != 3    # True  (not equal to)
5 > 3     # True  (greater than)
5 < 3     # False (less than)
5 >= 5    # True  (greater than or equal)
5 <= 3    # False (less than or equal)
```

**Logical Operators:**
```python
True and False   # False
True or False    # True
not True         # False
```

### String Formatting with f-strings
```python
name = "Priya"
course = "Python Full Stack"
fee = 25000

# f-string (recommended — Python 3.6+)
print(f"Hi {name}, you enrolled in {course}. Fee: ₹{fee}")

# Formatting numbers
pi = 3.14159
print(f"Pi is approximately {pi:.2f}")  # Pi is approximately 3.14

# Expressions inside f-strings
print(f"Fee with GST: ₹{fee * 1.18:.0f}")  # Fee with GST: ₹29500
```

---

## 3. Control Flow

### if / elif / else
```python
marks = 72

if marks >= 90:
    print("Grade: A+")
elif marks >= 75:
    print("Grade: A")
elif marks >= 60:
    print("Grade: B")
elif marks >= 40:
    print("Grade: C")
else:
    print("Grade: Fail")
```

### for Loop
```python
# Loop through a list
cities = ["Bhopal", "Delhi", "Pune", "Mumbai"]
for city in cities:
    print(f"TechPath has students from {city}")

# Loop with range
for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(f"Student {i}")

# Loop with index using enumerate
for index, city in enumerate(cities):
    print(f"{index + 1}. {city}")
```

### while Loop
```python
count = 1
while count <= 5:
    print(f"Attempt {count}")
    count += 1
```

### break, continue, pass
```python
# break — stop the loop
for num in range(1, 100):
    if num == 5:
        break
    print(num)  # Prints 1, 2, 3, 4

# continue — skip current iteration
for num in range(1, 6):
    if num == 3:
        continue
    print(num)  # Prints 1, 2, 4, 5

# pass — do nothing (placeholder)
for num in range(5):
    pass  # TODO: add logic later
```

### List Comprehensions
A compact way to create lists:
```python
# Regular way
squares = []
for x in range(1, 6):
    squares.append(x ** 2)

# Comprehension way (same result)
squares = [x ** 2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# With condition
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
# [4, 16, 36, 64, 100]

# Dictionary comprehension
prices = {"Chai": 10, "Coffee": 30, "Samosa": 15}
gst_prices = {item: price * 1.18 for item, price in prices.items()}
```

---

## 4. Functions

### Defining Functions
```python
def greet(name):
    """Greet a TechPath student."""
    return f"Welcome to TechPath Institute, {name}!"

message = greet("Ananya")
print(message)  # Welcome to TechPath Institute, Ananya!
```

### Default Arguments
```python
def calculate_fee(base_fee, discount=0):
    """Calculate fee after discount."""
    final = base_fee - (base_fee * discount / 100)
    return final

print(calculate_fee(25000))        # 25000 (no discount)
print(calculate_fee(25000, 10))    # 22500 (10% discount)
```

### *args and **kwargs
```python
# *args — accept any number of positional arguments
def total_marks(*marks):
    return sum(marks)

print(total_marks(85, 90, 78, 92))  # 345

# **kwargs — accept any number of keyword arguments
def student_info(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

student_info(name="Rahul", city="Bhopal", course="Python")
```

### Lambda Functions
Small anonymous functions for quick operations:
```python
square = lambda x: x ** 2
print(square(5))  # 25

# Useful with sorting
students = [("Rahul", 85), ("Priya", 92), ("Amit", 78)]
students.sort(key=lambda s: s[1], reverse=True)
# [('Priya', 92), ('Rahul', 85), ('Amit', 78)]
```

### Scope (LEGB Rule)
Python looks for variables in this order:
1. **L**ocal — inside the current function
2. **E**nclosing — in outer functions (for nested functions)
3. **G**lobal — at module level
4. **B**uilt-in — Python's built-in names (print, len, etc.)

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # "local"
    inner()

outer()
print(x)  # "global"
```

---

## 5. Data Structures in Depth

### Lists (Ordered, Mutable)
```python
students = ["Rahul", "Priya", "Amit", "Sneha"]

# Accessing
students[0]      # "Rahul" (first)
students[-1]     # "Sneha" (last)
students[1:3]    # ["Priya", "Amit"] (slice)

# Modifying
students.append("Neha")       # Add to end
students.insert(1, "Vikram")  # Insert at index 1
students.remove("Amit")       # Remove by value
popped = students.pop()       # Remove & return last item

# Useful methods
students.sort()               # Sort alphabetically
students.reverse()            # Reverse order
len(students)                 # Count items
"Rahul" in students           # True (check membership)
```

### Tuples (Ordered, Immutable)
```python
coordinates = (23.2599, 77.4126)  # Bhopal coordinates
# coordinates[0] = 25  # ERROR! Tuples cannot be changed

# Unpacking
lat, lon = coordinates
print(f"Bhopal: {lat}N, {lon}E")

# Named tuples (more readable)
from collections import namedtuple
Student = namedtuple("Student", ["name", "age", "city"])
s = Student("Priya", 21, "Pune")
print(s.name)  # "Priya"
```

### Sets (Unordered, Unique Items)
```python
skills = {"Python", "HTML", "CSS", "Python"}  # Duplicate removed
print(skills)  # {"Python", "HTML", "CSS"}

# Set operations
frontend = {"HTML", "CSS", "JavaScript"}
backend = {"Python", "SQL", "JavaScript"}

frontend & backend   # {"JavaScript"} — intersection
frontend | backend   # All skills — union
frontend - backend   # {"HTML", "CSS"} — difference
```

### Dictionaries (Key-Value Pairs)
```python
student = {
    "name": "Rahul Sharma",
    "age": 22,
    "city": "Bhopal",
    "courses": ["Python", "Web Dev"],
    "fee_paid": True
}

# Accessing
student["name"]           # "Rahul Sharma"
student.get("phone", "N/A")  # "N/A" (safe access with default)

# Modifying
student["age"] = 23                # Update
student["email"] = "r@mail.com"    # Add new key

# Iteration
for key, value in student.items():
    print(f"{key}: {value}")

# Useful methods
student.keys()     # All keys
student.values()   # All values
student.pop("email")  # Remove and return
```

### Unpacking
```python
# List unpacking
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

# Dictionary unpacking
defaults = {"theme": "dark", "lang": "en"}
user_prefs = {"lang": "hi", "font_size": 14}
merged = {**defaults, **user_prefs}
# {"theme": "dark", "lang": "hi", "font_size": 14}
```

---

## 6. String Operations & Regex

### Common String Methods
```python
text = "  Welcome to TechPath Institute  "

text.strip()          # Remove leading/trailing spaces
text.lower()          # All lowercase
text.upper()          # All uppercase
text.title()          # Title Case
text.replace("TechPath", "TP")  # Replace substring
text.split()          # Split into list of words
text.startswith("  We")  # True
text.endswith("te  ")    # True
text.find("Tech")     # 14 (index of first occurrence)
text.count("e")       # 3
",".join(["a", "b", "c"])  # "a,b,c"
```

### Regex Basics (re module)
Regular expressions are patterns for matching text.
```python
import re

text = "Contact us at support@techpath.biz or call 9876543210"

# Find all email addresses
emails = re.findall(r'[\w.]+@[\w.]+', text)
# ['support@techpath.biz']

# Find all phone numbers (10 digits)
phones = re.findall(r'\d{10}', text)
# ['9876543210']

# Check if string matches a pattern
if re.match(r'^[A-Z]', "Hello"):
    print("Starts with uppercase")

# Replace using regex
clean = re.sub(r'\d+', 'XXX', "Call 9876543210 or 1234567890")
# "Call XXX or XXX"

# Common patterns
# \d  — digit (0-9)
# \w  — word character (a-z, A-Z, 0-9, _)
# \s  — whitespace
# .   — any character
# +   — one or more
# *   — zero or more
# ?   — zero or one
# {n} — exactly n times
# ^   — start of string
# $   — end of string
```

---

## 7. Exception Handling

### try / except / finally
```python
try:
    age = int(input("Enter your age: "))
    print(f"You are {age} years old")
except ValueError:
    print("Please enter a valid number!")
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    print("This always runs")
```

### Common Exception Types
| Exception         | When it happens                     |
|--------------------|-------------------------------------|
| `ValueError`       | Wrong type of value                 |
| `TypeError`        | Wrong data type in operation        |
| `IndexError`       | List index out of range             |
| `KeyError`         | Dictionary key not found            |
| `FileNotFoundError`| File does not exist                 |
| `ZeroDivisionError`| Division by zero                    |
| `AttributeError`   | Object has no such attribute        |

### Custom Exceptions
```python
class InsufficientBalanceError(Exception):
    """Raised when account balance is too low."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw ₹{amount}. Balance is only ₹{balance}"
        )

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(balance, amount)
    return balance - amount

try:
    new_balance = withdraw(5000, 8000)
except InsufficientBalanceError as e:
    print(e)  # Cannot withdraw ₹8000. Balance is only ₹5000
```

---

## 8. File I/O

### Reading & Writing Text Files
```python
# Writing to a file
with open("students.txt", "w", encoding="utf-8") as f:
    f.write("Rahul Sharma, Bhopal\n")
    f.write("Priya Patel, Pune\n")
    f.write("Amit Kumar, Delhi\n")

# Reading a file
with open("students.txt", "r", encoding="utf-8") as f:
    content = f.read()       # Entire file as string
    # OR
    # lines = f.readlines()  # List of lines

# Reading line by line (memory efficient)
with open("students.txt", "r", encoding="utf-8") as f:
    for line in f:
        name, city = line.strip().split(", ")
        print(f"{name} is from {city}")
```

### Working with CSV
```python
import csv

# Writing CSV
students = [
    ["Name", "City", "Fee"],
    ["Rahul", "Bhopal", 25000],
    ["Priya", "Pune", 22000],
    ["Amit", "Delhi", 28000],
]

with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)

# Reading CSV
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Name']} from {row['City']} — Fee: ₹{row['Fee']}")
```

### Working with JSON
```python
import json

# Writing JSON
student_data = {
    "institute": "TechPath Institute",
    "students": [
        {"name": "Rahul", "city": "Bhopal", "fee": 25000},
        {"name": "Priya", "city": "Pune", "fee": 22000},
    ]
}

with open("students.json", "w", encoding="utf-8") as f:
    json.dump(student_data, f, indent=2, ensure_ascii=False)

# Reading JSON
with open("students.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for s in data["students"]:
    print(f"{s['name']} — ₹{s['fee']}")
```

### Context Managers (with statement)
The `with` statement ensures files are properly closed, even if an error occurs:
```python
# This is safe — file closes automatically
with open("data.txt", "r") as f:
    content = f.read()

# Without 'with' (NOT recommended)
f = open("data.txt", "r")
content = f.read()
f.close()  # Easy to forget!
```

---

## Quick Reference

| Concept | Syntax | Example |
|---------|--------|---------|
| Print | `print()` | `print("Hello")` |
| Input | `input()` | `name = input("Name: ")` |
| Type check | `type()` | `type(42)` → `int` |
| Length | `len()` | `len([1,2,3])` → `3` |
| Range | `range()` | `range(1, 10, 2)` → 1,3,5,7,9 |
| f-string | `f"..."` | `f"Hi {name}"` |
| List comp | `[expr for x in iter]` | `[x**2 for x in range(5)]` |
| Dict comp | `{k: v for ...}` | `{x: x**2 for x in range(5)}` |
| Ternary | `x if cond else y` | `"Pass" if marks >= 40 else "Fail"` |
