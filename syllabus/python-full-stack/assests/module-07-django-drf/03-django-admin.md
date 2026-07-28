# Django Admin Panel

**Module 07 — Django & Django REST Framework | Topic 3**

---

## What is the Django Admin?

Django comes with a built-in admin panel — a fully functional web interface where you can create, read, update, and delete records from your database. You do not need to build it yourself. It is ready out of the box.

**Analogy:** Think of the Django admin as the principal's office at TechPath Institute. The principal (admin) can see all student records, add new courses, update fee structures, and remove inactive students — all from a dashboard. Regular students (public users) cannot access this office.

**Why is it useful?**
- No need to write SQL queries to manage data
- Non-technical staff (like college clerks) can manage records
- Instant CRUD (Create, Read, Update, Delete) interface for all your models
- Built-in search, filtering, and sorting
- Handles permissions and access control

---

## Setting Up the Admin

### Step 1: Apply Migrations

Before using the admin, make sure all migrations are applied:

```bash
python manage.py migrate
```

### Step 2: Create a Superuser

A superuser is the top-level admin who has access to everything:

```bash
python manage.py createsuperuser
```

Django will ask:

```
Username: admin
Email: admin@techpath.biz
Password: ********
Password (again): ********
```

Choose a strong password. For local development, something like `admin123` is fine, but never use weak passwords in production.

### Step 3: Access the Admin Panel

Start the development server and visit `http://127.0.0.1:8000/admin/`:

```bash
python manage.py runserver
```

Log in with the superuser credentials you just created. You will see the admin dashboard with "Groups" and "Users" already available — these come from Django's built-in auth system.

---

## Registering Models

By default, only the User and Group models appear in the admin. To manage your own models, you need to register them.

### Basic Registration

Let us use a college management example with these models:

```python
# college/models.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    duration_months = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    date_of_birth = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=20, unique=True)
    method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
    ])

    def __str__(self):
        return f"{self.receipt_number} - Rs {self.amount}"
```

Now register them in `admin.py`:

```python
# college/admin.py
from django.contrib import admin
from .models import Department, Course, Student, FeePayment

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(FeePayment)
```

Refresh the admin panel and you will see all four models listed. You can now add, edit, and delete records through the web interface.

---

## Customizing with ModelAdmin

Basic registration works but looks plain. The `ModelAdmin` class lets you customize how your models appear and behave in the admin.

### list_display — Choose Which Columns to Show

By default, the admin list page shows only `__str__()` for each object. That is not very useful. Let us show more columns:

```python
# college/admin.py
from django.contrib import admin
from .models import Department, Course, Student, FeePayment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
```

Now the student list page shows a table with roll number, name, email, city, course, and active status — much more useful.

### list_filter — Add Sidebar Filters

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active', 'admission_date']
```

A filter sidebar appears on the right side of the list page. Clicking "Bhopal" shows only students from Bhopal.

### search_fields — Add a Search Box

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email', 'phone']
```

A search box appears at the top. Typing "Rahul" searches across name, roll number, email, and phone.

### ordering — Default Sort Order

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    ordering = ['roll_number']  # Sort by roll number ascending
    # ordering = ['-admission_date']  # Most recent first
```

### readonly_fields — Prevent Editing

Some fields should not be editable. For example, the admission date should stay fixed once set:

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    ordering = ['roll_number']
    readonly_fields = ['admission_date']
```

### list_per_page — Control Pagination

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_per_page = 25  # Show 25 students per page (default is 100)
```

### Complete ModelAdmin Options Reference

| Option | Purpose | Example |
|--------|---------|---------|
| `list_display` | Columns shown in list view | `['name', 'email', 'city']` |
| `list_filter` | Sidebar filter options | `['city', 'is_active']` |
| `search_fields` | Fields to search in | `['name', 'email']` |
| `ordering` | Default sort order | `['name']` or `['-created_at']` |
| `readonly_fields` | Non-editable fields | `['admission_date']` |
| `list_per_page` | Items per page | `25` |
| `list_display_links` | Which columns link to edit page | `['roll_number', 'name']` |
| `list_editable` | Fields editable directly in list view | `['is_active']` |
| `date_hierarchy` | Date-based drill-down navigation | `'admission_date'` |
| `fields` | Fields shown on edit form (and order) | `['name', 'email', 'course']` |
| `exclude` | Fields hidden from edit form | `['created_at']` |
| `prepopulated_fields` | Auto-fill slug from another field | `{'slug': ('name',)}` |

---

## Admin Actions — Bulk Operations

Admin actions let you perform operations on multiple selected objects at once. For example, marking several students as inactive.

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    actions = ['mark_inactive', 'mark_active']

    @admin.action(description='Mark selected students as INACTIVE')
    def mark_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} students marked as inactive.')

    @admin.action(description='Mark selected students as ACTIVE')
    def mark_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} students marked as active.')
```

