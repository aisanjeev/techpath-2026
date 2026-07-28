# HTMX for Modern Django

**Module 08 — Front-End for Python Developers | Topic 5**

---

## What Is HTMX?

Imagine you are at a restaurant. Instead of ordering the full meal every time you want more rice, you just wave at the waiter and they bring only the rice — the rest of your plate stays as it is. HTMX works the same way for web pages. Instead of reloading the entire page for a small change, HTMX fetches just the updated part from the server and swaps it into the page.

HTMX is a small JavaScript library that lets you add dynamic, interactive behavior to your web pages — **without writing any JavaScript yourself**. You use simple HTML attributes to tell the browser what to do.

**Why Python developers love HTMX:**
- You write Python (Django views) on the server — no need to learn React or Vue
- Your templates stay simple — just HTML
- No build tools, no npm, no webpack, no node_modules folder
- Works perfectly with Django's template system
- Much less code than a full JavaScript framework

---

## Installing HTMX

HTMX is just a single JavaScript file. The easiest way to add it is via a CDN script tag in your base template.

### Method 1: CDN (Quickest)

Add this line in your Django base template, just before the closing `</body>` tag:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TechPath Student Portal</title>
</head>
<body>
    {% block content %}{% endblock %}

    <!-- Add HTMX here -->
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
</body>
</html>
```

### Method 2: Download Locally

For production apps, download the file and serve it as a static file:

```bash
# Download HTMX into your Django static folder
cd myproject/static/js/
curl -O https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js
```

Then reference it in your template:

```html
<script src="{% static 'js/htmx.min.js' %}"></script>
```

| Method | Pros | Cons |
|--------|------|------|
| CDN | No setup, always latest | Needs internet, slower first load |
| Local file | Works offline, faster | Must update manually |

---

## Core HTMX Attributes

HTMX uses HTML attributes that start with `hx-`. Think of them as instructions you give to the browser: "When this happens, go fetch this URL and put the result here."

### The Big Six Attributes

| Attribute | What It Does | Example |
|-----------|-------------|---------|
| `hx-get` | Send a GET request to a URL | `hx-get="/search/"` |
| `hx-post` | Send a POST request to a URL | `hx-post="/students/add/"` |
| `hx-target` | Where to put the response HTML | `hx-target="#results"` |
| `hx-swap` | How to insert the response | `hx-swap="innerHTML"` |
| `hx-trigger` | What event triggers the request | `hx-trigger="keyup changed delay:300ms"` |
| `hx-indicator` | Show a loading spinner while waiting | `hx-indicator="#spinner"` |

### Understanding hx-swap Options

| Swap Value | What It Does |
|------------|-------------|
| `innerHTML` | Replaces the inside of the target (default) |
| `outerHTML` | Replaces the entire target element |
| `beforebegin` | Inserts before the target |
| `afterbegin` | Inserts inside target, at the start |
| `beforeend` | Inserts inside target, at the end |
| `afterend` | Inserts after the target |
| `delete` | Removes the target |
| `none` | Does not swap anything |

Think of it like arranging books on a shelf:
- `innerHTML` = Replace all books inside the shelf
- `outerHTML` = Replace the entire shelf with a new one
- `beforeend` = Add a new book at the end of the shelf
- `delete` = Remove the entire shelf

---

## Building Dynamic Pages with HTMX

### Example 1: Live Search — Student Directory

Rahul is building a student directory for TechPath Institute, Bhopal. He wants students to see results as they type — no page reload, no submit button.

**The HTML template:**

```html
<!-- templates/students/directory.html -->
{% extends "base.html" %}
{% block content %}
<h1>TechPath Student Directory</h1>

<input type="search"
       name="q"
       placeholder="Search students by name or city..."
       hx-get="/students/search/"
       hx-target="#student-list"
       hx-swap="innerHTML"
       hx-trigger="keyup changed delay:300ms"
       hx-indicator="#search-spinner">

<span id="search-spinner" class="htmx-indicator">
    Searching...
</span>

<div id="student-list">
    {% include "students/_student_rows.html" %}
</div>
{% endblock %}
```

**The partial template (just the results):**

```html
<!-- templates/students/_student_rows.html -->
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>City</th>
            <th>Course</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for student in students %}
        <tr id="student-{{ student.id }}">
            <td>{{ student.name }}</td>
            <td>{{ student.city }}</td>
            <td>{{ student.course }}</td>
            <td>
                <button hx-delete="/students/{{ student.id }}/delete/"
                        hx-target="#student-{{ student.id }}"
                        hx-swap="outerHTML"
                        hx-confirm="Are you sure you want to remove {{ student.name }}?">
                    Remove
                </button>
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="4">No students found.</td></tr>
        {% endfor %}
    </tbody>
</table>
```

**The Django view:**

```python
# views.py
from django.shortcuts import render
from .models import Student

def student_directory(request):
    students = Student.objects.all()
    return render(request, "students/directory.html", {"students": students})

def student_search(request):
    query = request.GET.get("q", "")
    students = Student.objects.all()
    if query:
        students = students.filter(name__icontains=query) | \
                   students.filter(city__icontains=query)
    return render(request, "students/_student_rows.html", {"students": students})
```

**What happens step by step:**
1. Priya types "Bho" in the search box
2. After 300ms of no more typing, HTMX sends a GET request to `/students/search/?q=Bho`
3. Django filters students whose name or city contains "Bho"
4. Django renders only the `_student_rows.html` partial — not the full page
5. HTMX replaces the content inside `#student-list` with the new rows
6. Priya sees students from Bhopal appear instantly, without any page reload

### Example 2: Inline Editing

Ananya wants to let trainers edit a student's city without opening a separate page:

