# File I/O — Reading and Writing Files

**Module 01 — Python Core: Language Fundamentals | Topic 8**

---

## Why File I/O?

Programs often need to read data from files or save results to files. Think of all the data around you:
- Student records in CSV files
- Configuration in JSON files
- Logs in text files
- Reports in various formats

Python makes file operations simple and safe.

---

## Opening and Reading Text Files

### The open() Function

```python
file = open("students.txt", "r")    # Open for reading
content = file.read()                # Read entire content
print(content)
file.close()                         # Always close!
```

### File Modes

| Mode | Description |
|------|-------------|
| `"r"` | Read (default) — file must exist |
| `"w"` | Write — creates new or overwrites existing |
| `"a"` | Append — adds to end of file |
| `"x"` | Create — fails if file exists |
| `"r+"` | Read and write |
| `"b"` | Binary mode (add to any mode, e.g. `"rb"`) |

### Reading Methods

```python
# Read entire file as one string
content = file.read()

# Read one line
line = file.readline()

# Read all lines into a list
lines = file.readlines()
# ['Line 1\n', 'Line 2\n', 'Line 3\n']
```

### Example: Reading a Student File

Suppose `students.txt` contains:

```
Rahul,Bhopal,85
Priya,Pune,92
Amit,Delhi,78
Sneha,Bhopal,88
```

```python
file = open("students.txt", "r")
for line in file:
    name, city, marks = line.strip().split(",")
    print(f"{name} from {city} scored {marks}")
file.close()
```

---

## Context Managers — The with Statement

The `with` statement automatically closes the file when the block ends — even if an exception occurs. **Always use `with` for file operations.**

```python
# Good — file is automatically closed
with open("students.txt", "r") as file:
    content = file.read()
    print(content)
# File is closed here automatically

# Bad — you might forget to close
file = open("students.txt", "r")
content = file.read()
file.close()    # What if an error happens before this line?
```

---

## Writing to Files

### Write Mode ("w") — Overwrites!

```python
with open("output.txt", "w") as file:
    file.write("TechPath Institute\n")
    file.write("Python Full Stack Course\n")
    file.write(f"Fee: ₹25,000\n")
```

**Warning:** `"w"` mode **deletes all existing content**. The file starts empty.

### Append Mode ("a") — Adds to End

```python
with open("log.txt", "a") as file:
    file.write("2026-07-25: Student Rahul enrolled\n")
    file.write("2026-07-25: Student Priya enrolled\n")
```

### Writing Multiple Lines

```python
students = ["Rahul", "Priya", "Amit", "Sneha"]

with open("students.txt", "w") as file:
    for student in students:
        file.write(f"{student}\n")

# Or use writelines()
with open("students.txt", "w") as file:
    lines = [f"{name}\n" for name in students]
    file.writelines(lines)
```

---

## Working with CSV Files

CSV (Comma-Separated Values) is one of the most common data formats. Python has a built-in `csv` module.

### Reading CSV

```python
import csv

with open("students.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)    # Skip header row
    
    for row in reader:
        name, city, marks = row
        print(f"{name} from {city}: {marks}")
```

### Reading CSV as Dictionaries

```python
import csv

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    
    for student in reader:
        print(f"{student['name']} — {student['marks']}")
```

If `students.csv` has a header row, `DictReader` uses it as keys automatically.

### Writing CSV

```python
import csv

students = [
    {"name": "Rahul", "city": "Bhopal", "marks": 85},
    {"name": "Priya", "city": "Pune", "marks": 92},
    {"name": "Amit", "city": "Delhi", "marks": 78},
]

with open("output.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "city", "marks"])
    writer.writeheader()
    writer.writerows(students)
```

**Note:** Always use `newline=""` when opening CSV files for writing on Windows to avoid extra blank lines.

### Complete CSV Example

```python
import csv

# Read students, calculate grades, write results
def get_grade(marks):
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    if marks >= 60: return "C"
    return "F"

# Read
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    students = list(reader)

# Process
for student in students:
    student["marks"] = int(student["marks"])
    student["grade"] = get_grade(student["marks"])

# Write
with open("results.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "city", "marks", "grade"])
    writer.writeheader()
    writer.writerows(students)

print("Results saved to results.csv")
```

---

## Working with JSON Files

JSON (JavaScript Object Notation) is the standard format for APIs and configuration files. Python has a built-in `json` module.

### JSON Format

```json
{
    "institute": "TechPath",
    "courses": [
        {"name": "Python Full Stack", "fee": 25000},
        {"name": "Web Development", "fee": 20000}
    ],
    "city": "Bhopal"
}
```

