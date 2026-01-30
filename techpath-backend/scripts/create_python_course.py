#!/usr/bin/env python3
"""
Create the Python Programming course via TechPath Courses API.

Uses admin login (or ADMIN_TOKEN) and POSTs the full course payload including
markdown description with code blocks. Run from backend root or set env.

Usage:
  Set env (or .env.local in backend root): BACKEND_API_BASE, ADMIN_EMAIL, ADMIN_PASSWORD.
  Or: ADMIN_TOKEN (Bearer token from admin login).

  cd techpath-backend && python scripts/create_python_course.py

Requires: requests (pip install requests)
"""

import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' is required. Run: pip install requests")
    sys.exit(1)

# Optional: load .env.local from backend root
_script_dir = os.path.dirname(os.path.abspath(__file__))
_backend_root = os.path.dirname(_script_dir)
_env_path = os.path.join(_backend_root, ".env.local")
if os.path.isfile(_env_path):
    try:
        with open(_env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and os.environ.get(k) is None:
                        os.environ[k] = v
    except Exception:
        pass

BACKEND_API_BASE ="http://localhost:8000/api/v1".rstrip("/")
ADMIN_EMAIL ="admin@techpath.biz"
ADMIN_PASSWORD ="TechPath2025!"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")

# Good-looking markdown description (with code blocks)
COURSE_DESCRIPTION = r"""Master **Python** from zero to building real scripts in 3 months. This offline, instructor-led course covers syntax, data structures, OOP, file handling, and hands-on projects—ideal for beginners and career switchers.

---

### What you'll build

- CLI tools and automation scripts
- File and data handling with JSON
- Small projects (calculator, file organizer, to-do or quiz app)

---

### From Hello World to real code

Get started in minutes:

```python
# Your first Python program
name = input("Your name? ")
print(f"Hello, {name}! Welcome to Python.")
```

Run it in the terminal:

```bash
python hello.py
```

---

### Core topics

| Area | You'll learn |
|------|----------------|
| **Basics** | Variables, types, operators, I/O |
| **Data structures** | Lists, tuples, dicts, sets |
| **Control flow** | `if`/`elif`/`else`, `for`, `while` |
| **Functions** | Definition, arguments, return, modules |
| **Files** | Read/write, JSON, `pathlib` |
| **OOP** | Classes, inheritance, exceptions, PEP 8 |

---

### Example: reading JSON

```python
import json
from pathlib import Path

def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)

config = load_config("settings.json")
print(config.get("debug", False))
```

---

### Example: config JSON

```json
{
  "debug": true,
  "log_level": "info"
}
```

---

### Projects you'll build

1. **CLI Calculator** – Functions and user input.
2. **File Organizer** – Sort files by type/date with `os` and `pathlib`.
3. **Mini app** – Your choice: to-do list, quiz, or similar.

---

*3 months · Offline · Beginner-friendly · Certificate on completion*
"""


def get_token() -> str:
    if ADMIN_TOKEN:
        return ADMIN_TOKEN.strip()
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("Set ADMIN_EMAIL and ADMIN_PASSWORD, or ADMIN_TOKEN (e.g. in .env.local).")
        sys.exit(1)
    r = requests.post(
        f"{BACKEND_API_BASE}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("Login failed: no access_token in response")
    return token


def get_first_category_id(session: requests.Session) -> int:
    r = session.get(f"{BACKEND_API_BASE}/courses/categories", timeout=15)
    r.raise_for_status()
    categories = r.json()
    if not categories:
        print("No course categories found. Create a category (e.g. Programming) in admin first.")
        sys.exit(1)
    return categories[0]["id"]


def build_payload(category_id: int) -> dict:
    return {
        "title": "Python Programming",
        "slug": "python-programming",
        "category_id": category_id,
        "description": COURSE_DESCRIPTION,
        "short_description": "Master Python in 3 months with offline classes. Covers fundamentals, data structures, OOP, and practical projects. Beginner-friendly, instructor-led.",
        "price": 0,
        "original_price": 15000,
        "emi_available": True,
        "emi_amount": 5000,
        "currency": "INR",
        "duration": "3 months",
        "duration_hours": 72,
        "batch_size": 20,
        "level": "beginner",
        "rating": 0,
        "review_count": 0,
        "enrollment_count": 0,
        "featured_image": None,
        "video_url": None,
        "instructor_name": "TechPath Instructor",
        "instructor_title": "Senior Python Developer",
        "instructor_bio": "Experienced in teaching Python and building production applications.",
        "instructor_image": None,
        "certification_name": "Python Programming Certificate",
        "certification_authority": "TechPath",
        "meta_title": "Python Programming Course – 3 Months Offline | TechPath",
        "meta_description": "Join our 3-month offline Python course. Learn from basics to projects. Beginner-friendly. Enroll now.",
        "next_batch_date": None,
        "status": "published",
        "featured": False,
        "is_active": True,
        "learning_outcomes": [
            "Write Python scripts and use the interpreter",
            "Use variables, data types, and operators",
            "Work with lists, tuples, dictionaries, and sets",
            "Define functions and use modules",
            "Handle files and exceptions",
            "Understand OOP: classes and objects",
            "Build a small project (e.g. CLI app or script)",
        ],
        "prerequisites": [
            "Basic computer use (file, folder, browser)",
            "No prior coding experience required",
            "Laptop for practice (optional for in-class)",
        ],
        "curriculum": [
            {
                "title": "Introduction to Python",
                "topics": ["Installation", "IDLE/VS Code", "Hello World", "Variables", "Input/Output"],
                "duration": "1 week",
            },
            {
                "title": "Data Types & Control Flow",
                "topics": ["Numbers", "Strings", "Lists", "Conditionals", "Loops"],
                "duration": "2 weeks",
            },
            {
                "title": "Functions & Modules",
                "topics": ["Defining functions", "Arguments", "Return", "Import", "Standard library"],
                "duration": "2 weeks",
            },
            {
                "title": "Data Structures & File Handling",
                "topics": ["Tuples", "Sets", "Dictionaries", "File read/write", "JSON"],
                "duration": "2 weeks",
            },
            {
                "title": "OOP & Best Practices",
                "topics": ["Classes", "Inheritance", "Exception handling", "PEP 8"],
                "duration": "2 weeks",
            },
            {
                "title": "Project",
                "topics": ["Design a small project", "Code review", "Presentation"],
                "duration": "2 weeks",
            },
        ],
        "projects": [
            {"title": "CLI Calculator", "description": "Simple calculator using functions and input handling."},
            {"title": "File Organizer Script", "description": "Sort files by type/date using os and pathlib."},
            {"title": "Mini Project", "description": "Small app or script of your choice (e.g. to-do list, quiz)."},
        ],
        "skill_ids": [],
    }


def main() -> None:
    if not BACKEND_API_BASE:
        print("Set BACKEND_API_BASE (e.g. http://localhost:8000/api/v1).")
        sys.exit(1)

    print("Backend API:", BACKEND_API_BASE)
    token = get_token()
    print("Auth OK.")

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Content-Type"] = "application/json"

    category_id = get_first_category_id(session)
    print("Using category_id:", category_id)

    payload = build_payload(category_id)
    r = session.post(f"{BACKEND_API_BASE}/courses/", json=payload, timeout=30)

    if r.status_code == 409:
        print("Course with slug 'python-programming' already exists. Delete it first or use a different slug.")
        sys.exit(1)
    r.raise_for_status()

    data = r.json()
    print("Course created successfully.")
    print("  id:", data.get("id"))
    print("  title:", data.get("title"))
    print("  slug:", data.get("slug"))
    print("  status:", data.get("status"))


if __name__ == "__main__":
    main()
