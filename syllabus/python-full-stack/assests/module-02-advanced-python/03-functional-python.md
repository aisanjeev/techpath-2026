# Functional Python

**Module 02 — Advanced Python | Topic 3**

---

## What is Functional Programming?

Functional programming (FP) treats computation as the evaluation of functions. Instead of changing data in place, you create new data by passing values through functions.

**Key ideas:**
- Functions are first-class — you can pass them around like variables
- Prefer pure functions — same input always gives same output
- Avoid side effects — don't modify external state
- Use higher-order functions — functions that take/return other functions

Python is not purely functional (like Haskell), but it supports many FP concepts.

---

## map() — Transform Every Item

`map()` applies a function to every item in an iterable and returns a new iterable.

```python
# Double every number
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)    # [2, 4, 6, 8, 10]

# Add 18% GST to all prices
prices = [500, 1200, 3500, 800]
with_gst = list(map(lambda p: round(p * 1.18, 2), prices))
print(with_gst)    # [590.0, 1416.0, 4130.0, 944.0]

# Convert names to uppercase
students = ["rahul", "priya", "amit"]
upper = list(map(str.upper, students))
print(upper)    # ['RAHUL', 'PRIYA', 'AMIT']

# Using a regular function
def format_fee(fee):
    return f"₹{fee:,}"

fees = [25000, 20000, 15000]
formatted = list(map(format_fee, fees))
print(formatted)    # ['₹25,000', '₹20,000', '₹15,000']
```

### map() with Multiple Iterables

```python
names = ["Rahul", "Priya", "Amit"]
marks = [85, 92, 78]

results = list(map(lambda n, m: f"{n}: {m}", names, marks))
print(results)    # ['Rahul: 85', 'Priya: 92', 'Amit: 78']
```

---

## filter() — Keep Matching Items

`filter()` keeps only items where the function returns `True`.

```python
# Keep only passing marks
marks = [85, 42, 91, 58, 73, 36, 88]
passing = list(filter(lambda m: m >= 60, marks))
print(passing)    # [85, 91, 73, 88]

# Keep only even numbers
numbers = range(1, 21)
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)    # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Filter students by city
students = [
    {"name": "Rahul", "city": "Bhopal"},
    {"name": "Priya", "city": "Pune"},
    {"name": "Amit", "city": "Bhopal"},
    {"name": "Sneha", "city": "Delhi"},
]
bhopal_students = list(filter(lambda s: s["city"] == "Bhopal", students))
print([s["name"] for s in bhopal_students])    # ['Rahul', 'Amit']

# Remove empty strings
data = ["Rahul", "", "Priya", "", "Amit", ""]
clean = list(filter(None, data))    # None removes falsy values
print(clean)    # ['Rahul', 'Priya', 'Amit']
```

---

## reduce() — Combine All Items into One

`reduce()` takes a function and applies it cumulatively to reduce a list to a single value.

```python
from functools import reduce

# Sum all numbers
numbers = [10, 20, 30, 40, 50]
total = reduce(lambda a, b: a + b, numbers)
print(total)    # 150

# How it works step by step:
# Step 1: a=10, b=20 → 30
# Step 2: a=30, b=30 → 60
# Step 3: a=60, b=40 → 100
# Step 4: a=100, b=50 → 150

# Find maximum
marks = [85, 92, 78, 95, 88]
maximum = reduce(lambda a, b: a if a > b else b, marks)
print(maximum)    # 95

# Concatenate strings
words = ["Python", "is", "awesome"]
sentence = reduce(lambda a, b: f"{a} {b}", words)
print(sentence)    # Python is awesome

# With initial value
numbers = [1, 2, 3, 4]
product = reduce(lambda a, b: a * b, numbers, 1)
print(product)    # 24 (1*1*2*3*4)
```

---

## Combining map, filter, reduce

```python
from functools import reduce

# Calculate total fee of enrolled students (fee > 0)
students = [
    {"name": "Rahul", "fee": 25000, "enrolled": True},
    {"name": "Priya", "fee": 20000, "enrolled": True},
    {"name": "Amit", "fee": 0, "enrolled": False},
    {"name": "Sneha", "fee": 15000, "enrolled": True},
]

total_revenue = reduce(
    lambda acc, fee: acc + fee,                               # Step 3: Sum
    map(lambda s: s["fee"],                                   # Step 2: Extract fee
        filter(lambda s: s["enrolled"], students)),           # Step 1: Only enrolled
    0
)
print(f"Total Revenue: ₹{total_revenue:,}")    # Total Revenue: ₹60,000
```

**Tip:** For readability, prefer list comprehensions for simple cases:

```python
# Same result, more readable
total = sum(s["fee"] for s in students if s["enrolled"])
```

---

## itertools — Iterator Building Blocks

The `itertools` module provides fast, memory-efficient tools for working with iterators.

### Infinite Iterators

