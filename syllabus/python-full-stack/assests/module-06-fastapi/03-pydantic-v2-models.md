# Pydantic v2 Models — Data Validation Made Easy

**Module 06 — FastAPI: Modern API Development | Topic 3**

---

## What is Pydantic?

Pydantic is a Python library that validates data using type hints. When a user sends data to your API, Pydantic checks that every field has the correct type, format, and value — before your code even runs.

**Without Pydantic:**
```python
# You manually check everything
def create_student(data):
    if "name" not in data:
        raise ValueError("Name is required")
    if not isinstance(data["name"], str):
        raise ValueError("Name must be a string")
    if len(data["name"]) < 1:
        raise ValueError("Name cannot be empty")
    if "email" not in data:
        raise ValueError("Email is required")
    # ... 20 more checks ...
```

**With Pydantic:**
```python
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
# That's it! Pydantic handles all validation automatically.
```

---

## Basic Models

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Student(BaseModel):
    name: str
    email: str
    age: int
    city: str = "Bhopal"              # Default value
    is_active: bool = True            # Default value
    phone: Optional[str] = None       # Optional field
    joined_at: datetime = datetime.now()
```

### Creating Instances

```python
# From keyword arguments
student = Student(name="Rahul Sharma", email="rahul@email.com", age=22)
print(student.name)       # "Rahul Sharma"
print(student.city)       # "Bhopal" (default)
print(student.phone)      # None (optional, not provided)

# From a dictionary
data = {"name": "Priya Patel", "email": "priya@email.com", "age": 21, "city": "Pune"}
student = Student(**data)
# Or:
student = Student.model_validate(data)
```

### Type Coercion

Pydantic automatically converts compatible types:

```python
# String "22" is automatically converted to int 22
student = Student(name="Amit", email="amit@email.com", age="22")
print(student.age)        # 22 (int, not str)
print(type(student.age))  # <class 'int'>

# But invalid values raise an error
student = Student(name="Amit", email="amit@email.com", age="not a number")
# ValidationError: Input should be a valid integer
```

---

## Field Validation

### Using Field()

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Student's full name",
        examples=["Rahul Sharma"]
    )
    age: int = Field(
        ge=16,           # Greater than or equal
        le=100,          # Less than or equal
        description="Student's age"
    )
    fee_paid: float = Field(
        ge=0,            # Cannot be negative
        default=0.0,
        description="Fee amount paid in INR"
    )
    email: str = Field(
        pattern=r'^[\w.-]+@[\w.-]+\.\w+$',
        description="Valid email address"
    )
```

### Validation Parameters

| Parameter | Type | Meaning |
|-----------|------|---------|
| `min_length` | str | Minimum characters |
| `max_length` | str | Maximum characters |
| `ge` | int/float | >= (greater than or equal) |
| `le` | int/float | <= (less than or equal) |
| `gt` | int/float | > (strictly greater) |
| `lt` | int/float | < (strictly less) |
| `pattern` | str | Regex pattern |
| `default` | any | Default value |
| `description` | str | Shows in API docs |
| `examples` | list | Example values for docs |
| `alias` | str | Alternative field name in input |

---

## Common Field Types

```python
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime, date
from typing import Optional
from enum import Enum

class CourseCategory(str, Enum):
    python = "python"
    web = "web"
    data = "data"

class Course(BaseModel):
    title: str                        # Required string
    price: float                      # Required number
    duration_weeks: int               # Required integer
    category: CourseCategory          # Must be one of the enum values
    is_published: bool = False        # Boolean with default
    website: Optional[HttpUrl] = None # Valid URL or None
    start_date: Optional[date] = None # Date (YYYY-MM-DD)
    tags: list[str] = []              # List of strings
    metadata: dict[str, str] = {}     # Dictionary
```

---

## Nested Models

Models can contain other models:

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str = Field(pattern=r'^\d{6}$')  # 6-digit Indian pincode

class Student(BaseModel):
    name: str
    email: str
    address: Address              # Nested model
    courses: list[str] = []       # List of course names
