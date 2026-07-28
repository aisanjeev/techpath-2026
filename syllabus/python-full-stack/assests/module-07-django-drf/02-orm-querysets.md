# Django ORM & QuerySets

**Module 07 — Django & Django REST Framework | Topic 2**

---

## What is an ORM?

ORM stands for **Object-Relational Mapping**. It lets you interact with your database using Python code instead of writing raw SQL queries.

**Analogy:** Imagine you want to order food at a restaurant in Delhi. You do not go into the kitchen yourself — you tell the waiter what you want, and the waiter handles everything in the kitchen. Similarly, the ORM is your waiter. You write Python code (your order), and the ORM converts it into SQL queries (kitchen operations) behind the scenes.

| Without ORM (Raw SQL) | With ORM (Django) |
|----------------------|-------------------|
| `SELECT * FROM students WHERE city='Bhopal';` | `Student.objects.filter(city='Bhopal')` |
| You must know SQL syntax | You write Python code |
| Database-specific (MySQL vs PostgreSQL differences) | Same code works with any database |
| Prone to SQL injection attacks | Automatically safe from SQL injection |

---

## Defining Models

A model is a Python class that represents a database table. Each attribute of the class represents a column in the table.

### Student and Course Example

We will use a college management system throughout this topic. Let us define our models:

```python
# students/models.py
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    enrolled_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
```

### Common Field Types

| Field Type | Python Type | Example Usage |
|-----------|-------------|---------------|
| `CharField(max_length=N)` | `str` | Name, city, status |
| `TextField()` | `str` | Long descriptions, bio |
| `IntegerField()` | `int` | Age, quantity, duration |
| `DecimalField(max_digits, decimal_places)` | `Decimal` | Fees, prices (Rs 15000.00) |
| `FloatField()` | `float` | Percentages, ratings |
| `BooleanField()` | `bool` | Is active, is paid |
| `DateField()` | `date` | Date of birth, joining date |
| `DateTimeField()` | `datetime` | Created at, updated at |
| `EmailField()` | `str` | Email addresses (with validation) |
| `URLField()` | `str` | Website links |
| `SlugField()` | `str` | URL-friendly strings |
| `FileField()` | File | Document uploads |
| `ImageField()` | Image | Photo uploads |

### Common Field Options

| Option | Meaning | Example |
|--------|---------|---------|
| `max_length=100` | Maximum characters allowed | `CharField(max_length=100)` |
| `default=True` | Default value if none provided | `BooleanField(default=True)` |
| `null=True` | Allow NULL in database | `CharField(null=True)` |
| `blank=True` | Allow empty in forms | `CharField(blank=True)` |
| `unique=True` | No duplicate values allowed | `EmailField(unique=True)` |
| `choices=[...]` | Limit to specific options | `CharField(choices=GENDER_CHOICES)` |
| `auto_now_add=True` | Set to current time on creation | `DateTimeField(auto_now_add=True)` |
| `auto_now=True` | Update to current time on every save | `DateTimeField(auto_now=True)` |

### Relationship Fields

| Field | Relationship | Example |
|-------|-------------|---------|
| `ForeignKey` | Many-to-One | Many students belong to one course |
| `OneToOneField` | One-to-One | One student has one profile |
| `ManyToManyField` | Many-to-Many | Students can enroll in many electives, each elective has many students |

The `on_delete` parameter for ForeignKey tells Django what to do when the related object is deleted:

| Option | Behavior |
|--------|----------|
| `CASCADE` | Delete the student if their course is deleted |
| `PROTECT` | Prevent deletion of course if students exist |
| `SET_NULL` | Set student's course to NULL (requires `null=True`) |
| `SET_DEFAULT` | Set to a default course |

---

## Migrations — Syncing Models to Database

After defining or changing models, you need to create and apply migrations:

```bash
# Step 1: Create migration files (Django reads your models and generates SQL)
python manage.py makemigrations
# Output: Migrations for 'students':
#   students/migrations/0001_initial.py
#     - Create model Course
#     - Create model Student

# Step 2: Apply migrations (actually creates tables in the database)
python manage.py migrate

# See the SQL that a migration would run (helpful for learning)
python manage.py sqlmigrate students 0001
```

**Golden Rule:** Every time you change a model (add a field, remove a field, change a field type), run `makemigrations` and then `migrate`.

---

## QuerySets — Talking to the Database

A QuerySet is a collection of database queries. Think of it as a list of objects from your database that you can filter, sort, and manipulate.

### Opening the Django Shell

```bash
python manage.py shell
```

### Creating Objects

```python
# Method 1: Create and save in one step
course = Course.objects.create(
    name='Python Full Stack',
    duration_months=6,
    fee=15000.00
)

# Method 2: Create object, then save
student = Student(
    name='Rahul Sharma',
    email='rahul@techpath.biz',
    phone='9876543210',
    city='Bhopal',
    gender='M',
    date_of_birth='2002-05-15',
    course=course
)
student.save()
```