**How to use:** In the student list page, select checkboxes next to students, choose "Mark selected students as INACTIVE" from the dropdown at the top, and click "Go." All selected students will be deactivated in one click.

---

## Inline Models — Edit Related Records on the Same Page

Imagine you are editing a student's profile and you also want to see their fee payments on the same page. Inline models make this possible.

### TabularInline — Compact Table Layout

```python
class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 1  # Show 1 empty form for adding new payments
    readonly_fields = ['receipt_number']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    inlines = [FeePaymentInline]
```

Now when you open a student's edit page, you will see their fee payments in a table at the bottom. You can add new payments, edit existing ones, or delete them — all without leaving the page.

### StackedInline — Vertical Layout

```python
class FeePaymentInline(admin.StackedInline):
    model = FeePayment
    extra = 1
```

`StackedInline` shows each related record in a vertical form layout (one field per line). Use it when related records have many fields. `TabularInline` is better when records have few fields and you want a compact table view.

| Inline Type | Layout | Best For |
|------------|--------|----------|
| `TabularInline` | Horizontal table (one row per record) | Records with 3-5 fields |
| `StackedInline` | Vertical form (one field per line) | Records with many fields |

### Inline Options

```python
class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 1                    # Empty forms to show for new records
    min_num = 0                  # Minimum number of forms
    max_num = 10                 # Maximum number of records allowed
    readonly_fields = ['receipt_number']
    can_delete = True            # Allow deleting from inline
```

---

## Inline for Courses Inside Department

Let us also show courses inside the department edit page:

```python
class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    fields = ['code', 'name', 'duration_months', 'fee', 'is_active']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'established_year']
    search_fields = ['name', 'head']
    inlines = [CourseInline]
```

Now editing a Department (like "Computer Science") shows all its courses right below.

---

## Customizing the Admin Site Title

By default, the admin header says "Django administration." You can change this to your institute's branding:

```python
# college/admin.py (at the top of the file, outside any class)
admin.site.site_header = 'TechPath Institute - Admin Portal'
admin.site.site_title = 'TechPath Admin'
admin.site.index_title = 'College Management Dashboard'
```

Now the admin panel shows "TechPath Institute - Admin Portal" in the header, "TechPath Admin" in the browser tab, and "College Management Dashboard" on the home page.

---

## Putting It All Together

Here is the complete `admin.py` for our college management system:

```python
# college/admin.py
from django.contrib import admin
from .models import Department, Course, Student, FeePayment

# Customize admin site branding
admin.site.site_header = 'TechPath Institute - Admin Portal'
admin.site.site_title = 'TechPath Admin'
admin.site.index_title = 'College Management Dashboard'


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    fields = ['code', 'name', 'duration_months', 'fee', 'is_active']


class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 1
    readonly_fields = ['receipt_number']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'established_year']
    search_fields = ['name', 'head']
    inlines = [CourseInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'duration_months', 'fee', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'city', 'course', 'is_active']
    list_filter = ['city', 'course', 'is_active']
    search_fields = ['name', 'roll_number', 'email', 'phone']
    ordering = ['roll_number']
    readonly_fields = ['admission_date']
    list_per_page = 25
    inlines = [FeePaymentInline]
    actions = ['mark_inactive', 'mark_active']

    @admin.action(description='Mark selected students as INACTIVE')
    def mark_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} students marked as inactive.')

    @admin.action(description='Mark selected students as ACTIVE')
    def mark_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} students marked as active.')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'student', 'amount', 'payment_date', 'method']
    list_filter = ['method', 'payment_date']
    search_fields = ['receipt_number', 'student__name']
    ordering = ['-payment_date']
```

---

## Summary

| Feature | How to Use |
|---------|-----------|
| Create superuser | `python manage.py createsuperuser` |
| Register a model | `admin.site.register(Model)` or `@admin.register(Model)` |
| Show columns | `list_display = ['field1', 'field2']` |
| Add filters | `list_filter = ['field1', 'field2']` |
| Add search | `search_fields = ['field1', 'field2']` |
| Sort by default | `ordering = ['field']` |
| Prevent editing | `readonly_fields = ['field']` |
| Bulk actions | Define method with `@admin.action`, add to `actions` list |
| Show related inline | Create `TabularInline` or `StackedInline`, add to `inlines` |
| Custom branding | `admin.site.site_header = 'Your Title'` |

---

## Practice Exercise

1. Create models for a college: Department, Course, Student, FeePayment
2. Register all models in admin with `list_display`, `list_filter`, and `search_fields`
3. Add a "mark as inactive" admin action for students
4. Use TabularInline to show fee payments inside the student edit page
5. Change the admin header to "TechPath Institute - Admin Portal"
6. Create a superuser and add 5 sample records through the admin panel

---

*TechPath Institute - Python Full Stack Development Course*
