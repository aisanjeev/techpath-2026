# Django Forms, Class-Based Views & Authentication

**Module 07 — Django & Django REST Framework | Topic 4**

---

## Part 1: Django Forms

### What are Django Forms?

Django Forms handle the tedious work of creating HTML forms, validating user input, and displaying error messages. Instead of writing HTML `<form>` tags and validation logic manually, Django generates it all from a Python class.

**Analogy:** Think of a college admission form. The form has fields (name, phone, course), rules (phone must be 10 digits, name cannot be empty), and error messages ("Please enter a valid phone number"). Django Forms handle all of this automatically — just like a printed form template that already has instructions and rules printed on it.

### Form vs ModelForm

Django provides two types of forms:

| Feature | `Form` | `ModelForm` |
|---------|--------|------------|
| Tied to a model? | No — you define fields manually | Yes — fields come from the model |
| Use case | Login, search, contact us | Create/edit database records |
| Saves to database? | You handle it manually | `form.save()` does it for you |
| Field definitions | You write each field | Auto-generated from model |

### Creating a Regular Form

```python
# students/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Email Address')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')
    phone = forms.CharField(max_length=10, required=False, label='Phone (Optional)')
```

### Creating a ModelForm

A ModelForm automatically creates form fields from your model:

```python
# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'city', 'gender', 'date_of_birth', 'course']
        # Or use: fields = '__all__'  (all fields)
        # Or use: exclude = ['is_active']  (all except these)

        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'e.g., Bhopal, Delhi, Pune',
                'class': 'form-control',
            }),
        }

        labels = {
            'date_of_birth': 'Date of Birth',
            'phone': 'Mobile Number',
        }
```

### Using a Form in a View

```python
# students/views.py
from django.shortcuts import render, redirect
from .forms import StudentForm

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Saves to database (ModelForm only)
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/register.html', {'form': form})
```

### Rendering a Form in a Template

```html
<!-- students/templates/students/register.html -->
<h1>Student Registration - TechPath Institute</h1>

<form method="POST">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Register</button>
</form>

{% if form.errors %}
    <div style="color: red;">
        <p>Please correct the errors below:</p>
        {{ form.errors }}
    </div>
{% endif %}
```

### Form Rendering Options

| Method | Output |
|--------|--------|
| `{{ form.as_p }}` | Each field wrapped in `<p>` tags |
| `{{ form.as_table }}` | Each field in a `<tr>` table row |
| `{{ form.as_div }}` | Each field wrapped in `<div>` tags |
| Manual rendering | Full control over HTML (see below) |

### Manual Form Rendering (Full Control)

```html
<form method="POST">
    {% csrf_token %}

    <div>
        <label for="{{ form.name.id_for_label }}">Name:</label>
        {{ form.name }}
        {% if form.name.errors %}
            <span style="color: red;">{{ form.name.errors.0 }}</span>
        {% endif %}
    </div>

    <div>
        <label for="{{ form.email.id_for_label }}">Email:</label>
        {{ form.email }}
        {% if form.email.errors %}
            <span style="color: red;">{{ form.email.errors.0 }}</span>
        {% endif %}
    </div>

    <button type="submit">Register</button>
</form>
```

### Form Validation — clean Methods

Django validates forms in stages. You can add custom validation using `clean_<fieldname>()` for a single field or `clean()` for cross-field validation.

```python
# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'city', 'date_of_birth', 'course']

    # Validate a single field
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        if phone and len(phone) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters.')
        return name

    # Cross-field validation
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        city = cleaned_data.get('city')

        # Example: students from Bhopal must use techpath.biz email
        if city == 'Bhopal' and email and '@techpath.biz' not in email:
            raise forms.ValidationError(
                'Bhopal campus students must register with a @techpath.biz email.'
            )
        return cleaned_data
```

### CSRF Protection

CSRF (Cross-Site Request Forgery) is a security attack where a malicious website tricks a user's browser into making unwanted requests. Django protects against this by default.

**How it works:**
1. Django generates a unique token for each user session
2. The `{% csrf_token %}` tag adds a hidden input with this token
3. When the form is submitted, Django checks that the token matches
4. If it does not match, Django rejects the request with a 403 error

**Rule:** Always include `{% csrf_token %}` inside every `<form method="POST">` tag. Without it, your form will not submit.

---

## Part 2: Class-Based Views (CBVs)

### Why Class-Based Views?

So far, we have written **function-based views** (FBVs). They work well for simple pages, but for common patterns like "show a list," "show details," or "create a record," you end up writing the same code again and again.

Class-Based Views provide ready-made views for common patterns. You just configure them.

