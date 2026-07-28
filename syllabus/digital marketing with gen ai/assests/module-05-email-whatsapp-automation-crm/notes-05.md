# Module 5: Email, WhatsApp, Marketing Automation & CRM

---

## Week 21: Email Marketing in 2026

### Day 115: Email Marketing in 2026 — Why Email Still Wins

#### Email vs Social Media ROI Comparison

| Channel | Average ROI | Cost Per Lead | Best For |
|---------|------------|---------------|----------|
| Email Marketing | Rs 36 for every Rs 1 spent | Rs 50-150 | Nurturing, retention, direct sales |
| Social Media (Organic) | Rs 5 for every Rs 1 spent | Rs 200-500 | Brand awareness, community |
| Social Media (Paid) | Rs 8 for every Rs 1 spent | Rs 100-300 | Lead generation, reach |
| WhatsApp Marketing | Rs 25 for every Rs 1 spent | Rs 30-80 | Engagement, support, India market |
| SMS Marketing | Rs 15 for every Rs 1 spent | Rs 20-60 | Alerts, OTPs, flash sales |

**Why email still wins in 2026:**
- You OWN your email list (no algorithm changes can take your audience away)
- Direct inbox access — no "pay to reach" model like social media
- Works for every business size — from chai shop to enterprise company
- Highest ROI of any digital channel for Indian businesses
- 4.5 billion email users worldwide (compared to 2 billion on Instagram)
- Email is the backbone of all marketing automation

**Email Marketing in India — Key Stats:**
- 750+ million internet users in India (2026)
- Average Indian professional checks email 3-4 times per day
- Mobile email opens: 65% in India (design for mobile first!)
- Best performing industries: E-commerce, EdTech, Finance, SaaS
- Hindi/regional language emails growing 40% YoY

#### Email Authentication: DKIM, SPF, and DMARC Explained Simply

Think of email authentication like Aadhaar verification for your emails. It proves YOU sent the email, not a scammer.

**Why this matters:** In 2024, Google and Yahoo made email authentication MANDATORY. If you don't have SPF, DKIM, and DMARC set up, your emails will go to spam. No exceptions.

##### SPF (Sender Policy Framework)
**What it does:** Tells the world which servers are allowed to send emails on behalf of your domain.

**Simple analogy:** Like a visitor list at a gated society — only people on the list can enter.

**How it works:**
1. You add a TXT record to your domain's DNS
2. When someone receives your email, their server checks: "Is this sender's IP on the allowed list?"
3. If yes — email passes. If no — flagged as suspicious.

**Example SPF Record:**
```
v=spf1 include:_spf.google.com include:mailerlite.com ~all
```
This says: "Only Google and MailerLite can send emails for my domain."

