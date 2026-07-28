# Search Engines & Keyword Research

**Module 03 — SEO Deep Dive | Topic 1**

---

## How Google Works — The 3-Step Process

Every time you search on Google, three things have already happened behind the scenes: **Crawling**, **Indexing**, and **Ranking**. Understanding this process is the foundation of all SEO work.

### Step 1: Crawling

Google sends out automated programs called **spiders** or **bots** (the main one is called **Googlebot**) to discover web pages.

- Googlebot follows links from page to page, just like you clicking links
- It reads the HTML code, text, images, and structure of every page it finds
- Google does not crawl every page every day — it has a **crawl budget** for each website

| Term | What It Means | Why It Matters |
|------|---------------|----------------|
| **Googlebot** | Google's web crawler that visits pages | If Googlebot cannot access your page, it will never appear in search |
| **Spider / Bot** | Another name for web crawlers | All search engines have their own bots (Bingbot, Yandex Bot, etc.) |
| **Crawl Budget** | Number of pages Google will crawl on your site in a given time | Large sites (10,000+ pages) need to use crawl budget wisely |
| **Crawl Rate** | How fast Googlebot fetches pages | Too fast can slow your server; too slow means delayed indexing |

> **Real Example:** Think of Googlebot as a Zomato delivery person exploring every lane in a city. They cannot visit every restaurant every hour, so they prioritise popular ones and revisit frequently.

### Step 2: Indexing

After crawling, Google stores the page content in its massive database called the **index**.

- Google analyses the page to understand its topic, keywords, and freshness
- Not every crawled page gets indexed — thin, duplicate, or low-quality pages may be skipped
- You can check your indexing status in Google Search Console using the URL Inspection tool

### Step 3: Ranking

When a user types a query, Google searches its index and **ranks** results based on 200+ factors.

- The goal is to show the most relevant, useful, and trustworthy result first
- Rankings change constantly as Google updates its algorithms

> **Simple Analogy:** Google is like a massive library. Crawling = librarian discovering new books. Indexing = filing books by topic on the right shelf. Ranking = recommending the best book when a student asks a question.

---

## Google's Top 10 Ranking Factors

Google uses 200+ signals, but these carry the most weight:

| # | Factor | What It Means | How to Optimise |
|---|--------|---------------|-----------------|
| 1 | **Content Quality** | Helpful, original, in-depth content | Write comprehensive content that answers user intent completely |
| 2 | **Backlinks** | Other websites linking to you | Earn links from relevant, authoritative websites |
| 3 | **Search Intent Match** | Your page matches what the user actually wants | Study the SERP before writing — match the format and depth |
| 4 | **E-E-A-T** | Experience, Expertise, Authoritativeness, Trustworthiness | Show credentials, cite sources, use author bios |
| 5 | **Page Experience** | Fast, mobile-friendly, secure pages | Optimise Core Web Vitals, use HTTPS |
| 6 | **Keyword Usage** | Target keyword in title, headings, and body | Place primary keyword in title tag, H1, first 100 words |
| 7 | **Freshness** | Recently updated content | Refresh old posts with current stats and examples |
| 8 | **Mobile-Friendliness** | Works well on phones | Use responsive design, large tap targets |
| 9 | **HTTPS Security** | Site uses SSL certificate | Install free SSL via Let's Encrypt |
| 10 | **Internal Linking** | Pages link to each other logically | Create hub-spoke content clusters |

---

## What is a Keyword?

A **keyword** is the word or phrase a user types into a search engine. In SEO, keywords are the bridge between what people search for and the content you provide.

- Single word: "marketing"
- Short phrase: "digital marketing"
- Long phrase: "digital marketing course in Varanasi for beginners"

> **Pro Tip:** You are not trying to rank for a keyword — you are trying to rank for the **intent** behind that keyword.

---

## Types of Keywords by Search Intent

Every search has a reason behind it. Understanding intent helps you create the right type of content.

| Intent Type | What the User Wants | Example Keywords | Best Content Format |
|-------------|--------------------|-----------------|--------------------|
| **Informational** | Learn something, get an answer | "what is SEO", "how to cook biryani" | Blog post, guide, video, infographic |
| **Navigational** | Find a specific website or brand | "TechPath Academy login", "Amazon India" | Homepage, login page, brand page |
| **Commercial** | Compare options before buying | "best laptops under ₹50,000", "Byjus vs Unacademy" | Comparison post, review, listicle |
| **Transactional** | Buy, sign up, or take action | "buy iPhone 16 online", "enroll digital marketing course" | Product page, pricing page, sign-up form |

> **Real Example:** If someone searches "protein powder" (informational), they want to learn. If they search "best protein powder in India" (commercial), they are comparing. If they search "buy MuscleBlaze protein 2kg" (transactional), they are ready to purchase. Your page must match the intent — a blog post will not rank for a transactional keyword.

---

## Long-Tail vs Short-Tail Keywords

| Feature | Short-Tail | Long-Tail |
|---------|-----------|-----------|
| **Length** | 1-2 words | 3+ words |
| **Example** | "digital marketing" | "digital marketing course in Varanasi with placement" |
| **Monthly Volume** | Very high (50,000+) | Lower (100-2,000) |
| **Competition** | Extremely high | Low to medium |
| **Conversion Rate** | Low (broad intent) | High (specific intent) |
| **Best For** | Brand awareness, large sites | New websites, targeted traffic, local businesses |

> **Fun Fact:** About 70% of all Google searches are long-tail keywords. A small coaching class in Lucknow will never rank for "digital marketing" but can easily rank for "digital marketing course near Hazratganj Lucknow fees."

**Strategy for Indian businesses:** Start with long-tail keywords that include your city name, service type, and a qualifier (fees, near me, best, for beginners). As your site gains authority, target shorter keywords.

