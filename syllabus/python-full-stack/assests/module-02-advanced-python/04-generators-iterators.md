# Generators & Iterators

**Module 02 — Advanced Python | Topic 4**

---

## The Problem: Memory

Imagine you need to process 10 million student records. Loading all of them into a list at once would use gigabytes of memory. Generators solve this by producing values **one at a time** — only when needed.

**Real-world analogy:** A generator is like a chapati maker at a dhaba. Instead of making 100 chapatis and stacking them all (wastes space, gets cold), the maker produces one chapati at a time, exactly when someone orders. That is **lazy evaluation**.

---

## Iterators — The Foundation

An iterator is any object that produces values one at a time using `__next__()`.

### How Python's for Loop Really Works

```python
students = ["Rahul", "Priya", "Amit"]

# What you write:
for name in students:
    print(name)

# What Python actually does:
iterator = iter(students)      # Get an iterator
print(next(iterator))          # Rahul
print(next(iterator))          # Priya
print(next(iterator))          # Amit
# next(iterator)               # StopIteration error — no more items
```

### The Iterator Protocol

Any object with `__iter__()` and `__next__()` methods is an iterator:

```python
class Countdown:
    """Iterator that counts down from a number."""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Usage
for num in Countdown(5):
    print(num, end=" ")    # 5 4 3 2 1
```

---

## Generators — Easy Iterators with yield

A generator function uses `yield` instead of `return`. Each time you call `next()`, it runs until the next `yield` and pauses.

```python
def countdown(n):
    """Generator that counts down from n."""
    while n > 0:
        yield n        # Pause here, give this value
        n -= 1         # Resume here on next call

# Usage
for num in countdown(5):
    print(num, end=" ")    # 5 4 3 2 1

# Or step through manually
gen = countdown(3)
print(next(gen))    # 3
print(next(gen))    # 2
print(next(gen))    # 1
# next(gen)         # StopIteration
```

### yield vs return

| Feature | `return` | `yield` |
|---------|----------|---------|
| Function type | Regular function | Generator function |
| Execution | Runs completely, returns once | Pauses at each yield, resumes |
| Memory | Stores all results | Produces one at a time |
| Can be used in for loop | No (returns single value) | Yes |

### How yield Works — Step by Step

```python
def simple_gen():
    print("Step 1")
    yield "A"
    print("Step 2")
    yield "B"
    print("Step 3")
    yield "C"
    print("Done")

gen = simple_gen()

print(next(gen))    # Prints "Step 1", returns "A"
print(next(gen))    # Prints "Step 2", returns "B"
print(next(gen))    # Prints "Step 3", returns "C"
# next(gen)         # Prints "Done", raises StopIteration
```

---

## Practical Generator Examples

### Reading Large Files

```python
def read_large_csv(filepath):
    """Read a CSV file line by line without loading entire file."""
    with open(filepath, "r") as f:
        header = f.readline().strip().split(",")
        for line in f:
            values = line.strip().split(",")
            yield dict(zip(header, values))

# Process millions of rows without running out of memory
for student in read_large_csv("students.csv"):
    if student["city"] == "Bhopal":
        print(student["name"])
```

### Generating Student IDs

```python
def id_generator(prefix="TP", start=1):
    """Generate unique student IDs."""
    counter = start
    while True:    # Infinite generator!
        yield f"{prefix}-{counter:04d}"
        counter += 1

gen = id_generator()
print(next(gen))    # TP-0001
print(next(gen))    # TP-0002
print(next(gen))    # TP-0003

# Take first 5 IDs
ids = [next(gen) for _ in range(5)]
print(ids)    # ['TP-0004', 'TP-0005', 'TP-0006', 'TP-0007', 'TP-0008']
```

### Fibonacci Sequence

```python
def fibonacci():
    """Generate infinite Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# First 10 Fibonacci numbers
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)    # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Data Pipeline

```python
def read_marks():
    """Simulate reading marks from a database."""
    data = [
        {"name": "Rahul", "marks": 85},
        {"name": "Priya", "marks": 92},
        {"name": "Amit", "marks": 42},
        {"name": "Sneha", "marks": 78},
        {"name": "Vikram", "marks": 55},
    ]
    for student in data:
        yield student

