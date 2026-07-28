# Module 6: Analytics, Strategy, Capstone & Job Placement

---

## Week 26: Web Analytics & Data

### Day 145: GA4 Architecture — Events, Parameters, Sessions

#### The Shift from Universal Analytics to GA4

**The fundamental change:** Universal Analytics (UA) was session-based. GA4 is event-based. Everything a user does — page view, scroll, click, purchase — is tracked as an EVENT with parameters.

| Concept | Universal Analytics (Old) | GA4 (Current) |
|---------|--------------------------|----------------|
| Base unit of measurement | Session (visit) | Event |
| How page views work | Separate "hit type" | Just another event called `page_view` |
| User identification | Client ID only (cookie) | Client ID + User ID + Google Signals |
| Data model | Session → Hits | User → Events → Parameters |
| Default attribution | Last-click | Data-driven (AI-powered) |
| Reporting | 100+ pre-built reports | Flexible explorations |
| Data retention | Unlimited | 2 months or 14 months (free tier) |
| Predictive capabilities | None | Purchase probability, churn probability |
| Cross-platform | Limited | Web + App unified |
| Machine learning | None | Built-in anomaly detection, insights |

#### GA4 Data Model Explained:

```
USER (identified by Client ID or User ID)
└── SESSION (a group of events within a time window)
    └── EVENT (every interaction)
        └── PARAMETERS (details about the event)
```

**Example — Rahul visits TechPath website:**
```
User: client_id_abc123 (Rahul's browser)
├── Session 1 (July 27, 10:00 AM)
│   ├── Event: session_start
│   ├── Event: page_view {page_title: "Home", page_location: "/"}
│   ├── Event: scroll {percent_scrolled: 90}
│   ├── Event: page_view {page_title: "Courses", page_location: "/courses"}
│   ├── Event: page_view {page_title: "Digital Marketing", page_location: "/courses/dm"}
│   ├── Event: cta_click {button_text: "Enroll Now"}
│   └── Event: form_submit {form_id: "enrollment"}
└── Session 2 (July 28, 3:00 PM)
    ├── Event: session_start
    ├── Event: page_view {page_title: "Payment", page_location: "/payment"}
    └── Event: purchase {value: 35000, currency: "INR", transaction_id: "TXN_001"}
```

#### Event Categories in GA4:

| Category | Examples | Setup Required? |
|----------|----------|----------------|
| **Automatically Collected** | `first_visit`, `session_start`, `page_view`, `user_engagement` | No — tracked by default |
| **Enhanced Measurement** | `scroll`, `outbound_click`, `file_download`, `video_start`, `video_complete`, `site_search` | Toggle ON in Admin (no code) |
| **Recommended Events** | `login`, `sign_up`, `purchase`, `add_to_cart`, `begin_checkout`, `generate_lead` | You implement via GTM or code |
| **Custom Events** | `cta_click`, `quiz_complete`, `whatsapp_chat_start` | You define and implement |

#### Event Parameters:
Every event can carry additional information through parameters.

```
Event: purchase
Parameters:
  - transaction_id: "TXN_12345"
  - value: 35000
  - currency: "INR"
  - coupon: "EARLYBIRD"
  - items: [
      {item_name: "Digital Marketing Course", item_category: "Education", price: 35000}
    ]
```

**Custom parameters you should track:**
- `button_text` — Which CTA was clicked
- `form_id` — Which form was submitted
- `page_section` — Which section of the page they interacted with
- `utm_source`, `utm_medium`, `utm_campaign` — Campaign details (auto-captured)

#### Sessions in GA4:
- A session starts when `session_start` event fires
- Sessions timeout after 30 minutes of inactivity (configurable)
- New session starts on midnight (resets daily)
- New session starts when campaign source changes (configurable)

> **Try This:** Open Google Analytics Demo Account (search "GA4 demo account" on Google). Navigate to Admin > Data Streams and explore the configuration. Then go to Reports > Realtime and observe how events fire as the demo store gets traffic.

---

### Day 146: GA4 Reports — Acquisition, Engagement, Monetization, Retention

#### Navigating GA4 Reports

GA4 has two main reporting areas:
1. **Reports** (left sidebar) — Pre-built summary reports
2. **Explore** (left sidebar) — Custom analysis (Explorations)

#### 1. Acquisition Reports
**Location:** Reports > Acquisition

| Report | What It Shows | When to Use |
|--------|--------------|-------------|
| **Acquisition Overview** | Summary of all traffic sources | Daily health check |
| **User Acquisition** | How NEW users found you (first touch) | Understanding discovery channels |
| **Traffic Acquisition** | How ALL sessions arrive (every visit) | Understanding overall traffic mix |

**Default Channel Groupings (how GA4 categorizes traffic):**

| Channel | How GA4 Identifies It | Example |
|---------|----------------------|---------|
| Organic Search | source = google/bing, medium = organic | Someone Googled you |
| Direct | source = (direct), no referrer | Typed URL or bookmarked |
| Organic Social | source = facebook/instagram/twitter, medium = social/organic | Organic social click |
| Paid Search | medium = cpc/ppc | Google Ads click |
| Paid Social | source = facebook/instagram, medium = paid | Meta Ads click |
| Referral | medium = referral | Link from another website |
| Email | medium = email | Click from email campaign |
| Display | medium = display/banner/cpm | Banner ad click |

**Key metrics in Acquisition reports:**
- **Users** — Unique people
- **New users** — First-time visitors
- **Sessions** — Total visits
- **Engaged sessions** — Sessions with 10+ sec, or 2+ pages, or conversion
- **Engagement rate** — Engaged sessions / Total sessions (higher is better)
- **Average engagement time** — How long users actively interact

#### 2. Engagement Reports
**Location:** Reports > Engagement

| Report | What to Look For |
|--------|-----------------|
| **Events** | Which events fire most, custom event tracking |
| **Pages and screens** | Most popular pages, time on page, engagement |
| **Landing pages** | First page users see — optimize these! |
| **Conversions** | Which events you marked as key events |

**Key Engagement Metrics:**
- **Engagement rate** = Engaged sessions / Total sessions (replaces old bounce rate)
- **Average engagement time** = Time users actively interact (not just idle tab)
- **Events per session** = How much users do per visit
- **Views per user** = Pages per user over time

**Note:** "Bounce rate" in GA4 = inverse of engagement rate (100% - engagement rate). A 55% engagement rate = 45% bounce rate.

#### 3. Monetization Reports
**Location:** Reports > Monetization

- E-commerce purchases (if tracking configured)
- Revenue by item, category, brand
- Purchase journey (add_to_cart → begin_checkout → purchase)
- Promotion performance (internal promotions)

**Important for e-commerce businesses. Skip if not selling online.**

#### 4. Retention Reports
**Location:** Reports > Retention

- New vs returning users over time
- User retention by cohort (Week 0, Week 1, Week 2...)
- Lifetime value by first acquisition source
- Engagement over time

**How to read cohort retention:**
- Row = Week users first visited
- Column = Weeks later
- Cell = % of original users who returned

Example: If Week 0 had 1,000 users and Week 4 shows 15%, that means 150 users came back after a month. For most websites, 10-20% at Week 4 is normal.

> **Try This:** In the GA4 Demo Account, navigate to each report section (Acquisition, Engagement, Monetization, Retention). For each, write down: (1) the top traffic source, (2) the most popular page, (3) the retention rate at Week 4. Compare User Acquisition vs Traffic Acquisition — what's different?

---

### Day 147: Conversion Tracking & Attribution Models

#### What is a Conversion (Key Event) in GA4?
A conversion is any event you mark as important to your business. GA4 calls them "Key Events."

**Common Key Events to track:**
- `generate_lead` — Form submission (lead gen)
- `purchase` — Transaction completed (e-commerce)
- `sign_up` — Account created
- `phone_call_click` — Clicked phone number (local business)
- `whatsapp_click` — Clicked WhatsApp chat button
- `demo_booked` — Booked a demo/consultation

**How to mark an event as a Key Event:**
1. Go to Admin > Events
2. Find your event in the list
3. Toggle "Mark as key event" ON
4. OR: Admin > Key Events > New Key Event > type the event name

