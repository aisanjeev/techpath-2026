# CSS3 and Modern Layouts

**Module 08 — Front-End for Python Developers | Topic 2**

---

## What Is CSS and Why Do You Need It?

In the previous topic, you built HTML pages. They work, but they look like a plain Word document from 2003 — black text on a white background, no colours, no spacing, no style.

CSS (Cascading Style Sheets) is the language that controls **how** your HTML looks. HTML is the skeleton; CSS is the skin, clothes, and makeup.

> **Analogy:** Imagine Priya builds a house (HTML). The walls, doors, and rooms are in place, but everything is bare concrete. CSS is the interior design — paint on the walls, tiles on the floor, curtains on the windows. Same house, completely different experience.

---

## CSS Basics Recap

### Three Ways to Add CSS

| Method | Where It Goes | When to Use |
|---|---|---|
| **Inline** | `style` attribute on the tag | Quick testing only — never in production |
| **Internal** | `<style>` block in `<head>` | Single-page demos |
| **External** | Separate `.css` file linked with `<link>` | Always use this in real projects |

```html
<!-- External CSS (recommended) -->
<link rel="stylesheet" href="styles.css">
```

### Selectors — Targeting the Right Elements

| Selector | Syntax | What It Targets |
|---|---|---|
| Element | `p { }` | All `<p>` tags |
| Class | `.card { }` | All elements with `class="card"` |
| ID | `#header { }` | The single element with `id="header"` |
| Descendant | `nav a { }` | All `<a>` inside `<nav>` |
| Group | `h1, h2, h3 { }` | All h1, h2, and h3 tags |
| Pseudo-class | `a:hover { }` | Links when the mouse hovers over them |

### The Box Model — Every Element Is a Box

Every HTML element is a rectangular box with four layers:

```
+------------------------------------------+
|              margin (outer space)         |
|  +------------------------------------+  |
|  |           border                    |  |
|  |  +------------------------------+  |  |
|  |  |        padding (inner space) |  |  |
|  |  |  +------------------------+  |  |  |
|  |  |  |      content           |  |  |  |
|  |  |  +------------------------+  |  |  |
|  |  +------------------------------+  |  |
|  +------------------------------------+  |
+------------------------------------------+
```

```css
.student-card {
    width: 300px;           /* content width */
    padding: 20px;          /* space inside the border */
    border: 2px solid #333; /* the border itself */
    margin: 15px;           /* space outside the border */
    box-sizing: border-box; /* width includes padding + border */
}
```

> **Tip:** Always add `box-sizing: border-box` to all elements. Without it, padding and border are added *on top of* the width, making layout calculations confusing.

```css
/* Add this at the top of every stylesheet */
*, *::before, *::after {
    box-sizing: border-box;
}
```

---

## Flexbox — One-Dimensional Layouts

Flexbox is the easiest way to arrange items in a row or column. Think of it as a shelf — you decide how items sit on that shelf.

### How to Enable Flexbox

```css
.container {
    display: flex;
}
```

That single line turns the container into a flex container. All direct children become flex items.

### Key Flexbox Properties

| Property | Applied To | What It Does | Common Values |
|---|---|---|---|
| `display: flex` | Container | Enables flexbox | `flex` |
| `flex-direction` | Container | Row or column layout | `row`, `column`, `row-reverse` |
| `justify-content` | Container | Horizontal alignment | `flex-start`, `center`, `space-between`, `space-around`, `space-evenly` |
| `align-items` | Container | Vertical alignment | `flex-start`, `center`, `stretch`, `flex-end` |
| `flex-wrap` | Container | Allow items to wrap to next line | `nowrap`, `wrap` |
| `gap` | Container | Space between items | `10px`, `1rem` |
| `flex` | Item | How much space an item takes | `1`, `2`, `0 0 auto` |

### Example: Student Dashboard Navigation Bar

```html
<nav class="dashboard-nav">
    <div class="logo">TechPath Institute</div>
    <div class="nav-links">
        <a href="/dashboard">Dashboard</a>
        <a href="/courses">My Courses</a>
        <a href="/assignments">Assignments</a>
        <a href="/profile">Profile</a>
    </div>
    <div class="user-info">Welcome, Sneha</div>
</nav>
```