```html
<!-- Display mode -->
<span hx-get="/students/5/edit-city/"
      hx-trigger="click"
      hx-swap="outerHTML"
      style="cursor: pointer; border-bottom: 1px dashed #666;">
    Bhopal
</span>
```

When the trainer clicks "Bhopal," HTMX fetches an edit form:

```html
<!-- The edit form returned by the server -->
<form hx-post="/students/5/update-city/"
      hx-swap="outerHTML">
    <input type="text" name="city" value="Bhopal" autofocus>
    <button type="submit">Save</button>
    <button hx-get="/students/5/show-city/" hx-swap="outerHTML">Cancel</button>
</form>
```

After submitting, the server returns the display mode again — all without a page reload.

### Example 3: Infinite Scroll

Amit is building a course catalog. Instead of page numbers (Page 1, 2, 3...), he wants new courses to load as the user scrolls down:

```html
<!-- templates/courses/_course_list.html -->
{% for course in courses %}
<div class="course-card">
    <h3>{{ course.title }}</h3>
    <p>{{ course.description }}</p>
    <p>Price: Rs. {{ course.price }}</p>
</div>
{% endfor %}

{% if has_more %}
<div hx-get="/courses/?page={{ next_page }}"
     hx-trigger="revealed"
     hx-swap="outerHTML"
     hx-indicator="#load-more-spinner">
    <span id="load-more-spinner" class="htmx-indicator">
        Loading more courses...
    </span>
</div>
{% endif %}
```

The `hx-trigger="revealed"` fires when the element scrolls into view — HTMX automatically loads the next batch.

### Example 4: Delete with Confirmation

The Remove button in our student directory already shows this pattern:

```html
<button hx-delete="/students/{{ student.id }}/delete/"
        hx-target="#student-{{ student.id }}"
        hx-swap="outerHTML"
        hx-confirm="Are you sure you want to remove {{ student.name }}?">
    Remove
</button>
```

`hx-confirm` shows a browser confirmation dialog. If the user clicks "OK," the DELETE request is sent. The server returns an empty string, and `outerHTML` swap replaces the entire row with nothing — the row disappears.

---

## HTMX vs React/Vue — When to Use Which

| Feature | HTMX | React / Vue |
|---------|------|-------------|
| Learning curve | Easy (just HTML attributes) | Steep (JSX, state, hooks, build tools) |
| Best for | Server-rendered apps, CRUD, dashboards | Complex SPAs, real-time apps, mobile apps |
| Language | Python (server-side) | JavaScript (client-side) |
| SEO | Naturally SEO-friendly | Needs SSR setup (Next.js, Nuxt) |
| Page transitions | Partial updates, feels fast | Full client-side routing |
| Offline support | Limited | Excellent (service workers) |
| Team size | Solo devs, small teams | Larger teams with JS expertise |
| Ecosystem | Small but growing | Massive (thousands of packages) |

**Use HTMX when:**
- You are a Python/Django developer and don't want to maintain a separate JS frontend
- Your app is mostly forms, tables, and CRUD operations
- You want quick development without build complexity
- Your team knows Python but not React

**Use React/Vue when:**
- You need rich client-side interactivity (drag-and-drop, complex animations)
- You are building a mobile app too (React Native)
- Your app needs to work offline
- You have a dedicated frontend team

Sneha, a TechPath graduate, built her company's internal HR dashboard entirely with Django + HTMX in 3 weeks. The same app with React would have taken 6-8 weeks and required a separate API layer.

---

## Integrating HTMX with Django — Important Details

### CSRF Token Handling

Django requires CSRF tokens for POST/PUT/DELETE requests. Add this to your base template so HTMX includes the token automatically:

```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    {% block content %}{% endblock %}
</body>
```

### Detecting HTMX Requests in Views

Sometimes you want to return a full page for normal requests but only a partial for HTMX requests:

```python
def student_list(request):
    students = Student.objects.all()
    context = {"students": students}

    # HTMX sends this header automatically
    if request.headers.get("HX-Request"):
        return render(request, "students/_student_rows.html", context)
    else:
        return render(request, "students/directory.html", context)
```

### URL Configuration

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.student_directory, name="student-directory"),
    path("students/search/", views.student_search, name="student-search"),
    path("students/<int:pk>/delete/", views.student_delete, name="student-delete"),
    path("students/<int:pk>/edit-city/", views.edit_city_form, name="edit-city"),
    path("students/<int:pk>/update-city/", views.update_city, name="update-city"),
]
```

---

## Quick Reference Card

```
hx-get="/url/"           → Fetch HTML from server (GET)
hx-post="/url/"          → Send data to server (POST)
hx-target="#element-id"  → Where to put the response
hx-swap="innerHTML"      → How to insert it
hx-trigger="click"       → What starts the request
hx-trigger="keyup changed delay:300ms"  → Debounced typing
hx-trigger="revealed"    → When element scrolls into view
hx-confirm="Sure?"       → Show confirmation dialog first
hx-indicator="#spinner"   → Show this element while loading
hx-headers='{...}'       → Send extra headers (like CSRF)
```

---

## Key Takeaways

1. HTMX adds interactivity to your Django pages using simple HTML attributes — no JavaScript required
2. Your Django views return HTML fragments, not JSON — this is the key difference from React/Vue
3. The core workflow is: user action triggers request, server returns HTML partial, HTMX swaps it into the page
4. Use `hx-trigger="keyup changed delay:300ms"` for live search to avoid flooding the server
5. Always handle CSRF tokens when using hx-post or hx-delete
6. HTMX is perfect for Python developers who want modern, interactive web apps without learning a JS framework

---

*TechPath Institute — Python Full Stack Development Program*
