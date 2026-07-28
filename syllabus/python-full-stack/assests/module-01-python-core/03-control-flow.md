# Control Flow

**Module 01 — Python Core: Language Fundamentals | Topic 3**

---

## What is Control Flow?

By default, Python runs code line by line from top to bottom. Control flow lets you change this — you can skip lines, repeat lines, or choose between different paths.

**Three types of control flow:**
1. **Conditional** — Do something only if a condition is true (`if/elif/else`)
2. **Loops** — Repeat something multiple times (`for`, `while`)
3. **Flow modifiers** — Change loop behavior (`break`, `continue`, `pass`)

---

## if / elif / else — Making Decisions

### Basic if Statement

```python
marks = 85

if marks >= 60:
    print("Pass!")    # This runs because 85 >= 60
```

**Indentation matters!** Python uses indentation (4 spaces) to define code blocks — not curly braces like other languages.

### if-else

```python
marks = 45

if marks >= 60:
    print("Pass!")
else:
    print("Fail — please try again")    # This runs
```

### if-elif-else (Multiple Conditions)

```python
marks = 78

if marks >= 90:
    grade = "A+"
elif marks >= 80:
    grade = "A"
elif marks >= 70:
    grade = "B"
elif marks >= 60:
    grade = "C"
elif marks >= 50:
    grade = "D"
else:
    grade = "F"

print(f"Marks: {marks}, Grade: {grade}")    # Marks: 78, Grade: B
```

**How it works:** Python checks conditions from top to bottom. The moment one is `True`, it runs that block and skips the rest.

### Nested if Statements

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("You can vote!")
    else:
        print("Bring your ID card")
else:
    print("You are too young to vote")
```

### Ternary Operator (One-Line if-else)

```python
age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)    # Adult

# Useful in f-strings
marks = 75
print(f"Result: {'Pass' if marks >= 60 else 'Fail'}")
```

### Real-World Example: Fee Calculator

```python
course = "Python Full Stack"
is_student = True
base_fee = 25000

# Apply discount
if is_student:
    discount = 0.10    # 10% student discount
elif course == "Python Full Stack":
    discount = 0.05    # 5% course discount
else:
    discount = 0

fee_after_discount = base_fee * (1 - discount)
gst = fee_after_discount * 0.18
total = fee_after_discount + gst

print(f"Base Fee: ₹{base_fee}")
print(f"Discount: {discount * 100}%")
print(f"After Discount: ₹{fee_after_discount}")
print(f"GST (18%): ₹{gst:.2f}")
print(f"Total: ₹{total:.2f}")
```

---

## for Loop — Repeating a Known Number of Times

Use `for` when you know how many times to repeat (or you are going through a collection).

### Looping Over a List

```python
students = ["Rahul", "Priya", "Amit", "Sneha"]

for student in students:
    print(f"Hello, {student}!")

# Output:
# Hello, Rahul!
# Hello, Priya!
# Hello, Amit!
# Hello, Sneha!
```

### range() — Generate Numbers

```python
# range(stop) — 0 to stop-1
for i in range(5):
    print(i)    # 0, 1, 2, 3, 4

# range(start, stop) — start to stop-1
for i in range(1, 6):
    print(i)    # 1, 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 20, 5):
    print(i)    # 0, 5, 10, 15

# Counting backwards
for i in range(5, 0, -1):
    print(i)    # 5, 4, 3, 2, 1
```

### Looping Over Strings

```python
city = "Bhopal"
for char in city:
    print(char, end=" ")    # B h o p a l
```

### enumerate() — Get Index + Value

```python
students = ["Rahul", "Priya", "Amit"]

for index, name in enumerate(students):
    print(f"{index + 1}. {name}")

# Output:
# 1. Rahul
# 2. Priya
# 3. Amit
```

### Looping Over Dictionaries

```python
student = {"name": "Rahul", "city": "Bhopal", "marks": 85}

# Keys only
for key in student:
    print(key)

# Keys and values
for key, value in student.items():
    print(f"{key}: {value}")

# Output:
# name: Rahul
# city: Bhopal
# marks: 85
```

### Nested Loops

```python
# Multiplication table
for i in range(1, 6):
    for j in range(1, 11):
        print(f"{i} x {j} = {i * j:2d}", end="   ")
    print()    # New line after each row
```

---

## while Loop — Repeating Until a Condition Changes

Use `while` when you don't know how many times to repeat — you keep going until a condition becomes `False`.

```python
count = 1