```css
.dashboard-nav {
    display: flex;
    justify-content: space-between;  /* logo left, links center, user right */
    align-items: center;             /* vertically centered */
    padding: 10px 20px;
    background-color: #1a1a2e;
    color: white;
}

.nav-links {
    display: flex;
    gap: 20px;          /* 20px space between each link */
}

.nav-links a {
    color: #e0e0e0;
    text-decoration: none;
}

.nav-links a:hover {
    color: #00d4ff;
}
```

### Example: Course Cards in a Row (with Wrapping)

```css
.course-grid {
    display: flex;
    flex-wrap: wrap;       /* cards wrap to next line on small screens */
    gap: 20px;
    padding: 20px;
}

.course-card {
    flex: 1 1 280px;       /* grow, shrink, minimum 280px wide */
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: white;
}
```

---

## CSS Grid — Two-Dimensional Layouts

Flexbox handles rows *or* columns. CSS Grid handles **both at the same time** — rows and columns together, like an Excel spreadsheet.

### How to Enable Grid

```css
.container {
    display: grid;
    grid-template-columns: 250px 1fr 1fr;   /* 3 columns */
    grid-template-rows: 60px 1fr 50px;       /* 3 rows */
    grid-gap: 15px;                          /* space between cells */
}
```

### Key Grid Properties

| Property | What It Does | Example |
|---|---|---|
| `grid-template-columns` | Define column sizes | `200px 1fr 1fr` |
| `grid-template-rows` | Define row sizes | `auto 1fr auto` |
| `grid-gap` (or `gap`) | Space between rows and columns | `15px` |
| `grid-column` | Span an item across columns | `grid-column: 1 / 3` |
| `grid-row` | Span an item across rows | `grid-row: 1 / 3` |
| `grid-area` | Name and place an item | `grid-area: sidebar` |
| `fr` | Fractional unit (share of free space) | `1fr 2fr` (1:2 ratio) |

### Example: Student Dashboard Layout

```html
<div class="dashboard">
    <header class="dash-header">TechPath Student Dashboard</header>
    <nav class="dash-sidebar">
        <a href="#">Dashboard</a>
        <a href="#">Courses</a>
        <a href="#">Assignments</a>
        <a href="#">Grades</a>
        <a href="#">Settings</a>
    </nav>
    <main class="dash-content">
        <h2>Welcome back, Amit!</h2>
        <p>You have 3 pending assignments and 1 upcoming quiz.</p>
    </main>
    <footer class="dash-footer">TechPath Institute, Bhopal</footer>
</div>
```

```css
.dashboard {
    display: grid;
    grid-template-columns: 220px 1fr;
    grid-template-rows: 60px 1fr 40px;
    grid-template-areas:
        "header  header"
        "sidebar content"
        "footer  footer";
    min-height: 100vh;
}

.dash-header  { grid-area: header;  background: #1a1a2e; color: white; }
.dash-sidebar { grid-area: sidebar; background: #f0f0f0; padding: 20px; }
.dash-content { grid-area: content; padding: 20px; }
.dash-footer  { grid-area: footer;  background: #333; color: white; }
```

### When to Use Flexbox vs Grid

| Situation | Use |
|---|---|
| Navigation bar (single row) | Flexbox |
| Card list that wraps | Flexbox |
| Full page layout (header, sidebar, content, footer) | Grid |
| Dashboard with fixed columns and rows | Grid |
| Centering a single element | Flexbox (`justify-content: center; align-items: center`) |

---

## Responsive Design — One Site, Every Screen

In India, over 70% of internet users browse on mobile phones. Your website must look good on a phone screen (360px wide) and on a desktop monitor (1920px wide).

### Media Queries

Media queries let you apply different CSS rules based on screen size.

```css
/* Mobile first: default styles are for small screens */

.course-grid {
    display: flex;
    flex-direction: column;   /* stack cards vertically on mobile */
    gap: 15px;
}

/* Tablet and up (768px+) */
@media (min-width: 768px) {
    .course-grid {
        flex-direction: row;
        flex-wrap: wrap;
    }

    .course-card {
        flex: 1 1 45%;        /* two cards per row */
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .course-card {
        flex: 1 1 30%;        /* three cards per row */
    }
}
```

### Common Breakpoints

| Name | Width | Devices |
|---|---|---|
| Small (mobile) | Up to 767px | Phones |
| Medium (tablet) | 768px — 1023px | Tablets, small laptops |
| Large (desktop) | 1024px and above | Laptops, desktops |

### Mobile-First Approach

Always write your base CSS for mobile screens, then add complexity for larger screens using `min-width` media queries. This is called **mobile-first** design.

