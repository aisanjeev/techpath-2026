"""
Django Model + View Example — Module 14 Code Snap

This is a reference file showing Django model and view patterns.
To use: create a Django project first with:
    django-admin startproject myproject
    cd myproject
    python manage.py startapp students

Then copy these patterns into the appropriate files.
"""

# =============================================
# students/models.py — Database Models
# =============================================

"""
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration_months = models.IntegerField()
    fee = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    marks = models.IntegerField(default=0)
    city = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    enrolled_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

    @property
    def grade(self):
        if self.marks >= 90: return "A+"
        if self.marks >= 75: return "A"
        if self.marks >= 60: return "B"
        if self.marks >= 45: return "C"
        return "F"

    class Meta:
        ordering = ['-marks']
"""


# =============================================
# students/admin.py — Admin Panel Config
# =============================================

"""
from django.contrib import admin
from .models import Student, Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_months', 'fee']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'course', 'marks', 'city', 'is_active']
    list_filter = ['course', 'city', 'is_active']
    search_fields = ['name', 'email']
"""


# =============================================
# students/views.py — API Views
# =============================================

"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Student, Course
import json

def student_list(request):
    students = Student.objects.select_related('course').all()

    # Filter by course
    course = request.GET.get('course')
    if course:
        students = students.filter(course__name__iexact=course)

    # Filter by city
    city = request.GET.get('city')
    if city:
        students = students.filter(city__iexact=city)

    # Search
    search = request.GET.get('search')
    if search:
        students = students.filter(name__icontains=search)

    data = list(students.values('id', 'name', 'email', 'marks', 'city',
                                 'course__name', 'enrolled_date'))
    return JsonResponse({"success": True, "data": data}, safe=False)


@require_http_methods(["POST"])
def student_create(request):
    try:
        body = json.loads(request.body)
        course = Course.objects.get(name=body['course'])
        student = Student.objects.create(
            name=body['name'],
            email=body['email'],
            course=course,
            marks=body.get('marks', 0),
            city=body.get('city', ''),
        )
        return JsonResponse({
            "success": True,
            "data": {"id": student.id, "name": student.name},
            "message": "Student created"
        }, status=201)
    except Course.DoesNotExist:
        return JsonResponse({"success": False, "error": "Course not found"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
"""


# =============================================
# students/urls.py — URL Routing
# =============================================

"""
from django.urls import path
from . import views

urlpatterns = [
    path('api/students/', views.student_list, name='student-list'),
    path('api/students/create/', views.student_create, name='student-create'),
]
"""


# =============================================
# Django Commands Cheat Sheet
# =============================================

"""
django-admin startproject myproject     # Create project
python manage.py startapp students      # Create app
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Create admin user
python manage.py runserver              # Run dev server at :8000
python manage.py shell                  # Python shell with Django
python manage.py test                   # Run tests

# In the shell:
from students.models import Student
Student.objects.all()                   # Get all
Student.objects.filter(city="Bhopal")   # Filter
Student.objects.create(name="Rahul")    # Create
Student.objects.get(id=1).delete()      # Delete
"""
