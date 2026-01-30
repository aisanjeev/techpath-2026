# Home Page – Performance Marketing Sections Plan

This doc outlines sections you can add to the home (and key landing) pages to align with **performance marketing best practices**: conversion, trust, clarity, and SEO.

---

## Already Implemented

| Section | Purpose | Data source |
|--------|---------|-------------|
| **Hero** | Above-the-fold value prop + primary CTA | Content API (home_landing_content) |
| **Stats** | Social proof, credibility | Content API |
| **Services** | Core offerings, internal links | Content API |
| **Case Studies** | Proof of results, trust | Case Studies API |
| **Features / Why Us** | Differentiators | Content API |
| **Testimonials** | Third-party validation | Content API |
| **FAQ** | Objection handling, long-tail SEO | Content API |
| **CTA** | Final conversion nudge | Content API |

---

## Recommended Sections to Add (Performance Marketing)

### 1. **Trust / Logos Bar**
- **Goal:** Instant credibility (“Trusted by X”).
- **Content:** 4–8 client or partner logos (or “As seen in”).
- **Best practice:** Grayscale, same height, link optional. Editable via Content API (list of logo URLs + optional links).
- **Placement:** Right after Hero or after Stats.

### 2. **Social Proof / Reviews Strip**
- **Goal:** Reinforce ratings (Google, G2, etc.) and review count.
- **Content:** “4.9/5 from 200+ reviews”, “G2 High Performer”, “Top 10 in category”.
- **Best practice:** Schema.org `AggregateRating` already helps SEO; a visible strip increases trust.
- **Data:** Content API (e.g. `reviews_strip: { rating, count, source, badge_url }`).

### 3. **Problem–Agitate–Solve (PAS) or Pain Points**
- **Goal:** Nail the problem, then present your solution.
- **Content:** 3–4 short “Struggling with X? We do Y.”
- **Best practice:** One line per pain, one line per outcome. Drives relevance and conversion.
- **Data:** Content API (list of `{ problem, outcome }` or reuse training-page style pain points).

### 4. **How It Works / Process**
- **Goal:** Reduce uncertainty (“What happens next?”).
- **Content:** 3–5 steps: e.g. “Consult → Plan → Build → Support”.
- **Best practice:** Numbered steps, short title + one sentence. Builds confidence before CTA.
- **Data:** Content API (e.g. `process_steps: [{ step, title, description }]`).

### 5. **Lead Magnet / Resource CTA**
- **Goal:** Capture leads without “Contact us” only.
- **Content:** “Download our Guide to X”, “Get the ROI Calculator”, “Watch the 5-min demo”.
- **Best practice:** One clear offer, form or link. Track in analytics.
- **Data:** Content API (title, description, button label, href, optional image).

### 6. **Industry or Use-Case Pills**
- **Goal:** “This is for people like me” + internal links.
- **Content:** Pills/chips: “Healthcare”, “Fintech”, “Retail”, “Startups”.
- **Best practice:** Link to /services or /case-studies filtered by industry/tag.
- **Data:** Content API or Tags API (list of `{ label, slug, href }`).

### 7. **Comparison / “Why Us vs Others”**
- **Goal:** Differentiate and pre-empt objections.
- **Content:** Simple table or list: “Us: X, Y, Z — Others: A, B, C”.
- **Best practice:** 3–5 rows max. Honest and specific.
- **Data:** Content API (e.g. `comparison: { us: string[], others: string[] }` or row-based).

### 8. **Urgency / Scarcity (Optional, Ethical)**
- **Goal:** Nudge for high-intent pages (e.g. training, limited cohort).
- **Content:** “Next cohort starts March 1”, “Only 5 spots left”, “Offer ends Friday”.
- **Best practice:** Only if true and not misleading. Can live in Hero badge or a small banner.
- **Data:** Content API (text, optional end date for countdown).

### 9. **Video Testimonial or Explainer**
- **Goal:** Higher engagement and trust than text-only.
- **Content:** One hero video (testimonial or 60–90 sec explainer).
- **Best practice:** Above the fold or after Hero; thumbnail + play button.
- **Data:** Content API (video_url, thumbnail_url, title, caption).

### 10. **Blog / Resources Teaser**
- **Goal:** SEO, authority, and repeat visits.
- **Content:** “Latest from our blog” – 3 posts with title, excerpt, image, link.
- **Best practice:** Fetch from Blog API; encourages internal linking and fresh content.
- **Data:** Blog API (existing); section title/subtitle from Content API.

---

## Suggested Order on Home Page

A flow that supports performance marketing:

1. **Hero** (value prop + CTA)
2. **Trust / Logos** (optional)
3. **Stats**
4. **Services**
5. **Case Studies** (proof)
6. **Pain Points or PAS** (optional)
7. **Features / Why Us**
8. **How It Works** (optional)
9. **Testimonials**
10. **Lead Magnet CTA** (optional)
11. **FAQ**
12. **Final CTA**

---

## Implementation Notes

- **Content API:** Add new blocks to `home_landing_content` (and optionally other landing pages) with sensible defaults so the site works without DB content.
- **New sections:** Prefer reusable Astro components (e.g. `TrustLogos.astro`, `ProcessSteps.astro`) and pass content from the Content API or other APIs.
- **SEO:** Keep one H1 per page (Hero); use H2 for section titles. Add/update schema.org where relevant (e.g. `HowTo` for process, `FAQPage` for FAQ).
- **Performance:** Lazy-load below-the-fold images and optional video; keep hero minimal for LCP.

You can phase these in: start with **Trust Logos**, **How It Works**, and **Blog Teaser** for quick wins, then add **Pain Points**, **Lead Magnet**, and **Reviews Strip** as needed.
