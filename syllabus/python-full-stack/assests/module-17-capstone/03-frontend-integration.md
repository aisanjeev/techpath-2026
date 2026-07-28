# Frontend Integration: Templates, HTMX, and API Connections

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 3**

---

## Choosing Your Frontend Approach

Before writing a single line of frontend code, you need to decide how your frontend will work. Think of it like choosing how to serve food in your restaurant — you can have a buffet (server-rendered pages), a la carte (API + separate frontend), or a mix of both.

### Three Main Approaches

| Approach | How It Works | Best For | Complexity |
|----------|-------------|----------|------------|
| **Django/Jinja Templates + HTMX** | Server renders HTML, HTMX adds interactivity | Quick MVPs, admin dashboards | Low |
| **Vanilla JS + Fetch API** | Separate HTML/CSS/JS calling your FastAPI backend | Simple frontends, learning fundamentals | Medium |
| **React/Next.js SPA** | Full JavaScript framework as a separate app | Complex UIs, real-time features | High |

**Recommendation for Capstone**: Start with Django Templates + HTMX or Vanilla JS + Fetch API. These are faster to build and easier to debug. You can always upgrade later.

---

## Approach 1: Django Templates with HTMX

If you chose Django for your backend, templates are the fastest way to build your frontend. HTMX is a small JavaScript library that makes your templates interactive without writing JavaScript.

### What is HTMX?

HTMX lets you make HTTP requests directly from HTML attributes. Instead of writing JavaScript fetch calls, you add attributes like `hx-get`, `hx-post`, and `hx-swap` to your HTML elements.

Think of it like this: regular HTML forms can only submit data with a full page reload. HTMX gives HTML superpowers — now any element can make requests and update parts of the page without reloading.

### Setting Up HTMX

Add HTMX to your base template:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Capstone{% endblock %}</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <link href="/static/css/output.css" rel="stylesheet">
</head>
<body class="bg-gray-50 min-h-screen">
    <nav class="bg-white shadow p-4">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <a href="/" class="text-xl font-bold text-blue-600">My Capstone</a>
            <div class="space-x-4">
                <a href="/dashboard" class="text-gray-600 hover:text-blue-600">Dashboard</a>
                <a href="/search" class="text-gray-600 hover:text-blue-600">Search</a>
            </div>
        </div>
    </nav>
    <main class="max-w-6xl mx-auto p-6">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### HTMX Search Example

Imagine Priya is building a Student Exam Portal. She wants students to search for exam papers without reloading the page.

```html
<!-- templates/search.html -->
{% extends "base.html" %}

{% block content %}
<h1 class="text-2xl font-bold mb-6">Search Exam Papers</h1>

<!-- Search input with HTMX -->
<input
    type="text"
    name="query"
    placeholder="Search by subject, year, or college..."
    class="w-full p-3 border rounded-lg"
    hx-get="/search/results"
    hx-trigger="keyup changed delay:300ms"
    hx-target="#search-results"
    hx-indicator="#loading"
/>

<!-- Loading spinner -->
<div id="loading" class="htmx-indicator text-center py-4">
    <p class="text-gray-500">Searching...</p>
</div>

<!-- Results appear here -->
<div id="search-results" class="mt-6">
    <!-- HTMX will insert results here -->
</div>
{% endblock %}
```

```python
# Django view for search
from django.shortcuts import render

def search_results(request):
    query = request.GET.get("query", "")
    papers = ExamPaper.objects.filter(
        subject__icontains=query
    )[:20]
    return render(request, "partials/search_results.html", {"papers": papers})
```

```html
<!-- templates/partials/search_results.html -->
{% for paper in papers %}
<div class="bg-white p-4 rounded-lg shadow mb-3 border-l-4 border-blue-500">
    <h3 class="font-semibold text-lg">{{ paper.subject }}</h3>
    <p class="text-gray-600">{{ paper.college }} | {{ paper.year }}</p>
    <a href="{{ paper.file.url }}" class="text-blue-600 hover:underline mt-2 inline-block">
        Download PDF
    </a>
</div>
{% empty %}
<p class="text-gray-500 text-center py-8">No papers found. Try a different search term.</p>
{% endfor %}
```

### HTMX Key Attributes

| Attribute | What It Does | Example |
|-----------|-------------|---------|
| `hx-get` | Makes a GET request to the URL | `hx-get="/api/items"` |
| `hx-post` | Makes a POST request | `hx-post="/api/items/create"` |
| `hx-target` | Where to put the response HTML | `hx-target="#results"` |
| `hx-trigger` | What triggers the request | `hx-trigger="click"` or `"keyup delay:300ms"` |
| `hx-swap` | How to insert the response | `hx-swap="innerHTML"` or `"outerHTML"` |
| `hx-indicator` | Element to show while loading | `hx-indicator="#spinner"` |

---

## Approach 2: Vanilla JS with Fetch API

If you chose FastAPI for your backend, you will build a separate frontend that calls your API using the Fetch API.

### Project Structure

