# Module 07 — Django & Django REST Framework — Teaching Notes

---

## What is Django?

- **Django** = a Python web framework that follows the **MVT** pattern (Model-View-Template)
- "The web framework for perfectionists with deadlines"
- Comes with admin panel, ORM, auth, forms — batteries included
- Used by Instagram, Pinterest, Mozilla, Disqus

### MVT Pattern

| Layer | What It Does | Django File |
|-------|-------------|-------------|
| **Model** | Defines database tables | `models.py` |
| **View** | Business logic, processes requests | `views.py` |
| **Template** | HTML pages (what user sees) | `templates/*.html` |
| **URL** | Maps URLs to views | `urls.py` |

```
User Request → urls.py → views.py → models.py (DB) → template → Response
```

---

## Django Setup

### Create a Project

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py startapp students
```

### Project Structure

```
mysite/
├── manage.py              # Command-line tool
├── mysite/
│   ├── settings.py        # Configuration
│   ├── urls.py            # Root URL routing
│   ├── wsgi.py            # WSGI deployment
│   └── asgi.py            # ASGI deployment
└── students/
    ├── models.py           # Database models
    ├── views.py            # View functions
    ├── urls.py             # App-level URLs (create this)
    ├── admin.py            # Admin panel registration
    ├── apps.py             # App config
    ├── serializers.py      # DRF serializers (create this)
    └── migrations/         # Database migrations
```

### Key manage.py Commands

```bash
python manage.py runserver            # Start dev server at :8000
python manage.py makemigrations       # Create migration files
python manage.py migrate              # Apply migrations to DB
python manage.py createsuperuser      # Create admin user
python manage.py shell                # Interactive Python shell
python manage.py collectstatic        # Gather static files
python manage.py test                 # Run tests
```

---

## Models (Database Tables)

### Defining Models

```python
# students/models.py
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.IntegerField(default=6)
    fee = models.DecimalField(max_digits=8, decimal_places=2)  # ₹50,000.00
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, default='Bhopal')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    marks = models.IntegerField(default=0)
    enrolled_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

    class Meta:
        ordering = ['-enrolled_on']
```

### Common Field Types

| Field | Python Type | Example |
|-------|------------|---------|
| `CharField` | str | `name = CharField(max_length=100)` |
| `TextField` | str (long) | `bio = TextField(blank=True)` |
| `IntegerField` | int | `marks = IntegerField(default=0)` |
| `DecimalField` | Decimal | `fee = DecimalField(max_digits=8, decimal_places=2)` |
| `BooleanField` | bool | `is_active = BooleanField(default=True)` |
| `DateField` | date | `dob = DateField()` |
| `DateTimeField` | datetime | `created_at = DateTimeField(auto_now_add=True)` |
| `EmailField` | str | `email = EmailField(unique=True)` |
| `ForeignKey` | FK relation | `course = ForeignKey(Course, on_delete=CASCADE)` |
| `ManyToManyField` | M2M | `tags = ManyToManyField(Tag)` |
| `FileField` | file upload | `resume = FileField(upload_to='resumes/')` |

### Migrations

```bash
python manage.py makemigrations    # Generates migration file
python manage.py migrate           # Applies to database
python manage.py showmigrations    # Lists migration status
```

---

## Django ORM (Querysets)

### Basic CRUD

```python
from students.models import Student, Course

# Create
course = Course.objects.create(name="Python Full Stack", duration_months=8, fee=45000)
student = Student.objects.create(name="Rahul Sharma", email="rahul@email.com", course=course, marks=85)

# Read
all_students = Student.objects.all()                   # All records
one = Student.objects.get(id=1)                         # Single record (raises if not found)
first = Student.objects.first()                         # First record or None

# Update
student.marks = 90
student.save()
# OR bulk update:
Student.objects.filter(city="Bhopal").update(marks=80)

# Delete
student.delete()
Student.objects.filter(marks__lt=40).delete()
```

### Filtering & Lookups

```python
# Exact match
Student.objects.filter(city="Bhopal")

# Case-insensitive contains
Student.objects.filter(name__icontains="rahul")

