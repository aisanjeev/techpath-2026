# AI Tools — Build Real Things with AI

**Module 07 — AI Tools Practical Mastery | Hands-On Projects**

---

## Why This Matters

> Knowing that ChatGPT exists is not a skill. Building a customer FAQ bot, generating a complete website, creating marketing content for a real business — these are skills companies pay for. This chapter gives you 5 projects that prove you can use AI productively.

---

## Project 1: AI-Powered Business Proposal

### Scenario

You're freelancing and a client asks for a business proposal for their new chai cafe. Use AI to create a professional proposal in 30 minutes instead of 3 hours.

### Step-by-Step with AI

**Prompt 1 — Research:**
```
You are a food & beverage business consultant. I'm opening a chai cafe 
called "Chai Adda" in Koramangala, Bangalore. Target: college students 
and young professionals (age 18-30). Budget: Rs 8 lakhs.

Give me:
1. Top 5 competitors in the area with their USP
2. What makes a chai cafe successful
3. Estimated monthly costs breakdown
4. Revenue projections for first 6 months
Format as tables wherever possible.
```

**Prompt 2 — Menu Design:**
```
Create a menu for Chai Adda with these sections:
- Classic Chai (5 varieties with Indian names)
- Special Chai (5 creative flavors)
- Snacks (8 items, Indian street food)
- Cold Beverages (4 items)

For each item include: Name, short description (max 10 words), price in ₹.
Format as a clean menu card layout.
```

**Prompt 3 — Social Media Content:**
```
Write 7 Instagram posts for Chai Adda's launch week.
Each post needs:
- Caption (under 100 words, include emojis)
- 5 hashtags (mix of popular and niche)
- Suggested image description (I'll generate with AI)
Day 1: Teaser, Day 2: Behind the scenes, Day 3: Menu reveal,
Day 4: Soft launch invite, Day 5: Customer reactions,
Day 6: Special offer, Day 7: Thank you post
```

> 🖼️ **IMAGE:** A mock Instagram feed showing 4 post cards for "Chai Adda" — each with a placeholder image area, caption preview below, and engagement metrics — illustrating what the AI-generated social media plan looks like when executed
> `ai-project-chai-adda-insta.png`

**What this teaches:** Using AI to multiply your productivity — what would take a marketing team 2 days, you did in 30 minutes. This is why companies hire people who can use AI tools.

---

## Project 2: Custom Chatbot for a Business

### Scenario

Build an FAQ chatbot for a computer training institute (like TechPath!) using ChatGPT or Claude.

### Step-by-Step

**Step 1: Define the knowledge base**

Write a "system prompt" that tells the AI everything about the business:

```
You are the AI assistant for TechPath Institute, an IT training center.

About TechPath:
- Location: Pune, Maharashtra
- Courses: ADCA (12 months, ₹35,000), DCA (6 months, ₹18,000), Tally (3 months, ₹8,000)
- Timings: Morning batch 9-12, Evening batch 5-8
- Labs: 30 computers, AC classrooms
- Placement: 85% placement rate, partner companies: TCS, Infosys, local IT firms
- Faculty: 5 trainers, all industry experienced
- Contact: 9876543210, info@techpath.biz

Rules:
- Be friendly and helpful
- Answer in English and Hindi (based on user's language)
- If you don't know something, say "Let me connect you with our counselor at 9876543210"
- When someone asks about fees, also mention the EMI option
- Always end with "Any other questions?"
```

**Step 2: Test with real questions**

| Customer asks | Bot should answer |
|--------------|-------------------|
| "What courses do you have?" | List all 3 courses with duration and fees |
| "Placement milega?" | "Yes! 85% placement rate..." |
| "Timing kya hai?" | Morning 9-12 and Evening 5-8 |
| "Fees jyada hai, discount?" | Mention EMI option, ask to call counselor |
| "Do you teach Python?" | Yes, covered in ADCA course, modules 10-11 |

**Step 3: Handle edge cases**

| Customer asks | Expected behavior |
|--------------|-------------------|
| "What's the weather today?" | "I can only help with TechPath queries..." |
| "Are you a real person?" | "I'm TechPath's AI assistant. For detailed queries, talk to our counselor..." |
| Abusive language | "I'm here to help! Let me connect you with our team..." |

---

## Project 3: AI Image Generation Portfolio

### Create 5 Professional Images Using AI

Use Canva AI, Microsoft Designer, or DALL-E to generate:

**Image 1: Business Logo**
```
Prompt: "Minimal modern logo for a tech company called 'CodeCraft'. 
Use a geometric code bracket symbol, dark blue and electric green colors, 
clean sans-serif font, white background, professional corporate style"
```

**Image 2: Social Media Banner**
```
Prompt: "LinkedIn banner for a web developer. Minimalist dark gradient 
background with subtle code elements, text area on right side for name, 
modern tech aesthetic, 1584x396 pixels"
```

**Image 3: Product Mockup**
```
Prompt: "Realistic mockup of a mobile app on iPhone 15 Pro, food delivery 
app showing restaurant listings, held in hand, blurred cafe background, 
professional photography style"
```

