"""
TechPath Institute — Advanced Python: OOP & Decorators
========================================================
Covers classes, inheritance, abstract classes, properties,
dunder methods, and decorators with Indian-context examples.

Run this file:  python code-oop-and-decorators.py
"""

from abc import ABC, abstractmethod
import time
import functools


# ──────────────────────────────────────────────
# 1. CLASSES & OBJECTS
# ──────────────────────────────────────────────

print("=" * 55)
print("1. CLASSES & OBJECTS")
print("=" * 55)


class Student:
    """Represents a TechPath Institute student."""

    # Class attribute — shared by all instances
    institute = "TechPath Institute"
    _count = 0

    def __init__(self, name, city, course, fee):
        self.name = name
        self.city = city
        self.course = course
        self._fee = fee  # "Private" by convention
        self._marks = []
        Student._count += 1

    def add_marks(self, *marks):
        """Add one or more marks."""
        self._marks.extend(marks)

    @property
    def fee(self):
        """Read-only access to fee."""
        return self._fee

    @property
    def average(self):
        """Calculated property — average marks."""
        if not self._marks:
            return 0.0
        return sum(self._marks) / len(self._marks)

    @property
    def grade(self):
        """Grade based on average marks."""
        avg = self.average
        if avg >= 90:
            return "A+"
        elif avg >= 75:
            return "A"
        elif avg >= 60:
            return "B"
        elif avg >= 40:
            return "C"
        return "Fail"

    def __str__(self):
        return f"{self.name} ({self.city}) — {self.course}"

    def __repr__(self):
        return f"Student(name='{self.name}', city='{self.city}')"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.name == other.name and self.course == other.course

    def __lt__(self, other):
        """Sort students by average marks (descending)."""
        return self.average > other.average  # Higher marks = first

    @classmethod
    def total_enrolled(cls):
        return cls._count

    @classmethod
    def from_dict(cls, data):
        """Create a Student from a dictionary."""
        return cls(data["name"], data["city"], data["course"], data["fee"])

    @staticmethod
    def is_passing(marks):
        """Check if given marks are passing (>= 40)."""
        return marks >= 40


# Creating students
s1 = Student("Rahul Sharma", "Bhopal", "Python Full Stack", 25000)
s2 = Student("Priya Patel", "Pune", "Web Development", 20000)
s3 = Student.from_dict({"name": "Amit Kumar", "city": "Delhi", "course": "Data Science", "fee": 30000})

s1.add_marks(85, 92, 78)
s2.add_marks(95, 88, 91)
s3.add_marks(72, 68, 75)

print(f"Student: {s1}")
print(f"Fee: ₹{s1.fee:,}")
print(f"Average: {s1.average:.1f} → Grade: {s1.grade}")
print(f"Is 35 passing? {Student.is_passing(35)}")
print(f"Total enrolled: {Student.total_enrolled()}")

# Sorting (uses __lt__)
students = [s1, s2, s3]
students.sort()
print("\nRanking:")
for rank, s in enumerate(students, 1):
    print(f"  {rank}. {s.name} — Avg: {s.average:.1f} ({s.grade})")


# ──────────────────────────────────────────────
# 2. INHERITANCE & MRO
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("2. INHERITANCE & MRO")
print("=" * 55)


class Person:
    """Base class for all people at TechPath."""

    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def introduce(self):
        return f"Hi, I am {self.name}, age {self.age}, from {self.city}"


class Trainee(Person):
    """A student/trainee at TechPath."""

    def __init__(self, name, age, city, course):
        super().__init__(name, age, city)
        self.course = course

    def introduce(self):
        return f"{super().introduce()}, studying {self.course}"


class Trainer(Person):
    """A trainer/instructor at TechPath."""

    def __init__(self, name, age, city, subject, experience_years):
        super().__init__(name, age, city)
        self.subject = subject
        self.experience = experience_years

    def introduce(self):
        return f"{super().introduce()}, teaching {self.subject} ({self.experience} yrs exp)"


trainee = Trainee("Ananya Verma", 20, "Bhopal", "Python")
trainer = Trainer("Vikram Sir", 35, "Delhi", "Python", 10)

print(trainee.introduce())
print(trainer.introduce())
print(f"\nTrainee is a Person? {isinstance(trainee, Person)}")
print(f"Trainer is a Trainee? {isinstance(trainer, Trainee)}")


# ──────────────────────────────────────────────
# 3. ABSTRACT CLASSES & MIXINS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("3. ABSTRACT CLASSES & MIXINS")
print("=" * 55)


class PaymentGateway(ABC):
    """Abstract base class for payment processing."""

    @abstractmethod
    def process(self, amount):
        pass

    @abstractmethod
    def refund(self, transaction_id):
        pass

    def receipt(self, amount, method):
        """Concrete method shared by all subclasses."""
        return f"Receipt: ₹{amount:,.2f} via {method}"


class UPIPayment(PaymentGateway):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def process(self, amount):
        return f"₹{amount:,} sent via UPI ({self.upi_id})"

    def refund(self, transaction_id):
        return f"UPI refund initiated for #{transaction_id}"


class CardPayment(PaymentGateway):
    def __init__(self, card_last_four):
        self.card = card_last_four

    def process(self, amount):
        return f"₹{amount:,} charged to card ending {self.card}"

    def refund(self, transaction_id):
        return f"Card refund initiated for #{transaction_id}"


upi = UPIPayment("rahul@paytm")
card = CardPayment("4567")

print(upi.process(25000))
print(card.process(25000))
print(upi.receipt(25000, "UPI"))

# Cannot instantiate abstract class
try:
    gw = PaymentGateway()
except TypeError as e:
    print(f"\nCannot create abstract class: {e}")

# Mixin example
class LoggingMixin:
    """Adds logging capability to any class."""
    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")


