# Ad Platforms & Auction Mechanics

**Module 04 — Paid Advertising | Topic 1**

---

## The World of Paid Advertising

Paid advertising (also called **Performance Marketing** or **PPC — Pay Per Click**) means paying platforms to show your ads to targeted audiences. Unlike SEO which takes months, paid ads can bring traffic within hours.

> **Simple Analogy:** SEO is like planting a mango tree — it takes years but gives fruit forever. Paid ads are like renting a stall at a mela — you pay money, you get customers immediately, but the moment you stop paying, the stall is gone.

---

## Overview of Major Ad Platforms

| Platform | Best For | Audience | Avg CPC (India) | Ad Format |
|----------|---------|----------|-----------------|-----------|
| **Google Ads** | Capturing people actively searching for your product/service | Intent-based (they are looking for you) | ₹15-80 (Search) | Text ads, Shopping, Display banners, YouTube video |
| **Meta Ads (Facebook + Instagram)** | Building awareness, retargeting, lead generation | Interest/behavior-based (you find them) | ₹5-25 | Image, Video, Carousel, Stories, Reels |
| **YouTube Ads** | Brand storytelling, product demos, reach | Video-first audiences | ₹1-5 (per view) | Skippable, Non-skippable, Bumper, Discovery |
| **LinkedIn Ads** | B2B marketing, job recruitment, professional services | Professional/career-based | ₹150-500+ | Sponsored Content, Message Ads, Text Ads |
| **Twitter/X Ads** | Real-time conversations, trending topics, thought leadership | News/conversation-based | ₹10-40 | Promoted Tweets, Trends, Follower Ads |
| **Pinterest Ads** | Visual products (fashion, home decor, food, weddings) | Visual discovery-based | ₹8-30 | Promoted Pins, Shopping Pins |
| **Quora Ads** | Reaching people asking specific questions | Question/answer-based | ₹10-35 | Text ads in Q&A feed |

### Which Platform to Choose?

| Your Goal | Best Platform | Why |
|-----------|--------------|-----|
| Capture people searching for your service | **Google Search Ads** | They are already looking for what you offer |
| Build brand awareness cheaply | **Meta Ads (Instagram/Facebook)** | Massive reach at low CPM in India |
| Target working professionals or B2B | **LinkedIn Ads** | Only platform with job title and company targeting |
| Show product demos or tutorials | **YouTube Ads** | Video format, massive Indian viewership |
| Sell visual products (clothing, decor) | **Pinterest + Instagram** | Visual discovery platforms |
| Retarget website visitors | **Meta Ads + Google Display** | Both have excellent retargeting capabilities |

---

## How Ad Auctions Work

Every time someone searches on Google or scrolls through Instagram, an **ad auction** happens in milliseconds. This auction determines which ads appear and in what order.

### The Ad Rank Formula (Google Ads)

```
Ad Rank = Maximum Bid x Quality Score x Expected Impact of Ad Extensions
```

- **Maximum Bid** — The most you are willing to pay per click
- **Quality Score** — Google's rating (1-10) of how good your ad and landing page are
- **Expected Impact of Extensions** — How much your ad extensions (sitelinks, callouts) improve the ad

> **Key Insight:** You do NOT need the highest bid to win the auction. A smaller budget with a high Quality Score can beat a big spender with a low Quality Score.

### Auction Example

Four advertisers are bidding on the keyword "digital marketing course Bhopal":

| Advertiser | Max Bid (₹) | Quality Score | Ad Rank (Bid x QS) | Position | Actual CPC (₹) |
|------------|-------------|---------------|--------------------|---------|--------------------|
| TechPath Academy | 50 | 9 | 450 | 1st | 34 |
| Competitor A | 80 | 5 | 400 | 2nd | 41 |
| Competitor B | 100 | 3 | 300 | 3rd | 67 |
| Competitor C | 40 | 6 | 240 | 4th | Below threshold |

**Notice:** TechPath bid the lowest (₹50) but won position 1 because of the highest Quality Score (9). Competitor B bid the highest (₹100) but only got position 3.

### Actual CPC Formula

You never pay your maximum bid. You only pay enough to beat the advertiser below you:

```
Actual CPC = (Ad Rank of advertiser below you / Your Quality Score) + ₹0.01
```

For TechPath: Actual CPC = (400 / 9) + 0.01 = ₹44.45 + ₹0.01 = approximately ₹44.46

> **Pro Tip:** This is why Quality Score is the most important thing in Google Ads. A high Quality Score means you pay less per click AND get better positions. Always optimise for Quality Score before increasing your bid.

---

## Quality Score — Deep Dive

