# HTML5 for Python Developers

**Module 08 — Front-End for Python Developers | Topic 1**

---

## Why Should a Python Developer Learn HTML?

Think of it this way: you have spent weeks building a brilliant FastAPI or Django backend. It can store student records, process payments, and send emails. But without HTML, your users see nothing — just raw JSON in a browser tab.

HTML is the **face** of your application. Your API is the brain; HTML is the body that people actually interact with. Every registration form, every dashboard, every "Submit" button is HTML under the hood.

> **Analogy:** Imagine you open a restaurant in Bhopal. You hire the best chef (your Python backend), but there are no tables, no menu cards, no entrance door. Customers cannot reach the food. HTML is the dining hall — the place where your backend's work is served to real people.

---

## HTML5 Semantic Tags

Before HTML5, developers used `<div>` for everything. A page had dozens of divs with names like `div-header`, `div-nav`, `div-content`. It was messy and confusing — like labelling every room in a house as "Room 1", "Room 2", "Room 3" instead of "Kitchen", "Bedroom", "Bathroom".

HTML5 introduced **semantic tags** — tags whose names describe their purpose.

### The Seven Essential Semantic Tags

| Tag | Purpose | Real-World Analogy |
|---|---|---|
| `<header>` | Top section of a page or section | The signboard of a shop |
| `<nav>` | Navigation links | The index page of a textbook |
| `<main>` | Primary content of the page | The main hall of a building |
| `<section>` | A thematic group of content | A chapter in a book |
| `<article>` | Self-contained content (blog post, news item) | A single newspaper article |
| `<aside>` | Side content (ads, related links) | Margin notes in a notebook |
| `<footer>` | Bottom section with credits, links | The back cover of a book |

### Example: TechPath Institute Landing Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechPath Institute — Python Full Stack Course</title>
</head>
<body>

    <header>
        <h1>TechPath Institute</h1>
        <p>Your path to a tech career starts here</p>
    </header>

    <nav>
        <a href="/">Home</a>
        <a href="/courses">Courses</a>
        <a href="/about">About Us</a>
        <a href="/contact">Contact</a>
    </nav>

    <main>
        <section>
            <h2>Python Full Stack Developer Course</h2>
            <p>Learn Python, Django, FastAPI, and modern frontend skills.</p>
        </section>

        <article>
            <h3>Student Success Story</h3>
            <p>Rahul from Bhopal completed the course and landed a job
               at an IT company in Pune within 3 months.</p>
        </article>

        <aside>
            <h4>Upcoming Batch</h4>
            <p>Next batch starts: August 2026</p>
            <p>Fee: Rs. 35,000 (EMI available)</p>
        </aside>
    </main>

    <footer>
        <p>TechPath Institute, Bhopal | contact@techpath.biz</p>
    </footer>

</body>
</html>
```

### Why Semantic Tags Matter

1. **Screen readers** (used by visually impaired users) can navigate by landmarks — "jump to main content", "go to navigation".
2. **Search engines** (Google, Bing) understand your page structure better, improving your ranking.
3. **Your teammates** can read and maintain the code faster.

---

## HTML5 Forms — The Gateway Between User and Backend

Every web application needs forms. When Priya registers for a course, she fills a form. When Amit logs in, he fills a form. When Sneha submits an assignment, she uploads through a form.

As a Python developer, you will process form data in your backend. But first, the form must exist in HTML.

### Common Input Types

| Input Type | What It Does | Example Use |
|---|---|---|
| `text` | Single line of text | Student name |
| `email` | Email with built-in validation | Student email |
| `password` | Hidden text for passwords | Login password |
| `number` | Numeric input with arrows | Age, marks |
| `date` | Date picker | Date of birth |
| `tel` | Phone number | Mobile number |
| `url` | Website address | Portfolio link |
| `file` | File upload | Resume, photo |
| `checkbox` | Multiple selections (tick boxes) | Agree to terms, select subjects |
| `radio` | Single selection from a group | Gender, payment mode |

### Other Form Elements

| Element | What It Does | Example Use |
|---|---|---|
| `<select>` | Dropdown menu | Choose city, choose course |
| `<textarea>` | Multi-line text input | Address, feedback |
| `<button>` | Clickable button | Submit, Cancel |

### Complete Example: Student Registration Form

```html
<form action="/api/v1/students/register" method="POST">

    <label for="name">Full Name *</label>
    <input type="text" id="name" name="name"
           placeholder="e.g. Ananya Sharma"
           required minlength="3" maxlength="100">

    <label for="email">Email Address *</label>
    <input type="email" id="email" name="email"
           placeholder="ananya@example.com"
           required>

    <label for="phone">Mobile Number *</label>
    <input type="tel" id="phone" name="phone"
           placeholder="9876543210"
           pattern="[6-9][0-9]{9}"
           title="Enter a valid 10-digit Indian mobile number"
           required>

    <label for="dob">Date of Birth</label>
    <input type="date" id="dob" name="dob"
           min="1990-01-01" max="2010-12-31">

    <label for="course">Select Course *</label>
    <select id="course" name="course" required>
        <option value="">-- Choose a course --</option>
        <option value="python-fullstack">Python Full Stack (Rs. 35,000)</option>
        <option value="data-science">Data Science (Rs. 40,000)</option>
        <option value="devops">DevOps Engineering (Rs. 30,000)</option>
    </select>

    <label for="city">City</label>
    <select id="city" name="city">
        <option value="bhopal">Bhopal</option>
        <option value="delhi">Delhi</option>
        <option value="pune">Pune</option>
        <option value="hyderabad">Hyderabad</option>
        <option value="bangalore">Bangalore</option>
    </select>

    <label>Gender</label>
    <input type="radio" id="male" name="gender" value="male">
    <label for="male">Male</label>
    <input type="radio" id="female" name="gender" value="female">
    <label for="female">Female</label>
    <input type="radio" id="other" name="gender" value="other">
    <label for="other">Other</label>

    <label for="address">Address</label>
    <textarea id="address" name="address" rows="3"
              placeholder="Enter your full address"></textarea>

    <label>
        <input type="checkbox" name="terms" required>
        I agree to the terms and conditions *
    </label>

    <label>
        <input type="checkbox" name="newsletter">
        Send me course updates via email
    </label>

    <button type="submit">Register Now</button>
    <button type="reset">Clear Form</button>

