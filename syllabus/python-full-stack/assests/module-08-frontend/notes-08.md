# Module 08 — Front-End for Python Developers — Teaching Notes

---

## HTML5 Fundamentals

### Semantic Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechPath Institute — Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav><!-- Navigation links --></nav>
    </header>
    <main>
        <section><!-- Page content --></section>
        <aside><!-- Sidebar --></aside>
    </main>
    <footer>
        <p>&copy; 2026 TechPath Institute, Bhopal</p>
    </footer>
    <script src="app.js"></script>
</body>
</html>
```

### Key Semantic Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `<header>` | Page/section header | Logo, navigation |
| `<nav>` | Navigation links | Menu bar |
| `<main>` | Main content area | One per page |
| `<section>` | Thematic grouping | Course listing |
| `<article>` | Self-contained content | Blog post |
| `<aside>` | Sidebar content | Filters, ads |
| `<footer>` | Page/section footer | Copyright, links |
| `<figure>` | Image with caption | Photo + description |

### HTML Forms

```html
<form action="/api/students" method="POST" id="studentForm">
    <label for="name">Full Name</label>
    <input type="text" id="name" name="name" required minlength="2" maxlength="50">

    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>

    <label for="city">City</label>
    <select id="city" name="city">
        <option value="Bhopal">Bhopal</option>
        <option value="Delhi">Delhi</option>
        <option value="Pune">Pune</option>
        <option value="Indore">Indore</option>
    </select>

    <label for="marks">Marks (0-100)</label>
    <input type="number" id="marks" name="marks" min="0" max="100">

    <button type="submit">Enroll Student</button>
</form>
```

### Accessibility Basics

- Always use `alt` on `<img>` tags
- Use `<label for="id">` with every form input
- Use semantic tags instead of `<div>` everywhere
- Test with keyboard navigation (Tab key)
- Use ARIA attributes when semantic HTML is not enough: `aria-label`, `aria-hidden`, `role`

---

## CSS3 Essentials

### Flexbox (One-Dimensional Layout)

```css
/* Horizontal navigation bar */
.navbar {
    display: flex;
    justify-content: space-between;  /* space items */
    align-items: center;             /* vertical center */
    gap: 16px;                       /* space between items */
    padding: 12px 24px;
    background: #1e293b;
    color: white;
}

/* Center a card on screen */
.center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Wrap cards in a row */
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.card-row .card {
    flex: 1 1 300px;    /* grow, shrink, min-width 300px */
}
```

### Flexbox Cheatsheet

| Property | Values | What It Does |
|----------|--------|--------------|
| `justify-content` | flex-start, center, space-between, space-around, space-evenly | Horizontal alignment |
| `align-items` | flex-start, center, flex-end, stretch | Vertical alignment |
| `flex-direction` | row, column, row-reverse, column-reverse | Main axis direction |
| `flex-wrap` | nowrap, wrap | Allow wrapping |
| `gap` | 16px, 1rem | Space between items |
| `flex` | 1 1 300px | grow shrink basis (shorthand) |

### CSS Grid (Two-Dimensional Layout)

```css
/* Dashboard layout */
.dashboard {
    display: grid;
    grid-template-columns: 250px 1fr;       /* sidebar + content */
    grid-template-rows: 60px 1fr 40px;      /* header + main + footer */
    min-height: 100vh;
}

