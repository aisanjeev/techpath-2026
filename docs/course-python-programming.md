# Course: Python Programming (Manual Entry Template)

**Use this file to edit content and feed into the admin/API. Duration: 3 months | Mode: Offline.**

---

## Required Fields

| Field | Value | Notes |
|-------|--------|--------|
| **title** | Python Programming | 1–255 chars |
| **slug** | python-programming | Lowercase, hyphens only (`a-z0-9-`) |
| **category_id** | 1 | Replace with your actual category ID (e.g. Programming) |
| **description** | *(see below)* | Min 10 chars |
| **price** | 0 | INR, ≥ 0 (edit as needed) |
| **currency** | INR | 3 chars |
| **duration** | 3 months | Max 50 chars |

---

## Description (long) – plain

```
Learn Python from basics to advanced in 3 months. This offline course covers syntax, data structures, OOP, file handling, and real-world projects. Ideal for beginners and anyone switching to programming. Hands-on sessions and live instructor support.
```

---

## Description (long) – Markdown with code (copy into admin)

Use the block below in the course **description** field in admin so it renders with headings, lists, and syntax-highlighted code. Code blocks use language tags: `python`, `bash`, `json`.

<details>
<summary>Click to expand: full markdown (copy everything inside the fence below)</summary>

Use **5 backticks** as the outer fence so inner ` ```python ` / ` ```bash ` don’t break. Copy from the opening ` ``` ` to the closing ` ``` ` (including the newline after the last line).

`````
Master **Python** from zero to building real scripts in 3 months. This offline, instructor-led course covers syntax, data structures, OOP, file handling, and hands-on projects—ideal for beginners and career switchers.

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
`````

</details>

**Paste tip:** When pasting into the admin description field, paste only the *content* between the two 5-backtick lines (not the backticks themselves). The inner blocks must stay as ` ```python `, ` ```bash `, ` ```json ` so the frontend can syntax-highlight them.

### Paste-ready block (no nesting)

If your editor breaks on nested fences, use this version. After pasting into admin, **remove the 4 spaces** in front of any line that starts with ` ``` ` (so that `    ```python` becomes ` ```python`).

```text
Master **Python** from zero to building real scripts in 3 months. This offline, instructor-led course covers syntax, data structures, OOP, file handling, and hands-on projects—ideal for beginners and career switchers.

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
```

---

## Short Description (max 500 chars)

```
Master Python in 3 months with offline classes. Covers fundamentals, data structures, OOP, and practical projects. Beginner-friendly, instructor-led.
```

---

## Pricing & Batch

| Field | Value |
|-------|--------|
| original_price | 15000 |
| emi_available | true |
| emi_amount | 5000 |
| duration_hours | 72 |
| batch_size | 20 |
| level | beginner |

---

## Instructor (optional)

| Field | Value |
|-------|--------|
| instructor_name | TechPath Instructor |
| instructor_title | Senior Python Developer |
| instructor_bio | Experienced in teaching Python and building production applications. |
| instructor_image | *(URL or path)* |

---

## Certification (optional)

| Field | Value |
|-------|--------|
| certification_name | Python Programming Certificate |
| certification_authority | TechPath |

---

## SEO (optional)

| Field | Value |
|-------|--------|
| meta_title | Python Programming Course – 3 Months Offline | TechPath |
| meta_description | Join our 3-month offline Python course. Learn from basics to projects. Beginner-friendly. Enroll now. |

---

## Media (optional)

| Field | Value |
|-------|--------|
| featured_image | *(URL or upload path)* |
| video_url | *(intro/promo video URL)* |

---

## Status & Visibility

| Field | Value |
|-------|--------|
| status | draft _or_ published |
| featured | false |
| is_active | true |
| next_batch_date | *(e.g. 2026-03-01)* |

---

## Learning Outcomes (list – one per line)

Edit and use as bullet list or JSON array:

- Write Python scripts and use the interpreter
- Use variables, data types, and operators
- Work with lists, tuples, dictionaries, and sets
- Define functions and use modules
- Handle files and exceptions
- Understand OOP: classes and objects
- Build a small project (e.g. CLI app or script)

---

## Prerequisites (list – one per line)

- Basic computer use (file, folder, browser)
- No prior coding experience required
- Laptop for practice (optional for in-class)

---

## Curriculum (modules)

Each module: **title**, **topics** (list), **duration** (optional).

**Module 1: Introduction to Python**
- Topics: Installation, IDLE/VS Code, Hello World, variables, input/output
- Duration: 1 week

**Module 2: Data Types & Control Flow**
- Topics: Numbers, strings, lists, conditionals, loops
- Duration: 2 weeks

