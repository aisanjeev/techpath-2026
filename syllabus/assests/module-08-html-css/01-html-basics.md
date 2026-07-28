# HTML — The Language of Web Pages

**Module 08 — HTML & CSS | Topic 1**

---

## What is HTML?

**HTML** = HyperText Markup Language — the language used to create every web page on the internet.

> **Think of building a house:**
> - **HTML** = The structure (walls, rooms, doors, windows)
> - **CSS** = The decoration (paint, furniture, curtains)
> - **JavaScript** = The electronics (lights, switches, automation)

When you right-click on any website and click "View Page Source" — that's HTML.

> 🖼️ **IMAGE:** Split view — left side shows a rendered web page (a simple profile card with name, photo, and bio), right side shows the HTML source code that creates it — with colored arrows connecting HTML elements to their visual output
> `html-source-to-output.png`

---

## How to Practice (Setup)

### Method 1: VS Code (Recommended)

1. Download VS Code from code.visualstudio.com
2. Install extension: **Live Server**
3. Create a file: `index.html`
4. Type `!` and press Tab → auto-generates HTML boilerplate
5. Right-click → Open with Live Server → see your page in browser
6. Every time you save (Ctrl+S), the browser auto-refreshes

> 🖼️ **IMAGE:** VS Code editor on the left half of screen showing HTML code, browser on right half showing the rendered page — with the Live Server icon highlighted in the bottom status bar
> `vscode-live-server-setup.png`

### Method 2: Online Editor (No Install)

- **CodePen** (codepen.io) — Write HTML/CSS/JS and see results instantly
- **JSFiddle** (jsfiddle.net) — Similar
- Good for quick experiments, not for full projects

---

## Your First HTML Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is my first web page.</p>
</body>
</html>
```

### What Each Part Means

| Tag | What It Does | Analogy |
|-----|-------------|---------|
| `<!DOCTYPE html>` | Tells browser "this is HTML5" | Book cover saying "Novel" |
| `<html lang="en">` | Root element, language is English | The book itself |
| `<head>` | Page info (title, CSS links) — NOT visible | Book's publishing info page |
| `<meta charset="UTF-8">` | Supports Hindi, emoji, special characters | Saying "this book is in Unicode" |
| `<meta name="viewport"...>` | Makes page mobile-friendly | "This book works on all screen sizes" |
| `<title>` | Text shown in browser tab | Book title on the spine |
| `<body>` | Everything visible goes here | The actual content of the book |

> 🖼️ **IMAGE:** A browser window with arrows pointing to different parts — the tab showing the `<title>` text, the page content showing `<body>` content, and the address bar showing the file name
> `html-page-anatomy-browser.png`

---

## HTML Tags — The Building Blocks

### How Tags Work

```
Opening tag     Content        Closing tag
    ↓              ↓              ↓
  <h1>      Welcome to TechPath  </h1>
```

- **Paired tags:** `<h1>content</h1>`, `<p>text</p>`, `<div>stuff</div>`
- **Self-closing tags:** `<img>`, `<br>`, `<hr>`, `<input>` (no closing tag needed)
- **Attributes:** Extra info added to tags: `<img src="photo.jpg" alt="My photo">`

---

## Text Tags

### Headings (h1 to h6)

```html
<h1>Main Title — Only ONE per page</h1>
<h2>Section Heading</h2>
<h3>Sub-section</h3>
<h4>Sub-sub-section</h4>
<h5>Minor heading</h5>
<h6>Smallest heading</h6>
```

> 🖼️ **IMAGE:** All 6 heading levels rendered in a browser, showing how they decrease in size from h1 (large, bold) to h6 (small, still bold) — with a ruler/scale on the side showing approximate pixel sizes
> `html-heading-levels.png`

**Rule:** Every page has exactly ONE `<h1>`. Google uses `<h1>` to understand what your page is about (SEO).

### Paragraphs, Bold, Italic, and More

```html
<p>This is a paragraph. Browsers add space above and below automatically.</p>

<p>This has <strong>bold text</strong> and <em>italic text</em> inside it.</p>