```
frontend/
|-- index.html
|-- pages/
|   |-- dashboard.html
|   |-- search.html
|   |-- login.html
|-- css/
|   |-- styles.css
|-- js/
|   |-- api.js         # API helper functions
|   |-- auth.js         # Login/logout logic
|   |-- dashboard.js    # Dashboard page logic
|   |-- search.js       # Search page logic
```

### API Helper (api.js)

```javascript
// js/api.js
const API_BASE = "http://localhost:8000/api/v1";

async function apiGet(endpoint) {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
            "Authorization": token ? `Bearer ${token}` : "",
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "/pages/login.html";
            return;
        }
        throw new Error(`API error: ${response.status}`);
    }

    return response.json();
}

async function apiPost(endpoint, data) {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: {
            "Authorization": token ? `Bearer ${token}` : "",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Something went wrong");
    }

    return response.json();
}
```

### Search Page Example

```html
<!-- pages/search.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search - My Capstone</title>
    <link href="../css/styles.css" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto p-6">
        <h1 class="text-2xl font-bold mb-6">Search Exam Papers</h1>

        <input
            type="text"
            id="searchInput"
            placeholder="Search by subject..."
            class="w-full p-3 border rounded-lg mb-6"
        />

        <div id="results" class="space-y-4">
            <!-- Results will be inserted here -->
        </div>
    </div>

    <script src="../js/api.js"></script>
    <script>
        const searchInput = document.getElementById("searchInput");
        const resultsDiv = document.getElementById("results");
        let debounceTimer;

        searchInput.addEventListener("input", function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });

        async function performSearch(query) {
            if (query.length < 2) {
                resultsDiv.innerHTML = "";
                return;
            }

            try {
                const data = await apiGet(`/papers?search=${encodeURIComponent(query)}`);
                renderResults(data.data);
            } catch (error) {
                resultsDiv.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
            }
        }

        function renderResults(papers) {
            if (papers.length === 0) {
                resultsDiv.innerHTML = '<p class="text-gray-500">No papers found.</p>';
                return;
            }

            resultsDiv.innerHTML = papers.map(paper => `
                <div class="bg-white p-4 rounded-lg shadow">
                    <h3 class="font-semibold">${paper.subject}</h3>
                    <p class="text-gray-600">${paper.college} | ${paper.year}</p>
                    <a href="${paper.file_url}" class="text-blue-600 hover:underline">
                        Download
                    </a>
                </div>
            `).join("");
        }
    </script>
</body>
</html>
```

---

## Tailwind CSS for Styling

Tailwind CSS gives you utility classes to style everything without writing custom CSS. It is like having a box of LEGO blocks — you combine small pieces to build any design.

### Setting Up Tailwind (Standalone)

```bash
# Download the standalone Tailwind CLI
# Visit: https://tailwindcss.com/blog/standalone-cli

# Or install via npm
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

### Essential Tailwind Classes

| Purpose | Classes | Example |
|---------|---------|---------|
| Spacing | `p-4`, `m-2`, `px-6`, `my-8` | Padding and margin |
| Layout | `flex`, `grid`, `grid-cols-3` | Flexbox and grid |
| Text | `text-lg`, `font-bold`, `text-gray-600` | Typography |
| Background | `bg-white`, `bg-blue-500` | Background colors |
| Border | `border`, `rounded-lg`, `shadow` | Borders and shadows |
| Responsive | `md:grid-cols-2`, `lg:text-xl` | Breakpoint prefixes |
| Hover | `hover:bg-blue-600`, `hover:underline` | Hover states |

### Responsive Card Layout

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
    <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold mb-2">Data Structures</h3>
        <p class="text-gray-600 mb-4">B.Tech CSE | 2024 | RGPV Bhopal</p>
        <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">Computer Science</span>
    </div>
    <!-- More cards... -->
</div>
```

---

## Connecting Frontend to Backend API

### Handling CORS

When your frontend (port 3000) calls your backend (port 8000), browsers block the request by default. This is called CORS (Cross-Origin Resource Sharing). You already set this up in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Handling Authentication

```javascript
// js/auth.js
async function login(email, password) {
    try {
        const response = await apiPost("/auth/login", { email, password });
        localStorage.setItem("token", response.data.access_token);
        window.location.href = "/pages/dashboard.html";
    } catch (error) {
        document.getElementById("error-message").textContent = error.message;
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/pages/login.html";
}

function isLoggedIn() {
    return localStorage.getItem("token") !== null;
}

// Protect pages that require login
if (!isLoggedIn() && !window.location.pathname.includes("login")) {
    window.location.href = "/pages/login.html";
}
```

---

## Common Frontend Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Not handling loading states | User thinks page is broken | Show a spinner or "Loading..." text |
| No error messages on API failure | User is confused when things fail | Display clear error messages |
| Hardcoding API URL | Breaks when deployed | Use environment variables or config file |
| Not escaping user input in HTML | XSS security vulnerability | Use `textContent` instead of `innerHTML` for user data |
| Forgetting responsive design | Unusable on mobile | Always test on mobile viewport (375px wide) |

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