#### Attribution Models Comparison

Attribution answers: "Which marketing channel gets CREDIT for the conversion?"

| Model | How It Works | Analogy | Best For |
|-------|-------------|---------|----------|
| **Last Click** | 100% credit to last touchpoint | The striker gets all credit for the goal | Simple tracking, short sales cycles |
| **First Click** | 100% credit to first touchpoint | The midfielder who started the play gets credit | Understanding awareness channels |
| **Linear** | Equal credit to all touchpoints | Entire team gets equal credit | When all channels contribute equally |
| **Time Decay** | More credit to recent touchpoints | Recent passes get more credit | Long sales cycles (30+ days) |
| **Position-Based** | 40% first, 40% last, 20% split middle | Assist and scorer get most credit | Balanced view for most businesses |
| **Data-Driven** | AI allocates based on actual patterns | AI decides based on actual game footage | Best accuracy (GA4 default, needs 400+ conversions/month) |

#### Attribution Example with Indian Context:

**Priya's journey to enrolling in TechPath's course (Rs 35,000):**

| Touchpoint | Day | Channel |
|-----------|-----|---------|
| 1st | Day 1 | Saw Instagram Reel about digital marketing careers |
| 2nd | Day 3 | Googled "digital marketing course Bhopal" → Clicked organic result |
| 3rd | Day 5 | Clicked Google Ad for TechPath |
| 4th | Day 7 | Opened email from TechPath → Clicked webinar link |
| 5th | Day 10 | Got WhatsApp message → Called and enrolled |

**Credit by model:**

| Model | Instagram | Organic | Google Ad | Email | WhatsApp |
|-------|-----------|---------|-----------|-------|----------|
| Last Click | Rs 0 | Rs 0 | Rs 0 | Rs 0 | Rs 35,000 |
| First Click | Rs 35,000 | Rs 0 | Rs 0 | Rs 0 | Rs 0 |
| Linear | Rs 7,000 | Rs 7,000 | Rs 7,000 | Rs 7,000 | Rs 7,000 |
| Time Decay | Rs 2,000 | Rs 4,000 | Rs 6,000 | Rs 10,000 | Rs 13,000 |
| Position-Based | Rs 14,000 | Rs 2,333 | Rs 2,333 | Rs 2,333 | Rs 14,000 |

**GA4 Default:** Data-Driven Attribution (only available with enough conversion data — minimum 400 conversions in 28 days). Falls back to Last Click if insufficient data.

**Which model should you use?**
- Starting out / Low data → Last Click (simple to understand)
- Want balanced view → Position-Based (recommended for most)
- Enough data → Data-Driven (let AI decide)

> **Try This:** Think of your own purchase journey (last thing you bought online). List all touchpoints from first awareness to purchase. Apply 3 different attribution models. Which channel would get the most/least credit in each?

---

### Day 148: Looker Studio Dashboards

#### What is Looker Studio?
Free reporting and dashboard tool by Google (formerly Google Data Studio). Connects to 800+ data sources and creates interactive visual reports. Perfect for client reports and internal dashboards.

#### Setting Up Your First Dashboard:

**Step 1: Go to lookerstudio.google.com**
**Step 2: Create > Report > Add data source:**

| Source | What It Connects To |
|--------|-------------------|
| Google Analytics 4 | Website traffic, events, conversions |
| Google Ads | Ad performance, cost, conversions |
| Google Search Console | SEO: queries, impressions, clicks, CTR |
| Google Sheets | Any data you put in a spreadsheet |
| BigQuery | Large datasets, warehouse |
| MySQL/PostgreSQL | Direct database queries |
| Facebook Ads | Via 3rd-party connectors (Supermetrics) |
| CSV Upload | One-time file uploads |

**Step 3: Design Your Dashboard**

**Dashboard Best Practices:**
1. **One page = one story** — Don't cram 50 charts on one page
2. **Top row = KPIs** — Scorecards showing the most important numbers
3. **Comparison period** — ALWAYS show vs previous period (WoW, MoM, YoY)
4. **Date filter** — Let the viewer change the time range
5. **Channel filter** — Let them drill down by traffic source
6. **Color coding** — Green = above target, Red = below target
7. **10-second rule** — Executive should understand the story in 10 seconds
8. **Group related charts** — Put traffic charts together, conversion charts together
9. **Consistent formatting** — Same date format, currency format, number abbreviations
10. **Add context** — Text boxes explaining what metrics mean

#### Essential Dashboard Components for Digital Marketing:

**Page 1: Traffic Overview**
- KPI Row: Users, Sessions, Engagement Rate, Conversions (with % change)
- Time series: Daily sessions (last 30 days)
- Pie chart: Traffic by channel
- Table: Top 10 landing pages (sessions, engagement, conversions)
- Geo map: Users by state/city (India)

**Page 2: SEO Performance** (Google Search Console data)
- KPI Row: Total Clicks, Impressions, Avg CTR, Avg Position
- Table: Top 20 queries (clicks, impressions, CTR, position)
- Time series: Clicks and impressions trend

**Page 3: Campaign Performance** (GA4 + Google Ads)
- KPI Row: Cost, Clicks, Conversions, CPA, ROAS
- Table: Performance by campaign
- Bar chart: Conversions by source/medium

> **Try This:** Create a Looker Studio report connected to the GA4 Demo Account. Add: 1 scorecard (Users), 1 time series (Sessions over time), 1 pie chart (Traffic by channel), and 1 table (Top pages). Apply a date range filter. Share the link.

---

### Day 149: Microsoft Clarity + Hotjar — Heatmaps & Session Recordings

#### Microsoft Clarity (100% Free, Unlimited)

**What it does:**
- **Heatmaps** — Visual maps showing where users click, scroll, and move their cursor
- **Session Recordings** — Watch actual user sessions (anonymized, no personal data)
- **Dead Clicks** — Elements users click that do nothing (frustrated expectation)
- **Rage Clicks** — Rapid frustrated clicking on same element (UX problem)
- **Excessive Scrolling** — Users scrolling back and forth (lost or confused)
- **Quick Backs** — Users who navigate to a page and immediately go back
- **Copilot AI** — AI-generated insights summarizing user behavior patterns

**Setting Up Clarity:**
1. Go to clarity.microsoft.com → Sign in with Microsoft account
2. Create new project → Add your website URL
3. Copy the tracking code → Paste in your website's `<head>` section
4. Wait 1-2 hours for data to start appearing
5. Dashboard shows: Total sessions, pages/session, scroll depth, JS errors

**How to Use Heatmaps:**
- **Click heatmaps** → Find: Where do people click most? Are they clicking non-clickable elements?
- **Scroll heatmaps** → Find: How far down do people scroll? Where do they stop?
- **Move heatmaps** → Find: Where does attention focus? (cursor = eye tracking proxy)

**How to Use Session Recordings:**
- Watch 20-30 recordings of users who converted → What did they do?
- Watch 20-30 recordings of users who bounced → Where did they get stuck?
- Look for patterns: Do multiple users struggle at the same point?

#### Hotjar (Free: 35 sessions/day)

Everything Clarity does PLUS:
- **Surveys** — Pop-up questions on your site ("What brought you here today?")
- **Feedback widgets** — Thumbs up/down on specific pages
- **User interviews** — Recruit site visitors for research calls

