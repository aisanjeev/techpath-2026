# Cheat Sheet: Front-End for Python Developers

**Module 08 — Quick Reference**
**TechPath Institute | Python Full Stack Course**

---

## 1. HTML5 Semantic Tags

| Tag | Purpose | Example Use |
|-----|---------|-------------|
| `<header>` | Page or section header | Logo, navigation bar |
| `<nav>` | Navigation links | Menu bar, breadcrumbs |
| `<main>` | Primary content (one per page) | Course listing area |
| `<section>` | Thematic group of content | "Our Courses" block |
| `<article>` | Self-contained content | Blog post, student card |
| `<aside>` | Sidebar / related content | Filters panel, ads |
| `<footer>` | Bottom of page or section | Copyright, contact links |
| `<figure>` | Image with caption | Photo + `<figcaption>` |
| `<details>` | Collapsible content | FAQ accordion |
| `<mark>` | Highlighted text | Search result highlight |
| `<time>` | Machine-readable date/time | `<time datetime="2026-01-15">` |

---

## 2. Common Form Input Types

| Type | What It Shows | Example |
|------|--------------|---------|
| `text` | Single-line text box | Name, city |
| `email` | Email with validation | `<input type="email">` |
| `password` | Hidden characters | Login password |
| `number` | Numeric spinner | Marks, age |
| `tel` | Phone number | Mobile number |
| `date` | Date picker | Date of birth |
| `file` | File upload button | Resume, photo |
| `checkbox` | Tick box (multiple) | Agree to terms |
| `radio` | Circle (pick one) | Gender, course type |
| `range` | Slider | Rating 1-10 |
| `url` | URL with validation | Portfolio link |
| `search` | Search box with clear icon | Student search |
| `color` | Colour picker | Theme colour |
| `hidden` | Not visible to user | CSRF token, student ID |

---

## 3. CSS Flexbox Properties

| Property | Values | What It Does |
|----------|--------|--------------|
| `display` | `flex` | Activates flexbox on the container |
| `flex-direction` | `row`, `column`, `row-reverse`, `column-reverse` | Sets the main axis direction |
| `justify-content` | `flex-start`, `center`, `flex-end`, `space-between`, `space-around`, `space-evenly` | Aligns items along the main axis |
| `align-items` | `stretch`, `flex-start`, `center`, `flex-end`, `baseline` | Aligns items along the cross axis |
| `flex-wrap` | `nowrap`, `wrap`, `wrap-reverse` | Allow items to wrap to the next line |
| `gap` | `16px`, `1rem` | Space between items |
| `align-self` | `auto`, `flex-start`, `center`, `flex-end`, `stretch` | Override align-items for one child |
| `flex` | `1 1 300px` | Shorthand: grow, shrink, basis |
| `order` | `0`, `1`, `-1` | Change visual order of a child |

```css
/* Center anything on screen */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Responsive card row */
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.card-row .card {
    flex: 1 1 300px;
}
```

---

## 4. CSS Grid Properties

| Property | Values | What It Does |
|----------|--------|--------------|
| `display` | `grid` | Activates grid on the container |
| `grid-template-columns` | `1fr 1fr`, `repeat(3, 1fr)`, `200px 1fr 200px` | Defines column sizes |
| `grid-template-rows` | `auto`, `60px 1fr 40px` | Defines row sizes |
| `gap` | `20px`, `16px 24px` | Row and column gaps |
| `grid-column` | `1 / 3`, `span 2` | Child spans multiple columns |
| `grid-row` | `1 / 3`, `span 2` | Child spans multiple rows |
| `place-items` | `center`, `start end` | Shorthand for align + justify items |
| `grid-template-areas` | Named layout regions | Semantic layout names |

```css
/* Auto-fit responsive grid (no media queries needed) */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

/* Dashboard layout with named areas */
.dashboard {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: 60px 1fr 40px;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
    min-height: 100vh;
}
```

---

## 5. Media Query Breakpoints

