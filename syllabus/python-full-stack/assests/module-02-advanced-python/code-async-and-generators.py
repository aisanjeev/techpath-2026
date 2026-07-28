"""
TechPath Institute — Advanced Python: Async & Generators
==========================================================
Covers generators, iterators, async/await, closures,
functional programming, and type hints.

Run this file:  python code-async-and-generators.py
"""

import asyncio
import itertools
import sys
import time
from functools import reduce
from typing import Generator


# ──────────────────────────────────────────────
# 1. GENERATORS
# ──────────────────────────────────────────────

print("=" * 55)
print("1. GENERATORS")
print("=" * 55)


def student_ids(prefix: str, start: int = 1, count: int = 5) -> Generator[str, None, None]:
    """Generate student IDs lazily."""
    for i in range(start, start + count):
        yield f"{prefix}-{i:04d}"


# Using the generator
print("Student IDs:")
for sid in student_ids("TP", 1, 5):
    print(f"  {sid}")

# Generator is lazy — values produced on demand
gen = student_ids("TP", 100, 3)
print(f"\nnext() calls:")
print(f"  {next(gen)}")  # TP-0100
print(f"  {next(gen)}")  # TP-0101
print(f"  {next(gen)}")  # TP-0102


def fibonacci(limit: int) -> Generator[int, None, None]:
    """Generate Fibonacci numbers up to a limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


print(f"\nFibonacci up to 100: {list(fibonacci(100))}")


# Generator for fee installments
def emi_schedule(total: float, months: int) -> Generator[dict, None, None]:
    """Generate monthly EMI schedule."""
    monthly = round(total / months, 2)
    remaining = total
    for month in range(1, months + 1):
        payment = monthly if month < months else remaining
        remaining = round(remaining - payment, 2)
        yield {
            "month": month,
            "payment": payment,
            "remaining": max(remaining, 0),
        }


print(f"\nEMI Schedule for ₹25,000 over 6 months:")
for emi in emi_schedule(25000, 6):
    print(f"  Month {emi['month']}: Pay ₹{emi['payment']:>9,.2f} | Remaining: ₹{emi['remaining']:>9,.2f}")


# ──────────────────────────────────────────────
# 2. GENERATOR EXPRESSIONS vs LIST COMPREHENSIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. GENERATOR EXPRESSIONS vs LIST COMPREHENSIONS")
print("=" * 55)

# List comprehension — creates entire list in memory
squares_list = [x ** 2 for x in range(10000)]

# Generator expression — lazy, memory efficient
squares_gen = (x ** 2 for x in range(10000))

print(f"List size in memory: {sys.getsizeof(squares_list):,} bytes")
print(f"Generator size in memory: {sys.getsizeof(squares_gen):,} bytes")

# Both work with sum, max, min, etc.
total_list = sum(squares_list)
total_gen = sum(x ** 2 for x in range(10000))  # Inline generator expression
print(f"Sum (list): {total_list:,}")
print(f"Sum (gen):  {total_gen:,}")

# Practical example — find students with high fees
student_data = [
    {"name": "Rahul", "fee": 25000},
    {"name": "Priya", "fee": 20000},
    {"name": "Amit", "fee": 30000},
    {"name": "Sneha", "fee": 15000},
    {"name": "Vikram", "fee": 28000},
]

high_fee_names = [s["name"] for s in student_data if s["fee"] >= 25000]
total_high_fees = sum(s["fee"] for s in student_data if s["fee"] >= 25000)
print(f"\nStudents with fee >= ₹25,000: {high_fee_names}")
print(f"Total high fees: ₹{total_high_fees:,}")


# ──────────────────────────────────────────────
# 3. FUNCTIONAL PROGRAMMING — map, filter, reduce
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("3. FUNCTIONAL PROGRAMMING — map, filter, reduce")
print("=" * 55)

fees = [15000, 20000, 25000, 30000, 18000, 22000]
print(f"Original fees: {fees}")

# map — apply GST to all fees
with_gst = list(map(lambda f: round(f * 1.18), fees))
print(f"With 18% GST: {with_gst}")

# filter — fees above average
avg_fee = sum(fees) / len(fees)
above_avg = list(filter(lambda f: f > avg_fee, fees))
print(f"Above average (₹{avg_fee:,.0f}): {above_avg}")

# reduce — total of all fees
total = reduce(lambda a, b: a + b, fees)
print(f"Total fees: ₹{total:,}")

# Chaining map + filter
discounted_high = list(
    map(
        lambda f: round(f * 0.9),
        filter(lambda f: f >= 25000, fees)
    )
)
print(f"10% discount on fees >= ₹25,000: {discounted_high}")

# Sorting with key functions
students = [
    ("Rahul", 78, "Bhopal"),
    ("Priya", 92, "Pune"),
    ("Amit", 85, "Delhi"),
    ("Sneha", 88, "Mumbai"),
    ("Vikram", 72, "Jaipur"),
]

by_marks = sorted(students, key=lambda s: s[1], reverse=True)
print(f"\nSorted by marks (desc):")
for name, marks, city in by_marks:
    print(f"  {name:10s} {marks} marks ({city})")


# ──────────────────────────────────────────────
# 4. ITERTOOLS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. ITERTOOLS")
print("=" * 55)

# chain — combine multiple iterables
batch_a = ["Rahul", "Priya", "Amit"]
batch_b = ["Sneha", "Vikram"]
batch_c = ["Ananya"]

all_students = list(itertools.chain(batch_a, batch_b, batch_c))
print(f"All students (chain): {all_students}")

# islice — slice a generator (get first N items)
first_3_fibs = list(itertools.islice(fibonacci(1000), 8))
print(f"First 8 Fibonacci: {first_3_fibs}")

# cycle — repeat forever (we take first 7)
days = itertools.cycle(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
next_7 = [next(days) for _ in range(10)]
print(f"Next 10 days: {next_7}")

# combinations and permutations
courses = ["Python", "Web", "Data"]
combos = list(itertools.combinations(courses, 2))
print(f"\nCourse combos (pick 2): {combos}")

# product — all combinations of sizes and timings
batches = ["Morning", "Evening"]
modes = ["Online", "Offline"]
options = list(itertools.product(batches, modes))
print(f"Batch options: {options}")

# accumulate — running total
monthly_fees = [5000, 5000, 5000, 5000, 5000]
running_total = list(itertools.accumulate(monthly_fees))
print(f"\nMonthly payments: {monthly_fees}")
print(f"Running total:    {running_total}")

# groupby — group sorted data
city_students = [
    ("Bhopal", "Rahul"), ("Bhopal", "Priya"),
    ("Delhi", "Amit"), ("Delhi", "Neha"),
    ("Pune", "Sneha"),
]
print("\nGrouped by city:")
for city, group in itertools.groupby(city_students, key=lambda x: x[0]):
    names = [s[1] for s in group]
    print(f"  {city}: {names}")


# ──────────────────────────────────────────────
# 5. CLOSURES
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. CLOSURES")
print("=" * 55)


def make_discount_calculator(discount_percent):
    """Returns a function that applies a specific discount."""
    def calculate(price):
        return round(price * (1 - discount_percent / 100), 2)
    return calculate


ten_percent = make_discount_calculator(10)
twenty_percent = make_discount_calculator(20)

original = 25000
print(f"Original: ₹{original:,}")
print(f"10% off:  ₹{ten_percent(original):,}")
print(f"20% off:  ₹{twenty_percent(original):,}")


def make_counter(name):
    """Returns increment/decrement/get functions sharing the same count."""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    def decrement():
        nonlocal count
        count -= 1
        return count

    def get():
        return count

    return increment, decrement, get


inc, dec, get = make_counter("attendance")
inc()
inc()
inc()
dec()
print(f"\nCounter after 3 inc, 1 dec: {get()}")


# ──────────────────────────────────────────────
# 6. TYPE HINTS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("6. TYPE HINTS")
print("=" * 55)

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StudentRecord:
    """Student with full type hints."""
    name: str
    city: str
    course: str
    fee: float
    marks: list[int] = field(default_factory=list)
    email: Optional[str] = None

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

    @property
    def passed(self) -> bool:
        return self.average >= 40.0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "city": self.city,
            "course": self.course,
            "fee": self.fee,
            "average": round(self.average, 1),
            "passed": self.passed,
        }


def process_students(students: list[StudentRecord]) -> dict[str, list[str]]:
    """Group students by pass/fail status."""
    result: dict[str, list[str]] = {"passed": [], "failed": []}
    for s in students:
        if s.passed:
            result["passed"].append(s.name)
        else:
            result["failed"].append(s.name)
    return result


records = [
    StudentRecord("Rahul", "Bhopal", "Python", 25000, [85, 78, 92]),
    StudentRecord("Priya", "Pune", "Python", 25000, [95, 88, 91], "priya@mail.com"),
    StudentRecord("Amit", "Delhi", "Python", 25000, [32, 28, 35]),
]

for r in records:
    print(f"{r.name}: avg={r.average:.1f}, passed={r.passed}")

groups = process_students(records)
print(f"\nPassed: {groups['passed']}")
print(f"Failed: {groups['failed']}")


# ──────────────────────────────────────────────
# 7. ASYNC/AWAIT
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("7. ASYNC/AWAIT")
print("=" * 55)


async def fetch_student_data(name: str, delay: float) -> dict:
    """Simulate fetching student data from an API."""
    print(f"  Fetching {name}...")
    await asyncio.sleep(delay)
    return {"name": name, "status": "active", "delay": delay}


async def fetch_all_sequential():
    """Fetch students one after another (slow)."""
    start = time.perf_counter()
    results = []
    for name, delay in [("Rahul", 0.5), ("Priya", 0.3), ("Amit", 0.4)]:
        result = await fetch_student_data(name, delay)
        results.append(result)
    elapsed = time.perf_counter() - start
    print(f"  Sequential: {len(results)} results in {elapsed:.2f}s")
    return results


async def fetch_all_concurrent():
    """Fetch all students at the same time (fast)."""
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_student_data("Rahul", 0.5),
        fetch_student_data("Priya", 0.3),
        fetch_student_data("Amit", 0.4),
    )
    elapsed = time.perf_counter() - start
    print(f"  Concurrent: {len(results)} results in {elapsed:.2f}s")
    return results


async def fetch_with_timeout():
    """Fetch with a timeout limit."""
    try:
        result = await asyncio.wait_for(
            fetch_student_data("Slow Student", 5.0),
            timeout=1.0
        )
        return result
    except asyncio.TimeoutError:
        print("  Timeout! Request took too long.")
        return None


async def main():
    """Run all async examples."""
    print("\n--- Sequential Execution ---")
    await fetch_all_sequential()

    print("\n--- Concurrent Execution ---")
    await fetch_all_concurrent()

    print("\n--- With Timeout ---")
    await fetch_with_timeout()


# Run the async event loop
asyncio.run(main())


# ──────────────────────────────────────────────
# 8. PUTTING IT ALL TOGETHER
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("8. PUTTING IT ALL TOGETHER")
print("=" * 55)


def batch_processor(items, batch_size=3):
    """Generator that yields items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


