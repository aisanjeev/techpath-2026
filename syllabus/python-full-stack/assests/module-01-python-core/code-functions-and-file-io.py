"""
TechPath Institute — Python Core: Functions & File I/O
=======================================================
A fully runnable Python file covering functions, exception
handling, and file operations with Indian-context examples.

Run this file:  python code-functions-and-file-io.py
"""

import csv
import json
import re
import os

# ──────────────────────────────────────────────
# 1. FUNCTIONS — BASICS
# ──────────────────────────────────────────────

print("=" * 50)
print("1. FUNCTIONS — BASICS")
print("=" * 50)


def greet_student(name, course="Python Full Stack"):
    """Greet a TechPath Institute student with their course name."""
    return f"Welcome to TechPath Institute, {name}! You are enrolled in {course}."


print(greet_student("Rahul"))
print(greet_student("Priya", "Web Development"))


def calculate_fee(base_fee, discount_percent=0, gst_percent=18):
    """Calculate final fee after discount and GST."""
    discounted = base_fee * (1 - discount_percent / 100)
    final = discounted * (1 + gst_percent / 100)
    return round(final, 2)


fee = calculate_fee(25000, discount_percent=10)
print(f"\nBase: ₹25,000 | 10% discount | 18% GST → Final: ₹{fee:,.2f}")


# ──────────────────────────────────────────────
# 2. *args AND **kwargs
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("2. *args AND **kwargs")
print("=" * 50)


def total_marks(*marks):
    """Calculate total and average marks for any number of subjects."""
    total = sum(marks)
    average = total / len(marks) if marks else 0
    return total, average


total, avg = total_marks(85, 92, 78, 88, 95)
print(f"Total: {total}, Average: {avg:.1f}")


def create_student_record(**details):
    """Create a formatted student record from keyword arguments."""
    print("\n--- Student Record ---")
    for key, value in details.items():
        # Convert snake_case key to Title Case
        label = key.replace("_", " ").title()
        print(f"  {label}: {value}")
    print("--- End of Record ---")


create_student_record(
    name="Ananya Verma",
    age=20,
    city="Bhopal",
    course="Python Full Stack",
    fee_paid=True,
    contact_number="9876543210",
)


# ──────────────────────────────────────────────
# 3. LAMBDA FUNCTIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("3. LAMBDA FUNCTIONS")
print("=" * 50)

# Simple lambda
add_gst = lambda price: round(price * 1.18, 2)
print(f"₹1000 + GST = ₹{add_gst(1000)}")

# Sorting with lambda
students = [
    {"name": "Rahul", "marks": 78, "city": "Bhopal"},
    {"name": "Priya", "marks": 92, "city": "Pune"},
    {"name": "Amit", "marks": 85, "city": "Delhi"},
    {"name": "Sneha", "marks": 88, "city": "Mumbai"},
]

# Sort by marks (descending)
by_marks = sorted(students, key=lambda s: s["marks"], reverse=True)
print("\nRanking by marks:")
for rank, s in enumerate(by_marks, 1):
    print(f"  {rank}. {s['name']} — {s['marks']} marks")

# map with lambda
fees = [15000, 20000, 25000, 30000]
with_gst = list(map(lambda f: round(f * 1.18), fees))
print(f"\nFees: {fees}")
print(f"With GST: {with_gst}")

# filter with lambda
high_scorers = list(filter(lambda s: s["marks"] >= 85, students))
print(f"\nHigh scorers (>=85): {[s['name'] for s in high_scorers]}")


# ──────────────────────────────────────────────
# 4. SCOPE (LEGB RULE)
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("4. SCOPE (LEGB RULE)")
print("=" * 50)

institute = "TechPath Institute"  # Global scope


def get_greeting():
    branch = "Bhopal"  # Local scope (enclosing for inner function)

    def format_message():
        # Accesses 'branch' from enclosing scope, 'institute' from global
        return f"{institute}, {branch} Branch"

    return format_message()


print(f"Greeting: {get_greeting()}")
print(f"Global 'institute' is still: {institute}")

# Demonstrating global keyword
counter = 0


def increment():
    global counter
    counter += 1


