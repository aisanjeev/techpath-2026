# CSS — Making Web Pages Beautiful

**Module 08 — HTML & CSS | Topic 2**

---

## What is CSS?

**CSS** = Cascading Style Sheets — controls how HTML looks.

> **HTML** says "show a heading" → **CSS** says "make it blue, 32px, centered, with a shadow"

Without CSS, every website would look like a plain text document from 1995. CSS is what makes the internet beautiful.

> 🖼️ **IMAGE:** Same web page shown side by side — left: unstyled HTML (plain black text on white, default fonts, no layout), right: same HTML with CSS applied (colored, properly spaced, modern card layout, nice fonts) — labeled "Without CSS" and "With CSS"
> `css-before-after.png`

---

## 3 Ways to Add CSS

### 1. Inline (inside the tag) — Avoid this

```html
<h1 style="color: blue; font-size: 32px;">Hello</h1>
```

**Why avoid:** Mixes content with styling. Impossible to maintain in real projects.

### 2. Internal (in `<head>`) — For quick experiments

```html
<head>
    <style>
        h1 { color: blue; font-size: 32px; }
    </style>
</head>
```

### 3. External file — ALWAYS use this in real projects

```html
<!-- In your HTML file -->
<head>
    <link rel="stylesheet" href="styles.css">
</head>
```

```css
/* styles.css — separate file */
h1 {
    color: blue;
    font-size: 32px;
}
```

**Why external:** Reusable across pages, clean separation, easier to maintain, browser caches it (faster loading).

---

## CSS Syntax

```css
selector {
    property: value;
    property: value;
}
```

```css
/* Example */
h1 {
    color: #1e293b;            /* text color */
    font-size: 36px;           /* text size */
    font-weight: 700;          /* boldness */
    text-align: center;        /* alignment */
    margin-bottom: 16px;       /* space below */
}
```

---

## CSS Selectors — Targeting Elements

### Basic Selectors

| Selector | What It Targets | Example |
|----------|----------------|---------|
| `h1` | All `<h1>` elements | `h1 { color: red; }` |
| `.card` | All elements with `class="card"` | `.card { padding: 20px; }` |
| `#header` | The ONE element with `id="header"` | `#header { background: blue; }` |
| `*` | Every single element | `* { margin: 0; padding: 0; }` |

### Combinator Selectors

| Selector | What It Means | Example |
|----------|--------------|---------|
| `div p` | Any `<p>` inside a `<div>` (any depth) | `div p { color: gray; }` |
| `div > p` | Direct child `<p>` only (not nested deeper) | `div > p { font-weight: bold; }` |
| `h2 + p` | The `<p>` immediately after an `<h2>` | `h2 + p { font-size: 18px; }` |
| `h2 ~ p` | All `<p>` elements after an `<h2>` (siblings) | `h2 ~ p { color: #666; }` |

### Pseudo-classes (State-based)

| Selector | When It Applies |
|----------|----------------|
| `a:hover` | When mouse hovers over a link |
| `a:active` | When link is being clicked |
| `a:visited` | After link has been clicked |
| `input:focus` | When input field is selected/active |
| `li:first-child` | First item in a list |
| `li:last-child` | Last item in a list |
| `li:nth-child(3)` | Third item |
| `li:nth-child(even)` | Every even item (2nd, 4th, 6th) |
| `input:required` | Required form fields |
| `input:invalid` | Fields with invalid input |

### Pseudo-elements (Part of an element)

| Selector | What It Targets |
|----------|----------------|
| `p::first-line` | First line of a paragraph |
| `p::first-letter` | First letter (for drop caps) |
| `div::before` | Insert content before element |
| `div::after` | Insert content after element |
| `::placeholder` | Placeholder text in inputs |
| `::selection` | Text that user selects/highlights |

```css
/* Custom text selection color */
::selection {
    background: #6366f1;
    color: white;
}

/* Add a required star after labels */
label.required::after {
    content: " *";
    color: red;
}
```

### Class vs ID — When to Use Which

| | Class `.` | ID `#` |
|-|-----------|--------|
| **How many?** | Many elements can share one class | Only ONE element per ID |
| **Reusable?** | Yes — `.card` on all cards | No — `#main-header` on one element |
| **CSS priority** | Lower | Higher |
| **Use for** | Styling multiple similar elements | Unique elements, JavaScript targets, page anchors |

**Real-world rule:** Use classes for 99% of your CSS. IDs are mainly for JavaScript and page navigation anchors.

---

