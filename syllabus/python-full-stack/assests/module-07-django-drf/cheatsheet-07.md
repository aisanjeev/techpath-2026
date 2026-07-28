# Cheat Sheet: Django & Django REST Framework

**Module 07 — Quick Reference**
**TechPath Institute | Python Full Stack Course**

---

## 1. Django CLI Commands

| Command | What It Does |
|---------|-------------|
| `django-admin startproject mysite` | Create a new Django project |
| `python manage.py startapp students` | Create a new app inside the project |
| `python manage.py runserver` | Start dev server at `http://127.0.0.1:8000` |
| `python manage.py makemigrations` | Generate migration files from model changes |
| `python manage.py migrate` | Apply migrations to the database |
| `python manage.py createsuperuser` | Create an admin user (username + password) |
| `python manage.py shell` | Open interactive Python shell with Django loaded |
| `python manage.py collectstatic` | Gather all static files into one folder |
| `python manage.py test` | Run all test cases |

---

## 2. MVT Pattern Summary

| Layer | Responsibility | File |
|-------|---------------|------|
| **Model** | Defines database tables and fields | `models.py` |
| **View** | Handles business logic and returns responses | `views.py` |
| **Template** | HTML pages shown to the user | `templates/*.html` |
| **URL Conf** | Maps URL paths to views | `urls.py` |

```
User Request → urls.py → views.py → models.py (DB query) → template → HTML Response
```

---

## 3. Model Field Types

| Field | Purpose | Example |
|-------|---------|---------|
| `CharField(max_length=100)` | Short text (name, title) | `name = models.CharField(max_length=100)` |
| `TextField()` | Long text (description, bio) | `bio = models.TextField()` |
| `IntegerField()` | Whole numbers | `age = models.IntegerField()` |
| `FloatField()` | Decimal numbers | `price = models.FloatField()` |
| `DecimalField(max_digits, decimal_places)` | Exact decimals (money) | `fee = models.DecimalField(max_digits=8, decimal_places=2)` |
| `BooleanField(default=False)` | True / False | `is_active = models.BooleanField(default=True)` |
| `DateField()` | Date only | `dob = models.DateField()` |
| `DateTimeField(auto_now_add=True)` | Date + time (auto-set on create) | `created_at = models.DateTimeField(auto_now_add=True)` |
| `EmailField()` | Email with validation | `email = models.EmailField(unique=True)` |
| `FileField(upload_to='files/')` | File upload | `resume = models.FileField(upload_to='resumes/')` |
| `ImageField(upload_to='imgs/')` | Image upload | `photo = models.ImageField(upload_to='photos/')` |
| `SlugField()` | URL-friendly text | `slug = models.SlugField(unique=True)` |
| `ForeignKey(Model, on_delete)` | Many-to-one relationship | `course = models.ForeignKey(Course, on_delete=models.CASCADE)` |
| `ManyToManyField(Model)` | Many-to-many relationship | `tags = models.ManyToManyField(Tag)` |
| `OneToOneField(Model, on_delete)` | One-to-one relationship | `profile = models.OneToOneField(User, on_delete=models.CASCADE)` |

**Common `on_delete` options:** `CASCADE` (delete related), `PROTECT` (block delete), `SET_NULL` (set to null), `SET_DEFAULT`

---

## 4. Common QuerySet Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `.all()` | Get all records | `Student.objects.all()` |
| `.filter(**kwargs)` | Get records matching condition | `Student.objects.filter(city="Mumbai")` |
| `.exclude(**kwargs)` | Get records NOT matching condition | `Student.objects.exclude(is_active=False)` |
| `.get(**kwargs)` | Get exactly one record (raises error if 0 or 2+) | `Student.objects.get(id=5)` |
| `.order_by('field')` | Sort results (`-field` for descending) | `Student.objects.order_by('-created_at')` |
| `.values('f1', 'f2')` | Return dictionaries instead of objects | `Student.objects.values('name', 'email')` |
| `.values_list('f', flat=True)` | Return flat list of one field | `Student.objects.values_list('name', flat=True)` |
| `.count()` | Count records | `Student.objects.filter(city="Delhi").count()` |
| `.exists()` | Check if any record exists (returns bool) | `Student.objects.filter(email=e).exists()` |
| `.first()` / `.last()` | Get first or last record | `Student.objects.order_by('name').first()` |
| `.create(**kwargs)` | Create and save a new record | `Student.objects.create(name="Amit", age=22)` |
| `.update(**kwargs)` | Update matching records | `Student.objects.filter(city="Pune").update(is_active=True)` |
| `.delete()` | Delete matching records | `Student.objects.filter(is_active=False).delete()` |
| `.annotate()` | Add computed fields | `Course.objects.annotate(total=Count('students'))` |
| `.aggregate()` | Compute summary values | `Student.objects.aggregate(Avg('age'))` |
| `.select_related('fk')` | JOIN for ForeignKey (reduces queries) | `Student.objects.select_related('course')` |
| `.prefetch_related('m2m')` | Separate query for M2M (reduces queries) | `Course.objects.prefetch_related('tags')` |

