# Testing with pytest

**Module 02 — Advanced Python | Topic 8**

---

## Why Test?

Testing ensures your code works correctly and keeps working when you make changes. Without tests, you are guessing that your code is correct.

**Real-world analogy:** Would you buy a car that has never been test-driven? Would you take a medicine that has never been tested? Your code deserves the same quality assurance.

### Types of Tests

| Type | What It Tests | Speed | Example |
|------|--------------|-------|---------|
| **Unit test** | A single function or method | Very fast | Test `calculate_fee()` |
| **Integration test** | Multiple components together | Medium | Test API endpoint with database |
| **End-to-end (E2E)** | Full user flow | Slow | Test complete enrollment flow |

We focus on **unit testing** with pytest — the most popular Python testing framework.

---

## Getting Started with pytest

### Installation

```bash
pip install pytest
```

### Your First Test

Create a file called `test_math.py`:

```python
# test_math.py
def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(5, 0) == 5
```

Run the tests:

```bash
pytest test_math.py
```

Output:

```
=================== test session starts ===================
test_math.py ...                                     [100%]
=================== 3 passed in 0.01s ====================
```

### Naming Conventions

| What | Convention |
|------|-----------|
| Test files | Start with `test_` or end with `_test.py` |
| Test functions | Start with `test_` |
| Test classes | Start with `Test` |
| Assert | Use `assert` statements |

---

## assert — The Heart of Testing

```python
# Basic assertions
assert 1 + 1 == 2                    # Equality
assert "Rahul" != "Priya"            # Inequality
assert 85 > 60                       # Greater than
assert 42 in [10, 42, 73]            # Membership
assert isinstance("hello", str)      # Type check
assert not False                     # Negation

# With message (shown on failure)
marks = 45
assert marks >= 60, f"Expected pass mark, got {marks}"
```

---

## Testing Real Functions

### File Structure

```
my-project/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   └── student.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_student.py
└── pytest.ini
```

### Example: Testing a Fee Calculator

```python
# app/calculator.py
def calculate_fee(base_price: float, gst_rate: float = 0.18) -> float:
    """Calculate total fee including GST."""
    if base_price < 0:
        raise ValueError("Base price cannot be negative")
    return round(base_price * (1 + gst_rate), 2)

def apply_discount(price: float, discount_percent: float) -> float:
    """Apply percentage discount."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(price * (1 - discount_percent / 100), 2)

def get_grade(marks: float) -> str:
    """Get grade based on marks."""
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    if marks >= 60: return "C"
    return "F"
```

```python
# tests/test_calculator.py
import pytest
from app.calculator import calculate_fee, apply_discount, get_grade

class TestCalculateFee:
    def test_basic_calculation(self):
        assert calculate_fee(1000) == 1180.0

    def test_custom_gst_rate(self):
        assert calculate_fee(1000, gst_rate=0.12) == 1120.0

    def test_zero_price(self):
        assert calculate_fee(0) == 0.0

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            calculate_fee(-500)

class TestApplyDiscount:
    def test_ten_percent_discount(self):
        assert apply_discount(25000, 10) == 22500.0

    def test_no_discount(self):
        assert apply_discount(25000, 0) == 25000.0

    def test_full_discount(self):
        assert apply_discount(25000, 100) == 0.0

    def test_invalid_discount_raises_error(self):
        with pytest.raises(ValueError):
            apply_discount(25000, 150)

class TestGetGrade:
    def test_grade_a_plus(self):
        assert get_grade(95) == "A+"

    def test_grade_a(self):
        assert get_grade(85) == "A"

    def test_grade_f(self):
        assert get_grade(45) == "F"

    def test_boundary_pass(self):
        assert get_grade(60) == "C"

    def test_boundary_fail(self):
        assert get_grade(59) == "F"
```

---

## Fixtures — Setup and Teardown

Fixtures provide reusable test data and setup/cleanup logic.

```python
import pytest

@pytest.fixture
def sample_student():
    """Provide a sample student dictionary."""
    return {
        "name": "Rahul Sharma",
        "city": "Bhopal",
        "course": "Python Full Stack",
        "fee": 25000,
        "marks": [85, 92, 78, 88],
    }

@pytest.fixture
def empty_student():
    return {
        "name": "New Student",
        "city": "",
        "course": "",
        "fee": 0,
        "marks": [],
    }

def test_student_has_name(sample_student):
    assert sample_student["name"] == "Rahul Sharma"

def test_student_marks_average(sample_student):
    avg = sum(sample_student["marks"]) / len(sample_student["marks"])
    assert avg == 85.75

def test_empty_student_no_marks(empty_student):
    assert len(empty_student["marks"]) == 0
```

### Fixture Scope

