# Module 4: Paid Advertising Cheat Sheet

## TechPath Academy | Digital Marketing with Gen AI

---

## Ad Metrics Formulas

| Metric | Formula | Example |
|--------|---------|---------|
| CPC | Spend / Clicks | ₹10,000 / 500 = ₹20 |
| CPM | (Spend / Impressions) x 1000 | (₹10,000 / 200,000) x 1000 = ₹50 |
| CTR | (Clicks / Impressions) x 100 | (500 / 20,000) x 100 = 2.5% |
| CPA | Spend / Conversions | ₹10,000 / 25 = ₹400 |
| ROAS | Revenue / Spend | ₹75,000 / ₹10,000 = 7.5x |
| Conv. Rate | (Conversions / Clicks) x 100 | (25 / 500) x 100 = 5% |
| CPL | Spend / Leads | ₹10,000 / 40 = ₹250 |
| Ad Rank | Max Bid x Quality Score | ₹50 x 9 = 450 |
| Actual CPC | (Rank below / Your QS) + ₹0.01 | (400 / 9) + 0.01 = ₹44.45 |

---

## Meta Campaign Structure

```
Campaign (1 objective, 1 budget strategy)
├── Ad Set 1 (Audience + Placement + Schedule + Budget)
│   ├── Ad 1 (Creative + Copy + CTA)
│   └── Ad 2 (Creative + Copy + CTA)
├── Ad Set 2 (Different audience)
│   ├── Ad 3
│   └── Ad 4
└── Ad Set 3 (Retargeting audience)
    ├── Ad 5
    └── Ad 6
```

**Structure Rule:** 1 Campaign = 1 Objective. Multiple audiences = Multiple Ad Sets. Multiple creatives = Multiple Ads within each Ad Set.

---

## Google Ads Match Types

| Match Type | Symbol | Keyword | Shows For | Does NOT Show For |
|------------|--------|---------|-----------|-------------------|
| Broad | none | digital marketing course | online marketing training, learn marketing, digital classes | completely unrelated |
| Phrase | "..." | "digital marketing course" | best digital marketing course, digital marketing course online | marketing digital course |
| Exact | [...] | [digital marketing course] | digital marketing course, digital marketing courses | best digital marketing course |
| Negative | - | -free | (blocks) | free digital marketing course |

**Quick Rule:** Start with Phrase Match. Add Exact for winners. Use Broad only with Smart Bidding. Always add negatives.

---

## Quality Score Factors (Google Ads)

| Factor | Weight | How to Improve |
|--------|--------|----------------|
| Expected CTR | High | Write compelling ads with keyword in headline |
| Ad Relevance | Medium | Match ad copy closely to keyword |
| Landing Page Experience | High | Fast, mobile, relevant page with keyword content |

**Quality Score Range:** 1-10. Target 7+ for all keywords. Below 5 = pause or fix immediately.

---

## Bidding Strategy Decision Tree

```
Starting out / No conversion data?
→ Use: Maximize Clicks

Have 15-30 conversions/month?
→ Use: Maximize Conversions

Have 30+ conversions/month + know target cost?
→ Use: Target CPA

Have 50+ conversions/month + revenue tracking?
→ Use: Target ROAS

Need full control (competitive keywords)?
→ Use: Manual CPC
```

---

## Ad Copy Character Limits

### Meta Ads
| Element | Character Limit | Best Practice |
|---------|----------------|---------------|
| Primary Text | 125 (visible without "See More") | Front-load key message |
| Headline | 40 characters | Clear value proposition |
| Description | 30 characters | Supporting detail |
| Link Description | 30 characters | Brief context |

### Google Ads (RSA)
| Element | Character Limit | Quantity |
|---------|----------------|----------|
| Headline | 30 characters each | Up to 15 (min 3) |
| Description | 90 characters each | Up to 4 (min 2) |
| Display URL Path | 15 characters each | 2 paths |

### YouTube Ads
| Element | Character Limit |
|---------|----------------|
| Companion Banner Headline | 25 characters |
| Video Title (In-Feed) | 100 characters |
| Video Description | 2 lines visible |

### LinkedIn Ads
| Element | Character Limit |
|---------|----------------|
| Headline | 70 characters |
| Introductory Text | 150 characters (before "See More") |
| Description | 100 characters |

---

## Indian Market Benchmarks (2026)

### Google Ads
| Industry | Avg CPC | Avg CTR | Avg Conv Rate |
|----------|---------|---------|---------------|
| Education | ₹15-40 | 3.5-5% | 3-6% |
| E-commerce | ₹8-25 | 2-4% | 1.5-3% |
| Real Estate | ₹30-80 | 2-3.5% | 1-2.5% |
| Healthcare | ₹20-60 | 3-5% | 2-4% |
| Local Services | ₹10-35 | 4-6% | 5-10% |

### Meta Ads
| Industry | Avg CPC | Avg CTR | Avg CPL |
|----------|---------|---------|---------|
| Education | ₹8-20 | 1.5-3% | ₹100-300 |
| E-commerce | ₹5-15 | 1-2.5% | ₹80-200 |
| Fashion | ₹3-10 | 1.5-3% | ₹50-150 |
| B2B | ₹20-50 | 0.5-1.5% | ₹300-800 |