Why? Because it is easier to add features for bigger screens than to remove them for smaller ones.

---

## CSS Variables (Custom Properties)

CSS Variables let you define values once and reuse them everywhere — just like variables in Python.

```css
:root {
    /* Define variables */
    --primary-color: #1a1a2e;
    --accent-color: #00d4ff;
    --text-color: #333;
    --bg-color: #f5f5f5;
    --card-radius: 8px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
}

/* Use variables */
.dashboard-nav {
    background-color: var(--primary-color);
    padding: var(--spacing-md);
}

.course-card {
    border-radius: var(--card-radius);
    margin-bottom: var(--spacing-md);
}

a:hover {
    color: var(--accent-color);
}
```

> **Why use variables?** If TechPath decides to change its brand colour from dark blue to green, you change one line (`--primary-color: #2e7d32`) and every element using that variable updates automatically. Without variables, you would search and replace across hundreds of lines.

---

## Bootstrap 5 — A CSS Framework

Writing all CSS from scratch takes time. **Bootstrap** is a free CSS framework made by Twitter that gives you ready-made components and a grid system. It is the most popular CSS framework in the world.

### Adding Bootstrap to Your Project

```html
<!-- Add to <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet">

<!-- Add before </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js">
</script>
```

### Bootstrap Grid System

Bootstrap divides the screen into **12 columns**. You choose how many columns each element spans.

```html
<div class="container">
    <div class="row">
        <div class="col-md-4">Course 1</div>   <!-- 4 of 12 columns -->
        <div class="col-md-4">Course 2</div>   <!-- 4 of 12 columns -->
        <div class="col-md-4">Course 3</div>   <!-- 4 of 12 columns -->
    </div>
</div>
```

| Class | Columns Spanned | Width |
|---|---|---|
| `col-12` | 12 (full width) | 100% |
| `col-md-6` | 6 (half width, medium screens+) | 50% |
| `col-md-4` | 4 (one-third, medium screens+) | 33.3% |
| `col-md-3` | 3 (one-quarter, medium screens+) | 25% |
| `col-lg-8` | 8 (two-thirds, large screens+) | 66.7% |

### Bootstrap Utility Classes

Instead of writing custom CSS, Bootstrap provides utility classes:

```html
<!-- Spacing -->
<div class="p-3 m-2">Padding 3, Margin 2</div>
<div class="mt-4">Margin-top 4</div>
<div class="px-3 py-2">Padding x-axis 3, y-axis 2</div>

<!-- Text -->
<p class="text-center text-primary fw-bold">Centered, blue, bold</p>

<!-- Background -->
<div class="bg-dark text-white p-3">Dark background, white text</div>

<!-- Display -->
<div class="d-flex justify-content-between align-items-center">Flexbox row</div>
<div class="d-none d-md-block">Hidden on mobile, visible on tablet+</div>
```

### Example: Student Registration Form with Bootstrap

```html
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow">
                <div class="card-header bg-dark text-white">
                    <h4 class="mb-0">Student Registration — TechPath Institute</h4>
                </div>
                <div class="card-body">
                    <form>
                        <div class="mb-3">
                            <label for="name" class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="name"
                                   placeholder="e.g. Rahul Verma" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email"
                                   placeholder="rahul@example.com" required>
                        </div>
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label for="phone" class="form-label">Mobile</label>
                                <input type="tel" class="form-control" id="phone"
                                       placeholder="9876543210">
                            </div>
                            <div class="col-md-6">
                                <label for="city" class="form-label">City</label>
                                <select class="form-select" id="city">
                                    <option>Bhopal</option>
                                    <option>Delhi</option>
                                    <option>Pune</option>
                                    <option>Hyderabad</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox"
                                   id="terms" required>
                            <label class="form-check-label" for="terms">
                                I agree to the terms and conditions
                            </label>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            Register
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
```

---

## Summary

| Concept | What You Learned |
|---|---|
| CSS Basics | Selectors, properties, and the box model |
| Flexbox | One-dimensional layouts with `display: flex`, `justify-content`, `align-items`, `gap` |
| CSS Grid | Two-dimensional layouts with `grid-template-columns`, `grid-template-areas` |
| Responsive Design | Media queries with mobile-first approach |
| CSS Variables | Define once with `--name`, use anywhere with `var(--name)` |
| Bootstrap 5 | 12-column grid, utility classes, ready-made components |

---

**Next Topic:** JavaScript and DOM Manipulation — making your pages interactive.