increment()
increment()
increment()
print(f"Counter after 3 increments: {counter}")


# ──────────────────────────────────────────────
# 5. EXCEPTION HANDLING
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("5. EXCEPTION HANDLING")
print("=" * 50)


def safe_divide(a, b):
    """Divide two numbers with error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  Error: Cannot divide {a} by zero!")
        return None
    except TypeError as e:
        print(f"  Error: Invalid types — {e}")
        return None
    else:
        print(f"  {a} / {b} = {result:.2f}")
        return result
    finally:
        print(f"  (Division attempt complete for {a}/{b})")


safe_divide(100, 3)
safe_divide(50, 0)
safe_divide("ten", 2)


# Custom exception
class EnrollmentError(Exception):
    """Raised when a student cannot be enrolled."""

    def __init__(self, student_name, reason):
        self.student_name = student_name
        self.reason = reason
        super().__init__(f"Cannot enroll {student_name}: {reason}")


def enroll_student(name, age, fee_paid):
    """Enroll a student with validation."""
    if age < 16:
        raise EnrollmentError(name, "Must be at least 16 years old")
    if not fee_paid:
        raise EnrollmentError(name, "Fee payment pending")
    return f"{name} enrolled successfully!"


print("\nEnrollment tests:")
for name, age, paid in [("Rahul", 22, True), ("Priya", 15, True), ("Amit", 20, False)]:
    try:
        result = enroll_student(name, age, paid)
        print(f"  {result}")
    except EnrollmentError as e:
        print(f"  {e}")


# ──────────────────────────────────────────────
# 6. REGEX
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("6. REGEX")
print("=" * 50)

text = """
TechPath Institute Student Directory:
Rahul Sharma — rahul.sharma@email.com — 9876543210 — Bhopal
Priya Patel — priya.p@gmail.com — 8765432109 — Pune
Amit Kumar — amit_k@yahoo.co.in — 7654321098 — Delhi
Office: info@techpath.biz — 0755-2556789
"""

# Find all email addresses
emails = re.findall(r"[\w.]+@[\w.]+", text)
print(f"Emails found: {emails}")

# Find all 10-digit mobile numbers
mobiles = re.findall(r"\b\d{10}\b", text)
print(f"Mobile numbers: {mobiles}")

# Find all names (capitalized word followed by capitalized word)
names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", text)
print(f"Names: {names}")

# Validate an email
def is_valid_email(email):
    pattern = r"^[\w.+-]+@[\w-]+\.[\w.]+$"
    return bool(re.match(pattern, email))

test_emails = ["rahul@email.com", "invalid@", "priya@mail.co.in", "@noname.com"]
for email in test_emails:
    status = "Valid" if is_valid_email(email) else "Invalid"
    print(f"  {email:25s} → {status}")


# ──────────────────────────────────────────────
# 7. FILE I/O — TEXT FILES
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("7. FILE I/O — TEXT FILES")
print("=" * 50)

# Write a text file
students_data = [
    "Rahul Sharma, Bhopal, Python Full Stack, 25000",
    "Priya Patel, Pune, Web Development, 20000",
    "Amit Kumar, Delhi, Data Science, 30000",
    "Sneha Gupta, Mumbai, Python Full Stack, 25000",
    "Vikram Singh, Jaipur, Web Development, 20000",
]

filename = "techpath_students.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("TechPath Institute — Student List\n")
    f.write("=" * 40 + "\n")
    for line in students_data:
        f.write(line + "\n")
print(f"Written {len(students_data)} records to {filename}")

# Read and process the text file
with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")
print("Students from the file:")
for line in lines[2:]:  # Skip header lines
    parts = line.strip().split(", ")
    if len(parts) == 4:
        name, city, course, fee = parts
        print(f"  {name} ({city}) — {course} — ₹{fee}")


# ──────────────────────────────────────────────
# 8. FILE I/O — CSV FILES
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("8. FILE I/O — CSV FILES")
print("=" * 50)

# Write CSV
csv_filename = "techpath_students.csv"
csv_data = [
    {"Name": "Rahul Sharma", "City": "Bhopal", "Course": "Python Full Stack", "Fee": 25000},
    {"Name": "Priya Patel", "City": "Pune", "Course": "Web Development", "Fee": 20000},
    {"Name": "Amit Kumar", "City": "Delhi", "Course": "Data Science", "Fee": 30000},
    {"Name": "Sneha Gupta", "City": "Mumbai", "Course": "Python Full Stack", "Fee": 25000},
]

with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "City", "Course", "Fee"])
    writer.writeheader()
    writer.writerows(csv_data)
print(f"Written {len(csv_data)} records to {csv_filename}")

# Read CSV and calculate stats
with open(csv_filename, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    records = list(reader)

total_fees = sum(int(r["Fee"]) for r in records)
avg_fee = total_fees / len(records)
print(f"Total students: {len(records)}")
print(f"Total fees collected: ₹{total_fees:,}")
print(f"Average fee: ₹{avg_fee:,.0f}")

# Course-wise count
from collections import Counter

course_counts = Counter(r["Course"] for r in records)
print("Course-wise enrollment:")
for course, count in course_counts.items():
    print(f"  {course}: {count} student(s)")


# ──────────────────────────────────────────────
# 9. FILE I/O — JSON FILES
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("9. FILE I/O — JSON FILES")
print("=" * 50)

# Write JSON
json_filename = "techpath_data.json"
institute_data = {
    "institute": "TechPath Institute",
    "city": "Bhopal",
    "established": 2024,
    "courses": [
        {"name": "Python Full Stack", "duration_months": 6, "fee": 25000},
        {"name": "Web Development", "duration_months": 4, "fee": 20000},
        {"name": "Data Science", "duration_months": 8, "fee": 30000},
    ],
    "contact": {
        "email": "info@techpath.biz",
        "phone": "0755-2556789",
    },
}

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(institute_data, f, indent=2, ensure_ascii=False)
print(f"Written institute data to {json_filename}")

# Read JSON
with open(json_filename, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"\nInstitute: {data['institute']}")
print(f"City: {data['city']}")
print(f"Contact: {data['contact']['email']}")
print(f"\nCourses offered:")
for course in data["courses"]:
    print(f"  {course['name']} — {course['duration_months']} months — ₹{course['fee']:,}")


# ──────────────────────────────────────────────
# 10. PUTTING IT ALL TOGETHER — Mini Project
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("10. MINI PROJECT — Student Report Generator")
print("=" * 50)


def generate_report(students, output_file="student_report.txt"):
    """Generate a formatted report from student data."""
    total_fee = sum(s["fee"] for s in students)
    avg_fee = total_fee / len(students)
    cities = set(s["city"] for s in students)

    report_lines = [
        "TechPath Institute — Student Report",
        "=" * 40,
        f"Total Students: {len(students)}",
        f"Cities Represented: {', '.join(sorted(cities))}",
        f"Total Fees: ₹{total_fee:,}",
        f"Average Fee: ₹{avg_fee:,.0f}",
        "",
        "Student Details:",
        "-" * 40,
    ]

    for i, s in enumerate(students, 1):
        report_lines.append(
            f"{i}. {s['name']:20s} | {s['city']:10s} | ₹{s['fee']:>8,}"
        )

    report_lines.append("-" * 40)
    report_lines.append("Report generated successfully.")

    report_text = "\n".join(report_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_text)

    return report_text


students_for_report = [
    {"name": "Rahul Sharma", "city": "Bhopal", "fee": 25000},
    {"name": "Priya Patel", "city": "Pune", "fee": 22000},
    {"name": "Amit Kumar", "city": "Delhi", "fee": 28000},
    {"name": "Ananya Verma", "city": "Bhopal", "fee": 25000},
    {"name": "Vikram Singh", "city": "Jaipur", "fee": 20000},
]

report = generate_report(students_for_report)
print(report)

# Clean up generated files
for f in [filename, csv_filename, json_filename, "student_report.txt"]:
    if os.path.exists(f):
        os.remove(f)
        print(f"\nCleaned up: {f}")

print("\n" + "=" * 50)
print("Program complete! You have mastered functions & file I/O.")
print("=" * 50)
