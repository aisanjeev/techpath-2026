# Module 08 — Assignment: Build a Complete Website

**Deadline:** End of Week 10
**Submission:** Zipped project folder OR GitHub repo link

---

## Build: Personal Portfolio Website

Create a multi-page responsive portfolio website with the following pages:

### Page 1: Home (index.html) — 25 marks
- Hero section with your name, title, and a brief intro
- "About Me" section with a professional photo placeholder
- Skills section showing your tech stack (use progress bars or tags)
- Call-to-action button linking to Contact page
- Responsive — works on mobile and desktop

### Page 2: Projects (projects.html) — 25 marks
- Grid layout of at least 4 project cards
- Each card: image, title, description, tech tags, "View Project" link
- Cards must use CSS Grid or Flexbox with `auto-fit`
- Hover effect on cards (transform + shadow)
- Filter tags at the top (HTML/CSS only — no JS filtering needed, just styled tags)

### Page 3: Contact (contact.html) — 20 marks
- Contact form with: Name, Email, Phone, Message (textarea)
- Proper HTML5 validation (required, type="email", minlength)
- Styled form inputs with focus states (border-color change + glow)
- Form action can point to Formspree or just `#`
- Contact info section (email, phone, location)
- Social media icon links

### Global Requirements — 30 marks
- **Consistent navbar** on all pages with active page highlighted
- **Footer** on all pages with copyright and social links
- **Mobile responsive** — hamburger menu or stacked layout on mobile
- **CSS Variables** for colors (`--primary`, `--text`, `--bg`)
- **Shared stylesheet** (one `style.css` used by all pages)
- **Google Fonts** — at least one custom font
- **No inline styles** — all CSS in external stylesheet
- **Semantic HTML** — proper use of header, nav, main, section, footer
- **Clean code** — proper indentation, meaningful class names

### Folder Structure
```
portfolio/
├── index.html
├── projects.html
├── contact.html
├── css/
│   └── style.css
├── images/
│   └── (project screenshots, profile photo)
└── README.md (brief description of project)
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| HTML structure | Semantic, accessible, valid | Mostly semantic | div-soup, no semantics |
| CSS quality | Variables, flexbox/grid, responsive | Works but inconsistent | Broken layout on mobile |
| Visual design | Professional, consistent | Decent but rough edges | Ugly or template-looking |
| Form | All validations, styled states | Basic validation | No validation |
| Responsiveness | Works perfectly on all sizes | Minor issues on mobile | Broken on mobile |
| Code quality | Clean, organized, commented where needed | Readable | Messy, inline styles |