<p>Line one<br>Line two (br forces a line break)</p>

<hr> <!-- Horizontal line divider -->

<p>Use <mark>highlight</mark> to mark important text.</p>

<p>H<sub>2</sub>O is water. E=mc<sup>2</sup> uses superscript.</p>

<blockquote>This is a quote. It appears indented.</blockquote>

<pre>
  This text keeps
    its exact spacing
      and line breaks (useful for code)
</pre>

<code>This is inline code like a variable name</code>
```

| Tag | Renders As | When to Use |
|-----|-----------|-------------|
| `<strong>` | **Bold** | Important text (also tells Google it's important) |
| `<b>` | **Bold** | Just visual bold (no importance) |
| `<em>` | *Italic* | Emphasis |
| `<i>` | *Italic* | Just visual italic |
| `<mark>` | Highlighted | Draw attention |
| `<del>` | ~~Strikethrough~~ | Deleted/old text |
| `<sub>` | Subscript | Chemical formulas (H₂O) |
| `<sup>` | Superscript | Math powers (x²) |
| `<code>` | Monospace | Code snippets |
| `<pre>` | Preserves formatting | Code blocks |
| `<blockquote>` | Indented block | Quotes |

---

## Links

```html
<!-- Basic link -->
<a href="https://www.google.com">Go to Google</a>

<!-- Open in new tab (ALWAYS use for external links) -->
<a href="https://www.google.com" target="_blank" rel="noopener">Google</a>

<!-- Link to another page on your site -->
<a href="about.html">About Us</a>
<a href="pages/contact.html">Contact</a>

<!-- Link to a section on the SAME page -->
<a href="#courses">Jump to Courses</a>
<!-- ... lots of content ... -->
<h2 id="courses">Our Courses</h2>

<!-- Email link -->
<a href="mailto:info@techpath.biz">Send us an email</a>

<!-- Phone link (useful on mobile — tapping calls the number) -->
<a href="tel:+919876543210">Call: +91-98765-43210</a>

<!-- Link with an image (click image to go somewhere) -->
<a href="https://techpath.biz">
    <img src="logo.png" alt="TechPath Logo">
</a>
```

**`target="_blank"` security:** Always add `rel="noopener"` when using `target="_blank"` — it prevents a security vulnerability where the new page can access your page.

---

## Images

```html
<!-- Local image -->
<img src="images/hero.jpg" alt="Students learning to code at TechPath" width="600">

<!-- Image from URL -->
<img src="https://example.com/photo.jpg" alt="Description of photo">

<!-- Responsive image (adapts to screen) -->
<img src="banner.jpg" alt="Welcome banner" style="max-width: 100%; height: auto;">

<!-- Figure with caption (semantic) -->
<figure>
    <img src="dashboard.png" alt="Sales dashboard showing monthly revenue">
    <figcaption>Figure 1: Monthly Revenue Dashboard</figcaption>
</figure>
```

### Image Best Practices

| Rule | Why |
|------|-----|
| Always add `alt` text | Screen readers, SEO, shows if image fails |
| Use descriptive alt text | "Students coding in lab" not just "image" |
| Compress images before uploading | Large images = slow page = users leave |
| Use `.webp` format when possible | 30% smaller than JPG, same quality |
| Set `width` and `height` or use CSS | Prevents layout shift while loading |

### Image Formats

| Format | Best For | Size |
|--------|----------|------|
| `.jpg` / `.jpeg` | Photos, complex images | Medium |
| `.png` | Logos, screenshots, transparency needed | Large |
| `.webp` | Everything (modern, best compression) | Small |
| `.svg` | Icons, logos (scales perfectly) | Tiny |
| `.gif` | Simple animations | Medium |

---

## Lists

```html
<!-- Unordered list (bullets) — for items with no specific order -->
<ul>
    <li>HTML & CSS</li>
    <li>JavaScript</li>
    <li>Python</li>
</ul>

<!-- Ordered list (numbers) — for steps or rankings -->
<ol>
    <li>Open VS Code</li>
    <li>Create index.html</li>
    <li>Write your code</li>
    <li>Open in browser</li>
</ol>

