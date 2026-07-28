# Module 5: Assignment — Email, WhatsApp, Marketing Automation & CRM

**Total Marks:** 100
**Submission Deadline:** End of Week 25
**Format:** Submit all deliverables as a single Google Drive folder link

---

## Task 1: Design a Lead Magnet and Opt-In Landing Page (30 Marks)

### Objective
Create a professional lead magnet PDF and a landing page that converts visitors into email subscribers.

### What to Do

**Part A: Create the Lead Magnet PDF (15 marks)**

Design a 5-7 page PDF titled: **"10 Free Tools Every Small Business in India Should Use"**

Your PDF must include:
- Professional cover page with title and TechPath Academy branding
- Table of contents
- 10 tools listed with: tool name, what it does, who it's for, pricing (free tier), and a quick-start tip
- Tools should span categories: social media, design, accounting, communication, analytics
- Final page with CTA (Call to Action) directing readers to your course/service
- Clean design (use Canva or Google Slides exported as PDF)

**Tools to consider including:** Canva, Google Analytics, WhatsApp Business, Zoho Invoice, Buffer, Google My Business, MailerLite, Trello, Razorpay, ChatGPT

**Part B: Create an Opt-In Landing Page (15 marks)**

Build a landing page using MailerLite or Carrd.co that includes:
- Clear headline communicating the benefit (e.g., "Get 10 Free Tools That Will Save You 5 Hours Every Week")
- Sub-headline explaining who this is for
- Mockup image of the PDF (create in Canva)
- 3-4 bullet points listing what's inside
- Email opt-in form (Name + Email fields only)
- Social proof element (e.g., "Downloaded by 500+ business owners")
- Trust elements (no spam promise, privacy note)

### Grading Criteria
| Criteria | Marks |
|----------|-------|
| PDF content quality and relevance to Indian businesses | 8 |
| PDF design (professional, readable, branded) | 7 |
| Landing page headline and copy | 5 |
| Landing page design and mobile responsiveness | 5 |
| Form setup and integration with email tool | 3 |
| Overall presentation | 2 |

---

## Task 2: Write a 7-Email Welcome Sequence (25 Marks)

### Objective
Write a complete 7-email welcome sequence for a hypothetical online clothing store called "StyleKart" (an Indian ethnic and western wear brand targeting women aged 22-35 in Tier-1 and Tier-2 cities).

### What to Do

For EACH of the 7 emails, write:

1. **Subject Line** (with an A/B alternative)
2. **Preview Text** (the text shown after subject line in inbox — max 60 characters)
3. **Email Body** (full copy, 150-300 words per email)
4. **CTA** (button text and where it links to)
5. **Send Timing** (when this email goes out relative to signup)

### Email Sequence Structure:
| Email # | Purpose | Send Timing |
|---------|---------|-------------|
| 1 | Welcome + Deliver 15% discount code | Immediately |
| 2 | Brand story — why StyleKart exists | Day 1 |
| 3 | Best sellers showcase (social proof) | Day 3 |
| 4 | Style guide / How to mix & match | Day 5 |
| 5 | Customer testimonials + UGC | Day 7 |
| 6 | Remind about discount (soft pitch) | Day 9 |
| 7 | Last chance — discount expires tomorrow | Day 11 |

### Requirements:
- Use Indian context (festival references, Indian cities, Indian names)
- Include personalization tokens where appropriate ({{first_name}}, {{city}})
- Make CTAs specific (not just "Click Here" — use action words)
- Each email should have ONE clear goal
- Subject lines should be under 50 characters

### Grading Criteria
| Criteria | Marks |
|----------|-------|
| Subject lines (compelling, A/B variants provided) | 5 |
| Preview text (adds context, not repeating subject) | 3 |
| Email body copy (clear, engaging, action-oriented) | 8 |
| CTAs (specific, compelling, correctly placed) | 4 |
| Indian context and personalization | 3 |
| Sequence flow and logic (builds towards sale) | 2 |

---

## Task 3: Build a 5-Step Zapier Automation (25 Marks)

### Objective
Create a working 5-step Zap that automates the lead capture and follow-up process.

### What to Build

**Automation Flow:**
```
Google Form Submission
    → Add to MailerLite Subscriber List (with tag "new-lead")
        → Send Welcome Email (via MailerLite)
            → Add Row to Google Sheet (lead tracker)
                → Send Slack Notification (to #new-leads channel)
```

### Step-by-Step Requirements:

**Step 1: Google Form (Trigger)**
- Create a form with fields: Full Name, Email, Phone, "How did you hear about us?" (dropdown), Interest Area (dropdown)
- The form should look professional

