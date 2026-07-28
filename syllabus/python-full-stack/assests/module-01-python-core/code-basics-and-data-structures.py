"""
TechPath Institute — Python Core: Basics & Data Structures
===========================================================
A fully runnable Python file covering variables, data types,
control flow, and data structures with Indian-context examples.

Run this file:  python code-basics-and-data-structures.py
"""

# ──────────────────────────────────────────────
# 1. VARIABLES & DATA TYPES
# ──────────────────────────────────────────────

print("=" * 50)
print("1. VARIABLES & DATA TYPES")
print("=" * 50)

# Basic variables
student_name = "Rahul Sharma"
age = 22
fee = 25000.00
is_enrolled = True
middle_name = None  # No middle name

print(f"Name: {student_name}")
print(f"Age: {age} (type: {type(age).__name__})")
print(f"Fee: ₹{fee:,.2f} (type: {type(fee).__name__})")
print(f"Enrolled: {is_enrolled} (type: {type(is_enrolled).__name__})")
print(f"Middle name: {middle_name} (type: {type(middle_name).__name__})")

# Type casting
user_input = "100"
number = int(user_input)
decimal = float(user_input)
back_to_str = str(number)
print(f"\nType casting: '{user_input}' → int({number}), float({decimal}), str('{back_to_str}')")


# ──────────────────────────────────────────────
# 2. OPERATORS
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("2. OPERATORS")
print("=" * 50)

base_fee = 25000
gst_rate = 18

# Arithmetic
total_fee = base_fee + (base_fee * gst_rate / 100)
print(f"Base fee: ₹{base_fee}")
print(f"GST ({gst_rate}%): ₹{base_fee * gst_rate / 100:.0f}")
print(f"Total fee: ₹{total_fee:.0f}")

# Floor division and modulo
total_months = 14
years = total_months // 12
remaining_months = total_months % 12
print(f"\n{total_months} months = {years} year(s) and {remaining_months} month(s)")

# Comparison
marks = 78
print(f"\nMarks: {marks}")
print(f"Passed (>= 40): {marks >= 40}")
print(f"Distinction (>= 75): {marks >= 75}")
print(f"Perfect (== 100): {marks == 100}")


# ──────────────────────────────────────────────
# 3. STRING OPERATIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("3. STRING OPERATIONS")
print("=" * 50)

institute = "  TechPath Institute, Bhopal  "

print(f"Original: '{institute}'")
print(f"Stripped: '{institute.strip()}'")
print(f"Upper: '{institute.strip().upper()}'")
print(f"Lower: '{institute.strip().lower()}'")
print(f"Replace: '{institute.strip().replace('Bhopal', 'Delhi')}'")
print(f"Split by comma: {institute.strip().split(', ')}")

# String slicing
course = "Python Full Stack"
print(f"\nCourse: '{course}'")
print(f"First 6 chars: '{course[:6]}'")
print(f"Last 5 chars: '{course[-5:]}'")
print(f"Reversed: '{course[::-1]}'")

# f-string formatting
price = 1599.5
quantity = 3
print(f"\nItem price: ₹{price:.2f}")
print(f"Quantity: {quantity}")
print(f"Total: ₹{price * quantity:,.2f}")
print(f"Padded: '{student_name:>30}'")  # Right-align in 30 chars


# ──────────────────────────────────────────────
# 4. CONTROL FLOW
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("4. CONTROL FLOW")
print("=" * 50)

# if/elif/else — Grade calculator
marks_list = [92, 78, 55, 38, 85]
print("Grade Calculator:")
for marks in marks_list:
    if marks >= 90:
        grade = "A+"
    elif marks >= 75:
        grade = "A"
    elif marks >= 60:
        grade = "B"
    elif marks >= 40:
        grade = "C"
    else:
        grade = "Fail"
    status = "Pass" if marks >= 40 else "Fail"
    print(f"  Marks: {marks:3d} → Grade: {grade:4s} ({status})")

# for loop with range
print("\nMultiplication table of 7:")
for i in range(1, 11):
    print(f"  7 x {i:2d} = {7 * i:3d}")

# while loop — simple countdown
print("\nCountdown:")
count = 5
while count > 0:
    print(f"  {count}...", end=" ")
    count -= 1
print("Launch!")

# break and continue
print("\nFirst student with marks > 80:")
student_marks = {"Rahul": 72, "Priya": 85, "Amit": 68, "Sneha": 91}
for name, marks in student_marks.items():
    if marks > 80:
        print(f"  Found: {name} with {marks} marks")
        break

print("\nStudents who passed (marks >= 40):")
all_marks = {"Rahul": 72, "Priya": 35, "Amit": 68, "Sneha": 28, "Vikram": 91}
for name, marks in all_marks.items():
    if marks < 40:
        continue  # Skip failed students
    print(f"  {name}: {marks}")


# ──────────────────────────────────────────────
# 5. LISTS
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("5. LISTS")
print("=" * 50)

# Creating and modifying lists
cities = ["Bhopal", "Delhi", "Pune", "Mumbai", "Chennai"]
print(f"Cities: {cities}")
print(f"First: {cities[0]}, Last: {cities[-1]}")
print(f"Slice [1:3]: {cities[1:3]}")