**When to use each:**
- Budget-conscious / Just starting → **Microsoft Clarity** (free, unlimited)
- Need surveys and feedback → **Hotjar** (or Clarity + separate survey tool)
- Both → Install BOTH (they don't conflict with each other)

#### What to Look For in Recordings:

| Behavior | What It Means | How to Fix |
|----------|--------------|-----------|
| Rage clicks on a button | Button looks clickable but isn't, or is broken | Make it work or remove it |
| Users not scrolling past hero | Content below fold is invisible | Add scroll indicators, tease content |
| Clicking on images expecting link | Images need to be linked or styled differently | Add links or remove click-bait styling |
| Going back immediately (Quick Back) | Page didn't match expectation from link/ad | Fix ad copy or page content alignment |
| Filling form then abandoning | Form too long or confusing | Reduce fields, add progress indicator |
| Ignoring CTA button | Button not visible or compelling enough | Change color, size, text, or position |

> **Try This:** Set up Microsoft Clarity on any website you have access to (even a free Carrd.co page). Wait 24 hours, then review the heatmap for your homepage. Note 3 observations about how visitors interact with the page.

---

### Day 150: UTM Tracking — Implementation & Best Practices

#### What are UTM Parameters?
UTM (Urchin Tracking Module) codes are tags added to the end of URLs that tell Google Analytics exactly where traffic came from. Without UTMs, GA4 cannot distinguish between a link from your email and a link from your WhatsApp.

#### The 5 UTM Parameters:

| Parameter | Purpose | Required? | Example Values |
|-----------|---------|-----------|----------------|
| `utm_source` | Which platform/site sent the traffic | Yes | google, facebook, instagram, newsletter, whatsapp |
| `utm_medium` | What type of channel | Yes | cpc, email, social, paid_social, banner, referral |
| `utm_campaign` | Which specific campaign | Yes | summer_sale_2026, dm_course_launch_jul2026 |
| `utm_term` | Which keyword (for paid search) | Optional | digital+marketing+course+bhopal |
| `utm_content` | Which specific link/ad variant | Optional | blue_button, hero_banner, sidebar_link |

#### UTM Naming Conventions (CRITICAL — Consistency is Everything):

**Rules to follow:**
1. **ALWAYS lowercase** — `facebook` not `Facebook` (GA4 treats these as different!)
2. **Use underscores** for spaces — `summer_sale` not `summer sale` or `summer-sale`
3. **Be consistent forever** — Once you pick `facebook`, never use `fb` or `Facebook`
4. **Include dates** in campaigns — `dm_course_launch_jul2026` not just `dm_course_launch`
5. **Be specific** — `instagram_story` not just `social`
6. **No special characters** — Never use ? & # @ in UTM values
7. **Document everything** — Maintain a master UTM spreadsheet for your team

#### Standard Source/Medium Combinations (Use These Exactly):

| Channel | utm_source | utm_medium | Usage |
|---------|-----------|-----------|-------|
| Google Search Ads | google | cpc | Google Ads paid search |
| Facebook/Meta Ads | facebook | paid_social | Paid ads on Facebook |
| Instagram Ads | instagram | paid_social | Paid ads on Instagram |
| Instagram Organic | instagram | social | Bio link, story swipe-up |
| Email Newsletter | newsletter | email | Regular email broadcasts |
| Email Automation | automation | email | Automated email sequences |
| WhatsApp Broadcast | whatsapp | messaging | WhatsApp marketing messages |
| YouTube Description | youtube | video | Links in video descriptions |
| LinkedIn Organic | linkedin | social | LinkedIn posts |
| LinkedIn Ads | linkedin | paid_social | Sponsored content |
| Influencer | [influencer_name] | partnership | Collab tracking |
| QR Code (offline) | qr_code | offline | Physical marketing materials |
| Blog Guest Post | [site_name] | referral | Guest post backlinks |

#### How to Build a UTM URL:

**Manual method:**
```
https://techpath.biz/courses/digital-marketing?utm_source=instagram&utm_medium=paid_social&utm_campaign=dm_course_jul2026&utm_content=carousel_ad_v2
```

**Google Campaign URL Builder:** https://ga-dev-tools.google/campaign-url-builder/

**Shortening UTM URLs:**
Long UTM URLs look ugly in social posts. Solutions:
- Use Bitly to shorten (free: 10 links/month with tracking)
- Use your own short URL (yoursite.com/go/campaign-name)
- WhatsApp/email: UTM links are fine as-is (users don't see the URL)

#### UTM Tracking Spreadsheet Template:

| Date | Campaign Name | Source | Medium | Content | Full URL | Purpose |
|------|--------------|--------|--------|---------|----------|---------|
| Jul 2026 | dm_course_jul2026 | instagram | paid_social | carousel_v1 | [full URL] | Course launch carousel ad |
| Jul 2026 | dm_course_jul2026 | newsletter | email | header_cta | [full URL] | Newsletter announcement |
| Jul 2026 | dm_course_jul2026 | whatsapp | messaging | broadcast_1 | [full URL] | WhatsApp broadcast |

> **Try This:** Create UTM-tagged URLs for this scenario: TechPath Academy is launching a free webinar. Create 5 different UTM links for: (1) Instagram bio, (2) Email newsletter, (3) WhatsApp broadcast, (4) LinkedIn post, (5) Google Ad. Use proper naming conventions. Put them in a spreadsheet.

---

### Self-Check Questions: Week 26

1. What are the 4 event categories in GA4? Give 2 examples of each.
2. How is engagement rate different from bounce rate? Which is better and why?
3. A user visits your site from a Google Ad, then comes back 5 days later from an email, then buys via a direct visit. Calculate the credit each channel gets under Last Click, First Click, and Linear attribution.
4. What data source would you connect to Looker Studio to report on SEO keyword performance?
5. Name 3 specific user behaviors Microsoft Clarity can detect that indicate UX problems.
6. Write a complete UTM URL for a Facebook ad promoting a summer sale on an Indian fashion website.
7. Why is UTM naming consistency critical? What happens if one team member uses "Facebook" and another uses "facebook"?

---

## Week 27: Marketing Strategy

### Day 151: 5-Step Marketing Strategy Framework

#### The Framework:

```
Step 1: AUDIT → Where are we NOW?
Step 2: GOALS → Where do we want to GO?
Step 3: STRATEGY → HOW will we get there?
Step 4: TACTICS → WHAT exactly will we do?
Step 5: MEASUREMENT → How do we KNOW it's working?
```

#### Step 1: AUDIT (Current State Assessment)

**What to audit:**
- **Website:** Speed (PageSpeed Insights), mobile-friendliness, UX, content quality, SEO health
- **SEO:** Current rankings, backlinks, domain authority, content gaps
- **Social Media:** Followers, engagement rate, posting frequency, content mix
- **Paid Ads:** Current spend, ROAS, CPA, best-performing campaigns
- **Email:** List size, open rate, CTR, revenue from email
- **Competitors:** Their traffic (SimilarWeb), their ads (Meta Ad Library), their content

**Tools for Auditing:**
| What | Tool | Free? |
|------|------|-------|
| Website speed | PageSpeed Insights | Yes |
| SEO health | Google Search Console | Yes |
| Social engagement | Manual calculation or Metricool | Free tier |
| Competitor traffic | SimilarWeb | 5 searches/day |
| Competitor ads | Meta Ad Library | Yes |
| Competitor keywords | Ubersuggest, SEMrush | Limited free |

**Audit Output:** A 1-page scorecard:
```
Website: 6/10 (slow on mobile, needs CTA optimization)
SEO: 4/10 (only 5 pages indexed, no backlinks)
Social: 7/10 (good engagement but inconsistent posting)
Email: 3/10 (500 subscribers, no automation)
Paid: Not started yet
Overall Digital Maturity: 5/10
```

#### Step 2: GOALS (SMART Goals)

Every goal must be:
- **S**pecific: Not "get more traffic" → "Increase organic traffic to course pages"
- **M**easurable: Include a number → "from 500 to 2,000 monthly visits"
- **A**chievable: Based on benchmarks → "2,000 is realistic given competitor data"
- **R**elevant: Tied to revenue → "more traffic = more leads = more enrollments"
- **T**ime-bound: Deadline → "by December 2026 (6 months)"

**Example SMART Goals for an Indian EdTech:**
1. Increase monthly organic traffic from 2,000 to 8,000 sessions by December 2026
2. Generate 200 qualified leads per month from digital channels by October 2026
3. Achieve Rs 10 lakh monthly revenue from online enrollments by March 2027
4. Grow Instagram from 2,000 to 15,000 followers by December 2026
5. Reduce cost per lead from Rs 500 to Rs 200 by November 2026

#### Step 3: STRATEGY (Channel & Approach Selection)

Based on goals + audience + budget, decide:
- **Which channels** to invest in (and which to IGNORE)
- **Content pillars** — 3-5 recurring content themes
- **Positioning** — How you'll be different from competitors
- **Audience prioritization** — Which persona gets attention first

#### Step 4: TACTICS (90-Day Action Plan)

Specific, weekly actions. Not "do social media" but:
- Week 1: Create 7 Instagram Reels (batch), publish Mon-Sat
- Week 2: Launch Google Ads campaign (3 ad groups, 5 keywords each)
- Week 3: Publish 2 blog posts (target: "digital marketing course India")

#### Step 5: MEASUREMENT (KPI Dashboard + Review Cadence)

- **Weekly:** Traffic, leads, cost/lead (quick pulse check)
- **Monthly:** Revenue, conversion rates, channel performance (deeper analysis)
- **Quarterly:** Strategy review, budget reallocation, new goals

> **Try This:** Pick a real business you visit regularly (your gym, a local restaurant, a shop). Audit their digital presence by checking their website, Instagram, and Google Business Profile. Give them a score out of 10 for each channel and write 3 recommendations.

---

### Day 152: Budget Planning & Channel Mix

#### Budget Allocation by Business Stage

| Channel | Startup (0-1 yr) | Growth (1-3 yr) | Mature (3+ yr) |
|---------|------------------|-----------------|-----------------|
| SEO & Content | 30% | 25% | 20% |
| Paid Ads (Google + Meta) | 25% | 35% | 30% |
| Social Media (organic) | 20% | 15% | 15% |
| Email & WhatsApp | 10% | 10% | 15% |
| Influencer/Partnerships | 5% | 10% | 10% |
| Tools & Software | 10% | 5% | 10% |

**Why allocation changes by stage:**
- **Startup:** Heavy SEO investment builds compounding traffic. Social builds awareness cheaply. Ads test what messaging works.
- **Growth:** Ads scale what's proven to work. SEO maintains. Influencers add credibility.
- **Mature:** Retention matters more (email/WhatsApp). Tools optimize efficiency. Ads maintain market share.

#### Budget Calculation Example:

**Scenario:** Digital Marketing agency for a restaurant in Pune
- Annual budget: Rs 3,00,000 (Rs 25,000/month)
- Stage: Growth

| Channel | % | Monthly Rs | What It Buys |
|---------|---|-----------|-------------|
| SEO & Content | 25% | 6,250 | 2 blog posts/month + local SEO optimization |
| Instagram/Meta Ads | 35% | 8,750 | Rs 250/day ad spend on Reels and offers |
| Social Media | 15% | 3,750 | Content creation, Canva Pro, scheduling tool |
| Email + WhatsApp | 10% | 2,500 | MailerLite + WhatsApp broadcasts |
| Influencer | 10% | 2,500 | 1 food blogger collaboration/month |
| Tools | 5% | 1,250 | Analytics, design tools |

> **Try This:** You're given a Rs 50,000/month budget for a new D2C brand selling organic skincare products in India. Allocate across channels. Justify each allocation in 1 sentence. What would you change if the budget were cut to Rs 20,000/month?

---

### Day 153: Forecasting & Goal Modeling

#### Revenue Forecasting Formula:

```
Projected Revenue = Traffic x Conversion Rate x Average Order Value (AOV)
```

**Example:**
- Monthly website visitors: 20,000
- Conversion rate: 2%
- Average Order Value: Rs 1,500
- **Projected Revenue: 20,000 x 0.02 x 1,500 = Rs 6,00,000/month**

#### Leads Required Calculation:

```
Leads Needed = Revenue Goal / (Close Rate x Average Deal Value)
```

**Example for a course selling at Rs 35,000:**
- Revenue goal: Rs 10,50,000/month (30 enrollments)
- Close rate (lead → paid): 10%
- Leads needed: 10,50,000 / (0.10 x 35,000) = 300 leads/month

#### Working Backwards from Goals:

```
Goal: 300 leads/month
├── Website needs: 300 / 5% conversion rate = 6,000 visitors/month
│   ├── From SEO (40%): 2,400 visitors → Need 20 ranking keywords
│   ├── From Ads (35%): 2,100 visitors → Budget: 2,100 x Rs 30 CPC = Rs 63,000
│   ├── From Social (15%): 900 visitors → Need 30K followers with 3% click rate
│   └── From Email (10%): 600 visitors → Need 6,000 subscribers with 10% CTR
```

#### Forecasting Models:

**Conservative (use this for client proposals):** Based on industry averages
**Moderate:** Based on your best-performing months
**Optimistic:** Based on best-case scenario (everything works perfectly)

Always present all three to clients:
```
Conservative: Rs 3,00,000/month by Month 6
Moderate: Rs 5,00,000/month by Month 6
Optimistic: Rs 8,00,000/month by Month 6
```

> **Try This:** A local gym charges Rs 3,000/month membership. They want Rs 5,00,000/month revenue. Calculate: (1) How many members needed? (2) If their website converts at 3%, how many visitors? (3) At Rs 50 per click on Google Ads, what's the ad budget to fill the gap?

---

### Day 154: Competitive Intelligence

#### Competitive Analysis Framework:

**Step 1: Identify 3-5 competitors**
- Direct competitors (same product/service/location)
- Indirect competitors (different product, same audience)
- Aspirational competitors (where you want to be in 2 years)

**Step 2: Analyze each competitor across:**

| Dimension | What to Check | Tool |
|-----------|--------------|------|
| Traffic volume | Monthly visits, growth trend | SimilarWeb |
| Traffic sources | % organic vs paid vs social | SimilarWeb |
| Top keywords | What they rank for that you don't | SEMrush / Ubersuggest |
| Content strategy | Blog frequency, topics, formats | Manual review |
| Social strategy | Posting frequency, engagement, content types | Manual + Metricool |
| Ad strategy | What ads they run, messaging, creatives | Meta Ad Library |
| Pricing | How they price, packages, discounts | Website review |
| Reviews | Customer sentiment, complaints | Google Reviews, Glassdoor |
| Tech stack | What tools/platforms they use | BuiltWith |

**Step 3: Create Competitor Matrix**

| Factor | You | Competitor A | Competitor B | Competitor C |
|--------|-----|-------------|-------------|-------------|
| Monthly traffic | 2,000 | 15,000 | 8,000 | 25,000 |
| Instagram followers | 500 | 5,000 | 12,000 | 3,000 |
| Blog posts/month | 2 | 8 | 4 | 12 |
| Google Ads active | No | Yes | Yes | Yes |
| Avg review rating | 4.5 | 4.2 | 4.8 | 4.0 |
| Pricing | Rs 35K | Rs 45K | Rs 25K | Rs 50K |

**Step 4: Identify gaps and opportunities**
- What are competitors doing that you're NOT? (Gaps to fill)
- What are competitors doing POORLY? (Opportunity to beat them)
- What are competitors IGNORING? (Blue ocean opportunity)

> **Try This:** Pick 3 competitors for TechPath Academy (other digital marketing institutes in India). Use SimilarWeb (free) and Instagram to compare their: traffic, social following, content frequency, and pricing. What opportunity do you see?

---

### Day 155: Pitch Deck Creation

#### 10-Slide Pitch Deck Structure:

| Slide | Title | What to Include | Time |
|-------|-------|----------------|------|
| 1 | Cover | Proposal title, client name, your name, date | 15 sec |
| 2 | About Us | Team credentials, 2-3 key achievements | 45 sec |
| 3 | The Challenge | Client's problems with EVIDENCE (audit data) | 60 sec |
| 4 | Market Opportunity | Industry trends, competitor gaps, opportunity size | 60 sec |
| 5 | Our Strategy | 3-4 strategic pillars, channel selection, approach | 90 sec |
| 6 | Tactical Plan | 90-day breakdown, weekly actions, content plan | 90 sec |
| 7 | Expected Results | Projected KPIs at 3/6/12 months with numbers | 60 sec |
| 8 | Case Study | Before/after from similar project (numbers!) | 60 sec |
| 9 | Investment | Pricing packages, what's included, ROI justification | 60 sec |
| 10 | Next Steps | CTA, onboarding timeline, contact details | 30 sec |

**Pitch Deck Design Rules:**
- Maximum 6 words per bullet point
- One idea per slide (never cram two concepts)
- Dark text on light background (or the inverse — not both mixed)
- 3 colors max (brand color + neutral + accent)
- Every number should be visualized (chart, graph, or highlighted)
- Presenter speaks, slides SUPPORT — they don't replace you

---

### Day 156: Client Proposal & Pricing

#### Pricing Models for Digital Marketing Services (India 2026):

| Model | How It Works | Best For | Range |
|-------|-------------|----------|-------|
| **Monthly Retainer** | Fixed fee per month, defined scope | Ongoing relationships | Rs 15K-2L/month |
| **Project-Based** | Fixed fee for a defined deliverable | One-time projects | Rs 25K-5L per project |
| **Hourly** | Charge per hour of work | Consulting, training | Rs 1K-5K/hour |
| **Performance** | Fee tied to results (leads, sales) | PPC, lead gen | 15-20% of ad spend |
| **Hybrid** | Base retainer + performance bonus | Aligned incentives | Retainer + 10% of revenue above target |

#### How to Price Your Services (Pricing Formula):

```
Monthly Rate = (Desired Annual Income / 12) / Number of Clients You Can Handle

Example:
- Want to earn Rs 6 LPA as a freelancer
- Can handle 4 clients comfortably
- Monthly rate per client: Rs 50,000 / 4 = Rs 12,500/month minimum
```

**Indian Market Rates (2026):**

| Service | Freelancer Rate | Agency Rate |
|---------|----------------|-------------|
| SEO (basic) | Rs 10-20K/month | Rs 25-50K/month |
| Social Media Management | Rs 8-15K/month | Rs 20-40K/month |
| Content Writing | Rs 1-3K/article | Rs 3-8K/article |
| Google Ads Management | 15% of spend (min Rs 8K) | 20% of spend (min Rs 15K) |
| Meta Ads Management | 15% of spend (min Rs 8K) | 20% of spend (min Rs 15K) |
| Email Marketing | Rs 5-10K/month | Rs 15-25K/month |
| Full-Service Digital | Rs 25-50K/month | Rs 75K-2L/month |

> **Try This:** Create a pricing page for yourself as a freelance digital marketer. List 3 packages (Basic/Standard/Premium) with: what's included, monthly price, and ideal client type. Price them based on the Indian market rates above.

---

### Self-Check Questions: Week 27

1. What are the 5 steps in the marketing strategy framework?
2. Write a SMART goal for a restaurant wanting more delivery orders online.
3. If a business has Rs 1,00,000/month budget at Growth stage, how much goes to paid ads?
4. Calculate: Website needs 15,000 visitors/month. Conversion rate is 2%. AOV is Rs 800. What's the projected monthly revenue?
5. Name 3 free tools for competitive intelligence and what each shows you.
6. What are the 10 slides in a pitch deck? Which slide gets the most time?
7. A freelancer wants to earn Rs 8 LPA and can handle 5 clients. What should they charge per client per month?

---

## Week 28: AI in Marketing 2026

### Day 157: AI Types in Marketing (Generative, Predictive, Agentic)

#### Three Types of AI in Marketing:

##### 1. Generative AI
**What it does:** Creates NEW content — text, images, video, audio, code
**Tools:** ChatGPT, Claude, Midjourney, DALL-E, Runway, Synthesia
**Marketing uses:**
- Write blog posts, ad copy, email sequences (10x faster)
- Generate social media graphics and carousels
- Create video scripts and AI voiceovers
- Design landing pages from text descriptions
- Generate product descriptions at scale

##### 2. Predictive AI
**What it does:** Analyzes historical data to predict future outcomes
**Tools:** GA4 predictive audiences, HubSpot lead scoring, Salesforce Einstein
**Marketing uses:**
- Predict which leads will convert (lead scoring)
- Forecast campaign performance before spending budget
- Identify churn-risk customers before they leave
- Optimal send time prediction for emails
- Dynamic pricing (adjust based on demand patterns)

##### 3. Agentic AI
**What it does:** Takes autonomous actions based on goals — the newest and most powerful type
**Tools:** Custom GPTs with actions, AI agents, Claude with tool use, AutoGPT concepts
**Marketing uses:**
- Automatically adjust ad budgets based on real-time performance
- Monitor brand mentions and respond without human intervention
- Run A/B tests, analyze results, and implement winners automatically
- Generate weekly reports and email them to stakeholders
- Handle customer support queries end-to-end

#### The AI Marketing Stack 2026:

| Category | Top Tools | Monthly Cost | What It Replaces |
|----------|-----------|-------------|-----------------|
| Content Writing | ChatGPT Plus, Claude Pro | Rs 1,600-2,000 | 80% of copywriter's drafting time |
| Image Generation | Midjourney, DALL-E 3, Canva AI | Rs 800-2,500 | Stock photos, basic design |
| Video | Runway, Synthesia, HeyGen | Rs 2,000-5,000 | Simple explainer videos |
| SEO Optimization | Surfer SEO AI, Clearscope | Rs 5,000-8,000 | Manual content optimization |
| Social Media | Predis AI, Ocoya | Rs 1,000-3,000 | Content ideation + creation |
| Ads Optimization | Google Performance Max, Meta Advantage+ | Built into ad spend | Manual bid adjustments |
| Email Optimization | Subject line AI, send time AI (built into ESPs) | Built into ESP | Manual testing |
| Analytics | GA4 AI Insights, Amplitude AI | Free-Rs 8,000 | Manual data analysis |
| Customer Support | Tidio AI (Lyro), ManyChat AI | Rs 2,000-5,000 | Tier-1 support agents |

---

### Day 158: Custom GPTs for Marketing

#### What are Custom GPTs?
Custom versions of ChatGPT trained on YOUR specific instructions, knowledge, and tools. You create them once, then use repeatedly for consistent outputs.

#### Custom GPTs Every Marketer Should Build:

| GPT Name | Purpose | Instructions Include |
|----------|---------|---------------------|
| Brand Voice Writer | Write copy in your brand's tone | Brand guidelines, tone examples, do/don't list |
| SEO Content Creator | Generate SEO-optimized articles | Target keywords, content structure, word count |
| Social Media Manager | Generate post ideas + captions | Platform specs, hashtag strategy, persona details |
| Email Sequence Writer | Create email drip campaigns | Sequence templates, CTA formulas, brand voice |
| Ad Copy Generator | Write Google/Meta ad variations | Character limits, USPs, competitor positioning |
| Client Report Narrator | Turn data into insights | Report template, KPI definitions, analysis framework |
| Proposal Writer | Generate client proposals | Proposal structure, pricing, case studies |

#### Building a Custom GPT (Step-by-Step):

1. Go to chat.openai.com → Explore GPTs → Create
2. **Name:** "TechPath Content Writer"
3. **Description:** "Creates blog posts and social content for TechPath Academy in our brand voice"
4. **Instructions:** (This is the key part)
```
You are TechPath Academy's content writer. Follow these rules:
- Tone: Professional but friendly. Simple English. No jargon without explanation.
- Audience: Indian college students and freshers (age 18-25) interested in digital marketing careers.
- Always include: Practical examples, Indian context (INR, Indian companies, Indian cities), actionable tips.
- Never include: Complex technical terms without explanation, content irrelevant to Indian market.
- Format: Use headings, bullet points, and short paragraphs. Maximum 3 sentences per paragraph.
- CTA: Every piece ends with a clear call-to-action related to TechPath's courses.
```
5. **Knowledge:** Upload brand guidelines PDF, past content examples, competitor analysis
6. **Capabilities:** Enable web browsing (for research), DALL-E (for images)
7. Test with sample prompts → Refine instructions based on output quality

> **Try This:** Build a Custom GPT (free ChatGPT users can't create, but can plan). Write the complete instructions for a "LinkedIn Post Generator" GPT that creates posts for a digital marketing professional in India. Include: tone, format, topics, hashtags, and do/don't rules.

---

### Day 159: Vibe Coding for Marketers

#### What is Vibe Coding?
Using AI tools to build functional websites, landing pages, and tools by describing what you want in plain English — without writing a single line of code yourself. The AI generates the code.

#### Tools for Vibe Coding:

| Tool | URL | Best For | Cost |
|------|-----|----------|------|
| **Bolt.new** | bolt.new | Full web apps from text description | Free tier available |
| **Lovable** | lovable.dev | Beautiful landing pages | Free tier |
| **v0 by Vercel** | v0.dev | UI components, sections | Free tier |
| **Replit Agent** | replit.com | Build apps conversationally | Free tier |
| **Cursor** | cursor.sh | AI code editor (for learning) | Free tier |
| **Claude Artifacts** | claude.ai | Quick interactive tools, calculators | Included with Claude |

#### What Marketers Can Build with Vibe Coding:

1. **Landing pages** — For campaigns, lead magnets, product launches
2. **Calculators** — ROI calculator, EMI calculator, savings calculator
3. **Quiz tools** — Lead generation quizzes ("Find your perfect course")
4. **Portfolio websites** — Personal brand showcase
5. **Micro-tools** — UTM builder, headline analyzer, word counter
6. **Dashboards** — Simple data visualization pages
7. **Email templates** — Custom HTML email designs
8. **Pricing pages** — Interactive pricing calculators

#### Example: Building a Landing Page with Bolt.new

**Prompt to Bolt.new:**
```
Build a modern landing page for TechPath Academy's Digital Marketing course.
Include:
- Hero section with headline "Launch Your Digital Marketing Career in 6 Months" and a CTA button "Enroll Now"
- Social proof section: "500+ students placed, 4.8 rating, 85% placement rate"
- 3-column features section: Live Projects, Industry Certifications, Placement Support
- Testimonial carousel with 3 student reviews
- Pricing section: Rs 35,000 (show Rs 50,000 crossed out)
- FAQ accordion section
- Contact form (Name, Email, Phone, Course Interest)
- Footer with social links
- Color scheme: Dark blue and orange
- Mobile responsive
- Indian context throughout
```

**Result:** A fully functional landing page in 2-3 minutes.

> **Try This:** Go to bolt.new (or v0.dev). Describe a simple landing page for a fictional business in 5-6 sentences. See what it generates. Then try asking it to add/change features iteratively. Save the result — this is a portfolio piece!

---

### Self-Check Questions: Week 28

1. What are the 3 types of AI in marketing? Give 1 example tool for each.
2. How would you use generative AI to create a month's worth of social content in one afternoon?
3. What is a Custom GPT and why would a marketer build one?
4. Write the instruction prompt for a Custom GPT that generates Instagram captions for a fitness brand.
5. What is vibe coding? Name 3 tools and what each creates best.
6. A client asks: "Will AI replace my marketing team?" How would you answer?

---

## Week 29: Career Preparation

### Day 160: ATS-Optimized Resume Building

#### What is ATS?
Applicant Tracking System — software that scans resumes BEFORE a human sees them. 75%+ of Indian companies use ATS (Naukri's built-in ATS, LinkedIn, Greenhouse, Workday).

**If ATS can't read your resume, no human ever will.**

#### Top 10 ATS Rules:

1. **Simple single-column format** — No tables, text boxes, columns, headers/footers
2. **Standard section headings** — Use: "Work Experience", "Education", "Skills" (NOT creative names like "My Journey")
3. **Include keywords EXACTLY as in job description** — If JD says "Google Analytics" don't write just "GA4"
4. **Standard fonts** — Arial, Calibri, Times New Roman (size 11-12pt)
5. **Save as PDF** — Unless specifically asked for .docx
6. **No images or icons** — ATS cannot read them (rating stars, logos, etc.)
7. **Spell out acronyms first time** — "Search Engine Optimization (SEO)"
8. **Use bullet points** — Not paragraphs. Start each with an action verb.
9. **Include dates** — "Jun 2025 - Present" format (month/year)
10. **One page** — For freshers and 0-5 years experience

#### Resume Template for Digital Marketing Fresher:

```
RAHUL SHARMA
+91 98765 43210 | rahul.sharma@email.com | linkedin.com/in/rahulsharma | Bhopal, India

PROFESSIONAL SUMMARY
Digital Marketing professional with hands-on experience in SEO, Google Ads, social media marketing,
and marketing automation. Completed 6-month intensive training with 10+ live projects. Google Analytics
and Google Ads certified. Seeking a role where I can apply data-driven marketing strategies to drive
growth.

SKILLS
Digital Marketing | Search Engine Optimization (SEO) | Google Ads | Meta Ads | Social Media Marketing |
Content Marketing | Email Marketing | Marketing Automation | Google Analytics 4 (GA4) | Google Tag
Manager | Looker Studio | HubSpot CRM | Zapier | Canva | WordPress | MailerLite | A/B Testing

PROJECTS & EXPERIENCE
Digital Marketing Intern — TechPath Academy | Jun 2026 - Present
• Managed Instagram account growing followers from 0 to 2,500 in 3 months through Reels-first strategy
• Set up and managed Google Ads campaigns with Rs 50,000 monthly budget achieving 4.2x ROAS
• Built complete email automation funnel generating 150+ leads/month using MailerLite
• Created GA4 dashboard in Looker Studio tracking 15+ KPIs for weekly client reporting
• Wrote 12 SEO-optimized blog posts ranking on Page 1 for 8 target keywords

Freelance Digital Marketer | Mar 2026 - Jun 2026
• Managed social media for 3 local businesses in Bhopal (restaurant, salon, tuition centre)
• Increased client Instagram engagement by 120% through content calendar and Reels strategy
• Set up Google Business Profiles and improved local search visibility for all 3 clients

EDUCATION
Digital Marketing with Gen AI (6-Month Program) — TechPath Academy | 2026
Bachelor of Commerce — Barkatullah University, Bhopal | 2025

CERTIFICATIONS
• Google Analytics Certification (2026)
• Google Ads Search Certification (2026)
• Meta Certified Digital Marketing Associate (2026)
• HubSpot Inbound Marketing Certification (2026)
• HubSpot Email Marketing Certification (2026)
```

**Action Verbs for Resume Bullets:**
Managed, Created, Increased, Optimized, Built, Launched, Generated, Analyzed, Developed, Implemented, Designed, Grew, Achieved, Reduced, Improved, Tracked, Led, Collaborated

> **Try This:** Write your resume using the template above. Even if you haven't completed all projects yet, write it as if you have (you will by the end of this course). Include at least 3 bullet points with NUMBERS.

---

### Day 161: LinkedIn Profile Optimization

#### LinkedIn Profile Optimization Checklist:

| Section | What to Optimize | Example |
|---------|-----------------|---------|
| **Photo** | Professional headshot, plain background, smile | Ring light + white wall + formal shirt |
| **Banner** | Custom image showing your expertise | "Digital Marketing Specialist | Helping Brands Grow Online" |
| **Headline** | Not "Student at XYZ" — use keywords + value prop | "Digital Marketing Specialist | SEO, Google Ads & Social Media | Helping Indian Businesses Get More Leads Online" |
| **About** | 3 paragraphs: Who you are, what you do, what you want | Include keywords, achievements, personality |
| **Experience** | Add projects as work experience | TechPath Internship, Freelance work, even class projects |
| **Featured** | Pin 3 best posts/projects | Portfolio link, case study, certification |
| **Skills** | Add 50 skills (max), get endorsements | Ask classmates to endorse you |
| **Certifications** | Add ALL completed certifications | Google, Meta, HubSpot certs |
| **Recommendations** | Get 3+ from peers/mentors | Write for others first, they'll reciprocate |

#### LinkedIn Content Strategy (For Job Seekers):

**Post 3-5 times per week:**
- Monday: Share a learning/insight from the week
- Wednesday: Break down a marketing concept (educational)
- Friday: Share a project result or case study
- Weekend: Engage on others' posts (comment 10-15 posts)

**Post Format That Works:**

```
Hook line (grab attention — 1 line)

[blank line]

Story or insight (5-8 lines, keep short)

[blank line]

Key takeaway (1-2 bullets)

[blank line]

CTA: "What do you think?" or "Share your experience below"

#DigitalMarketing #SEO #CareerGrowth
```

---

### Day 162-163: Interview Preparation — 30 Common DM Interview Questions

#### The STAR Method for Interview Answers:

- **S**ituation — Set the scene briefly (1-2 sentences)
- **T**ask — What was your responsibility/challenge (1 sentence)
- **A**ction — What YOU specifically did (3-4 sentences — the bulk of your answer)
- **R**esult — Quantified outcome (1-2 sentences with NUMBERS)

#### 30 Most Common Digital Marketing Interview Questions (India 2026):

**General (1-5):**

**Q1: What is digital marketing?**
Marketing products and services through digital channels — search engines, social media, email, websites, apps, and messaging platforms — to reach customers where they spend time online. It's measurable, targetable, and scalable compared to traditional marketing.

**Q2: What's the difference between inbound and outbound marketing?**
Inbound: Attract customers to you with valuable content (SEO, blogs, social media). They come when they're ready. Outbound: Push messages to audience (cold calls, TV ads, billboards). You interrupt them. Modern marketing is 70-80% inbound.

**Q3: What is your favourite digital marketing channel and why?**
Pick ONE you know well. Example: "Content marketing and SEO — because it compounds. One good blog post can generate leads for years with zero ongoing cost. I built a blog that gets 5,000 monthly visits from a single 3,000-word article."

**Q4: How do you stay updated with marketing trends?**
"I follow Search Engine Journal, HubSpot Blog, and Neil Patel daily. I'm subscribed to Marketing Brew newsletter. I'm active on LinkedIn following industry leaders like Rand Fishkin and Sorav Jain. I also test new tools personally every month."

**Q5: What KPIs would you track for a new e-commerce brand?**
Traffic (by source), Conversion rate, Customer Acquisition Cost (CAC), ROAS, Average Order Value (AOV), Cart abandonment rate, Email revenue percentage, Return customer rate.

**SEO (6-8):**

**Q6: What are the 3 pillars of SEO?**
On-page (content, meta tags, internal links, headings), Off-page (backlinks, brand mentions, social signals), Technical (site speed, mobile-friendly, crawlability, schema markup, Core Web Vitals).

**Q7: What is a backlink and why does it matter?**
A link from another website to yours — like a "vote of confidence." Google uses backlinks as a major ranking factor. 1 link from a high-authority site (DA 70+) is worth more than 100 links from low-quality sites.

**Q8: Website traffic dropped 40% overnight. What do you do?**
Step 1: Check Google Search Console for manual actions or security issues. Step 2: Check if there was a Google algorithm update (Search Engine Roundtable). Step 3: Check technical issues (is the site down? is indexing blocked?). Step 4: Review recent site changes (redesign? content removed? redirects broken?). Step 5: Check if competitors surged. Step 6: Compare time period (seasonal drop?).

**Social Media (9-11):**

**Q9: How would you grow an Instagram account from 0 to 10,000?**
Focus 100% on Reels (algorithm favors them). Post daily for 90 days. Use trending audio. Niche down (don't be generic). Engage genuinely with 30 accounts daily. Collab with similar-size creators. Run a giveaway at 1,000 followers. Create shareable/saveable content.

**Q10: Organic reach is declining. How do you still grow organically?**
Focus on Reels/Shorts (algorithm boost for video). Create "saveable" and "shareable" content (value > entertainment for reach). Build a community (WhatsApp group, DMs, comments). Leverage UGC. Cross-promote platforms. Use SEO on YouTube/Pinterest (these are search engines).

**Q11: What metrics matter most for social media?**
Engagement rate (not vanity follower count), Saves and Shares (higher algorithmic value than likes), Click-through to website, Conversion from social traffic, DM conversations (for service businesses).

**Paid Ads (12-15):**

**Q12: What is ROAS and what's a good ROAS?**
Return on Ad Spend = Revenue from Ads / Cost of Ads. A ROAS of 4x means you earned Rs 4 for every Rs 1 spent. Good: 3-5x (most businesses). Great: 5-10x. Exceptional: 10x+. Break-even ROAS = 1 / Profit Margin (50% margin needs 2x minimum).

**Q13: Google Ads vs Meta Ads — when to use which?**
Google = Intent-based. People are SEARCHING for a solution. Use when: search volume exists, people know they have a problem. Meta = Interest-based. People aren't searching, you FIND them. Use when: creating awareness, visual product, emotional purchase, audiences don't know they need you yet.

**Q14: What is Quality Score in Google Ads?**
Google's rating (1-10) of your ad's relevance. Based on: Expected CTR, Ad relevance to keyword, Landing page experience. Higher score = lower CPC (you pay less per click) + better ad position. A QS of 10 can pay 50% less than a QS of 5 for the same keyword.

**Q15: How would you reduce CPA (Cost Per Acquisition) on Google Ads?**
Improve Quality Score (better ads + landing pages). Add negative keywords (stop irrelevant clicks). Tighten targeting (remove low-performing locations/devices). Test ad copy variations. Improve landing page conversion rate. Use audience segments (remarketing converts cheaper). Adjust bid strategy based on data.

**Email Marketing (16-18):**

**Q16: How would you improve email open rates below 15%?**
Fix sender reputation (clean list, remove bounces). A/B test subject lines aggressively. Segment — send relevant content to each group. Optimize send time (test different days/times). Use personalization in subject line. Re-engage or remove inactive subscribers (they drag down rates).

**Q17: What is email deliverability and how do you maintain it?**
The ability to land in inbox (not spam). Maintain with: Authentication (SPF/DKIM/DMARC), permission-based list only, low complaint rate (below 0.1%), consistent sending volume (don't spike), avoid spam trigger words, clean list monthly (remove bounces + inactive).

**Q18: How would you write a high-converting email sequence?**
Follow the 7-email welcome framework: (1) Deliver lead magnet + set expectations, (2) Tell your story, (3) Give a quick win, (4) Social proof/case study, (5) Address objections, (6) Soft introduce offer, (7) Direct offer with urgency. Each email has ONE goal and ONE CTA.

**Analytics (19-21):**

**Q19: Explain sessions vs users vs page views in GA4.**
User = One unique person (tracked by cookie/device). Session = One visit by that user (resets after 30 min inactivity). Page view = One page loaded. Example: 1 user visits 3 pages in the morning (1 session, 3 page views), returns in the evening (same user, new session). Total: 1 user, 2 sessions, multiple page views.

**Q20: What is a conversion funnel? How do you analyze drop-off?**
The step-by-step journey from awareness to purchase. Example: Visit (100%) → View product (40%) → Add to cart (15%) → Checkout (8%) → Purchase (5%). Analyze: Where's the biggest drop? If 40% view product but only 15% add to cart → product page needs improvement (better images, reviews, pricing clarity).

**Q21: How do you measure content marketing ROI?**
(Traffic from content x Conversion rate x Average order value) - Content creation cost. Also track: Rankings gained, Backlinks earned, Email sign-ups from content, Brand search volume increase, Social shares.

**Strategy (22-25):**

**Q22: How would you allocate a Rs 5 lakh monthly budget?**
Depends on business stage and goals. For a Growth-stage D2C brand: 35% paid ads (Google + Meta), 25% content/SEO (blog + video), 15% social media (organic + tools), 10% email/WhatsApp, 10% influencer partnerships, 5% tools. I'd reallocate every month based on ROAS data.

**Q23: How would you market with zero budget?**
Leverage free channels: SEO (blog posts targeting long-tail keywords), Organic social media (Reels daily), WhatsApp community building, Strategic partnerships/collaborations, User-generated content campaigns, Google Business Profile optimization, Referral program (incentivize word-of-mouth), PR/guest posting for backlinks.

**Q24: Describe your approach to competitor analysis.**
Identify 5 competitors → Analyze: traffic volume and sources (SimilarWeb), keywords they rank for (Ubersuggest), ads they run (Meta Ad Library), content strategy (blog frequency, topics), social engagement, pricing, reviews. Create comparison matrix. Identify gaps (what they miss that I can do better) and opportunities (underserved channels/topics).

**Q25: A campaign is underperforming after 1 week. What do you do?**
Don't panic — check data objectively. (1) Which metric is poor? Traffic? CTR? Conversion? (2) Compare to benchmarks (is it actually bad or just meeting expectations?). (3) Identify the bottleneck (ads getting clicks but landing page not converting = LP problem). (4) Form one hypothesis. (5) Make ONE change (not five). (6) Run for 3-5 more days. (7) Analyze. Repeat.

**Scenario-Based (26-28):**

**Q26: Client wants results in 1 week. How do you respond?**
Be honest about timelines. Quick wins possible: Google Ads (leads within 24 hours), social media boosted posts (reach within hours), email blast to existing list (revenue today). Long-term results: SEO (3-6 months), content marketing (2-3 months), organic social (1-3 months). Present a 30/60/90 day plan showing what's achievable at each milestone.

**Q27: How would you handle negative reviews online?**
Respond quickly (within 24 hours). Be empathetic ("We're sorry you had this experience"). Don't be defensive. Acknowledge the specific issue. Take conversation offline ("Please DM/call us so we can resolve this"). Fix the actual problem. Follow up after resolution. Never delete legitimate negative reviews — they build trust when handled well.

**Q28: A client's website has 50,000 monthly visitors but only 10 leads/month. What's wrong?**
Conversion rate of 0.02% is extremely low (average: 2-5%). Diagnose: (1) Is traffic relevant? (check keywords — maybe traffic is for informational queries not buying intent). (2) Is there a clear CTA? (3) Is the form/page confusing? (4) Mobile experience? (65% traffic is mobile). (5) Page speed? (6) Is there social proof? Use Clarity/heatmaps to see where users drop off.

**Personal & Career (29-30):**

**Q29: What would you do in your first 30 days at this job?**
Week 1: Learn the business, products, audience. Audit current marketing. Meet all stakeholders. Week 2-3: Identify quick wins and critical gaps. Implement 2-3 quick wins for early credibility. Week 4: Present a 90-day plan with priorities, budget needs, and expected outcomes. Throughout: Ask lots of questions, listen more than I speak.

**Q30: Where do you see yourself in 3 years?**
"I want to grow from executing campaigns to leading strategy. In 3 years, I see myself managing a portfolio of brands or leading a marketing team — with a proven track record of measurable ROI. I'm specifically interested in deepening my expertise in [your strongest area: SEO/performance marketing/content], while developing leadership skills."

---

### Day 164: Salary Negotiation & Career Planning

#### Indian Digital Marketing Salary Benchmarks 2026:

| Role | Experience | Salary Range (Annual) |
|------|-----------|----------------------|
| Digital Marketing Executive | 0-1 year (Fresher) | Rs 2.5 - 4.5 LPA |
| SEO Executive | 0-2 years | Rs 3 - 5 LPA |
| Social Media Executive | 0-2 years | Rs 2.5 - 4.5 LPA |
| Content Writer | 0-2 years | Rs 2.5 - 5 LPA |
| PPC/Performance Marketing Exec | 1-2 years | Rs 3.5 - 6 LPA |
| Digital Marketing Manager | 3-5 years | Rs 6 - 12 LPA |
| SEO Manager | 3-5 years | Rs 7 - 14 LPA |
| Performance Marketing Manager | 3-5 years | Rs 8 - 15 LPA |
| Content Marketing Manager | 3-5 years | Rs 6 - 12 LPA |
| Head of Digital Marketing | 6-8 years | Rs 15 - 30 LPA |
| VP Marketing | 8-12 years | Rs 25 - 60 LPA |
| Freelancer (Starting) | 0-1 year | Rs 15,000 - 50,000/month |
| Freelancer (Established) | 2-4 years | Rs 50,000 - 2,00,000/month |
| Freelancer (Expert) | 4+ years | Rs 2,00,000 - 5,00,000+/month |

**City-wise salary multiplier:**
- Mumbai/Bangalore/Gurugram: 1.3x - 1.5x
- Pune/Hyderabad/Chennai/Noida: 1.0x - 1.2x
- Bhopal/Jaipur/Lucknow/Indore: 0.7x - 0.9x (but lower cost of living)
- Remote work: Earning Tier-1 salaries from Tier-2 cities (growing trend)

#### Salary Negotiation Tips:

1. **Research first** — Know the market rate (Glassdoor, AmbitionBox, Naukri salary tool)
2. **Never give first number** — "What's the budget for this role?"
3. **If forced to give range** — Quote 15-20% above your minimum acceptable
4. **Negotiate total compensation** — Not just salary: joining bonus, learning budget, WFH days, health insurance
5. **Use competing offers** — Having 2+ offers gives leverage
6. **Highlight value** — "In my internship, I generated 150 leads/month. That's Rs X value to the company."
7. **Get it in writing** — Verbal offers mean nothing

> **Try This:** Research the salary for "Digital Marketing Executive" in your city on Glassdoor and AmbitionBox. What's the median? What's the top 25%? What skills command the highest premium?

---

### Self-Check Questions: Week 29

1. What are 10 rules for making a resume ATS-friendly?
2. What should your LinkedIn headline say? (Write one for yourself)
3. Use the STAR method to answer: "Tell me about a time you improved a marketing metric."
4. How would you respond to: "Why should we hire you over someone with 2 years experience?"
5. What is the average starting salary for a Digital Marketing Executive in a Tier-2 city in India?
6. Name 3 things you can negotiate beyond base salary.

---

## Week 30: Capstone & Placement

### Day 165-170: Industry Capstone Build (7 Days)

**The capstone project combines EVERYTHING you learned in 6 months.**

#### Capstone Requirements:

Choose ONE of these options:

**Option A: Full Digital Marketing Setup for a Real Business**
- Audit current digital presence
- Strategy document (10+ pages)
- Implement: Website/landing page, social profiles, Google Business, GA4, email system
- Run for 2 weeks with real results
- Present results with data

**Option B: Personal Brand Launch**
- Portfolio website live (with 5+ case studies)
- LinkedIn fully optimized with 1,000+ connections
- 3 freelance profiles active (Fiverr, Upwork, LinkedIn)
- 5 cold pitches sent with responses documented
- Content published (5+ LinkedIn posts, 2+ blog posts)

**Option C: Campaign Challenge**
- Run a full marketing campaign for TechPath Academy (or partner business)
- Budget: Rs 5,000 ad spend (provided)
- Goal: Maximum leads at lowest cost
- Track everything in GA4
- Present: Strategy, execution, results, learnings

#### Capstone Deliverables:
1. Strategy document
2. Implementation evidence (screenshots, links, access)
3. Results dashboard (Looker Studio or manual)
4. 10-minute presentation (recorded video OR live)
5. Reflection document (what worked, what didn't, what you'd do differently)

---

### Day 171-175: Demo Day, Applications & Freelancing

#### Building Your Freelance Career:

**Platform Setup Priority:**
1. **Week 1:** Fiverr (easiest to get started, make 3 gigs)
2. **Week 2:** Upwork (better quality clients, takes longer)
3. **Week 3:** LinkedIn Services (highest value, needs network)
4. **Ongoing:** Build direct client pipeline (best margins, no commission)

**Getting First Clients Faster:**
- Price 30% below market initially (build reviews fast)
- Offer 1-2 free/discounted projects to get testimonials
- Deliver 120% — over-deliver on first 5 clients
- Ask every happy client for a review AND referral
- Niche down — "Instagram marketing for restaurants in Pune" beats "digital marketing"

#### Cold Outreach Template:

```
Subject: Quick idea to get [Business Name] more [leads/followers/sales]

Hi [Name],

I noticed [something specific about their business — shows you did research].

I help [type of business] get [specific result] through [your service].

For example, [brief result you achieved for similar business].

Would you be open to a quick 15-minute call this week to discuss how I could help [Business Name] [specific benefit]?

No pressure either way.

Best,
[Your Name]
[Your LinkedIn/portfolio link]
```

> **Try This:** Send 3 cold outreach messages today to businesses you can genuinely help. Use the template above but personalize each one. Track responses.

---

### Self-Check Questions: Week 30 (Final)

1. What are the 3 capstone options? Which would you choose and why?
2. What's the most important thing to do in your first week as a freelancer?
3. Write a cold outreach message to a restaurant that has 500 Instagram followers and no Google Business Profile.
4. If you had to earn Rs 30,000/month from freelancing starting today, what 2 services would you offer and at what price?
5. What were the 3 most valuable things you learned in this entire 6-month program?