**Breaking it down:**
- `v=spf1` — Version of SPF (always spf1)
- `include:_spf.google.com` — Allow Google servers
- `include:mailerlite.com` — Allow MailerLite servers
- `~all` — Soft fail for everything else (mark as suspicious but don't reject)
- `-all` would be hard fail (reject everything else — stricter)

##### DKIM (DomainKeys Identified Mail)
**What it does:** Adds a digital signature to your emails proving they weren't tampered with in transit.

**Simple analogy:** Like a sealed envelope with a wax stamp — if someone opens and changes the letter, the seal breaks.

**How it works:**
1. Your email server signs each email with a private key
2. A matching public key is published in your DNS
3. Receiving server uses the public key to verify the signature matches

**Example DKIM Record:**
```
selector._domainkey.yourdomain.com → v=DKIM1; k=rsa; p=MIGfMA0GCS...
```

##### DMARC (Domain-based Message Authentication, Reporting & Conformance)
**What it does:** Tells receiving servers what to do when SPF or DKIM checks fail.

**Simple analogy:** Like instructions to the security guard: "If someone doesn't have proper ID, reject them / quarantine them / let them in but note it."

**DMARC Policies:**
- `p=none` — Monitor only, don't take action (start here for 2 weeks)
- `p=quarantine` — Send to spam folder
- `p=reject` — Block the email completely (strongest protection)

**Example DMARC Record:**
```
v=DMARC1; p=quarantine; rua=mailto:reports@yourdomain.com; pct=100
```

##### Setup Order (Must Follow This Sequence):
1. **First** set up SPF (takes 5 minutes)
2. **Then** set up DKIM (takes 10 minutes, ESP provides the key)
3. **Finally** enable DMARC (start with `p=none` for 2 weeks, monitor reports, then move to `quarantine`)

##### How to Check Your Email Authentication:
- Send a test email to mail-tester.com — it gives you a score out of 10
- Use mxtoolbox.com to check DNS records
- Google Postmaster Tools shows delivery issues

> **Try This:** Go to mail-tester.com. Send an email from your Gmail to the address shown. Check your score. What authentication issues does it find?

---

### Day 116: ESP Comparison — Choosing the Right Email Tool

#### ESP (Email Service Provider) Detailed Comparison

| Feature | MailerLite | Brevo (Sendinblue) | Mailchimp | ConvertKit | Klaviyo | ActiveCampaign |
|---------|-----------|-------------------|-----------|------------|---------|----------------|
| **Free Tier** | 1,000 subscribers, 12,000 emails/month | 300 emails/day (unlimited contacts) | 500 contacts, 1,000 emails/month | 1,000 subscribers | 250 contacts | 14-day trial only |
| **Paid Starting** | Rs 750/month | Rs 650/month | Rs 900/month | Rs 2,400/month | Rs 1,700/month | Rs 2,500/month |
| **Best For** | Beginners, small business | Transactional + marketing | E-commerce | Creators, bloggers | E-commerce (advanced) | Advanced automation |
| **Automation** | Good (visual builder) | Good (workflows) | Basic (journeys) | Good (visual) | Advanced (flows) | Best-in-class |
| **Templates** | 90+ drag-and-drop | 40+ | 100+ | Minimal (text-focused) | 80+ | 125+ |
| **Landing Pages** | Yes (free) | Yes (free) | Yes (paid plans) | Yes (free) | Yes | Yes |
| **A/B Testing** | Subject + content | Subject + send time | Subject only (free) | Subject | Everything | Everything |
| **Segmentation** | Good | Good | Good | Good | Advanced | Advanced |
| **India Pricing** | Affordable | Most affordable | Expensive | Mid-range | Expensive | Expensive |
| **Deliverability** | Excellent | Good | Good | Excellent | Excellent | Excellent |
| **Learning Curve** | Easy (1-2 days) | Easy (1-2 days) | Medium (3-5 days) | Easy (1-2 days) | Hard (1-2 weeks) | Hard (1-2 weeks) |
| **WhatsApp** | No | Yes (built-in) | No | No | No | SMS only |
| **SMS** | No | Yes (built-in) | Yes (paid add-on) | No | Yes | Yes |
| **Customer Support** | Email + Chat | Email + Phone | Email (paid: chat) | Email + Chat | Email + Chat | Email + Chat + Phone |

#### Decision Framework — Which ESP Should You Choose?

**For Indian Businesses Starting Out:**
```
Just starting, need free → MailerLite
Need email + SMS + WhatsApp → Brevo
E-commerce on Shopify → Klaviyo (if budget allows) or MailerLite
Creator/Coach → ConvertKit
Need complex automation → ActiveCampaign
Agency managing clients → ActiveCampaign or MailerLite (cheaper per client)
```

#### Step-by-Step: Setting Up MailerLite (Recommended for Beginners)

1. Go to mailerlite.com → Click "Sign Up Free"
2. Enter email, password, accept terms
3. **Account Setup:**
   - Company name: Your business name
   - Industry: Select yours
   - Subscribers: "Under 1,000" (for new accounts)
   - How will you collect: "Website forms, lead magnets"
4. **Verify email** — Click the link sent to your inbox
5. **Add sending domain:**
   - Settings → Domains → Add domain
   - Follow DNS setup instructions (add SPF and DKIM records)
   - Verification takes 24-48 hours
6. **You're ready!** Create your first form and automation

> **Try This:** Sign up for MailerLite's free plan right now. Complete the account setup. Navigate through every section in the left sidebar (Subscribers, Campaigns, Automation, Forms, Sites) to familiarize yourself with the interface.

---

### Day 117: List Building & Lead Magnets

#### What is a Lead Magnet?
Something valuable you give away FREE in exchange for an email address. The better the lead magnet, the higher your conversion rate.

#### Types of Lead Magnets That Work in India

| Type | Example | Best For | Conversion Rate |
|------|---------|----------|-----------------|
| PDF Guide | "50 Free Marketing Tools for Indian Startups" | B2B, coaches | 20-30% |
| Checklist | "Complete GST Filing Checklist" | Service businesses | 25-35% |
| Template | "Instagram Content Calendar Template" | Freelancers, agencies | 30-40% |
| Free Tool/Calculator | "EMI Calculator" or "GST Calculator" | Finance, SaaS | 35-50% |
| Mini Course | "5-Day Instagram Reels Challenge" | Coaches, educators | 15-25% |
| Webinar | "How to Get Your First 1000 Followers" | Coaches, SaaS | 10-20% |
| Discount Code | "Get 15% Off Your First Order" | E-commerce | 40-60% |
| Quiz | "What Type of Entrepreneur Are You?" | Coaches, personal brands | 30-45% |
| Case Study | "How We Got 10,000 Leads in 30 Days" | Agencies, SaaS | 15-25% |
| Toolkit | "Complete Digital Marketing Starter Kit" | Education, agencies | 20-30% |
| Swipe File | "100 High-Converting Email Subject Lines" | Marketers | 25-35% |
| Resource List | "Top 20 Free Tools for Instagram Growth" | General audience | 20-30% |

#### Lead Magnet Formula
A great lead magnet is:
- **Specific** — Solves ONE clear problem (not "everything about marketing")
- **Quick Win** — Gives results in under 10 minutes of reading
- **High Perceived Value** — Looks like it should cost money
- **Easy to Consume** — Not a 100-page ebook nobody reads (5-10 pages max)
- **Relevant** — Directly related to what you sell (qualifies the lead)
- **Actionable** — Reader can DO something immediately after reading

#### Opt-in Form Best Practices

**Form Placement (where to put it):**
1. Above the fold on landing page (most important)
2. Exit-intent popup (fires when mouse moves to close tab)
3. Within blog posts (after the introduction paragraph)
4. Sticky footer bar
5. Sidebar widget
6. End of blog post
7. Between content sections (inline)

**Form Design Rules:**
1. Keep it to 2-3 fields max (Name + Email, or just Email)
2. Clear headline stating the benefit — NOT "Subscribe to our newsletter"
3. Show what they're getting (mockup of the PDF/template)
4. Use contrasting CTA button color (orange on blue, green on white)
5. Add social proof ("Join 5,000+ marketers")
6. Reduce friction — "No spam. Unsubscribe anytime."
7. Mobile-first design — buttons must be thumb-friendly

#### List Building Strategies (Free Methods)

| Strategy | How to Do It | Expected Results |
|----------|-------------|-----------------|
| Blog + Content Upgrade | Write blog post, offer related PDF within it | 5-15% of readers opt in |
| Instagram Bio Link | Link to landing page with lead magnet | 2-5 subscribers/day |
| WhatsApp Status/Group | Share lead magnet link in status | 10-30 subscribers/post |
| YouTube Description | "Download my free template — link below" | 1-3% of viewers |
| Guest Posting | Write for other blogs, link to your lead magnet | 50-200 per guest post |
| Quora/Reddit Answers | Answer questions, link to relevant resource | 5-20/day if consistent |
| Webinar/Workshop | Free workshop, collect emails at registration | 100-500 per event |
| Referral | "Share with a friend, both get bonus" | 10-20% viral growth |

> **Try This:** Create a lead magnet idea for a business you want to start (or for TechPath Academy). Write down: (1) the title, (2) what's inside (5 bullet points), (3) who it's for, (4) what problem it solves. Bonus: Actually create it using Canva or Google Docs.

---

### Day 118: Email Design & Copywriting

#### Email Design Principles

**The F-Pattern:** People scan emails in an F-shape — left to right at the top, then down the left side. Put your most important content in the top-left.

**Mobile-First Design (65% of Indians open email on phone):**
- Single column layout (600px max width)
- Font size: minimum 14px body, 22px headings
- Buttons: minimum 44x44px tap target
- Images: max-width: 100% (responsive)
- Preheader text: always fill it (shown in inbox preview)

**Email Types and Their Design:**

| Email Type | Design Approach | Length |
|-----------|----------------|--------|
| Welcome | Branded, personal, simple | 150-200 words |
| Newsletter | Multi-section, scannable | 300-500 words |
| Promotional | Hero image, clear CTA | 100-150 words |
| Transactional | Minimal, informational | 50-100 words |
| Re-engagement | Emotional, compelling | 100-150 words |

#### Email Copywriting Framework: AIDA

- **A**ttention → Subject line (gets them to open)
- **I**nterest → First line (gets them to keep reading)
- **D**esire → Body (makes them want what you offer)
- **A**ction → CTA (tells them exactly what to do next)

#### Subject Line Formulas

| Formula | Example | When to Use |
|---------|---------|-------------|
| Number + Benefit | "7 tools that save 5 hours/week" | Educational content |
| How to + Result | "How to get 1000 followers in 30 days" | Tutorial content |
| Question | "Are you making this SEO mistake?" | Problem-aware audience |
| Curiosity Gap | "I can't believe this actually worked" | Engaged audience |
| Urgency | "24 hours left — Rs 5000 off" | Sales, limited offers |
| Personal | "Rahul, your weekly report is ready" | Personalized content |
| Social Proof | "Why 10,000+ marketers read this" | Authority building |
| Contrarian | "Stop posting on Instagram (do this instead)" | Attention-grabbing |

**Subject Line Rules:**
- Under 50 characters (mobile-safe: under 35)
- Don't use ALL CAPS or excessive !!!
- Avoid spam words: FREE, URGENT, ACT NOW, LIMITED TIME, CLICK HERE
- Use numbers (odd numbers perform better — 7 not 6)
- Add emoji sparingly (test — 1 max, at the beginning or end)
- A/B test EVERY campaign (test 2 subject lines minimum)

#### CTA (Call to Action) Best Practices
- Use action verbs: "Download Now", "Start Free Trial", "Get My Discount"
- Be specific: "Download the Free Template" not "Click Here"
- One primary CTA per email (don't confuse with multiple options)
- Button > text link (3x higher click rate)
- Contrasting color button
- Above the fold for promotional emails
- Repeat CTA at the end for longer emails

> **Try This:** Write 5 different subject lines for this scenario: You're sending an email to 500 subscribers announcing a free webinar on "How to Start Freelancing in Digital Marketing." Use 5 different formulas from the table above.

---

### Day 119: Email Sequences & Drip Campaigns

#### What is a Drip Campaign?
A series of pre-written emails sent automatically based on a trigger (sign-up, purchase, behavior) on a scheduled timeline.

#### 7-Email Welcome Sequence Template

This is the most important email automation. 60-70% of your total email revenue comes from automated sequences, not one-off campaigns.

##### Email 1: Welcome + Deliver Lead Magnet (Send immediately)
**Subject:** Here's your [Lead Magnet Name] (+ a quick hello)
**Purpose:** Deliver what you promised, set expectations
**Content Structure:**
- Thank them for joining (1 line)
- Deliver the lead magnet (download link/button)
- Brief intro of who you are (2-3 lines)
- Tell them what to expect (how often you'll email, what topics)
- Ask them to whitelist your email (reply or add to contacts)
- PS: One sentence teasing next email

##### Email 2: Your Story + Value (Day 1)
**Subject:** How I went from [Before] to [After]
**Purpose:** Build connection and trust
**Content Structure:**
- Share your story or brand story (relatable, human)
- Connect to their pain point ("I know what it's like to...")
- Show the transformation
- End with one helpful tip they can use today

##### Email 3: Quick Win / Best Content (Day 3)
**Subject:** The #1 mistake [audience] makes with [topic]
**Purpose:** Provide immediate value — make them glad they subscribed
**Content Structure:**
- Identify a common mistake
- Explain why it matters
- Give the solution (actionable tip)
- They should be able to get a result TODAY from this email

##### Email 4: Social Proof / Case Study (Day 5)
**Subject:** How [Name] achieved [Result] in [Timeframe]
**Purpose:** Build credibility through others' results
**Content Structure:**
- Introduce the person (name, context, challenge)
- What they did (brief steps)
- The result (specific numbers)
- Relate it back to the reader ("You can do this too because...")

##### Email 5: Address Objections (Day 7)
**Subject:** "But will this work for me?"
**Purpose:** Handle common objections before they become blockers
**Content Structure:**
- "I hear this a lot..." (acknowledge their doubts)
- List 3-4 common objections
- Address each one honestly (don't be salesy)
- More social proof from different types of people

##### Email 6: Soft Pitch (Day 9)
**Subject:** I made something for people like you
**Purpose:** Introduce your product/service naturally
**Content Structure:**
- Recap value you've provided ("Over the past week, you learned...")
- Transition: "Some of you asked how to go deeper..."
- Introduce your paid offering naturally
- Explain who it's for AND who it's NOT for
- Benefits (not features)
- Low-pressure CTA — "Learn more" not "Buy now"

##### Email 7: Direct Offer + Urgency (Day 11)
**Subject:** Last chance: [Offer details]
**Purpose:** Convert interested readers with a deadline
**Content Structure:**
- Remind them of the problem (1-2 lines)
- Present the complete offer clearly
- Add urgency (limited time, limited spots, price going up)
- Include 2-3 testimonials
- Strong CTA with clear next step
- PS with additional incentive ("PS: First 20 buyers also get...")

#### Other Important Email Sequences:

**Cart Abandonment (E-commerce):**
- Email 1 (1 hour): "You forgot something" + product image
- Email 2 (24 hours): Social proof + reminder
- Email 3 (48 hours): Offer discount (5-10% off)

**Post-Purchase:**
- Email 1 (Immediately): Order confirmation + thank you
- Email 2 (Day 3): "How to get the most from your purchase"
- Email 3 (Day 7): Ask for review
- Email 4 (Day 14): Cross-sell related products

**Re-engagement (Win-back):**
- Email 1: "We miss you" + what's new
- Email 2: "Is this goodbye?" + special offer
- Email 3: "Last email from us" (unless they click to stay)

> **Try This:** Write Email 1 and Email 6 of a welcome sequence for a hypothetical online course platform called "SkillBridge" that teaches coding to beginners in India. Include: subject line, preview text, full body copy, and CTA button text.

---

### Day 120: Segmentation & Personalization

#### Segmentation Types

##### 1. Demographic Segmentation
- Age group (18-24, 25-34, 35-44, etc.)
- Gender
- Location (city/state — Mumbai vs Tier-2 cities)
- Job title / Industry
- Income level
- Language preference (English/Hindi/Regional)

##### 2. Behavioral Segmentation
- Purchase history (first-time buyer, repeat customer, VIP)
- Website activity (pages visited, time spent, features used)
- Email engagement (opens, clicks, inactive for 30/60/90 days)
- Product interest (based on clicks/views/cart additions)
- Cart abandonment (left items in cart)
- Content consumed (which blogs/videos they watched)

##### 3. Engagement-Based Segmentation
| Segment | Definition | Strategy |
|---------|-----------|----------|
| Highly Engaged | Opens 80%+ of emails, clicks regularly | Send more often, early access, loyalty perks |
| Moderately Engaged | Opens 30-70%, occasional clicks | Standard frequency, relevant content |
| Low Engagement | Opens less than 30%, rarely clicks | Re-engagement campaign, reduce frequency |
| Inactive | No opens in 90+ days | Win-back series (3 emails), then remove from list |

##### 4. Lifecycle Stage Segmentation
| Stage | Who They Are | What to Send |
|-------|-------------|-------------|
| New subscriber | Just joined, curious | Welcome sequence, education |
| Lead | Showed interest, downloaded content | Case studies, webinars, demos |
| Customer | Made first purchase | Onboarding, tips, cross-sell |
| Repeat customer | 2+ purchases | Loyalty perks, early access, referral ask |
| Advocate | Refers others, leaves reviews | VIP treatment, ambassador program |
| At-risk | Hasn't purchased in X days | Win-back offer, feedback request |

#### Personalization Techniques

| Level | What It Is | Example |
|-------|-----------|---------|
| Basic | Name in subject/body | "Hi Rahul, here's your weekly report" |
| Behavioral | Based on actions | "Still thinking about the SEO course? Here's what others said" |
| Dynamic Content | Different content blocks per segment | VIP customers see exclusive offer, others see standard |
| Predictive | AI-suggested content/products | "Based on your history, you might like..." |
| Location-based | City/weather triggers | "It's raining in Mumbai — perfect day for our indoor workshop" |

> **Try This:** You have a list of 5,000 subscribers for an online store selling fitness equipment. Create 4 segments and write a 1-sentence email strategy for each segment. What would you send each group and why?

---

### Day 121: A/B Testing & Email Analytics

#### A/B Testing Methodology

**What to Test (in priority order):**
1. **Subject lines** — Biggest impact on open rates
2. **Send time** — When your audience is most active
3. **CTA button** — Color, text, placement
4. **From name** — Brand name vs person's name vs both
5. **Email length** — Short vs long
6. **Personalization** — Name in subject vs no name
7. **Content format** — Text-only vs designed template
8. **Offer type** — Percentage off vs rupee amount off

#### A/B Testing Rules (Must Follow):
1. Test **ONE** variable at a time (otherwise you can't know what worked)
2. Minimum sample size: 1,000 subscribers per variation
3. Run test for at least 4 hours before picking winner (24 hours is better)
4. Statistical significance: Wait for 95% confidence
5. Document every test and result in a spreadsheet
6. Winner becomes the new control (test against it next time)
7. Don't stop testing — what works now may not work in 3 months

#### Email Metrics Deep Dive

| Metric | Formula | Good Benchmark (India) | What It Tells You |
|--------|---------|----------------------|-------------------|
| Open Rate | Opens / Delivered x 100 | 18-25% | Subject line + sender reputation |
| Click-Through Rate (CTR) | Clicks / Delivered x 100 | 2-5% | Content + CTA relevance |
| Click-to-Open Rate (CTOR) | Clicks / Opens x 100 | 10-20% | Content quality (among those who opened) |
| Unsubscribe Rate | Unsubscribes / Delivered x 100 | Below 0.5% | List quality + content relevance |
| Bounce Rate | Bounces / Sent x 100 | Below 2% | List hygiene |
| Spam Complaint Rate | Complaints / Delivered x 100 | Below 0.1% | Permission + expectations |
| Conversion Rate | Conversions / Clicks x 100 | 1-5% | Landing page + offer quality |
| Revenue Per Email | Total Revenue / Emails Sent | Varies | Overall email program health |

#### How to Read Your Email Dashboard:

**High opens, low clicks:** Subject line is good, but content/CTA doesn't match expectations. Fix: Better content alignment with subject promise.

**Low opens, high clicks (among openers):** Content is great but subject line is weak. Fix: Better subject lines.

**High unsubscribes after a specific email:** That email didn't meet expectations. Fix: Review what changed.

**Declining open rates over time:** List fatigue or deliverability issue. Fix: Clean list, re-engage inactive, warm up sending domain.

> **Try This:** Set up an A/B test plan for your next email campaign. Write two subject lines you would test. Predict which will win and why. After sending (if using a real tool), compare your prediction with actual results.

---

### Day 122: Email Deliverability

#### What is Deliverability?
The ability to land in the inbox (not spam, not promotions tab, not bounced). Even with perfect content, if emails don't reach the inbox, nothing else matters.

#### Deliverability Factors (What Gmail/Yahoo Look At):

| Factor | Weight | How to Optimize |
|--------|--------|----------------|
| Authentication (SPF/DKIM/DMARC) | Critical | Set up all three correctly |
| Sender Reputation | Very High | Maintain low bounces, complaints |
| Engagement | High | Send to engaged subscribers, remove inactive |
| Content Quality | Medium | Avoid spam words, balance text/images |
| List Quality | High | Permission-based only, regular cleaning |
| Sending Patterns | Medium | Consistent volume, gradual increases |
| Infrastructure | Medium | Dedicated IP for 100K+ sends |

#### Complete Deliverability Checklist

**Before sending ANY campaign:**
- [ ] SPF, DKIM, DMARC records configured correctly
- [ ] Sending from a custom domain (not @gmail.com or ESP subdomain)
- [ ] Email list is 100% permission-based (no purchased lists EVER)
- [ ] Bounce rate is below 2%
- [ ] Unsubscribe rate is below 0.5%
- [ ] Spam complaint rate is below 0.1%
- [ ] List cleaned in last 30 days (removed hard bounces, invalids)
- [ ] Subject line avoids spam trigger words
- [ ] HTML email has a plain text version
- [ ] Images have alt text
- [ ] Unsubscribe link is clearly visible (not hidden in tiny text)
- [ ] Physical address is included (legal requirement)
- [ ] Email renders correctly on mobile
- [ ] All links working (no broken URLs)
- [ ] Sending domain has been warmed up (if new)
- [ ] Text-to-image ratio is at least 60:40 (more text than images)
- [ ] No URL shorteners in links (use full URLs)
- [ ] Test email sent to yourself first

#### Domain Warmup Schedule (For New Sending Domains):
| Day | Emails to Send | Target |
|-----|---------------|--------|
| 1-2 | 50/day | Most engaged subscribers only |
| 3-4 | 100/day | Highly engaged |
| 5-7 | 250/day | Engaged |
| 8-10 | 500/day | All engaged |
| 11-14 | 1,000/day | Full list gradually |
| 15-21 | 2,500/day | Expand |
| 22-30 | 5,000+/day | Full volume |

> **Try This:** Send a test email to mail-tester.com and score your deliverability. If using Gmail, check your score. Research how to improve any issues flagged. Document the score and 3 actions to improve.

---

### Self-Check Questions: Week 21

1. What does SPF stand for, and what does it protect against?
2. Name 3 differences between MailerLite and Klaviyo.
3. What are 5 characteristics of a great lead magnet?
4. Write the AIDA framework for a promotional email selling an online course.
5. How many emails should a welcome sequence have, and what is the purpose of Email 4?
6. What is the difference between CTR and CTOR?
7. Your open rate is 12% (below average). List 3 possible causes and fixes.
8. What is domain warmup, and why is it necessary?

---

## Week 22: WhatsApp Business & SMS Marketing

### Day 123: WhatsApp Business Strategy (India-Specific)

#### Why WhatsApp Marketing Matters in India
- 500+ million WhatsApp users in India (most in the world)
- 98% message open rate (vs 20% for email)
- Average response time: 90 seconds
- Most trusted messaging platform in India
- Used by all age groups (unlike Instagram which skews younger)
- Perfect for local businesses (everyone's already on it)

#### WhatsApp Business App vs API Comparison

| Feature | WhatsApp Business App (Free) | WhatsApp Business API (Paid) |
|---------|-------------------------------|------------------------------|
| **Cost** | Free | Rs 0.50-1.00 per conversation |
| **Best For** | Small business, 1 person managing | Medium-large business, teams |
| **Messages/day** | Limited (can get banned if too many) | Unlimited (within rate limits) |
| **Automation** | Basic quick replies, greeting, away message | Full chatbots, drip sequences, flows |
| **Broadcast Limit** | 256 contacts per list | Unlimited broadcasts |
| **Multi-agent** | No (1 phone, 1 person) | Yes (full team access, assign conversations) |
| **CRM Integration** | No | Yes (via BSPs — HubSpot, Zoho, etc.) |
| **Template Messages** | No (only broadcast to saved contacts) | Yes (pre-approved by Meta, rich media) |
| **Green Tick** | No | Yes (after verification, builds trust) |
| **Catalog** | Yes (basic product listing) | Yes (with API and cart integration) |
| **Setup Time** | 5 minutes (download app) | 1-2 weeks (apply through BSP) |
| **Phone Number** | Your business mobile | Dedicated number (can be landline) |
| **Analytics** | Basic (messages sent/delivered/read) | Advanced (response time, agent performance) |

#### When to Upgrade from App to API:
- You're sending more than 50 messages/day manually
- You need multiple people to respond to messages
- You want automated sequences (welcome, order updates)
- You need CRM integration
- Your broadcast list exceeds 256 people
- You want the verified green tick badge

#### WhatsApp Business App Setup (Step-by-Step):

1. Download "WhatsApp Business" from Play Store/App Store (NOT regular WhatsApp)
2. Register with your business phone number
3. Complete Business Profile:
   - Business name (cannot change later — choose wisely!)
   - Category (e.g., Education, Restaurant, Retail)
   - Description (max 256 characters — include what you do + location)
   - Business address
   - Business hours
   - Email and website
4. Set up Quick Replies (saves time on FAQ):
   - /thanks → "Thank you for your message! We'll get back to you within 1 hour."
   - /hours → "We're open Mon-Sat, 9 AM to 7 PM IST."
   - /pricing → "Our courses start at Rs 15,000. Want me to share the full fee structure?"
5. Set up Greeting Message: Auto-sent when someone messages for the first time
6. Set up Away Message: Auto-sent outside business hours
7. Create Catalog: Add your products/services with photos and prices
8. Create Labels: Organize contacts (New Lead, Interested, Customer, VIP)

> **Try This:** Download WhatsApp Business (if you haven't already). Set up a complete business profile for a hypothetical business. Create 5 Quick Replies and a Greeting Message.

---

### Day 124: WhatsApp BSP Tools (WATI, AiSensy, Interakt, Zoko)

#### WhatsApp BSP (Business Solution Provider) Detailed Comparison — India

| BSP | Starting Price | Free Trial | Key Features | Best For |
|-----|---------------|-----------|-------------|----------|
| **WATI** | Rs 2,499/month | 7 days | Easy chatbot builder, shared inbox, broadcast, Shopify integration | Small-medium businesses needing chatbots |
| **AiSensy** | Rs 999/month | 14 days | Cheapest in India, click-to-WhatsApp ads, drip campaigns | Startups, budget-conscious businesses |
| **Interakt** | Rs 999/month | 14 days | Shopify native integration, COD confirmation, order updates | E-commerce stores on Shopify |
| **Zoko** | Rs 3,499/month | 7 days | Multi-agent inbox, round-robin assignment, advanced analytics | Customer support teams |
| **Gallabox** | Rs 1,999/month | 7 days | Workflow automation, payment collection, Google Sheets sync | Service businesses |
| **DelightChat** | Rs 2,499/month | 14 days | Omnichannel (WhatsApp + Instagram + Email), D2C focused | D2C brands selling on multiple channels |

#### How to Get the WhatsApp Green Tick (Verified Badge):

Requirements:
1. Business must be a "notable" entity (brand awareness, search results, press)
2. Must be using WhatsApp Business API (not the free app)
3. Must have 2-factor authentication enabled
4. Business must be real (registered company)

Process:
1. Apply through your BSP (WATI/AiSensy etc. have a "Request Green Tick" option)
2. Submit: Business documents, website link, proof of entity
3. Wait 3-7 business days for Meta review
4. If rejected, wait 30 days before reapplying

#### WhatsApp Marketing Best Practices for India:
1. **Always get opt-in** — Send opt-in message before marketing (TRAI + Meta requirement)
2. **Respond within 24 hours** — Free conversation window is 24 hours from last user message
3. **Use template messages wisely** — Each costs money and needs Meta approval (24-48 hr review)
4. **Personalize** — Use {name}, {order_id}, {product_name} variables
5. **Don't spam** — Max 2-3 marketing messages per week (users block fast)
6. **Include opt-out** — "Reply STOP to unsubscribe" (required by Meta)
7. **Best sending times India** — 10 AM-12 PM and 7 PM-9 PM (avoid early morning/late night)
8. **Use multimedia** — Images/videos get 3x higher engagement than text-only
9. **Keep messages short** — Under 150 words for marketing messages
10. **Use buttons** — Quick Reply buttons get 3x more engagement than asking users to type

---

### Day 125: Chatbots — ManyChat, Chatfuel, Tidio

#### What is a Chatbot?
An automated conversation flow that responds to users without human intervention. Can handle FAQs, collect information, qualify leads, and route to humans when needed.

#### Chatbot Platform Comparison

| Feature | ManyChat | Chatfuel | Tidio |
|---------|----------|----------|-------|
| **Free Tier** | 1,000 contacts | 50 conversations/month | 50 conversations/month |
| **Best Channel** | Instagram DM + WhatsApp | Facebook Messenger | Website live chat |
| **Ease of Use** | Easy (drag-and-drop) | Easy (block-based) | Easy (visual) |
| **AI Capability** | Basic keyword matching | Basic + AI add-on | Built-in AI (Lyro) |
| **E-commerce** | Shopify integration | Limited | Shopify + WooCommerce |
| **India Suitability** | Great (Instagram popular) | Okay (FB declining) | Great (website focus) |
| **Paid Starting** | $15/month | $14.99/month | $29/month |

#### Chatbot Flow Design Principles:

**Key Elements of a Good Chatbot:**
1. **Welcome message** — Greet and show menu options immediately
2. **Quick reply buttons** — Max 3-4 options per message (reduce typing)
3. **Human handoff** — Always have "Talk to a person" option
4. **Fallback response** — When bot doesn't understand ("I didn't get that. Here are your options...")
5. **Exit/restart option** — Let user start over at any time
6. **Typing indicators** — Add 1-2 second delays between messages (feels natural)
7. **Personality** — Give the bot a name and consistent tone

#### Example Chatbot Flow for TechPath Academy:

```
WELCOME: "Hi! I'm TechBot from TechPath Academy. How can I help you today?"
├── [Course Info] 
│   → "We offer 3 programs:" [Show carousel]
│   ├── [Digital Marketing] → Details, duration, fee → "Want a free demo class?" → Collect phone
│   ├── [Web Development] → Details, duration, fee → "Want a free demo class?" → Collect phone
│   └── [Data Analytics] → Details, duration, fee → "Want a free demo class?" → Collect phone
│
├── [Fee & EMI Options]
│   → "Our fees range from Rs 25,000 to Rs 50,000"
│   → "EMI available: 3/6/9 months at 0% interest"
│   → "Want to speak with a counselor?" → Collect name + phone → Assign to team
│
├── [Placement Support]
│   → Show stats: "85% placement rate, avg Rs 4.5 LPA"
│   → Show testimonials (carousel)
│   → "Book a free career counseling session?" → Calendar link
│
├── [Talk to Someone]
│   → "A human will be with you shortly!"
│   → Route to live agent (business hours)
│   → Outside hours: "Our team is away. Leave your number, we'll call by 10 AM"
│
└── [Something Else]
    → "Type your question and I'll try to help!"
    → AI keyword matching
    → Fallback: "I couldn't find an answer. Let me connect you with our team."
```

#### Step-by-Step: Building a Bot with ManyChat

1. Go to manychat.com → Sign up → Connect your Instagram account
2. Go to Automation → + New Automation
3. Choose trigger: "User sends any message" OR "User clicks Story mention"
4. Add first message: Welcome text + Quick Reply buttons
5. For each button → Add new message with relevant info
6. Add "Collect user input" step for phone/email
7. Connect to Google Sheets (via Zapier) or use ManyChat's built-in CRM
8. Test the flow by messaging yourself
9. Set live!

> **Try This:** Design a chatbot flow (on paper or in a Google Doc) for a local restaurant. Include: Welcome message, Menu (with 3 categories), Online Order, Table Reservation, and Talk to Staff. Draw it as a flowchart.

---

### Day 126: SMS Marketing in India (Textlocal, MSG91, DLT Compliance)

#### SMS Marketing Overview in India

**Key Facts:**
- 1.2+ billion mobile connections in India
- SMS open rate: 98% (read within 3 minutes on average)
- All bulk SMS in India is regulated by TRAI (Telecom Regulatory Authority of India)
- DLT (Distributed Ledger Technology) registration is MANDATORY since 2021
- Non-compliance: Rs 1,000+ fine PER unauthorized message

#### SMS Service Providers for India

| Provider | Per SMS Cost | DLT Support | API | Best For |
|----------|------------|-------------|-----|----------|
| Textlocal | Rs 0.20-0.25 | Yes | Yes | Small-medium business, easy dashboard |
| MSG91 | Rs 0.15-0.20 | Yes | Yes | Developers, OTP-heavy businesses |
| Twilio | Rs 0.25-0.35 | Yes | Yes | Global businesses, complex integrations |
| Gupshup | Custom | Yes | Yes | WhatsApp + SMS combined |
| Kaleyra | Custom | Yes | Yes | Enterprise, high volume |

#### DLT Compliance for India — Complete Guide

**What is DLT?** Distributed Ledger Technology — TRAI requires ALL businesses sending bulk SMS (more than a few personal messages) to register on the DLT platform. Without this, your messages will be blocked.

##### Step 1: Choose a DLT Operator and Register

| Operator | DLT Portal URL |
|----------|---------------|
| Jio | https://trueconnect.jio.com |
| Airtel | https://www.airtel.in/business/commercial-communication |
| Vi (Vodafone-Idea) | https://smartping.live/entity/reg-home |
| BSNL | https://www.ucc-bsnl.co.in |

**Registration Requirements:**
- Business PAN card
- GST certificate (or declaration if GST-exempt)
- Company registration certificate
- Authorized signatory details
- Business email and phone
- Fee: Rs 5,000 one-time (approximate, varies by operator)

##### Step 2: Register Headers (Sender IDs)

Your sender ID is the 6-character name that appears instead of a phone number.

| Category | Format | Example | When to Use |
|----------|--------|---------|-------------|
| Promotional | VM-XXXXXX | VM-TECHPT | Marketing messages, offers |
| Transactional | XX-XXXXXX | AD-TECHPT | OTPs, order confirmations |
| Service-Implicit | XI-XXXXXX | TI-TECHPT | Updates to existing customers |
| Service-Explicit | XE-XXXXXX | TE-TECHPT | Opted-in service messages |

##### Step 3: Register Message Templates

Every SMS text must be pre-approved as a template. Variables are marked with {#var#}.

**Example templates:**
```
Dear {#var#}, your OTP for login is {#var#}. Valid for 5 minutes. Do not share. - TechPath
```
```
Hi {#var#}, your class for {#var#} starts tomorrow at {#var#}. Join link: {#var#}. - TechPath Academy
```
```
Exciting offer! Get {#var#}% off on {#var#} courses. Enroll now: {#var#}. T&C apply. Reply STOP to opt out. - TechPath
```

##### Step 4: Understand SMS Categories

| Category | Timing | DND Bypass | Use Case |
|----------|--------|-----------|----------|
| **Promotional** | 10 AM - 9 PM only | NO (blocked on DND numbers) | Offers, marketing |
| **Transactional** | 24/7 | YES | OTPs, payment alerts, delivery updates |
| **Service-Implicit** | 24/7 | YES | Existing customer updates |
| **Service-Explicit** | 9 AM - 9 PM | YES | Opted-in marketing |

**Important DLT Rules:**
- Scrubbing against DND (Do Not Disturb) is MANDATORY for promotional SMS
- Templates must be approved before use (takes 1-3 days)
- Non-compliance penalty: Rs 1,000+ per unauthorized message
- All content must match registered templates exactly (variable substitution only)
- Consent records must be maintained for audit

> **Try This:** Write 3 SMS templates (under 160 characters each) for a gym in Bhopal: (1) a promotional offer for new joiners, (2) a transactional message for payment confirmation, and (3) a service message for class schedule change. Mark variables with {#var#}.

---

### Self-Check Questions: Week 22

1. What are 3 differences between WhatsApp Business App and WhatsApp API?
2. Which WhatsApp BSP would you recommend for a small e-commerce business in India on a tight budget? Why?
3. Name 5 elements every chatbot should have.
4. What is DLT and why is it required in India?
5. What are the 4 SMS categories in India and when can each be sent?
6. A business sends a promotional SMS at 10 PM. What happens?
7. Design a 3-message WhatsApp drip sequence for a new lead who asked about a digital marketing course.

---

## Week 23: Marketing Automation

### Day 127: Marketing Automation Fundamentals

#### What is Marketing Automation?
Software that automates repetitive marketing tasks based on triggers, conditions, and actions. Instead of manually sending follow-ups, the system does it for you — at scale, 24/7.

**Real-World Example:**
Without automation: Rahul fills your contact form. You manually check the form, open your email, write a reply, add him to a spreadsheet, tell your sales team.
With automation: Rahul fills form → auto-email sent instantly → added to CRM → tagged based on interest → sales team notified on Slack → follow-up email scheduled for Day 3. All in 0 seconds.

#### Core Concepts of Marketing Automation:

##### Trigger (What starts the automation?)
| Trigger Type | Examples |
|-------------|----------|
| Form submitted | Contact form, lead magnet download, quiz |
| Email event | Opened email, clicked link, didn't open |
| Page visited | Pricing page, specific product page |
| Tag/property change | Lead score reached 70, status changed |
| Date/time | Birthday, 30 days after signup, Monday 9 AM |
| Purchase event | First purchase, repeat purchase, cart abandoned |
| External event | New row in Google Sheet, webhook received |

##### Condition (What decides the path?)
| Condition Type | Examples |
|---------------|----------|
| If/Else | If email was opened → send follow-up. Else → try different subject. |
| Tag check | If subscriber has tag "VIP" → send exclusive offer |
| Score check | If lead score > 50 → notify sales team |
| Property check | If location = "Mumbai" → show Mumbai event |
| Time check | If it's been 7 days since last email → send re-engagement |

##### Action (What does the system do?)
| Action Type | Examples |
|------------|----------|
| Send email | Welcome email, nurture email, offer |
| Add/remove tag | "engaged", "interested-in-seo", "purchased" |
| Update field | Change lead status, add score points |
| Wait/Delay | Wait 2 days before next email |
| Notify team | Slack message, email alert to sales |
| Move to list/segment | Add to "hot leads" list |
| Webhook | Send data to another system |
| Branch/Split | A/B test different paths |

#### Types of Marketing Automation Workflows:

1. **Welcome/Onboarding** — New subscriber → educate → convert
2. **Lead Nurturing** — Warm lead → provide value → build trust → sell
3. **Lead Scoring** — Track actions → assign points → alert sales at threshold
4. **Cart Abandonment** — Left cart → remind → offer discount → recover sale
5. **Re-engagement** — Inactive user → win-back campaign → clean list
6. **Post-purchase** — Bought → thank → support → review → upsell
7. **Event-based** — Birthday/anniversary → special offer

> **Try This:** Map out an automation workflow on paper for this scenario: Someone downloads a "Free SEO Checklist" from your website. What should happen automatically over the next 14 days? Include at least 5 steps with triggers, conditions, and actions.

---

### Day 128: Zapier Deep Dive

#### What is Zapier?
Zapier connects 6,000+ apps together without code. A "Zap" is an automated workflow: when THIS happens in App A → do THAT in App B.

#### How a Zap Works:
```
Trigger (App 1) → Filter (optional) → Action (App 2) → Action (App 3) → ...
```

#### Zapier Terminology:
- **Zap** = An automated workflow
- **Trigger** = The event that starts the Zap
- **Action** = What happens after the trigger
- **Task** = One successful run of an action (Zapier counts these for billing)
- **Filter** = Only continue if a condition is met
- **Path** = Split into different outcomes based on conditions
- **Formatter** = Transform data between steps (dates, text, numbers)

#### Common Zaps for Digital Marketers:

**1. Lead Capture → CRM + Notification:**
```
Google Form (new response)
  → MailerLite (add subscriber + tag)
  → Google Sheets (add row to lead tracker)
  → Slack (#new-leads notification)
```

**2. New Blog Post → Multi-Channel Promotion:**
```
WordPress (new post published)
  → Buffer (create social post for Twitter/LinkedIn)
  → MailerLite (send to subscriber list)
  → Slack (#content-team notification)
```

**3. E-commerce Order → Full Follow-Up:**
```
Shopify (new order)
  → Google Sheets (add to orders tracker)
  → MailerLite (tag as "customer")
  → Delay 7 days → MailerLite (send review request email)
```

**4. Meeting Booked → Prep Automation:**
```
Calendly (new booking)
  → Google Calendar (create event with details)
  → Gmail (send prep email with agenda)
  → Slack (notify sales team)
  → HubSpot (create/update contact)
```

**5. Webinar → Complete Follow-up:**
```
Zoom (webinar registration)
  → MailerLite (add to "webinar" group)
  → Google Sheets (tracking)
  → 1 hour before: Email reminder
  → After webinar: Send recording + CTA email
```

#### Step-by-Step: Building Your First Zap

1. Go to zapier.com → Sign up (free plan: 5 Zaps, 100 tasks/month)
2. Click "Create Zap"
3. **Choose Trigger App:** Google Forms → New Response in Spreadsheet
4. **Connect account:** Sign in with your Google account
5. **Configure trigger:** Select your specific form
6. **Test trigger:** Submit a test response in Google Forms first, then test in Zapier
7. **Add Action:** Click + → Choose MailerLite → Add/Update Subscriber
8. **Connect MailerLite:** Use your API key (found in Settings → Integrations)
9. **Map fields:** Email ← Form email field, Name ← Form name field
10. **Test action:** Click "Test" — verify subscriber appears in MailerLite
11. **Name your Zap:** Something descriptive like "Form → MailerLite Lead Capture"
12. **Turn ON** the Zap

> **Try This:** Create a free Zapier account. Build a simple Zap: Google Form submission → Google Sheets row (just move data from form to sheet). Test it with 3 submissions. Verify all data flows correctly.

---

### Day 129: Make.com Deep Dive

#### Make.com vs Zapier — When to Choose What

| Need | Zapier | Make.com |
|------|--------|----------|
| Simple 2-step automation | Yes | Overkill |
| Complex branching logic | Limited | Excellent |
| Budget-friendly | Expensive at scale | Much cheaper |
| 6,000+ integrations | Yes | 1,500+ |
| Large data processing | Expensive (per task) | Better value (per operation) |
| Visual workflow design | Linear (left to right) | Flowchart (any direction) |
| Real-time triggers | 1-15 min polling | Instant webhooks |
| Error handling | Basic (retry) | Advanced (retry, break, ignore, commit) |
| Indian app support | Razorpay, Zoho, etc. | Growing |

#### Make.com Key Concepts:

- **Scenario** = A workflow (equivalent to a Zap)
- **Module** = A single step/action (trigger or action)
- **Router** = Split flow into multiple paths based on conditions
- **Iterator** = Loop through an array/list of items
- **Aggregator** = Combine multiple items into one
- **Error Handler** = What to do when a step fails

#### Building a Scenario in Make.com:

1. Go to make.com → Sign up (free: 2 scenarios, 1,000 operations/month)
2. Click "Create a new scenario"
3. Click the big + in the center → Search for your trigger app
4. Connect your account → Configure the trigger
5. Click the small + on the right side of the module → Add next step
6. For branching: Right-click the connection line → Add a Router
7. Each router path can have a filter (condition)
8. Click "Run once" to test with real data
9. Schedule the scenario (every 15 min, hourly, instantly via webhook)

#### Advanced Make.com Features:

**Webhooks (Instant triggers):**
Instead of polling every 15 minutes, a webhook fires INSTANTLY when an event happens. Perfect for time-sensitive automations like order notifications.

**Data Store:**
Built-in simple database. Store data between runs — like a counter, a lookup table, or a queue.

**Iterators + Aggregators:**
Process a list of items one by one (iterate), then combine results (aggregate). Example: Get 50 contacts from a CSV, send personalized email to each, then log all results to one sheet row.

> **Try This:** Create a free Make.com account. Build a scenario: Webhook trigger → Send email (use the built-in Email module). Get the webhook URL, trigger it using a browser, and verify the email arrives.

---

### Day 130: Lead Scoring & Nurture Workflows

#### Lead Scoring Model — Complete Framework

Lead scoring assigns numerical points to contacts based on WHO they are (demographic fit) and WHAT they do (behavioral engagement). When score reaches a threshold, the lead is passed to sales.

##### Demographic Scoring (Fit Score — Max 50 points)

| Factor | Criteria | Points | Reasoning |
|--------|----------|--------|-----------|
| Job Title | Decision maker (CEO, Director, VP, Owner) | +20 | Can approve purchases |
| Job Title | Manager (Marketing Mgr, Sales Mgr) | +15 | Influences decisions |
| Job Title | Influencer (Executive, Coordinator) | +10 | Recommends solutions |
| Job Title | Student / Intern | +5 | Future buyer, low priority now |
| Company Size | Enterprise (500+ employees) | +15 | High deal value |
| Company Size | Mid-market (50-499 employees) | +12 | Good deal value |
| Company Size | Small business (10-49 employees) | +8 | Moderate value |
| Company Size | Micro/Solo (1-9 employees) | +4 | Low value but high volume |
| Industry | Exact target industry match | +15 | Highest conversion likelihood |
| Industry | Related industry | +8 | Moderate fit |
| Industry | Unrelated | +2 | Low fit |
| Location | Target city/region | +10 | Serviceable |
| Location | Other (remote possible) | +5 | Still possible |
| Budget | Confirmed budget available | +25 | Ready to buy |
| Budget | Exploring options | +10 | Considering |

##### Behavioral Scoring (Engagement Score — Max 50 points)

| Action | Points | Reasoning |
|--------|--------|-----------|
| Visited pricing page | +20 | Strong buying signal |
| Requested demo/consultation | +30 | Strongest signal |
| Submitted contact form | +25 | Active outreach |
| Downloaded lead magnet | +10 | Interested in topic |
| Attended webinar | +15 | Invested time |
| Watched product video | +10 | Exploring solution |
| Opened 3+ emails this week | +10 | Engaged |
| Clicked email CTA | +5 | Moderate engagement |
| Visited 5+ pages in one session | +10 | Researching deeply |
| Viewed case studies/testimonials | +15 | Evaluating credibility |
| Returned to site 3+ times | +10 | Persistent interest |
| Inactive 30+ days | -15 | Cooling off |
| Inactive 60+ days | -25 | Gone cold |
| Unsubscribed from emails | -30 | Disengaged |
| Marked email as spam | -50 | Remove from scoring |

##### Score Categories & Actions:

| Score Range | Category | Action |
|-------------|----------|--------|
| 0-25 | Cold | Add to nurture sequence, educational content only |
| 26-50 | Warm | Increase engagement — case studies, webinar invites, comparisons |
| 51-75 | Hot | Alert sales team, send personalized outreach within 24 hours |
| 76-100 | Sales-Ready | Immediate call/meeting, custom proposal, close the deal |

#### Lead Nurture Workflow Design:

**Cold Lead Nurture (Score 0-25):**
```
Week 1: Educational blog post email
Week 2: Industry report / free resource
Week 3: How-to video link
Week 4: Case study (light — results without sales pitch)
→ If score increases above 25, move to Warm workflow
→ If no engagement after 4 weeks, pause for 2 weeks then try again
```

**Warm Lead Nurture (Score 26-50):**
```
Day 1: Personalized email acknowledging their interest
Day 3: Detailed case study from their industry
Day 5: Comparison guide (your solution vs alternatives)
Day 7: Webinar/workshop invitation
Day 10: "Any questions?" personal email from sales rep
→ If score reaches 50+, trigger sales team alert
```

> **Try This:** Create a lead scoring model for your dream business (or for TechPath Academy). List at least 8 factors (4 demographic, 4 behavioral) with point values. Then describe what happens when a lead reaches 30, 50, and 75 points.

---

### Day 131: Drip Campaigns Across Channels

#### What is a Multi-Channel Drip Campaign?
Instead of only emailing leads, you reach them across multiple channels in a coordinated sequence — email + WhatsApp + SMS + retargeting ads.

#### Multi-Channel Drip Campaign Example: Course Launch

| Day | Channel | Message |
|-----|---------|---------|
| Day 0 | Email | Welcome + lead magnet delivery |
| Day 1 | WhatsApp | "Hi {name}! Did you get a chance to check your download? Any questions?" |
| Day 2 | Email | Your story + value |
| Day 3 | Instagram (retargeting ad) | Testimonial video from past student |
| Day 5 | Email | Case study (student success) |
| Day 5 | SMS | "Reminder: Free workshop this Saturday. Register: [link]" |
| Day 7 | Email | Workshop reminder + what to expect |
| Day 7 | WhatsApp | "Workshop starts in 2 hours! Here's your join link: [link]" |
| Day 8 | Email | Workshop recording + limited-time offer |
| Day 9 | WhatsApp | "Only 5 seats left at early bird price. Shall I reserve yours?" |
| Day 10 | Email | FAQ + objection handling |
| Day 11 | Email + SMS | "Last day for Rs 5000 discount. Don't miss it!" |

#### Channel Selection Guidelines:

| Channel | Best For | Frequency Max | Open/Response Rate |
|---------|----------|--------------|-------------------|
| Email | Long content, detailed info, sequences | 3-4/week | 20-25% open |
| WhatsApp | Quick updates, personal touch, urgency | 2-3/week | 90%+ open |
| SMS | OTPs, time-sensitive alerts, reminders | 1-2/week | 98% open |
| Push notifications | App users, real-time updates | 1/day | 5-15% open |
| Retargeting ads | Visual reminders, social proof | Always on | 0.5-2% CTR |

#### Automation Tool Selection for Multi-Channel:

| Requirement | Tool |
|-------------|------|
| Email only | MailerLite, ConvertKit |
| Email + SMS | Brevo, ActiveCampaign |
| Email + WhatsApp | Brevo, AiSensy + MailerLite via Zapier |
| Full multi-channel | ActiveCampaign + WATI + Zapier (most businesses) |
| Enterprise | HubSpot Marketing Hub + WhatsApp BSP |

> **Try This:** Design a 10-day multi-channel drip campaign for a new gym in Pune that just collected 200 leads from a "Free Week Pass" campaign. Plan which channel to use each day and what message to send. Consider: email, WhatsApp, and SMS.

---

### Self-Check Questions: Week 23

1. What are the three core components of any marketing automation workflow?
2. Name 5 common triggers that can start an automation.
3. Compare Zapier and Make.com — give 3 scenarios where each is the better choice.
4. What is lead scoring? Why would a score of 75 be treated differently than a score of 25?
5. A lead has opened 5 emails, visited the pricing page twice, and downloaded a case study. Using the scoring model above, calculate their behavioral score.
6. What is the advantage of a multi-channel drip campaign over email-only?
7. You have a budget of Rs 2,000/month for automation tools. Which combination would you choose?

---

## Week 24: CRM & Customer Lifecycle

### Day 132: CRM Fundamentals (HubSpot, Zoho, Pipedrive, Salesforce)

#### What is a CRM?
Customer Relationship Management — a system to track every interaction with leads and customers in ONE place. No more spreadsheets, sticky notes, or forgotten follow-ups.

**Why businesses need a CRM:**
- 50% of leads never get a follow-up (without CRM)
- Sales teams using CRM see 29% increase in revenue
- Average sales rep spends 17% of time entering data (CRM automates this)
- Impossible to scale past 50 leads manually

#### CRM Comparison (Detailed)

| Feature | HubSpot Free | Zoho CRM Free | Pipedrive | Freshsales | Salesforce |
|---------|-------------|---------------|-----------|------------|-----------|
| **Price** | Free (core CRM) | Free (3 users) | Rs 1,000/user/month | Free (3 users) | Rs 3,000/user/month |
| **Contacts** | 1,000,000 | 5,000 | Unlimited | Unlimited | Unlimited |
| **Best For** | Startups, SMBs | Indian SMBs | Sales-focused teams | Indian startups | Enterprise |
| **Pipeline Views** | Kanban board | Kanban + list | Best-in-class Kanban | Kanban | All views |
| **Email Integration** | Gmail, Outlook | Gmail, Outlook, Zoho Mail | Gmail, Outlook | Gmail, Outlook | All + custom |
| **Automation** | Limited (free) | Basic workflows | Good (paid) | AI-powered (Freddy) | Advanced |
| **WhatsApp** | No (paid only) | Zoho channels | No | Yes | Via integration |
| **India Support** | Email | Local support teams | Email | Indian company (local) | Expensive local |
| **Mobile App** | Good | Good | Excellent | Good | Good |
| **Learning Curve** | Easy (1-2 days) | Medium (3-5 days) | Easy (1-2 days) | Easy | Hard (2-4 weeks) |
| **Scalability** | Good (paid plans scale) | Good | Limited | Good | Unlimited |

#### Choosing a CRM — Decision Tree:
```
Budget = Rs 0?
├── Yes → HubSpot Free or Zoho Free or Freshsales Free
│   ├── Need Indian support? → Zoho or Freshsales
│   ├── Want marketing too? → HubSpot (best free marketing tools)
│   └── Need WhatsApp? → Freshsales
└── No →
    ├── Pure sales team? → Pipedrive
    ├── Marketing + Sales + Service? → HubSpot (paid)
    ├── Indian business, budget-conscious? → Zoho
    └── Enterprise, 50+ users? → Salesforce
```

---

### Day 133: HubSpot CRM Hands-On Setup

#### Step-by-Step HubSpot Free CRM Setup:

**1. Create Account:**
- Go to hubspot.com → "Get started free"
- Sign up with email → Verify → Complete onboarding wizard
- Select: "I want to organize my contacts and track deals"

**2. Set Up Your Pipeline:**
- Go to Sales → Deals → Board View
- Click "Edit stages" (gear icon)
- Delete default stages
- Create your stages:
  - Stage 1: "New Lead" — Probability: 10%
  - Stage 2: "Contacted" — Probability: 25%
  - Stage 3: "Meeting Booked" — Probability: 40%
  - Stage 4: "Proposal Sent" — Probability: 60%
  - Stage 5: "Won" — Probability: 100%
  - Stage 6: "Lost" — Probability: 0%

**3. Import Contacts:**
- Contacts → Import → Start an import → File from computer
- Upload a CSV with columns: First Name, Last Name, Email, Phone, Company, Deal Amount, Lead Status
- Map each column to HubSpot properties
- Review and complete import

**4. Create Contact Properties (Custom Fields):**
- Settings → Properties → Create property
- Useful custom properties for digital marketing:
  - "Lead Source" (dropdown: Google, Social, Referral, Event)
  - "Course Interest" (dropdown: Digital Marketing, Web Dev, Data)
  - "Budget Range" (dropdown: Under 20K, 20-50K, 50K+)
  - "Follow-up Date" (date picker)

**5. Create a Simple Workflow:**
- Automation → Workflows → Create workflow
- Trigger: "Contact property Lead Status changes to Qualified"
- Action 1: Send internal email notification to sales
- Action 2: Create task "Schedule call" due in 2 days
- Action 3: Set property "Pipeline Stage" to "Contacted"
- Turn on the workflow

**6. Connect Email:**
- Settings → Email → Connect personal email (Gmail/Outlook)
- Now all emails to/from contacts are logged automatically
- Email templates available from CRM

> **Try This:** Sign up for HubSpot Free CRM. Create a pipeline with 5 stages. Import 10 sample contacts (use Indian names and phone numbers). Create 2 deals and drag them through pipeline stages. Explore the Reports section.

---

### Day 134: Customer Lifecycle — AARRR Framework (Pirate Metrics)

#### What is AARRR?
A framework created by Dave McClure to track the complete customer lifecycle. Called "Pirate Metrics" because AARRR sounds like a pirate. Each letter represents a stage.

##### 1. Acquisition — How do users FIND you?

**Question:** Where are users coming from?
**Metrics:** Website traffic, new visitors, traffic by source, cost per visit
**Indian example:** Priya searches "digital marketing course Bhopal" on Google and clicks on TechPath's website.

**Key Metric:** Cost per Acquisition (CPA) by channel
```
CPA = Marketing spend on channel / New users from that channel
```

##### 2. Activation — Do users have a GREAT first experience?

**Question:** Did they reach the "aha moment"?
**Metrics:** Sign-up rate, onboarding completion, first key action
**Indian example:** Priya attends a free demo class and thinks "This is exactly what I need!"

**Key Metric:** Activation Rate
```
Activation Rate = Users who complete key action / Total new users x 100
```

**The "Aha Moment" examples:**
- SaaS product: First report generated
- Course platform: First lesson completed
- E-commerce: First product added to wishlist
- App: Completed onboarding + used core feature

##### 3. Retention — Do users COME BACK?

**Question:** Are they using the product/service regularly?
**Metrics:** DAU/MAU ratio, return visits, login frequency, email opens, churn rate
**Indian example:** Priya returns every week for classes, opens all emails, engages on WhatsApp group.

**Key Metric:** Retention Rate (cohort-based)
```
Week 1 Retention = Users active in Week 1 / Users who signed up x 100
```

**Retention benchmarks:**
- Excellent: 40%+ at Day 30
- Good: 20-40% at Day 30
- Poor: Below 20% at Day 30

##### 4. Revenue — Do users PAY you?

**Question:** How do you monetize?
**Metrics:** Conversion rate, ARPU (Average Revenue Per User), LTV, MRR
**Indian example:** Priya enrolls in the 6-month course for Rs 35,000.

**Key Metrics:**
```
LTV (Lifetime Value) = Average Order Value x Purchase Frequency x Customer Lifespan
ARPU = Total Revenue / Total Active Users
```

##### 5. Referral — Do users TELL OTHERS?

**Question:** Would they recommend you? Do they actively bring new users?
**Metrics:** NPS score, referral rate, viral coefficient
**Indian example:** Priya refers her friend Ananya and earns Rs 2,000 cashback.

**Key Metric:** Viral Coefficient
```
Viral Coefficient = Invites sent per user x Conversion rate of invites
If > 1: Organic growth (each user brings more than 1 new user)
```

---

### Day 135: Loyalty & Referral Programs

#### Loyalty Program Types for Indian Businesses:

| Type | How It Works | Example | Best For |
|------|-------------|---------|----------|
| Points-based | Rs 100 spent = 1 point, redeem at threshold | Flipkart SuperCoins | E-commerce, retail |
| Tier-based | Spend more → unlock better perks | MakeMyTrip, airline programs | Travel, luxury |
| Cashback | Get % back on every purchase | Paytm, CRED | Fintech, frequent purchases |
| Referral | Bring a friend, both get rewarded | CRED, Groww, Uber | Apps, subscriptions |
| Stamp/Punch | "Buy X, get 1 free" | Local coffee shops | Food, frequent small purchases |
| Subscription | Pay monthly/yearly for perks | Amazon Prime, Zomato Gold | E-commerce, delivery |

#### Referral Program Design (Complete):

**Formula for a Successful Referral Program:**
1. Reward should be 10-20% of your Customer Acquisition Cost (CAC)
2. Reward BOTH the referrer AND the new customer (two-sided incentive)
3. Make sharing easy (WhatsApp share button is CRITICAL for India)
4. Track with unique referral codes or links
5. Show referral count/status in the user's dashboard

**Referral Program Example for TechPath Academy:**
```
Program Name: "Learn Together, Earn Together"

For the Referrer:
- Rs 2,000 cashback after friend enrolls
- Additional: If 3 referrals, get Rs 5,000 bonus (incentivize more)

For the New Student:
- Rs 1,500 off course fee
- Free access to 1 extra workshop

Sharing Mechanism:
- Unique referral link: techpath.biz/refer/RAHUL2026
- WhatsApp share button (pre-written message)
- Instagram story template with code

Tracking:
- Dashboard showing: referrals sent, pending, converted
- Automatic payout after 15-day enrollment confirmation
```

---

### Day 136: Personalization & Dynamic Content

#### Levels of Personalization:

| Level | What It Is | Example | Tools |
|-------|-----------|---------|-------|
| 1. Name | Use first name in communications | "Hi Rahul" in email | Any ESP |
| 2. Segment | Different content per group | Students get tips, professionals get case studies | ESP segmentation |
| 3. Behavioral | Based on what they did | "Based on your recent visit to our SEO course page..." | CRM + automation |
| 4. Dynamic | Different blocks shown to different people | VIP sees exclusive offer, new users see intro | ActiveCampaign, HubSpot |
| 5. Predictive | AI predicts what they want next | "You might also like..." | Klaviyo, Salesforce Einstein |
| 6. Real-time | Changes based on live context | "It's raining in your city — indoor workout ideas" | Advanced |

#### Dynamic Content Examples:

**Email with dynamic content block:**
```
Subject: Your weekly recommendations, {first_name}

[IF tag = "beginner"]
  Here are 3 beginner-friendly resources for this week...
[ELSE IF tag = "advanced"]
  Advanced strategies we think you'll love...
[ELSE]
  Top picks from this week...
[END IF]
```

**Website personalization:**
```
[IF visitor = returning AND viewed "pricing"]
  Show: "Ready to start? Use code WELCOME15 for 15% off"
[ELSE IF visitor = new]
  Show: "New here? Download our free guide to get started"
[ELSE]
  Show: Standard homepage content
[END IF]
```

> **Try This:** Design a loyalty program for a hypothetical cloud kitchen (food delivery brand) in Pune called "Spice Box." Include: program name, how points are earned, reward tiers, and a referral component. Make it specifically appealing to the 22-30 age group in India.

---

### Self-Check Questions: Week 24

1. What are 5 key features to look for when choosing a CRM?
2. What makes HubSpot Free different from Zoho Free CRM?
3. Explain the AARRR framework with an Indian e-commerce example at each stage.
4. Calculate the Lifetime Value (LTV) for a customer who orders Rs 800 worth of food every week for 2 years.
5. Name 4 types of loyalty programs. Which type is best for a beauty salon?
6. What is dynamic content in email marketing? Give an example.
7. A coaching business has 1,000 students. 200 referred a friend. The referral conversion rate is 30%. What is the viral coefficient?

---

## Week 25: Capstone — Build Complete Lead-to-Customer Funnel

### Day 137-144: Funnel Capstone Project

#### Lead-to-Customer Funnel Architecture

```
STAGE 1: AWARENESS (Top of Funnel — TOFU)
├── Blog posts / SEO content
├── Social media content (Reels, posts)
├── Paid ads (Google Search, Instagram)
├── YouTube videos
└── Goal: Drive traffic to landing page

STAGE 2: CAPTURE (Lead Magnet)
├── Landing page with opt-in form
├── Lead magnet delivery (PDF, template, course)
├── WhatsApp opt-in
└── Goal: Convert visitor → subscriber (target: 20-30% conversion)

STAGE 3: NURTURE (Middle of Funnel — MOFU)
├── 7-email welcome sequence (automated)
├── WhatsApp follow-up messages
├── Lead scoring (track engagement)
├── Segment by interest + engagement
└── Goal: Build trust, qualify leads

STAGE 4: CONVERT (Bottom of Funnel — BOFU)
├── Sales page / Webinar / Demo
├── Limited-time offer + urgency
├── Social proof (testimonials, case studies)
├── Follow-up sequence (cart abandonment style)
└── Goal: Turn lead → customer (target: 3-8% conversion)

STAGE 5: RETAIN & GROW (Post-Purchase)
├── Onboarding emails
├── Customer success check-ins
├── Upsell / Cross-sell sequences
├── Referral program
├── Loyalty rewards
└── Goal: Maximize LTV, generate referrals
```

#### Complete Funnel Tool Stack (Budget: Under Rs 5,000/month)

| Funnel Stage | Tool | Cost |
|-------------|------|------|
| Landing page | MailerLite (built-in pages) | Free |
| Email marketing | MailerLite | Free (up to 1K subscribers) |
| WhatsApp | AiSensy or WhatsApp Business App | Rs 999/month or Free |
| Automation | Zapier (5 free Zaps) | Free |
| CRM | HubSpot Free | Free |
| Analytics | GA4 + Looker Studio | Free |
| Social proof | Google Reviews | Free |
| Forms | Google Forms + Tally | Free |
| **Total** | | **Rs 0 - 2,000/month** |

#### Capstone Project Checklist:

- [ ] Landing page live with lead magnet offer
- [ ] Email opt-in form working and connected to ESP
- [ ] Lead magnet auto-delivered on signup
- [ ] 5+ email welcome sequence automated
- [ ] Lead scoring configured (at least 5 criteria)
- [ ] CRM pipeline with 5 stages
- [ ] At least 1 Zapier automation connecting tools
- [ ] WhatsApp Business set up with quick replies
- [ ] GA4 tracking on landing page
- [ ] At least 10 test leads run through the complete funnel
- [ ] Documentation of the entire flow (flowchart)

> **Try This:** Build the actual funnel. Start today. Use all free tools. Get your landing page live, email sequence running, and CRM configured. Run 5 test leads through and document every step. This IS your portfolio piece.

---

### Self-Check Questions: Week 25 (Capstone)

1. Draw the complete funnel from awareness to referral. Label each stage with the tools you would use.
2. What conversion rate would you target at each stage?
3. If 1,000 people visit your landing page, 250 sign up (25%), 50 attend your webinar (20% of subscribers), and 10 buy (20% of attendees) — what is your overall conversion rate from visitor to customer?
4. Name 3 metrics you would track weekly to know if your funnel is healthy.
5. Your email sequence has a 22% open rate but only 1% click rate. What's likely wrong and how would you fix it?