**Step 2: MailerLite (Action)**
- Add the form respondent as a subscriber
- Map all form fields correctly
- Add tag "new-lead" and a tag based on their Interest Area

**Step 3: MailerLite Welcome Email (Action)**
- Trigger the welcome automation in MailerLite
- OR send a specific email via Zapier's email action

**Step 4: Google Sheet (Action)**
- Add a row with: Name, Email, Phone, Source, Interest, Date/Time of submission
- Sheet should be organized with proper headers

**Step 5: Slack Notification (Action)**
- Post to a Slack channel (create a free workspace for this)
- Message format: "New Lead: [Name] from [Source] interested in [Interest Area] — [Email]"

### Submission Requirements:
- Screenshot of complete Zap (all 5 steps visible)
- Screenshot of Zap history showing at least 3 successful test runs
- Link to the Google Form
- Link to the Google Sheet (with sample data from tests)
- Brief write-up (200 words) explaining what you learned

### Grading Criteria
| Criteria | Marks |
|----------|-------|
| All 5 steps configured correctly | 10 |
| Data mapping is accurate (fields match) | 5 |
| Zap tested successfully (3+ runs shown) | 5 |
| Documentation quality | 3 |
| Error handling consideration | 2 |

---

## Task 4: Set Up HubSpot Free CRM (20 Marks)

### Objective
Set up a functional CRM with a sales pipeline, sample contacts, and one automated workflow.

### What to Do

**Part A: Pipeline Setup (8 marks)**

Create a sales pipeline in HubSpot with these 5 stages:
1. **New Lead** — Just captured, not yet contacted
2. **Contacted** — Initial outreach done (email/WhatsApp/call)
3. **Meeting Scheduled** — Discovery call or demo booked
4. **Proposal Sent** — Custom quote or proposal shared
5. **Won / Lost** — Deal closed or lost (with reason)

Set realistic deal probability for each stage.

**Part B: Import Contacts (6 marks)**

Import 30 sample contacts into HubSpot. Each contact should have:
- Name (use Indian names)
- Email (use test emails)
- Phone (use Indian format: +91 XXXXX XXXXX)
- Company name
- Lead Status (New, Contacted, Qualified, Unqualified)
- Lead Source (Google, Social Media, Referral, WhatsApp, Event)
- Deal value (between Rs 5,000 and Rs 50,000)

Distribute contacts across pipeline stages:
- New Lead: 10 contacts
- Contacted: 8 contacts
- Meeting Scheduled: 5 contacts
- Proposal Sent: 4 contacts
- Won: 2 contacts, Lost: 1 contact

**Part C: Automated Workflow (6 marks)**

Create ONE automated workflow:
- **Trigger:** When a contact's lead status changes to "Qualified"
- **Action 1:** Send an internal notification email to sales team
- **Action 2:** Create a task "Schedule discovery call" with due date = 2 days
- **Action 3:** Update contact property — add "qualified-lead" tag

### Submission Requirements:
- Screenshot of pipeline view with deals in each stage
- Screenshot of contacts list showing imported contacts
- Screenshot of workflow setup (trigger + all actions)
- Screenshot of workflow execution log
- Export of contacts as CSV (from HubSpot)

### Grading Criteria
| Criteria | Marks |
|----------|-------|
| Pipeline stages configured correctly with probabilities | 4 |
| Pipeline has deals in each stage | 4 |
| 30 contacts imported with all required fields | 4 |
| Contacts distributed across stages correctly | 2 |
| Workflow trigger is correct | 2 |
| Workflow actions are logical and complete | 3 |
| Overall setup quality | 1 |

---

## Submission Checklist

Before submitting, make sure you have:

- [ ] **Task 1:** Lead magnet PDF + Landing page live URL + Screenshot
- [ ] **Task 2:** 7-email sequence document (Google Doc or PDF)
- [ ] **Task 3:** Zapier screenshots + Google Form link + Google Sheet link + Write-up
- [ ] **Task 4:** HubSpot screenshots (pipeline, contacts, workflow) + CSV export
- [ ] All files organized in a single Google Drive folder
- [ ] Google Drive folder sharing set to "Anyone with the link can view"
- [ ] Your name and batch number mentioned in the folder name

---

## Tips for Success

1. **Start early** — Task 3 requires tool setup that takes time
2. **Use free tiers** — All tools have free plans sufficient for this assignment
3. **Test everything** — Don't just set it up, make sure it actually works
4. **Screenshot often** — Document your process as you go
5. **Ask for help** — Post questions in the class WhatsApp group
6. **Think like a user** — Would YOU click on that subject line? Would YOU fill that form?