<!-- Nested list -->
<ul>
    <li>Frontend
        <ul>
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
        </ul>
    </li>
    <li>Backend
        <ul>
            <li>Python</li>
            <li>FastAPI</li>
        </ul>
    </li>
</ul>

<!-- Description list (for terms + definitions) -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language — structure of web pages</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets — styling of web pages</dd>
</dl>
```

---

## Tables

```html
<table>
    <caption>Student Marks — Semester 1</caption>
    <thead>
        <tr>
            <th>Name</th>
            <th>HTML</th>
            <th>CSS</th>
            <th>JavaScript</th>
            <th>Total</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Rahul Sharma</td>
            <td>85</td>
            <td>78</td>
            <td>92</td>
            <td>255</td>
        </tr>
        <tr>
            <td>Priya Patel</td>
            <td>90</td>
            <td>88</td>
            <td>75</td>
            <td>253</td>
        </tr>
        <tr>
            <td>Amit Kumar</td>
            <td>72</td>
            <td>95</td>
            <td>80</td>
            <td>247</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>Class Average</td>
            <td>82</td>
            <td>87</td>
            <td>82</td>
            <td>252</td>
        </tr>
    </tfoot>
</table>
```

| Tag | Purpose |
|-----|---------|
| `<table>` | Container for the entire table |
| `<caption>` | Title above the table |
| `<thead>` | Header row section |
| `<tbody>` | Data rows section |
| `<tfoot>` | Footer row section (totals, averages) |
| `<tr>` | Table row |
| `<th>` | Header cell (bold, centered by default) |
| `<td>` | Data cell |

### Spanning Columns and Rows

```html
<!-- Merge 3 columns into one (like Excel merge cells) -->
<td colspan="3">This cell spans 3 columns</td>

<!-- Merge 2 rows into one -->
<td rowspan="2">This cell spans 2 rows</td>
```

---

## Semantic HTML — Why It Matters

**Semantic tags** tell the browser AND Google what each part of your page IS.

```html
<!-- ❌ Old way — div for everything -->
<div class="header">
    <div class="navigation">...</div>
</div>
<div class="content">
    <div class="article">...</div>
    <div class="sidebar">...</div>
</div>
<div class="footer">...</div>

<!-- ✅ Semantic way — meaningful tags -->
<header>
    <nav>...</nav>
</header>
<main>
    <article>...</article>
    <aside>...</aside>