Quality Score (QS) is Google's rating from 1 to 10 for each keyword in your account. It is based on three components:

| Component | Weight | What Google Checks | How to Improve |
|-----------|--------|-------------------|----------------|
| **Expected CTR** | High | How likely people are to click your ad based on historical performance | Write compelling ad copy with keyword in headline, use numbers and CTAs |
| **Ad Relevance** | Medium | How closely your ad text matches the search query | Include the exact keyword in your headline, create tight ad groups with related keywords |
| **Landing Page Experience** | High | Is the landing page relevant, fast, mobile-friendly, and useful? | Send users to a specific page (not homepage), match the ad promise, load under 3 seconds |

| Quality Score | Meaning | Your Action |
|---------------|---------|-------------|
| 7-10 | Excellent | Maintain, scale budget |
| 5-6 | Average | Optimise ad copy and landing page |
| 1-4 | Poor | Pause keyword, fix landing page, rewrite ad, or remove the keyword |

---

## Campaign Structure

All major ad platforms follow a similar hierarchy:

```
Account
└── Campaign (budget, objective, targeting scope)
    └── Ad Group / Ad Set (specific audience, keywords, or theme)
        └── Ads (the actual creative people see)
```

### Google Ads Structure

```
Campaign: "DM Course Bhopal"
├── Ad Group: "Digital Marketing Course"
│   ├── Keywords: digital marketing course bhopal, DM course bhopal, learn digital marketing bhopal
│   ├── Ad 1: RSA with 15 headlines
│   └── Ad 2: RSA with different messaging
├── Ad Group: "SEO Training"
│   ├── Keywords: SEO training bhopal, learn SEO bhopal
│   └── Ad 1: RSA focused on SEO
└── Ad Group: "Google Ads Course"
    ├── Keywords: google ads course bhopal, PPC training bhopal
    └── Ad 1: RSA focused on Google Ads
```

### Meta Ads Structure

```
Campaign: "Lead Gen — DM Course" (objective: leads)
├── Ad Set 1: "25-35 Age, Bhopal" (audience + budget)
│   ├── Ad 1: Carousel ad showing course modules
│   └── Ad 2: Video testimonial from placed student
├── Ad Set 2: "18-24 Age, MP State" (different audience)
│   ├── Ad 1: Single image ad with offer
│   └── Ad 2: Reel-style video ad
└── Ad Set 3: "Website Retargeting" (custom audience)
    └── Ad 1: "Still thinking? Here's what students say..."
```

---

## Campaign Objectives by Platform

| Platform | Awareness | Consideration | Conversion |
|----------|-----------|--------------|------------|
| **Google Ads** | Display campaigns, YouTube reach | Search ads, Discovery | Search ads, Shopping, Performance Max |
| **Meta Ads** | Brand Awareness, Reach | Traffic, Engagement, Video Views | Leads, Sales, App Installs |
| **LinkedIn Ads** | Brand Awareness | Website Visits, Engagement, Video Views | Lead Gen, Conversions |
| **YouTube** | Bumper ads, Masthead | TrueView In-Stream, Discovery | TrueView for Action |

> **Rule of Thumb:** Choose your objective based on where your customer is in the funnel. New brand? Start with Awareness. Have website traffic but no leads? Run Conversion campaigns with retargeting.

---

## Setting Up Google Tag Manager (GTM)

**Google Tag Manager** is a free tool that lets you add tracking codes (tags) to your website without editing the code directly.

### Why Use GTM?

| Without GTM | With GTM |
|-------------|----------|
| Add tracking code to every page manually | Add one GTM code, manage everything from dashboard |
| Need a developer for every change | Marketers can add/remove tags without developers |
| Hard to manage multiple tracking codes | Organised tags, triggers, and variables in one place |
| Risk breaking your website | Preview mode lets you test before publishing |

### Setup Steps

1. Go to tagmanager.google.com and create an account
2. Create a Container (one per website)
3. Add the GTM code snippet to your website's `<head>` and `<body>`
4. In GTM, add tags for: Google Analytics 4, Meta Pixel, Google Ads Conversion Tracking
5. Use Preview mode to test that tags fire correctly
6. Publish the container

---

## Installing Meta Pixel

The **Meta Pixel** is a piece of code you add to your website that tracks visitor actions. It powers Meta Ads retargeting and conversion tracking.

### What Meta Pixel Tracks

| Event | What It Tracks |
|-------|---------------|
| **PageView** | Every page visit (automatic) |
| **Lead** | Form submissions |
| **Purchase** | Completed purchases |
| **AddToCart** | Items added to cart |
| **ViewContent** | Product/course page views |
| **CompleteRegistration** | Sign-up completions |
| **InitiateCheckout** | Checkout page views |