all_students = [
    {"name": "Rahul", "fee": 25000, "city": "Bhopal"},
    {"name": "Priya", "fee": 20000, "city": "Pune"},
    {"name": "Amit", "fee": 30000, "city": "Delhi"},
    {"name": "Sneha", "fee": 25000, "city": "Mumbai"},
    {"name": "Vikram", "fee": 18000, "city": "Jaipur"},
    {"name": "Ananya", "fee": 22000, "city": "Bhopal"},
    {"name": "Deepak", "fee": 28000, "city": "Delhi"},
]

# Process in batches using generator
print("Processing students in batches of 3:")
for batch_num, batch in enumerate(batch_processor(all_students, 3), 1):
    names = [s["name"] for s in batch]
    total = sum(s["fee"] for s in batch)
    print(f"  Batch {batch_num}: {names} — Total: ₹{total:,}")

# Use reduce to get grand total
grand_total = reduce(lambda acc, s: acc + s["fee"], all_students, 0)
print(f"\nGrand total: ₹{grand_total:,}")

# Use itertools.groupby after sorting by city
sorted_by_city = sorted(all_students, key=lambda s: s["city"])
print("\nCity-wise summary:")
for city, group in itertools.groupby(sorted_by_city, key=lambda s: s["city"]):
    students_in_city = list(group)
    city_total = sum(s["fee"] for s in students_in_city)
    print(f"  {city}: {len(students_in_city)} students, ₹{city_total:,}")


print("\n" + "=" * 55)
print("Program complete! You have mastered Async & Generators.")
print("=" * 55)
