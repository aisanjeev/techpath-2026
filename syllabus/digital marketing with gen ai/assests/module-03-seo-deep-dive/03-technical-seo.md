# Technical SEO

**Module 03 — SEO Deep Dive | Topic 3**

---

## What is Technical SEO?

**Technical SEO** covers all the behind-the-scenes work that helps search engines crawl, index, and render your website properly. Even the best content will not rank if Google cannot access or understand your pages.

> **Simple Analogy:** On-page SEO is the design of your shop and the products inside. Technical SEO is the plumbing, electricity, and road access that makes the shop functional. If the road is broken, no customers can reach you — no matter how good your products are.

---

## Core Web Vitals

Google uses three performance metrics called **Core Web Vitals** as ranking signals. These measure real user experience on your website.

| Metric | Full Name | What It Measures | Good | Needs Improvement | Poor |
|--------|-----------|------------------|------|-------------------|------|
| **LCP** | Largest Contentful Paint | How fast the largest visible content loads | < 2.5 seconds | 2.5s - 4.0s | > 4.0s |
| **INP** | Interaction to Next Paint | How fast the page responds when user clicks/taps | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift | How much content jumps around while loading | < 0.1 | 0.1 - 0.25 | > 0.25 |

> **Real Example (CLS):** You are reading a news article on your phone. Just as you tap a link, an ad loads above it and pushes the content down. You accidentally click the ad instead. That annoying jump is what CLS measures.

### How to Check Core Web Vitals

| Tool | Type | What It Shows |
|------|------|--------------|
| **PageSpeed Insights** (pagespeed.web.dev) | Lab + Field data | LCP, INP, CLS scores with specific fix recommendations |
| **Google Lighthouse** (Chrome DevTools > Lighthouse tab) | Lab data | Performance score, accessibility, SEO audit |
| **Google Search Console** (Core Web Vitals report) | Field data | Pages grouped as Good, Needs Improvement, or Poor |
| **Chrome User Experience Report (CrUX)** | Field data | Real user data from Chrome browsers |

### How to Improve Each Metric

**LCP — Make the main content load faster:**

| Problem | Fix |
|---------|-----|
| Large hero image (2MB JPEG) | Compress to WebP (200KB), add width/height attributes |
| Heavy CSS/JS blocking render | Minify CSS, defer non-critical JS, inline critical CSS |
| Slow server response | Use a CDN (Cloudflare free tier works great for Indian sites) |
| No browser caching | Set cache headers for static assets (images, CSS, JS) |
| Third-party scripts loading first | Load analytics/chat widgets after page content |

**INP — Make the page respond to clicks faster:**

| Problem | Fix |
|---------|-----|
| Heavy JavaScript on main thread | Break long tasks into smaller chunks |
| Too many event listeners | Remove unused JavaScript, use event delegation |
| Complex animations | Use CSS animations instead of JavaScript, use `requestAnimationFrame` |

**CLS — Stop content from jumping:**

| Problem | Fix |
|---------|-----|
| Images without dimensions | Always add `width` and `height` attributes to `<img>` tags |
| Ads loading and pushing content | Reserve space for ads using CSS `min-height` |
| Web fonts causing text shift | Use `font-display: swap` in your CSS |
| Content injected above fold | Never dynamically insert banners above existing content |

---

## Page Speed Optimisation

| Technique | What It Does | Impact |
|-----------|-------------|--------|
| **Image compression** | Reduce file size without visible quality loss | High — images are usually the largest files on a page |
| **Minification** | Remove whitespace and comments from CSS/JS code | Medium — saves 10-30% file size |
| **CDN (Content Delivery Network)** | Serve files from a server nearest to the user | High — Indian user gets content from Mumbai server instead of US |
| **Browser caching** | Store static files on user's device so they load instantly on repeat visits | Medium |
| **Lazy loading** | Load images only when user scrolls to them | Medium-High |
| **Above-the-fold optimisation** | Load visible content first, defer the rest | High |
| **GZIP / Brotli compression** | Compress text files (HTML, CSS, JS) during transfer | Medium — reduces transfer size by 60-80% |

> **Pro Tip:** For Indian websites, Cloudflare's free plan provides CDN, GZIP compression, and basic caching — all with no cost. This alone can improve your PageSpeed score by 15-30 points.

---

## Mobile-First Indexing

Since 2019, Google primarily uses the **mobile version** of your website for ranking — even for desktop searches. This is called **mobile-first indexing**.

