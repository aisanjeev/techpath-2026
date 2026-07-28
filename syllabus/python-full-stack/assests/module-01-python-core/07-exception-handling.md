# Exception Handling

**Module 01 — Python Core: Language Fundamentals | Topic 7**

---

## What are Exceptions?

An exception is an error that happens while your program is running. Without handling, exceptions crash your program with an ugly error message.

**Real-world analogy:** Imagine you are withdrawing money from an ATM. What if there is no money in the machine? What if you enter a wrong PIN? The ATM does not crash — it shows a friendly error message. That is exception handling.

```python
# This will crash!
number = int("hello")    # ValueError: invalid literal for int()
```

### Common Exception Types

| Exception | When It Happens | Example |
|-----------|----------------|---------|
| `ValueError` | Wrong value type | `int("hello")` |
| `TypeError` | Wrong data type in operation | `"5" + 3` |
| `NameError` | Variable not defined | `print(xyz)` |
| `IndexError` | List index out of range | `[1,2,3][5]` |
| `KeyError` | Dict key not found | `{"a": 1}["b"]` |
| `ZeroDivisionError` | Division by zero | `10 / 0` |
| `FileNotFoundError` | File does not exist | `open("missing.txt")` |
| `AttributeError` | Object has no attribute | `"hello".append("!")` |
| `ImportError` | Module not found | `import nonexistent` |

---

## try / except — Catching Exceptions

The `try` block contains code that might fail. The `except` block handles the error gracefully.

```python
try:
    age = int(input("Enter your age: "))
    print(f"You are {age} years old")
except ValueError:
    print("Please enter a valid number!")
```

### Catching Multiple Exceptions

```python
try:
    marks = [85, 92, 78]
    index = int(input("Enter index (0-2): "))
    print(f"Marks: {marks[index]}")
except ValueError:
    print("Please enter a number!")
except IndexError:
    print("Index out of range! Use 0, 1, or 2.")
```

### Catching Multiple Exceptions in One Line

```python
try:
    result = 10 / int(input("Enter a number: "))
except (ValueError, ZeroDivisionError) as e:
    print(f"Error: {e}")
```

### Catching All Exceptions (Use Carefully)

```python
try:
    # Some risky operation
    result = 10 / 0
except Exception as e:
    print(f"Something went wrong: {e}")
    print(f"Error type: {type(e).__name__}")
```

**Warning:** Avoid bare `except:` (without specifying the exception type) in production code — it catches everything, including keyboard interrupts, making it hard to debug.

---

## try / except / else / finally

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found! Creating a new one...")
    content = ""
else:
    # Runs ONLY if no exception occurred
    print(f"File loaded: {len(content)} characters")
finally:
    # ALWAYS runs — exception or not
    print("Operation complete.")
```

### Flow Chart

```
try block
    ├── Exception occurs → except block → finally block
    └── No exception     → else block   → finally block
```

### When to Use Each

| Block | When It Runs | Use For |
|-------|-------------|---------|
| `try` | Always (first) | Code that might fail |
| `except` | Only if exception occurs | Handle the error |
| `else` | Only if NO exception | Code that depends on try succeeding |
| `finally` | ALWAYS | Cleanup (close files, connections) |

---

## Real-World Examples

### Safe Number Input

```python
def get_number(prompt):
    """Keep asking until user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")

# Usage
fee = get_number("Enter course fee (in ₹): ")
print(f"Fee: ₹{fee}")
```

### Safe Dictionary Access

```python
student = {"name": "Rahul", "city": "Bhopal"}

# Without exception handling — crashes if key missing
# print(student["email"])    # KeyError!

# Option 1: try/except
try:
    email = student["email"]
except KeyError:
    email = "Not provided"

# Option 2: .get() method (better for dicts)
email = student.get("email", "Not provided")
```

### Safe File Reading

```python
def read_config(filepath):
    """Read a config file safely."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Config file '{filepath}' not found!")
        return None
    except PermissionError:
        print(f"No permission to read '{filepath}'")
        return None
```

### Safe Division

```python
def safe_divide(a, b):
    """Divide two numbers safely."""
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Both arguments must be numbers"