### Installation Steps

1. Go to Meta Business Manager > Events Manager > Pixels
2. Click "Add" to create a new pixel
3. Choose installation method: Manual (code) or Partner Integration (WordPress plugin) or via GTM
4. Add the base pixel code to your website's `<head>`
5. Add event codes on relevant pages (e.g., Lead event on thank-you page)
6. Use Meta Pixel Helper (Chrome extension) to verify the pixel is firing

---

## Conversion Tracking Explained

A **conversion** is any valuable action a user takes after clicking your ad: form submission, purchase, phone call, sign-up, or download.

| Platform | Conversion Tracking Tool | What to Track |
|----------|------------------------|--------------|
| **Google Ads** | Google Ads Conversion Tag (via GTM) | Form submissions, phone calls, purchases |
| **Meta Ads** | Meta Pixel + Conversions API | Lead forms, registrations, purchases |
| **LinkedIn** | LinkedIn Insight Tag | Lead form fills, page visits |
| **Analytics** | Google Analytics 4 (GA4) | All conversions across all channels |

> **Real Example:** TechPath runs a Google Search ad for "digital marketing course Bhopal." Without conversion tracking, they only know 100 people clicked the ad (₹3,000 spent). With conversion tracking, they know 8 of those 100 people filled the enquiry form — giving a Cost Per Lead of ₹375. Now they can calculate if this is profitable.

---

## Attribution Windows

An **attribution window** is the time period after a user clicks (or views) your ad during which a conversion is credited to that ad.

| Platform | Default Click Attribution | Default View Attribution |
|----------|--------------------------|-------------------------|
| **Google Ads** | 30 days | 1 day (display only) |
| **Meta Ads** | 7 days click | 1 day view |
| **LinkedIn** | 30 days click | 7 days view |

> **Example:** A user clicks your Meta ad on Monday but does not sign up. On Thursday (3 days later), they return directly to your website and sign up. Because the conversion happened within the 7-day click window, Meta credits this conversion to the ad.

---

## Trainer Activity: Calculate Ad Rank for 4 Advertisers

> **Class Exercise (15 minutes)**
>
> **Scenario:** Four coaching institutes are bidding on the keyword "spoken English course Lucknow" in Google Ads.
>
> **Calculate Ad Rank and determine positions:**
>
> | Advertiser | Max Bid (₹) | Quality Score | Ad Rank = Bid x QS | Position |
> |------------|-------------|---------------|--------------------|---------  |
> | FluentSpeak | 60 | 7 | ? | ? |
> | EnglishGuru | 90 | 4 | ? | ? |
> | SpeakWell | 45 | 10 | ? | ? |
> | TalkRight | 75 | 5 | ? | ? |
>
> **Questions to answer:**
> 1. Which advertiser gets position 1? Why?
> 2. Who bid the highest but did not get the top position?
> 3. Calculate the Actual CPC for the position 1 advertiser using the formula: (Ad Rank of #2 / QS of #1) + ₹0.01
> 4. If SpeakWell increases their bid to ₹60 but keeps QS at 10, what is their new Ad Rank?
> 5. What advice would you give to EnglishGuru to improve their position without increasing their bid?
>
> **Answers (for trainer):**
> - SpeakWell: 45 x 10 = 450 (Position 1)
> - FluentSpeak: 60 x 7 = 420 (Position 2)
> - TalkRight: 75 x 5 = 375 (Position 3)
> - EnglishGuru: 90 x 4 = 360 (Position 4)
> - SpeakWell Actual CPC: (420 / 10) + 0.01 = ₹42.01

---

## Summary

- Major ad platforms: Google Ads (search intent), Meta Ads (interest-based), LinkedIn (B2B), YouTube (video), Twitter/X, Pinterest, Quora
- Ad auctions use the formula: **Ad Rank = Max Bid x Quality Score x Ad Extensions Impact**
- **Quality Score** (1-10) is based on expected CTR, ad relevance, and landing page experience
- A high Quality Score means lower CPC and better ad positions — always optimise QS before increasing bids
- Campaign structure follows: **Campaign > Ad Group/Ad Set > Ads** on all platforms
- Use **Google Tag Manager** to manage all tracking codes in one place without editing website code
- Install **Meta Pixel** to track conversions and enable retargeting for Facebook/Instagram ads
- **Conversion tracking** is mandatory — without it, you cannot measure ROI or optimise campaigns
- **Attribution windows** determine how long after a click/view a conversion is credited to an ad
