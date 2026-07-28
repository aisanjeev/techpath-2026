# Python Data Structures

**Module 10 — Python Programming | Topic 2**

---

## Lists — Ordered, Changeable Collections

```python
# Create a list
marks = [85, 90, 78, 92, 88]
names = ["Rahul", "Priya", "Amit"]
mixed = [1, "hello", True, 3.14]

# Access items (index starts at 0)
print(marks[0])      # 85 (first)
print(marks[-1])     # 88 (last)
print(marks[1:3])    # [90, 78] (slice)
```

### List Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `.append(x)` | Add to end | `marks.append(95)` |
| `.insert(i, x)` | Add at position | `marks.insert(0, 100)` |
| `.remove(x)` | Remove first match | `marks.remove(78)` |
| `.pop()` | Remove last (or at index) | `marks.pop()` |
| `.sort()` | Sort in place | `marks.sort()` |
| `.reverse()` | Reverse in place | `marks.reverse()` |
| `.index(x)` | Find position | `marks.index(90)` → `1` |
| `.count(x)` | Count occurrences | `marks.count(90)` → `1` |
| `len(list)` | Length | `len(marks)` → `5` |

### List Comprehension

```python
# Create new list from existing
numbers = [1, 2, 3, 4, 5]

# Squares of all numbers
squares = [x**2 for x in numbers]           # [1, 4, 9, 16, 25]

# Only even numbers
evens = [x for x in numbers if x % 2 == 0]  # [2, 4]

# Uppercase names
names = ["rahul", "priya"]
upper = [n.upper() for n in names]           # ["RAHUL", "PRIYA"]
```

---

## Tuples — Like Lists but Cannot Change

```python
# Create a tuple
coordinates = (10, 20)
colors = ("red", "green", "blue")

# Access (same as list)
print(colors[0])    # "red"

# CANNOT modify
# colors[0] = "yellow"   # ERROR!

# Unpack
x, y = coordinates
print(x, y)    # 10 20

# When to use tuple?
# When data should NOT change (coordinates, config values)
```

---

## Dictionaries — Key-Value Pairs

```python
# Create a dictionary
student = {
    "name": "Rahul",
    "age": 20,
    "course": "ADCA",
    "marks": [85, 90, 78]
}

# Access values
print(student["name"])          # Rahul
print(student.get("email", "N/A"))  # N/A (safe access)

# Add / update
student["email"] = "rahul@email.com"
student["age"] = 21

# Remove
del student["email"]

# Loop through
for key, value in student.items():
    print(f"{key}: {value}")

# Check if key exists
if "name" in student:
    print("Name exists!")
```

### Dictionary Methods

| Method | What It Does |
|--------|-------------|
| `.keys()` | All keys |
| `.values()` | All values |
| `.items()` | All key-value pairs |
| `.get(key, default)` | Safe access with fallback |
| `.update(dict2)` | Merge another dict |
| `.pop(key)` | Remove and return value |

---

## Sets — Unique Items Only

```python
# Create a set (no duplicates allowed)
fruits = {"apple", "banana", "mango"}
numbers = {1, 2, 3, 2, 1}    # {1, 2, 3} — duplicates removed

# Add / remove
fruits.add("grapes")
fruits.remove("banana")

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)    # Union: {1, 2, 3, 4, 5, 6}
print(a & b)    # Intersection: {3, 4}
print(a - b)    # Difference: {1, 2}
```

---

## Comparison Table

| Feature | List | Tuple | Dict | Set |
|---------|------|-------|------|-----|
| **Syntax** | `[1,2,3]` | `(1,2,3)` | `{"a":1}` | `{1,2,3}` |
| **Ordered?** | Yes | Yes | Yes (3.7+) | No |
| **Changeable?** | Yes | No | Yes | Yes |
| **Duplicates?** | Yes | Yes | No (keys) | No |
| **Access by** | Index | Index | Key | N/A |
| **Use for** | General lists | Fixed data | Key-value data | Unique items |

---

## File Handling

```python
# Write to file
with open("notes.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Python is great!\n")

# Read entire file
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)

# Read line by line
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())

# Append to file
with open("notes.txt", "a") as f:
    f.write("New line added.\n")
```

| Mode | What It Does |
|------|-------------|
| `"r"` | Read (default) |
| `"w"` | Write (overwrites) |
| `"a"` | Append (adds to end) |
| `"x"` | Create new (error if exists) |

> **Always use `with` statement** — it automatically closes the file.

---

## Error Handling

```python
try:
    age = int(input("Enter age: "))
    print(f"You are {age} years old")
except ValueError:
    print("Please enter a valid number!")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Done!")   # Always runs
```

### Common Errors

| Error | Cause |
|-------|-------|
| `SyntaxError` | Wrong code structure |
| `NameError` | Variable doesn't exist |
| `TypeError` | Wrong data type used |
| `ValueError` | Right type, wrong value |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key doesn't exist |
| `ZeroDivisionError` | Dividing by zero |
| `FileNotFoundError` | File doesn't exist |

---

## Modules & Imports

```python
# Import entire module
import math
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.14159...

# Import specific function
from random import randint, choice
print(randint(1, 100))         # Random number 1-100
print(choice(["a", "b", "c"])) # Random pick

# Import with alias
import datetime as dt
today = dt.date.today()
print(today)

# Common built-in modules
# math, random, datetime, os, json, csv, re
```

---

## OOP Basics — Classes & Objects

```python
class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course
        self.marks = []

    def add_marks(self, mark):
        self.marks.append(mark)

    def average(self):
        if not self.marks:
            return 0
        return sum(self.marks) / len(self.marks)

    def display(self):
        print(f"{self.name} | Age: {self.age} | Course: {self.course}")
        print(f"Marks: {self.marks} | Average: {self.average():.1f}")

# Create objects
s1 = Student("Rahul", 20, "ADCA")
s1.add_marks(85)
s1.add_marks(90)
s1.add_marks(78)
s1.display()
```

---

## Summary

- **Lists** `[]` — ordered, changeable, use for most collections
- **Tuples** `()` — ordered, cannot change, use for fixed data
- **Dicts** `{}` — key-value pairs, use for structured data
- **Sets** `{}` — unique items only, use for removing duplicates
- **List comprehension** — short way to create lists: `[x**2 for x in nums]`
- **File handling** — use `with open()` for safe file operations
- **Try/except** — handle errors gracefully
- **Classes** — blueprint for creating objects with data and methods
