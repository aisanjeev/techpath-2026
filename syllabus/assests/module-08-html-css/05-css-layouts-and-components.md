# CSS — Layout Patterns & Reusable Components

**Module 08 — HTML & CSS | Topic 5 — What Professionals Actually Build**

---

## Why This Matters

> Every website uses the same 10-15 layout patterns. Learn them once, and you can build any website. Interviewers ask "Build a card layout" or "Create a responsive navbar" — not "What is the box model?"

---

## Pattern 1: Responsive Navbar (Every Website Needs One)

> 🖼️ **IMAGE:** Two views of the same navbar — desktop showing horizontal logo + links + CTA button, and mobile showing hamburger menu icon with vertical links when opened — side by side comparison
> `css-responsive-navbar-pattern.png`

```html
<nav class="navbar">
    <a href="/" class="nav-logo">TechPath</a>
    <input type="checkbox" id="menu-toggle" class="menu-toggle">
    <label for="menu-toggle" class="hamburger">&#9776;</label>
    <ul class="nav-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#courses">Courses</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
        <li><a href="#enroll" class="nav-cta">Enroll Now</a></li>
    </ul>
</nav>
```

```css
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-logo {
    font-size: 24px;
    font-weight: 800;
    color: var(--primary, #6366f1);
}

.nav-links {
    display: flex;
    gap: 32px;
    align-items: center;
}

.nav-links a {
    font-size: 15px;
    color: #475569;
    transition: color 0.2s;
}

.nav-links a:hover { color: var(--primary, #6366f1); }

.nav-cta {
    background: var(--primary, #6366f1) !important;
    color: white !important;
    padding: 10px 20px;
    border-radius: 8px;
}

/* Hamburger — hidden on desktop */
.menu-toggle { display: none; }
.hamburger { display: none; font-size: 28px; cursor: pointer; }

/* Mobile */
@media (max-width: 768px) {
    .hamburger { display: block; }

    .nav-links {
        display: none;
        flex-direction: column;
        position: absolute;
        top: 60px;
        left: 0;
        right: 0;
        background: white;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        gap: 0;
    }

    .nav-links li { padding: 12px 0; border-bottom: 1px solid #f1f5f9; }

    .menu-toggle:checked ~ .nav-links { display: flex; }
}
```

**Key technique:** Pure CSS hamburger menu using a hidden checkbox — no JavaScript needed!

---

## Pattern 2: Hero Section (First Thing Users See)

```html
<section class="hero">
    <div class="hero-content">
        <span class="hero-badge">New Batch Starting July 2026</span>
        <h1>Launch Your IT Career in 12 Months</h1>
        <p>Join 500+ students who got placed at top IT companies. Learn Python, Web Development, AI Tools, and more.</p>
        <div class="hero-buttons">
            <a href="#courses" class="btn btn-primary">Explore Courses</a>
            <a href="#demo" class="btn btn-outline">Book Free Demo</a>
        </div>
        <div class="hero-stats">
            <div class="stat"><span class="stat-number">500+</span> Students Placed</div>
            <div class="stat"><span class="stat-number">85%</span> Placement Rate</div>
            <div class="stat"><span class="stat-number">15+</span> Hiring Partners</div>
        </div>
    </div>
</section>
```

```css
.hero {
    min-height: 90vh;
    display: flex;
    align-items: center;
    padding: 80px 24px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
}

.hero-content {
    max-width: 700px;
    margin: 0 auto;
    text-align: center;
}

.hero-badge {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(99, 102, 241, 0.2);
    color: #818cf8;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 24px;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 3.5rem);  /* responsive font size! */
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 20px;
}

.hero p {
    font-size: 1.125rem;
    color: #94a3b8;
    margin-bottom: 32px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-buttons {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 48px;
}

.btn {
    display: inline-block;
    padding: 14px 28px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.2s;
    cursor: pointer;
    border: 2px solid transparent;
}

.btn-primary {
    background: #6366f1;
    color: white;
}
.btn-primary:hover { background: #4f46e5; transform: translateY(-2px); }

.btn-outline {
    background: transparent;
    color: white;
    border: 2px solid rgba(255,255,255,0.3);
}
.btn-outline:hover { border-color: white; }

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
}

.stat-number {
    display: block;
    font-size: 2rem;
    font-weight: 800;
    color: #818cf8;
}

.stat { font-size: 14px; color: #94a3b8; }
```

**Key technique:** `clamp(2rem, 5vw, 3.5rem)` makes the heading responsive WITHOUT media queries — it smoothly scales between 2rem (min) and 3.5rem (max).

---

## Pattern 3: Feature/Service Cards Grid

```html
<section class="features">
    <h2 class="section-title">Why Choose TechPath?</h2>
    <p class="section-subtitle">Everything you need to launch your IT career</p>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">💻</div>
            <h3>Hands-On Projects</h3>
            <p>Build 6 real projects that go straight to your portfolio and GitHub.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered Learning</h3>
            <p>Learn to use ChatGPT, Claude, and AI tools that 10x your productivity.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Placement Support</h3>
            <p>Resume building, mock interviews, and direct referrals to hiring partners.</p>
        </div>
    </div>
</section>
```

```css
.features { padding: 80px 24px; }

.section-title {
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 12px;
}

.section-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1.125rem;
    margin-bottom: 48px;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    max-width: 1100px;
    margin: 0 auto;
}

.feature-card {
    background: white;
    border: 1px solid #f1f5f9;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.feature-card h3 {
    font-size: 1.25rem;
    margin-bottom: 8px;
}

.feature-card p {
    color: #64748b;
    font-size: 0.9375rem;
    line-height: 1.6;
}
```

