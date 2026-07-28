# OOP — Classes & Objects

**Module 02 — Advanced Python | Topic 1**

---

## What is Object-Oriented Programming?

Object-Oriented Programming (OOP) is a way of organizing code around **objects** — bundles of data and behavior. Instead of writing loose functions and variables, you group related things together.

**Real-world analogy:** Think of a class as a **form template** (like an admission form at TechPath Institute). The template defines what information is needed — name, city, course, fee. Each filled-in form is an **object** — a specific student with their own data.

### Why OOP?

| Without OOP | With OOP |
|-------------|----------|
| Variables and functions scattered everywhere | Data and behavior grouped together |
| Hard to manage as code grows | Easy to organize large projects |
| Copy-paste code for similar things | Reuse code with inheritance |
| Difficult to maintain | Change one class, everything updates |

---

## Defining a Class

```python
class Student:
    """Represents a TechPath Institute student."""

    # Class attribute — shared by ALL students
    institute = "TechPath Institute"

    def __init__(self, name, city, course, fee):
        """Constructor — runs when you create a new student."""
        # Instance attributes — unique to each student
        self.name = name
        self.city = city
        self.course = course
        self.fee = fee
        self.marks = []    # Each student has their own marks list

    def add_marks(self, mark):
        """Add a mark for this student."""
        self.marks.append(mark)

    def average(self):
        """Calculate average marks."""
        if not self.marks:
            return 0
        return sum(self.marks) / len(self.marks)

    def display(self):
        """Print student info."""
        print(f"{self.name} ({self.city}) — {self.course}")
        print(f"  Fee: ₹{self.fee:,}")
        if self.marks:
            print(f"  Average: {self.average():.1f}")
```

### Creating Objects (Instances)

```python
# Create two student objects
s1 = Student("Rahul Sharma", "Bhopal", "Python Full Stack", 25000)
s2 = Student("Priya Patel", "Pune", "Web Development", 20000)

# Use methods
s1.add_marks(85)
s1.add_marks(92)
s1.display()
# Rahul Sharma (Bhopal) — Python Full Stack
#   Fee: ₹25,000
#   Average: 88.5

# Access attributes
print(s1.name)          # Rahul Sharma
print(s1.institute)     # TechPath Institute (class attribute)
print(Student.institute) # TechPath Institute (also accessible via class)
```

### self — What Is It?

`self` refers to the **current object**. When you call `s1.add_marks(85)`, Python internally calls `Student.add_marks(s1, 85)` — it passes `s1` as `self`.

```python
class Counter:
    def __init__(self):
        self.count = 0    # 'self' = the specific counter object

    def increment(self):
        self.count += 1   # Modify THIS counter's count

c1 = Counter()
c2 = Counter()
c1.increment()
c1.increment()
print(c1.count)    # 2
print(c2.count)    # 0 — c2 is a separate object
```

---

## Class Attributes vs Instance Attributes

```python
class Course:
    # Class attribute — same for all courses
    institute = "TechPath Institute"
    total_courses = 0

    def __init__(self, name, fee):
        # Instance attributes — different for each course
        self.name = name
        self.fee = fee
        Course.total_courses += 1    # Modify class attribute

c1 = Course("Python Full Stack", 25000)
c2 = Course("Web Development", 20000)

print(Course.total_courses)    # 2
print(c1.institute)           # TechPath Institute
print(c2.institute)           # TechPath Institute
```

| Feature | Class Attribute | Instance Attribute |
|---------|----------------|-------------------|
| Defined in | Class body (outside methods) | Inside `__init__` with `self.` |
| Shared | Yes — all objects share it | No — each object has its own |
| Access | `ClassName.attr` or `self.attr` | `self.attr` only |
| Use case | Constants, counters | Object-specific data |

---

## The __init__ Method (Constructor)

`__init__` is called automatically when you create a new object. It sets up the initial state.

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        """Initialize account with owner name and optional balance."""
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("Amount must be positive!")
            return
        self.balance += amount
        self.transactions.append(f"+₹{amount}")
        print(f"Deposited ₹{amount}. Balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient balance! Available: ₹{self.balance}")
            return
        self.balance -= amount
        self.transactions.append(f"-₹{amount}")
        print(f"Withdrawn ₹{amount}. Balance: ₹{self.balance}")

# Usage
acc = BankAccount("Rahul", 10000)
acc.deposit(5000)      # Deposited ₹5000. Balance: ₹15000
acc.withdraw(3000)     # Withdrawn ₹3000. Balance: ₹12000
acc.withdraw(20000)    # Insufficient balance! Available: ₹12000
```

---

## __str__ and __repr__ — String Representations

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        """Human-readable string (for print, f-strings)."""
        return f"{self.name} — ₹{self.price:,}"

    def __repr__(self):
        """Developer-friendly string (for debugging, REPL)."""
        return f"Product(name='{self.name}', price={self.price})"


laptop = Product("HP Pavilion", 55000)
print(laptop)         # HP Pavilion — ₹55,000  (uses __str__)
print(repr(laptop))   # Product(name='HP Pavilion', price=55000)  (uses __repr__)
print(f"Item: {laptop}")  # Item: HP Pavilion — ₹55,000  (uses __str__)
```

