# Cheat Sheet: Python Programming

**Module 10 — Quick Reference**

---

## Basics

```python
print("Hello")              # Output
name = input("Name: ")      # Input (always string)
age = int(input("Age: "))   # Convert to int
```

---

## Data Types

| Type | Example |
|------|---------|
| str | `"Hello"` |
| int | `42` |
| float | `3.14` |
| bool | `True` / `False` |
| list | `[1, 2, 3]` |
| tuple | `(1, 2, 3)` |
| dict | `{"key": "val"}` |
| set | `{1, 2, 3}` |

---

## String Methods

| Method | What |
|--------|------|
| `.upper()` / `.lower()` | Case change |
| `.strip()` | Remove whitespace |
| `.split(",")` | Split to list |
| `",".join(list)` | List to string |
| `.replace(old, new)` | Replace text |
| `.find(sub)` | Find position |
| `f"Hello {var}"` | f-string |

---

## List Methods

| Method | What |
|--------|------|
| `.append(x)` | Add to end |
| `.pop()` | Remove last |
| `.sort()` | Sort in place |
| `.reverse()` | Reverse |
| `.index(x)` | Find position |
| `len(list)` | Length |

---

## Dictionary

```python
d = {"name": "R", "age": 20}
d["name"]                # Access
d["email"] = "r@e.com"   # Add
d.get("x", "default")    # Safe access
d.keys() / d.values()    # Keys / Values
for k, v in d.items():   # Loop
```

---

## Control Flow

```python
# If/elif/else
if x > 0:
    print("Positive")
elif x == 0:
    print("Zero")
else:
    print("Negative")

# For loop
for i in range(5):       # 0,1,2,3,4
for item in list:        # each item

# While loop
while condition:
    # code
```

---

## Functions

```python
def greet(name, msg="Hello"):
    return f"{msg}, {name}!"

# Lambda
square = lambda x: x ** 2
```

---

## List Comprehension

```python
squares = [x**2 for x in range(5)]
evens = [x for x in nums if x % 2 == 0]
```

---

## File Handling

```python
with open("file.txt", "r") as f:
    content = f.read()

with open("file.txt", "w") as f:
    f.write("Hello")
```

---

## Error Handling

```python
try:
    risky_code()
except ValueError:
    print("Bad value")
except Exception as e:
    print(f"Error: {e}")
```

---

## Common Modules

| Module | Use |
|--------|-----|
| `math` | sqrt, pi, ceil, floor |
| `random` | randint, choice, shuffle |
| `datetime` | date, time, timedelta |
| `os` | File/folder operations |
| `json` | Read/write JSON |
| `csv` | Read/write CSV |
