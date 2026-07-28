# Django MVT Architecture

**Module 07 — Django & Django REST Framework | Topic 1**

---

## What is Django?

Django is a high-level Python web framework that helps you build web applications quickly and with less code. It was created to make common web development tasks fast and easy, so you can focus on writing your app rather than reinventing the wheel.

**Why Django is popular in India:**
- Used by companies like Instagram, Mozilla, Pinterest, and many Indian startups
- Excellent for building job portals, e-commerce sites, and SaaS products
- Django developers earn well in India (Rs 5-18 LPA for freshers with good skills)
- Huge community — easy to find answers to your questions

**Django's motto:** *"The web framework for perfectionists with deadlines."*

---

## The MVT Pattern — Django's Architecture

Most web frameworks follow an architectural pattern to organize code. Django uses the **MVT** pattern, which stands for **Model - View - Template**.

### The Restaurant Analogy

Think of a Django application like a restaurant in Bhopal:

| Restaurant Role | Django Component | What It Does |
|----------------|-----------------|-------------|
| **Menu card** | **URL Router** | Customer (browser) reads the menu (URL) and places an order (request) |
| **Host / Receptionist** | **URL Dispatcher** | Directs the customer's order to the right chef |
| **Chef** | **View** | Receives the order, gets ingredients from kitchen, prepares the dish |
| **Kitchen / Pantry** | **Model** | Stores all raw ingredients (data), chef fetches what they need |
| **Plate / Presentation** | **Template** | The dish is plated beautifully and served to the customer (HTML response) |

When Rahul visits `techpath.biz/courses/`, here is what happens:

1. The **URL dispatcher** sees `/courses/` and knows which **View** to call
2. The **View** asks the **Model** for a list of courses from the database
3. The **Model** queries the database and returns course data
4. The **View** passes the data to a **Template**
5. The **Template** renders a beautiful HTML page with the course list
6. The HTML page is sent back to Rahul's browser

### MVT vs MVC — What is the Difference?

If you have read about frameworks like Spring or Laravel, you have seen the **MVC** (Model-View-Controller) pattern. Django's MVT is very similar:

| MVC (Other Frameworks) | MVT (Django) | Role |
|------------------------|-------------|------|
| Model | Model | Handles data and database |
| View | Template | What the user sees (HTML) |
| Controller | View | Business logic, processes requests |

The naming is slightly confusing — Django's "View" does the job of a traditional "Controller", and Django's "Template" does the job of a traditional "View." Just remember: **in Django, Views handle logic, Templates handle display.**

---

## Creating a Django Project

### Step 1: Install Django

```bash
pip install django
```

Verify installation:

```bash
python -m django --version
# Output: 5.1.x
```

### Step 2: Create a Project

```bash
django-admin startproject techpath_college
```

This creates the following structure:

```
techpath_college/
    manage.py
    techpath_college/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

### Step 3: Run the Development Server

```bash
cd techpath_college
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. You will see the Django welcome page with a rocket.

---

## Understanding the Project Structure

Let us look at each file Django created:

| File | Purpose | Analogy |
|------|---------|---------|
| `manage.py` | Command-line tool for your project | The restaurant manager — handles all operations |
| `settings.py` | All project configuration | The restaurant's rule book — timings, menu rules, staff |
| `urls.py` | URL routing — maps URLs to views | The menu card — tells which URL goes where |
| `wsgi.py` | Entry point for production servers | The front door for traditional serving |
| `asgi.py` | Entry point for async servers | The front door for modern async serving |
| `__init__.py` | Makes the folder a Python package | A name plate on the restaurant door |

### The `manage.py` File

You will use `manage.py` for almost everything. Here are the most common commands:

```bash
python manage.py runserver          # Start development server
python manage.py startapp myapp     # Create a new app
python manage.py makemigrations     # Create database migration files
python manage.py migrate            # Apply migrations to database
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Open interactive Python shell
python manage.py collectstatic      # Collect static files for production
```

### The `settings.py` File

This is the brain of your project. Key settings every beginner should know:

```python
# settings.py

# Security key — keep this SECRET in production
SECRET_KEY = 'django-insecure-abc123...'

# Turn this OFF in production
DEBUG = True

# Which domains can access your site
ALLOWED_HOSTS = []  # Add your domain here for production

# Apps installed in your project
INSTALLED_APPS = [
    'django.contrib.admin',       # Admin panel
    'django.contrib.auth',        # Authentication system
    'django.contrib.contenttypes',# Content type framework
    'django.contrib.sessions',    # Session management
    'django.contrib.messages',    # Flash messages
    'django.contrib.staticfiles', # CSS, JS, images
]

# Database configuration (default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Language and timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'   # Set to Indian timezone
```

---

## Creating a Django App

A Django **project** can contain multiple **apps**. Think of it this way:

- **Project** = The entire college (TechPath Institute)
- **App** = One department (courses, students, attendance, fees)

Each app handles one specific feature. This keeps your code organized.

### Creating an App