| Method | When Used | Purpose |
|--------|-----------|---------|
| `__str__` | `print()`, `str()`, f-strings | For end users |
| `__repr__` | REPL, `repr()`, debugging | For developers |

---

## @property — Computed Attributes

`@property` lets you access a method like an attribute. Use it when the "attribute" needs calculation or validation.

```python
class Product:
    def __init__(self, name, base_price):
        self.name = name
        self._base_price = base_price    # Convention: _ means "private"

    @property
    def price_with_gst(self):
        """Price including 18% GST."""
        return round(self._base_price * 1.18, 2)

    @property
    def base_price(self):
        return self._base_price

    @base_price.setter
    def base_price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative!")
        self._base_price = value


item = Product("Keyboard", 1500)
print(item.price_with_gst)    # 1770.0  (no parentheses — like an attribute!)
print(item.base_price)         # 1500

item.base_price = 2000         # Uses the setter
print(item.price_with_gst)    # 2360.0

# item.base_price = -500       # ValueError: Price cannot be negative!
```

---

## Common Dunder (Magic) Methods

Dunder = "double underscore". These special methods let your objects work with Python operators and built-in functions.

```python
class Marks:
    def __init__(self, subject, score):
        self.subject = subject
        self.score = score

    def __str__(self):
        return f"{self.subject}: {self.score}"

    def __eq__(self, other):
        """Enable == comparison."""
        return self.score == other.score

    def __lt__(self, other):
        """Enable < comparison (also enables sorting)."""
        return self.score < other.score

    def __add__(self, other):
        """Enable + operator."""
        return Marks("Total", self.score + other.score)

    def __len__(self):
        """Enable len() — return score as 'length'."""
        return self.score


m1 = Marks("Python", 85)
m2 = Marks("Django", 92)

print(m1 == m2)        # False
print(m1 < m2)         # True
total = m1 + m2
print(total)           # Total: 177
print(len(m1))         # 85

# Sorting works because __lt__ is defined
marks = [Marks("Python", 85), Marks("Django", 92), Marks("React", 78)]
marks.sort()
print([str(m) for m in marks])    # ['React: 78', 'Python: 85', 'Django: 92']
```

### Common Dunder Methods Reference

| Method | Operator/Function | Example |
|--------|------------------|---------|
| `__init__` | Constructor | `obj = Class()` |
| `__str__` | `print()`, `str()` | `print(obj)` |
| `__repr__` | `repr()`, REPL | `repr(obj)` |
| `__eq__` | `==` | `a == b` |
| `__lt__` | `<` | `a < b` |
| `__gt__` | `>` | `a > b` |
| `__le__` / `__ge__` | `<=` / `>=` | `a <= b` |
| `__add__` | `+` | `a + b` |
| `__sub__` | `-` | `a - b` |
| `__mul__` | `*` | `a * b` |
| `__len__` | `len()` | `len(obj)` |
| `__getitem__` | `obj[key]` | `obj["name"]` |
| `__contains__` | `in` | `x in obj` |
| `__bool__` | `bool()` | `if obj:` |
| `__call__` | `obj()` | `obj()` |

---

## Private and Protected Attributes

Python does not have strict access control, but uses conventions:

| Convention | Meaning | Example |
|------------|---------|---------|
| `name` | Public | `self.name` |
| `_name` | Protected (by convention) | `self._balance` |
| `__name` | Name-mangled (harder to access) | `self.__password` |

```python
class User:
    def __init__(self, name, password):
        self.name = name           # Public
        self._role = "student"     # Protected by convention
        self.__password = password  # Name-mangled

u = User("Rahul", "secret123")
print(u.name)          # Rahul
print(u._role)         # student (accessible but "please don't")
# print(u.__password)  # AttributeError!
print(u._User__password)  # secret123 (name-mangling, avoid this)
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Class | `class MyClass:` | Blueprint for objects |
| Constructor | `def __init__(self):` | Initialize object state |
| Instance attribute | `self.name = value` | Per-object data |
| Class attribute | `name = value` (in class body) | Shared data |
| Method | `def method(self):` | Object behavior |
| `__str__` | `def __str__(self):` | Human-readable string |
| `@property` | `@property` decorator | Computed/validated attributes |
| Private | `self._name` / `self.__name` | Access control convention |

---

## Practice Tasks

1. Create a `Course` class with name, fee, duration, and a method to display course info
2. Create a `BankAccount` class with deposit, withdraw, and transaction history
3. Add `__str__` and `__repr__` to your classes
4. Use `@property` to create a read-only `fee_with_gst` attribute
5. Create a `Student` class that tracks marks and calculates grade using dunder methods
