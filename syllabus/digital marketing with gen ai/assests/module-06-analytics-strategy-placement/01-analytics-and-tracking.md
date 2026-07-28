# Analytics & Tracking — Measure Everything

**Module 06 — Analytics, Strategy & Career Readiness | Topic 1**

---

## Why Analytics Matters

If you cannot measure it, you cannot improve it. Analytics tells you what is working, what is wasting money, and where to focus your efforts. Without analytics, digital marketing is just guessing with a budget.

Think of analytics like the speedometer and fuel gauge in a car. You could drive without looking at them, but you would not know how fast you are going, when you are running out of fuel, or whether you should take the highway or a shortcut. Analytics gives you those instruments for your marketing.

> **Real Example:** Swiggy tracks everything — what you search for, how long you browse before ordering, which restaurants you skip, and when you usually order dinner. This data drives their push notification timing, restaurant recommendations, and dynamic pricing. Their analytics team is one of the largest in the company.

---

## Google Analytics 4 (GA4)

GA4 is the current version of Google Analytics, launched in 2020 to replace Universal Analytics. It is free, powerful, and used by 90%+ of websites worldwide. Every digital marketer must know GA4.

### Setting Up GA4 via Google Tag Manager (GTM)

Google Tag Manager is a container that lets you add tracking codes to your website without editing code every time.

**Setup steps:**
1. Create a Google Analytics 4 property at analytics.google.com
2. Copy your Measurement ID (starts with G-, like G-ABC123XYZ)
3. Create a Google Tag Manager account at tagmanager.google.com
4. Add the GTM container code to your website's `<head>` section
5. In GTM, create a new tag → Google Analytics: GA4 Configuration
6. Paste your Measurement ID
7. Set trigger to "All Pages"
8. Publish the container

**Data streams:** GA4 can track web, iOS app, and Android app — all in one property. Most businesses start with web only.

---

### GA4 Event Types

GA4 is built around events — every user action is tracked as an event.

| Event Type | What It Tracks | Setup Required | Examples |
|-----------|---------------|---------------|---------|
| **Automatically Collected** | Basic interactions | None — works out of the box | page_view, session_start, first_visit, user_engagement |
| **Enhanced Measurement** | Common interactions | Toggle on in settings | scroll, outbound_click, site_search, video_start, video_complete, file_download |
| **Recommended** | Industry-standard events | Manual setup in GTM | login, sign_up, purchase, add_to_cart, begin_checkout |
| **Custom** | Your unique business events | Manual setup in GTM | applied_for_demo, downloaded_brochure, watched_testimonial |

**Custom event example:** Track when someone clicks "Download Brochure" on your website.

In GTM:
1. Create a trigger: Click → matches CSS selector `.download-btn`
2. Create a tag: GA4 Event → Event name: `download_brochure`
3. Add parameters: `brochure_name`, `page_location`
4. Publish

---

### Key GA4 Reports

| Report | What It Shows | Business Question It Answers |
|--------|-------------|---------------------------|
| **Realtime** | Users on your site right now, their location, active pages | "Is our just-launched campaign driving traffic right now?" |
| **Acquisition Overview** | Where users come from (Google, Instagram, direct, referral) | "Which channel brings the most visitors?" |
| **Traffic Acquisition** | Performance by channel (sessions, engagement, conversions) | "Which channel brings users who actually buy?" |
| **Engagement Overview** | Top pages, events triggered, average session duration | "What do people do on our website?" |
| **Pages and Screens** | Views, time spent per page | "Which blog post gets the most reads?" |
| **Monetization** | Revenue, purchases, average order value | "How much money did our website make today?" |
| **Retention** | New vs returning users, cohort analysis | "Are users coming back after their first visit?" |

---

### GA4 vs Universal Analytics — Key Differences

If you ever see old tutorials or hear senior marketers mention "UA" or "Universal Analytics," know that GA4 works very differently.

| Feature | Universal Analytics (Dead) | GA4 (Current) |
|---------|--------------------------|----------------|
| Data Model | Session-based (pageviews) | Event-based (everything is an event) |
| Cross-Platform | Web only | Web + App in one property |
| Reporting | 100+ pre-built reports | Fewer reports, but highly customizable |
| Privacy | Relied on cookies heavily | Built for a cookieless future |
| Machine Learning | Limited | Built-in (predictive audiences, anomaly detection) |
| Bounce Rate | Old definition (single-page sessions) | Replaced by "Engagement Rate" |
| Goals/Conversions | Goals (max 20) | Key Events (unlimited) |