**Analogy:** Think of FBVs like cooking a dish from scratch every time. CBVs are like using a recipe template — the basic steps are already written, and you just fill in the ingredients (model, template, fields).

### FBV vs CBV Comparison

Showing a list of students using both approaches:

```python
# Function-Based View (manual)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# Class-Based View (automatic)
from django.views.generic import ListView

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
```

Both do the same thing, but the CBV requires less code and follows a standard pattern.

### The Five Essential CBVs

| View | Purpose | HTTP Method | Template Convention |
|------|---------|-------------|-------------------|
| `ListView` | Show a list of objects | GET | `app/model_list.html` |
| `DetailView` | Show one object | GET | `app/model_detail.html` |
| `CreateView` | Form to create a new object | GET + POST | `app/model_form.html` |
| `UpdateView` | Form to edit an existing object | GET + POST | `app/model_form.html` |
| `DeleteView` | Confirm and delete an object | GET + POST | `app/model_confirm_delete.html` |

### ListView — Display All Students

```python
# students/views.py
from django.views.generic import ListView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20  # Show 20 students per page
    ordering = ['name']
```

Template (`students/templates/students/student_list.html`):

```html
<h1>All Students - TechPath Institute</h1>
<table>
    <tr><th>Roll No</th><th>Name</th><th>City</th><th>Course</th></tr>
    {% for student in students %}
        <tr>
            <td>{{ student.roll_number }}</td>
            <td><a href="{% url 'student_detail' student.pk %}">{{ student.name }}</a></td>
            <td>{{ student.city }}</td>
            <td>{{ student.course.name }}</td>
        </tr>
    {% empty %}
        <tr><td colspan="4">No students registered yet.</td></tr>
    {% endfor %}
</table>
```

### DetailView — Show One Student

```python
class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
```

Template (`students/templates/students/student_detail.html`):

```html
<h1>{{ student.name }}</h1>
<p>Roll Number: {{ student.roll_number }}</p>
<p>Email: {{ student.email }}</p>
<p>City: {{ student.city }}</p>
<p>Course: {{ student.course.name }}</p>
<p>Admission Date: {{ student.admission_date }}</p>

<a href="{% url 'student_update' student.pk %}">Edit</a>
<a href="{% url 'student_delete' student.pk %}">Delete</a>
```

### CreateView — Register a New Student

```python
from django.urls import reverse_lazy

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'email', 'phone', 'city', 'gender', 'date_of_birth', 'course']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
```

### UpdateView — Edit Student Details

```python
class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'email', 'phone', 'city', 'is_active']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
```

Both CreateView and UpdateView use the same template by default:

```html
<!-- students/templates/students/student_form.html -->
<h1>{% if object %}Edit Student{% else %}Register New Student{% endif %}</h1>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>

<a href="{% url 'student_list' %}">Cancel</a>
```

### DeleteView — Remove a Student

```python
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
```

Template (`students/templates/students/student_confirm_delete.html`):

```html
<h1>Delete Student</h1>
<p>Are you sure you want to delete "{{ object.name }}"?</p>

<form method="POST">
    {% csrf_token %}
    <button type="submit" style="color: red;">Yes, Delete</button>
    <a href="{% url 'student_list' %}">Cancel</a>
</form>
```

### URL Configuration for CBVs

CBVs are used in `urls.py` with `.as_view()`:

```python
# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
]
```

### Template Naming Convention Summary

If you do not specify `template_name`, Django looks for templates with these default names:

| View | Default Template Name |
|------|-----------------------|
| `ListView` | `app_name/model_list.html` |
| `DetailView` | `app_name/model_detail.html` |
| `CreateView` | `app_name/model_form.html` |
| `UpdateView` | `app_name/model_form.html` |
| `DeleteView` | `app_name/model_confirm_delete.html` |

For our Student model in the `students` app, the defaults would be `students/student_list.html`, `students/student_detail.html`, and so on.

---

## Part 3: Django Authentication

### What Does Django Auth Provide?

Django includes a complete authentication system out of the box:

- User registration
- Login and logout
- Password hashing (never stores plain text)
- Password reset via email
- Session management
- Permission and group management
- The `@login_required` decorator to protect views

### Setting Up Authentication URLs

Django provides built-in views for login, logout, and password management. Add them to your project:

```python
# techpath_college/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth URLs
    path('students/', include('students.urls')),
]
```

This single line gives you these URLs:

| URL | View | Purpose |
|-----|------|---------|
| `/accounts/login/` | LoginView | User login page |
| `/accounts/logout/` | LogoutView | Logs user out |
| `/accounts/password_change/` | PasswordChangeView | Change current password |
| `/accounts/password_change/done/` | PasswordChangeDoneView | Confirmation page |
| `/accounts/password_reset/` | PasswordResetView | Request password reset email |
| `/accounts/password_reset/done/` | PasswordResetDoneView | Email sent confirmation |
| `/accounts/reset/<uidb64>/<token>/` | PasswordResetConfirmView | Enter new password |
| `/accounts/reset/done/` | PasswordResetCompleteView | Reset complete |

### Creating the Login Template

Django's built-in auth views look for templates in `registration/`. Create the directory `templates/registration/` at the project level.

First, tell Django where to find project-level templates in `settings.py`:

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this line
        'APP_DIRS': True,
        ...
    },
]

# Where to redirect after login/logout
LOGIN_REDIRECT_URL = '/students/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'
```

Now create the login template:

```html
<!-- templates/registration/login.html -->
<h1>Login - TechPath Institute</h1>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>

{% if form.errors %}
    <p style="color: red;">Invalid username or password. Please try again.</p>
{% endif %}

<p>
    <a href="{% url 'password_reset' %}">Forgot your password?</a>
</p>
<p>
    Don't have an account? <a href="{% url 'register' %}">Register here</a>
</p>
```

### User Registration View

Django does not provide a built-in registration view, but it gives you `UserCreationForm` to make one easily:

```python
# students/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
```

Template:

```html
<!-- templates/registration/register.html -->
<h1>Create Account - TechPath Institute</h1>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>

<p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
```

Add the URL:

```python
# students/urls.py
from .views import RegisterView

urlpatterns = [
    # ... other urls ...
    path('register/', RegisterView.as_view(), name='register'),
]
```

### Protecting Views with @login_required

To ensure only logged-in users can access certain pages:

```python
# For function-based views
from django.contrib.auth.decorators import login_required

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})
```

If Amit tries to visit `/students/` without logging in, Django automatically redirects him to `/accounts/login/?next=/students/`. After logging in, he is sent back to the page he originally wanted.

```python
# For class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
```

Note: `LoginRequiredMixin` must come **before** `ListView` in the class inheritance. The order matters.

### Password Reset Flow

The password reset flow works in four steps:

```
1. User visits /accounts/password_reset/
   → Enters email address
   → Django sends an email with a reset link

2. User clicks the link in the email
   → Taken to /accounts/reset/<uid>/<token>/
   → Enters new password twice

3. Django validates the token and updates the password

4. User is redirected to /accounts/reset/done/ (success page)
```

For password reset emails to work, configure email settings in `settings.py`:

```python
# settings.py

# For development: print emails to console instead of sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production: use actual email service
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Accessing User in Templates

You can check if a user is logged in and access their data in any template:

```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
{% endif %}
```

### Accessing User in Views

```python
def profile(request):
    current_user = request.user            # The logged-in user
    is_logged_in = request.user.is_authenticated  # True or False
    username = request.user.username       # e.g., 'sneha_patel'
    email = request.user.email             # e.g., 'sneha@techpath.biz'
    return render(request, 'profile.html', {'user': current_user})
```

---

## Summary

| Feature | Key Points |
|---------|-----------|
| **Form** | Standalone form, define fields manually, no model tie |
| **ModelForm** | Auto-generates fields from model, `form.save()` writes to DB |
| **clean_fieldname()** | Validates one specific field |
| **clean()** | Cross-field validation |
| **CSRF** | Always add `{% csrf_token %}` in POST forms |
| **ListView** | Shows list of objects, default template: `model_list.html` |
| **DetailView** | Shows one object, default template: `model_detail.html` |
| **CreateView** | Form to create, default template: `model_form.html` |
| **UpdateView** | Form to edit, default template: `model_form.html` |
| **DeleteView** | Confirm delete, default template: `model_confirm_delete.html` |
| **@login_required** | Decorator for function views to require authentication |
| **LoginRequiredMixin** | Mixin for class views to require authentication |
| **UserCreationForm** | Built-in form for user registration |
| **LOGIN_REDIRECT_URL** | Where to go after successful login |
| **Password Reset** | Built-in 4-step flow with email verification |

---

## Practice Exercise

Build a complete student registration system:

1. Create a `StudentForm` (ModelForm) with custom validation for phone (10 digits only)
2. Create CBVs for list, detail, create, update, and delete operations
3. Add login and registration using Django's built-in auth
4. Protect the create, update, and delete views with `LoginRequiredMixin`
5. Add a navbar that shows "Login/Register" for guests and "Welcome, username / Logout" for logged-in users
6. Configure password reset to print emails to the console

---

*TechPath Institute - Python Full Stack Development Course*
