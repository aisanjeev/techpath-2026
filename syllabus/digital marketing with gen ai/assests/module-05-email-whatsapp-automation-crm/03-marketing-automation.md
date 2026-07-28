# Marketing Automation — Work Smarter, Not Harder

**Module 05 — Email, WhatsApp, Marketing Automation & CRM | Topic 3**

---

## What is Marketing Automation?

Marketing automation means using software to perform repetitive marketing tasks automatically — sending emails, posting on social media, updating spreadsheets, notifying your team — without you doing it manually every time.

Think of it like setting up dominoes. You arrange them once, and when the first one falls (a customer signs up), the rest follow automatically (welcome email, CRM update, team notification) without you touching anything.

**Without automation (manual process):**
1. Customer fills a form on your website
2. You notice the form submission (maybe hours later)
3. You copy their details into a spreadsheet
4. You manually send a welcome email
5. You tell your sales team on WhatsApp about the new lead

**With automation (automated process):**
1. Customer fills a form → everything below happens in 2 seconds:
   - Welcome email sent automatically
   - Contact added to CRM with proper tags
   - Sales team gets a Slack notification
   - Lead is added to a nurture email sequence
   - A row is created in Google Sheets for tracking

> **Fun Fact:** Companies using marketing automation see 451% more qualified leads. The reason is simple — no lead falls through the cracks when a machine remembers to follow up every single time.

---

## Popular Automation Tools Compared

| Tool | Type | Free Tier | Ease of Use | Best For |
|------|------|-----------|-------------|----------|
| **Zapier** | Connector (connects apps) | 5 Zaps, 100 tasks/month | Very Easy | Beginners, small teams |
| **Make.com** | Visual workflow builder | 1,000 operations/month | Easy-Medium | Visual thinkers, complex flows |
| **n8n** | Open-source connector | Unlimited (self-hosted) | Medium | Developers, budget-conscious |
| **HubSpot Workflows** | Built-in CRM automation | Limited (free CRM) | Easy | HubSpot users, sales teams |
| **Mailchimp Journeys** | Email-focused automation | Limited free tier | Easy | Email-centric businesses |
| **Pabbly Connect** | Indian alternative to Zapier | 100 tasks/month | Easy | Indian businesses, budget option |

**Quick recommendation:**
- Learning automation? Start with **Zapier** (easiest to understand)
- Need complex workflows? Use **Make.com** (more powerful, cheaper)
- Developer or tight budget? Try **n8n** (free, self-hosted)
- Already using HubSpot CRM? Use **HubSpot Workflows**

---

## Zapier Deep Dive

Zapier is the most beginner-friendly automation tool. It connects 6,000+ apps and lets you build automations without writing a single line of code.

### Key Concepts

| Term | Meaning | Example |
|------|---------|---------|
| **Zap** | One complete automation | "When a form is submitted, send an email" |
| **Trigger** | The event that starts the automation | "New form submission in Google Forms" |
| **Action** | What happens after the trigger | "Send an email via Gmail" |
| **Filter** | A condition that must be true | "Only if the city is Mumbai" |
| **Path** | Different actions based on conditions | "If budget > ₹50K → assign to senior sales; else → assign to junior" |
| **Task** | One action execution (Zapier counts these for billing) | Sending one email = 1 task |

### How Zapier Works — Step by Step

```
TRIGGER (Something happens)
  ↓
FILTER (Should we continue? Check a condition)
  ↓
ACTION 1 (Do something)
  ↓
ACTION 2 (Do something else)
  ↓
PATH (If this → do A; If that → do B)
```

### Your First Zap — Form to Email to Sheet

1. **Trigger:** New submission in Google Forms
2. **Action 1:** Send a welcome email via Gmail
3. **Action 2:** Add a row in Google Sheets with the form data

This takes 5 minutes to set up and runs forever without any manual work.

---

## 10 Essential Marketing Automations