| Breakpoint | Min-Width | Target Devices |
|------------|-----------|----------------|
| Mobile (default) | No query | Phones (< 576px) |
| Small | `576px` | Large phones |
| Medium | `768px` | Tablets |
| Large | `992px` | Laptops |
| Extra Large | `1200px` | Desktops |
| XXL | `1400px` | Large desktops |

```css
/* Mobile-first: start with phone styles, add larger screens */
.container { padding: 16px; }

@media (min-width: 768px) {
    .container { max-width: 720px; margin: 0 auto; }
}

@media (min-width: 1200px) {
    .container { max-width: 1140px; }
}
```

---

## 6. Bootstrap 5 Grid Classes

| Class | What It Does | Example |
|-------|-------------|---------|
| `container` | Centered fixed-width wrapper | `<div class="container">` |
| `container-fluid` | Full-width wrapper | `<div class="container-fluid">` |
| `row` | Flex row for columns | `<div class="row">` |
| `col` | Equal-width column | `<div class="col">` |
| `col-6` | Half width (6 of 12 columns) | `<div class="col-6">` |
| `col-md-4` | 4 columns on medium+ screens | `<div class="col-md-4">` |
| `col-lg-3` | 3 columns on large+ screens | `<div class="col-lg-3">` |
| `g-4` | Gap between columns (gutter) | `<div class="row g-4">` |
| `offset-md-2` | Push column right by 2 units | `<div class="col-md-8 offset-md-2">` |

**Common utility classes:**

| Class | What It Does |
|-------|-------------|
| `d-flex`, `d-none`, `d-md-block` | Display utilities |
| `justify-content-center` | Flex justify |
| `text-center`, `text-start` | Text alignment |
| `mt-4`, `mb-3`, `p-2`, `px-4` | Margin and padding (0-5 scale) |
| `bg-primary`, `bg-dark` | Background colours |
| `text-white`, `text-muted` | Text colours |
| `rounded`, `shadow` | Border radius, box shadow |
| `btn btn-primary` | Styled button |
| `table table-striped` | Styled table |
| `alert alert-success` | Alert message |

---

## 7. JavaScript DOM Methods

| Method | What It Does | Example |
|--------|-------------|---------|
| `document.getElementById('id')` | Select by ID | `const el = document.getElementById('name')` |
| `document.querySelector('.cls')` | Select first match (CSS selector) | `const el = document.querySelector('.card')` |
| `document.querySelectorAll('.cls')` | Select all matches | `const cards = document.querySelectorAll('.card')` |
| `el.textContent = '...'` | Set plain text | `heading.textContent = 'Hello'` |
| `el.innerHTML = '...'` | Set HTML content | `div.innerHTML = '<p>Hi</p>'` |
| `el.style.color = 'red'` | Set inline style | `el.style.display = 'none'` |
| `el.classList.add('active')` | Add a CSS class | `el.classList.add('highlight')` |
| `el.classList.remove('active')` | Remove a CSS class | `el.classList.remove('hidden')` |
| `el.classList.toggle('open')` | Toggle a CSS class | `el.classList.toggle('show')` |
| `document.createElement('div')` | Create new element | `const li = document.createElement('li')` |
| `parent.appendChild(child)` | Add child element | `list.appendChild(li)` |
| `el.remove()` | Remove element from DOM | `card.remove()` |
| `el.setAttribute('src', url)` | Set any attribute | `img.setAttribute('alt', 'Photo')` |
| `el.addEventListener('click', fn)` | Listen for events | `btn.addEventListener('click', handleClick)` |

---

## 8. Fetch API Patterns

### GET Request

```javascript
const response = await fetch('http://localhost:8000/api/students/');
const data = await response.json();
```

### POST Request

```javascript
const response = await fetch('http://localhost:8000/api/students/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ name: 'Rahul', city: 'Bhopal', marks: 85 }),
});
const result = await response.json();
```

### PUT Request (Update)

```javascript
const response = await fetch('http://localhost:8000/api/students/1/', {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ name: 'Rahul Sharma', marks: 90 }),
});
```

### DELETE Request