---

### Conversions / Key Events Setup

In GA4, conversions are called "Key Events." You mark specific events as key events to track your most important actions.

**Common key events for Indian businesses:**

| Business Type | Key Event | How to Track |
|--------------|-----------|-------------|
| E-commerce | `purchase` | Shopify/WooCommerce auto-sends |
| SaaS | `sign_up` | Track form submission |
| Education | `applied_for_course` | Track "Apply Now" button click |
| Real Estate | `contact_form_submit` | Track form submission |
| B2B Services | `request_demo` | Track demo request form |
| Blog/Media | `newsletter_signup` | Track email capture form |

### Audiences and Segments

Audiences let you group users based on shared traits. You can use audiences for analysis or target them with Google Ads.

**Example audiences:**
- Users who visited the pricing page but did not sign up (retarget with ads)
- Users from Mumbai who visited 3+ times in the last week (high intent)
- Users who added to cart but did not purchase (abandoned cart audience)

---

## Looker Studio (Google Data Studio)

Looker Studio is Google's free dashboard and reporting tool. It lets you create beautiful, interactive reports by connecting to data sources like GA4, Google Ads, Google Sheets, and more.

**What you can do with Looker Studio:**
- Create a single dashboard showing GA4 + Google Ads + social media data
- Share live dashboards with clients (they see real-time data without needing GA4 access)
- Schedule automatic email reports (weekly/monthly PDF sent to your inbox)
- Use templates to build dashboards in minutes

**Building a dashboard — step by step:**
1. Go to lookerstudio.google.com
2. Click "Create" → "Report"
3. Add a data source (Google Analytics 4)
4. Drag and drop charts: scorecards, time series, bar charts, tables
5. Add filters: date range, channel, city
6. Style with your brand colors
7. Share the link with your team or client

| Chart Type | Best For | Example |
|-----------|----------|---------|
| **Scorecard** | Single key number | Total users: 12,450 |
| **Time Series** | Trends over time | Sessions per day for the last 30 days |
| **Bar Chart** | Comparing categories | Sessions by channel (organic vs paid vs social) |
| **Pie Chart** | Proportions | Device split (mobile 65%, desktop 30%, tablet 5%) |
| **Table** | Detailed data with multiple columns | Top 10 pages with views, avg. time, bounce rate |
| **Geo Map** | Location data | Users by Indian state |

> **Pro Tip:** Never build a dashboard from scratch when a template exists. Search "GA4 Looker Studio template" and you will find dozens of professional free templates. Customize them with your data source and branding.

---

## Heatmaps and Session Recordings

Heatmaps and session recordings show you HOW users interact with your pages — where they click, how far they scroll, and where they get confused.

### Microsoft Clarity (Free, Unlimited)

Microsoft Clarity is 100% free with unlimited traffic. It is the best starting point for heatmaps.

**What Clarity provides:**
- **Click Heatmaps** — Where users click on each page
- **Scroll Heatmaps** — How far down users scroll (most people never reach the bottom)
- **Session Recordings** — Watch real user sessions like a video replay
- **Dead Clicks** — Places where users click but nothing happens (broken link? Missing button?)
- **Rage Clicks** — Places where users click repeatedly in frustration
- **Quick Backs** — Pages where users land and immediately hit back (bad landing page)

| Tool | Free Tier | Pricing | Best For |
|------|-----------|---------|----------|
| **Microsoft Clarity** | Unlimited (everything free) | Free forever | Everyone, no excuse not to use it |
| **Hotjar** | 35 sessions/day | ₹2,500/month for more | Surveys, feedback widgets |
| **Crazy Egg** | 30-day trial | ₹2,000/month | A/B testing + heatmaps |
| **Lucky Orange** | Free (limited) | ₹800/month | Live chat + heatmaps combo |

**What heatmaps tell you:**

| Heatmap Type | Insight | Action to Take |
|-------------|---------|---------------|
| **Click** | Users click on an image that is not a link | Make it clickable or add a CTA |
| **Click** | Nobody clicks your CTA button | Change button color, text, or position |
| **Scroll** | Only 30% of users reach your pricing section | Move pricing higher on the page |
| **Scroll** | Users stop scrolling at a long text block | Break it up with images, bullets, or video |
| **Dead Click** | Users click on a phone number that is not clickable | Add `tel:` link to make it clickable |
| **Rage Click** | Users repeatedly click a dropdown that does not work on mobile | Fix the mobile dropdown menu |