# Greater than / less than
Student.objects.filter(marks__gte=80)         # marks >= 80
Student.objects.filter(marks__lt=40)          # marks < 40

# In a list
Student.objects.filter(city__in=["Bhopal", "Delhi", "Pune"])

# Date range
from datetime import date
Student.objects.filter(enrolled_on__year=2026)
Student.objects.filter(enrolled_on__gte=date(2026, 1, 1))

# Null check
Student.objects.filter(phone__isnull=True)

# Chaining (AND)
Student.objects.filter(city="Bhopal", marks__gte=80)

# OR queries
from django.db.models import Q
Student.objects.filter(Q(city="Bhopal") | Q(city="Delhi"))

# Exclude
Student.objects.exclude(marks__lt=40)
```

### Aggregations & Annotations

```python
from django.db.models import Count, Avg, Max, Min, Sum

# Aggregation (returns dict)
Student.objects.aggregate(
    avg_marks=Avg('marks'),
    total=Count('id'),
    top_score=Max('marks'),
)
# {'avg_marks': 78.5, 'total': 25, 'top_score': 98}

# Annotation (adds computed field to each row)
courses = Course.objects.annotate(
    student_count=Count('students'),
    avg_marks=Avg('students__marks'),
)
for c in courses:
    print(f"{c.name}: {c.student_count} students, avg {c.avg_marks}")
```

### Performance: select_related & prefetch_related

```python
# BAD: N+1 queries (1 query per student to fetch course)
for s in Student.objects.all():
    print(s.course.name)     # Hits DB each time!

# GOOD: select_related (ForeignKey — single JOIN query)
for s in Student.objects.select_related('course'):
    print(s.course.name)     # No extra queries

# GOOD: prefetch_related (reverse FK / M2M — 2 queries total)
for c in Course.objects.prefetch_related('students'):
    print(c.name, c.students.count())
```

---

## Django Admin

### Register Models

```python
# students/admin.py
from django.contrib import admin
from .models import Student, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_months', 'fee', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'course', 'city', 'marks', 'enrolled_on']
    list_filter = ['course', 'city', 'gender']
    search_fields = ['name', 'email']
    list_per_page = 20
    list_editable = ['marks']          # Edit marks directly in list view
    readonly_fields = ['enrolled_on']
    actions = ['mark_passed']

    @admin.action(description="Mark selected students as passed (80+)")
    def mark_passed(self, request, queryset):
        queryset.update(marks=80)
```

### Access Admin

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@techpath.biz
# Password: (choose one)
python manage.py runserver
# Visit: http://localhost:8000/admin/
```

---

## Views & URLs

### Function-Based Views (FBV)

```python
# students/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student

def student_list(request):
    students = Student.objects.select_related('course').all()
    return render(request, 'students/list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})
```

### Class-Based Views (CBV)

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class StudentListView(ListView):
    model = Student
    template_name = 'students/list.html'
    context_object_name = 'students'
    paginate_by = 10

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'email', 'phone', 'city', 'course', 'marks']
    template_name = 'students/form.html'
    success_url = reverse_lazy('student-list')
```

### URL Configuration

```python
# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),
    path('students/new/', views.StudentCreateView.as_view(), name='student-create'),
]

# mysite/urls.py (root)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
]
```

---

## Django Forms & Authentication

### Model Forms

```python
# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'city', 'course', 'marks']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100")
        return marks
```

### Built-in Authentication

```python
# mysite/urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
]

# settings.py
LOGIN_REDIRECT_URL = '/students/'
LOGOUT_REDIRECT_URL = '/login/'
```

### Protecting Views

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Function view
@login_required
def student_list(request):
    ...

# Class view
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
```

---

## Django REST Framework (DRF)

### Setup

```bash
pip install djangorestframework django-filter
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Serializers

```python
# students/serializers.py
from rest_framework import serializers
from .models import Student, Course

class CourseSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'duration_months', 'fee', 'is_active', 'student_count']

class StudentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'phone', 'city', 'gender', 'course',
                  'course_name', 'marks', 'enrolled_on']
        read_only_fields = ['enrolled_on']

    def validate_marks(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Marks must be between 0 and 100")
        return value
```

### ViewSets & Routers

```python
# students/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('course').all()
    serializer_class = StudentSerializer
    filterset_fields = ['course', 'city', 'gender']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'marks', 'enrolled_on']
    ordering = ['-enrolled_on']

    @action(detail=False, methods=['get'])
    def stats(self, request):
        data = Student.objects.aggregate(
            total=Count('id'),
            avg_marks=Avg('marks'),
        )
        return Response(data)

    @action(detail=False, methods=['get'])
    def toppers(self, request):
        toppers = Student.objects.filter(marks__gte=90).order_by('-marks')[:5]
        serializer = self.get_serializer(toppers, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.annotate(student_count=Count('students'))
    serializer_class = CourseSerializer
    search_fields = ['name']

# students/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('courses', views.CourseViewSet)

urlpatterns = router.urls
```

### DRF URLs

```python
# mysite/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),     # /api/students/, /api/courses/
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login
]
```

---

## DRF Authentication & Permissions

### Token Authentication

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Custom Permissions

```python
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # Public actions:
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []   # No auth needed for read
        return [IsAuthenticated()]
```

### Throttling

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/hour',
        'user': '200/hour',
    },
}
```

---

## Django Channels (WebSockets)

### Setup

```bash
pip install channels channels-redis
```

```python
# settings.py
INSTALLED_APPS = [..., 'channels']
ASGI_APPLICATION = 'mysite.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    },
}
```

### WebSocket Consumer

```python
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data.get('sender', 'Anonymous')

        await self.channel_layer.group_send(
            self.room_group,
            {'type': 'chat_message', 'message': message, 'sender': sender}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))
```

### Routing

```python
# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# mysite/asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})
```

---

## Celery + Redis (Background Tasks)

### Setup

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
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

### Define Tasks

```python
# students/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(student_name, student_email):
    send_mail(
        subject=f"Welcome to TechPath Institute, {student_name}!",
        message=f"Dear {student_name},\n\nYour enrollment is confirmed.\n\n— TechPath Institute, Bhopal",
        from_email="admin@techpath.biz",
        recipient_list=[student_email],
    )
    return f"Email sent to {student_email}"

@shared_task
def generate_report():
    from .models import Student
    count = Student.objects.count()
    return f"Report generated: {count} students total"
```

### Call Tasks

```python
# In a view or signal
from .tasks import send_welcome_email

# Async (runs in background)
send_welcome_email.delay("Rahul Sharma", "rahul@email.com")

# With countdown (30 seconds delay)
send_welcome_email.apply_async(args=["Priya Patel", "priya@email.com"], countdown=30)
```

### Periodic Tasks (Celery Beat)

```bash
pip install django-celery-beat
```

```python
# settings.py
INSTALLED_APPS = [..., 'django_celery_beat']

CELERY_BEAT_SCHEDULE = {
    'daily-report': {
        'task': 'students.tasks.generate_report',
        'schedule': 86400.0,   # Every 24 hours (seconds)
    },
}
```

### Run Celery

```bash
celery -A mysite worker -l info           # Start worker
celery -A mysite beat -l info             # Start scheduler
```

---

## Key Differences: FastAPI vs Django

| Feature | FastAPI | Django |
|---------|---------|--------|
| Speed | Very fast (async) | Moderate |
| Admin Panel | None (build your own) | Built-in |
| ORM | None (use SQLAlchemy) | Built-in Django ORM |
| Auth | Manual (JWT libs) | Built-in (sessions, permissions) |
| API Docs | Auto (Swagger + ReDoc) | Via DRF (Browsable API) |
| Best For | Microservices, APIs | Full web apps |
| Learning Curve | Easy | Moderate |
| Templates | Not built-in | Built-in (Jinja-like) |

---

## Quick Reference: DRF Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid data |
| 401 | Unauthorized | No/invalid token |
| 403 | Forbidden | No permission |
| 404 | Not Found | Object doesn't exist |
| 429 | Too Many Requests | Throttled |