# Adding and removing
cities.append("Kolkata")
print(f"After append: {cities}")
cities.insert(2, "Jaipur")
print(f"After insert at 2: {cities}")
removed = cities.pop(2)
print(f"Popped index 2 ({removed}): {cities}")
cities.remove("Chennai")
print(f"Removed Chennai: {cities}")

# Sorting
fees = [25000, 18000, 32000, 15000, 28000]
print(f"\nOriginal fees: {fees}")
print(f"Sorted: {sorted(fees)}")
print(f"Sorted desc: {sorted(fees, reverse=True)}")
print(f"Min: ₹{min(fees)}, Max: ₹{max(fees)}, Avg: ₹{sum(fees)/len(fees):.0f}")

# List comprehension
print("\nList comprehensions:")
squares = [x ** 2 for x in range(1, 6)]
print(f"  Squares of 1-5: {squares}")

even_numbers = [x for x in range(1, 21) if x % 2 == 0]
print(f"  Even numbers 1-20: {even_numbers}")

discounted = [f"₹{fee * 0.9:.0f}" for fee in fees]
print(f"  10% discount on fees: {discounted}")


# ──────────────────────────────────────────────
# 6. TUPLES
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("6. TUPLES")
print("=" * 50)

# Tuples are immutable (cannot be changed)
bhopal_coords = (23.2599, 77.4126)
delhi_coords = (28.6139, 77.2090)
pune_coords = (18.5204, 73.8567)

print(f"Bhopal: lat={bhopal_coords[0]}, lon={bhopal_coords[1]}")

# Tuple unpacking
lat, lon = bhopal_coords
print(f"Unpacked — Latitude: {lat}, Longitude: {lon}")

# Multiple return values (tuples)
def min_max(numbers):
    return min(numbers), max(numbers)

lowest, highest = min_max([45, 82, 67, 91, 33])
print(f"Min: {lowest}, Max: {highest}")

# Tuple as dictionary key (because it's immutable)
distances = {
    ("Bhopal", "Delhi"): 778,
    ("Bhopal", "Pune"): 862,
    ("Delhi", "Mumbai"): 1400,
}
print(f"\nBhopal to Delhi: {distances[('Bhopal', 'Delhi')]} km")


# ──────────────────────────────────────────────
# 7. SETS
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("7. SETS")
print("=" * 50)

# Sets have unique items only
python_students = {"Rahul", "Priya", "Amit", "Sneha", "Rahul"}
web_students = {"Priya", "Vikram", "Sneha", "Neha"}

print(f"Python students: {python_students}")  # Rahul appears once
print(f"Web students: {web_students}")
print(f"Both courses: {python_students & web_students}")
print(f"All students: {python_students | web_students}")
print(f"Only Python: {python_students - web_students}")
print(f"Only one course: {python_students ^ web_students}")  # Symmetric diff


# ──────────────────────────────────────────────
# 8. DICTIONARIES
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("8. DICTIONARIES")
print("=" * 50)

# Student record
student = {
    "name": "Ananya Verma",
    "age": 20,
    "city": "Bhopal",
    "courses": ["Python", "Web Dev"],
    "fee_paid": True,
    "marks": {"Python": 88, "Web Dev": 75, "DBMS": 92},
}

print(f"Name: {student['name']}")
print(f"City: {student['city']}")
print(f"Courses: {', '.join(student['courses'])}")
print(f"Phone: {student.get('phone', 'Not provided')}")

# Nested access
print(f"Python marks: {student['marks']['Python']}")
avg = sum(student["marks"].values()) / len(student["marks"])
print(f"Average marks: {avg:.1f}")

# Dictionary comprehension
menu = {"Chai": 10, "Coffee": 30, "Samosa": 15, "Poha": 20, "Jalebi": 25}
print(f"\nMenu: {menu}")

gst_menu = {item: round(price * 1.05, 2) for item, price in menu.items()}
print(f"With 5% GST: {gst_menu}")

expensive = {item: price for item, price in menu.items() if price >= 20}
print(f"Items ≥ ₹20: {expensive}")

# Iterating
print("\n--- Canteen Menu ---")
for item, price in sorted(menu.items(), key=lambda x: x[1]):
    print(f"  {item:<10} ₹{price}")

print(f"\nTotal menu value: ₹{sum(menu.values())}")


# ──────────────────────────────────────────────
# 9. UNPACKING
# ──────────────────────────────────────────────

print("\n" + "=" * 50)
print("9. UNPACKING")
print("=" * 50)

# List unpacking with *
first, second, *rest = [100, 90, 85, 78, 72, 65]
print(f"Topper: {first}, Runner-up: {second}")
print(f"Others: {rest}")

first, *middle, last = ["Rahul", "Priya", "Amit", "Sneha", "Vikram"]
print(f"First: {first}, Last: {last}, Middle: {middle}")

# Dictionary merging with **
defaults = {"theme": "light", "language": "English", "font_size": 14}
user_prefs = {"theme": "dark", "font_size": 16}
final = {**defaults, **user_prefs}
print(f"\nMerged preferences: {final}")


print("\n" + "=" * 50)
print("Program complete! Great job working through basics.")
print("=" * 50)
