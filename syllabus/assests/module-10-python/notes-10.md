# Module 10 — Python Programming — Quick Revision Notes

---

## Python Basics
- Python is **interpreted** (runs line by line, no compiling)
- Indentation matters (4 spaces = one block)
- File extension: `.py` | Run: `python filename.py`

## Variables & Data Types
```python
name = "Rahul"         # str
age = 22               # int
price = 99.5           # float
is_student = True      # bool
skills = ["Python", "HTML"]  # list
student = {"name": "Rahul", "age": 22}  # dict
coordinates = (28.6, 77.2)  # tuple (immutable)
unique_tags = {"python", "web"}  # set (unique values)
```

| Type | Mutable? | Ordered? | Example |
|------|----------|----------|---------|
| `str` | No | Yes | `"hello"` |
| `int/float` | No | — | `42`, `3.14` |
| `list` | Yes | Yes | `[1, 2, 3]` |
| `tuple` | No | Yes | `(1, 2, 3)` |
| `dict` | Yes | Yes | `{"a": 1}` |
| `set` | Yes | No | `{1, 2, 3}` |

## String Operations
```python
name = "Rahul Sharma"
name.upper()          # "RAHUL SHARMA"
name.lower()          # "rahul sharma"
name.split()          # ["Rahul", "Sharma"]
name.replace("Rahul", "Amit")
name.startswith("R")  # True
len(name)             # 12
f"Hello {name}"       # f-string (formatted)
```

## Input/Output
```python
name = input("Enter name: ")  # always returns str
age = int(input("Enter age: "))  # convert to int
print(f"Hello {name}, you are {age}")
```

## Conditionals
```python
if marks >= 90:
    grade = "A+"
elif marks >= 60:
    grade = "B"
else:
    grade = "F"
```

## Loops
```python
# for loop
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for item in my_list:      # iterate list
    print(item)

for key, value in my_dict.items():  # iterate dict
    print(f"{key}: {value}")

# while loop
while count > 0:
    count -= 1

# List comprehension
squares = [x**2 for x in range(10)]
even = [x for x in numbers if x % 2 == 0]
```

## Functions
```python
def calculate_grade(marks):
    """Return grade based on marks."""
    if marks >= 90:
        return "A+"
    elif marks >= 60:
        return "B"
    return "F"

# Default parameter
def greet(name="Guest"):
    return f"Hello {name}"

# Multiple return values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

low, high, avg = get_stats([10, 20, 30])
```

## Lists
```python
fruits = ["apple", "banana", "mango"]
fruits.append("grape")       # add
fruits.insert(0, "kiwi")     # insert at index
fruits.remove("banana")      # remove by value
fruits.pop()                 # remove last
fruits.sort()                # sort in-place
fruits.reverse()             # reverse in-place
len(fruits)                  # count
"apple" in fruits            # True
fruits[0]                    # first item
fruits[-1]                   # last item
fruits[1:3]                  # slice
```

## Dictionaries
```python
student = {"name": "Rahul", "age": 22, "course": "ADCA"}
student["name"]              # "Rahul"
student.get("email", "N/A")  # safe access
student["city"] = "Bhopal"   # add/update
del student["age"]           # delete
student.keys()               # all keys
student.values()             # all values
student.items()              # key-value pairs
```

## File Handling
```python
# Write
with open("data.txt", "w") as f:
    f.write("Hello World\n")

# Read
with open("data.txt", "r") as f:
    content = f.read()

# Append
with open("data.txt", "a") as f:
    f.write("New line\n")

# Read lines
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```

## Error Handling
```python
try:
    num = int(input("Enter number: "))
    result = 100 / num
except ValueError:
    print("Not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Done")
```

## Useful Built-in Functions
| Function | Purpose | Example |
|----------|---------|---------|
| `len()` | Length | `len([1,2,3])` → 3 |
| `type()` | Data type | `type(42)` → int |
| `range()` | Number sequence | `range(1, 11)` |
| `enumerate()` | Index + value | `for i, v in enumerate(lst)` |
| `zip()` | Pair two lists | `zip(names, marks)` |
| `sorted()` | Sort (new list) | `sorted(lst, reverse=True)` |
| `map()` | Apply function | `list(map(int, ["1","2"]))` |
| `filter()` | Filter items | `list(filter(lambda x: x>0, lst))` |
| `round()` | Round number | `round(3.14159, 2)` → 3.14 |
