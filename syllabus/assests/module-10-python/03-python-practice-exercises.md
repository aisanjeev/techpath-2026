# Python Practice Exercises

**Module 10 — Python Programming | Practice Problems**

---

## Beginner Level

### Exercise 1: Temperature Converter

Write a function that converts Celsius to Fahrenheit and vice versa.

```python
# Formula: F = (C × 9/5) + 32

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

# Test
print(celsius_to_fahrenheit(100))   # 212.0
print(fahrenheit_to_celsius(98.6))  # 37.0
```

---

### Exercise 2: Even/Odd Checker

```python
def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Test with multiple numbers
for n in [1, 2, 3, 10, 15, 22]:
    print(f"{n} is {check_even_odd(n)}")
```

---

### Exercise 3: Simple Calculator

```python
def calculator():
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            return "Cannot divide by zero!"
        result = num1 / num2
    else:
        return "Invalid operator!"

    return f"{num1} {operator} {num2} = {result}"

print(calculator())
```

---

### Exercise 4: Multiplication Table

```python
def multiplication_table(number):
    print(f"\nMultiplication Table for {number}:")
    print("-" * 20)
    for i in range(1, 11):
        print(f"{number} x {i:2d} = {number * i:3d}")

multiplication_table(7)
```

---

## Intermediate Level

### Exercise 5: Student Grade System

```python
def student_report(name, marks):
    total = sum(marks)
    average = total / len(marks)
    highest = max(marks)
    lowest = min(marks)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 40:
        grade = "D"
    else:
        grade = "F"

    status = "PASS" if grade != "F" else "FAIL"

    print(f"\n--- Student Report ---")
    print(f"Name:    {name}")
    print(f"Marks:   {marks}")
    print(f"Total:   {total}")
    print(f"Average: {average:.1f}")
    print(f"Highest: {highest}")
    print(f"Lowest:  {lowest}")
    print(f"Grade:   {grade}")
    print(f"Status:  {status}")

student_report("Rahul", [85, 92, 78, 95, 88])
```

---

### Exercise 6: Password Strength Checker

```python
def check_password(password):
    issues = []

    if len(password) < 8:
        issues.append("At least 8 characters")
    if not any(c.isupper() for c in password):
        issues.append("At least one uppercase letter")
    if not any(c.islower() for c in password):
        issues.append("At least one lowercase letter")
    if not any(c.isdigit() for c in password):
        issues.append("At least one number")
    if not any(c in "!@#$%^&*()_+-=" for c in password):
        issues.append("At least one special character")

    if not issues:
        return "Strong password!"
    else:
        return f"Weak password. Missing:\n" + "\n".join(f"  - {i}" for i in issues)

# Test
print(check_password("hello"))
print()
print(check_password("MyP@ss2026"))
```

---

### Exercise 7: Word Counter

```python
def count_words(text):
    words = text.split()
    word_count = {}

    for word in words:
        word = word.lower().strip(".,!?;:")
        word_count[word] = word_count.get(word, 0) + 1

    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(word_count)}")
    print("\nTop words:")
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:5]:
        print(f"  '{word}' appeared {count} times")

text = "Python is great. Python is easy. Python is fun. I love Python programming."
count_words(text)
```

---

### Exercise 8: Contact Book

```python
contacts = {}

def add_contact(name, phone, email=""):
    contacts[name] = {"phone": phone, "email": email}
    print(f"Added: {name}")

def search_contact(name):
    if name in contacts:
        c = contacts[name]
        print(f"Name: {name}")
        print(f"Phone: {c['phone']}")
        print(f"Email: {c['email'] or 'N/A'}")
    else:
        print(f"'{name}' not found.")

def show_all():
    if not contacts:
        print("No contacts.")
        return
    print(f"\n{'Name':<15} {'Phone':<15} {'Email'}")
    print("-" * 45)
    for name, info in contacts.items():
        print(f"{name:<15} {info['phone']:<15} {info['email'] or 'N/A'}")

# Test
add_contact("Rahul", "9876543210", "rahul@email.com")
add_contact("Priya", "9123456789")
add_contact("Amit", "9988776655", "amit@email.com")
show_all()
print()
search_contact("Priya")
```

---

## Advanced Level

### Exercise 9: File-Based Quiz Game

```python
import random

questions = [
    {"q": "Capital of India?", "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"], "answer": 1},
    {"q": "Largest planet?", "options": ["Mars", "Saturn", "Jupiter", "Venus"], "answer": 2},
    {"q": "Python creator?", "options": ["Elon Musk", "Guido van Rossum", "Mark Z", "Bill Gates"], "answer": 1},
    {"q": "HTML stands for?", "options": ["Hyper Text ML", "High Tech ML", "Hyper Transfer ML", "Home Tool ML"], "answer": 0},
    {"q": "1 KB = ? bytes", "options": ["100", "512", "1024", "2048"], "answer": 2},
]

def run_quiz():
    score = 0
    random.shuffle(questions)

    print("=== QUIZ GAME ===\n")

    for i, q in enumerate(questions):
        print(f"Q{i+1}. {q['q']}")
        for j, opt in enumerate(q["options"]):
            print(f"  {j+1}. {opt}")

        try:
            answer = int(input("Your answer (1-4): ")) - 1
            if answer == q["answer"]:
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong! Answer: {q['options'][q['answer']]}\n")
        except ValueError:
            print("Invalid input. Skipped.\n")

    print(f"\nScore: {score}/{len(questions)}")
    percentage = (score / len(questions)) * 100
    print(f"Percentage: {percentage:.0f}%")
    print("PASS!" if percentage >= 60 else "Try again!")

run_quiz()
```

---

### Exercise 10: Expense Tracker

```python
from datetime import date

expenses = []

def add_expense(category, amount, description=""):
    expenses.append({
        "date": str(date.today()),
        "category": category,
        "amount": amount,
        "description": description
    })
    print(f"Added: {category} - Rs.{amount}")

def show_summary():
    if not expenses:
        print("No expenses recorded.")
        return

    total = sum(e["amount"] for e in expenses)
    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    print(f"\n=== Expense Summary ===")
    print(f"Total Expenses: Rs.{total}")
    print(f"\nBy Category:")
    for cat, amt in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        percentage = (amt / total) * 100
        print(f"  {cat:<15} Rs.{amt:>8.2f}  ({percentage:.1f}%)")

# Test
add_expense("Food", 250, "Lunch")
add_expense("Transport", 150, "Auto")
add_expense("Food", 180, "Dinner")
add_expense("Shopping", 500, "Books")
add_expense("Transport", 100, "Bus")
show_summary()
```

---

## Exercises Summary

| # | Exercise | Concepts Practiced |
|---|---------|-------------------|
| 1 | Temperature Converter | Functions, math |
| 2 | Even/Odd Checker | Conditionals, modulo |
| 3 | Simple Calculator | Input, conditionals |
| 4 | Multiplication Table | Loops, formatting |
| 5 | Student Grades | Lists, functions, conditionals |
| 6 | Password Checker | Strings, any(), list comp |
| 7 | Word Counter | Dicts, string methods, sorting |
| 8 | Contact Book | Dictionaries, functions |
| 9 | Quiz Game | Lists, dicts, random, loops |
| 10 | Expense Tracker | Dicts, lists, functions, datetime |