**What this means for you:**

| Check | Why It Matters |
|-------|---------------|
| Site is responsive (adapts to all screen sizes) | If your desktop site looks great but mobile is broken, rankings suffer |
| Same content on mobile and desktop | Do not hide content on mobile — Google indexes the mobile version |
| Tap targets are 48px minimum | Small buttons frustrate mobile users |
| No intrusive popups on mobile | Google penalises pages with full-screen popups on mobile |
| Text readable without zooming (16px+ base font) | If users have to pinch-to-zoom, your mobile experience is poor |

---

## HTTPS and SSL

**HTTPS** (HyperText Transfer Protocol Secure) encrypts data between user and server. It is a confirmed Google ranking factor.

| HTTP | HTTPS |
|------|-------|
| Not encrypted — data can be intercepted | Encrypted — data is secure |
| Browser shows "Not Secure" warning | Browser shows padlock icon |
| No ranking boost | Confirmed ranking signal |
| Free | Free via Let's Encrypt |

**Steps to implement:**
1. Get an SSL certificate (Let's Encrypt is free)
2. Install it on your web server
3. Redirect all HTTP URLs to HTTPS using 301 redirects
4. Update all internal links to use HTTPS
5. Fix mixed content (HTTP images/scripts on HTTPS pages)

---

## robots.txt

The `robots.txt` file lives at `yoursite.com/robots.txt` and tells search engine bots which pages they can and cannot crawl.

### Syntax and Examples

```
# Allow all bots to crawl everything
User-agent: *
Allow: /

# Block admin and private pages
User-agent: *
Disallow: /admin/
Disallow: /cart/
Disallow: /thank-you/
Disallow: /wp-admin/

# Allow blog to be crawled
Allow: /blog/

# Tell bots where to find the sitemap
Sitemap: https://techpath.biz/sitemap.xml
```

### Key Rules

| Rule | Meaning |
|------|---------|
| `User-agent: *` | Applies to all bots |
| `User-agent: Googlebot` | Applies only to Google's bot |
| `Disallow: /` | Block everything (dangerous — do not use unless intentional) |
| `Disallow:` (empty value) | Allow everything |
| `Disallow: /admin/` | Block the /admin/ directory |
| `Sitemap:` directive | Tells bots where your XML sitemap is located |

> **Important Warning:** robots.txt is a **suggestion**, not a security measure. Malicious bots can ignore it completely. Never use robots.txt to hide sensitive pages — use password protection or noindex instead.

---

## XML Sitemap

An XML sitemap (`sitemap.xml`) is a file listing all the important pages on your site that you want search engines to index.

### What to Include and Exclude

| Include | Exclude |
|---------|---------|
| All important content pages | Admin/login pages |
| Blog posts | Thank-you/confirmation pages |
| Product/service pages | Paginated tag/author archives |
| Category pages | Duplicate content pages |
| Contact/about pages | Pages with noindex tag |

### How to Submit

1. Generate sitemap using your CMS (WordPress: Yoast SEO plugin) or an online generator
2. Upload `sitemap.xml` to your website root
3. Go to Google Search Console > Sitemaps
4. Enter `https://yoursite.com/sitemap.xml` and click Submit
5. Check back in a few days to see how many URLs Google has discovered and indexed

---

## Canonical Tags

A **canonical tag** tells Google which version of a page is the "original" when the same content exists at multiple URLs.

```html
<link rel="canonical" href="https://techpath.biz/courses/digital-marketing/" />
```

### When to Use Canonical Tags

| Scenario | Problem | Canonical Solution |
|----------|---------|-------------------|
| Page accessible via multiple URLs | `techpath.biz/courses/dm` and `techpath.biz/courses/digital-marketing` | Point both to one canonical URL |
| HTTP and HTTPS versions | Same page at http:// and https:// | Canonical to HTTPS version |
| www and non-www | `www.techpath.biz` and `techpath.biz` | Pick one, canonical to it |
| URL parameters | `/products?color=red&size=L` and `/products?size=L&color=red` | Canonical to the clean base URL |
| Syndicated content | Your article republished on Medium | Canonical on Medium copy pointing to your original |

---

## Hreflang Tags (Multilingual Sites)

If your website has content in multiple languages (common in India with Hindi and English versions), use **hreflang** tags to tell Google which version to show to which audience.

```html
<link rel="alternate" hreflang="en" href="https://techpath.biz/courses/" />
<link rel="alternate" hreflang="hi" href="https://techpath.biz/hi/courses/" />
<link rel="alternate" hreflang="x-default" href="https://techpath.biz/courses/" />
```

- `x-default` = fallback for users whose language is not specified

---

## 301 vs 302 Redirects

| Type | Name | When to Use | SEO Impact |
|------|------|-------------|-----------|
| **301** | Permanent Redirect | Page permanently moved to new URL | Passes 90-99% of link equity to new URL |
| **302** | Temporary Redirect | Page temporarily moved (maintenance, A/B testing) | Does NOT pass link equity — old URL keeps its rankings |

> **Common Mistake:** Many Indian websites use 302 redirects when they should use 301. If you permanently changed your URL from `/old-page/` to `/new-page/`, always use 301 — otherwise you lose all the SEO authority the old page had built up.

---

## Crawl Errors and How to Fix Them

| Error | What It Means | How to Fix |
|-------|---------------|-----------|
| **404 Not Found** | Page does not exist | 301 redirect to a relevant page, or create the missing page |
| **500 Server Error** | Server crashed while loading the page | Check server logs, fix code errors, contact hosting provider |
| **Soft 404** | Page returns 200 status but shows error content | Return proper 404 status code for missing pages |
| **Redirect Chain** | A redirects to B, B redirects to C | Update A to redirect directly to C |
| **Redirect Loop** | A redirects to B, B redirects back to A | Fix the redirect rules to break the loop |
| **Blocked by robots.txt** | Important page is disallowed in robots.txt | Remove the Disallow rule for that page |

---

## Site Architecture

Good site architecture means any page is reachable within **3 clicks from the homepage**.

### Flat vs Deep Architecture

| Type | Structure | Example | SEO Impact |
|------|----------|---------|-----------|
| **Flat** | Homepage > Page (2 levels) | `techpath.biz/seo-course/` | Easy to crawl, authority flows well |
| **Medium** | Homepage > Category > Page (3 levels) | `techpath.biz/courses/seo-course/` | Ideal for most websites |
| **Deep** | Homepage > Cat > Subcat > Sub-subcat > Page (5+ levels) | `techpath.biz/edu/courses/marketing/seo/basics/` | Hard to crawl, authority diluted |

**Best Practice:** Keep click depth to 3 levels maximum. Use breadcrumb navigation so users (and Google) always know where they are.

```
Home > Courses > Digital Marketing Course
```

---

## Trainer Activity: Run PageSpeed Insights on 3 Websites and Compare

> **Class Exercise (20 minutes)**
>
> **Task:** Open PageSpeed Insights (pagespeed.web.dev) and test 3 websites:
> 1. A large brand website (e.g., flipkart.com or zomato.com)
> 2. A local small business website from your city
> 3. Your own project website (or techpath.biz)
>
> **For each website, record:**
>
> | Metric | Website 1 | Website 2 | Website 3 |
> |--------|-----------|-----------|-----------|
> | **Performance Score (Mobile)** | | | |
> | **Performance Score (Desktop)** | | | |
> | **LCP** | | | |
> | **INP** | | | |
> | **CLS** | | | |
> | **Largest Issue Identified** | | | |
>
> **Discussion Questions:**
> - Which website scored best? Why do you think so?
> - Why is the mobile score almost always lower than desktop?
> - Pick the worst-scoring site — what are the top 3 fixes Google recommends?
> - What free tools or techniques could the small business use to improve their score?

---

## Summary

- **Core Web Vitals** are Google's page experience ranking signals: LCP (< 2.5s), INP (< 200ms), CLS (< 0.1)
- Use **PageSpeed Insights** and **Lighthouse** to check and improve your scores
- Key speed fixes: compress images (WebP), use a CDN, enable caching, minify CSS/JS, lazy load images
- **Mobile-first indexing** means Google primarily ranks the mobile version of your site
- **HTTPS** is a ranking factor — use free SSL from Let's Encrypt
- **robots.txt** tells bots what to crawl; **XML sitemap** lists pages you want indexed
- **Canonical tags** prevent duplicate content issues by pointing Google to the original URL
- Use **301 redirects** for permanent URL changes (passes SEO authority) and **302** only for temporary moves
- Keep **site architecture flat** — every page reachable within 3 clicks from the homepage
- Fix crawl errors (404s, redirect chains, server errors) regularly using Google Search Console
