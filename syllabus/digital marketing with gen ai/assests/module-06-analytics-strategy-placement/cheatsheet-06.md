# Module 6: Cheatsheet — Analytics, Strategy & Career

## GA4 Key Events List

### Automatically Collected Events (No Setup Needed)
| Event | What It Tracks |
|-------|---------------|
| `first_visit` | User's first visit ever |
| `session_start` | A new session begins |
| `page_view` | A page is loaded/viewed |
| `user_engagement` | App/site is in focus for 1+ seconds |

### Enhanced Measurement Events (Toggle On in Admin)
| Event | What It Tracks |
|-------|---------------|
| `scroll` | User scrolls past 90% of page |
| `click` (outbound) | Click on link leaving your site |
| `file_download` | PDF, doc, xls, etc. downloaded |
| `video_start` | Embedded YouTube video starts |
| `video_progress` | 10%, 25%, 50%, 75% watched |
| `video_complete` | Video watched to end |
| `view_search_results` | Site search performed |

### Recommended Events (You Set Up)
| Event | Use Case |
|-------|----------|
| `sign_up` | Account creation |
| `login` | User logs in |
| `add_to_cart` | Product added to cart |
| `begin_checkout` | Checkout process started |
| `purchase` | Transaction completed |
| `generate_lead` | Lead form submitted |
| `share` | Content shared |

---

## UTM Parameter Quick Guide

### Structure
```
https://yoursite.com/page?utm_source=___&utm_medium=___&utm_campaign=___
```

### Standard Values