```javascript
const response = await fetch('http://localhost:8000/api/students/1/', {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` },
});
if (response.ok) console.log('Deleted successfully');
```

### Error Handling Pattern

```javascript
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error.message);
        alert('Something went wrong. Please try again.');
    }
}
```

---

## 9. CORS Fix

### FastAPI

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Django

```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]  # Add FIRST

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5500',
    'http://localhost:3000',
]
```

---

## 10. HTMX Attributes

| Attribute | What It Does | Example |
|-----------|-------------|---------|
| `hx-get` | Send GET request | `hx-get="/api/students/"` |
| `hx-post` | Send POST request | `hx-post="/api/students/"` |
| `hx-put` | Send PUT request | `hx-put="/api/students/1/"` |
| `hx-delete` | Send DELETE request | `hx-delete="/api/students/1/"` |
| `hx-target` | Where to put the response HTML | `hx-target="#results"` |
| `hx-swap` | How to insert the response | `innerHTML`, `outerHTML`, `beforeend`, `afterend` |
| `hx-trigger` | When to fire the request | `click`, `submit`, `keyup changed delay:300ms`, `load` |
| `hx-confirm` | Show confirm dialog first | `hx-confirm="Delete this student?"` |
| `hx-indicator` | Show loading spinner | `hx-indicator="#spinner"` |
| `hx-vals` | Extra values as JSON | `hx-vals='{"page": 2}'` |
| `hx-headers` | Extra headers as JSON | `hx-headers='{"X-CSRFToken": "..."}'` |
| `hx-push-url` | Update browser URL bar | `hx-push-url="true"` |

```html
<!-- Search with debounce -->
<input type="search" name="q"
       hx-get="/students/search/"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results">

<!-- Delete row -->
<button hx-delete="/api/students/1/"
        hx-confirm="Are you sure?"
        hx-target="closest tr"
        hx-swap="outerHTML">
    Delete
</button>
```

---

## 11. Chart.js Quick Setup

```html
<canvas id="myChart" width="400" height="200"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script>
new Chart(document.getElementById('myChart'), {
    type: 'bar',   // bar, line, pie, doughnut, radar, scatter
    data: {
        labels: ['Rahul', 'Priya', 'Ananya', 'Vikram'],
        datasets: [{
            label: 'Marks',
            data: [85, 92, 78, 45],
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
        }]
    },
    options: {
        responsive: true,
        scales: { y: { beginAtZero: true } },
        plugins: { title: { display: true, text: 'Student Marks' } }
    }
});
</script>
```

**Chart types at a glance:**

| Type | Best For |
|------|---------|
| `bar` | Comparing values (marks, counts) |
| `line` | Trends over time (attendance, enrollment) |
| `pie` / `doughnut` | Parts of a whole (city distribution) |
| `radar` | Multi-dimensional comparison |
| `scatter` | Correlation between two values |

---

## 12. SSE / Streaming Patterns

### FastAPI Backend (Server-Sent Events)

```python
from fastapi.responses import StreamingResponse

async def generate(prompt: str):
    for word in answer.split():
        yield f"data: {word}\n\n"
        await asyncio.sleep(0.1)
    yield "data: [DONE]\n\n"

@app.get("/api/chat/stream")
async def stream(prompt: str):
    return StreamingResponse(generate(prompt), media_type="text/event-stream")
```

### JavaScript Frontend (Consuming SSE)

```javascript
// Using fetch + ReadableStream (recommended for POST support)
async function streamChat(prompt) {
    const response = await fetch(`/api/chat/stream?prompt=${encodeURIComponent(prompt)}`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        for (const line of text.split('\n')) {
            if (line.startsWith('data: ')) {
                const word = line.slice(6);
                if (word === '[DONE]') return;
                outputDiv.textContent += word + ' ';
            }
        }
    }
}

// Using EventSource (simpler, GET only)
const source = new EventSource('/api/chat/stream?prompt=Hello');
source.onmessage = (event) => {
    if (event.data === '[DONE]') { source.close(); return; }
    outputDiv.textContent += event.data + ' ';
};
```

---

*TechPath Institute, Bhopal | Python Full Stack Developer Course | 2026*
