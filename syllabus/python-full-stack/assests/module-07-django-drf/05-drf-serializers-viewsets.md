# DRF Serializers & ViewSets

**Module 07 — Django & Django REST Framework | Topic 5**

---

## What is Django REST Framework (DRF)?

Imagine you run a restaurant. Your kitchen (Django) makes great food, but it only serves dine-in customers (web pages). Now you want to deliver food via Swiggy and Zomato too. You need a **packaging system** that wraps your food in boxes so delivery apps can handle it. DRF is that packaging system — it wraps your Django data into JSON so mobile apps, React frontends, and other services can consume it.

**DRF = Django REST Framework** — a powerful toolkit for building Web APIs on top of Django.

### Why Use DRF?

| Without DRF | With DRF |
|-------------|----------|
| You manually convert querysets to JSON using `json.dumps()` | Serializers handle conversion automatically |
| You write raw `if request.method == 'GET'` logic | ViewSets give you CRUD in a few lines |
| No built-in pagination | Built-in pagination classes |
| No browsable API | Beautiful browsable API for testing |
| Manual input validation | Automatic validation with clear error messages |

---

## Installing DRF

```bash
pip install djangorestframework
```

Add it to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',   # Add this line
    'students',         # Your app
]
```

---

## Our Example: Student Management API

Throughout this topic, we will build a complete API for managing students at TechPath Institute, Bhopal. Let us start with the model.

```python
# students/models.py
from django.db import models

class Student(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)
    semester = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    city = models.CharField(max_length=50, default='Bhopal')
    enrolled_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.branch})"
```

Run migrations after creating the model:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Serializers — Converting Data to JSON and Back

A **serializer** is like a translator. It converts complex Django model objects into simple Python dictionaries (which become JSON), and it also converts incoming JSON data back into model objects.

### Serializer vs ModelSerializer

| Feature | `Serializer` | `ModelSerializer` |
|---------|-------------|-------------------|
| Field definition | You define every field manually | Auto-generates fields from model |
| Validation | You write all validation yourself | Auto-validates based on model constraints |
| `create()` / `update()` | You must write them | Already implemented |
| Use when | You need full control or non-model data | 90% of the time — for model-based APIs |

### Basic Serializer (Manual Way)

```python
# students/serializers.py
from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    branch = serializers.CharField(max_length=3)
    semester = serializers.IntegerField()
    cgpa = serializers.DecimalField(max_digits=4, decimal_places=2)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        # ... repeat for all fields
        instance.save()
        return instance
```

This is a lot of repetitive work. That is why we use `ModelSerializer` instead.

### ModelSerializer (The Smart Way)

```python
# students/serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Include all fields
```

That is it. DRF reads your model and automatically creates all fields, validation, `create()`, and `update()` methods.

### Controlling Which Fields to Include

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'branch', 'semester', 'cgpa']
        # Or exclude specific fields:
        # exclude = ['is_active']
```

### Adding Custom Validation

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_cgpa(self, value):
        """CGPA must be between 0 and 10."""
        if value < 0 or value > 10:
            raise serializers.ValidationError("CGPA must be between 0 and 10.")
        return value

    def validate_semester(self, value):
        """Semester must be between 1 and 8."""
        if value < 1 or value > 8:
            raise serializers.ValidationError("Semester must be between 1 and 8.")
        return value

    def validate(self, data):
        """Cross-field validation: final year students must have CGPA."""
        if data.get('semester', 0) >= 7 and data.get('cgpa', 0) == 0:
            raise serializers.ValidationError(
                "Final year students must have a valid CGPA."
            )
        return data
```

### Read-Only and Write-Only Fields

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['enrolled_on']  # Cannot be set via API
        extra_kwargs = {
            'email': {'write_only': False},
            'cgpa': {'required': True},
        }
```

---

## ViewSets — CRUD in Minutes

A **ViewSet** is like a smart employee who knows how to handle all types of requests for a resource. Instead of writing separate views for list, create, retrieve, update, and delete, a ViewSet handles all of them.

