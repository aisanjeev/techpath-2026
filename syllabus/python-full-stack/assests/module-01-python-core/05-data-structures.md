# Data Structures — list, tuple, set, dict

**Module 01 — Python Core: Language Fundamentals | Topic 5**

---

## Why Data Structures Matter

So far, you have stored single values in variables. But real programs deal with collections of data — a list of students, a set of unique cities, a dictionary of student profiles. Python gives you four built-in data structures:

| Structure | Ordered? | Mutable? | Duplicates? | Syntax |
|-----------|----------|----------|-------------|--------|
| **list** | Yes | Yes | Yes | `[1, 2, 3]` |
| **tuple** | Yes | No | Yes | `(1, 2, 3)` |
| **set** | No | Yes | No | `{1, 2, 3}` |
| **dict** | Yes* | Yes | Keys: No | `{"a": 1}` |

*Dicts are insertion-ordered since Python 3.7.

---

## Lists — Ordered, Mutable Collections

A list is the most versatile data structure. Think of it as a to-do list — you can add, remove, and reorder items.

### Creating Lists

```python
students = ["Rahul", "Priya", "Amit", "Sneha"]
marks = [85, 92, 78, 88]
mixed = ["Rahul", 22, True, 85.5]    # Different types allowed
empty = []
```

### Accessing Items (Indexing)

```python
students = ["Rahul", "Priya", "Amit", "Sneha"]

print(students[0])     # Rahul (first item)
print(students[1])     # Priya (second item)
print(students[-1])    # Sneha (last item)
print(students[-2])    # Amit (second from last)
```

### Slicing

```python
students = ["Rahul", "Priya", "Amit", "Sneha", "Vikram"]

print(students[1:3])     # ['Priya', 'Amit'] (index 1 to 2)
print(students[:3])      # ['Rahul', 'Priya', 'Amit'] (first 3)
print(students[2:])      # ['Amit', 'Sneha', 'Vikram'] (from index 2)
print(students[::2])     # ['Rahul', 'Amit', 'Vikram'] (every 2nd)
print(students[::-1])    # Reversed list
```

### List Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `append(x)` | Add to end | `students.append("Ananya")` |
| `insert(i, x)` | Add at index | `students.insert(0, "Vikram")` |
| `extend(list)` | Add multiple items | `students.extend(["A", "B"])` |
| `remove(x)` | Remove first occurrence | `students.remove("Amit")` |
| `pop(i)` | Remove and return at index | `students.pop(0)` |
| `pop()` | Remove and return last | `students.pop()` |
| `index(x)` | Find index of item | `students.index("Priya")` |
| `count(x)` | Count occurrences | `marks.count(85)` |
| `sort()` | Sort in place | `marks.sort()` |
| `sort(reverse=True)` | Sort descending | `marks.sort(reverse=True)` |
| `reverse()` | Reverse in place | `students.reverse()` |
| `copy()` | Shallow copy | `new = students.copy()` |
| `clear()` | Remove all items | `students.clear()` |

### Common List Operations

```python
students = ["Rahul", "Priya", "Amit"]

# Length
print(len(students))    # 3

# Check membership
print("Rahul" in students)      # True
print("Sneha" not in students)   # True

# Concatenation
batch_a = ["Rahul", "Priya"]
batch_b = ["Amit", "Sneha"]
all_students = batch_a + batch_b

# Repetition
dashes = ["-"] * 20

# Unpacking
first, *rest = students
print(first)    # Rahul
print(rest)     # ['Priya', 'Amit']
```

### Sorting

```python
marks = [78, 92, 85, 45, 88]

# sorted() — returns new list, original unchanged
sorted_marks = sorted(marks)
print(sorted_marks)    # [45, 78, 85, 88, 92]

# .sort() — modifies the list in place
marks.sort(reverse=True)
print(marks)    # [92, 88, 85, 78, 45]

# Sort complex data
students = [
    {"name": "Rahul", "marks": 78},
    {"name": "Priya", "marks": 92},
    {"name": "Amit", "marks": 85},
]
students.sort(key=lambda s: s["marks"], reverse=True)
# Now: Priya (92), Amit (85), Rahul (78)
```

