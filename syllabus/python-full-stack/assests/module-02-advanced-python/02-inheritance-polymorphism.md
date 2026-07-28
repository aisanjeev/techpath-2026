# Inheritance & Polymorphism

**Module 02 — Advanced Python | Topic 2**

---

## What is Inheritance?

Inheritance lets you create a new class based on an existing class. The new class (child) gets all the attributes and methods of the existing class (parent), and can add or override them.

**Real-world analogy:** Think of a general "Vehicle" category. Cars, bikes, and buses are all vehicles — they share common features (wheels, engine, speed) but each has unique features too. In OOP, `Vehicle` is the parent class, and `Car`, `Bike`, `Bus` are child classes.

```
Vehicle (Parent)
├── Car (Child)
├── Bike (Child)
└── Bus (Child)
```

---

## Basic Inheritance

```python
class Person:
    """Base class for all people."""
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def introduce(self):
        return f"Hi, I am {self.name} from {self.city}, age {self.age}"


class Student(Person):
    """Student inherits from Person."""
    def __init__(self, name, city, age, course, fee):
        super().__init__(name, city, age)    # Call parent's __init__
        self.course = course
        self.fee = fee
        self.marks = []

    def add_marks(self, mark):
        self.marks.append(mark)

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0


class Instructor(Person):
    """Instructor inherits from Person."""
    def __init__(self, name, city, age, specialization, experience):
        super().__init__(name, city, age)
        self.specialization = specialization
        self.experience = experience

    def introduce(self):
        """Override parent's introduce method."""
        base = super().introduce()
        return f"{base}\nI teach {self.specialization} ({self.experience} years experience)"


# Usage
s = Student("Rahul", "Bhopal", 22, "Python Full Stack", 25000)
print(s.introduce())    # Uses Person's introduce (inherited)
# Hi, I am Rahul from Bhopal, age 22

i = Instructor("Sneha", "Delhi", 30, "Python", 5)
print(i.introduce())    # Uses Instructor's introduce (overridden)
# Hi, I am Sneha from Delhi, age 30
# I teach Python (5 years experience)
```

### super() — Call the Parent

`super()` gives you access to the parent class. Use it to:
1. Call the parent's `__init__` (most common)
2. Extend a parent method without rewriting it

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)    # Call Animal.__init__
        self.breed = breed

    def speak(self):
        return f"{self.name} says: Woof!"

dog = Dog("Bruno", "Labrador")
print(dog.speak())    # Bruno says: Woof!
```

---

## isinstance() and issubclass()

```python
s = Student("Priya", "Pune", 21, "Web Dev", 20000)

print(isinstance(s, Student))    # True
print(isinstance(s, Person))     # True (Student IS a Person)
print(isinstance(s, Instructor)) # False

print(issubclass(Student, Person))      # True
print(issubclass(Person, Student))      # False
```

---

## Method Resolution Order (MRO)

When a class inherits from multiple parents, Python needs to decide which method to use. The MRO defines this order.

```python
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.greet())    # Hello from B

# Check the MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

Python follows the **C3 Linearization** algorithm: it goes left to right through parent classes, depth-first, but never visits a class before all its children.

**Simple rule:** In `class D(B, C)`, Python checks D first, then B, then C, then A.

---

## Multiple Inheritance

A class can inherit from more than one parent:

```python
class Printable:
    def to_string(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class Saveable:
    def to_dict(self):
        return self.__dict__.copy()

class Student(Printable, Saveable):
    def __init__(self, name, course):
        self.name = name
        self.course = course

s = Student("Amit", "Python Full Stack")
print(s.to_string())    # Student(name=Amit, course=Python Full Stack)
print(s.to_dict())      # {'name': 'Amit', 'course': 'Python Full Stack'}
```

---

## Abstract Base Classes (ABC)

An abstract class is a blueprint that **cannot be instantiated** directly. It forces child classes to implement certain methods.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def area(self):
        """Every shape MUST implement area()."""
        pass

    @abstractmethod
    def perimeter(self):
        """Every shape MUST implement perimeter()."""
        pass

    def describe(self):
        """Concrete method — inherited as-is."""
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


