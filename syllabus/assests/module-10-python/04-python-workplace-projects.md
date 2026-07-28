# Python — Workplace Projects & Interview Problems

**Module 10 — Python Programming | Job-Ready Practice**

---

## Why This Matters

> Every Python interview has two parts: "Explain this concept" and "Solve this problem." Theory alone won't pass the second part. These projects and problems are what companies actually ask freshers.

---

## Project 1: Student Management System (CLI)

A complete CRUD application that runs in the terminal — the kind of project that proves you understand real programming.

```python
import json
import os
from datetime import datetime

DATA_FILE = "students.json"

def load_students():
    """Load students from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    """Save students to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

def generate_id(students):
    """Generate next student ID"""
    if not students:
        return "STU001"
    last_id = max(int(s["id"][3:]) for s in students)
    return f"STU{last_id + 1:03d}"

def add_student(students):
    """Add a new student"""
    print("\n--- Add New Student ---")
    name = input("Name: ").strip()
    if not name:
        print("Error: Name cannot be empty")
        return

    age = input("Age: ").strip()
    try:
        age = int(age)
        if age < 15 or age > 60:
            print("Error: Age must be between 15 and 60")
            return
    except ValueError:
        print("Error: Age must be a number")
        return

    course = input("Course (ADCA/DCA/Tally): ").strip().upper()
    if course not in ("ADCA", "DCA", "TALLY"):
        print("Error: Invalid course")
        return

    phone = input("Phone (10 digits): ").strip()
    if not phone.isdigit() or len(phone) != 10:
        print("Error: Phone must be 10 digits")
        return

    student = {
        "id": generate_id(students),
        "name": name,
        "age": age,
        "course": course,
        "phone": phone,
        "enrolled_on": datetime.now().strftime("%Y-%m-%d"),
        "status": "Active"
    }

    students.append(student)
    save_students(students)
    print(f"\nStudent {student['id']} — {name} added successfully!")

def view_all(students):
    """Display all students in a formatted table"""
    if not students:
        print("\nNo students found.")
        return

    print(f"\n{'ID':<8} {'Name':<20} {'Age':<5} {'Course':<8} {'Phone':<12} {'Status':<8}")
    print("-" * 65)
    for s in students:
        print(f"{s['id']:<8} {s['name']:<20} {s['age']:<5} {s['course']:<8} {s['phone']:<12} {s['status']:<8}")
    print(f"\nTotal students: {len(students)}")

def search_student(students):
    """Search by name or ID"""
    query = input("\nSearch (name or ID): ").strip().lower()
    results = [s for s in students
               if query in s["name"].lower() or query in s["id"].lower()]

    if results:
        view_all(results)
    else:
        print("No matching students found.")

def update_student(students):
    """Update student details"""
    student_id = input("\nEnter student ID to update: ").strip().upper()
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        print("Student not found.")
        return

    print(f"\nUpdating: {student['name']} ({student['id']})")
    print("Press Enter to keep current value.\n")

    name = input(f"Name [{student['name']}]: ").strip()
    phone = input(f"Phone [{student['phone']}]: ").strip()
    status = input(f"Status [{student['status']}] (Active/Inactive): ").strip()

    if name:
        student["name"] = name
    if phone and phone.isdigit() and len(phone) == 10:
        student["phone"] = phone
    if status in ("Active", "Inactive"):
        student["status"] = status

    save_students(students)
    print("Student updated successfully!")

def delete_student(students):
    """Delete a student with confirmation"""
    student_id = input("\nEnter student ID to delete: ").strip().upper()
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        print("Student not found.")
        return

    confirm = input(f"Delete {student['name']} ({student['id']})? (yes/no): ").strip().lower()
    if confirm == "yes":
        students.remove(student)
        save_students(students)
        print("Student deleted.")
    else:
        print("Cancelled.")

def course_report(students):
    """Show student count by course"""
    if not students:
        print("\nNo data.")
        return

    courses = {}
    for s in students:
        courses[s["course"]] = courses.get(s["course"], 0) + 1

    print("\n--- Course Report ---")
    for course, count in sorted(courses.items()):
        bar = "█" * count
        print(f"{course:<8} {count:>3} {bar}")
    print(f"\nTotal: {len(students)}")

def main():
    print("=" * 40)
    print("   STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)

    students = load_students()

    while True:
        print("\n1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Course Report")
        print("7. Exit")

        choice = input("\nChoice (1-7): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            course_report(students)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try 1-7.")

main()
```

### What This Teaches

| Concept | Where in Code |
|---------|--------------|
| File I/O (JSON) | load_students, save_students |
| Functions | Every operation is a function |
| Input validation | Age check, phone check, empty check |
| List comprehension | Search filtering |
| String formatting | Table display with f-strings |
| Dictionary operations | Student data, course counting |
| Error handling | try/except for age parsing |
| Data persistence | JSON file storage |

---

## Project 2: File Organizer Script

A Python script that sorts messy Downloads folder into organized subfolders.