---

## Tuples — Ordered, Immutable Collections

A tuple is like a list, but you **cannot change it** after creation. Use tuples for data that should not be modified.

### Creating Tuples

```python
coordinates = (23.2599, 77.4126)    # Bhopal coordinates
rgb_color = (255, 128, 0)
single = (42,)    # One-item tuple needs trailing comma!
empty = ()
```

### Accessing Items

```python
coordinates = (23.2599, 77.4126)
print(coordinates[0])    # 23.2599
print(coordinates[1])    # 77.4126
```

### Tuple Unpacking

```python
# Assign tuple values to separate variables
name, city, marks = ("Rahul", "Bhopal", 85)
print(f"{name} from {city}: {marks}")

# Swap variables
a, b = 5, 10
a, b = b, a    # Uses tuple unpacking internally
```

### Why Use Tuples Instead of Lists?

| Feature | Tuple | List |
|---------|-------|------|
| Mutability | Cannot change | Can change |
| Performance | Slightly faster | Slightly slower |
| As dict key | Yes | No |
| Safety | Data protected | Data can be modified |
| Use case | Fixed data (coordinates, RGB) | Dynamic data (student list) |

```python
# Tuples can be dictionary keys (lists cannot)
locations = {
    (23.26, 77.41): "Bhopal",
    (28.61, 77.21): "Delhi",
    (18.52, 73.86): "Pune",
}
print(locations[(23.26, 77.41)])    # Bhopal
```

### Named Tuples

For more readable tuples, use `namedtuple`:

```python
from collections import namedtuple

Student = namedtuple("Student", ["name", "city", "marks"])
s = Student("Priya", "Pune", 92)

print(s.name)     # Priya
print(s.marks)    # 92
print(s[0])       # Priya (still works by index)
```

---

## Sets — Unordered, Unique Collections

A set stores **unique items only** — duplicates are automatically removed. Sets are unordered, so you cannot access items by index.

### Creating Sets

```python
cities = {"Bhopal", "Delhi", "Pune", "Bhopal", "Delhi"}
print(cities)    # {'Bhopal', 'Delhi', 'Pune'} — duplicates removed

# From a list
marks = [85, 92, 78, 85, 92]
unique_marks = set(marks)
print(unique_marks)    # {78, 85, 92}

empty_set = set()    # NOT {} — that creates an empty dict!
```

### Set Operations

```python
batch_a = {"Rahul", "Priya", "Amit"}
batch_b = {"Priya", "Sneha", "Vikram"}

# Union — all students from both batches
print(batch_a | batch_b)
# {'Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram'}

# Intersection — students in BOTH batches
print(batch_a & batch_b)
# {'Priya'}

# Difference — only in batch_a
print(batch_a - batch_b)
# {'Rahul', 'Amit'}

# Symmetric difference — in one but not both
print(batch_a ^ batch_b)
# {'Rahul', 'Amit', 'Sneha', 'Vikram'}
```

### Set Methods

| Method | What It Does |
|--------|-------------|
| `add(x)` | Add one item |
| `update(set)` | Add multiple items |
| `remove(x)` | Remove (error if missing) |
| `discard(x)` | Remove (no error if missing) |
| `pop()` | Remove and return random item |
| `issubset(set)` | Check if all items are in other set |
| `issuperset(set)` | Check if contains all items of other set |

### When to Use Sets

```python
# Remove duplicates from a list
emails = ["a@b.com", "c@d.com", "a@b.com", "e@f.com"]
unique_emails = list(set(emails))

# Fast membership check (faster than list for large data)
valid_courses = {"Python Full Stack", "Web Development", "Data Science"}
if "Python Full Stack" in valid_courses:
    print("Valid course!")
```

---

## Dictionaries — Key-Value Pairs