**Module 3: Functions & Modules**
- Topics: Defining functions, arguments, return, import, standard library
- Duration: 2 weeks

**Module 4: Data Structures & File Handling**
- Topics: Tuples, sets, dictionaries, file read/write, JSON
- Duration: 2 weeks

**Module 5: OOP & Best Practices**
- Topics: Classes, inheritance, exception handling, PEP 8
- Duration: 2 weeks

**Module 6: Project**
- Topics: Design a small project, code review, presentation
- Duration: 2 weeks

---

## Projects (title + optional description)

1. **CLI Calculator** – Simple calculator using functions and input handling.
2. **File Organizer Script** – Sort files by type/date using `os` and `pathlib`.
3. **Mini Project** – Small app or script of your choice (e.g. to-do list, quiz).

---

## JSON Payload (for API / import)

Use this after replacing `category_id` (and optional `skill_ids`) with real IDs.

```json
{
  "title": "Python Programming",
  "slug": "python-programming",
  "category_id": 1,
  "description": "Learn Python from basics to advanced in 3 months. This offline course covers syntax, data structures, OOP, file handling, and real-world projects. Ideal for beginners and anyone switching to programming. Hands-on sessions and live instructor support.",
  "short_description": "Master Python in 3 months with offline classes. Covers fundamentals, data structures, OOP, and practical projects. Beginner-friendly, instructor-led.",
  "price": 0,
  "original_price": 15000,
  "emi_available": true,
  "emi_amount": 5000,
  "currency": "INR",
  "duration": "3 months",
  "duration_hours": 72,
  "batch_size": 20,
  "level": "beginner",
  "rating": 0,
  "review_count": 0,
  "enrollment_count": 0,
  "featured_image": null,
  "video_url": null,
  "instructor_name": "TechPath Instructor",
  "instructor_title": "Senior Python Developer",
  "instructor_bio": "Experienced in teaching Python and building production applications.",
  "instructor_image": null,
  "certification_name": "Python Programming Certificate",
  "certification_authority": "TechPath",
  "meta_title": "Python Programming Course – 3 Months Offline | TechPath",
  "meta_description": "Join our 3-month offline Python course. Learn from basics to projects. Beginner-friendly. Enroll now.",
  "next_batch_date": null,
  "status": "draft",
  "featured": false,
  "is_active": true,
  "learning_outcomes": [
    "Write Python scripts and use the interpreter",
    "Use variables, data types, and operators",
    "Work with lists, tuples, dictionaries, and sets",
    "Define functions and use modules",
    "Handle files and exceptions",
    "Understand OOP: classes and objects",
    "Build a small project (e.g. CLI app or script)"
  ],
  "prerequisites": [
    "Basic computer use (file, folder, browser)",
    "No prior coding experience required",
    "Laptop for practice (optional for in-class)"
  ],
  "curriculum": [
    { "title": "Introduction to Python", "topics": ["Installation", "IDLE/VS Code", "Hello World", "Variables", "Input/Output"], "duration": "1 week" },
    { "title": "Data Types & Control Flow", "topics": ["Numbers", "Strings", "Lists", "Conditionals", "Loops"], "duration": "2 weeks" },
    { "title": "Functions & Modules", "topics": ["Defining functions", "Arguments", "Return", "Import", "Standard library"], "duration": "2 weeks" },
    { "title": "Data Structures & File Handling", "topics": ["Tuples", "Sets", "Dictionaries", "File read/write", "JSON"], "duration": "2 weeks" },
    { "title": "OOP & Best Practices", "topics": ["Classes", "Inheritance", "Exception handling", "PEP 8"], "duration": "2 weeks" },
    { "title": "Project", "topics": ["Design a small project", "Code review", "Presentation"], "duration": "2 weeks" }
  ],
  "projects": [
    { "title": "CLI Calculator", "description": "Simple calculator using functions and input handling." },
    { "title": "File Organizer Script", "description": "Sort files by type/date using os and pathlib." },
    { "title": "Mini Project", "description": "Small app or script of your choice (e.g. to-do list, quiz)." }
  ],
  "skill_ids": []
}
```

---

## Notes

- **category_id**: Create a category (e.g. "Programming" / `programming`) in the admin and use its ID.
- **skill_ids**: Optional; add IDs of skills (e.g. Python, Programming) if you have them.
- **next_batch_date**: Use ISO datetime if you have a fixed batch start, e.g. `2026-03-01T10:00:00`.
- **status**: Use `draft` until ready, then `published`.
- Slug must be unique and only `a-z`, `0-9`, `-`.
