# Module 13 — GenAI-Powered Website Development — Quick Revision Notes

---

## What is GenAI Website Development?
- Using AI tools to **generate, modify, and deploy** websites faster
- Not replacing coding skills — **amplifying** them
- You still need HTML/CSS/JS knowledge to review, fix, and customize AI output

## AI Website Builders
| Tool | Strength | Free? |
|------|----------|-------|
| **v0.dev** (Vercel) | React/Tailwind components | Free tier |
| **Claude** | Full code generation, debugging | Free tier |
| **ChatGPT** | Code + explanation | Free tier |
| **Bolt.new** | Full-stack app scaffolding | Free tier |
| **Cursor** | AI code editor | Free tier |

## The AI-Assisted Workflow
1. **Plan** — sketch layout, list sections, define content
2. **Prompt** — describe what you want to the AI tool
3. **Generate** — AI creates code
4. **Review** — read the code, understand what it does
5. **Customize** — modify colors, content, layout
6. **Test** — check responsiveness, accessibility, performance
7. **Deploy** — push live (GitHub Pages, Vercel, Netlify)

## Effective Prompting for Code
```
Bad:  "Make me a website"
Good: "Create a responsive landing page for a computer training institute 
       called TechPath in Bhopal. Include: hero section with CTA button, 
       3 course cards (ADCA, DCA, Tally), testimonials section, contact 
       form, footer. Use HTML + Tailwind CSS. Mobile-first design."
```

**Prompt structure:**
1. What to build (specific component/page)
2. Context (who is it for, industry)
3. Sections/features needed
4. Tech stack (HTML/CSS, React, Tailwind)
5. Style preferences (colors, modern/minimal)

## Tailwind CSS Quick Reference
```html
<!-- Layout -->
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="container mx-auto px-4">

<!-- Spacing -->
<div class="p-4 m-2 mt-8 mb-4 px-6 py-3">

<!-- Typography -->
<h1 class="text-3xl font-bold text-gray-900">
<p class="text-sm text-gray-600 leading-relaxed">

<!-- Colors -->
<div class="bg-indigo-600 text-white hover:bg-indigo-700">
<div class="bg-gray-50 border border-gray-200">

<!-- Responsive -->
<div class="text-sm md:text-base lg:text-lg">
<div class="grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">

<!-- Effects -->
<div class="rounded-lg shadow-md hover:shadow-xl transition">
<div class="opacity-80 hover:opacity-100">
```

## GitHub Pages Deployment
```bash
# 1. Create repository on GitHub
# 2. Push your code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main

# 3. Settings → Pages → Source: main → /root → Save
# Site live at: https://username.github.io/repo/
```

## Vercel Deployment
1. Push code to GitHub
2. Go to vercel.com → Import Project
3. Select your repo → Deploy
4. Get a free `.vercel.app` URL

## Key Concepts
- **Static Site** — HTML/CSS/JS only, no server needed (GitHub Pages)
- **SSR** — Server-Side Rendering (Next.js, Astro)
- **Responsive** — works on all screen sizes (mobile-first)
- **Accessibility** — usable by everyone (alt text, semantic HTML, keyboard navigation)
- **SEO** — found by search engines (meta tags, headings, alt text)
- **Performance** — loads fast (optimize images, minimize CSS/JS)