```python
@pytest.fixture(scope="function")    # Default — new for each test
def per_test_data():
    return {"counter": 0}

@pytest.fixture(scope="module")      # Shared across all tests in file
def database_connection():
    conn = create_connection()
    yield conn           # yield = setup + teardown
    conn.close()         # Cleanup after all tests

@pytest.fixture(scope="session")     # Shared across all test files
def app_config():
    return load_config()
```

### Fixture with Teardown

```python
import json
from pathlib import Path

@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary JSON file for testing."""
    file_path = tmp_path / "test_data.json"
    data = [
        {"name": "Rahul", "marks": 85},
        {"name": "Priya", "marks": 92},
    ]
    file_path.write_text(json.dumps(data))
    yield file_path    # Test runs here
    # Cleanup is automatic — tmp_path is removed after test
```

---

## @pytest.mark.parametrize — Test Multiple Inputs

Instead of writing separate tests for each input, use parametrize:

```python
import pytest
from app.calculator import get_grade

@pytest.mark.parametrize("marks, expected_grade", [
    (95, "A+"),
    (90, "A+"),
    (89, "A"),
    (80, "A"),
    (79, "B"),
    (70, "B"),
    (69, "C"),
    (60, "C"),
    (59, "F"),
    (0, "F"),
])
def test_get_grade(marks, expected_grade):
    assert get_grade(marks) == expected_grade
```

This generates 10 separate tests from one function!

### Parametrize with IDs

```python
@pytest.mark.parametrize("base, gst, expected", [
    pytest.param(1000, 0.18, 1180.0, id="standard-gst"),
    pytest.param(1000, 0.12, 1120.0, id="reduced-gst"),
    pytest.param(1000, 0.05, 1050.0, id="minimal-gst"),
    pytest.param(0, 0.18, 0.0, id="zero-price"),
])
def test_calculate_fee(base, gst, expected):
    assert calculate_fee(base, gst) == expected
```

---

## Mocking — Fake External Dependencies

Use `unittest.mock` to replace external dependencies (APIs, databases, files) with fake implementations.

```python
from unittest.mock import patch, MagicMock
import pytest

# Function that calls an external API
def get_student_from_api(student_id):
    import requests
    response = requests.get(f"https://api.techpath.com/students/{student_id}")
    if response.status_code == 200:
        return response.json()
    return None

# Test with mocking — no real API call
@patch("requests.get")
def test_get_student_success(mock_get):
    # Setup the mock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Rahul", "city": "Bhopal"}
    mock_get.return_value = mock_response

    # Call the function
    result = get_student_from_api("TP-001")

    # Verify
    assert result["name"] == "Rahul"
    mock_get.assert_called_once_with("https://api.techpath.com/students/TP-001")

@patch("requests.get")
def test_get_student_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_student_from_api("TP-999")
    assert result is None
```

---

## Testing Exceptions

```python
import pytest

def test_negative_fee_raises_error():
    with pytest.raises(ValueError) as exc_info:
        calculate_fee(-500)
    
    assert "cannot be negative" in str(exc_info.value)
    assert exc_info.type == ValueError

def test_invalid_type_raises_error():
    with pytest.raises(TypeError):
        calculate_fee("not a number")
```

---

## Coverage — How Much Code Is Tested?

```bash
pip install pytest-cov
pytest --cov=app tests/
```

Output:

```
---------- coverage: platform win32, python 3.12.4 ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py             0      0   100%
app/calculator.py          15      0   100%
app/student.py             25      3    88%
-------------------------------------------
TOTAL                      40      3    93%
```

Generate HTML coverage report:

```bash
pytest --cov=app --cov-report=html tests/
# Open htmlcov/index.html in browser
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::test_basic_calculation

# Run specific class
pytest tests/test_calculator.py::TestCalculateFee

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print output
pytest -s

# Run only failed tests from last run
pytest --lf

# Run tests matching a keyword
pytest -k "grade"
```

---

## pytest.ini — Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks test as slow
    integration: marks test as integration test
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Test function | `def test_name():` | Define a test |
| Assert | `assert x == y` | Check expected result |
| `pytest.raises` | `with pytest.raises(Error):` | Test exceptions |
| Fixture | `@pytest.fixture` | Reusable test setup |
| Parametrize | `@pytest.mark.parametrize` | Test multiple inputs |
| Mock | `@patch("module.func")` | Fake external dependencies |
| Coverage | `pytest --cov=app` | Check test coverage |

---

## Practice Tasks

1. Write tests for a `calculate_bmi()` function with edge cases
2. Use `@pytest.mark.parametrize` to test grade boundaries
3. Create a fixture that provides a list of sample students
4. Mock an API call and test both success and failure cases
5. Achieve 100% coverage on a small module
