# Module 4: Paid Advertising (Performance Marketing Deep Dive)

## TechPath Academy | Digital Marketing with Gen AI

---

## Week 16: Ad Auction, Conversion Tracking & Landing Pages

### How Ad Auctions Work

Every time someone searches on Google or scrolls through Instagram, an ad auction happens in milliseconds. Understanding this auction is the foundation of paid advertising.

#### The Ad Rank Formula

```
Ad Rank = Maximum Bid × Quality Score × Expected Impact of Extensions
```

- **Maximum Bid** — The most you're willing to pay per click (CPC bid)
- **Quality Score** — Google's rating (1-10) of your ad relevance and landing page quality
- **Expected Impact of Extensions** — How much your ad extensions (sitelinks, callouts, etc.) improve performance

**Key Insight:** You don't always need the highest bid to win. A ₹50 bid with Quality Score 9 beats a ₹100 bid with Quality Score 4.

Example:
| Advertiser | Max Bid | Quality Score | Ad Rank | Position | Actual CPC |
|------------|---------|---------------|---------|----------|------------|
| TechPath | ₹50 | 9 | 450 | 1st | ₹34 |
| Competitor A | ₹80 | 5 | 400 | 2nd | ₹41 |
| Competitor B | ₹100 | 4 | 400 | 3rd | ₹51 |

**Actual CPC Formula:**
```
Actual CPC = (Ad Rank of advertiser below you / Your Quality Score) + ₹0.01
```

You only pay enough to beat the person below you — not your maximum bid.

---

### Quality Score (Google Ads)

Quality Score is rated 1-10 for each keyword. It's based on:

| Component | Weight | What Google Checks |
|-----------|--------|-------------------|
| Expected CTR | High | How likely people are to click your ad (based on history) |
| Ad Relevance | Medium | How closely your ad matches the search query |
| Landing Page Experience | High | Is the landing page relevant, fast, and mobile-friendly? |

**How to improve Quality Score:**
1. Use the target keyword in ad headline
2. Make ad copy specific to the keyword (not generic)
3. Send users to a highly relevant landing page (not homepage)
4. Ensure landing page loads fast (< 3 seconds)
5. Make landing page mobile-friendly
6. Include the keyword on the landing page

**Try This:** Open Google and search for any commercial keyword (e.g., "digital marketing course Bhopal" or "buy laptop online India"). Look at the top 3-4 ads that appear. For each ad, evaluate: (1) Does the headline match your search query closely? (2) What ad extensions do they use (sitelinks, callouts, phone number)? (3) Click on one ad — does the landing page match the ad's promise, or does it send you to a generic homepage? Rate each advertiser's likely Quality Score (1-10) based on what you observe.

---

### Key Advertising Metrics

| Metric | Formula | What It Means | Good Benchmark (India) |
|--------|---------|---------------|----------------------|
| CPC | Total Spend / Total Clicks | Cost per click | ₹5-50 (depends on industry) |
| CPM | (Total Spend / Impressions) × 1000 | Cost per 1000 views | ₹50-300 |
| CTR | (Clicks / Impressions) × 100 | Click-through rate | 2-5% (Search), 0.5-1.5% (Display) |
| CPA | Total Spend / Total Conversions | Cost per acquisition/conversion | ₹100-2000 (depends on industry) |
| ROAS | Revenue Generated / Ad Spend | Return on ad spend | 3x-5x minimum |
| Conversion Rate | (Conversions / Clicks) × 100 | % of clicks that convert | 2-5% (landing page), 1-3% (website) |
| CPL | Total Spend / Total Leads | Cost per lead | ₹50-500 |
| Frequency | Impressions / Reach | How often same person sees ad | Keep < 3 for awareness, < 7 for retargeting |

**Worked Examples:**

**Example 1:** Rahul spent ₹10,000 on Meta Ads. Got 500 clicks, 25 conversions, ₹75,000 in revenue.
- CPC = ₹10,000 / 500 = ₹20
- CTR = need impressions data
- CPA = ₹10,000 / 25 = ₹400
- Conversion Rate = (25/500) × 100 = 5%
- ROAS = ₹75,000 / ₹10,000 = 7.5x (excellent!)

**Example 2:** Priya spent ₹5,000 on Google Ads. Got 200,000 impressions, 3,000 clicks, 15 leads.
- CPM = (₹5,000 / 200,000) × 1000 = ₹25
- CTR = (3,000 / 200,000) × 100 = 1.5%
- CPC = ₹5,000 / 3,000 = ₹1.67
- CPL = ₹5,000 / 15 = ₹333