```python
import itertools

# count — infinite counter
for i in itertools.count(start=1, step=5):
    if i > 20:
        break
    print(i, end=" ")    # 1 6 11 16

# cycle — repeat forever
colors = itertools.cycle(["red", "green", "blue"])
for _ in range(6):
    print(next(colors), end=" ")    # red green blue red green blue

# repeat — repeat a value
fives = list(itertools.repeat(5, times=4))
print(fives)    # [5, 5, 5, 5]
```

### Combinatoric Iterators

```python
# product — cartesian product (all combinations)
sizes = ["S", "M", "L"]
colors = ["Red", "Blue"]
combos = list(itertools.product(sizes, colors))
print(combos)
# [('S','Red'), ('S','Blue'), ('M','Red'), ('M','Blue'), ('L','Red'), ('L','Blue')]

# permutations — order matters
teams = ["A", "B", "C"]
matchups = list(itertools.permutations(teams, 2))
print(matchups)    # [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# combinations — order doesn't matter
pairs = list(itertools.combinations(teams, 2))
print(pairs)    # [('A','B'), ('A','C'), ('B','C')]
```

### Useful itertools Functions

```python
# chain — combine multiple iterables
batch_a = ["Rahul", "Priya"]
batch_b = ["Amit", "Sneha"]
all_students = list(itertools.chain(batch_a, batch_b))
print(all_students)    # ['Rahul', 'Priya', 'Amit', 'Sneha']

# groupby — group consecutive items
data = [("Bhopal", "Rahul"), ("Bhopal", "Amit"), ("Delhi", "Sneha"), ("Delhi", "Vikram")]
for city, group in itertools.groupby(data, key=lambda x: x[0]):
    names = [name for _, name in group]
    print(f"{city}: {names}")
# Bhopal: ['Rahul', 'Amit']
# Delhi: ['Sneha', 'Vikram']

# islice — slice an iterator (like list slicing but for any iterable)
first_5 = list(itertools.islice(range(1000000), 5))
print(first_5)    # [0, 1, 2, 3, 4]

# accumulate — running totals
monthly_fees = [25000, 20000, 15000, 30000]
running_total = list(itertools.accumulate(monthly_fees))
print(running_total)    # [25000, 45000, 60000, 90000]
```

---

## functools — Function Tools

### partial() — Pre-fill Arguments

```python
from functools import partial

def calculate_fee(base, gst_rate, discount):
    price_after_discount = base * (1 - discount)
    return round(price_after_discount * (1 + gst_rate), 2)

# Create specialized versions
calculate_with_gst = partial(calculate_fee, gst_rate=0.18, discount=0)
calculate_student = partial(calculate_fee, gst_rate=0.18, discount=0.10)

print(calculate_with_gst(25000))     # 29500.0
print(calculate_student(25000))      # 26550.0
```

### lru_cache() — Memoization

Cache results of expensive function calls:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))    # 12586269025 (instant!)
# Without cache, this would take forever
```

### total_ordering — Auto-generate Comparison Methods

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __eq__(self, other):
        return self.marks == other.marks

    def __lt__(self, other):
        return self.marks < other.marks

# Now ==, !=, <, <=, >, >= all work!
s1 = Student("Rahul", 85)
s2 = Student("Priya", 92)
print(s1 < s2)     # True
print(s1 >= s2)    # False (auto-generated!)
```

---

## Closures — Functions That Remember

A closure is a function that remembers the variables from the scope where it was created:

```python
def make_multiplier(factor):
    """Create a function that multiplies by a fixed factor."""
    def multiply(number):
        return number * factor    # 'factor' is remembered
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))     # 10
print(triple(5))     # 15
print(double(100))   # 200

# Practical: GST calculator factory
def make_gst_calculator(rate):
    def calculate(amount):
        return round(amount * (1 + rate), 2)
    return calculate

gst_18 = make_gst_calculator(0.18)
gst_12 = make_gst_calculator(0.12)

print(gst_18(1000))    # 1180.0
print(gst_12(1000))    # 1120.0
```

---

## Summary

| Concept | What It Does | Example |
|---------|-------------|---------|
| `map()` | Transform every item | `map(func, items)` |
| `filter()` | Keep matching items | `filter(func, items)` |
| `reduce()` | Combine all into one | `reduce(func, items)` |
| `itertools` | Iterator utilities | `chain`, `product`, `groupby` |
| `functools.partial` | Pre-fill arguments | `partial(func, arg=val)` |
| `lru_cache` | Cache function results | `@lru_cache` |
| Closure | Function that remembers scope | `def outer(): def inner():` |

---

## Practice Tasks

1. Use `map()` to add 18% GST to a list of prices
2. Use `filter()` to find all students from "Bhopal" in a list of dicts
3. Use `reduce()` to find the student with the highest marks
4. Use `itertools.combinations` to generate all possible student pairs for a project
5. Write a closure that creates a greeting function for a specific language
