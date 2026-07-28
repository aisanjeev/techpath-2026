# GenAI-Powered Website Development

**Module 13 — GenAI Website Dev | Topic 1**

---

## What is GenAI-Powered Web Dev?

Using AI tools to **speed up** website building — from design to code to deployment.

| Traditional Way | GenAI Way |
|-----------------|----------|
| Design mockup manually in Figma | Describe → AI generates design |
| Write HTML/CSS from scratch | AI generates starter code |
| Debug by reading error messages | AI explains + fixes bugs |
| Search Stack Overflow for solutions | Ask AI directly |
| Hours to build a page | Minutes with AI assistance |

> **AI doesn't replace you** — it makes you 5-10x faster. You still need to understand the code.

---

## AI Tools for Web Development

| Tool | What It Does | Cost |
|------|-------------|------|
| **v0.dev** | Generate React/Next.js UI from text | Free tier |
| **Claude / ChatGPT** | Write HTML/CSS/JS, debug, explain | Free tiers |
| **GitHub Copilot** | Auto-complete code in VS Code | Free for students |
| **Cursor** | AI-native code editor | Free tier |
| **Bolt.new** | Full-stack app from a prompt | Free tier |
| **Lovable** | AI website builder | Free tier |
| **Replit** | Write + run code with AI | Free tier |

---

## Workflow: AI-Assisted Web Project

### Step 1: Plan with AI

```
Prompt: "I'm building a portfolio website for a web developer. 
List the pages I need and what should go on each page."
```

AI suggests: Home, About, Skills, Projects, Contact

### Step 2: Generate HTML Structure

```
Prompt: "Create the HTML structure for a portfolio website with:
- Responsive navbar with Home, About, Projects, Contact links
- Hero section with name and tagline
- Skills section with a grid of skill cards
- Projects section with 3 project cards (image, title, description, link)
- Contact form (name, email, message)
- Footer
Use semantic HTML5 tags."
```

### Step 3: Add CSS Styling

```
Prompt: "Add modern CSS to this HTML:
- Dark theme with accent color #3b82f6
- Mobile-first responsive design
- Smooth hover transitions on cards and buttons
- Flexbox for layout
- Google Font: Inter"
```

### Step 4: Add JavaScript

```
Prompt: "Add JavaScript for:
- Mobile hamburger menu toggle
- Smooth scroll to sections on nav click
- Form validation (required fields, valid email)
- Scroll-triggered animations (fade in on scroll)"
```

### Step 5: Debug with AI

```
Prompt: "My navbar doesn't collapse on mobile. Here's my HTML and CSS:
[paste code]
What's wrong and how do I fix it?"
```

---

## Building with v0.dev

### What is v0?

**v0.dev** by Vercel generates production-ready React components from text descriptions.

### Example Prompts

| Prompt | What You Get |
|--------|-------------|
| "A pricing table with 3 tiers" | Complete pricing component |
| "A dashboard with sidebar nav" | Dashboard layout |
| "A login form with social auth" | Login page |
| "An e-commerce product card" | Product card component |

### Workflow

1. Go to **v0.dev**
2. Describe your component
3. AI generates code + live preview
4. Click "Copy Code" → paste into your project
5. Customize as needed

---

## Building with Bolt.new

**Bolt.new** generates full-stack web applications:

1. Go to **bolt.new**
2. Describe your app: "Create a todo app with add, delete, mark complete"
3. AI generates the complete project
4. Edit code in-browser
5. Deploy with one click

---

## Hosting Your Website

### Free Hosting Options

| Platform | Best For | Deploy Method |
|----------|---------|--------------|
| **Vercel** | React, Next.js | Git push → auto deploy |
| **Netlify** | Static sites, HTML | Drag-and-drop or Git |
| **GitHub Pages** | Static HTML/CSS/JS | Push to gh-pages branch |
| **Render** | Full-stack apps | Git connect |
| **Railway** | Backend APIs | Git connect |

### Deploy to Vercel (Easiest)

```bash
# Install Vercel CLI
npm install -g vercel

# In your project folder
vercel

# Follow prompts → gets a live URL
```

### Deploy to GitHub Pages

```bash
# Create repo on GitHub, push your code
# Go to Settings → Pages → Select branch → Save
# Your site is live at: username.github.io/repo-name
```

---

## Domain Names

| Free Subdomain | Custom Domain |
|---------------|--------------|
| yourname.vercel.app | yourname.com |
| yourname.netlify.app | yourname.in |
| yourname.github.io | yourname.dev |

To use a custom domain:
1. Buy from Namecheap, GoDaddy, or Google Domains (~$10-15/year)
2. Point DNS to your hosting platform
3. Add domain in hosting settings

---

## SEO Basics

Make your website findable on Google:

```html
<head>
    <title>Rahul Sharma — Web Developer Portfolio</title>
    <meta name="description" content="Web developer specializing in React and Python. View my projects and contact me.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta property="og:title" content="Rahul Sharma — Portfolio">
    <meta property="og:description" content="Web developer portfolio">
    <meta property="og:image" content="preview-image.jpg">
</head>
```

| SEO Rule | What To Do |
|----------|-----------|
| **Title tag** | Unique, descriptive, under 60 chars |
| **Meta description** | Summary, under 160 chars |
| **Headings** | One H1 per page, use H2-H6 for structure |
| **Alt text** | Describe every image |
| **Fast loading** | Compress images, minimize CSS/JS |
| **Mobile-friendly** | Responsive design |
| **HTTPS** | Use SSL certificate |

---

## Summary

- **GenAI tools** speed up web development 5-10x
- Use **v0.dev** for React components, **Bolt.new** for full apps
- AI workflow: Plan → Generate → Customize → Debug → Deploy
- **Vercel, Netlify, GitHub Pages** = free hosting
- Always **understand the code AI generates** — don't blindly copy
- Learn **SEO basics** to make your site findable
- AI is your assistant, not your replacement