```python
import os
import shutil
from pathlib import Path

# Define file categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql", ".java", ".cpp"],
    "Installers": [".exe", ".msi", ".dmg", ".deb", ".apk"],
}

def organize_folder(folder_path):
    """Organize files in a folder by type"""
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        return

    moved_count = 0
    skipped_count = 0

    for file in folder.iterdir():
        # Skip directories
        if file.is_dir():
            continue

        # Find matching category
        extension = file.suffix.lower()
        category = "Others"

        for cat_name, extensions in FILE_TYPES.items():
            if extension in extensions:
                category = cat_name
                break

        # Create category folder
        target_folder = folder / category
        target_folder.mkdir(exist_ok=True)

        # Handle duplicate filenames
        target_path = target_folder / file.name
        if target_path.exists():
            base = file.stem
            counter = 1
            while target_path.exists():
                target_path = target_folder / f"{base}_{counter}{file.suffix}"
                counter += 1

        # Move file
        shutil.move(str(file), str(target_path))
        print(f"  {file.name} → {category}/")
        moved_count += 1

    print(f"\nDone! Moved {moved_count} files, skipped {skipped_count}.")

# Run it
downloads = str(Path.home() / "Downloads")
print(f"Organizing: {downloads}\n")
organize_folder(downloads)
```

> This is a script you'll actually use in your own life, and it demonstrates Python automation skills that employers value.

---

## Top 20 Interview Coding Problems

### Easy Level (Must Solve)

**1. Reverse a string**
```python
def reverse_string(s):
    return s[::-1]

# "hello" → "olleh"
```

**2. Check if palindrome**
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

# "racecar" → True, "hello" → False
```

**3. Find the largest number in a list**
```python
def find_largest(numbers):
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num
    return largest

# Don't just use max() — interviewers want to see your logic
```

**4. Count vowels in a string**
```python
def count_vowels(s):
    return sum(1 for char in s.lower() if char in "aeiou")

# "Hello World" → 3
```

**5. FizzBuzz (asked in 80% of interviews)**
```python
for i in range(1, 101):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

**6. Check if a number is prime**
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

**7. Remove duplicates from a list (keep order)**
```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# [1, 3, 2, 3, 1, 4] → [1, 3, 2, 4]
```

### Medium Level (Practice These)

**8. Find second largest number**
```python
def second_largest(numbers):
    unique = list(set(numbers))
    unique.sort()
    return unique[-2] if len(unique) >= 2 else None

# [5, 2, 8, 1, 8, 3] → 5
```

**9. Count word frequency in a sentence**
```python
def word_frequency(sentence):
    words = sentence.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# "the cat and the dog" → {"the": 2, "cat": 1, "and": 1, "dog": 1}
```

**10. Fibonacci sequence**
```python
def fibonacci(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

# fibonacci(8) → [0, 1, 1, 2, 3, 5, 8, 13]
```

**11. Find common elements in two lists**
```python
def common_elements(list1, list2):
    return list(set(list1) & set(list2))

# [1,2,3,4], [3,4,5,6] → [3, 4]
```

**12. Sort a dictionary by value**
```python
scores = {"Rahul": 85, "Priya": 92, "Amit": 78}
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
# {"Priya": 92, "Rahul": 85, "Amit": 78}
```

**13. Matrix transpose**
```python
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

# [[1,2,3], [4,5,6]] → [[1,4], [2,5], [3,6]]
```

### Hard Level (Impress Interviewers)

**14. Find all pairs that sum to a target**
```python
def find_pairs(numbers, target):
    seen = set()
    pairs = []
    for num in numbers:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs

# find_pairs([1,2,3,4,5], 6) → [(2,4), (1,5)]
```

**15. Check if two strings are anagrams**
```python
def are_anagrams(s1, s2):
    return sorted(s1.lower().replace(" ", "")) == sorted(s2.lower().replace(" ", ""))

# "listen", "silent" → True
```

---

## Common Python Interview Questions (Theory)

| Question | Answer |
|----------|--------|
| List vs Tuple | List is mutable (can change), tuple is immutable (fixed) |
| What are *args and **kwargs? | *args = variable positional args, **kwargs = variable keyword args |
| What is a decorator? | A function that wraps another function to add behavior |
| Deep copy vs shallow copy | Shallow copies references, deep copies actual objects |
| What is a generator? | Yields values one at a time (memory efficient for large data) |
| What is `__init__`? | Constructor — runs when you create an object |
| What is `self`? | Reference to the current object instance |
| GIL in Python? | Global Interpreter Lock — only one thread runs Python at a time |
| How is memory managed? | Reference counting + garbage collector |
| Mutable vs immutable types | Mutable: list, dict, set. Immutable: int, str, tuple, frozenset |

---

## Practice Plan

### Week 1: Basics
- Solve problems 1-7 above
- Build the Student Management System

### Week 2: Intermediate
- Solve problems 8-13
- Build the File Organizer
- Practice on HackerRank (Easy section)

### Week 3: Advanced
- Solve problems 14-15
- Study theory questions
- Mock interview practice with a friend