These are the automations every digital marketer should set up. They save hours of manual work every week.

| # | Automation | Trigger | Actions | Tools Used |
|---|-----------|---------|---------|------------|
| 1 | **New Lead Welcome** | Form submitted | Send welcome email + add to CRM | Google Forms → Gmail → HubSpot |
| 2 | **Lead to CRM + Sales Alert** | Form submitted | Add contact to CRM, notify sales on Slack | Typeform → Zoho CRM → Slack |
| 3 | **Cart Abandonment Recovery** | Cart abandoned (1 hour) | Send 3-email sequence over 3 days | Shopify → Mailchimp (3-step) |
| 4 | **Webinar Registration** | Webinar signup | Confirmation email + 3 reminders (1 day, 1 hour, 5 min before) | Zoom → Gmail → Google Calendar |
| 5 | **Blog to Social Media** | New blog published | Auto-post to LinkedIn, Twitter, Facebook | WordPress → Buffer/Hootsuite |
| 6 | **Review Notification** | New Google review | Slack notification to team | Google Business → Slack |
| 7 | **Invoice Thank You** | Invoice marked paid | Send thank-you WhatsApp | Razorpay → WhatsApp API |
| 8 | **Hot Lead Assignment** | Lead score > 80 | Assign to senior sales rep + send alert | HubSpot → Gmail → Slack |
| 9 | **Birthday Coupon** | Contact birthday (from CRM) | Send discount coupon email | HubSpot → Mailchimp |
| 10 | **Unsubscribe Feedback** | Email unsubscribe | Send feedback survey | Mailchimp → Typeform → Sheets |

> **Pro Tip:** Start with automation #1 (New Lead Welcome) — it is the easiest to set up and has the highest immediate impact. A lead that gets a response within 5 minutes is 10x more likely to convert than one that waits an hour.

---

## Multi-Step Workflows with If/Then Logic

Real-world automations are rarely just "trigger → action." They need decision-making — different paths based on conditions.

**Example: E-commerce order follow-up**

```
Trigger: Customer places order on Shopify
  ↓
Action: Send order confirmation email
  ↓
Wait: 7 days (for delivery)
  ↓
Filter: Was the order delivered?
  ├── YES → Send "Rate your experience" email
  │            ↓
  │          Wait: 3 days
  │            ↓
  │          Filter: Did they leave a review?
  │            ├── YES → Send thank-you coupon (10% off next order)
  │            └── NO → Send gentle reminder
  │
  └── NO → Alert support team on Slack
```

**Example: Lead qualification for a Hyderabad real estate company**

```
Trigger: Lead fills inquiry form on website
  ↓
Action: Add to CRM with tag "New Lead"
  ↓
Path: What is the budget?
  ├── Budget > ₹1 Crore → Tag as "Premium"
  │     → Assign to senior agent
  │     → Send luxury project brochure
  │
  ├── Budget ₹50L-1Cr → Tag as "Mid-Range"
  │     → Assign to regular agent
  │     → Send 3-bedroom options
  │
  └── Budget < ₹50L → Tag as "Budget"
        → Add to email nurture sequence
        → Send affordable project catalog
```

---

## Make.com (Formerly Integromat)

Make.com is more powerful than Zapier for complex workflows. It uses a visual drag-and-drop interface where you can see your entire automation as a flowchart.

**Make.com vs Zapier:**

| Feature | Zapier | Make.com |
|---------|--------|----------|
| Interface | Step-by-step list | Visual flowchart |
| Free Tier | 100 tasks/month | 1,000 operations/month |
| Complexity | Simple to medium | Simple to very complex |
| Branching | Paths (limited) | Routers (unlimited branches) |
| Pricing (Paid) | ₹1,500/month (750 tasks) | ₹750/month (10,000 operations) |
| Error Handling | Basic retry | Advanced (custom error routes) |
| Scheduling | Every 1-15 minutes | Every 1 minute to custom |
| Learning Curve | 30 minutes to first Zap | 1-2 hours to first scenario |