### ModelViewSet

```python
# students/views.py
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

These three lines give you all of the following endpoints:

| HTTP Method | URL | Action | Description |
|-------------|-----|--------|-------------|
| GET | `/api/students/` | list | Get all students |
| POST | `/api/students/` | create | Add a new student |
| GET | `/api/students/1/` | retrieve | Get student with id=1 |
| PUT | `/api/students/1/` | update | Update all fields of student 1 |
| PATCH | `/api/students/1/` | partial_update | Update some fields of student 1 |
| DELETE | `/api/students/1/` | destroy | Delete student 1 |

---

## Routers — Automatic URL Configuration

A **Router** automatically creates URL patterns for your ViewSet. Think of it as a traffic policeman who directs requests to the right ViewSet method.

```python
# students/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Now include this in your project's main `urls.py`:

```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
]
```

Visit `http://localhost:8000/api/students/` in your browser and you will see DRF's beautiful browsable API.

---

## Pagination — Don't Send Everything at Once

Imagine TechPath Institute has 10,000 students. Sending all records in one response would be slow and wasteful. Pagination splits results into pages, like pages of a book.

### PageNumberPagination

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

Now `GET /api/students/` returns 10 students at a time:

```json
{
    "count": 150,
    "next": "http://localhost:8000/api/students/?page=2",
    "previous": null,
    "results": [ ... 10 students ... ]
}
```

### LimitOffsetPagination

This gives the client more control — "give me 5 records starting from the 20th":

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}
```

Request: `GET /api/students/?limit=5&offset=20`

| Pagination Type | Use When |
|----------------|----------|
| PageNumberPagination | Simple pages (page 1, page 2, page 3...) |
| LimitOffsetPagination | Client needs precise control (skip 20, take 5) |

---

## Filtering with django-filter

Rahul wants to see only CSE students from Bhopal. Without filtering, he would have to fetch all students and filter on the frontend. That is wasteful. Let the backend do it.

### Setup

```bash
pip install django-filter
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_filters',
]
```

Configure DRF:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Adding Filters to the ViewSet

```python
# students/views.py
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'semester', 'city', 'is_active']
```

Now Rahul can filter: `GET /api/students/?branch=CSE&city=Bhopal`

---

## Searching and Ordering

### Search

Priya wants to search students by name or email without knowing the exact value. DRF has a built-in `SearchFilter`:

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'semester', 'city']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'cgpa', 'semester', 'enrolled_on']
    ordering = ['name']  # Default ordering
```

Search: `GET /api/students/?search=priya`

This searches in both `name` and `email` fields.

### Ordering

Sort by CGPA descending: `GET /api/students/?ordering=-cgpa`

Sort by branch, then name: `GET /api/students/?ordering=branch,name`

---

## Complete Example — Putting It All Together

Here is the final Student API with all features combined:

```python
# students/serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['enrolled_on']

    def validate_cgpa(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("CGPA must be between 0 and 10.")
        return value
```

```python
# students/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'semester', 'city', 'is_active']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'cgpa', 'semester']
    ordering = ['name']
```

```python
# students/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StudentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### Testing with the Browsable API

1. Run the server: `python manage.py runserver`
2. Open `http://localhost:8000/api/students/` in your browser
3. You will see a form to POST new students and a list of existing ones
4. Try adding Amit (CSE, Semester 5, CGPA 8.2, Pune) using the form

---

## Quick Reference

| Concept | What It Does |
|---------|-------------|
| Serializer | Converts model instances to/from JSON |
| ModelSerializer | Auto-generates serializer from model |
| ViewSet | Handles all CRUD operations for a model |
| ModelViewSet | ViewSet + queryset + serializer = full CRUD |
| DefaultRouter | Auto-generates URLs for ViewSets |
| PageNumberPagination | Splits results into numbered pages |
| DjangoFilterBackend | Exact-match filtering on fields |
| SearchFilter | Partial text search across fields |
| OrderingFilter | Sort results by specified fields |

---

*TechPath Institute — Python Full Stack Development Program*