/* Stats cards — auto-fit responsive grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
}
```

### CSS Variables

```css
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --bg: #f8fafc;
    --text: #1e293b;
    --card-bg: #ffffff;
    --border: #e2e8f0;
    --success: #16a34a;
    --danger: #dc2626;
    --radius: 8px;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 20px;
}

.btn-primary {
    background: var(--primary);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: var(--radius);
    cursor: pointer;
}
.btn-primary:hover {
    background: var(--primary-dark);
}
```

### Responsive Design

```css
/* Mobile-first approach */
.container {
    padding: 16px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Stack on mobile, side-by-side on desktop */
.layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

@media (min-width: 768px) {
    .layout {
        grid-template-columns: 250px 1fr;   /* Sidebar + content on tablet+ */
    }
}

@media (min-width: 1024px) {
    .layout {
        grid-template-columns: 280px 1fr 300px;  /* Sidebar + content + right panel */
    }
}

/* Hide sidebar on mobile */
.sidebar {
    display: none;
}
@media (min-width: 768px) {
    .sidebar {
        display: block;
    }
}
```

---

## Bootstrap 5

### Setup (CDN)

```html
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Your HTML -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
```

### Common Components

```html
<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="#">TechPath Institute</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="#">Students</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Courses</a></li>
            </ul>
        </div>
    </div>
</nav>

<!-- Cards Grid -->
<div class="container mt-4">
    <div class="row g-4">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Python Full Stack</h5>
                    <p class="card-text">8 months | ₹45,000</p>
                    <a href="#" class="btn btn-primary">View Details</a>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Table -->
<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr><th>#</th><th>Name</th><th>City</th><th>Marks</th></tr>
    </thead>
    <tbody>
        <tr><td>1</td><td>Rahul Sharma</td><td>Bhopal</td><td>85</td></tr>
    </tbody>
</table>

<!-- Alert -->
<div class="alert alert-success" role="alert">
    Student enrolled successfully!
</div>

<!-- Modal -->
<button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</button>
<div class="modal fade" id="deleteModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Confirm Delete</h5>
                <button class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">Are you sure you want to delete this student?</div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-danger">Delete</button>
            </div>
        </div>
    </div>
</div>
```

---

## JavaScript Essentials for API Calls

### DOM Manipulation

```javascript
// Select elements
const heading = document.getElementById('title');
const cards = document.querySelectorAll('.card');
const form = document.querySelector('#studentForm');

// Change content
heading.textContent = 'Student List';
heading.innerHTML = '<strong>Student List</strong>';

// Change styles
heading.style.color = '#2563eb';
heading.classList.add('active');
heading.classList.toggle('hidden');

// Create elements
const li = document.createElement('li');
li.textContent = 'Rahul Sharma — 85 marks';
document.getElementById('studentList').appendChild(li);
```

### Fetch API (GET)

```javascript
// Fetch students from your API
async function loadStudents() {
    try {
        const response = await fetch('http://localhost:8000/api/students/');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        const tbody = document.getElementById('studentBody');
        tbody.innerHTML = '';

        data.results.forEach((student, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${student.name}</td>
                <td>${student.city}</td>
                <td>${student.marks}</td>
                <td>
                    <span class="badge ${student.marks >= 40 ? 'bg-success' : 'bg-danger'}">
                        ${student.marks >= 40 ? 'Pass' : 'Fail'}
                    </span>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading students:', error);
        alert('Failed to load students. Is your API running?');
    }
}

// Load on page load
document.addEventListener('DOMContentLoaded', loadStudents);
```

### Fetch API (POST)

```javascript
// Create a new student
async function createStudent(event) {
    event.preventDefault();

    const form = event.target;
    const studentData = {
        name: form.name.value,
        email: form.email.value,
        city: form.city.value,
        course: parseInt(form.course.value),
        marks: parseInt(form.marks.value),
    };

    try {
        const response = await fetch('http://localhost:8000/api/students/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`,   // JWT token
            },
            body: JSON.stringify(studentData),
        });

        if (response.status === 201) {
            alert('Student created successfully!');
            form.reset();
            loadStudents();   // Reload the list
        } else {
            const error = await response.json();
            alert('Error: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.getElementById('studentForm').addEventListener('submit', createStudent);
```

### CORS (Cross-Origin Resource Sharing)

When your frontend (port 5500) calls your backend (port 8000), you need CORS:

```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]  # Add FIRST

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5500',    # VS Code Live Server
    'http://localhost:3000',    # React dev server
    'http://127.0.0.1:5500',
]
# Or for development only:
# CORS_ALLOW_ALL_ORIGINS = True
```

---

## HTMX — Dynamic Django Templates Without Heavy JS

### What is HTMX?
- Add `hx-*` attributes to HTML elements to make AJAX requests
- No JavaScript needed — just HTML attributes
- Perfect for Django: server returns HTML fragments, HTMX swaps them in

### Setup

```html
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

### Common Patterns

```html
<!-- Load content on click -->
<button hx-get="/api/students/" hx-target="#student-list" hx-swap="innerHTML">
    Load Students
</button>
<div id="student-list"><!-- Students appear here --></div>

<!-- Search with auto-complete (triggers after typing) -->
<input type="search"
       name="search"
       hx-get="/students/search/"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results"
       placeholder="Search students...">
<div id="results"></div>

<!-- Delete with confirmation -->
<button hx-delete="/api/students/1/"
        hx-confirm="Are you sure you want to delete this student?"
        hx-target="closest tr"
        hx-swap="outerHTML">
    Delete
</button>

<!-- Inline editing -->
<td hx-get="/students/1/edit/" hx-trigger="click" hx-swap="innerHTML">
    Rahul Sharma (click to edit)
</td>

<!-- Form submission without page reload -->
<form hx-post="/api/students/" hx-target="#student-list" hx-swap="beforeend">
    <input name="name" required>
    <input name="email" required>
    <button type="submit">Add Student</button>
</form>
```

### HTMX Attributes Cheatsheet

| Attribute | What It Does | Example |
|-----------|-------------|---------|
| `hx-get` | GET request | `hx-get="/api/students/"` |
| `hx-post` | POST request | `hx-post="/api/students/"` |
| `hx-put` | PUT request | `hx-put="/api/students/1/"` |
| `hx-delete` | DELETE request | `hx-delete="/api/students/1/"` |
| `hx-target` | Where to put the response | `hx-target="#results"` |
| `hx-swap` | How to insert | `innerHTML`, `outerHTML`, `beforeend` |
| `hx-trigger` | When to fire | `click`, `keyup delay:300ms`, `load` |
| `hx-confirm` | Show confirmation dialog | `hx-confirm="Are you sure?"` |
| `hx-indicator` | Show loading spinner | `hx-indicator="#spinner"` |

---

## Data Visualization

### Chart.js

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<canvas id="marksChart" width="400" height="200"></canvas>

<script>
// Bar chart — marks by student
const ctx = document.getElementById('marksChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Rahul', 'Priya', 'Ananya', 'Vikram', 'Neha'],
        datasets: [{
            label: 'Marks',
            data: [85, 92, 78, 45, 88],
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
        }]
    },
    options: {
        scales: { y: { beginAtZero: true, max: 100 } },
        plugins: { title: { display: true, text: 'Student Marks — TechPath Institute' } }
    }
});
</script>
```

### Chart Types

| Type | Best For |
|------|---------|
| `bar` | Comparing values (marks, counts) |
| `line` | Trends over time (attendance, enrollment) |
| `pie` / `doughnut` | Parts of a whole (city distribution) |
| `radar` | Multi-dimensional comparison |
| `scatter` | Correlation between two values |

### Loading Chart Data from Your API

```javascript
async function loadChart() {
    const response = await fetch('http://localhost:8000/api/students/stats/');
    const stats = await response.json();

    new Chart(document.getElementById('cityChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(stats.city_distribution),
            datasets: [{
                data: Object.values(stats.city_distribution),
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
            }]
        },
    });
}
loadChart();
```

---

## Streaming AI Responses (SSE)

### Server-Sent Events (SSE) — Backend (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_response(prompt: str):
    """Simulate streaming AI response word by word"""
    words = f"Hello! You asked about {prompt}. Here is a detailed answer from TechPath AI assistant.".split()
    for word in words:
        yield f"data: {word}\n\n"
        await asyncio.sleep(0.1)   # Simulate typing delay
    yield "data: [DONE]\n\n"

@app.get("/api/chat/stream")
async def chat_stream(prompt: str = "Python"):
    return StreamingResponse(
        generate_response(prompt),
        media_type="text/event-stream"
    )
```