**When to choose Make.com over Zapier:**
- You need more than 3 steps in your automation
- You want to process data (format dates, calculate prices, merge fields)
- You need conditional branching with multiple paths
- Budget matters — Make.com gives 10x more operations for the same price

---

## n8n — The Free Open-Source Option

n8n is a free, self-hosted automation tool. You install it on your own server, and there are no limits on tasks or workflows.

**Best for:**
- Developers who can set up a server
- Businesses with high automation volume (saves thousands in Zapier/Make costs)
- Companies with data privacy requirements (everything runs on your server)

**Cost comparison (10,000 tasks per month):**

| Tool | Monthly Cost | Annual Cost |
|------|-------------|-------------|
| Zapier | ₹4,000-8,000 | ₹48,000-96,000 |
| Make.com | ₹750-1,500 | ₹9,000-18,000 |
| n8n (self-hosted) | ₹500-1,000 (server cost only) | ₹6,000-12,000 |
| n8n (cloud) | ₹1,500/month | ₹18,000 |

---

## ROI of Marketing Automation

Here is how to calculate the return on investment for automation:

**Example: A D2C brand in Jaipur selling organic skincare**

| Metric | Before Automation | After Automation |
|--------|------------------|-----------------|
| Time to respond to new leads | 4-6 hours | Under 2 minutes |
| Leads followed up | 60% (rest forgotten) | 100% (automated) |
| Cart recovery rate | 0% (no system) | 12% (3-email sequence) |
| Hours spent on repetitive tasks/week | 15 hours | 2 hours |
| Revenue from recovered carts (monthly) | ₹0 | ₹45,000 |
| Automation tool cost (monthly) | ₹0 | ₹2,500 |

**Net gain:** 13 hours of time saved per week + ₹42,500 additional monthly revenue.

> **Real Example:** Lenskart uses automation to send personalized reminders when your prescription is about to expire, recommend new frames based on your face shape data, and trigger re-engagement emails if you have not visited in 90 days. This automation drives crores in repeat purchases annually.

---

## Trainer Activity: Build a 3-Step Zapier Automation

**Time:** 20 minutes

**Task:** Using free Zapier accounts (sign up at zapier.com), build this automation live in class:

**Trigger:** New Google Form submission (create a simple "Contact Us" form)
**Action 1:** Send a confirmation email via Gmail to the person who submitted
**Action 2:** Add a new row in Google Sheets with the form data

**Steps:**
1. Create a Google Form with fields: Name, Email, Phone, Message
2. Create a Google Sheet with matching columns
3. In Zapier, create a new Zap
4. Set trigger: Google Forms → New Response
5. Add action 1: Gmail → Send Email (to the form submitter's email)
6. Add action 2: Google Sheets → Create Spreadsheet Row
7. Test the Zap by submitting the form

**Discussion after:** How would you extend this automation? (Add a Slack notification? Schedule a follow-up email for 2 days later? Add to a CRM?)

---

## Summary

- Marketing automation means **software doing repetitive tasks** so you focus on strategy
- **Zapier** is easiest for beginners; **Make.com** is better value for complex workflows; **n8n** is free and self-hosted
- Every marketer should set up at least **3 essential automations**: lead welcome, cart recovery, and review notifications
- Multi-step workflows use **if/then logic** to route leads and customize responses
- Make.com gives **10x more operations** than Zapier at the same price point
- Automation saves **15+ hours per week** of manual, repetitive work
- **Cart abandonment recovery** alone can add ₹40,000-50,000/month in recovered revenue for a small e-commerce brand
- Start simple with **one automation**, test it, then build more — do not try to automate everything at once
- The ROI of automation is not just money — it is **consistency** (the machine never forgets to follow up)

---

*TechPath Academy — Digital Marketing with Generative AI*
