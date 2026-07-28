# Module 08 — HTML & CSS — Quick Revision Notes

---

## HTML Basics
- **HTML** = Structure (skeleton) | **CSS** = Styling (skin) | **JS** = Behavior (muscles)
- Every HTML file starts with `<!DOCTYPE html>`
- Tags come in pairs: `<p>text</p>` (except self-closing: `<img>`, `<br>`, `<input>`)

## Essential Tags
| Tag | Purpose | Example |
|-----|---------|---------|
| `<h1>-<h6>` | Headings (h1=biggest) | `<h1>Title</h1>` |
| `<p>` | Paragraph | `<p>Text here</p>` |
| `<a href="">` | Link | `<a href="https://...">Click</a>` |
| `<img src="" alt="">` | Image | `<img src="photo.jpg" alt="desc">` |
| `<ul>/<ol>` + `<li>` | Lists (unordered/ordered) | `<ul><li>Item</li></ul>` |
| `<div>` | Generic container | Grouping elements |
| `<span>` | Inline container | Styling part of text |
| `<table>` | Table | `<table><tr><td>Cell</td></tr></table>` |
| `<form>` | Form container | `<form action="/submit">...</form>` |
| `<input>` | Form input | `<input type="text" name="email">` |
| `<button>` | Clickable button | `<button>Submit</button>` |

## Semantic HTML
| Tag | Meaning |
|-----|---------|
| `<header>` | Page/section header |
| `<nav>` | Navigation links |
| `<main>` | Main content |
| `<section>` | Thematic section |
| `<article>` | Independent content |
| `<aside>` | Sidebar content |
| `<footer>` | Page/section footer |

## CSS Selectors
| Selector | Targets | Example |
|----------|---------|---------|
| `element` | All of that element | `p { color: red; }` |
| `.class` | Elements with class | `.card { border: 1px; }` |
| `#id` | One specific element | `#header { height: 60px; }` |
| `parent child` | Nested elements | `nav a { color: white; }` |
| `:hover` | On mouse hover | `button:hover { opacity: 0.8; }` |
| `::before/after` | Pseudo-elements | `.card::before { content: ""; }` |

## Specificity (Which CSS Wins)
Inline (1000) > ID (100) > Class (10) > Element (1)

## Box Model
```
┌─────── Margin (outside) ──────┐
│ ┌──── Border ────┐            │
│ │ ┌── Padding ──┐│            │
│ │ │  Content    ││            │
│ │ └─────────────┘│            │
│ └────────────────┘            │
└───────────────────────────────┘
```
Always use: `* { box-sizing: border-box; }`

## Flexbox (1D Layout)
```css
.container {
  display: flex;
  justify-content: center;    /* horizontal */
  align-items: center;         /* vertical */
  gap: 16px;                   /* space between */
  flex-wrap: wrap;             /* allow wrapping */
}
```

## CSS Grid (2D Layout)
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
```

## Responsive Design
```css
/* Mobile-first: write mobile CSS first, then add for larger */
@media (min-width: 768px) { /* tablet+ */ }
@media (min-width: 1024px) { /* desktop+ */ }
```

## CSS Variables
```css
:root { --primary: #6366f1; --text: #0f172a; }
.btn { background: var(--primary); color: var(--text); }
```

## Units
| Unit | Type | Use |
|------|------|-----|
| `px` | Absolute | Borders, shadows |
| `rem` | Relative to root font | Font sizes, spacing |
| `%` | Relative to parent | Widths |
| `vw/vh` | Viewport width/height | Full-screen sections |
| `fr` | Fraction (Grid only) | Grid columns |

## Key Properties
| Property | Values |
|----------|--------|
| `position` | static, relative, absolute, fixed, sticky |
| `display` | block, inline, flex, grid, none |
| `overflow` | visible, hidden, scroll, auto |
| `z-index` | Higher number = on top (needs position) |
| `transition` | `property duration timing` |
| `transform` | `translateX()`, `scale()`, `rotate()` |