```

**Input JSON:**
```json
{
    "name": "Rahul Sharma",
    "email": "rahul@email.com",
    "address": {
        "street": "MG Road",
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462001"
    },
    "courses": ["Python", "FastAPI"]
}
```

---

## Custom Validators

### Field Validators

```python
from pydantic import BaseModel, field_validator

class Student(BaseModel):
    name: str
    email: str
    age: int
    phone: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip().title()  # "rahul sharma" → "Rahul Sharma"

    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 16:
            raise ValueError('Student must be at least 16 years old')
        if v > 100:
            raise ValueError('Age seems invalid')
        return v

    @field_validator('phone')
    @classmethod
    def validate_indian_phone(cls, v):
        if v is None:
            return v
        import re
        if not re.match(r'^[6-9]\d{9}$', v):
            raise ValueError('Must be a valid 10-digit Indian mobile number')
        return v
```

### Model Validators (Cross-Field Validation)

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def end_after_start(self):
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self
```

---

## Serialization — Converting Models to Dictionaries/JSON

```python
student = Student(name="Rahul Sharma", email="rahul@email.com", age=22, city="Bhopal")

# Convert to dictionary
data = student.model_dump()
# {"name": "Rahul Sharma", "email": "rahul@email.com", "age": 22, "city": "Bhopal", ...}

# Exclude certain fields
data = student.model_dump(exclude={"phone", "is_active"})

# Include only certain fields
data = student.model_dump(include={"name", "email"})

# Exclude unset fields (useful for partial updates)
data = student.model_dump(exclude_unset=True)

# Convert to JSON string
json_str = student.model_dump_json()
```

### exclude_unset for Partial Updates

```python
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    fee_paid: Optional[float] = None

# Client sends: {"city": "Pune"}
update = StudentUpdate(city="Pune")

# model_dump() includes ALL fields (even None ones)
update.model_dump()
# {"name": None, "email": None, "city": "Pune", "fee_paid": None}

# model_dump(exclude_unset=True) includes ONLY what was sent
update.model_dump(exclude_unset=True)
# {"city": "Pune"}  ← Perfect for partial updates!
```

---

## ConfigDict — Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class StudentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,     # Read from ORM objects (SQLAlchemy)
        str_strip_whitespace=True, # Auto-strip spaces from strings
        str_min_length=1,          # No empty strings by default
    )

    id: int
    name: str
    email: str
    city: str
```

### from_attributes=True

This lets Pydantic read data from ORM objects (like SQLAlchemy models):

```python
# Without from_attributes:
student = db_student  # SQLAlchemy object
response = StudentResponse(
    id=student.id,
    name=student.name,
    email=student.email,
    city=student.city
)

# With from_attributes=True:
response = StudentResponse.model_validate(db_student)  # Automatic!
```

---

## Schema Patterns for APIs

### Separate Create, Update, and Response Schemas

```python
# Base schema (shared fields)
class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    city: str = "Bhopal"

# Create schema (what the client sends when creating)
class StudentCreate(StudentBase):
    password: str = Field(min_length=8)

# Update schema (all fields optional for partial updates)
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    city: Optional[str] = None

# Response schema (what the client receives)
class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    # Note: password is NOT in the response schema
```

This pattern ensures:
- **Create** requires all mandatory fields + password
- **Update** allows partial updates (only changed fields)
- **Response** never exposes the password

---

## Error Handling

When validation fails, FastAPI returns a 422 error with details:

```json
{
    "detail": [
        {
            "type": "value_error",
            "loc": ["body", "email"],
            "msg": "value is not a valid email address",
            "input": "not-an-email"
        },
        {
            "type": "int_parsing",
            "loc": ["body", "age"],
            "msg": "Input should be a valid integer",
            "input": "twenty"
        }
    ]
}
```

The error tells you exactly **which field** failed and **why**.

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| BaseModel | Define data structures with automatic validation |
| Field() | Add constraints like min_length, ge, pattern |
| field_validator | Custom validation logic per field |
| model_validator | Cross-field validation |
| model_dump() | Convert to dictionary |
| exclude_unset=True | Only include fields that were actually sent |
| from_attributes=True | Read from SQLAlchemy ORM objects |
| Separate schemas | Different schemas for Create, Update, Response |

---

*TechPath Institute — Python Full Stack Development*