---

## UTM Tracking

UTM (Urchin Tracking Module) parameters are tags you add to your URLs to track exactly where traffic comes from. Without UTMs, GA4 lumps a lot of traffic into "direct" or "unassigned."

### The 5 UTM Parameters

| Parameter | Required? | What It Tracks | Example |
|-----------|-----------|---------------|---------|
| `utm_source` | Yes | Which platform sent the traffic | `instagram`, `newsletter`, `google` |
| `utm_medium` | Yes | Type of marketing channel | `social`, `email`, `cpc`, `referral` |
| `utm_campaign` | Yes | Campaign name | `summer_sale_2026`, `diwali_launch` |
| `utm_content` | No | Which specific link/creative was clicked | `banner_image`, `text_link`, `cta_button` |
| `utm_term` | No | Paid keyword (for search ads) | `buy_shoes_online`, `digital_marketing_course` |

### UTM Example

**Original URL:**
```
https://techpath.biz/courses/digital-marketing
```

**Tagged URL:**
```
https://techpath.biz/courses/digital-marketing?utm_source=instagram&utm_medium=social&utm_campaign=july_launch&utm_content=bio_link
```

Now in GA4, you can see: "15 users came from Instagram → Social → July Launch → Bio Link"

### UTM Naming Conventions

| Rule | Good | Bad |
|------|------|-----|
| Use lowercase only | `utm_source=instagram` | `utm_source=Instagram` (creates a duplicate entry) |
| Use underscores, not spaces | `summer_sale_2026` | `summer sale 2026` (breaks the URL) |
| Be consistent | Always `facebook`, never `fb` | Switching between `facebook`, `fb`, `Facebook` |
| Be specific | `diwali_sale_oct2026` | `sale` (too vague, cannot distinguish from other sales) |

### Common UTM Mistakes

| Mistake | Why It is a Problem | Fix |
|---------|-------------------|-----|
| Forgetting UTMs on social posts | Traffic shows as "direct" or "social" with no details | Always add UTMs to links in social posts |
| Using different capitalization | `Instagram` and `instagram` appear as two separate sources | Always use lowercase |
| Not tracking email links | Email traffic blends with "direct" | Tag every link in every email |
| Using personal UTMs for ads | Google Ads has auto-tagging — UTMs override it | Let Google Ads auto-tag; use UTMs for non-Google channels |
| Making URLs too long | Looks ugly when shared | Use a URL shortener like Bitly after adding UTMs |

**UTM builder tools:**
- Google Campaign URL Builder (free, official) — ga-dev-tools.google/ga4/campaign-url-builder
- UTM.io (free + paid, saves UTM presets for teams)

---

## Trainer Activity: Set Up GA4 and Track Custom Events

**Time:** 20 minutes

**Task:** Using a free website (WordPress.com, Wix, or a simple HTML page), set up basic analytics tracking:

1. **Create a GA4 property** at analytics.google.com
2. **Install the tracking code** on your practice website (use GTM or direct install)
3. **Define 3 custom events** you would track if this were a real business:
   - Example: `clicked_contact_button`, `scrolled_to_pricing`, `watched_video`
4. **Create a UTM-tagged link** using Google's Campaign URL Builder:
   - Source: `instagram`
   - Medium: `social`
   - Campaign: `class_demo_july2026`
5. **Open the GA4 Realtime report** and visit your website using the UTM link

Verify that the visit appears in the Realtime report with the correct source/medium/campaign.

Each student shares their screen showing the Realtime report with their tagged traffic.

---

## Summary

- **GA4** is free, event-based analytics — every digital marketer must know it
- Set up GA4 through **Google Tag Manager (GTM)** for flexibility
- GA4 has 4 event types: **automatically collected, enhanced measurement, recommended, and custom**
- Key reports: **Acquisition** (where users come from), **Engagement** (what they do), **Monetization** (do they buy)
- **Looker Studio** creates free, shareable dashboards connecting GA4, Ads, and Sheets
- **Microsoft Clarity** provides free unlimited heatmaps and session recordings — install it on every website
- Heatmaps reveal **dead clicks, rage clicks, and scroll drop-off points** that text data cannot show
- **UTM parameters** (source, medium, campaign, content, term) track exactly where traffic comes from
- Always use **lowercase, underscores, and consistent naming** for UTMs
- Without proper tracking, you are **guessing instead of marketing** — set up analytics before spending a single rupee on ads

---

*TechPath Academy — Digital Marketing with Generative AI*
