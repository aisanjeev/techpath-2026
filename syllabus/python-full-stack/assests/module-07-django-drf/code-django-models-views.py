"""
Django Models & Views — Module 07 Code Snap
This file shows Django models, admin config, views, and URL patterns
for a student management system at TechPath Institute, Bhopal.

NOTE: This is a reference file — not runnable standalone.
      Use 'django-admin startproject institute' to set up, then
      copy relevant parts into your app files.
"""

# ============================================================
# PART 1: Models (students/models.py)
# ============================================================

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    """Course offered by TechPath Institute"""
    name = models.CharField(max_length=100, unique=True)
    duration_months = models.IntegerField(default=6)
    fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Fee in INR (e.g., 45000.00)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"

    class Meta:
        ordering = ["name"]


class Student(models.Model):
    """Student enrolled at TechPath Institute"""
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    CITY_CHOICES = [
        ("Bhopal", "Bhopal"),
        ("Delhi", "Delhi"),
        ("Pune", "Pune"),
        ("Indore", "Indore"),
        ("Mumbai", "Mumbai"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default="Bhopal")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="students"
    )
    marks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    enrolled_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.course.name}"

    @property
    def status(self):
        """Pass/Fail based on marks"""
        return "Pass" if self.marks >= 40 else "Fail"

    class Meta:
        ordering = ["-enrolled_on"]


class Attendance(models.Model):
    """Daily attendance record"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]


# ============================================================
# PART 2: Admin Configuration (students/admin.py)
# ============================================================

from django.contrib import admin
# from .models import Student, Course, Attendance  # uncomment in real file


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_months", "fee", "is_active", "student_count"]
    list_filter = ["is_active"]
    search_fields = ["name"]

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Enrolled"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "course", "city", "marks", "status", "enrolled_on"]
    list_filter = ["course", "city", "gender"]
    search_fields = ["name", "email"]
    list_per_page = 20
    list_editable = ["marks"]
    readonly_fields = ["enrolled_on"]
    actions = ["mark_as_passed", "export_as_csv"]

    def status(self, obj):
        return obj.status
    status.short_description = "Result"

    @admin.action(description="Set marks to 40 (minimum pass)")
    def mark_as_passed(self, request, queryset):
        updated = queryset.filter(marks__lt=40).update(marks=40)
        self.message_user(request, f"{updated} students marked as passed.")


# ============================================================
# PART 3: Views — Function-Based (students/views.py)
# ============================================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
# from .models import Student, Course  # uncomment in real file
# from .forms import StudentForm       # uncomment in real file


def student_list(request):
    """List students with search & filter"""
    students = Student.objects.select_related("course").all()

    # Search
    search = request.GET.get("search", "")
    if search:
        students = students.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )

    # Filter by course
    course_id = request.GET.get("course")
    if course_id:
        students = students.filter(course_id=course_id)

    # Filter by city
    city = request.GET.get("city")
    if city:
        students = students.filter(city=city)

    context = {
        "students": students,
        "courses": Course.objects.all(),
        "search": search,
        "total": students.count(),
    }
    return render(request, "students/list.html", context)


def student_detail(request, pk):
    """Show single student details"""
    student = get_object_or_404(
        Student.objects.select_related("course"),
        pk=pk
    )
    attendance = student.attendance.all()[:30]
    context = {
        "student": student,
        "attendance": attendance,
        "attendance_pct": _calc_attendance(attendance),
    }
    return render(request, "students/detail.html", context)


def _calc_attendance(records):
    """Helper to calculate attendance percentage"""
    if not records:
        return 0
    present = sum(1 for r in records if r.is_present)
    return round(present / len(records) * 100, 1)


@login_required
def dashboard(request):
    """Admin dashboard with stats"""
    stats = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.filter(is_active=True).count(),
        "avg_marks": Student.objects.aggregate(avg=Avg("marks"))["avg"] or 0,
        "city_wise": (
            Student.objects
            .values("city")
            .annotate(count=Count("id"))
            .order_by("-count")
        ),
        "course_wise": (
            Course.objects
            .annotate(count=Count("students"))
            .filter(count__gt=0)
            .order_by("-count")
        ),
    }
    return render(request, "students/dashboard.html", stats)


# ============================================================
# PART 4: Class-Based Views (CBV)
# ============================================================

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentListView(ListView):
    model = Student
    template_name = "students/list.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("course")
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ["name", "email", "phone", "city", "course", "marks"]
    template_name = "students/form.html"
    success_url = reverse_lazy("student-list")


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ["name", "email", "phone", "city", "marks"]
    template_name = "students/form.html"
    success_url = reverse_lazy("student-list")


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "students/confirm_delete.html"
    success_url = reverse_lazy("student-list")


# ============================================================
# PART 5: URL Configuration (students/urls.py)
# ============================================================

from django.urls import path
# from . import views  # uncomment in real file

urlpatterns = [
    # Function-based views
    path("", student_list, name="student-list"),
    path("student/<int:pk>/", student_detail, name="student-detail"),
    path("dashboard/", dashboard, name="dashboard"),

    # Class-based views (alternative — use one set, not both)
    # path("", StudentListView.as_view(), name="student-list"),
    # path("student/new/", StudentCreateView.as_view(), name="student-create"),
    # path("student/<int:pk>/edit/", StudentUpdateView.as_view(), name="student-update"),
    # path("student/<int:pk>/delete/", StudentDeleteView.as_view(), name="student-delete"),
]


# ============================================================
# SAMPLE DATA — Run in Django shell (python manage.py shell)
# ============================================================

"""
from students.models import Course, Student

# Create courses
python_course = Course.objects.create(name="Python Full Stack", duration_months=8, fee=45000)
data_course = Course.objects.create(name="Data Science", duration_months=6, fee=35000)
web_course = Course.objects.create(name="Web Development", duration_months=4, fee=25000)

# Create students
students_data = [
    {"name": "Rahul Sharma", "email": "rahul@email.com", "city": "Bhopal", "course": python_course, "marks": 85},
    {"name": "Priya Patel", "email": "priya@email.com", "city": "Indore", "course": python_course, "marks": 92},
    {"name": "Ananya Singh", "email": "ananya@email.com", "city": "Delhi", "course": data_course, "marks": 78},
    {"name": "Vikram Joshi", "email": "vikram@email.com", "city": "Pune", "course": web_course, "marks": 65},
    {"name": "Neha Gupta", "email": "neha@email.com", "city": "Bhopal", "course": python_course, "marks": 88},
    {"name": "Amit Kumar", "email": "amit@email.com", "city": "Delhi", "course": data_course, "marks": 45},
    {"name": "Deepika Verma", "email": "deepika@email.com", "city": "Mumbai", "course": web_course, "marks": 71},
    {"name": "Rohan Tiwari", "email": "rohan@email.com", "city": "Bhopal", "course": python_course, "marks": 56},
]

for s in students_data:
    Student.objects.create(**s)

print(f"Created {Student.objects.count()} students in {Course.objects.count()} courses")
"""