## Colors in CSS

### Color Formats

| Format | Example | When to Use |
|--------|---------|-------------|
| **Name** | `color: red;` | Quick experiments only |
| **Hex** | `color: #3b82f6;` | Most common in production |
| **Hex short** | `color: #fff;` | Short for `#ffffff` |
| **RGB** | `color: rgb(59, 130, 246);` | When you need number values |
| **RGBA** | `color: rgba(0, 0, 0, 0.5);` | With transparency (0=invisible, 1=solid) |
| **HSL** | `color: hsl(217, 91%, 60%);` | Easiest to adjust (change lightness for shades) |

### Professional Color System

Don't pick random colors. Define a palette and use it consistently:

```css
:root {
    /* Primary brand color */
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;

    /* Neutral/gray scale */
    --text-dark: #0f172a;
    --text: #1e293b;
    --text-light: #64748b;
    --text-muted: #94a3b8;
    --border: #e2e8f0;
    --bg-light: #f8fafc;
    --bg-white: #ffffff;

    /* Status colors */
    --success: #22c55e;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;
}

/* Use them everywhere */
h1 { color: var(--text-dark); }
p { color: var(--text); }
.card { border: 1px solid var(--border); }
.btn { background: var(--primary); }
.btn:hover { background: var(--primary-dark); }
```

> 🖼️ **IMAGE:** A color palette card showing the above color system — primary colors (3 shades of purple), gray scale (6 shades from dark to light), and status colors (green, yellow, red, blue) — each swatch labeled with the CSS variable name and hex code
> `css-color-system-palette.png`

**Why CSS variables?** Change `--primary: #6366f1` to `--primary: #e11d48` (red) in ONE place, and your entire site changes color. This is how professional designers work.

---

## Text & Typography

```css
body {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 16px;         /* base size — everything else relative to this */
    line-height: 1.6;        /* space between lines — 1.5 to 1.8 is comfortable */
    color: #1e293b;
}

h1 {
    font-size: 2.5rem;       /* 40px (relative to root 16px) */
    font-weight: 800;        /* extra bold (100=thin, 400=normal, 700=bold, 900=black) */
    letter-spacing: -0.025em; /* tighten heading letters slightly */
    line-height: 1.2;        /* tighter line height for headings */
}

h2 { font-size: 2rem; font-weight: 700; }    /* 32px */
h3 { font-size: 1.5rem; font-weight: 600; }  /* 24px */

p {
    font-size: 1rem;         /* 16px */
    margin-bottom: 1rem;     /* space after paragraph */
    max-width: 65ch;         /* limit line length for readability (~65 characters) */
}

small, .caption { font-size: 0.875rem; color: #64748b; }  /* 14px */

.uppercase {
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
}
```

### Adding Google Fonts

```html
<!-- In <head> -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Inter', sans-serif; }
```

**Popular font pairings:**

| Heading Font | Body Font | Style |
|-------------|-----------|-------|
| Inter Bold | Inter Regular | Clean, modern (best for beginners) |
| Poppins SemiBold | Open Sans Regular | Friendly, rounded |
| Montserrat Bold | Lato Regular | Professional, geometric |
| Playfair Display | Source Sans Pro | Elegant, editorial |

---

## The Box Model — Every Element is a Box

> 🖼️ **IMAGE:** CSS Box Model diagram — nested rectangles showing Content (innermost, blue), Padding (green), Border (yellow line), and Margin (orange, outermost) — with pixel measurements on each side (top/right/bottom/left), and a note showing that `box-sizing: border-box` makes width include padding+border
> `css-box-model-detailed.png`

```css
.card {
    /* Content dimensions */
    width: 300px;
    height: auto;              /* let content decide height */

    /* Padding — space INSIDE the border (content to border) */
    padding: 24px;             /* all 4 sides */
    padding: 16px 24px;        /* top/bottom, left/right */
    padding: 10px 20px 30px 40px; /* top, right, bottom, left (clockwise) */

    /* Border — the visible line */
    border: 1px solid #e2e8f0;
    border-radius: 12px;       /* rounded corners */

    /* Margin — space OUTSIDE the border (between elements) */
    margin: 16px;
    margin: 0 auto;            /* center horizontally */

    /* Shadow — depth effect */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);

    /* IMPORTANT: makes width include padding + border */
    box-sizing: border-box;
}
```

### The `box-sizing` Fix (Use This Always)

Without `box-sizing: border-box`, a 300px wide box with 20px padding becomes 340px total. That breaks layouts.