```bash
python manage.py startapp courses
```

This creates:

```
courses/
    __init__.py
    admin.py        # Register models for admin panel
    apps.py         # App configuration
    models.py       # Database models (tables)
    tests.py        # Unit tests
    views.py        # Business logic
    migrations/     # Database migration files
        __init__.py
```

### Register the App in settings.py

After creating an app, you must tell Django about it:

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',  # Add your app here
]
```

If you forget this step, Django will not detect your models or templates.

---

## URL Routing — How Django Maps URLs

URL routing tells Django: "When someone visits this URL, run this view function."

### Project-Level URLs

```python
# techpath_college/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),   # Delegate to app URLs
    path('students/', include('students.urls')),
]
```

### App-Level URLs

Create a file `courses/urls.py`:

```python
# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.course_create, name='course_create'),
]
```

### How `path()` Works

```python
path('courses/<int:course_id>/', views.course_detail, name='course_detail')
#     ^-- URL pattern              ^-- view function     ^-- URL name
```

| Part | Meaning |
|------|---------|
| `'courses/<int:course_id>/'` | URL pattern — `<int:course_id>` captures a number from the URL |
| `views.course_detail` | The view function to call when this URL is visited |
| `name='course_detail'` | A name for this URL — use it in templates and redirects |

### URL Path Converters

| Converter | Example URL | What It Captures |
|-----------|-------------|------------------|
| `<int:id>` | `/courses/5/` | Integer: `5` |
| `<str:slug>` | `/courses/python-basics/` | String: `python-basics` |
| `<slug:slug>` | `/courses/python-101/` | Slug (letters, numbers, hyphens): `python-101` |
| `<uuid:pk>` | `/users/550e8400-...` | UUID value |

### How `include()` Works

`include()` lets you split URLs across apps. When Django sees `courses/` in the main `urls.py`, it strips that prefix and passes the rest to `courses/urls.py`.

```
User visits: /courses/5/
                |
    Main urls.py matches "courses/" → delegates to courses/urls.py
                |
    courses/urls.py matches "5/" → calls course_detail(request, course_id=5)
```

---

## Writing Your First View

A view is a Python function (or class) that receives a web request and returns a web response.

### Simple View (HttpResponse)

```python
# courses/views.py
from django.http import HttpResponse

def course_list(request):
    return HttpResponse("<h1>Welcome to TechPath Courses</h1>")
```

### View with Template

```python
# courses/views.py
from django.shortcuts import render

def course_list(request):
    courses = [
        {'name': 'Python Full Stack', 'price': 15000},
        {'name': 'Data Science', 'price': 18000},
        {'name': 'DevOps', 'price': 20000},
    ]
    return render(request, 'courses/course_list.html', {'courses': courses})
```

### The Template

Create the file at `courses/templates/courses/course_list.html`:

```html
<!-- courses/templates/courses/course_list.html -->
<!DOCTYPE html>
<html>
<head><title>TechPath Courses</title></head>
<body>
    <h1>Available Courses at TechPath Institute</h1>
    <ul>
        {% for course in courses %}
            <li>{{ course.name }} - Rs {{ course.price }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

Notice the template path convention: `app_name/templates/app_name/template.html`. This double nesting prevents name conflicts between apps.

---

## The Complete Request-Response Cycle

Let us trace what happens when Priya visits `http://127.0.0.1:8000/courses/` step by step:

```
1. Browser sends GET request to /courses/

2. Django's URL dispatcher checks techpath_college/urls.py
   → Matches "courses/" → delegates to courses/urls.py

3. courses/urls.py checks remaining URL ""
   → Matches "" → calls views.course_list(request)

4. course_list() view runs:
   → Queries the database (or uses hardcoded data)
   → Passes data to template "courses/course_list.html"

5. Template engine renders HTML:
   → Replaces {{ course.name }} with actual values
   → Loops through {% for %} blocks

6. Rendered HTML is sent back as HttpResponse

7. Priya's browser displays the courses page
```

---

## Summary

| Concept | What It Is | Key File |
|---------|-----------|----------|
| **Project** | The whole application | `settings.py`, `urls.py` |
| **App** | One feature module | `models.py`, `views.py`, `urls.py` |
| **Model** | Database table definition | `models.py` |
| **View** | Business logic handler | `views.py` |
| **Template** | HTML with dynamic data | `templates/` folder |
| **URL Router** | Maps URLs to views | `urls.py` |
| **manage.py** | Command-line tool | Root of project |
| **settings.py** | Project configuration | Inside project folder |

---

## Practice Exercise

1. Create a Django project called `college_portal`
2. Create an app called `students`
3. Add a view that shows a welcome message at `/students/`
4. Add another view at `/students/<int:roll_no>/` that shows "Student Roll No: X"
5. Set `TIME_ZONE = 'Asia/Kolkata'` in settings.py

In the next topic, we will learn about Django Models and how to interact with databases using the ORM.

---

*TechPath Institute - Python Full Stack Development Course*