</main>
<footer>...</footer>
```

> 🖼️ **IMAGE:** A web page wireframe divided into labeled sections — `<header>` at top with `<nav>` inside, `<main>` in the center containing `<article>` (large) and `<aside>` (sidebar), and `<footer>` at bottom — each section labeled with its semantic tag name
> `semantic-html-layout.png`

| Semantic Tag | What It Represents | Use For |
|-------------|-------------------|---------|
| `<header>` | Top section | Logo, navigation, banner |
| `<nav>` | Navigation links | Menu, breadcrumbs |
| `<main>` | Primary content | Main page content (ONE per page) |
| `<section>` | Grouped content | "Our Services", "About Us" sections |
| `<article>` | Independent content | Blog post, product card, news item |
| `<aside>` | Secondary content | Sidebar, related links, ads |
| `<footer>` | Bottom section | Copyright, social links, sitemap |
| `<figure>` | Image with caption | Photos, diagrams, code examples |
| `<details>` | Collapsible content | FAQ answers, extra info |
| `<time>` | Date/time | "Posted on `<time datetime="2026-01-15">Jan 15, 2026</time>`" |

### Why Use Semantic HTML?

| Benefit | Explanation |
|---------|-------------|
| **SEO** | Google understands your page better → higher ranking |
| **Accessibility** | Screen readers navigate by landmarks (header, nav, main) |
| **Code readability** | `<nav>` is clearer than `<div class="navigation">` |
| **Future-proof** | Standard that all browsers support |

---

## Forms — Getting User Input

### Complete Form Example

```html
<form action="/api/register" method="POST">
    <!-- Text input -->
    <div class="form-group">
        <label for="fullname">Full Name *</label>
        <input type="text" id="fullname" name="fullname"
               placeholder="Enter your full name"
               required
               minlength="2"
               maxlength="100">
    </div>

    <!-- Email -->
    <div class="form-group">
        <label for="email">Email *</label>
        <input type="email" id="email" name="email"
               placeholder="you@example.com"
               required>
    </div>

    <!-- Phone -->
    <div class="form-group">
        <label for="phone">Phone</label>
        <input type="tel" id="phone" name="phone"
               placeholder="+91-98765-43210"
               pattern="[0-9]{10}">
    </div>

    <!-- Password -->
    <div class="form-group">
        <label for="password">Password *</label>
        <input type="password" id="password" name="password"
               required
               minlength="8"
               placeholder="Minimum 8 characters">
    </div>

    <!-- Date -->
    <div class="form-group">
        <label for="dob">Date of Birth</label>
        <input type="date" id="dob" name="dob">
    </div>

    <!-- Number -->
    <div class="form-group">
        <label for="age">Age</label>
        <input type="number" id="age" name="age" min="15" max="60">
    </div>

    <!-- Dropdown -->
    <div class="form-group">
        <label for="course">Select Course *</label>
        <select id="course" name="course" required>
            <option value="">-- Choose a course --</option>
            <option value="adca">ADCA — 12 Months (₹35,000)</option>
            <option value="dca">DCA — 6 Months (₹18,000)</option>
            <option value="tally">Tally Pro — 3 Months (₹8,000)</option>
        </select>
    </div>

    <!-- Radio buttons (choose ONE) -->
    <div class="form-group">
        <label>Preferred Batch *</label>
        <label><input type="radio" name="batch" value="morning" required> Morning (9 AM - 12 PM)</label>
        <label><input type="radio" name="batch" value="evening"> Evening (5 PM - 8 PM)</label>
        <label><input type="radio" name="batch" value="weekend"> Weekend (Sat-Sun)</label>
    </div>

    <!-- Checkbox (choose MULTIPLE) -->
    <div class="form-group">
        <label>How did you hear about us?</label>
        <label><input type="checkbox" name="source" value="google"> Google Search</label>
        <label><input type="checkbox" name="source" value="instagram"> Instagram</label>
        <label><input type="checkbox" name="source" value="friend"> Friend</label>
        <label><input type="checkbox" name="source" value="banner"> Banner/Poster</label>
    </div>

    <!-- Textarea (multi-line text) -->
    <div class="form-group">
        <label for="message">Any Questions?</label>
        <textarea id="message" name="message" rows="4"
                  placeholder="Ask us anything..."></textarea>
    </div>

    <!-- File upload -->
    <div class="form-group">
        <label for="photo">Upload Photo</label>
        <input type="file" id="photo" name="photo" accept="image/*">
    </div>

    <!-- Terms checkbox -->
    <div class="form-group">
        <label>
            <input type="checkbox" name="terms" required>
            I agree to the <a href="/terms">Terms & Conditions</a> *
        </label>
    </div>

    <!-- Submit button -->
    <button type="submit">Register Now</button>
    <button type="reset">Clear Form</button>