---

## Pattern 4: Testimonial Section

```css
.testimonial-card {
    background: #f8fafc;
    border-radius: 16px;
    padding: 32px;
    position: relative;
}

.testimonial-card::before {
    content: '"';
    font-size: 4rem;
    color: #6366f1;
    position: absolute;
    top: 16px;
    left: 24px;
    opacity: 0.3;
    font-family: Georgia, serif;
}

.testimonial-text {
    font-size: 1rem;
    color: #334155;
    line-height: 1.7;
    font-style: italic;
    margin-bottom: 20px;
}

.testimonial-author {
    display: flex;
    align-items: center;
    gap: 12px;
}

.testimonial-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #6366f1;
}

.testimonial-name { font-weight: 600; font-size: 15px; }
.testimonial-role { color: #64748b; font-size: 14px; }
```

---

## Pattern 5: Footer

```css
.footer {
    background: #0f172a;
    color: #94a3b8;
    padding: 60px 24px 24px;
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 48px;
    max-width: 1100px;
    margin: 0 auto;
}

.footer h4 {
    color: white;
    margin-bottom: 16px;
    font-size: 16px;
}

.footer a {
    display: block;
    padding: 4px 0;
    color: #94a3b8;
    font-size: 14px;
    transition: color 0.2s;
}

.footer a:hover { color: white; }

.footer-bottom {
    border-top: 1px solid #1e293b;
    margin-top: 40px;
    padding-top: 24px;
    text-align: center;
    font-size: 14px;
}

@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: 1fr 1fr;
        gap: 32px;
    }
}

@media (max-width: 480px) {
    .footer-grid { grid-template-columns: 1fr; }
}
```

---

## Pattern 6: Form Styling

```css
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 6px;
    color: #334155;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 15px;
    font-family: inherit;
    outline: none;
    background: white;
    transition: border-color 0.2s, box-shadow 0.2s;
}

/* Focus state — colored border + glow */
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* Error state */
.form-group input:invalid:not(:placeholder-shown) {
    border-color: #ef4444;
}

/* Disabled state */
.form-group input:disabled {
    background: #f1f5f9;
    cursor: not-allowed;
}

.form-group textarea {
    min-height: 120px;
    resize: vertical;
}
```

> 🖼️ **IMAGE:** Three input field states side by side — Default (gray border), Focused (purple border with light purple glow), Error (red border with red text below saying "Please enter a valid email") — each labeled
> `css-input-states.png`

---

## CSS Variables in Practice — Theme System

```css
/* Light theme (default) */
:root {
    --bg-body: #ffffff;
    --bg-card: #ffffff;
    --bg-section: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --border: #e2e8f0;
    --primary: #6366f1;
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-body: #0f172a;
        --bg-card: #1e293b;
        --bg-section: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --border: #334155;
        --primary: #818cf8;
    }
}

/* Use variables everywhere */
body { background: var(--bg-body); color: var(--text-primary); }
.card { background: var(--bg-card); border: 1px solid var(--border); }
section.alt { background: var(--bg-section); }
p { color: var(--text-secondary); }
```

Now your entire site supports dark mode automatically!

---

## Debugging CSS (Essential Skill)

### Chrome DevTools

1. Right-click any element → **Inspect**
2. See the HTML on the left, CSS on the right
3. You can **edit CSS live** — changes show instantly (not saved to file)
4. Toggle properties on/off with checkboxes
5. Add new properties in the "element.style" section

> 🖼️ **IMAGE:** Chrome DevTools open — showing the Elements panel with an HTML element selected (highlighted on the page in blue), the Styles panel on the right showing CSS rules with one property unchecked/crossed out, and the box model diagram at the bottom showing margin/padding/border values
> `chrome-devtools-inspect.png`

### Common Debugging Steps

| Problem | How to Debug |
|---------|-------------|
| Element not showing | Check `display: none`, `opacity: 0`, `visibility: hidden`, or zero width/height |
| Styles not applying | Check selector specificity — more specific selectors win |
| Layout broken | Inspect the box model — unexpected margin, padding, or width |
| Things overlapping | Check `z-index` and `position` values |
| Not responsive | Resize browser or use DevTools device toggle (Ctrl+Shift+M) |
| Flexbox misbehaving | DevTools shows a "flex" badge — click it to see flex lines |

---

## Interview Questions They'll Ask

| Question | Key Points |
|----------|-----------|
| "Box model?" | Content → Padding → Border → Margin. Use `box-sizing: border-box` |
| "Flexbox vs Grid?" | Flexbox = 1D (row/col). Grid = 2D (rows AND cols) |
| "Position values?" | static (default), relative, absolute, fixed, sticky |
| "Specificity?" | Inline > ID > Class > Element. More specific wins |
| "How to center a div?" | `display: flex; justify-content: center; align-items: center;` |
| "Mobile-first?" | Write mobile CSS first, use `min-width` media queries for larger screens |
| "CSS variables?" | Define in `:root`, use with `var(--name)`, great for themes |
| "Pseudo-elements?" | `::before` and `::after` add content via CSS. Need `content: ""` |

---

## Practice: Build a Complete Page

Take all patterns from this file and combine them into one page:
1. Navbar (Pattern 1)
2. Hero section (Pattern 2)
3. Features grid (Pattern 3)
4. Testimonials (Pattern 4)
5. Contact form (Pattern 6)
6. Footer (Pattern 5)

This gives you a **complete landing page template** that you can reuse for freelance projects.