### Retrieving Objects

```python
# Get ALL students
all_students = Student.objects.all()
# Returns: <QuerySet [<Student: Rahul Sharma>, <Student: Priya Patel>, ...]>

# Get ONE student by primary key
rahul = Student.objects.get(pk=1)
# Returns: <Student: Rahul Sharma>

# Get ONE student by any field
priya = Student.objects.get(email='priya@techpath.biz')
# Raises DoesNotExist if not found
# Raises MultipleObjectsReturned if more than one match
```

### Filtering Objects

`filter()` returns a QuerySet of objects that match the given conditions:

```python
# Students from Bhopal
bhopal_students = Student.objects.filter(city='Bhopal')

# Active students from Bhopal
active_bhopal = Student.objects.filter(city='Bhopal', is_active=True)

# Students NOT from Bhopal
non_bhopal = Student.objects.exclude(city='Bhopal')
```

### Ordering Results

```python
# Order by name (A to Z)
students = Student.objects.all().order_by('name')

# Order by name (Z to A)
students = Student.objects.all().order_by('-name')

# Order by city first, then by name
students = Student.objects.all().order_by('city', 'name')
```

### Limiting Results

```python
# First 5 students
top_5 = Student.objects.all()[:5]

# Students 6 to 10 (pagination)
page_2 = Student.objects.all()[5:10]

# First student
first = Student.objects.first()

# Last student
last = Student.objects.last()
```

### Counting and Checking Existence

```python
# How many students?
count = Student.objects.count()
# Returns: 45

# Are there any students from Pune?
exists = Student.objects.filter(city='Pune').exists()
# Returns: True or False
```

---

## Field Lookups — Advanced Filtering

Field lookups use the double-underscore (`__`) syntax. They are like adding conditions to your WHERE clause.

```python
# Name contains "Sharma" (case-sensitive)
Student.objects.filter(name__contains='Sharma')

# Name contains "sharma" (case-insensitive)
Student.objects.filter(name__icontains='sharma')

# Fee greater than Rs 15000
Course.objects.filter(fee__gt=15000)

# Fee between Rs 10000 and Rs 20000
Course.objects.filter(fee__range=(10000, 20000))

# Students from Bhopal, Delhi, or Pune
Student.objects.filter(city__in=['Bhopal', 'Delhi', 'Pune'])

# Students whose phone number is not set
Student.objects.filter(phone__isnull=True)

# Students who enrolled in 2025
Student.objects.filter(enrolled_on__year=2025)

# Courses that start with "Python"
Course.objects.filter(name__startswith='Python')
```

### Complete Lookup Reference

| Lookup | SQL Equivalent | Example |
|--------|---------------|---------|
| `__exact` | `= value` | `name__exact='Rahul'` |
| `__iexact` | `ILIKE value` | `city__iexact='bhopal'` |
| `__contains` | `LIKE '%value%'` | `name__contains='Shar'` |
| `__icontains` | `ILIKE '%value%'` | `name__icontains='shar'` |
| `__startswith` | `LIKE 'value%'` | `name__startswith='Ra'` |
| `__endswith` | `LIKE '%value'` | `email__endswith='@gmail.com'` |
| `__gt` | `> value` | `fee__gt=15000` |
| `__gte` | `>= value` | `fee__gte=15000` |
| `__lt` | `< value` | `fee__lt=20000` |
| `__lte` | `<= value` | `fee__lte=20000` |
| `__in` | `IN (...)` | `city__in=['Bhopal', 'Delhi']` |
| `__range` | `BETWEEN a AND b` | `fee__range=(10000, 20000)` |
| `__isnull` | `IS NULL` | `phone__isnull=True` |
| `__year` | Extract year | `enrolled_on__year=2025` |
| `__month` | Extract month | `enrolled_on__month=6` |

---

## Values and Value Lists

Sometimes you do not need full model objects. `values()` and `values_list()` return lighter results:

```python
# Get dictionaries instead of objects
Student.objects.filter(city='Bhopal').values('name', 'email')
# Returns: <QuerySet [{'name': 'Rahul Sharma', 'email': 'rahul@...'}, ...]>

# Get tuples instead of objects
Student.objects.filter(city='Bhopal').values_list('name', 'email')
# Returns: <QuerySet [('Rahul Sharma', 'rahul@...'), ...]>

# Get flat list of one field
cities = Student.objects.values_list('city', flat=True).distinct()
# Returns: <QuerySet ['Bhopal', 'Delhi', 'Pune', ...]>
```

---

## Aggregations and Annotations

Aggregations compute summary values across a QuerySet. Annotations add computed fields to each object.