**Image 4: Presentation Background**
```
Prompt: "Abstract geometric background for business presentation, 
dark navy blue with subtle gradient to purple, low-poly style, 
professional, widescreen 16:9 ratio, space for text in center"
```

**Image 5: Blog Thumbnail**
```
Prompt: "Blog post thumbnail for article about Python programming, 
minimalist illustration of a Python snake made of code characters, 
flat design, yellow and blue colors, modern tech blog style"
```

> 🖼️ **IMAGE:** A 2x3 grid showing the 5 AI-generated images described above (placeholder boxes with descriptions), demonstrating the variety of visual content AI can create
> `ai-image-generation-portfolio.png`

### Image Prompt Formula

```
Subject + Style + Colors + Mood + Technical Details
```

**Bad:** "A dog"
**Good:** "Golden retriever puppy sitting in autumn leaves, soft bokeh background, warm golden hour lighting, shot on Canon 85mm lens, professional pet photography"

---

## Project 4: AI-Powered Data Analysis Report

### Scenario

Your manager gives you an Excel file with 6 months of sales data and says "Give me insights by 4 PM."

### Step-by-Step

**Step 1:** Copy the data (or describe it) and paste into ChatGPT/Claude

```
Here's our last 6 months sales data:

Month   | Revenue    | Orders | Returns | New Customers
Jan 26  | 12,50,000  | 340    | 15      | 45
Feb 26  | 14,30,000  | 380    | 22      | 52
Mar 26  | 11,80,000  | 310    | 18      | 38
Apr 26  | 16,20,000  | 420    | 12      | 68
May 26  | 15,70,000  | 395    | 19      | 55
Jun 26  | 18,50,000  | 480    | 8       | 72

Analyze this data and give me:
1. Key trends (what's growing, what's concerning)
2. Growth rates month-over-month
3. Return rate analysis
4. Customer acquisition cost if marketing spend was ₹2L/month
5. Forecast for Jul-Sep based on the trend
6. Top 3 recommendations

Format as a professional report with sections and tables.
```

**Step 2:** Ask AI to create charts

```
Now create Python code using matplotlib to make:
1. Revenue trend line chart (with ₹ formatting on Y-axis)
2. Orders vs Returns bar chart
3. New customer growth line chart

Use a professional dark theme. Save as PNG files.
```

**Step 3:** Ask for executive summary

```
Write a 3-paragraph executive summary of this analysis 
for the CEO. No jargon. Focus on: what's working, what needs 
attention, and what we should do next quarter.
```

**What this teaches:** AI doesn't replace your analytical thinking — it speeds up the execution. The real skill is knowing what questions to ask and which insights matter.

---

## Project 5: AI Course Content Creator

### Scenario

You need to create training material for a 1-hour workshop on "Excel for Beginners."

### Use AI to Generate

```
Create a complete 1-hour workshop plan on "Excel for Beginners" 
for college students with no prior experience.

Include:
1. Slide-by-slide outline (15-18 slides, what each slide shows)
2. 5 hands-on exercises (progressively harder)
3. A quiz with 10 questions (MCQ with answers)
4. A one-page cheat sheet students can take home
5. 3 real-world scenarios to demonstrate ("Your boss asks you to...")

Rules:
- Simple language, no jargon
- Use Indian examples (₹, Indian names, local context)
- Each exercise should take 5-7 minutes max
```

Then use:
- **Canva AI** or **Gamma.app** to generate the slides from the outline
- **ChatGPT/Claude** to write detailed speaker notes
- **AI image tools** to create exercise screenshots

---

## AI Workflow Cheat Sheet for Different Jobs

| Job Role | AI Tool | What To Do |
|----------|---------|------------|
| **Content Writer** | ChatGPT/Claude | Draft → Edit → Humanize → Publish |
| **Web Developer** | Cursor/Copilot | Generate boilerplate → Customize → Debug |
| **Data Analyst** | ChatGPT + Python | Paste data → Ask for insights → Generate charts |
| **Designer** | Canva AI + Midjourney | Generate concepts → Refine in Canva → Export |
| **Marketing** | ChatGPT + Canva | Content calendar → Captions → Social graphics |
| **HR** | ChatGPT | Job descriptions → Interview questions → Onboarding docs |
| **Sales** | ChatGPT | Proposals → Cold emails → Client follow-ups |
| **Support** | ChatGPT/Claude | FAQ bot → Ticket categorization → Response templates |

> 🖼️ **IMAGE:** A flowchart showing the "AI-Assisted Work" process: Idea → AI Draft (fast, 80% done) → Human Review (catch errors, add context) → Refine with AI (feedback loop) → Final Output — with "human in the loop" emphasized at each review step
> `ai-assisted-workflow.png`

---

## What NOT to Do with AI (Common Mistakes)

| Mistake | Why It's Bad | Do This Instead |
|---------|-------------|-----------------|
| Copy-paste AI output directly | Sounds generic, may have errors | Edit, add your voice, verify facts |
| Trust AI numbers blindly | AI can hallucinate statistics | Cross-check all data and claims |
| Use AI for final answers | AI is a draft tool, not truth | Use as starting point, refine yourself |
| Ignore AI limitations | Each model has knowledge cutoffs | Check dates, verify current information |
| Share confidential data | AI providers may train on your data | Remove sensitive info before pasting |