</form>
```

### Form Attributes That Save You Backend Work

These attributes add **client-side validation** — the browser checks the data before it even reaches your Python server.

| Attribute | What It Does | Example |
|---|---|---|
| `required` | Field cannot be empty | `<input required>` |
| `placeholder` | Grey hint text inside the field | `placeholder="Enter name"` |
| `pattern` | Regex pattern the value must match | `pattern="[A-Za-z ]+"` |
| `min` / `max` | Minimum and maximum values (numbers/dates) | `min="18" max="60"` |
| `minlength` / `maxlength` | Character count limits | `minlength="3" maxlength="50"` |
| `step` | Increment for number inputs | `step="0.5"` |
| `disabled` | Field is visible but not editable | `<input disabled>` |
| `readonly` | Field value is sent but not editable | `<input readonly>` |

> **Important:** Client-side validation is a convenience, not a security measure. Always validate again in your Python backend. A malicious user can bypass HTML validation using browser dev tools.

---

## Accessibility Basics

Accessibility means making your website usable by everyone — including people who use screen readers, keyboard-only navigation, or have colour vision differences.

### Three Rules Every Developer Must Follow

**Rule 1: Every image needs alt text**

```html
<!-- Good -->
<img src="campus.jpg" alt="TechPath Institute campus building in Bhopal">

<!-- Bad -->
<img src="campus.jpg">

<!-- Decorative images that add no information -->
<img src="decoration.png" alt="">
```

**Rule 2: Every input needs a label**

```html
<!-- Good: label linked using "for" and "id" -->
<label for="email">Email</label>
<input type="email" id="email" name="email">

<!-- Bad: no label at all -->
<input type="email" name="email">
```

**Rule 3: Use ARIA attributes when HTML alone is not enough**

ARIA (Accessible Rich Internet Applications) attributes add extra information for screen readers.

```html
<!-- Tell screen readers this div is a navigation menu -->
<div role="navigation" aria-label="Main menu">
    <a href="/">Home</a>
    <a href="/courses">Courses</a>
</div>

<!-- Tell screen readers about a loading state -->
<div aria-live="polite" aria-busy="true">
    Loading student records...
</div>

<!-- Mark the current page in navigation -->
<a href="/courses" aria-current="page">Courses</a>
```

### Quick Accessibility Checklist

| Check | Why It Matters |
|---|---|
| All images have `alt` text | Screen readers describe images aloud |
| All form inputs have `<label>` | Screen readers announce what each field is for |
| Colour is not the only indicator | Colour-blind users cannot rely on colour alone |
| Page has a logical heading order (h1 > h2 > h3) | Screen readers use headings to navigate |
| Links have descriptive text (not "click here") | Users need to know where a link goes |

---

## How Django and Jinja2 Templates Use HTML

As a Python developer, you will rarely write plain `.html` files. Instead, you will use **template engines** that mix HTML with Python-like logic.

### Django Template Example

```html
<!-- templates/registration.html -->
{% extends "base.html" %}

{% block title %}Student Registration{% endblock %}

{% block content %}
<main>
    <h2>Register for {{ course.name }}</h2>
    <p>Fee: Rs. {{ course.fee|intcomma }}</p>

    <form method="POST" action="{% url 'register' %}">
        {% csrf_token %}

        {% for field in form %}
        <div>
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
            <span class="error">{{ field.errors.0 }}</span>
            {% endif %}
        </div>
        {% endfor %}

        <button type="submit">Register</button>
    </form>
</main>
{% endblock %}
```

### Jinja2 Template Example (Used with FastAPI)

```html
<!-- templates/students.html -->
<main>
    <h2>Student List — {{ city }} Campus</h2>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
            </tr>
        </thead>
        <tbody>
            {% for student in students %}
            <tr>
                <td>{{ student.name }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.course }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</main>
```

> **Key takeaway:** Whether you use Django, FastAPI with Jinja2, or a JavaScript frontend — the HTML you write is the same. The template engine just helps you inject dynamic data into it.

---

## Summary

| Concept | What You Learned |
|---|---|
| Why HTML matters for Python devs | Your backend needs a face — HTML is that face |
| Semantic tags | Use `header`, `nav`, `main`, `section`, `article`, `aside`, `footer` instead of generic divs |
| Form input types | `text`, `email`, `number`, `date`, `tel`, `select`, `textarea`, `checkbox`, `radio` |
| Form validation attributes | `required`, `placeholder`, `pattern`, `min`, `max`, `minlength`, `maxlength` |
| Accessibility | Alt text for images, labels for inputs, ARIA for dynamic content |
| Templates | Django and Jinja2 mix HTML with Python logic using `{% %}` and `{{ }}` |

---

**Next Topic:** CSS3 and Modern Layouts — making your HTML look professional with Flexbox, Grid, and Bootstrap.