class AuditablePayment(UPIPayment, LoggingMixin):
    def process(self, amount):
        result = super().process(amount)
        self.log(f"Processed payment of ₹{amount:,}")
        return result


auditable = AuditablePayment("priya@gpay")
print(f"\n{auditable.process(15000)}")

# Show MRO
print(f"\nMRO: {[c.__name__ for c in AuditablePayment.__mro__]}")


# ──────────────────────────────────────────────
# 4. DUNDER METHODS — CUSTOM CONTAINER
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("4. DUNDER METHODS — CUSTOM CONTAINER")
print("=" * 55)


class CourseCart:
    """A shopping cart of courses with dunder methods."""

    def __init__(self):
        self._items = []

    def add(self, course_name, price):
        self._items.append({"course": course_name, "price": price})

    def __len__(self):
        return len(self._items)

    def __contains__(self, course_name):
        return any(item["course"] == course_name for item in self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def __add__(self, other):
        """Merge two carts."""
        new_cart = CourseCart()
        new_cart._items = self._items + other._items
        return new_cart

    @property
    def total(self):
        return sum(item["price"] for item in self._items)

    def __str__(self):
        lines = [f"Cart ({len(self)} items, Total: ₹{self.total:,}):"]
        for item in self._items:
            lines.append(f"  - {item['course']}: ₹{item['price']:,}")
        return "\n".join(lines)


cart1 = CourseCart()
cart1.add("Python Full Stack", 25000)
cart1.add("Web Development", 20000)

cart2 = CourseCart()
cart2.add("Data Science", 30000)

print(cart1)
print(f"\nItems in cart: {len(cart1)}")
print(f"Python in cart? {'Python Full Stack' in cart1}")
print(f"First item: {cart1[0]}")

merged = cart1 + cart2
print(f"\nMerged cart total: ₹{merged.total:,}")

print("\nIterating over merged cart:")
for item in merged:
    print(f"  {item['course']} — ₹{item['price']:,}")


# ──────────────────────────────────────────────
# 5. DECORATORS
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("5. DECORATORS")
print("=" * 55)


# Timer decorator
def timer(func):
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed:.4f}s")
        return result
    return wrapper


# Retry decorator
def retry(max_attempts=3):
    """Retry a function up to max_attempts times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator


# Validate decorator
def validate_positive(func):
    """Ensure all numeric arguments are positive."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Negative value not allowed: {arg}")
        return func(*args, **kwargs)
    return wrapper


@timer
def compute_squares(n):
    """Compute sum of squares up to n."""
    return sum(i ** 2 for i in range(n))


@validate_positive
def calculate_emi(principal, rate, months):
    """Calculate monthly EMI."""
    monthly_rate = rate / 12 / 100
    emi = principal * monthly_rate * (1 + monthly_rate) ** months
    emi /= ((1 + monthly_rate) ** months - 1)
    return round(emi, 2)


print("Timer decorator:")
result = compute_squares(1_000_000)
print(f"  Result: {result:,}")

print("\nValidate decorator:")
try:
    emi = calculate_emi(25000, 12, 6)
    print(f"  EMI for ₹25,000 at 12% for 6 months: ₹{emi:,}")
except ValueError as e:
    print(f"  Error: {e}")

try:
    calculate_emi(-5000, 12, 6)
except ValueError as e:
    print(f"  Error: {e}")


# Stacking decorators
@timer
@validate_positive
def fee_with_gst(base_fee, gst_rate):
    """Calculate fee with GST."""
    return round(base_fee * (1 + gst_rate / 100), 2)


print("\nStacked decorators (timer + validate):")
result = fee_with_gst(25000, 18)
print(f"  ₹25,000 + 18% GST = ₹{result:,}")


# Retry decorator
import random

@retry(max_attempts=3)
def unreliable_api_call():
    """Simulate an API call that sometimes fails."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Server timeout")
    return {"status": "success", "data": "Student list fetched"}


print("\nRetry decorator:")
try:
    result = unreliable_api_call()
    print(f"  Success: {result}")
except ConnectionError:
    print("  All attempts failed!")


# ──────────────────────────────────────────────
# 6. DATACLASSES
# ──────────────────────────────────────────────

print("\n" + "=" * 55)
print("6. DATACLASSES")
print("=" * 55)

from dataclasses import dataclass, field


@dataclass
class Course:
    name: str
    duration_months: int
    fee: float
    tags: list[str] = field(default_factory=list)

    @property
    def fee_per_month(self):
        return round(self.fee / self.duration_months, 2)

    @property
    def fee_with_gst(self):
        return round(self.fee * 1.18, 2)


@dataclass
class Enrollment:
    student_name: str
    course: Course
    city: str
    discount_percent: float = 0

    @property
    def final_fee(self):
        base = self.course.fee_with_gst
        return round(base * (1 - self.discount_percent / 100), 2)


python_course = Course("Python Full Stack", 6, 25000, ["python", "web", "backend"])
web_course = Course("Web Development", 4, 20000, ["html", "css", "javascript"])

enrollment = Enrollment("Rahul Sharma", python_course, "Bhopal", discount_percent=10)

print(f"Course: {python_course}")
print(f"Fee per month: ₹{python_course.fee_per_month:,}")
print(f"Fee with GST: ₹{python_course.fee_with_gst:,}")
print(f"\nEnrollment: {enrollment.student_name}")
print(f"Final fee (after 10% discount): ₹{enrollment.final_fee:,}")

# Auto-generated __eq__
python2 = Course("Python Full Stack", 6, 25000)
print(f"\nSame course? {python_course.name == python2.name}")


print("\n" + "=" * 55)
print("Program complete! You have mastered OOP & Decorators.")
print("=" * 55)
