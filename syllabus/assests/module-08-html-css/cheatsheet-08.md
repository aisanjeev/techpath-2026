# Cheat Sheet: HTML & CSS

**Module 08 — Quick Reference**

---

## HTML Tags

| Tag | What |
|-----|------|
| `<h1>`-`<h6>` | Headings |
| `<p>` | Paragraph |
| `<a href="">` | Link |
| `<img src="" alt="">` | Image |
| `<ul>/<ol> + <li>` | Lists |
| `<div>` | Container (block) |
| `<span>` | Container (inline) |
| `<table>` | Table |
| `<form>` | Form |
| `<input>` | Form input |
| `<button>` | Button |

---

## Semantic Tags

| Tag | Meaning |
|-----|---------|
| `<header>` | Page header |
| `<nav>` | Navigation |
| `<main>` | Main content |
| `<section>` | Content group |
| `<article>` | Independent content |
| `<footer>` | Page footer |

---

## CSS Selectors

| Selector | Targets |
|----------|---------|
| `h1` | All h1 tags |
| `.class` | Elements with class |
| `#id` | Element with ID |
| `*` | Everything |
| `a:hover` | On mouse hover |

---

## Box Model (inside → outside)

Content → Padding → Border → Margin

```css
.box {
  width: 300px;
  padding: 20px;
  border: 2px solid #ddd;
  margin: 16px;
  border-radius: 8px;
}
```

---

## Flexbox

```css
.container {
  display: flex;
  justify-content: center;   /* horizontal */
  align-items: center;        /* vertical */
  gap: 16px;                  /* spacing */
  flex-wrap: wrap;             /* wrap items */
}
```

| justify-content | Effect |
|----------------|--------|
| flex-start | Left |
| center | Center |
| flex-end | Right |
| space-between | Space between |
| space-evenly | Even space |

---

## Responsive Design

```css
/* Mobile first */
.box { width: 100%; }

/* Tablet */
@media (min-width: 768px) {
  .box { width: 50%; }
}

/* Desktop */
@media (min-width: 1024px) {
  .box { width: 33%; }
}
```

---

## Units

| Unit | Type | Use |
|------|------|-----|
| px | Fixed | Exact sizes |
| rem | Relative to root | Font sizes |
| % | Relative to parent | Widths |
| vh/vw | Viewport | Full screen |

---

## Colors

```css
color: red;              /* name */
color: #3b82f6;          /* hex */
color: rgb(59, 130, 246); /* rgb */
color: rgba(0,0,0,0.5);  /* with opacity */
```