### Reading JSON

```python
import json

with open("config.json", "r") as file:
    data = json.load(file)    # Parse JSON file to Python dict

print(data["institute"])      # TechPath
print(data["courses"][0])     # {'name': 'Python Full Stack', 'fee': 25000}
```

### Writing JSON

```python
import json

students = [
    {"name": "Rahul", "city": "Bhopal", "marks": 85},
    {"name": "Priya", "city": "Pune", "marks": 92},
]

with open("students.json", "w") as file:
    json.dump(students, file, indent=2, ensure_ascii=False)
```

**`indent=2`** makes the JSON file readable (pretty-printed).
**`ensure_ascii=False`** allows Unicode characters like ₹ to appear correctly.

### JSON String Conversion

```python
import json

# Dict to JSON string
data = {"name": "Rahul", "fee": 25000}
json_string = json.dumps(data, indent=2)
print(json_string)

# JSON string to dict
json_text = '{"name": "Priya", "city": "Pune"}'
data = json.loads(json_text)
print(data["name"])    # Priya
```

### JSON Methods Summary

| Method | Purpose | Input → Output |
|--------|---------|---------------|
| `json.load(file)` | Read JSON file | File → Dict |
| `json.dump(data, file)` | Write to JSON file | Dict → File |
| `json.loads(string)` | Parse JSON string | String → Dict |
| `json.dumps(data)` | Convert to JSON string | Dict → String |

**Memory trick:** The `s` in `loads`/`dumps` stands for "string".

---

## File Path Handling with pathlib

The `pathlib` module provides an object-oriented way to work with file paths. It works across Windows, Mac, and Linux.

```python
from pathlib import Path

# Create a path
data_dir = Path("data")
file_path = data_dir / "students.csv"    # Use / operator!

# Check existence
print(file_path.exists())      # True/False
print(file_path.is_file())     # True/False
print(data_dir.is_dir())       # True/False

# File info
print(file_path.name)          # students.csv
print(file_path.stem)          # students
print(file_path.suffix)        # .csv
print(file_path.parent)        # data

# Create directory
data_dir.mkdir(exist_ok=True)  # Creates if doesn't exist

# List files in directory
for f in Path(".").glob("*.py"):
    print(f.name)

# Read/write shortcuts
content = file_path.read_text(encoding="utf-8")
file_path.write_text("Hello!", encoding="utf-8")
```

---

## Handling File Errors

```python
from pathlib import Path

filepath = Path("data/students.csv")

# Check before opening
if not filepath.exists():
    print(f"File not found: {filepath}")
elif not filepath.is_file():
    print(f"Not a file: {filepath}")
else:
    with open(filepath, "r") as f:
        content = f.read()

# Or use try/except
try:
    with open("students.csv", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File does not exist!")
except PermissionError:
    print("No permission to read this file!")
except UnicodeDecodeError:
    print("File contains non-text data. Try binary mode ('rb').")
```

---

## Practical Example: Student Management System

```python
import json
from pathlib import Path

DATA_FILE = Path("students.json")

def load_students():
    """Load students from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_students(students):
    """Save students to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)

def add_student(name, city, marks):
    """Add a new student."""
    students = load_students()
    students.append({
        "name": name,
        "city": city,
        "marks": marks,
    })
    save_students(students)
    print(f"Added {name}")

def show_all():
    """Display all students."""
    students = load_students()
    if not students:
        print("No students found.")
        return
    
    print(f"\n{'Name':<15} {'City':<10} {'Marks':<6}")
    print("-" * 35)
    for s in students:
        print(f"{s['name']:<15} {s['city']:<10} {s['marks']:<6}")

# Usage
add_student("Rahul", "Bhopal", 85)
add_student("Priya", "Pune", 92)
show_all()
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| `open(path, mode)` | Open a file (r/w/a/x) |
| `with` statement | Auto-closes file — always use this |
| `.read()` / `.readline()` / `.readlines()` | Read file content |
| `.write()` / `.writelines()` | Write to file |
| `csv` module | Read/write CSV files |
| `json` module | Read/write JSON files |
| `pathlib.Path` | Cross-platform file paths |
| `load`/`dump` | JSON file operations |
| `loads`/`dumps` | JSON string operations |

---

## Practice Tasks

1. Read a text file and count the number of lines, words, and characters
2. Create a CSV file with 5 student records, then read and display them in a formatted table
3. Create a JSON config file for a TechPath application (institute name, courses, fee, city)
4. Write a program that appends log entries to a file with timestamps
5. Build a contact book that saves/loads contacts from a JSON file