print(safe_divide(10, 3))      # 3.333...
print(safe_divide(10, 0))      # Cannot divide by zero
print(safe_divide(10, "a"))    # Both arguments must be numbers
```

---

## Raising Exceptions

Use `raise` to throw an exception when something is wrong:

```python
def enroll_student(name, age):
    """Enroll a student with age validation."""
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    if age < 16:
        raise ValueError("Student must be at least 16 years old")
    if age > 60:
        raise ValueError("Student must be under 60 years old")
    
    print(f"Enrolled {name} (age {age}) successfully!")

# Valid
enroll_student("Rahul", 22)    # Enrolled Rahul (age 22) successfully!

# Invalid
try:
    enroll_student("Priya", 14)
except ValueError as e:
    print(f"Enrollment failed: {e}")
    # Enrollment failed: Student must be at least 16 years old
```

### Re-raising Exceptions

Sometimes you want to log an error but still let it propagate:

```python
def process_payment(amount):
    try:
        # Simulate payment processing
        if amount <= 0:
            raise ValueError("Amount must be positive")
        print(f"Processing ₹{amount}...")
    except ValueError:
        print("Logging error...")    # Log it
        raise                        # Re-raise the same exception
```

---

## Custom Exceptions

Create your own exception classes for specific errors in your application:

```python
class TechPathError(Exception):
    """Base exception for TechPath application."""
    pass

class EnrollmentError(TechPathError):
    """Raised when enrollment fails."""
    pass

class PaymentError(TechPathError):
    """Raised when payment fails."""
    def __init__(self, amount, reason):
        self.amount = amount
        self.reason = reason
        super().__init__(f"Payment of ₹{amount} failed: {reason}")

# Using custom exceptions
def process_enrollment(name, fee_paid, total_fee):
    if fee_paid < total_fee:
        raise PaymentError(
            amount=fee_paid,
            reason=f"Insufficient amount. Need ₹{total_fee - fee_paid} more."
        )
    print(f"{name} enrolled successfully!")

try:
    process_enrollment("Amit", 15000, 25000)
except PaymentError as e:
    print(f"Error: {e}")
    print(f"Amount paid: ₹{e.amount}")
    # Error: Payment of ₹15000 failed: Insufficient amount. Need ₹10000 more.
    # Amount paid: ₹15000
```

### Exception Hierarchy for a Project

```python
class AppError(Exception):
    """Base exception for the application."""
    pass

class ValidationError(AppError):
    """Invalid input data."""
    pass

class NotFoundError(AppError):
    """Resource not found."""
    pass

class AuthenticationError(AppError):
    """Authentication failed."""
    pass

class AuthorizationError(AppError):
    """User not authorized."""
    pass
```

---

## Best Practices

### Do: Be Specific

```python
# Good — catches only the expected error
try:
    value = int(user_input)
except ValueError:
    print("Please enter a number")

# Bad — catches everything, hides bugs
try:
    value = int(user_input)
except:
    print("Something went wrong")
```

### Do: Use else for Success Logic

```python
# Good
try:
    data = load_file("config.json")
except FileNotFoundError:
    data = default_config()
else:
    print("Config loaded successfully")

# Less clear
try:
    data = load_file("config.json")
    print("Config loaded successfully")    # This is in the try block
except FileNotFoundError:
    data = default_config()
```

### Do: Use finally for Cleanup

```python
connection = None
try:
    connection = connect_to_database()
    data = connection.query("SELECT * FROM students")
except ConnectionError:
    print("Database connection failed")
finally:
    if connection:
        connection.close()    # Always close the connection
```

### Do: Use Context Managers (with) When Possible

```python
# Instead of try/finally for files, use 'with'
with open("data.txt", "r") as f:
    content = f.read()
# File is automatically closed, even if an exception occurs
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| `try/except` | `try: ... except Error:` | Catch and handle errors |
| `else` | `else:` after except | Runs if no exception |
| `finally` | `finally:` | Always runs (cleanup) |
| `raise` | `raise ValueError("msg")` | Throw an exception |
| Custom exceptions | `class MyError(Exception)` | Application-specific errors |
| `as e` | `except ValueError as e` | Access error message |

---

## Practice Tasks

1. Write a function that safely divides two numbers (handle ZeroDivisionError and TypeError)
2. Create a "safe input" function that keeps asking until the user enters a valid integer
3. Create a custom `InvalidAgeError` exception and use it in a student registration function
4. Write a function that reads a JSON file and handles FileNotFoundError and json.JSONDecodeError
5. Create a mini banking system where withdrawing more than the balance raises an `InsufficientFundsError`
