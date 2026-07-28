# Module 10 — Assignment: Python Projects

**Deadline:** End of Week 16
**Submission:** Python files (.py) + output screenshots

---

## Task 1: Student Management System — 35 marks

Build a command-line application that manages student records.

**Features:**
- Add student (name, roll number, course, marks for 5 subjects)
- View all students in a formatted table
- Search by name or roll number
- Calculate and display: total, percentage, grade
- Delete a student by roll number
- Save data to a JSON file and load on startup

**Requirements:**
- Use functions for each operation
- Use a `while True` loop with a menu (1-6 options)
- Store students as a list of dictionaries
- Use `json` module for file I/O
- Handle errors (invalid marks, duplicate roll numbers, file not found)

---

## Task 2: Expense Analyzer — 30 marks

Create a program that reads expenses from a CSV file and generates a report.

**Input CSV format:**
```
date,description,category,amount
2026-01-15,Chai and samosa,Food,50
2026-01-15,Bus ticket,Transport,30
```

**Features:**
- Read CSV file using `csv` module
- Total spending per category (use dictionary)
- Highest single expense
- Daily average spending
- Month-wise spending summary
- Print formatted report with aligned columns

**Requirements:**
- Use `csv.DictReader` to read data
- Create at least 20 sample expense entries
- Use functions for each calculation
- Handle file not found error

---

## Task 3: Password Generator & Validator — 20 marks

**Generator:**
- Generate random password of given length
- Options: include uppercase, lowercase, digits, special characters
- Use `random` and `string` modules

**Validator:**
- Check if a password meets rules: min 8 chars, has uppercase, lowercase, digit, special char
- Return which rules pass/fail

---

## Task 4: Quiz Game — 15 marks

- Store 10 questions in a list of dictionaries (question, options, correct_index)
- Show questions one by one with 4 options
- Track score and show result at the end
- Show correct answer if user gets it wrong
- Use `random.shuffle` to randomize question order

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Functions | Clean, reusable, well-named | Functions exist but messy | No functions |
| File I/O | JSON + CSV both work | One works | No file handling |
| Error handling | All edge cases handled | Basic try/except | Program crashes |
| Logic | All features work correctly | Most features work | Partial implementation |
| Code style | Clean, readable, consistent | Readable | Hard to follow |