while count <= 5:
    print(f"Attempt {count}")
    count += 1    # Don't forget this! Otherwise infinite loop

print("Done!")
```

### Real-World Example: Login System

```python
correct_password = "techpath123"
attempts = 3

while attempts > 0:
    password = input("Enter password: ")
    
    if password == correct_password:
        print("Login successful! Welcome to TechPath.")
        break
    else:
        attempts -= 1
        print(f"Wrong password. {attempts} attempts left.")

if attempts == 0:
    print("Account locked. Contact support.")
```

### while with else

The `else` block runs when the while loop finishes normally (without `break`):

```python
count = 1
while count <= 3:
    print(count)
    count += 1
else:
    print("Loop completed normally")    # This runs
```

---

## break, continue, pass

### break — Exit the Loop Immediately

```python
# Find the first student with marks > 90
students = [
    {"name": "Rahul", "marks": 78},
    {"name": "Priya", "marks": 92},
    {"name": "Amit", "marks": 85},
]

for student in students:
    if student["marks"] > 90:
        print(f"Topper found: {student['name']}")
        break    # Stop searching
```

### continue — Skip to Next Iteration

```python
# Print only even numbers
for i in range(1, 11):
    if i % 2 != 0:
        continue    # Skip odd numbers
    print(i)    # 2, 4, 6, 8, 10
```

### pass — Do Nothing (Placeholder)

```python
# Placeholder for code you'll write later
for student in students:
    if student["marks"] < 60:
        pass    # TODO: send warning email
    else:
        print(f"{student['name']} passed")
```

`pass` is also used in empty functions and classes:

```python
def calculate_gpa():
    pass    # Will implement later

class Student:
    pass    # Will add attributes later
```

---

## Comprehensions — One-Line Loops

Comprehensions let you create lists, sets, and dicts in a single line. They are shorter and faster than regular loops.

### List Comprehension

```python
# Regular loop
squares = []
for i in range(1, 6):
    squares.append(i ** 2)

# List comprehension (same result, one line)
squares = [i ** 2 for i in range(1, 6)]
print(squares)    # [1, 4, 9, 16, 25]
```

### With Condition (Filtering)

```python
marks = [85, 42, 91, 58, 73, 36, 88]

# Only passing marks (>= 60)
passing = [m for m in marks if m >= 60]
print(passing)    # [85, 91, 73, 88]

# Transform + filter
grades = [f"{m} (Pass)" if m >= 60 else f"{m} (Fail)" for m in marks]
```

### Dictionary Comprehension

```python
students = ["Rahul", "Priya", "Amit"]
marks = [85, 92, 78]

# Create dict from two lists
result = {name: mark for name, mark in zip(students, marks)}
print(result)    # {'Rahul': 85, 'Priya': 92, 'Amit': 78}
```

### Set Comprehension

```python
# Unique first letters
cities = ["Bhopal", "Bangalore", "Delhi", "Bhopal", "Delhi"]
first_letters = {city[0] for city in cities}
print(first_letters)    # {'B', 'D'}
```

### When to Use Comprehensions

| Use Comprehension When... | Use Regular Loop When... |
|---------------------------|--------------------------|
| Creating a new list/dict/set | Complex logic (multiple ifs, try/except) |
| Simple transform or filter | Side effects (printing, API calls) |
| One-line readability | More than 2 conditions |

---

## Pattern: for-else

The `else` block after a `for` loop runs only if the loop completed without hitting `break`:

```python
# Check if a student is in the list
search = "Sneha"
students = ["Rahul", "Priya", "Amit"]

for student in students:
    if student == search:
        print(f"Found {search}!")
        break
else:
    print(f"{search} not found in the list")    # This runs
```

---

## Summary

| Concept | Syntax | Use When |
|---------|--------|----------|
| `if/elif/else` | `if condition:` | Choose between paths |
| `for` | `for item in collection:` | Known number of iterations |
| `while` | `while condition:` | Unknown number of iterations |
| `break` | `break` | Exit loop early |
| `continue` | `continue` | Skip current iteration |
| `pass` | `pass` | Placeholder (do nothing) |
| List comprehension | `[expr for x in list]` | Create new list in one line |

---

## Practice Tasks

1. Write a grade calculator: input marks, print grade (A+/A/B/C/D/F)
2. Print the multiplication table of a number entered by the user
3. Write a number guessing game using a `while` loop
4. Use a list comprehension to extract all even numbers from 1 to 50
5. Loop through a list of 5 student names and print them with serial numbers using `enumerate()`