### Consuming SSE — Frontend (JavaScript)

```javascript
async function streamChat(prompt) {
    const outputDiv = document.getElementById('chatOutput');
    outputDiv.textContent = '';

    const response = await fetch(`/api/chat/stream?prompt=${encodeURIComponent(prompt)}`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const word = line.slice(6);
                if (word === '[DONE]') return;
                outputDiv.textContent += word + ' ';
            }
        }
    }
}
```

---

## Django Template Integration

### Serving HTML from Django Views

```python
# views.py — return HTML that calls your own API
def dashboard(request):
    return render(request, 'dashboard.html')
```

```html
<!-- templates/dashboard.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <h1>Dashboard</h1>
    <div id="stats"></div>
    <script src="{% static 'js/dashboard.js' %}"></script>
</body>
</html>
```

### Static Files Setup

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

```
project/
├── static/
│   ├── css/style.css
│   └── js/dashboard.js
└── templates/
    └── dashboard.html
```

---

## Key Takeaways

| Concept | Tool | When to Use |
|---------|------|-------------|
| Page structure | HTML5 semantic tags | Always |
| Layout | Flexbox (1D), Grid (2D) | Layout design |
| Responsive | Media queries, Bootstrap | Mobile-friendly pages |
| Quick UI | Bootstrap 5 | Rapid prototyping |
| API calls | Fetch API + async/await | Consuming REST APIs |
| Dynamic Django | HTMX | Server-rendered dynamic UIs |
| Charts | Chart.js | Data visualization |
| Streaming | SSE + fetch reader | AI chat, live data |
| CORS | django-cors-headers | Frontend on different port |