```css
/* Add this at the TOP of every CSS file */
*, *::before, *::after {
    box-sizing: border-box;
}
```

Now `width: 300px` means the box is 300px total, including padding and border. Every professional CSS file starts with this.

---

## Flexbox — Modern Layout System

Flexbox arranges items in a row or column with powerful alignment controls.

```css
.container {
    display: flex;              /* activate flexbox */
    flex-direction: row;        /* row (default) or column */
    justify-content: center;    /* main axis alignment (horizontal for row) */
    align-items: center;        /* cross axis alignment (vertical for row) */
    gap: 16px;                  /* space between items */
    flex-wrap: wrap;            /* allow items to wrap to next line */
}
```

> 🖼️ **IMAGE:** Flexbox visual cheat sheet — 6 small diagrams arranged in a 2x3 grid, each showing colored boxes inside a container: (1) justify-content: flex-start, (2) justify-content: center, (3) justify-content: space-between, (4) align-items: flex-start, (5) align-items: center, (6) align-items: stretch — each diagram labeled with the property value
> `css-flexbox-visual-guide.png`

### justify-content (Main Axis)

| Value | What It Does |
|-------|-------------|
| `flex-start` | Items packed at start (left for row) |
| `flex-end` | Items packed at end (right) |
| `center` | Items centered |
| `space-between` | First item at start, last at end, equal space between |
| `space-around` | Equal space around each item |
| `space-evenly` | Perfectly equal spaces everywhere |

### align-items (Cross Axis)

| Value | What It Does |
|-------|-------------|
| `flex-start` | Items at top |
| `flex-end` | Items at bottom |
| `center` | Items vertically centered |
| `stretch` | Items stretch to fill container height (default) |
| `baseline` | Items aligned by their text baseline |

### Real-World Flexbox Patterns

```css
/* Navbar: logo left, links right */
nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
}

/* Center something on the entire page */
.hero {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Footer columns */
.footer {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 32px;
}
```

---

## CSS Grid — Two-Dimensional Layout

Grid works in BOTH rows AND columns. Perfect for page layouts and card grids.

```css
/* 3-column card grid */
.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* 3 equal columns */
    gap: 24px;
}

/* Auto-responsive grid (NO media query needed!) */
.auto-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}
```

> 🖼️ **IMAGE:** CSS Grid layout examples — top shows a 3-column equal grid with 6 cards, bottom shows the same grid responsively wrapping to 2 columns and then 1 column as the viewport gets smaller — with the CSS code `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` shown below
> `css-grid-responsive.png`

### Grid vs Flexbox — When to Use Which

| Use | Flexbox | Grid |
|-----|---------|------|
| **Direction** | One-dimensional (row OR column) | Two-dimensional (rows AND columns) |
| **Navbar** | ✅ Perfect | Overkill |
| **Card grid** | Works with wrap | ✅ Better (even spacing) |
| **Page layout** | Not ideal | ✅ Perfect |
| **Centering** | ✅ Easy | Also easy |
| **Uneven items** | ✅ Handles well | Items fit grid strictly |

**Simple rule:** Use Flexbox for components (navbar, buttons, cards). Use Grid for page layout and multi-column grids.

### Full Page Layout with Grid

```css
body {
    display: grid;
    grid-template-rows: auto 1fr auto;  /* header, main (fills space), footer */
    min-height: 100vh;
}

/* Sidebar layout */
.page {
    display: grid;
    grid-template-columns: 250px 1fr;  /* 250px sidebar + flexible main */
    gap: 0;
}
```

---

## Responsive Design — Works on Every Screen

### The Viewport Meta Tag (Required)

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Without this, mobile browsers render at desktop width and zoom out — your page looks tiny on phones.

### Mobile-First Approach

Write CSS for mobile first, then add larger screen styles with `@media`:

```css
/* Default: mobile styles */
.container {
    width: 100%;
    padding: 16px;
}

.card-grid {
    display: grid;
    grid-template-columns: 1fr;        /* 1 column on mobile */
    gap: 16px;
}

/* Tablet (768px and up) */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        margin: 0 auto;
        padding: 24px;
    }
    .card-grid {
        grid-template-columns: repeat(2, 1fr);  /* 2 columns */
    }
}

/* Desktop (1024px and up) */
@media (min-width: 1024px) {
    .container {
        max-width: 1100px;
    }
    .card-grid {
        grid-template-columns: repeat(3, 1fr);  /* 3 columns */
    }
}
```