---

### Conversion Tracking

A conversion is any valuable action — purchase, form submission, phone call, app download.

#### Why Track Conversions?
- Know which ads/keywords/audiences drive real business results
- Optimize campaigns toward conversions (not just clicks)
- Calculate ROAS and CPA accurately
- Feed data to AI-powered bidding (Smart Bidding needs 30+ conversions/month)

#### Tracking Methods

| Method | Platform | What It Tracks |
|--------|----------|----------------|
| Meta Pixel | Facebook/Instagram | Page views, add to cart, purchases, leads |
| Google Ads Tag | Google Ads | Conversions from search, display, YouTube |
| Google Analytics 4 | All channels | Events, goals, e-commerce transactions |
| Google Tag Manager | All platforms | Central place to manage all tracking codes |
| UTM Parameters | Any link | Source, medium, campaign for each link |

#### Google Tag Manager (GTM) Setup

GTM is a free tool that manages all your tracking codes in one place (so you don't need a developer every time).

**How GTM works:**
1. Install ONE GTM code snippet on your website
2. Add all other tags (Meta Pixel, Google Ads, Analytics) through GTM interface
3. Use triggers (page view, button click, form submission) to fire tags
4. Use variables to capture dynamic data (page URL, click text, form values)

**GTM Concepts:**
- **Container** — One per website, holds all your tags
- **Tag** — A piece of tracking code (e.g., Meta Pixel, Google Ads conversion tag)
- **Trigger** — When to fire the tag (e.g., on page load, on button click, on form submit)
- **Variable** — Dynamic values (e.g., page URL, click text, transaction value)

**Common GTM Setup:**
```
Container: techpath.biz
├── Tags:
│   ├── GA4 Configuration (fires on all pages)
│   ├── Meta Pixel Base Code (fires on all pages)
│   ├── Meta Pixel Purchase Event (fires on thank-you page)
│   ├── Google Ads Conversion (fires on form submission)
│   └── LinkedIn Insight Tag (fires on all pages)
├── Triggers:
│   ├── All Pages (Page View)
│   ├── Thank You Page (Page View where URL contains /thank-you)
│   ├── Form Submission (Form Submit trigger)
│   └── CTA Button Click (Click trigger on .btn-cta class)
└── Variables:
    ├── Page URL
    ├── Click Text
    └── Form ID
```

#### UTM Parameters

Add UTM parameters to any link to track where traffic comes from:

```
https://techpath.biz/digital-marketing-course?utm_source=facebook&utm_medium=paid&utm_campaign=dm_launch_july&utm_content=carousel_ad_v2
```

| Parameter | What It Tracks | Example |
|-----------|---------------|---------|
| utm_source | Where the click came from | facebook, google, instagram, linkedin |
| utm_medium | Type of marketing | paid, organic, email, referral |
| utm_campaign | Campaign name | dm_launch_july, diwali_sale |
| utm_content | Which ad variation | carousel_v1, video_testimonial |
| utm_term | Keyword (for search) | digital+marketing+course+bhopal |

**Try This:** Solve these advertising math problems: (1) You spent Rs.15,000 on Meta Ads and got 750 clicks, 30 leads, and Rs.90,000 in revenue. Calculate CPC, CPL, Conversion Rate, and ROAS. (2) Build a UTM link for a hypothetical Instagram carousel ad promoting a Diwali sale for your brand — include all 5 UTM parameters. Use Google's Campaign URL Builder (ga-dev-tools.google/ga4/campaign-url-builder) to generate it.

---

### Landing Page Best Practices

A landing page is a standalone page designed for ONE goal (conversion). It's where your ad sends people.

**Key Elements:**

| Element | Best Practice | Why |
|---------|--------------|-----|
| Headline | Match your ad headline exactly | Maintains scent — user sees consistency |
| Hero Section | Clear value proposition above the fold | Users decide in 5 seconds |
| Social Proof | Testimonials, logos, numbers | Builds trust ("500+ students placed") |
| CTA Button | One clear action, contrasting color | Don't confuse with multiple options |
| Form | Minimum fields (name, phone, email) | Every extra field loses 10% conversions |
| Mobile Design | Thumb-friendly, fast loading | 70%+ traffic in India is mobile |
| Speed | Load under 3 seconds | 53% bounce if page takes > 3 seconds |
| Trust Signals | Photos, certifications, reviews | Reduces anxiety about taking action |

**Landing Page vs Website Page:**
| Feature | Landing Page | Website Page |
|---------|-------------|--------------|
| Navigation | None (remove header/footer) | Full navigation |
| Goal | ONE specific conversion | Multiple purposes |
| Content | Focused on one offer | Broad information |
| Links | Only CTA (no distractions) | Multiple links |
| Use Case | Ad campaigns | Organic/direct traffic |

**Try This:** Find 3 landing pages from Indian ed-tech or D2C brands (search Google Ads for "digital marketing course" or "online MBA" and click the ads). For each landing page, check: (1) Does the headline match the ad you clicked? (2) Is there a clear single CTA above the fold? (3) How many form fields do they ask for? (4) What social proof elements are present (testimonials, logos, numbers)? (5) Test the page load speed using PageSpeed Insights. Score each landing page out of 10 based on the best practices table above.

**Self-Check Questions:**
1. What is the Ad Rank formula, and why doesn't the highest bidder always win position 1?
2. What are the 3 components of Google's Quality Score, and which ones carry the most weight?
3. What is ROAS, and what is considered a "good" ROAS for most businesses?
4. Explain the difference between a landing page and a regular website page. Why should ad campaigns use dedicated landing pages?
5. What are UTM parameters? Name all 5 and explain when you would use `utm_content`.

---

## Week 17: Meta Ads (Facebook & Instagram Advertising)

### Meta Business Suite Structure

```
Meta Business Suite (business.facebook.com)
├── Business Manager
│   ├── Ad Account 1
│   │   ├── Campaign 1 (Objective: Traffic)
│   │   │   ├── Ad Set 1 (Audience: 25-35, Bhopal, Interest: Digital Marketing)
│   │   │   │   ├── Ad 1 (Image ad - testimonial)
│   │   │   │   └── Ad 2 (Carousel ad - curriculum)
│   │   │   └── Ad Set 2 (Audience: 18-24, MP, Interest: Career)
│   │   │       ├── Ad 3 (Video ad - campus tour)
│   │   │       └── Ad 4 (Image ad - placement stats)
│   │   └── Campaign 2 (Objective: Leads)
│   │       └── ...
│   ├── Pages (Facebook Page, Instagram Profile)
│   ├── Pixels (Meta Pixel)
│   └── People (Team members with roles)
```

### Campaign Objectives (Awareness → Consideration → Conversion)

| Stage | Objective | Best For | Billing |
|-------|-----------|----------|---------|
| Awareness | Brand Awareness | New brand, reach maximum people | CPM |
| Awareness | Reach | Show ad to maximum unique people | CPM |
| Consideration | Traffic | Drive website visits | CPC |
| Consideration | Engagement | Likes, comments, shares | CPE |
| Consideration | Video Views | Get video watched | CPV |
| Consideration | Lead Generation | Collect leads IN Facebook (no landing page) | CPL |
| Conversion | Conversions | Purchases, sign-ups on website | CPA |
| Conversion | Catalog Sales | E-commerce dynamic product ads | CPA |
| Conversion | App Installs | Mobile app downloads | CPI |

**For TechPath (educational institute):**
- Start with: Traffic + Lead Generation
- Scale to: Conversions (once pixel has 50+ conversion events)

**Try This:** Open Meta Ad Library (facebook.com/ads/library) and search for ads by 3 Indian brands (try boAt, Mamaearth, and Lenskart or any 3 brands you know). For each brand, note: (1) What ad format do they use most — image, video, or carousel? (2) What is their hook in the first line of ad text? (3) What campaign objective do you think they are optimizing for — awareness, traffic, or conversions? (4) How many active ads are they running right now? This gives you real-world insight into how brands allocate ad budgets.

---

### Meta Audience Targeting

#### 3 Types of Audiences

| Type | What | How to Create | Best For |
|------|------|---------------|----------|
| Core Audience | People based on demographics, interests, behaviors | Built in Ad Manager using targeting options | Reaching new people (prospecting) |
| Custom Audience | People who already interacted with you | Upload customer list, website visitors, app users, video viewers | Retargeting warm audiences |
| Lookalike Audience | People similar to your existing customers | Created from Custom Audience (Meta finds similar people) | Scaling — finding new customers like existing ones |

#### Core Audience Targeting Options

| Category | Options |
|----------|---------|
| Location | Country, State, City, Pin code, Radius around location |
| Age | 18-65+ (select range) |
| Gender | All, Male, Female |
| Language | Hindi, English, Regional languages |
| Interests | Digital Marketing, Entrepreneurship, Business, Technology, Education |
| Behaviors | Small business owners, Engaged shoppers, Mobile users |
| Connections | People who like your page, Friends of followers |
| Placement | Facebook Feed, Instagram Feed, Stories, Reels, Messenger |

**Targeting Example for TechPath Bhopal:**
- Location: Bhopal + 30km radius
- Age: 18-28
- Education: Graduation, Post-graduation
- Interests: Digital Marketing, Social Media Marketing, Career development, MBA
- Behavior: Engaged with education content, Used job portals recently
- Exclude: Current students (Custom Audience of enrolled students)

**Try This:** Design a targeting strategy for a hypothetical business (choose one: a new gym in your city, an online Spoken English course, or a local bakery). Define: (1) Core Audience — location, age range, gender, 3 interests, 1 behavior. (2) Custom Audience — what source would you use to create it (website visitors, video viewers, or customer list)? (3) Lookalike Audience — which Custom Audience would you base it on, and why? Write it out in the same format as the TechPath Bhopal example above.

---

### Meta Ad Formats

| Format | Specs | Best For |
|--------|-------|----------|
| Single Image | 1080×1080 px, ratio 1:1, text < 125 chars | Simple offers, testimonials |
| Carousel | 2-10 cards, 1080×1080 each | Showing multiple features/courses |
| Video | Up to 240 min, ratio 1:1 or 9:16 | Storytelling, testimonials, walkthroughs |
| Stories/Reels | 1080×1920 (9:16), 15-60 sec | Short, immersive, full-screen content |
| Collection | Hero image/video + product grid | E-commerce, course catalogs |
| Lead Form | In-app form (no landing page needed) | Quick lead generation |

---

### Ad Copy Frameworks

#### 1. AIDA (Attention → Interest → Desire → Action)
```
[ATTENTION] Struggling to get placed after graduation?
[INTEREST] TechPath's 6-month Digital Marketing course teaches you 15+ in-demand skills
[DESIRE] with live projects, Google & Meta certifications, and 500+ placement partners
[ACTION] Seats filling fast — Register for free demo class today!
```

#### 2. PAS (Problem → Agitate → Solution)
```
[PROBLEM] 73% of graduates in MP don't get a job in their field.
[AGITATE] Every month without a relevant skill is a month of lost salary.
[SOLUTION] TechPath's Digital Marketing course — from zero to job-ready in 6 months. 100% placement assistance. ₹45,000 (EMI available).
```

#### 3. Pain-Promise-Proof-Push
```
[PAIN] Tired of applying to 100 jobs and getting no response?
[PROMISE] What if you could land a ₹4-8 LPA digital marketing job in 6 months?
[PROOF] 500+ TechPath students already did. Companies like Infosys, TCS, and 50+ startups hire from us.
[PUSH] Free demo class this Saturday — only 20 spots. Register now →
```

**Try This:** Pick any product or service (your own project, a local business, or TechPath itself). Write 3 different ad copies using each of the 3 frameworks above — AIDA, PAS, and Pain-Promise-Proof-Push. Keep each ad copy under 125 words. Then ask 2-3 friends or classmates to read all 3 and vote on which one they would click. This teaches you that the market decides what works, not your personal preference.

---

### Live ₹1000 Meta Ad (Classroom Exercise)

Students will run a REAL ad with ₹1000 budget:

1. **Objective:** Traffic or Lead Generation
2. **Audience:** Hyper-local (your city + specific interest)
3. **Duration:** 3-5 days
4. **Creative:** One image ad + one video/carousel
5. **Track:** Impressions, reach, clicks, CTR, CPC, leads (if any)
6. **Optimize:** After Day 2, turn off the losing ad, scale the winner

---

### Retargeting Strategy

Retargeting = showing ads to people who already visited your site or interacted with your content.

**Retargeting Funnel:**
```
Level 1 (Hot): Visited pricing page but didn't buy → Show testimonial + limited offer
Level 2 (Warm): Visited blog/course page → Show course benefits + free demo invite
Level 3 (Cool): Watched 50%+ of video ad → Show carousel with curriculum highlights
Level 4 (Cold): Engaged with FB/IG post → Show brand awareness content
```

**Retargeting Audiences to Create:**
- Website visitors (last 30 days) — exclude converters
- Visited specific page (pricing, course page)
- Video viewers (25%, 50%, 75%, 95% watched)
- Lead form openers who didn't submit
- Instagram/Facebook page engagers (last 60 days)

**Try This:** Map out a retargeting funnel for any business of your choice. Draw the 4 levels (Hot → Warm → Cool → Cold) and for each level specify: (1) The audience definition (what action did they take?), (2) The ad message/angle you would show them, (3) The duration of the audience window (e.g., last 7 days, last 30 days). Think about it this way — someone who visited your pricing page yesterday needs a very different message than someone who just liked a Facebook post last month.

**Self-Check Questions:**
1. What are the 3 types of Meta audiences, and when would you use each one?
2. Explain the difference between a Campaign, Ad Set, and Ad in Meta's structure.
3. Which campaign objective should a new business start with, and when should they move to Conversions?
4. Write an ad copy using the PAS framework for a product/service of your choice.
5. What is retargeting, and why do retargeting audiences convert 3-5x better than cold audiences?

---

## Week 18: Google Ads

### Google Ads Account Structure

```
Google Ads Account
├── Campaign 1: Brand Search
│   ├── Ad Group: Brand Terms
│   │   ├── Keywords: "techpath academy", "techpath bhopal"
│   │   └── Ads: RSA with brand messaging
│   └── Ad Group: Brand + Service
│       ├── Keywords: "techpath digital marketing course"
│       └── Ads: RSA with course details
├── Campaign 2: Generic Search
│   ├── Ad Group: Digital Marketing Course
│   │   ├── Keywords: "digital marketing course bhopal", "learn digital marketing"
│   │   └── Ads: RSA with USPs
│   └── Ad Group: SEO Course
│       ├── Keywords: "SEO course", "learn SEO bhopal"
│       └── Ads: RSA with SEO-specific copy
├── Campaign 3: Display Remarketing
│   └── Ad Group: Website Visitors
│       ├── Audience: All visitors - converters
│       └── Ads: Display banners with offer
└── Campaign 4: YouTube
    └── Ad Group: Brand Video
        ├── Audience: In-market for education
        └── Ads: 30-sec skippable video
```

---

### Google Ads Keyword Match Types

| Match Type | Symbol | Example Keyword | Ads Show For | Won't Show For |
|------------|--------|----------------|-------------|----------------|
| Broad Match | none | digital marketing course | "online marketing class," "learn digital marketing free," "marketing training" | Anything totally unrelated |
| Phrase Match | " " | "digital marketing course" | "best digital marketing course," "digital marketing course in bhopal," "affordable digital marketing course online" | "course on digital" (wrong order/meaning) |
| Exact Match | [ ] | [digital marketing course] | "digital marketing course," "digital marketing courses" (close variants only) | "best digital marketing course" |
| Negative | - | -free | | "free digital marketing course" (excluded) |

**Strategy:** Start with Phrase Match (balance of reach and relevance). Add Exact Match for top-performing keywords. Use Broad Match only with Smart Bidding and good conversion data. Always add Negative Keywords.

**Negative Keyword Examples for TechPath:**
- free, torrent, download, pdf
- jobs, salary, vacancy, hiring (unless running job-related campaigns)
- review, complaint, scam
- other city names (if targeting only Bhopal)

**Try This:** For a business of your choice, create a complete keyword match type plan. Pick one product/service keyword and write it out in all 3 match types (Broad, Phrase, Exact). Then brainstorm 10 negative keywords that you would add to avoid wasted spend. For example, if your business is a premium coaching institute, what searches would you want to EXCLUDE? Think about intent mismatches, competitor terms, job seekers, and freebie seekers.

---

### Responsive Search Ads (RSA)

RSA is the default Google Search ad format. You provide multiple headlines and descriptions — Google's AI tests combinations.

**Requirements:**
- Up to 15 Headlines (30 characters each)
- Up to 4 Descriptions (90 characters each)
- Google tests different combinations and shows the best performing

**Best Practices:**
1. Use all 15 headline slots (minimum 8-10)
2. Include keyword in at least 3 headlines
3. Include your USP/differentiator in 2-3 headlines
4. Include a CTA in 2-3 headlines ("Enroll Now," "Book Free Demo")
5. Include numbers/proof ("500+ Placed," "4.8/5 Rating")
6. Make each headline make sense on its own (they appear in any combination)
7. Pin important headlines to Position 1 or 2 (use sparingly)

**Example RSA for TechPath:**
```
Headlines:
H1: Digital Marketing Course Bhopal [keyword]
H2: 6-Month Career Program [duration]
H3: 500+ Students Placed [proof]
H4: ₹45,000 (EMI Available) [price]
H5: Google & Meta Certified [credibility]
H6: Learn SEO, Ads, Social Media [curriculum]
H7: Live Projects + Internship [USP]
H8: Free Demo Class Saturday [CTA]
H9: TechPath Academy Bhopal [brand]
H10: 100% Placement Assistance [promise]

Descriptions:
D1: Join TechPath's Digital Marketing course. Learn from industry experts with real projects. Placement in top companies guaranteed. (89 chars)
D2: Master SEO, Google Ads, Meta Ads, AI tools in 6 months. Weekend and weekday batches available. Enroll today! (87 chars)
```

**Try This:** Write a complete RSA for a business of your choice. Create at least 10 headlines (30 chars each) and 3 descriptions (90 chars each). Ensure you include: at least 2 headlines with the keyword, 2 with social proof/numbers, 2 with a CTA, and 2 with your USP. Count the characters for each headline and description to make sure none exceed the limit. Bonus: Ask ChatGPT or Claude to generate 5 more headline variations and evaluate which ones you would actually use.

---

### Google Ads Bidding Strategies

| Strategy | Type | Best For | Requirement |
|----------|------|----------|-------------|
| Manual CPC | Manual | Full control, learning phase | Good understanding of keyword values |
| Enhanced CPC | Semi-auto | Adjusts bid for likely converters | Some conversion data |
| Maximize Clicks | Automated | Getting maximum traffic within budget | New campaigns, limited data |
| Maximize Conversions | Smart Bidding | Getting most conversions possible | 30+ conversions/month |
| Target CPA | Smart Bidding | Getting conversions at specific cost | 30+ conversions/month + know target CPA |
| Target ROAS | Smart Bidding | Getting specific return on spend | 50+ conversions/month + know target ROAS |
| Maximize Conversion Value | Smart Bidding | Maximizing revenue | Revenue tracking + 50+ conversions/month |

**Decision Tree:**
- Just starting out? → Maximize Clicks (gather data)
- Have 30+ conversions/month? → Maximize Conversions or Target CPA
- Have revenue tracking? → Target ROAS or Maximize Conversion Value
- Very competitive keywords? → Manual CPC (to control spend)

---

### Display Ads & Performance Max

**Display Ads:**
- Visual banner ads shown across 2 million+ websites and apps
- Best for remarketing (showing ads to past visitors) and brand awareness
- Lower intent than search, but much cheaper (CPM ₹20-100)
- Sizes: 300×250, 728×90, 160×600, 320×50 (mobile)

**Performance Max (PMax):**
- Google's AI-driven campaign type that runs across ALL Google properties
- Channels: Search, Display, YouTube, Gmail, Maps, Discover
- You provide: goals, budget, creative assets (images, videos, headlines, descriptions)
- Google's AI handles: bidding, targeting, placement, creative combinations
- Best for: e-commerce, lead gen with sufficient conversion data (50+/month)

**Try This:** You are launching Google Ads for a new business with zero conversion data and a budget of Rs.500/day. Using the Decision Tree above, answer: (1) Which bidding strategy would you start with, and why? (2) After 2 months, you now have 45 conversions/month with an average CPA of Rs.350. Your target CPA is Rs.300. Which bidding strategy would you switch to? (3) After 4 months, you have revenue tracking set up and 60+ conversions/month. What should your bidding strategy be now? Write out your reasoning for each transition.

**Self-Check Questions:**
1. What are the 3 keyword match types in Google Ads? Give an example of what each would match for the keyword "digital marketing course."
2. How many headlines and descriptions can you provide in a Responsive Search Ad, and what are the character limits for each?
3. When should you use Target CPA vs Target ROAS bidding? What data do you need for each?
4. What is the difference between Display Ads and Performance Max campaigns?
5. What are negative keywords, and why are they essential for controlling ad spend?

---

## Week 19: YouTube, LinkedIn & Other Platforms

### YouTube Ad Types

| Ad Type | Length | Skippable? | Billing | Best For |
|---------|--------|-----------|---------|----------|
| TrueView In-Stream (Skippable) | 12s - 3min recommended | Yes, after 5 seconds | CPV (pay when watched 30s or full) | Brand storytelling, tutorials |
| Non-Skippable In-Stream | 15-20 seconds | No | CPM | Short, punchy brand messages |
| Bumper Ads | 6 seconds max | No | CPM | Brand recall, simple messages |
| In-Feed (Discovery) | Any length | N/A (user chooses to watch) | CPC (pay when clicked) | Tutorial content, longer videos |
| YouTube Shorts | Up to 60 seconds | Yes | CPV/CPM | Mobile-first, Gen Z audience |

**YouTube Ad Script Structure (30 seconds):**
```
0-5 sec: HOOK (grab attention — question, bold statement, visual shock)
5-15 sec: PROBLEM + SOLUTION (relate to viewer's pain, introduce your offer)
15-25 sec: PROOF (testimonials, numbers, results)
25-30 sec: CTA (clear next step — visit URL, call, register)
```

**Try This:** Go to YouTube and watch 5 ads intentionally (don't skip them). For each ad, note: (1) What type is it — skippable in-stream, non-skippable, or bumper? (2) What was the hook in the first 5 seconds — did it make you want to keep watching? (3) Did it follow the HOOK → PROBLEM → PROOF → CTA structure? (4) Write a 30-second ad script for TechPath (or your own project) following the structure above. Keep the hook under 5 seconds — this is the hardest part because that's where most viewers decide to skip.

---

### LinkedIn Ads (B2B)

LinkedIn is the best platform for B2B (business-to-business) advertising.

**Targeting Options (unique to LinkedIn):**
- Job title (CEO, Marketing Manager, HR Head)
- Company name (target employees of specific companies)
- Company size (1-10, 11-50, 51-200, 201-500, 500+)
- Industry (IT, Healthcare, Education, Finance)
- Seniority (Entry, Manager, Director, VP, C-Suite)
- Skills (Digital Marketing, SEO, Data Analytics)
- Groups (members of specific LinkedIn groups)

**LinkedIn Ad Formats:**
| Format | Best For | Avg CPC (India) |
|--------|----------|-----------------|
| Single Image | Brand awareness, lead gen | ₹80-200 |
| Carousel | Multiple features/case studies | ₹80-200 |
| Video | Thought leadership, events | ₹50-150 (CPV) |
| Text Ads | Budget-friendly awareness | ₹30-80 |
| Message Ads (InMail) | Direct outreach, event invites | ₹30-50 per send |
| Document Ads | Whitepapers, reports | ₹80-150 |
| Lead Gen Forms | Collect leads without leaving LinkedIn | ₹100-300 per lead |

**When to use LinkedIn vs Meta:**
- LinkedIn: Selling to businesses (B2B), recruiting, high-ticket services (₹50,000+)
- Meta: Selling to consumers (B2C), local businesses, courses, e-commerce

---

### Other Advertising Platforms

| Platform | Best For | Indian Audience |
|----------|----------|-----------------|
| Microsoft Ads (Bing) | B2B, professionals, desktop users | Smaller but high-intent audience |
| Pinterest Ads | Fashion, home decor, recipes, weddings | Growing Indian female audience (25-44) |
| Quora Ads | Education, SaaS, professional services | High-intent question-askers |
| Twitter/X Ads | News, tech, politics, thought leadership | Urban, educated audience |
| Programmatic (DV360) | Large-scale display across premium sites | Enterprise advertisers (₹5L+ budgets) |

**Try This:** You are the marketing manager for a B2B SaaS company selling HR software to mid-size companies (50-500 employees) in India. Design a LinkedIn ad campaign: (1) Choose your targeting — job titles, company size, industry, seniority. (2) Pick an ad format and justify your choice. (3) Write the ad copy (headline + description). (4) Calculate: if LinkedIn's average CPL in India is Rs.200, how much budget do you need to generate 50 leads? Now compare — would the same campaign work on Meta? Why or why not?

**Self-Check Questions:**
1. What are the 5 YouTube ad types, and which one should you use for a 6-second brand recall message?
2. Name 3 targeting options unique to LinkedIn that you cannot do on Meta.
3. When should you choose LinkedIn Ads over Meta Ads? Give a specific business scenario for each.
4. What is the recommended YouTube ad script structure for a 30-second ad? Why are the first 5 seconds critical?
5. What is Programmatic advertising (DV360), and what budget level is it suited for?

---

## Week 20: AI for Ads & Capstone Campaign

### AI Tools for Ad Creative

| Tool | What It Does | Pricing |
|------|-------------|---------|
| AdCreative.ai | Generates ad creatives (images + copy) using AI | From $29/month |
| Pencil AI | Creates video ad variations automatically | From $49/month |
| Pebblely | AI product photography (removes/changes backgrounds) | Free tier available |
| Midjourney | AI image generation for ad visuals | From $10/month |
| Canva AI (Magic Design) | Auto-generates designs from text prompts | Free + Pro ₹500/month |
| ChatGPT / Claude | Ad copy generation, A/B testing variations | Free + paid tiers |
| Predis.ai | AI social media ad creation + scheduling | From $29/month |

### AI for Ad Copy Generation

Use AI to generate multiple ad copy variations quickly:

**Prompt template for ad copy:**
```
Write 5 Facebook ad primary texts for [product/service].
Target audience: [age, location, interests]
Key benefit: [main value proposition]
Tone: [friendly/professional/urgent]
Include: [social proof, price, offer, CTA]
Character limit: 125 characters for headline, 90 for description
```

### Smart Bidding & AI Optimization

Google's Smart Bidding uses machine learning to optimize bids in real-time:

**What AI considers for each auction:**
- Device (mobile/desktop/tablet)
- Location (user's city, neighborhood)
- Time of day and day of week
- Search query (exact words used)
- Browser and OS
- Remarketing list membership
- Demographics (age, gender)
- Ad creative being shown

**Tip:** Smart Bidding works best with:
- 30+ conversions per month (minimum)
- Consistent conversion tracking
- 2+ weeks of learning period (don't change settings)
- Sufficient budget (not too constrained)

**Try This:** Use ChatGPT or Claude to generate ad creatives for a campaign. Write a prompt using the template above for a product/service of your choice. Generate: (1) 5 Facebook ad primary texts using the PAS framework. (2) 10 Google RSA headlines (30 chars each). (3) 3 YouTube ad hooks (the first 5-second line only). Evaluate the AI output — which ones would you actually use? Edit the best 2-3 to make them sound more human and specific to your brand. This teaches you that AI is a starting point, not a final draft.

---

### Capstone: Multi-Platform ₹2000 Campaign

Students will plan and execute a real ₹2000 campaign across platforms:

**Budget Split (suggested):**
- Meta Ads (Facebook/Instagram): ₹1200
- Google Ads (Search): ₹800

**Requirements:**
1. Set up proper conversion tracking (GTM + Meta Pixel + Google Ads tag)
2. Create campaign structure for both platforms
3. Design 3+ ad creatives per platform
4. Run for 5-7 days
5. Daily monitoring and optimization
6. Final report with ROAS, CPA, best-performing creative, learnings

**Self-Check Questions:**
1. Name 3 AI tools for ad creative generation and what each one does.
2. What data signals does Google's Smart Bidding consider for each auction? Name at least 5.
3. What is the minimum number of conversions per month needed for Smart Bidding to work effectively?
4. If you had Rs.2000 to split between Meta Ads and Google Ads for a local coaching institute, how would you split it and why?
5. Why should you wait at least 2 weeks before changing Smart Bidding settings? What is the "learning period"?

---

## Key Formulas Summary

| Metric | Formula |
|--------|---------|
| CPC | Total Ad Spend / Total Clicks |
| CPM | (Total Ad Spend / Total Impressions) × 1000 |
| CTR | (Total Clicks / Total Impressions) × 100 |
| CPA | Total Ad Spend / Total Conversions |
| ROAS | Total Revenue / Total Ad Spend |
| Conversion Rate | (Total Conversions / Total Clicks) × 100 |
| CPL | Total Ad Spend / Total Leads |
| Ad Rank | Max Bid × Quality Score |
| Actual CPC | (Ad Rank below you / Your Quality Score) + ₹0.01 |

---

## Key Takeaways

- Quality Score matters more than budget — improve relevance to pay less per click
- Always set up conversion tracking BEFORE running ads (you can't optimize what you can't measure)
- Start small (₹500-1000/day), test creatives, then scale winners
- Retargeting audiences convert 3-5x better than cold audiences
- AI bidding (Smart Bidding) outperforms manual bidding when you have enough data (30+ conversions/month)
- Meta = best for B2C, visual products, local businesses
- Google Search = best for high-intent queries (people actively searching)
- LinkedIn = best for B2B, expensive services, recruiting
- Landing pages dedicated to each campaign outperform sending traffic to homepage
- Test everything: audiences, creatives, copy, landing pages — the market decides what works
