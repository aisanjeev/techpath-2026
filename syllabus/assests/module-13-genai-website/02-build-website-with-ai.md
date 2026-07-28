# Build a Complete Website with AI — Step-by-Step

**Module 13 — GenAI Website Development | Full Project**

---

## Why This Matters

> In 2024, a freelancer charged Rs 15,000 to build a landing page manually. In 2026, you can build the same page in 1 hour using AI tools — and charge Rs 8,000 for "AI-assisted development." This chapter teaches you how.

---

## Project: Build a Training Institute Website

### What We're Building

A 5-page website for a computer training institute — the kind of project that earns Rs 5,000-15,000 on freelance platforms.

**Pages:**
1. Home — Hero section, features, testimonials
2. Courses — Course cards with details
3. About — Team, mission, stats
4. Contact — Form, map, info
5. Blog — Article list layout

---

### Phase 1: Plan with AI

Before touching any code, plan the website with AI.

**Prompt to ChatGPT/Claude:**
```
I'm building a website for "TechPath Institute" — a computer 
training center in Pune, India.

Courses: ADCA (12 months, ₹35,000), DCA (6 months, ₹18,000), 
Tally Pro (3 months, ₹8,000)
USPs: 85% placement rate, industry trainers, AC labs, 30 computers

Create a detailed sitemap with:
1. All 5 pages with their sections
2. Content outline for each section (headings, bullet points)
3. CTA (call-to-action) strategy for each page
4. Color scheme suggestion (professional, trustworthy)
5. What content I need (text, images, testimonials)

Format as a structured document I can follow.
```

---

### Phase 2: Generate with v0.dev or Bolt.new