**Filter lookups:** `name__contains`, `age__gte`, `date__year`, `city__in=["Mumbai","Delhi"]`, `email__isnull=True`

---

## 5. URL Patterns

```python
# mysite/urls.py (project level)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/students/', include('students.urls')),
]

# students/urls.py (app level)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student-list'),
    path('<int:pk>/', views.student_detail, name='student-detail'),
]
```

| Pattern | Matches | Captured As |
|---------|---------|-------------|
| `path('items/', view)` | `/items/` | Nothing |
| `path('items/<int:pk>/', view)` | `/items/5/` | `pk=5` |
| `path('items/<str:slug>/', view)` | `/items/hello/` | `slug="hello"` |
| `path('items/<uuid:id>/', view)` | `/items/550e...f47/` | `id=UUID(...)` |

---

## 6. Class-Based Views (CBV)

| View | Purpose | Key Attributes |
|------|---------|---------------|
| `ListView` | Display list of objects | `model`, `template_name`, `context_object_name`, `paginate_by` |
| `DetailView` | Display single object | `model`, `template_name` |
| `CreateView` | Form to create an object | `model`, `fields`, `template_name`, `success_url` |
| `UpdateView` | Form to update an object | `model`, `fields`, `template_name`, `success_url` |
| `DeleteView` | Confirm and delete an object | `model`, `template_name`, `success_url` |

```python
from django.views.generic import ListView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'students/list.html'
    context_object_name = 'students'
    paginate_by = 10
```

**URL wiring:** `path('students/', StudentListView.as_view(), name='student-list')`

---

## 7. DRF Essentials — Serializer, ViewSet, Router

```python
# serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # or ['id', 'name', 'email']

# views.py
from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# urls.py
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

router = DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = router.urls
```

**Auto-generated endpoints:**

| Method | URL | Action |
|--------|-----|--------|
| GET | `/students/` | List all |
| POST | `/students/` | Create one |
| GET | `/students/1/` | Retrieve one |
| PUT | `/students/1/` | Full update |
| PATCH | `/students/1/` | Partial update |
| DELETE | `/students/1/` | Delete one |

---

## 8. DRF Authentication

### Token Authentication (built-in)

```python
# settings.py
INSTALLED_APPS = [..., 'rest_framework.authtoken']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

```bash
python manage.py migrate          # creates token table
python manage.py drf_createtoken username  # generate token
```

**Client sends:** `Authorization: Token abc123...`

### Simple JWT (recommended for production)

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

| Endpoint | Request Body | Returns |
|----------|-------------|---------|
| `POST /api/token/` | `{"username": "...", "password": "..."}` | `{"access": "...", "refresh": "..."}` |
| `POST /api/token/refresh/` | `{"refresh": "..."}` | `{"access": "..."}` |

**Client sends:** `Authorization: Bearer eyJ...`

---

## 9. DRF Permissions

| Permission Class | Who Can Access |
|-----------------|---------------|
| `AllowAny` | Everyone (no auth needed) |
| `IsAuthenticated` | Logged-in users only |
| `IsAdminUser` | Staff users only (`is_staff=True`) |
| `IsAuthenticatedOrReadOnly` | Anyone can read; only logged-in users can write |

```python
from rest_framework.permissions import IsAuthenticated

class StudentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    ...
```

**Custom permission:**

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```

---

## 10. Celery Quick Setup

```bash
pip install celery redis
```

```python
# mysite/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# students/tasks.py
from celery import shared_task

@shared_task
def send_welcome_email(student_id):
    # long-running work here
    pass

# Call it from anywhere:
send_welcome_email.delay(student_id=42)
```

**Start worker:** `celery -A mysite worker --loglevel=info`

---

## 11. Common HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| `200` | OK | Successful GET, PUT, PATCH |
| `201` | Created | Successful POST (new resource) |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Validation errors, malformed data |
| `401` | Unauthorized | Missing or invalid auth token |
| `403` | Forbidden | Authenticated but not allowed |
| `404` | Not Found | Resource does not exist |
| `405` | Method Not Allowed | Wrong HTTP method for that endpoint |
| `500` | Internal Server Error | Unhandled server bug |

---

*TechPath Institute — Django & DRF Quick Reference*
