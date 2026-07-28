# Bootstrap — Build Websites Fast

**Module 09 — JavaScript + Bootstrap | Topic 2**

---

## What is Bootstrap?

**Bootstrap** is a free CSS framework that gives you ready-made components and responsive grid system. Instead of writing CSS from scratch, you use Bootstrap's pre-built classes.

| Without Bootstrap | With Bootstrap |
|-------------------|---------------|
| Write all CSS yourself | Use ready-made classes |
| Build grid system manually | `row` + `col` classes |
| Design buttons from scratch | `btn btn-primary` |
| Hours of work | Minutes of work |

> Bootstrap was made by Twitter. It's the most popular CSS framework in the world.

---

## Setting Up Bootstrap

### Option 1: CDN Link (easiest)

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <h1 class="text-center text-primary">Hello Bootstrap!</h1>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

## Grid System — Responsive Layouts

Bootstrap divides the page into **12 columns**. You can combine columns to create any layout.

### Basic Grid

```html
<div class="container">
    <div class="row">
        <div class="col-4">Column 1 (4/12)</div>
        <div class="col-4">Column 2 (4/12)</div>
        <div class="col-4">Column 3 (4/12)</div>
    </div>
</div>
```

### Column Sizes

| Class | Width | Use For |
|-------|-------|---------|
| `col-12` | 100% (full width) | Single column |
| `col-6` | 50% | Two equal columns |
| `col-4` | 33.3% | Three equal columns |
| `col-3` | 25% | Four equal columns |
| `col-8` + `col-4` | 66% + 33% | Content + sidebar |

### Responsive Breakpoints

| Class | Screen Size | Device |
|-------|------------|--------|
| `col-` | All sizes | Default |
| `col-sm-` | 576px+ | Phone landscape |
| `col-md-` | 768px+ | Tablet |
| `col-lg-` | 992px+ | Desktop |
| `col-xl-` | 1200px+ | Large desktop |

```html
<!-- Full width on mobile, 2 columns on tablet, 3 on desktop -->
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">Card 1</div>
    <div class="col-12 col-md-6 col-lg-4">Card 2</div>
    <div class="col-12 col-md-6 col-lg-4">Card 3</div>
</div>
```

---

## Text & Typography

| Class | What It Does |
|-------|-------------|
| `text-center` | Center text |
| `text-start` | Left align |
| `text-end` | Right align |
| `text-primary` | Blue text |
| `text-danger` | Red text |
| `text-success` | Green text |
| `text-muted` | Gray text |
| `fw-bold` | Bold text |
| `fs-1` to `fs-6` | Font sizes (1=biggest) |
| `lead` | Larger paragraph text |
| `text-uppercase` | ALL CAPS |

---

## Buttons

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-outline-primary">Outline</button>
<button class="btn btn-lg btn-primary">Large Button</button>
<button class="btn btn-sm btn-primary">Small Button</button>
```

| Class | Color |
|-------|-------|
| `btn-primary` | Blue |
| `btn-secondary` | Gray |
| `btn-success` | Green |
| `btn-danger` | Red |
| `btn-warning` | Yellow |
| `btn-info` | Cyan |
| `btn-dark` | Black |
| `btn-outline-*` | Bordered, no fill |

---

## Cards

```html
<div class="card" style="width: 18rem;">
    <img src="course.jpg" class="card-img-top" alt="Course">
    <div class="card-body">
        <h5 class="card-title">Web Development</h5>
        <p class="card-text">Learn HTML, CSS, and JavaScript.</p>
        <a href="#" class="btn btn-primary">Enroll Now</a>
    </div>
</div>
```

---

## Navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="#">TechPath</a>
        <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="#">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Courses</a></li>
                <li class="nav-item"><a class="nav-link" href="#">About</a></li>
                <li class="nav-item"><a class="nav-link" href="#">Contact</a></li>
            </ul>
        </div>
    </div>
</nav>
```

---

## Forms

```html
<form class="p-4">
    <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" class="form-control" placeholder="your@email.com">
    </div>
    <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control">
    </div>
    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input">
        <label class="form-check-label">Remember me</label>
    </div>
    <button class="btn btn-primary">Login</button>
</form>
```

---

## Spacing Utilities

Bootstrap uses a numbering system for spacing: 0 to 5.

| Class | What It Does |
|-------|-------------|
| `m-3` | Margin all sides (1rem) |
| `mt-3` | Margin top |
| `mb-3` | Margin bottom |
| `ms-3` | Margin start (left) |
| `me-3` | Margin end (right) |
| `mx-3` | Margin left + right |
| `my-3` | Margin top + bottom |
| `p-3` | Padding all sides |
| `pt-3` | Padding top |
| `pb-3` | Padding bottom |

| Number | Size |
|--------|------|
| 0 | 0 |
| 1 | 0.25rem (4px) |
| 2 | 0.5rem (8px) |
| 3 | 1rem (16px) |
| 4 | 1.5rem (24px) |
| 5 | 3rem (48px) |

---

## Other Useful Components

| Component | Class | Use |
|-----------|-------|-----|
| **Alert** | `alert alert-success` | Notification messages |
| **Badge** | `badge bg-primary` | Small labels/counts |
| **Modal** | `modal` | Popup dialogs |
| **Carousel** | `carousel` | Image slider |
| **Accordion** | `accordion` | Collapsible sections |
| **Table** | `table table-striped` | Styled tables |
| **Spinner** | `spinner-border` | Loading indicator |
| **Toast** | `toast` | Small notifications |

---

## Flexbox Utilities in Bootstrap

```html
<div class="d-flex justify-content-center align-items-center gap-3">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

| Class | What |
|-------|------|
| `d-flex` | Display flex |
| `justify-content-center` | Center horizontal |
| `justify-content-between` | Space between |
| `align-items-center` | Center vertical |
| `flex-column` | Stack vertically |
| `gap-3` | Gap between items |

---

## Summary

- **Bootstrap** = ready-made CSS components and grid system
- **Grid:** 12 columns, use `col-*` classes for layout
- **Responsive:** `col-md-6` = 50% on tablet, `col-lg-4` = 33% on desktop
- **Components:** Buttons, Cards, Navbar, Forms, Modals — all pre-built
- **Spacing:** `m-*` for margin, `p-*` for padding (0-5 scale)
- **Colors:** `text-primary`, `bg-danger`, `btn-success` etc.
- Add Bootstrap via CDN link — no installation needed