---

## Meta Audience Types

| Type | What | When to Use |
|------|------|-------------|
| Core (Interest) | Demographics + Interests + Behaviors | Cold audience, prospecting |
| Custom | Your own data (website visitors, email list, video viewers) | Retargeting warm audience |
| Lookalike | People similar to your Custom Audience | Scaling, finding new customers |

**Retargeting Priority:**
1. Website visitors (last 7 days) — hottest
2. Add-to-cart abandoners — very hot
3. Video viewers (75%+) — warm
4. Page engagers (last 30 days) — warm
5. Lookalike of converters — cool but qualified

---

## Ad Copy Frameworks

### AIDA
```
[Attention] Bold hook / question / statistic
[Interest] Describe the benefit / what's in it for them
[Desire] Social proof / FOMO / emotional pull
[Action] Clear CTA with urgency
```

### PAS
```
[Problem] Name their pain point directly
[Agitate] Make them feel the cost of not solving it
[Solution] Present your product as the answer + CTA
```

### Pain-Promise-Proof-Push
```
[Pain] "Tired of...?" / "Struggling with...?"
[Promise] "What if you could...?" / "Imagine..."
[Proof] "500+ students already..." / "4.8/5 rating"
[Push] "Limited seats" / "Offer ends Friday" / "Register now"
```

---

## UTM Parameters Quick Reference

```
?utm_source=   (where: facebook, google, instagram, email)
&utm_medium=   (how: paid, organic, cpc, social, referral)
&utm_campaign= (what: diwali_sale, dm_launch_july)
&utm_content=  (which ad: video_v1, carousel_v2)
&utm_term=     (keyword: digital+marketing+course)
```

**Example:**
```
techpath.biz/course?utm_source=facebook&utm_medium=paid&utm_campaign=jan_batch&utm_content=testimonial_video
```

---

## Quick Campaign Checklist

### Before Launching:
- [ ] Conversion tracking set up and tested (GTM Preview Mode)
- [ ] Meta Pixel / Google Ads tag firing correctly
- [ ] Landing page live, fast (< 3s), mobile-friendly
- [ ] UTM parameters added to all ad URLs
- [ ] Budget set (daily, not lifetime for testing phase)
- [ ] Ad creatives reviewed (no text > 20% of image for Meta)
- [ ] Negative keywords added (Google Ads)
- [ ] Audience exclusions set (exclude existing customers)
- [ ] A/B test plan ready (at least 2 creatives per ad set)

### Daily Monitoring:
- [ ] Check spend vs budget (no overspend)
- [ ] Check CTR (below 1% = ad fatigue or wrong audience)
- [ ] Check CPC (rising CPC = increase relevance or change creative)
- [ ] Check frequency (> 3 = audience fatigue, expand or refresh)
- [ ] Check conversion rate (dropping = landing page issue)

### Weekly Optimization:
- [ ] Pause underperforming ads (lowest CTR, highest CPA)
- [ ] Scale winning ads (increase budget by 20% max per change)
- [ ] Add negative keywords (check search terms report — Google)
- [ ] Refresh creatives if frequency > 4
- [ ] Test new audiences if current ones saturating
- [ ] Update bids based on performance data

---

## Google Ads Campaign Types Comparison

| Type | Where Ads Show | Best For | Budget Level |
|------|---------------|----------|--------------|
| Search | Google Search results | High-intent leads | Any (₹500/day+) |
| Display | Websites, apps, Gmail | Remarketing, awareness | Medium (₹300/day+) |
| Shopping | Google Shopping tab, search | E-commerce products | Medium-High |
| Video | YouTube | Brand awareness, consideration | Medium (₹500/day+) |
| Performance Max | ALL Google channels | Conversions at scale | High (₹1000/day+) |
| Demand Gen | YouTube, Discover, Gmail | Visual discovery campaigns | Medium |

---

## YouTube Ad Types Quick Comparison

| Type | Length | Skip? | Pay When | Best For |
|------|--------|-------|----------|----------|
| Skippable In-Stream | Any (rec 30s) | After 5s | 30s watched or full | Storytelling |
| Non-Skippable | 15-20s | No | Impression (CPM) | Short brand messages |
| Bumper | 6s max | No | Impression (CPM) | Brand recall |
| In-Feed | Any | User clicks | Click (CPC) | Tutorial content |
| Shorts | Up to 60s | Yes | View/CPM | Mobile-first, Gen Z |

---

## ROAS Decision Making

| ROAS | Verdict | Action |
|------|---------|--------|
| > 5x | Excellent | Scale budget aggressively (increase 20-50%) |
| 3x - 5x | Good | Scale gradually (increase 10-20%) |
| 2x - 3x | Break-even | Optimize (new creatives, better audiences) |
| 1x - 2x | Losing money | Major changes needed or pause |
| < 1x | Significant loss | Pause immediately, investigate |

**Note:** Target ROAS depends on margins. Low-margin products (e-commerce) need 4-5x. High-margin services (courses) can work at 2-3x.