---

## Keyword Research Tools

| Tool | Free / Paid | Best For |
|------|------------|----------|
| **Google Keyword Planner** | Free (needs Google Ads account) | Finding volume and CPC data for Indian keywords |
| **Ubersuggest** | Free (3 searches/day) | Beginners, keyword ideas + difficulty score |
| **Google Trends** | Free | Comparing keyword popularity over time and by region |
| **Google Autocomplete** | Free | Finding what real users are searching |
| **People Also Ask** | Free (in Google SERP) | Finding related questions to answer |
| **Ahrefs** | Paid (from $99/month) | Competitor keyword analysis, backlink data |
| **SEMrush** | Paid (from $119/month) | Full SEO suite, keyword gap analysis |
| **AnswerThePublic** | Free (limited) | Finding question-based keywords |

---

## How to Evaluate a Keyword

Before targeting any keyword, check these four metrics:

| Metric | What It Tells You | What to Look For |
|--------|-------------------|-----------------|
| **Search Volume** | How many people search this per month | 100-10,000 is ideal for new sites. Below 100 = not enough traffic. Above 50,000 = too competitive for beginners |
| **Keyword Difficulty (KD)** | How hard it is to rank on page 1 (scale 0-100) | Target KD below 30 for new websites |
| **CPC (Cost Per Click)** | What advertisers pay per click in Google Ads | High CPC = high commercial value (people are willing to spend money) |
| **Trend** | Is the keyword growing, stable, or declining? | Use Google Trends to check. Avoid declining keywords |

> **Pro Tip:** A keyword with low volume (500/month) but high CPC (₹80+) often converts better than a keyword with high volume (20,000/month) but low CPC (₹5). CPC indicates commercial intent.

---

## Step-by-Step Keyword Research Process

Here is a practical process for finding keywords for a local Indian business. Let us use the example of a **coaching class in Varanasi** that teaches spoken English.

### Step 1: Brainstorm Seed Keywords (5-10 broad terms)

- spoken English
- English speaking course
- English coaching
- learn English
- English class Varanasi

### Step 2: Expand Using Tools

Open Google Keyword Planner and type each seed keyword. Note every relevant suggestion:

| Seed Keyword | Tool Suggestions |
|-------------|-----------------|
| spoken English | spoken English course, spoken English classes near me, English speaking practice |
| English coaching Varanasi | English coaching class in Varanasi fees, best English institute Varanasi, IELTS coaching Varanasi |

Also check Google Autocomplete — start typing your seed keyword and note what Google suggests.

### Step 3: Filter and Group by Intent

Remove irrelevant keywords (e.g., "English movie download") and group the rest:

- **Informational:** how to improve spoken English, English grammar rules
- **Commercial:** best English coaching in Varanasi, spoken English course fees
- **Transactional:** enroll English speaking course Varanasi, join English class online

### Step 4: Prioritise Using the 3-Filter Rule

For each keyword, check: Volume > 100 AND KD < 30 AND intent matches your page type.

| Keyword | Volume | KD | CPC | Intent | Priority |
|---------|--------|-----|-----|--------|----------|
| spoken English course in Varanasi | 320 | 12 | ₹45 | Commercial | High |
| best English coaching Varanasi fees | 210 | 8 | ₹62 | Commercial | High |
| how to improve spoken English | 12,000 | 52 | ₹15 | Informational | Low (too competitive) |
| English speaking practice online free | 8,500 | 44 | ₹8 | Informational | Low |

### Step 5: Map Keywords to Pages

Assign each priority keyword to a specific page on your website:

| Keyword | Assigned Page |
|---------|--------------|
| spoken English course in Varanasi | /courses/spoken-english/ |
| best English coaching Varanasi fees | /courses/spoken-english/ (secondary keyword) |
| IELTS coaching Varanasi | /courses/ielts-preparation/ |
| how to improve English speaking | /blog/tips-improve-spoken-english/ |

> **Important Rule:** One page = one primary keyword. Never target the same keyword on two different pages (this is called **keyword cannibalisation** and confuses Google).

---

## Trainer Activity: Find 10 Keywords for a Coaching Class in Varanasi

> **Class Exercise (20 minutes)**
>
> **Scenario:** You are the digital marketer for "Sunrise English Academy" in Varanasi. They teach spoken English, IELTS preparation, and personality development.
>
> **Steps:**
> 1. Open Google Keyword Planner (or Ubersuggest free version)
> 2. Enter 3 seed keywords related to the business
> 3. Find 10 relevant long-tail keywords
> 4. For each keyword, note: Volume, KD, CPC, and Intent type
> 5. Fill in this table on the board:
>
> | # | Keyword | Volume | KD | CPC (₹) | Intent |
> |---|---------|--------|-----|---------|--------|
> | 1 | | | | | |
> | 2 | | | | | |
> | ... | | | | | |
> | 10 | | | | | |
>
> **Bonus:** Which 3 keywords would you target first and why?

---

## Summary

- Google works in three steps: **Crawling** (Googlebot discovers pages) then **Indexing** (stores in database) then **Ranking** (shows best results)
- Google uses 200+ ranking factors — content quality, backlinks, and search intent match are the top three
- Keywords are the words users type into search engines — they are your SEO targets
- Four types of keyword intent: **Informational**, **Navigational**, **Commercial**, **Transactional**
- Long-tail keywords (3+ words) are easier to rank for and convert better than short-tail keywords
- Always evaluate keywords by Volume, KD, CPC, and Trend before targeting them
- Map one primary keyword to one page — never target the same keyword on multiple pages
- For Indian local businesses, add city name and qualifiers (fees, best, near me) to keywords
