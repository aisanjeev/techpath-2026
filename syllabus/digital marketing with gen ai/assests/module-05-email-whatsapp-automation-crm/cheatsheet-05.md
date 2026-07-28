# Module 5: Cheatsheet — Email, WhatsApp, Automation & CRM

## Email Marketing Benchmarks (India 2026)

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| Open Rate | 25%+ | 18-25% | Below 15% |
| Click-Through Rate (CTR) | 5%+ | 2-5% | Below 1.5% |
| Unsubscribe Rate | Below 0.2% | 0.2-0.5% | Above 0.5% |
| Bounce Rate | Below 1% | 1-2% | Above 3% |
| Spam Complaint Rate | Below 0.05% | 0.05-0.1% | Above 0.1% |
| List Growth Rate | 5%+/month | 2-5%/month | Below 1%/month |

---

## Subject Line Formulas That Work

| Formula | Example |
|---------|---------|
| Number + Benefit | "7 tools that save 5 hours every week" |
| How to + Desired Result | "How to get your first 1000 followers" |
| Question | "Are you making this common SEO mistake?" |
| Curiosity Gap | "This one change doubled our leads" |
| Urgency | "Only 24 hours left to claim your spot" |
| Personal + Name | "Rahul, your weekly marketing report" |
| Social Proof | "Why 10,000+ marketers read this daily" |
| Pain Point | "Tired of posting and getting zero engagement?" |
| Contrarian | "Stop writing blog posts (do this instead)" |
| List | "The 3-step email formula I use daily" |

**Subject line rules:**
- Keep under 50 characters (mobile-friendly)
- Don't use ALL CAPS or excessive !!!
- Avoid spam words: FREE, URGENT, ACT NOW, LIMITED TIME
- Use numbers (odd numbers perform better)
- Add emoji sparingly (1 max, test with your audience)

---

## DKIM/SPF/DMARC Quick Check Commands

Check any domain's email authentication:

```bash
# Check SPF record
nslookup -type=txt yourdomain.com

# Check DKIM record
nslookup -type=txt selector._domainkey.yourdomain.com

# Check DMARC record
nslookup -type=txt _dmarc.yourdomain.com
```

**Online tools:**
- MXToolbox: mxtoolbox.com/SuperTool.aspx
- Mail-Tester: mail-tester.com (send a test email, get a score)
- DMARC Analyzer: dmarcanalyzer.com

**Quick fixes for common issues:**
- SPF failing → Make sure all sending services are in your SPF record
- DKIM failing → Re-generate DKIM key in your ESP and update DNS
- DMARC failing → Start with `p=none` and monitor reports

---

## WhatsApp Business API Pricing (India, 2026)

| Conversation Category | Price per Conversation |
|-----------------------|----------------------|
| Marketing | Rs 0.77 |
| Utility (order updates, alerts) | Rs 0.35 |
| Authentication (OTPs) | Rs 0.30 |
| Service (customer-initiated) | Rs 0.40 |

**Key rules:**
- 24-hour conversation window after customer's last message = free replies
- Template messages (outbound) need Meta approval
- First 1,000 conversations/month are FREE
- User-initiated conversations are cheaper than business-initiated

**Template message approval tips:**
- Keep it under 1,024 characters
- No URL shorteners (use full links)
- Include opt-out option
- Avoid promotional language in utility templates
- Approval takes 24-48 hours

---

## Lead Scoring Quick Template

### Demographic Score (Max 50 points)

| Factor | Criteria | Points |
|--------|----------|--------|
| Job Title | Decision maker (Owner/Director/Manager) | +20 |
| Job Title | Influencer (Executive/Coordinator) | +10 |
| Company Size | 50+ employees | +15 |
| Company Size | 10-49 employees | +10 |
| Industry | Matches target industry | +10 |
| Location | Target city | +5 |

### Behavioral Score (Max 50 points)

| Action | Points |
|--------|--------|
| Visited pricing page | +15 |
| Submitted contact form | +20 |
| Downloaded lead magnet | +8 |
| Attended webinar | +12 |
| Opened 3+ emails this week | +5 |
| Clicked email CTA | +5 |
| No activity 30+ days | -10 |