def filter_passing(students):
    """Keep only passing students."""
    for s in students:
        if s["marks"] >= 60:
            yield s

def add_grade(students):
    """Add grade to each student."""
    for s in students:
        if s["marks"] >= 90: s["grade"] = "A+"
        elif s["marks"] >= 80: s["grade"] = "A"
        elif s["marks"] >= 70: s["grade"] = "B"
        else: s["grade"] = "C"
        yield s

# Chain generators into a pipeline
pipeline = add_grade(filter_passing(read_marks()))
for student in pipeline:
    print(f"{student['name']}: {student['marks']} ({student['grade']})")
# Rahul: 85 (A)
# Priya: 92 (A+)
# Sneha: 78 (B)
```

---

## Generator Expressions

Like list comprehensions, but with parentheses instead of brackets. They produce values lazily.

```python
# List comprehension — creates entire list in memory
squares_list = [x ** 2 for x in range(1000000)]    # Uses ~8MB

# Generator expression — produces values one at a time
squares_gen = (x ** 2 for x in range(1000000))      # Uses ~120 bytes!

# Usage
print(sum(squares_gen))    # Works the same, uses almost no memory

# Practical: Sum of fees for enrolled students
students = [
    {"name": "Rahul", "fee": 25000, "enrolled": True},
    {"name": "Priya", "fee": 20000, "enrolled": True},
    {"name": "Amit", "fee": 0, "enrolled": False},
]

total = sum(s["fee"] for s in students if s["enrolled"])
print(f"Total: ₹{total:,}")    # Total: ₹45,000
```

### When to Use Generator Expressions

| Use List Comprehension | Use Generator Expression |
|------------------------|--------------------------|
| Need to access items multiple times | Processing items once |
| Need length, indexing | Feeding into sum(), max(), min() |
| Small to medium data | Large data (millions of items) |
| `[x for x in data]` | `(x for x in data)` |

---

## yield from — Delegating to Sub-generators

`yield from` lets a generator delegate to another generator:

```python
def batch_a():
    yield "Rahul"
    yield "Priya"

def batch_b():
    yield "Amit"
    yield "Sneha"

# Without yield from
def all_students_v1():
    for s in batch_a():
        yield s
    for s in batch_b():
        yield s

# With yield from (cleaner)
def all_students_v2():
    yield from batch_a()
    yield from batch_b()

print(list(all_students_v2()))    # ['Rahul', 'Priya', 'Amit', 'Sneha']
```

### Flattening Nested Lists

```python
def flatten(nested):
    """Flatten any nested iterable."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)    # Recursive!
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))    # [1, 2, 3, 4, 5, 6, 7]
```

---

## Memory Comparison

```python
import sys

# List — stores everything in memory
big_list = [x ** 2 for x in range(100000)]
print(f"List size: {sys.getsizeof(big_list):,} bytes")    # ~824,456 bytes

# Generator — stores almost nothing
big_gen = (x ** 2 for x in range(100000))
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")   # ~200 bytes

# Both produce the same values, but the generator uses 4000x less memory!
```

---

## Summary

| Concept | Syntax | Key Point |
|---------|--------|-----------|
| Iterator | `__iter__` + `__next__` | Protocol for sequential access |
| `iter()` / `next()` | `iter(list)`, `next(it)` | Manual iteration |
| Generator function | `def f(): yield x` | Lazy, memory-efficient |
| Generator expression | `(x for x in data)` | One-line generator |
| `yield from` | `yield from gen()` | Delegate to sub-generator |
| Lazy evaluation | Values produced on demand | Saves memory |
| Pipeline | Chain generators | Composable data processing |

---

## Practice Tasks

1. Write a generator that produces the first `n` even numbers
2. Create a generator that reads a file line by line and yields non-empty lines
3. Build a data pipeline with 3 generators: read -> filter -> transform
4. Compare memory usage of a list vs generator for 1 million numbers
5. Write a generator that yields Fibonacci numbers below a given limit
