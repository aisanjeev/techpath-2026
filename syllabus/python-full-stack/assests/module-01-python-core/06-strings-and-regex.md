# Strings & Regular Expressions

**Module 01 — Python Core: Language Fundamentals | Topic 6**

---

## Strings in Python

A string is a sequence of characters enclosed in quotes. Strings are **immutable** — once created, they cannot be changed (any "modification" creates a new string).

```python
name = "Rahul Sharma"
city = 'Bhopal'
bio = """Rahul is a Python developer
from Bhopal, MP."""
```

---

## String Indexing & Slicing

Strings work like lists — each character has an index.

```python
name = "TechPath"
#       T e c h P a t h
#       0 1 2 3 4 5 6 7
#      -8-7-6-5-4-3-2-1

print(name[0])       # T
print(name[4])       # P
print(name[-1])      # h
print(name[-4])      # P
```

### Slicing

```python
name = "TechPath Institute"

print(name[0:4])      # Tech
print(name[4:8])      # Path
print(name[:8])       # TechPath
print(name[9:])       # Institute
print(name[::2])      # TcPt nttt
print(name[::-1])     # etutitsnI htaPcheT (reversed)
```

---

## Essential String Methods

### Case Methods

```python
text = "techPath Institute"

print(text.upper())        # TECHPATH INSTITUTE
print(text.lower())        # techpath institute
print(text.title())        # Techpath Institute
print(text.capitalize())   # Techpath institute
print(text.swapcase())     # TECHpATH iNSTITUTE
```

### Search Methods

```python
text = "Learn Python at TechPath Institute, Bhopal"

print(text.find("Python"))        # 6 (index where found)
print(text.find("Java"))          # -1 (not found)
print(text.index("Python"))       # 6 (same as find)
# text.index("Java")              # ValueError! (use find for safety)

print(text.count("a"))            # 3
print(text.startswith("Learn"))   # True
print(text.endswith("Bhopal"))    # True
print("Python" in text)           # True
```

### Trim & Pad Methods

```python
name = "   Rahul   "

print(name.strip())       # "Rahul" (remove both sides)
print(name.lstrip())      # "Rahul   " (remove left)
print(name.rstrip())      # "   Rahul" (remove right)

# Padding
print("42".zfill(5))          # 00042
print("Rahul".ljust(15))      # "Rahul          "
print("Rahul".rjust(15))      # "          Rahul"
print("Rahul".center(15))     # "     Rahul     "
print("Rahul".center(15, "-"))  # "-----Rahul-----"
```

### Replace & Split

```python
text = "Python is great. Python is fun."

# Replace
print(text.replace("Python", "Coding"))
# "Coding is great. Coding is fun."

print(text.replace("Python", "Coding", 1))    # Replace only first
# "Coding is great. Python is fun."

# Split — break string into list
csv_data = "Rahul,Bhopal,85,Python"
parts = csv_data.split(",")
print(parts)    # ['Rahul', 'Bhopal', '85', 'Python']

# Split lines
multiline = "Line 1\nLine 2\nLine 3"
lines = multiline.splitlines()
print(lines)    # ['Line 1', 'Line 2', 'Line 3']

# Join — combine list into string
students = ["Rahul", "Priya", "Amit"]
print(", ".join(students))    # Rahul, Priya, Amit
print(" | ".join(students))   # Rahul | Priya | Amit
```

### Validation Methods

```python
print("hello".isalpha())      # True (only letters)
print("12345".isdigit())      # True (only digits)
print("hello123".isalnum())   # True (letters + digits)
print("   ".isspace())        # True (only whitespace)
print("hello".islower())      # True
print("HELLO".isupper())      # True
print("Hello World".istitle()) # True
```

---

## String Methods Quick Reference

| Method | Purpose | Example |
|--------|---------|---------|
| `upper()` | All uppercase | `"hi".upper()` → `"HI"` |
| `lower()` | All lowercase | `"HI".lower()` → `"hi"` |
| `strip()` | Remove whitespace | `" hi ".strip()` → `"hi"` |
| `split(sep)` | Break into list | `"a,b".split(",")` → `["a","b"]` |
| `join(list)` | Combine list | `",".join(["a","b"])` → `"a,b"` |
| `replace(old, new)` | Replace text | `"hi".replace("h","H")` → `"Hi"` |
| `find(sub)` | Find index | `"hello".find("ll")` → `2` |
| `count(sub)` | Count occurrences | `"hello".count("l")` → `2` |
| `startswith(s)` | Check prefix | `"hello".startswith("he")` → `True` |
| `endswith(s)` | Check suffix | `"hello".endswith("lo")` → `True` |
| `zfill(n)` | Pad with zeros | `"42".zfill(5)` → `"00042"` |

---

## Regular Expressions (regex)

Regular expressions are patterns used to search, match, and manipulate text. Python provides the `re` module for regex.

**Real-world analogy:** Regex is like a search template. Instead of searching for the exact word "Rahul", you can search for "any word that starts with R and has 5 letters".

### Importing re

```python
import re
```

### Basic Pattern Matching

```python
import re

text = "Contact us at support@techpath.com or call 9876543210"

# Find an email
match = re.search(r"[\w.]+@[\w.]+", text)
if match:
    print(match.group())    # support@techpath.com

# Find a phone number
match = re.search(r"\d{10}", text)
if match:
    print(match.group())    # 9876543210
```

### Common Regex Patterns