### Score Categories
- **0-25:** Cold — Nurture with content
- **26-50:** Warm — Increase engagement
- **51-75:** Hot — Alert sales team
- **76-100:** Ready — Immediate outreach

---

## AARRR Metrics Per Stage

| Stage | Key Metric | How to Track | Target |
|-------|-----------|-------------|--------|
| **A**cquisition | New visitors/leads per month | GA4, UTM tracking | 10% growth/month |
| **A**ctivation | Sign-up to first action rate | Product analytics | 40-60% |
| **R**etention | Return visit rate (Week 1, 4, 8) | GA4, email opens | 25%+ at Week 4 |
| **R**evenue | Conversion rate (lead to paid) | CRM, payment data | 3-8% |
| **R**eferral | Referral rate (% who refer) | Referral program data | 10-20% |

---

## CRM Pipeline Stages Template

```
Stage 1: NEW LEAD          → Probability: 10%
  Action: Send welcome email within 1 hour

Stage 2: CONTACTED         → Probability: 20%
  Action: Make first call/WhatsApp within 24 hours

Stage 3: QUALIFIED         → Probability: 40%
  Action: Book discovery meeting within 3 days

Stage 4: PROPOSAL SENT     → Probability: 60%
  Action: Follow up within 2 days if no response

Stage 5: NEGOTIATION       → Probability: 80%
  Action: Address objections, offer alternatives

Stage 6: WON              → Probability: 100%
  Action: Send onboarding email, start delivery

Stage 6: LOST             → Probability: 0%
  Action: Ask for feedback, add to nurture sequence
```

---

## Zapier vs Make.com Quick Comparison

| Need | Use Zapier | Use Make.com |
|------|-----------|-------------|
| Simple 2-3 step automation | Yes | Overkill |
| Complex branching logic | Limited | Yes |
| Budget is tight | No (expensive) | Yes (cheaper) |
| Need 6,000+ app integrations | Yes | Limited (1,500+) |
| Processing large data batches | Expensive | Better value |
| Quick setup (under 5 min) | Yes | Takes longer |
| Visual workflow building | Linear view | Flowchart view |
| Real-time triggers | 1-15 min polling | Instant (webhooks) |
| Indian tools (Razorpay, Zoho) | Good support | Growing |

---

## 7-Email Welcome Sequence Outline

| # | Timing | Purpose | Subject Line Angle |
|---|--------|---------|-------------------|
| 1 | Immediately | Deliver lead magnet + welcome | "Here's your [thing]" |
| 2 | Day 1 | Tell your story, build trust | "How I/we [achieved result]" |
| 3 | Day 3 | Share best tip (quick win) | "The #1 [mistake/tip]" |
| 4 | Day 5 | Social proof / case study | "How [name] got [result]" |
| 5 | Day 7 | Address objections | "But will this work for...?" |
| 6 | Day 9 | Soft pitch (introduce offer) | "I made this for you" |
| 7 | Day 11 | Hard pitch + urgency | "Last chance / Doors closing" |

**Rules for every email:**
- ONE goal per email
- ONE CTA (don't confuse with multiple links)
- PS line at the end (highest-read part after subject)
- Preheader text that adds context (not repeats subject)
- Mobile-first design (60%+ open on mobile in India)

---

## Key Formulas

**Email ROI:**
```
ROI = (Revenue from Email - Cost of Email) / Cost of Email x 100
```

**List Growth Rate:**
```
Growth Rate = (New Subscribers - Unsubscribes - Bounces) / Total List Size x 100
```

**Customer Lifetime Value:**
```
LTV = Average Order Value x Purchase Frequency x Customer Lifespan
```

**Lead Score Threshold:**
```
If Total Score >= 70 → Pass to Sales
If Total Score 40-69 → Continue Nurturing
If Total Score < 40 → Re-engage or Archive
```

**Cost per Lead (Email):**
```
CPL = ESP Monthly Cost / New Subscribers Acquired
```