| utm_source | utm_medium | When to Use |
|-----------|-----------|-------------|
| `google` | `cpc` | Google Ads (paid search) |
| `google` | `organic` | Auto-detected (don't set) |
| `facebook` | `paid_social` | Facebook/Meta paid ads |
| `instagram` | `social` | Instagram organic posts |
| `newsletter` | `email` | Email campaigns |
| `whatsapp` | `messaging` | WhatsApp broadcasts |
| `youtube` | `video` | YouTube descriptions |
| `linkedin` | `social` | LinkedIn organic |
| `qr_code` | `offline` | Physical marketing |

### Naming Rules
- Always lowercase
- Underscores for spaces (not hyphens or %20)
- Include date: `campaign_name_jul2026`
- Be specific: `instagram_story` not just `social`
- No special characters: ? & # @

---

## Attribution Models (1-Line Each)

| Model | Credit Goes To |
|-------|---------------|
| **Last Click** | Final touchpoint before purchase (simple but unfair to awareness) |
| **First Click** | The channel that introduced the user (ignores nurture) |
| **Linear** | Equal split across all touchpoints (fair but unhelpful for prioritizing) |
| **Time Decay** | More credit to recent touches (good for long cycles) |
| **Position-Based** | 40% first + 40% last + 20% middle (balanced for most businesses) |
| **Data-Driven** | AI allocates based on actual patterns (GA4 default, best accuracy) |

---

## Looker Studio Data Sources

| Source | What You Can Report On |
|--------|----------------------|
| Google Analytics 4 | Website traffic, engagement, conversions |
| Google Ads | Ad performance, keywords, cost |
| Google Search Console | SEO: impressions, clicks, positions |
| Google Sheets | Any manual data, CRM exports, budgets |
| BigQuery | Large datasets, warehouse |
| MySQL / PostgreSQL | Direct database connection |
| Facebook Ads | Via Supermetrics or Funnel.io (paid connectors) |
| CSV Upload | One-time data imports |

---

## Pitch Deck: 10-Slide Template

| # | Slide | Time | Key Content |
|---|-------|------|-------------|
| 1 | Cover | 15s | Title, name, date, client logo |
| 2 | About Us | 45s | Credentials, team, 2 achievements |
| 3 | The Challenge | 60s | Their problems with DATA (audit findings) |
| 4 | Market Opportunity | 60s | Industry size, trends, competitor gaps |
| 5 | Our Strategy | 90s | 3-4 pillars, channels, high-level approach |
| 6 | Tactical Plan | 90s | 90-day timeline, month-by-month actions |
| 7 | Expected Results | 60s | Projected KPIs with numbers at 3/6/12 months |
| 8 | Case Study | 60s | Similar result, before/after with proof |
| 9 | Investment | 60s | Pricing packages, ROI justification |
| 10 | Next Steps | 30s | CTA, timeline, contact info |

**Total presentation time: 8-10 minutes**

---

## Pricing Benchmarks India 2026 (Digital Marketing Services)

| Service | Monthly Retainer | Per Project |
|---------|-----------------|-------------|
| SEO (basic) | Rs 15,000 - 30,000 | Rs 50,000 - 1,50,000 |
| SEO (advanced) | Rs 30,000 - 50,000 | Rs 1,50,000 - 5,00,000 |
| Social Media Management | Rs 10,000 - 30,000 | — |
| Content Writing (per piece) | — | Rs 1,000 - 5,000/article |
| PPC Management | 15-20% of ad spend | Min Rs 10,000/month |
| Email Marketing | Rs 5,000 - 15,000 | — |
| Full-Service Digital Marketing | Rs 50,000 - 2,00,000 | — |
| WhatsApp Marketing | Rs 5,000 - 20,000 | — |
| Influencer Campaign | — | Rs 25,000 - 5,00,000 |
| Website (WordPress) | — | Rs 25,000 - 1,50,000 |
| Landing Page | — | Rs 5,000 - 25,000 |

**Freelancer hourly rates:**
- Beginner (0-1 yr): Rs 500 - 1,000/hr
- Intermediate (1-3 yr): Rs 1,000 - 2,500/hr
- Expert (3+ yr): Rs 2,500 - 5,000/hr
- International clients: $15 - $50/hr (Rs 1,250 - 4,200/hr)

---

## ATS Resume Checklist

- [ ] Simple single-column format (no tables, graphics, headers/footers)
- [ ] Standard fonts: Arial, Calibri, or Times New Roman (11-12pt)
- [ ] Standard section headings: Summary, Experience, Education, Skills, Certifications
- [ ] Keywords from job description included naturally
- [ ] Bullet points starting with ACTION VERBS (Managed, Created, Increased, Built)
- [ ] Numbers/metrics in achievements (Increased traffic by 150%, Managed Rs 5L budget)
- [ ] Dates in standard format (Jun 2025 - Present)
- [ ] 1 page for 0-5 years experience
- [ ] Saved as PDF (unless .docx specified)
- [ ] No images, icons, or colored boxes
- [ ] Acronyms spelled out first: "Search Engine Optimization (SEO)"
- [ ] Contact: Name, Phone, Email, LinkedIn, City (no full address needed)
- [ ] Tested with a free ATS scanner (resumeworded.com or jobscan.co)

---

## 10 Must-Know Interview Answers (Condensed)

| Question | Answer Framework |
|----------|-----------------|
| "What is digital marketing?" | Marketing via digital channels — SEO, social, email, paid ads, content — to reach customers where they spend time online. |
| "How would you grow Instagram from zero?" | Define niche → Daily Reels (30 days) → Trending audio → Engage 20-30 accounts/day → Collabs at 500 followers → Giveaway. |
| "What is ROAS?" | Revenue / Ad Spend. ROAS 4x = earned Rs 4 for every Rs 1 spent. Minimum viable: 3x for most businesses. |
| "Google Ads vs Meta Ads?" | Google = intent (they're searching). Meta = interest (they don't know they need it). Use both: Meta for awareness, Google for conversion. |
| "How to improve email open rates?" | Better subject lines + Segment list + Right send time + Clean inactive subscribers + A/B test everything. |
| "Explain a marketing funnel." | Awareness → Interest → Consideration → Decision → Purchase → Retention → Referral. Measure drop-off at each stage. |
| "How do you handle underperforming campaigns?" | Check data → Find bottleneck → Hypothesis → Change ONE variable → Measure 3-5 days → Iterate. |
| "What KPIs for a new e-commerce brand?" | Traffic, Conversion rate, AOV, CAC, ROAS, Cart abandonment rate, Repeat purchase rate. |
| "How would you allocate Rs 5L/month?" | Depends on stage. Growth: 35% paid ads, 25% content/SEO, 15% social, 10% email, 10% influencer, 5% tools. |
| "Where do you see yourself in 3 years?" | From execution to strategy. Managing a team or portfolio of clients. Proven ROI track record. Possibly specializing in [your strongest channel]. |

---

## Freelance Platform Comparison

| Feature | Fiverr | Upwork | LinkedIn Services |
|---------|--------|--------|-------------------|
| **Model** | Gig-based (buyer finds you) | Proposal-based (you apply to jobs) | Network-based |
| **Commission** | 20% | 10-20% (sliding) | 0% |
| **Best For** | Quick projects, side income | Long-term contracts, serious freelancing | High-value B2B clients |
| **Getting Started** | Easier (make gig, wait) | Harder (compete with proposals) | Requires strong profile |
| **Client Quality** | Mixed (many budget buyers) | Better (serious businesses) | Best (professional clients) |
| **Income Potential** | Rs 10K-50K/month (starting) | Rs 20K-1L/month (starting) | Rs 50K+ (established) |
| **Indian Freelancer Tip** | Price 20-30% below western competitors to start | Write proposals with Indian context, highlight timezone overlap | Build content presence first |

**Strategy for freshers:**
1. Start on Fiverr (easiest to get first reviews)
2. Move to Upwork after 5-10 reviews (better clients)
3. Build LinkedIn presence throughout (long-term)
4. After 6 months: Direct clients via cold outreach (no commission)

---

## Key Formulas

**Forecasting Revenue:**
```
Revenue = Traffic x Conversion Rate x Average Order Value
```

**Leads Needed:**
```
Leads = Revenue Target / (Close Rate x Average Deal Size)
```

**ROAS (Return on Ad Spend):**
```
ROAS = Revenue from Ads / Cost of Ads
Good: 3-5x | Great: 5-10x | Exceptional: 10x+
```

**CAC (Customer Acquisition Cost):**
```
CAC = Total Marketing Spend / Number of New Customers
```

**LTV:CAC Ratio:**
```
Healthy ratio = 3:1 or higher (earn 3x what you spend to acquire)
```

**Budget per Channel:**
```
Channel Budget = Total Budget x Channel Percentage
```

**Break-Even ROAS:**
```
Break-Even ROAS = 1 / Profit Margin
Example: 50% margin → need 2x ROAS to break even
```