| Pattern | Meaning | Example |
|---------|---------|---------|
| `.` | Any character (except newline) | `a.c` matches "abc", "a1c" |
| `\d` | Any digit (0-9) | `\d{3}` matches "123" |
| `\D` | Any non-digit | `\D+` matches "abc" |
| `\w` | Word character (letter, digit, `_`) | `\w+` matches "hello_42" |
| `\W` | Non-word character | `\W` matches "@", " " |
| `\s` | Whitespace (space, tab, newline) | `\s+` matches "   " |
| `\S` | Non-whitespace | `\S+` matches "hello" |
| `^` | Start of string | `^Hello` matches "Hello world" |
| `$` | End of string | `world$` matches "Hello world" |

### Quantifiers

| Quantifier | Meaning | Example |
|------------|---------|---------|
| `*` | 0 or more | `ab*c` matches "ac", "abc", "abbc" |
| `+` | 1 or more | `ab+c` matches "abc", "abbc" (not "ac") |
| `?` | 0 or 1 | `colou?r` matches "color", "colour" |
| `{n}` | Exactly n | `\d{4}` matches "2026" |
| `{n,m}` | Between n and m | `\d{2,4}` matches "42", "123", "2026" |

### Character Classes

```python
# [abc] — matches a, b, or c
# [a-z] — matches any lowercase letter
# [A-Z] — matches any uppercase letter
# [0-9] — matches any digit
# [^abc] — matches anything EXCEPT a, b, c

import re

text = "Rahul's PIN is 462011 and phone is +91-9876543210"

# Find all numbers
numbers = re.findall(r"\d+", text)
print(numbers)    # ['462011', '91', '9876543210']

# Find Indian phone number
phone = re.search(r"\+91-\d{10}", text)
print(phone.group())    # +91-9876543210
```

### re Module Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `re.search(pattern, text)` | Find first match | Returns match object or None |
| `re.match(pattern, text)` | Match at start only | Like search but only at beginning |
| `re.findall(pattern, text)` | Find all matches | Returns list of strings |
| `re.finditer(pattern, text)` | Find all (as iterator) | Returns match objects |
| `re.sub(pattern, repl, text)` | Replace matches | Returns new string |
| `re.split(pattern, text)` | Split by pattern | Returns list |
| `re.compile(pattern)` | Pre-compile pattern | For reuse |

### Practical Examples

```python
import re

# 1. Validate Indian phone number
def is_valid_phone(phone):
    pattern = r"^(\+91|0)?[6-9]\d{9}$"
    return bool(re.match(pattern, phone))

print(is_valid_phone("9876543210"))     # True
print(is_valid_phone("+919876543210"))  # True
print(is_valid_phone("1234567890"))     # False (doesn't start with 6-9)

# 2. Validate email
def is_valid_email(email):
    pattern = r"^[\w.+-]+@[\w-]+\.[\w.]+$"
    return bool(re.match(pattern, email))

print(is_valid_email("rahul@techpath.com"))    # True
print(is_valid_email("not-an-email"))           # False

# 3. Extract all emails from text
text = """
Contact Rahul at rahul@techpath.com
or Priya at priya.patel@gmail.com
"""
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(emails)    # ['rahul@techpath.com', 'priya.patel@gmail.com']

# 4. Clean up text
messy = "Hello!!!   How   are   you???"
clean = re.sub(r"\s+", " ", messy)       # Multiple spaces to one
clean = re.sub(r"[!?]+", "", clean)      # Remove ! and ?
print(clean)    # "Hello How are you"

# 5. Extract data from formatted text
log = "2026-07-25 14:30:00 ERROR: Database connection failed"
match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+): (.+)", log)
if match:
    date, time, level, message = match.groups()
    print(f"Date: {date}, Level: {level}, Message: {message}")
```

### Groups — Capture Parts of a Match

```python
import re

text = "Rahul Sharma, Age: 22, City: Bhopal"

# Named groups
pattern = r"(?P<name>\w+ \w+), Age: (?P<age>\d+), City: (?P<city>\w+)"
match = re.search(pattern, text)

if match:
    print(match.group("name"))    # Rahul Sharma
    print(match.group("age"))     # 22
    print(match.group("city"))    # Bhopal
    print(match.groupdict())      # {'name': 'Rahul Sharma', 'age': '22', 'city': 'Bhopal'}
```

---

## String Formatting Comparison

| Method | Syntax | Best For |
|--------|--------|----------|
| f-strings | `f"Hello {name}"` | Modern code (Python 3.6+) |
| `.format()` | `"Hello {}".format(name)` | Older code, templates |
| `%` formatting | `"Hello %s" % name` | Very old code (avoid) |

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Strings are immutable | Methods return NEW strings |
| Indexing | `s[0]` first, `s[-1]` last |
| Slicing | `s[start:stop:step]` |
| `split()` / `join()` | Convert between string and list |
| `strip()` | Remove whitespace |
| `find()` / `replace()` | Search and replace |
| `re.search()` | Find first regex match |
| `re.findall()` | Find all regex matches |
| `re.sub()` | Replace with regex |
| `r"..."` | Raw string — no escape processing |

---

## Practice Tasks

1. Take a full name as input and print it in UPPERCASE, lowercase, and Title Case
2. Count how many vowels are in a string entered by the user
3. Write a regex to validate an Indian PIN code (6 digits, starts with 1-9)
4. Extract all phone numbers from a paragraph using `re.findall()`
5. Write a function that censors email addresses in text (replace with `***@***.com`)
