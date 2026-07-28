# Cheat Sheet — Python Core: Language Fundamentals

**Module 01 | Quick Reference Card**

---

## Setup & Environment

```bash
python --version                    # Check Python version
pip install package_name            # Install package
pip freeze > requirements.txt       # Save dependencies
pip install -r requirements.txt     # Install from file
python -m venv venv                 # Create virtual environment
venv\Scripts\activate               # Activate (Windows)
source venv/bin/activate            # Activate (Mac/Linux)
deactivate                          # Deactivate venv
```

---

## Data Types

| Type | Example | Check |
|------|---------|-------|
| `int` | `42`, `-7`, `1_00_000` | `type(x)` or `isinstance(x, int)` |
| `float` | `3.14`, `-2.5` | `isinstance(x, float)` |
| `str` | `"hello"`, `'hi'` | `isinstance(x, str)` |
| `bool` | `True`, `False` | `isinstance(x, bool)` |
| `None` | `None` | `x is None` |

### Type Casting

```python
int("42")       # 42          str(42)       # "42"
float("3.14")   # 3.14        bool(0)       # False
int(3.9)        # 3 (truncates, not rounds!)
```

### Falsy Values

`0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`

---

## Operators

| Operator | Example | Result |
|----------|---------|--------|
| `+` `-` `*` `/` | `10 / 3` | `3.333` |
| `//` | `10 // 3` | `3` (floor) |
| `%` | `10 % 3` | `1` (remainder) |
| `**` | `2 ** 10` | `1024` (power) |
| `==` `!=` `>` `<` `>=` `<=` | `5 >= 5` | `True` |
| `and` `or` `not` | `True and False` | `False` |
| `in` | `"a" in "abc"` | `True` |
| `is` | `x is None` | Identity check |

---

## f-Strings

```python
f"Hello {name}"                    # Variable
f"Total: ₹{price:.2f}"           # 2 decimals
f"Count: {n:05d}"                  # Zero-padded
f"Salary: ₹{sal:,}"              # Thousands separator
f"Score: {pct:.1%}"                # Percentage
f"{'Pass' if m>=60 else 'Fail'}"   # Ternary
```

---

## Control Flow

```python
# if-elif-else
if x > 90:    grade = "A+"
elif x > 80:  grade = "A"
else:         grade = "B"

# Ternary
status = "Pass" if marks >= 60 else "Fail"

# for loop
for i in range(5):           # 0,1,2,3,4
for i in range(1, 6):        # 1,2,3,4,5
for i in range(0, 10, 2):    # 0,2,4,6,8
for i, v in enumerate(lst):  # index + value

# while loop
while condition:
    # do something
    break       # exit loop
    continue    # skip to next iteration
```

---

## Functions

```python
def greet(name, greeting="Hello"):           # Default arg
    """Docstring."""
    return f"{greeting}, {name}!"

def total(*args):                             # *args = tuple
    return sum(args)

def profile(**kwargs):                        # **kwargs = dict
    for k, v in kwargs.items(): print(f"{k}: {v}")

square = lambda x: x ** 2                    # Lambda

# Scope: Local → Enclosing → Global → Built-in (LEGB)
```

---

## Data Structures

### List (ordered, mutable)

```python
lst = [1, 2, 3]
lst.append(4)           lst.insert(0, 0)
lst.remove(2)           lst.pop()              # remove last
lst.sort()              lst.reverse()
lst.index(3)            lst.count(1)
len(lst)                3 in lst               # membership
lst[0]                  lst[-1]                # index
lst[1:3]                lst[::-1]              # slice/reverse
sorted(lst, key=func)                          # new sorted list
```

### Tuple (ordered, immutable)

```python
t = (1, 2, 3)
a, b, c = t             # unpacking
single = (42,)           # one-item tuple needs comma
```

### Set (unordered, unique)

```python
s = {1, 2, 3}
s.add(4)                 s.discard(2)
a | b                    # union
a & b                    # intersection
a - b                    # difference
```

### Dict (key-value)

```python
d = {"name": "Rahul", "age": 22}
d["name"]                d.get("email", "N/A")
d["email"] = "r@t.com"   d.pop("age")
d.keys()    d.values()    d.items()
d.update({"city": "Bhopal"})
```

---

## Comprehensions

```python
[x**2 for x in range(5)]                     # List
[x for x in lst if x > 0]                    # Filtered
{x: x**2 for x in range(5)}                  # Dict
{x for x in lst}                              # Set
```

---

## Strings

```python
s.upper()    s.lower()    s.title()    s.strip()
s.split(",")              ",".join(lst)
s.replace("old", "new")   s.find("sub")       # -1 if not found
s.startswith("pre")        s.endswith("suf")
s.isdigit()   s.isalpha()  s.isalnum()
s[0:5]        s[::-1]      len(s)
```

---

## Regex (import re)

```python
re.search(r"pattern", text)       # First match (or None)
re.findall(r"pattern", text)      # All matches (list)
re.sub(r"pattern", "repl", text)  # Replace
re.split(r"pattern", text)        # Split by pattern
re.match(r"pattern", text)        # Match at start only

# Common patterns
\d   digit       \D   non-digit      .    any char
\w   word char   \W   non-word       \s   whitespace
^    start       $    end
+    1 or more   *    0 or more      ?    0 or 1
{n}  exactly n   {n,m} n to m
[a-z] range      [^a] not a          (group)
```

---

## Exception Handling

```python
try:
    risky_code()
except ValueError as e:
    print(f"Error: {e}")
except (TypeError, KeyError):
    print("Type or key error")
else:
    print("No error occurred")
finally:
    print("Always runs")

raise ValueError("Custom message")

class MyError(Exception):
    pass
```

---

## File I/O

```python
# Text files
with open("file.txt", "r") as f:
    content = f.read()           # Entire file
    lines = f.readlines()        # List of lines

with open("file.txt", "w") as f:   # Overwrite
    f.write("Hello\n")

with open("file.txt", "a") as f:   # Append
    f.write("More\n")

# CSV
import csv
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])

# JSON
import json
data = json.load(open("f.json"))          # File → dict
json.dump(data, open("f.json","w"), indent=2)  # Dict → file
json.loads('{"a":1}')                     # String → dict
json.dumps({"a": 1})                      # Dict → string

# pathlib
from pathlib import Path
p = Path("data") / "file.txt"
p.exists()    p.is_file()    p.is_dir()
p.read_text()                p.write_text("hi")
p.name   p.stem   p.suffix   p.parent
```

---

## Common Built-in Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `len()` | Length | `len([1,2,3])` → `3` |
| `type()` | Type | `type(42)` → `<class 'int'>` |
| `range()` | Number sequence | `range(1, 6)` |
| `enumerate()` | Index + value | `enumerate(["a","b"])` |
| `zip()` | Pair iterables | `zip([1,2], ["a","b"])` |
| `map()` | Apply function | `map(str, [1,2,3])` |
| `filter()` | Filter items | `filter(bool, [0,1,2])` |
| `sorted()` | New sorted list | `sorted([3,1,2])` |
| `min()` / `max()` | Min/max value | `max([3,1,2])` → `3` |
| `sum()` | Total | `sum([1,2,3])` → `6` |
| `abs()` | Absolute value | `abs(-5)` → `5` |
| `round()` | Round number | `round(3.14, 1)` → `3.1` |
| `isinstance()` | Type check | `isinstance(42, int)` → `True` |
| `input()` | User input | `input("Name: ")` → str |
| `print()` | Output | `print("Hi", end="")` |
