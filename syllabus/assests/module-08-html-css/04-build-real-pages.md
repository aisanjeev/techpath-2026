# HTML & CSS — Build Real Web Pages

**Module 08 — HTML & CSS | Project-Based Learning**

---

## Why This Matters

> Knowing `<div>` and `color: red` doesn't get you hired. Building actual pages does. This chapter walks you through 4 complete pages that you'll build from scratch — the same kind companies pay Rs 3,000-10,000 to get built.

---

## Project 1: Personal Portfolio Page

### What You'll Build

A single-page portfolio website with: hero section, about, skills, projects, and contact.

> 🖼️ **IMAGE:** Full-length screenshot of a modern portfolio page — dark hero section with name and tagline, about section with photo, skills shown as colored pills/tags, 3 project cards in a grid, and a contact form at the bottom
> `html-portfolio-page-final.png`

### Complete Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rahul Sharma — Web Developer</title>
    <style>
        /* Reset & Base */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #1e293b;
        }
        a { text-decoration: none; color: inherit; }
        img { max-width: 100%; display: block; }

        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            padding: 16px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            z-index: 100;
        }
        .nav-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-logo { font-weight: 700; font-size: 20px; color: #6366f1; }
        .nav-links { display: flex; gap: 32px; list-style: none; }
        .nav-links a { font-size: 15px; color: #64748b; transition: color 0.2s; }
        .nav-links a:hover { color: #6366f1; }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 0 24px;
        }
        .hero-content {
            max-width: 1100px;
            margin: 0 auto;
            color: white;
        }
        .hero-label {
            font-size: 16px;
            color: #818cf8;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .hero h1 { font-size: 56px; font-weight: 800; line-height: 1.1; margin-bottom: 20px; }
        .hero p { font-size: 20px; color: #94a3b8; max-width: 600px; margin-bottom: 32px; }
        .btn {
            display: inline-block;
            padding: 14px 32px;
            background: #6366f1;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            transition: background 0.2s;
        }
        .btn:hover { background: #4f46e5; }

        /* Section Base */
        section { padding: 100px 24px; }
        .section-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 16px;
        }
        .section-subtitle {
            text-align: center;
            color: #64748b;
            font-size: 18px;
            margin-bottom: 60px;
        }
        .container { max-width: 1100px; margin: 0 auto; }

        /* Skills */
        .skills-grid { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
        .skill-tag {
            padding: 10px 24px;
            background: #f1f5f9;
            border-radius: 24px;
            font-size: 15px;
            font-weight: 500;
            color: #334155;
            border: 1px solid #e2e8f0;
        }
        .skill-tag.highlight { background: #eef2ff; color: #4f46e5; border-color: #c7d2fe; }

        /* Projects Grid */
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 32px; }
        .project-card {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .project-card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.12); }
        .project-img { height: 200px; background: #e2e8f0; }
        .project-info { padding: 24px; }
        .project-info h3 { font-size: 20px; margin-bottom: 8px; }
        .project-info p { font-size: 15px; color: #64748b; margin-bottom: 16px; }
        .project-tags { display: flex; gap: 8px; flex-wrap: wrap; }
        .project-tags span {
            font-size: 13px;
            padding: 4px 12px;
            background: #f1f5f9;
            border-radius: 12px;
            color: #475569;
        }

        /* Contact */
        .contact-form { max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 8px; font-size: 15px; }
        .form-group input, .form-group textarea {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }
        .form-group input:focus, .form-group textarea:focus { border-color: #6366f1; }
        .form-group textarea { height: 150px; resize: vertical; }

        /* Footer */
        footer {
            background: #0f172a;
            color: #94a3b8;
            text-align: center;
            padding: 32px;
            font-size: 15px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 36px; }
            .nav-links { display: none; }
            section { padding: 60px 16px; }
            .projects-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-container">
            <div class="nav-logo">RS.</div>
            <ul class="nav-links">
                <li><a href="#about">About</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-content">
            <div class="hero-label">Hello, I'm</div>
            <h1>Rahul Sharma</h1>
            <p>A full-stack developer who builds web applications with Python, JavaScript, and AI tools. ADCA graduate ready to create great products.</p>
            <a href="#projects" class="btn">View My Work</a>
        </div>
    </section>

    <section id="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <p class="section-subtitle">
                I'm a recent ADCA graduate passionate about building useful web applications.
                I specialize in Python (FastAPI, Django) for the backend and modern JavaScript for the frontend.
                I believe in clean code, simple design, and solving real problems.
            </p>
        </div>
    </section>

    <section id="skills" style="background:#f8fafc;">
        <div class="container">
            <h2 class="section-title">Skills</h2>
            <p class="section-subtitle">Technologies I work with</p>
            <div class="skills-grid">
                <span class="skill-tag highlight">Python</span>
                <span class="skill-tag highlight">JavaScript</span>
                <span class="skill-tag">HTML & CSS</span>
                <span class="skill-tag highlight">FastAPI</span>
                <span class="skill-tag">Django</span>
                <span class="skill-tag">React</span>
                <span class="skill-tag">Bootstrap</span>
                <span class="skill-tag highlight">SQL</span>
                <span class="skill-tag">Git & GitHub</span>
                <span class="skill-tag">Docker</span>
                <span class="skill-tag highlight">AI Tools</span>
                <span class="skill-tag">Figma</span>
            </div>
        </div>
    </section>

    <section id="projects">
        <div class="container">
            <h2 class="section-title">Projects</h2>
            <p class="section-subtitle">Things I've built</p>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-img" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);"></div>
                    <div class="project-info">
                        <h3>E-Commerce API</h3>
                        <p>Complete REST API with user auth, product CRUD, cart, and order management.</p>
                        <div class="project-tags">
                            <span>FastAPI</span><span>PostgreSQL</span><span>JWT</span>
                        </div>
                    </div>
                </div>
                <div class="project-card">
                    <div class="project-img" style="background:linear-gradient(135deg,#06b6d4,#0891b2);"></div>
                    <div class="project-info">
                        <h3>AI Chatbot</h3>
                        <p>Student FAQ chatbot powered by Claude API with conversation memory.</p>
                        <div class="project-tags">
                            <span>JavaScript</span><span>Claude API</span><span>HTML/CSS</span>
                        </div>
                    </div>
                </div>
                <div class="project-card">
                    <div class="project-img" style="background:linear-gradient(135deg,#f59e0b,#d97706);"></div>
                    <div class="project-info">
                        <h3>Sales Dashboard</h3>
                        <p>Data analysis of 10K+ records with interactive charts and automated reports.</p>
                        <div class="project-tags">
                            <span>Python</span><span>Pandas</span><span>Matplotlib</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" style="background:#f8fafc;">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <p class="section-subtitle">Have a project in mind? Let's talk.</p>
            <form class="contact-form">
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input type="text" id="name" placeholder="Rahul Sharma">
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" placeholder="rahul@example.com">
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" placeholder="Tell me about your project..."></textarea>
                </div>
                <button type="submit" class="btn" style="width:100%;border:none;cursor:pointer;font-family:inherit;">Send Message</button>
            </form>
        </div>
    </section>

    <footer>
        <p>Built by Rahul Sharma | 2026</p>
    </footer>
</body>
</html>
```

### What This Teaches

| Concept | Where in the Code |
|---------|-------------------|
| Flexbox layout | Navigation, skills grid |
| CSS Grid | Projects grid |
| Fixed navbar | `position: fixed` on nav |
| Gradient backgrounds | Hero, project cards |
| Hover effects | Cards, links, buttons |
| Responsive design | Media query at bottom |
| Smooth colors | Consistent color palette |
| Form styling | Contact section |

---

## Project 2: Pricing Table

### What You'll Build

A 3-column pricing table (Basic, Pro, Enterprise) — every SaaS website has one.

> 🖼️ **IMAGE:** Three pricing cards side by side — Basic (₹499/mo, gray header), Pro (₹999/mo, purple header, highlighted as "Popular" with a badge), Enterprise (₹2499/mo, dark header) — each with feature list, checkmarks, and a CTA button
> `html-pricing-table-final.png`

```html
<!-- Add to a new HTML file -->
<style>
    .pricing-section {
        padding: 80px 24px;
        background: #f8fafc;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    .pricing-grid {
        max-width: 1000px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
        align-items: start;
    }
    .pricing-card {
        background: white;
        border-radius: 16px;
        padding: 40px 32px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
    }
    .pricing-card.featured {
        border: 2px solid #6366f1;
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(99,102,241,0.2);
        position: relative;
    }
    .pricing-card.featured::before {
        content: "Most Popular";
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: #6366f1;
        color: white;
        padding: 4px 20px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
    }
    .plan-name { font-size: 20px; font-weight: 600; color: #64748b; margin-bottom: 8px; }
    .plan-price { font-size: 48px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
    .plan-price span { font-size: 18px; font-weight: 400; color: #94a3b8; }
    .plan-desc { font-size: 15px; color: #94a3b8; margin-bottom: 32px; }
    .feature-list { list-style: none; text-align: left; margin-bottom: 32px; }
    .feature-list li {
        padding: 10px 0;
        font-size: 15px;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
    }
    .feature-list li::before { content: "✓ "; color: #22c55e; font-weight: 700; }
    .feature-list li.disabled { color: #cbd5e1; }
    .feature-list li.disabled::before { content: "✗ "; color: #cbd5e1; }
    .plan-btn {
        width: 100%;
        padding: 14px;
        border: 2px solid #6366f1;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        background: white;
        color: #6366f1;
        transition: all 0.2s;
    }
    .plan-btn:hover, .pricing-card.featured .plan-btn {
        background: #6366f1;
        color: white;
    }
    @media (max-width: 768px) {
        .pricing-grid { grid-template-columns: 1fr; }
        .pricing-card.featured { transform: scale(1); }
    }
</style>

<section class="pricing-section">
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="plan-name">Basic</div>
            <div class="plan-price">₹499<span>/month</span></div>
            <div class="plan-desc">For individuals getting started</div>
            <ul class="feature-list">
                <li>5 Projects</li>
                <li>10GB Storage</li>
                <li>Email Support</li>
                <li class="disabled">Custom Domain</li>
                <li class="disabled">Priority Support</li>
            </ul>
            <button class="plan-btn">Get Started</button>
        </div>
        <div class="pricing-card featured">
            <div class="plan-name">Pro</div>
            <div class="plan-price">₹999<span>/month</span></div>
            <div class="plan-desc">For growing teams</div>
            <ul class="feature-list">
                <li>Unlimited Projects</li>
                <li>100GB Storage</li>
                <li>Priority Support</li>
                <li>Custom Domain</li>
                <li class="disabled">White Label</li>
            </ul>
            <button class="plan-btn">Get Started</button>
        </div>
        <div class="pricing-card">
            <div class="plan-name">Enterprise</div>
            <div class="plan-price">₹2,499<span>/month</span></div>
            <div class="plan-desc">For large organizations</div>
            <ul class="feature-list">
                <li>Unlimited Everything</li>
                <li>1TB Storage</li>
                <li>Dedicated Support</li>
                <li>Custom Domain</li>
                <li>White Label</li>
            </ul>
            <button class="plan-btn">Contact Sales</button>
        </div>
    </div>
</section>
```

---

## Project 3: Responsive Navigation Bar

A navbar that collapses into a hamburger menu on mobile — every website needs this.

> 🖼️ **IMAGE:** Two views of the same navbar — desktop view showing horizontal menu (Logo, Home, About, Services, Contact, CTA button), and mobile view showing hamburger icon and the same links stacked vertically when opened
> `html-responsive-navbar.png`

### Key CSS Techniques in This Page

| Technique | What It Does | Real Use |
|-----------|-------------|----------|
| `position: fixed` | Navbar stays on top while scrolling | Every professional site |
| `backdrop-filter: blur()` | Frosted glass effect | Modern navbars |
| `grid-template-columns` | Multi-column layouts | Project grids, pricing |
| `@media (max-width)` | Different layout on mobile | Responsive design |
| `::before` pseudo-element | Add content via CSS | Badges, icons |
| `transform: scale()` | Enlarge elements | Featured/highlighted card |
| `transition` | Smooth hover effects | Buttons, cards |
| `linear-gradient` | Gradient backgrounds | Hero sections, buttons |

---

## Common Layout Patterns (Copy & Use)

### Center Everything (Most Common Pattern)

```css
/* Flexbox center */
.center-flex {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Grid center (simpler) */
.center-grid {
    display: grid;
    place-items: center;
    min-height: 100vh;
}
```

### Two-Column Layout

```css
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
}

@media (max-width: 768px) {
    .two-col { grid-template-columns: 1fr; }
}
```

### Card Grid (Auto-Responsive)

```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}
```

This grid automatically adjusts — 3 columns on desktop, 2 on tablet, 1 on mobile. No media query needed!

---

## Practice Exercises

### Exercise 1: Clone a Real Website Section
Pick any Indian company website (Zerodha, Razorpay, Freshworks). Clone just the hero section — match colors, fonts, layout as closely as possible.

### Exercise 2: Responsive Card Gallery
Create a page with 6-8 image cards (like a photo gallery or product grid). Must work on mobile, tablet, and desktop using CSS Grid.

### Exercise 3: Landing Page
Build a complete landing page for a fictional product with:
- Fixed navbar
- Hero section with heading + CTA button
- 3-feature section with icons
- Testimonial section
- Footer with links
- Fully responsive (looks good on phone)