```python
from django.db.models import Count, Sum, Avg, Max, Min

# --- Aggregations (return a single dictionary) ---

# Average course fee
Course.objects.aggregate(avg_fee=Avg('fee'))
# Returns: {'avg_fee': Decimal('17666.67')}

# Total fees collected (sum of all course fees)
Course.objects.aggregate(total=Sum('fee'))
# Returns: {'total': Decimal('53000.00')}

# Highest and lowest fee
Course.objects.aggregate(highest=Max('fee'), lowest=Min('fee'))
# Returns: {'highest': Decimal('20000.00'), 'lowest': Decimal('15000.00')}


# --- Annotations (add computed field to each object) ---

# Count students per course
courses = Course.objects.annotate(student_count=Count('students'))
for c in courses:
    print(f"{c.name}: {c.student_count} students")
# Output:
# Python Full Stack: 25 students
# Data Science: 18 students
# DevOps: 12 students

# Total fee revenue per course (fee * number of students)
from django.db.models import F
courses = Course.objects.annotate(
    student_count=Count('students'),
    revenue=F('fee') * Count('students')
)
```

---

## Optimizing Queries — select_related and prefetch_related

When you access related objects, Django makes extra database queries. This is called the **N+1 problem**.

### The N+1 Problem

```python
# BAD: This makes 1 query for students + 1 query per student for course = N+1 queries
students = Student.objects.all()
for student in students:
    print(student.name, student.course.name)  # Each .course triggers a new query!
```

If you have 100 students, this makes **101 database queries**. That is very slow.

### select_related (for ForeignKey / OneToOne)

`select_related` performs a SQL JOIN and fetches related objects in a single query:

```python
# GOOD: Only 1 query using JOIN
students = Student.objects.select_related('course').all()
for student in students:
    print(student.name, student.course.name)  # No extra query — already loaded
```

Use `select_related` when: a student has ONE course (ForeignKey going "forward").

### prefetch_related (for ManyToMany / Reverse ForeignKey)

`prefetch_related` makes a separate query for related objects and joins them in Python:

```python
# GOOD: 2 queries instead of N+1
courses = Course.objects.prefetch_related('students').all()
for course in courses:
    print(f"{course.name}: {course.students.count()} students")
```

Use `prefetch_related` when: a course has MANY students (reverse relationship or ManyToMany).

### Quick Decision Guide

| Relationship | Use | Why |
|-------------|-----|-----|
| ForeignKey (forward) | `select_related` | SQL JOIN is efficient for single objects |
| OneToOneField | `select_related` | Same as ForeignKey |
| ManyToManyField | `prefetch_related` | Cannot JOIN many-to-many efficiently |
| Reverse ForeignKey | `prefetch_related` | One course has many students |

---

## Updating and Deleting

```python
# --- Update single object ---
student = Student.objects.get(pk=1)
student.city = 'Pune'
student.save()

# --- Bulk update (no .save() needed, very fast) ---
Student.objects.filter(city='Bhopal').update(is_active=False)

# --- Delete single object ---
student = Student.objects.get(pk=1)
student.delete()

# --- Bulk delete ---
Student.objects.filter(is_active=False).delete()
```

---

## Chaining QuerySets

QuerySets are **lazy** — they do not hit the database until you actually use the data (iterate, slice, print, etc.). This means you can chain methods:

```python
# This builds the query but does NOT execute it yet
results = (
    Student.objects
    .filter(city='Bhopal')
    .filter(is_active=True)
    .exclude(gender='O')
    .select_related('course')
    .order_by('name')
    .values('name', 'email', 'course__name')
)

# Query executes only when you use the data
for student in results:
    print(student)
```

---

## Summary

| Operation | Code |
|-----------|------|
| Create | `Model.objects.create(field=value)` |
| Get one | `Model.objects.get(pk=1)` |
| Get all | `Model.objects.all()` |
| Filter | `Model.objects.filter(field=value)` |
| Exclude | `Model.objects.exclude(field=value)` |
| Order | `Model.objects.order_by('field')` |
| Count | `Model.objects.count()` |
| Exists | `Model.objects.filter(...).exists()` |
| Update | `Model.objects.filter(...).update(field=value)` |
| Delete | `Model.objects.filter(...).delete()` |
| Aggregate | `Model.objects.aggregate(Avg('field'))` |
| Annotate | `Model.objects.annotate(count=Count('related'))` |
| Optimize FK | `Model.objects.select_related('fk_field')` |
| Optimize M2M | `Model.objects.prefetch_related('m2m_field')` |

---

## Practice Exercise

Using the Student and Course models above:

1. Create 3 courses: Python Full Stack (Rs 15000), Data Science (Rs 18000), DevOps (Rs 20000)
2. Create 5 students across different cities (Bhopal, Delhi, Pune)
3. Query all students from Bhopal
4. Find courses with fee greater than Rs 15000
5. Count students per course using annotation
6. Use `select_related` to fetch students with their course names efficiently

---

*TechPath Institute - Python Full Stack Development Course*