# shape = Shape()    # TypeError! Cannot instantiate abstract class
rect = Rectangle(10, 5)
circ = Circle(7)

print(rect.describe())    # Rectangle: area=50.00, perimeter=30.00
print(circ.describe())    # Circle: area=153.94, perimeter=43.98
```

---

## Polymorphism — One Interface, Many Forms

Polymorphism means the same method name works differently for different classes.

```python
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class UPI(PaymentMethod):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        return f"Paid ₹{amount:,} via UPI ({self.upi_id})"

class CreditCard(PaymentMethod):
    def __init__(self, card_number):
        self.card_last4 = card_number[-4:]

    def pay(self, amount):
        return f"Paid ₹{amount:,} via Credit Card (****{self.card_last4})"

class NetBanking(PaymentMethod):
    def __init__(self, bank):
        self.bank = bank

    def pay(self, amount):
        return f"Paid ₹{amount:,} via Net Banking ({self.bank})"

# Polymorphism in action — same .pay() method, different behavior
methods = [
    UPI("rahul@upi"),
    CreditCard("4111222233334444"),
    NetBanking("SBI"),
]

for method in methods:
    print(method.pay(25000))

# Paid ₹25,000 via UPI (rahul@upi)
# Paid ₹25,000 via Credit Card (****4444)
# Paid ₹25,000 via Net Banking (SBI)
```

---

## Mixins — Reusable Behavior Blocks

A mixin is a small class that provides specific behavior. It is not meant to be used alone — you mix it into other classes.

```python
import json
from datetime import datetime

class TimestampMixin:
    """Adds created_at timestamp to any class."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def set_timestamp(self):
        self.created_at = datetime.now().isoformat()

class JsonMixin:
    """Adds JSON serialization to any class."""
    def to_json(self):
        return json.dumps(self.__dict__, indent=2, default=str)

class LogMixin:
    """Adds logging capability."""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class Student(TimestampMixin, JsonMixin, LogMixin):
    def __init__(self, name, course):
        self.name = name
        self.course = course
        self.set_timestamp()

s = Student("Priya", "Python Full Stack")
s.log("Student created")         # [Student] Student created
print(s.to_json())
# {
#   "name": "Priya",
#   "course": "Python Full Stack",
#   "created_at": "2026-07-25T10:30:00"
# }
```

---

## Composition vs Inheritance

Sometimes it is better to **have** something than to **be** something.

```python
# Inheritance: Student IS a Person
class Student(Person):
    pass

# Composition: Student HAS an Address
class Address:
    def __init__(self, street, city, pincode):
        self.street = street
        self.city = city
        self.pincode = pincode

    def full_address(self):
        return f"{self.street}, {self.city} - {self.pincode}"

class Student:
    def __init__(self, name, address):
        self.name = name
        self.address = address    # Composition — Student HAS an Address

addr = Address("MP Nagar", "Bhopal", "462011")
s = Student("Rahul", addr)
print(s.address.full_address())    # MP Nagar, Bhopal - 462011
```

| Use | When |
|-----|------|
| Inheritance | "is-a" relationship (Student is a Person) |
| Composition | "has-a" relationship (Student has an Address) |

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Inheritance | `class Child(Parent):` | Reuse parent's code |
| `super()` | `super().__init__()` | Call parent's method |
| MRO | `Class.__mro__` | Method lookup order |
| Abstract class | `class X(ABC):` + `@abstractmethod` | Force child implementation |
| Polymorphism | Same method name, different behavior | Flexible code |
| Mixin | Multiple small parent classes | Reusable behaviors |
| Composition | `self.obj = OtherClass()` | "has-a" relationships |

---

## Practice Tasks

1. Create `Animal`, `Dog`, `Cat` classes with inheritance and override `speak()`
2. Create an abstract `Shape` class with `Rectangle`, `Circle`, `Triangle` implementations
3. Build a payment system using polymorphism (UPI, card, cash)
4. Create a `JsonMixin` and `LogMixin` and mix them into a `Student` class
5. Refactor a class hierarchy to use composition instead of inheritance