A dictionary stores data as **key-value pairs**. Think of it as a real dictionary — you look up a word (key) to find its meaning (value).

### Creating Dictionaries

```python
student = {
    "name": "Rahul",
    "age": 22,
    "city": "Bhopal",
    "course": "Python Full Stack",
    "fee": 25000,
    "is_enrolled": True,
}
```

### Accessing Values

```python
# Using keys
print(student["name"])       # Rahul
print(student["city"])       # Bhopal

# Using .get() — safer (returns None if key missing)
print(student.get("email"))              # None
print(student.get("email", "N/A"))       # N/A (default value)

# student["email"] would raise KeyError!
```

### Adding and Modifying

```python
# Add new key
student["email"] = "rahul@techpath.com"

# Modify existing
student["fee"] = 22000

# Update multiple keys at once
student.update({"city": "Delhi", "batch": 2026})
```

### Dictionary Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `keys()` | All keys | `student.keys()` |
| `values()` | All values | `student.values()` |
| `items()` | Key-value pairs | `student.items()` |
| `get(key, default)` | Safe access | `student.get("age", 0)` |
| `pop(key)` | Remove and return | `student.pop("email")` |
| `update(dict)` | Merge another dict | `student.update({...})` |
| `setdefault(k, v)` | Set if not exists | `student.setdefault("marks", [])` |
| `copy()` | Shallow copy | `new = student.copy()` |

### Looping Over Dictionaries

```python
student = {"name": "Rahul", "city": "Bhopal", "marks": 85}

# Keys
for key in student:
    print(key)

# Values
for value in student.values():
    print(value)

# Both
for key, value in student.items():
    print(f"{key}: {value}")
```

### Nested Dictionaries

```python
classroom = {
    "batch": "Python Full Stack 2026",
    "students": [
        {"name": "Rahul", "city": "Bhopal", "marks": 85},
        {"name": "Priya", "city": "Pune", "marks": 92},
        {"name": "Amit", "city": "Delhi", "marks": 78},
    ],
    "instructor": {
        "name": "Sneha Verma",
        "experience": "5 years",
    },
}

# Access nested data
print(classroom["students"][0]["name"])        # Rahul
print(classroom["instructor"]["name"])         # Sneha Verma

# Loop nested
for s in classroom["students"]:
    print(f"{s['name']} — {s['marks']}")
```

### Dictionary Comprehension

```python
# Square numbers
squares = {x: x ** 2 for x in range(1, 6)}
print(squares)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter students by marks
students = {"Rahul": 85, "Priya": 92, "Amit": 42, "Sneha": 78}
toppers = {name: marks for name, marks in students.items() if marks >= 80}
print(toppers)    # {'Rahul': 85, 'Priya': 92}
```

---

## Choosing the Right Data Structure

| Need | Use | Example |
|------|-----|---------|
| Ordered collection you can modify | `list` | Student names |
| Fixed collection that won't change | `tuple` | Coordinates, RGB colors |
| Unique values, no duplicates | `set` | Unique email addresses |
| Key-value mapping | `dict` | Student profiles |
| Fast lookup by key | `dict` or `set` | Config settings |

---

## Summary

| Structure | Create | Add | Remove | Access |
|-----------|--------|-----|--------|--------|
| `list` | `[1, 2]` | `.append(3)` | `.remove(1)` | `lst[0]` |
| `tuple` | `(1, 2)` | N/A | N/A | `tup[0]` |
| `set` | `{1, 2}` | `.add(3)` | `.discard(1)` | `in` check |
| `dict` | `{"a": 1}` | `d["b"] = 2` | `d.pop("a")` | `d["a"]` |

---

## Practice Tasks

1. Create a list of 5 student names. Add two more, remove one, sort it, and print.
2. Create a tuple of your city's (lat, lon) and use it as a dictionary key.
3. Given two lists of student names, use sets to find students in both lists.
4. Create a nested dictionary representing a classroom with students and an instructor.
5. Use a dictionary comprehension to create a grade mapping: marks to grade for each student.