### Common Breakpoints

| Breakpoint | Device |
|-----------|--------|
| 0 - 767px | Mobile phones |
| 768px - 1023px | Tablets |
| 1024px - 1279px | Small laptops |
| 1280px+ | Desktops |

### Responsive Units

| Unit | What It Is | Use For |
|------|-----------|---------|
| `px` | Fixed pixels | Borders, shadows, tiny details |
| `rem` | Relative to root font-size (16px) | Font sizes, spacing, widths |
| `em` | Relative to parent font-size | Padding inside components |
| `%` | Percentage of parent | Widths, responsive containers |
| `vw` | Viewport width (100vw = full screen) | Full-width sections |
| `vh` | Viewport height (100vh = full screen) | Full-height hero sections |
| `ch` | Width of "0" character | Max-width for text (65ch = ~65 chars) |
| `fr` | Fraction of available space | Grid columns |

**Rule of thumb:** Use `rem` for most things, `%` for widths, `px` for tiny things (1px border).

---

## CSS Transitions & Hover Effects

```css
/* Smooth button hover */
.btn {
    background: #6366f1;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;    /* smooth 0.2 second transition */
}

.btn:hover {
    background: #4f46e5;
    transform: translateY(-2px);  /* lift up slightly */
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Card hover lift */
.card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

/* Color fade on links */
a {
    color: #6366f1;
    transition: color 0.2s;
}
a:hover {
    color: #4f46e5;
}
```

### Transform Properties

| Transform | Effect |
|-----------|--------|
| `translateY(-4px)` | Move up by 4px |
| `translateX(10px)` | Move right by 10px |
| `scale(1.05)` | Grow 5% bigger |
| `rotate(45deg)` | Rotate 45 degrees |
| `skewX(5deg)` | Skew/tilt |

---

## CSS Reset — Start Clean

Every browser adds default styles (margins on body, padding on lists, etc.). A CSS reset removes all of that so you start from a clean slate.

```css
/* Minimal reset — add at the TOP of your CSS file */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1e293b;
    background: #ffffff;
    -webkit-font-smoothing: antialiased;
}

img {
    max-width: 100%;
    display: block;
}

a {
    text-decoration: none;
    color: inherit;
}

ul, ol {
    list-style: none;
}

button, input, textarea, select {
    font: inherit;
}
```

**Every professional project starts with this.** Copy it into every new `styles.css` file.

---

## Practice Exercises

### Exercise 1: Style the Registration Form
Take the HTML form from the HTML chapter and style it:
- Card container (white, rounded, shadow)
- Labels above inputs (bold, smaller font)
- Inputs: full width, padding, border, rounded, focus state (colored border)
- Submit button: brand color, white text, hover effect
- Responsive: form is 600px max on desktop, full width on mobile

### Exercise 2: Flexbox Navigation
Create a navigation bar using Flexbox:
- Logo on the left, links on the right
- Links change color on hover
- Fixed to top of page (stays while scrolling)
- On mobile (below 768px): stack vertically

### Exercise 3: CSS Grid Photo Gallery
Create a 3-column photo gallery using Grid:
- 9 images in a grid (use placeholder colored boxes if no photos)
- Gap between images
- On tablet: 2 columns
- On mobile: 1 column
- Hover effect: slight zoom + shadow

### Exercise 4: Complete Page Styling
Take a plain HTML page (with header, sections, cards, form, footer) and style it completely:
- Use CSS variables for colors
- Apply the CSS reset
- Style every section professionally
- Make fully responsive
- Add hover effects on buttons and cards
- Test on your phone (use Chrome DevTools → toggle device toolbar)

> 🖼️ **IMAGE:** Chrome DevTools device toolbar button highlighted — showing how to toggle between desktop and mobile view in the browser, with an iPhone frame visible around the page preview
> `chrome-devtools-responsive-toggle.png`

---

## Summary

- **CSS** controls visual appearance — colors, fonts, layout, spacing, animations
- Always use **external CSS files** in real projects
- Use **CSS variables** (`--primary: #6366f1`) for consistent, maintainable design
- **Box Model:** content → padding → border → margin (always use `box-sizing: border-box`)
- **Flexbox** = one-direction layout (navbars, button groups, centering)
- **CSS Grid** = two-direction layout (page layouts, card grids)
- **Mobile-first:** write mobile CSS first, add larger screen styles with `@media`
- Start every project with a **CSS reset**
- Use **rem** for sizes, **%** for widths, keep **px** for tiny things
