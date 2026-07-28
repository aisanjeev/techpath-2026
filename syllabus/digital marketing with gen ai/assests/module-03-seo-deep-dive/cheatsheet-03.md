# Module 3: SEO Cheat Sheet

## TechPath Academy | Digital Marketing with Gen AI

---

## Title Tag Formula

```
Primary Keyword | Secondary Keyword | Brand Name
```
- Length: 50-60 characters
- Put most important keyword first
- Example: `Digital Marketing Course Bhopal | 100% Placement | TechPath`

---

## Meta Description Formula

```
[What you offer] + [Key benefit/proof] + [CTA]
```
- Length: 150-155 characters
- Include primary keyword naturally
- Example: `Learn Digital Marketing in 6 months at TechPath Bhopal. 500+ students placed in top companies. Limited seats — Enroll now!`

---

## Core Web Vitals Thresholds

| Metric | Good | Needs Work | Poor |
|--------|------|-----------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |

---

## robots.txt Syntax

```
User-agent: *              # All bots
Disallow: /admin/          # Block admin
Disallow: /cart/           # Block cart
Disallow: /search?         # Block internal search
Allow: /blog/              # Explicitly allow

Sitemap: https://example.com/sitemap.xml
```

Key rules:
- `Disallow: /` = block everything
- `Disallow:` (empty) = allow everything
- `*` = wildcard (all bots)
- Lines starting with `#` = comments

---

## XML Sitemap Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page/</loc>
    <lastmod>2026-07-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

Priority guide: Homepage = 1.0, Service pages = 0.8, Blog = 0.6, Legal = 0.3

---

## JSON-LD Schema Template (FAQ)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Your question here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Your answer here."
      }
    }
  ]
}
```

---

## Google Search Operators

| Operator | What It Does | Example |
|----------|-------------|---------|
| `site:` | Search within one site | `site:techpath.biz SEO` |
| `inurl:` | Find keyword in URL | `inurl:digital-marketing-course` |
| `intitle:` | Find keyword in title | `intitle:"best coaching Varanasi"` |
| `intext:` | Find keyword in body text | `intext:"SEO course fee"` |
| `filetype:` | Find specific file types | `filetype:pdf SEO checklist` |
| `-` | Exclude a term | `SEO course -free` |
| `" "` | Exact match phrase | `"digital marketing institute Bhopal"` |
| `*` | Wildcard (any word) | `"best * course in India"` |
| `OR` | Either term | `SEO OR SEM course` |
| `related:` | Similar websites | `related:techpath.biz` |

---

## Backlink Quality Checklist

A good backlink has:
- [ ] High Domain Authority (DA 30+)
- [ ] Relevant to your niche/industry
- [ ] Dofollow (passes link equity)
- [ ] From a page with real traffic
- [ ] Natural anchor text (not keyword-stuffed)
- [ ] Editorial placement (within content, not footer/sidebar)
- [ ] From a unique referring domain (not the same site again)
- [ ] Recently published/updated page

---

## Local SEO NAP Checklist

**NAP = Name, Address, Phone** (must be identical everywhere)

- [ ] Google Business Profile
- [ ] Website footer and contact page
- [ ] Facebook Business Page
- [ ] Instagram Business Profile
- [ ] Justdial listing
- [ ] Sulekha listing
- [ ] IndiaMART (if applicable)
- [ ] Yelp India
- [ ] LinkedIn Company Page
- [ ] Apple Maps

**Rules:**
- Exact same spelling (don't abbreviate "Road" in one place and write "Rd." in another)
- Same phone number format everywhere (+91-7000-123456)
- Same pin code format
- Update ALL listings if anything changes

---

## On-Page SEO Quick Checklist

- [ ] Title tag: 50-60 chars, primary keyword first
- [ ] Meta description: 150-155 chars, includes CTA
- [ ] URL: Short, lowercase, hyphens, keyword included
- [ ] H1: One per page, includes primary keyword
- [ ] H2-H3: Logical hierarchy, includes secondary keywords
- [ ] Images: Alt text, compressed, descriptive file names
- [ ] Internal links: 3-5 per page, descriptive anchor text
- [ ] External links: 1-2 to authoritative sources
- [ ] Schema markup: Relevant type (FAQ, Article, LocalBusiness)
- [ ] Content: Answers user intent, 1500+ words for competitive keywords
- [ ] Keyword density: 1-2% (don't stuff)
- [ ] Mobile: Readable, tappable, no horizontal scroll

---

## Heading Structure Template

```
H1: Primary Keyword + Context
  H2: Major Topic 1
    H3: Subtopic 1a
    H3: Subtopic 1b
  H2: Major Topic 2
    H3: Subtopic 2a
    H3: Subtopic 2b
  H2: FAQ / Related Questions
    H3: Question 1
    H3: Question 2
```

---

## Quick Keyword Research Process

1. **Seed** — Write 5 broad topics related to your business
2. **Expand** — Put each into Ubersuggest/Keyword Planner, get 50+ suggestions
3. **Filter** — Remove irrelevant terms, keep volume > 100
4. **Classify** — Tag each with intent (info/nav/transact/commercial)
5. **Prioritize** — Pick KD < 30 + volume > 100 + matching intent
6. **Map** — Assign 1 primary keyword per page (no cannibalization)

---

## SEO Metrics to Track Monthly

| Metric | Tool | Target |
|--------|------|--------|
| Organic Traffic | Google Analytics 4 | Month-over-month growth |
| Keyword Rankings | GSC / SE Ranking | Top 20 keywords improving |
| Impressions | Google Search Console | Steady increase |
| CTR | Google Search Console | > 3% average |
| Backlinks | Ahrefs / GSC | New referring domains monthly |
| Core Web Vitals | PageSpeed Insights | All green |
| Indexed Pages | GSC Coverage Report | No unexpected drops |
| Bounce Rate | GA4 | < 60% for blog content |

---

## Content Length Guidelines

| Content Type | Recommended Length | When to Use |
|-------------|-------------------|-------------|
| Blog Post (informational) | 1,500 - 3,000 words | Targeting competitive keywords |
| Service Page | 800 - 1,500 words | For each service you offer |
| Product Page | 500 - 1,000 words | E-commerce products |
| Landing Page | 500 - 1,500 words | Ads/campaign landing |
| Pillar Page | 3,000 - 5,000+ words | Topical authority building |
| FAQ Page | 1,000 - 2,000 words | Common questions |

---

## Quick Fixes for Common SEO Issues

| Issue | Quick Fix |
|-------|-----------|
| Slow LCP | Compress images, use WebP, add lazy loading |
| High CLS | Set width/height on images, reserve ad space |
| Duplicate content | Add canonical tags |
| Pages not indexed | Check robots.txt, submit in GSC |
| Low CTR | Rewrite title tag and meta description |
| Keyword cannibalization | Merge pages or differentiate intent |
| Broken links (404) | Redirect to relevant page (301) |
| Thin content | Expand to 1500+ words or merge with similar page |