**Using v0.dev (Vercel's AI):**

Go to v0.dev and enter:
```
Create a modern, responsive hero section for a computer training 
institute called "TechPath Institute". Include:
- Navigation bar with logo, menu items (Home, Courses, About, Contact)
- Large heading: "Launch Your IT Career in 12 Months"
- Subheading about placement rate and practical training
- Two CTA buttons: "Explore Courses" (primary) and "Book Free Demo" (outline)
- Trust indicators: "500+ Students Placed | 85% Placement Rate | 15+ Hiring Partners"
- Modern gradient background, Indian context
- Fully responsive, works on mobile
```

**Using Bolt.new:**
```
Build a complete 5-page website for TechPath Institute, 
a computer training center. Include:
- Responsive navbar with mobile hamburger menu
- Home: Hero + 3 feature cards + testimonials carousel + CTA
- Courses: 3 course cards with pricing, duration, syllabus toggle
- About: Team section, stats counter, mission statement
- Contact: Contact form + Google Maps embed + address/phone
- Footer: Links, social media, newsletter signup
- Use Tailwind CSS, modern design, Indian rupee pricing
```

> 🖼️ **IMAGE:** Screenshot of v0.dev interface showing a generated hero section code preview on the left and the live rendered component on the right — showing the TechPath hero section with gradient background, heading, and CTA buttons
> `v0-dev-hero-generation.png`

---

### Phase 3: Customize the AI Output

AI gives you 80% of the work. The remaining 20% is what makes it yours.

**Common things to customize:**

| What | AI Default | Your Change |
|------|-----------|-------------|
| Colors | Random blue | Brand colors from Figma |
| Font | System font | Google Fonts (Inter, Poppins) |
| Images | Placeholder/stock | Real photos or Unsplash |
| Text | Lorem ipsum or generic | Real institute content |
| Layout spacing | Inconsistent | 8px spacing system |
| Mobile menu | Basic | Smooth slide-in animation |
| Contact form | Non-functional | Connect to Formspree or backend |
| SEO | Missing | Add meta tags, title, description |

### Essential Customizations

**1. SEO Meta Tags (every page needs these)**

```html
<head>
    <title>TechPath Institute — Best Computer Training in Pune | ADCA, DCA Courses</title>
    <meta name="description" content="Join TechPath Institute for industry-ready 
    computer courses. ADCA, DCA, Tally with 85% placement rate. Enroll now!">
    <meta name="keywords" content="computer course Pune, ADCA course, IT training, 
    placement guarantee, coding classes">
    <meta property="og:title" content="TechPath Institute — Launch Your IT Career">
    <meta property="og:description" content="85% placement rate. Learn from industry experts.">
    <meta property="og:image" content="https://techpath.biz/og-image.png">
    <link rel="canonical" href="https://techpath.biz">
</head>
```

**2. Working Contact Form (using Formspree)**

```html
<form action="https://formspree.io/f/your-form-id" method="POST">
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="tel" name="phone" placeholder="Phone Number" required>
    <select name="course">
        <option value="">Select Course</option>
        <option value="ADCA">ADCA — 12 Months (₹35,000)</option>
        <option value="DCA">DCA — 6 Months (₹18,000)</option>
        <option value="Tally">Tally Pro — 3 Months (₹8,000)</option>
    </select>
    <textarea name="message" placeholder="Your Message"></textarea>
    <button type="submit">Send Enquiry</button>
</form>
```

**3. Google Analytics**

```html
<!-- Add before closing </head> tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

### Phase 4: Debug with AI

When something doesn't work (and it won't the first time):

```
My navbar hamburger menu doesn't open on mobile. Here's my HTML 
and CSS code:

[paste code]

The issue is: clicking the hamburger icon does nothing.
The expected behavior is: a slide-in menu should appear.

Fix this and explain what was wrong.
```

### Common Issues AI Helps Fix

| Issue | Prompt |
|-------|--------|
| Layout broken on mobile | "This layout breaks below 768px. Fix the CSS responsive design" |
| Form not submitting | "My form shows 405 error. Here's the form HTML..." |
| Images not loading | "Images show broken icon. Paths are..." |
| Slow page load | "My page takes 8 seconds to load. Here's the code, suggest optimizations" |
| CSS not applying | "This CSS rule isn't taking effect. Here's the HTML structure and CSS..." |

---

### Phase 5: Deploy for Free

#### Option A: GitHub Pages (simplest)

```bash
# 1. Create GitHub repo
git init
git add .
git commit -m "Initial website"
git remote add origin https://github.com/you/techpath-website.git
git push -u origin main

# 2. Go to GitHub repo → Settings → Pages
# 3. Source: main branch, / (root) folder
# 4. Save → site is live at: https://you.github.io/techpath-website/
```

#### Option B: Vercel (recommended)

```bash
npm install -g vercel
vercel login
vercel
# Follow prompts → site is live at a vercel.app URL
```

#### Option C: Netlify (drag and drop)

1. Go to netlify.com → Sign up
2. Drag your project folder into the browser
3. Site is live instantly!

---

### Phase 6: Add Custom Domain

1. Buy domain from GoDaddy/Namecheap/Hostinger (Rs 500-1000/year)
2. In your hosting dashboard (Vercel/Netlify):
   - Settings → Domains → Add custom domain
3. In domain registrar:
   - Add DNS record: CNAME → `your-site.vercel.app`
4. Wait 5-30 minutes → your site is live at `www.yourdomain.com`!

> 🖼️ **IMAGE:** Split screen showing Vercel dashboard "Domain" settings on the left (with custom domain field and DNS instructions), and GoDaddy/Namecheap DNS records panel on the right (showing the CNAME record being added) — arrows showing which value goes where
> `custom-domain-setup.png`

---

## Freelance Project Workflow

When a client hires you to build their website:

```
Day 1: Understand requirements (call/meeting)
       └→ What pages? What content? Any references?

Day 2: Plan with AI (sitemap, content outline)
       └→ Share plan with client for approval

Day 3: Generate with AI tools (v0, Bolt, Cursor)
       └→ Get the 80% done fast

Day 4: Customize (colors, content, images, forms)
       └→ Make it unique, not template-looking

Day 5: Test & Fix (mobile, speed, forms, links)
       └→ Test on phone, tablet, desktop

Day 6: Deploy & handover (hosting, domain, docs)
       └→ Client gets live URL + admin access
```

**Pricing guide for beginners:**

| Project Type | Time | Price Range |
|-------------|------|-------------|
| Landing page (1 page) | 1-2 days | Rs 3,000-5,000 |
| Business website (3-5 pages) | 3-5 days | Rs 5,000-15,000 |
| Portfolio site | 2-3 days | Rs 3,000-8,000 |
| E-commerce (basic) | 5-7 days | Rs 10,000-25,000 |

---

## Practice Exercise

### Build and deploy one of these:

1. **Personal portfolio** — Your own portfolio page, deployed live
2. **Restaurant website** — Menu, about, contact, gallery
3. **Gym/fitness center** — Classes, trainers, pricing, contact
4. **Coaching center** — Similar to TechPath but your own design

**Requirements:**
- At least 3 pages
- Fully responsive (works on phone)
- Working contact form
- Deployed to a live URL
- SEO meta tags added
- Page loads in under 3 seconds

Share the live URL on your LinkedIn and GitHub!