</form>
```

> 🖼️ **IMAGE:** A rendered registration form in a browser showing all the input types — text field, email, phone, dropdown, radio buttons, checkboxes, textarea, file upload, and submit button — styled cleanly with labels and placeholders visible
> `html-complete-form-rendered.png`

### All Input Types

| Type | What It Shows | Keyboard on Mobile |
|------|-------------|-------------------|
| `text` | Normal text field | Regular keyboard |
| `email` | Email field (auto-validates @) | Email keyboard (has @ key) |
| `password` | Hidden dots/stars | Regular keyboard |
| `number` | Number field with +/- arrows | Number pad |
| `tel` | Phone number | Phone dial pad |
| `date` | Calendar date picker | Date picker |
| `time` | Time picker | Time picker |
| `url` | URL field (validates http://) | URL keyboard (has .com) |
| `search` | Search field (with clear X) | Regular with search key |
| `range` | Slider | — |
| `color` | Color picker popup | Color picker |
| `file` | File upload button | File browser |
| `hidden` | Invisible (sends data silently) | — |
| `checkbox` | Tick box (multiple selections) | — |
| `radio` | Circle (single selection) | — |

### Built-in Validation Attributes

| Attribute | What It Does | Example |
|-----------|-------------|---------|
| `required` | Must fill before submit | `<input required>` |
| `minlength` | Minimum characters | `minlength="8"` |
| `maxlength` | Maximum characters | `maxlength="100"` |
| `min` / `max` | Number range | `min="18" max="60"` |
| `pattern` | Must match regex | `pattern="[0-9]{10}"` (10 digits) |
| `placeholder` | Hint text inside field | `placeholder="Enter name"` |
| `disabled` | Can't interact | `<input disabled>` |
| `readonly` | Can see but not edit | `<input readonly>` |
| `autofocus` | Cursor starts here | `<input autofocus>` |
| `autocomplete` | Browser suggests | `autocomplete="email"` |

---

## HTML Entities — Special Characters

| Character | Code | Renders As |
|-----------|------|-----------|
| `&lt;` | Less than | < |
| `&gt;` | Greater than | > |
| `&amp;` | Ampersand | & |
| `&copy;` | Copyright | © |
| `&nbsp;` | Non-breaking space | (space that won't collapse) |
| `&rupee;` or `&#8377;` | Rupee sign | ₹ |
| `&hearts;` | Heart | ♥ |
| `&rarr;` | Right arrow | → |

Useful when you want to show `<div>` as text (not as a tag):
```html
<p>Use &lt;div&gt; to create a container.</p>
<!-- Renders: Use <div> to create a container. -->
```

---

## Multimedia Tags

### Video

```html
<video width="640" controls>
    <source src="intro.mp4" type="video/mp4">
    Your browser does not support video.
</video>

<!-- Autoplay, muted, loop (for background videos) -->
<video autoplay muted loop>
    <source src="background.mp4" type="video/mp4">
</video>
```

### YouTube Embed

```html
<iframe width="560" height="315"
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="Video title"
    frameborder="0"
    allowfullscreen>
</iframe>
```

### Audio

```html
<audio controls>
    <source src="song.mp3" type="audio/mpeg">
</audio>
```

### Google Maps Embed

```html
<iframe
    src="https://www.google.com/maps/embed?pb=PLACE_ID"
    width="600" height="450"
    style="border:0;"
    allowfullscreen
    loading="lazy">
</iframe>
```

---

## Practice Exercises

### Exercise 1: Your First Page
Create `index.html` with:
- Your name as `<h1>`
- A paragraph about yourself
- An image (use any photo from your computer)
- A list of 5 skills
- A link to your favorite website
- Open in browser — verify everything shows correctly

### Exercise 2: Student Registration Form
Create a complete registration form with:
- Text fields: name, father's name, address
- Email, phone, date of birth
- Dropdown: select course
- Radio: batch timing
- Checkboxes: subjects interested in
- Textarea: why do you want to learn IT?
- File upload: photo
- Required validation on mandatory fields
- Submit and Reset buttons

### Exercise 3: Class Timetable
Create an HTML table showing a weekly class timetable:
- Rows: Monday to Friday
- Columns: 9-10 AM, 10-11 AM, 11-12 PM, 12-1 PM (Lunch), 1-2 PM, 2-3 PM
- Use `colspan` to merge the lunch break across the row
- Use `<thead>`, `<tbody>`, `<caption>`

### Exercise 4: Resume in HTML
Create your resume as a web page:
- Header with name and contact info
- Sections: Education, Skills, Projects, Certifications
- Use semantic HTML (header, main, section, footer)
- Include a profile photo with `<figure>` and `<figcaption>`
- Add links to your LinkedIn and GitHub

---

## Summary

- **HTML** = structure of every web page
- Tags come in pairs `<tag>content</tag>` or are self-closing `<img>`
- Use **semantic tags** for better SEO and accessibility
- **Forms** collect user input with built-in validation
- Always add **alt text** to images
- Use `<h1>` only ONCE per page
- Practice by building real pages, not just reading about tags
