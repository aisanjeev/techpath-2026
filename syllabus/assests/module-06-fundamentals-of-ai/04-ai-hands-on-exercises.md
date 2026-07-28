# AI — Hands-On Exercises & Real-World Applications

**Module 06 — Fundamentals of AI | Practice & Understanding**

---

## Why This Matters

> Saying "I know about AI" is worth nothing in 2026. Saying "I used Claude API to build a student FAQ bot that handles 50+ question types" gets you hired. This chapter bridges the gap between AI theory and doing something useful with it.

---

## Exercise 1: AI in Your Daily Life — Identification Map

### Task

For one full day, notice and write down every time you interact with AI. Most people don't realize they use AI 20-50 times daily.

| Time | App/Service | AI Feature | AI Type |
|------|------------|------------|---------|
| 7:00 AM | Phone alarm | Smart alarm (learns sleep pattern) | ML |
| 7:15 AM | Google Maps | Traffic prediction, route suggestion | ML + Real-time data |
| 7:30 AM | Instagram | Feed algorithm, face filters | Recommendation + Computer Vision |
| 8:00 AM | Gmail | Spam filter, smart compose | NLP + Classification |
| 8:30 AM | Spotify | Discover Weekly playlist | Recommendation system |
| 9:00 AM | Google Search | Search ranking, autocomplete | NLP + Ranking |
| 10:00 AM | Paytm/GPay | Fraud detection on transaction | Anomaly detection |
| 12:00 PM | Swiggy/Zomato | Restaurant recommendations, ETA | ML + Optimization |
| 3:00 PM | YouTube | Video recommendations | Recommendation + NLP |
| 6:00 PM | Netflix | "Because you watched..." | Collaborative filtering |
| 9:00 PM | Phone keyboard | Autocorrect, next word prediction | NLP |

> 🖼️ **IMAGE:** A visual "AI in daily life" infographic — a clock/timeline showing 24 hours with icons around it (phone, maps, email, music, food delivery, shopping, streaming) — each with a short label of the AI used
> `ai-daily-life-timeline.png`

---

## Exercise 2: Understanding ML Types — Sorting Challenge

### Classify each example as Supervised, Unsupervised, or Reinforcement Learning

| # | Example | Your Answer | Correct Answer |
|---|---------|-------------|----------------|
| 1 | Email spam filter (trained on labeled spam/not-spam) | ___ | Supervised |
| 2 | Netflix grouping users by viewing habits | ___ | Unsupervised |
| 3 | Self-driving car learning to stay in lane | ___ | Reinforcement |
| 4 | Doctor diagnosis tool trained on X-ray images | ___ | Supervised |
| 5 | Customer segmentation for marketing | ___ | Unsupervised |
| 6 | YouTube recommendations based on your history | ___ | Supervised |
| 7 | Robot learning to walk through trial and error | ___ | Reinforcement |
| 8 | Predicting house prices from area, rooms, location | ___ | Supervised |
| 9 | Detecting unusual credit card transactions | ___ | Unsupervised (anomaly detection) |
| 10 | Chess-playing AI (AlphaZero) | ___ | Reinforcement |
| 11 | Sorting news articles into categories | ___ | Supervised |
| 12 | Finding patterns in customer purchase data | ___ | Unsupervised |

### How to Remember

```
Supervised   = Teacher gives answer key. "This is spam, this is not."
Unsupervised = No answer key. "Find patterns yourself."
Reinforcement = Trial and error + rewards. "Good move! Bad move!"
```

> 🖼️ **IMAGE:** Three-column visual — Supervised (teacher with labeled examples), Unsupervised (magnifying glass over unlabeled data clusters), Reinforcement (robot with thumbs up/down feedback arrows) — each with 3 bullet point examples underneath
> `ml-types-visual.png`

---

## Exercise 3: Prompt Engineering — 10 Practice Challenges

### The Prompt Formula

```
Role + Context + Task + Format + Constraints
```

**Bad prompt:** "Write about marketing"
**Good prompt:** "You are a digital marketing expert. I run a small bakery in Pune with a Rs 5,000 monthly marketing budget. Write a 30-day social media plan for Instagram. Format as a table with columns: Day, Post Type, Caption Idea, Hashtags. Focus on local customers within 5km radius."

### Challenge 1: Resume Bullet Point Improver
```
Task: Take a weak resume bullet and make it strong.

Input: "Worked on a website"

Your prompt should ask the AI to:
- Add specific tech stack
- Add a measurable outcome
- Use action verbs
- Keep it under 2 lines

Expected output:
"Built a responsive e-commerce website using React and Node.js,
 increasing online orders by 40% in the first quarter."
```

### Challenge 2: Email Writer
```
Scenario: You need to email your professor asking for a deadline extension.

Write a prompt that gives AI:
- Your role (student)
- Context (project delay reason)
- Tone (respectful, professional)
- Constraints (under 100 words, formal)
```

### Challenge 3: Data Analyzer
```
Scenario: You have monthly sales data in a table.

Write a prompt that asks AI to:
- Identify the best and worst performing months
- Calculate growth rate
- Suggest 3 reasons for any decline
- Recommend actions for next quarter
- Format as executive summary with bullet points
```

### Challenge 4: Code Debugger
```
Scenario: Your Python code has a bug.

Write a prompt that:
- Shares the code
- Describes what it should do
- Describes what it actually does (the error)
- Asks for fix + explanation of what went wrong
```

### Challenge 5: Meeting Notes Summarizer
```
Write a prompt that converts raw meeting notes into:
- 3-line executive summary
- Action items table (Task, Owner, Deadline)
- Key decisions made
- Open questions for next meeting
```

### Challenges 6-10: Try These Yourself

6. **Product Description Writer** — Write selling descriptions for an online store
7. **Interview Question Generator** — Generate technical questions for a specific role
8. **Study Notes Creator** — Convert a textbook chapter into concise study notes
9. **API Documentation Writer** — Document a REST API endpoint
10. **Bug Report Writer** — Convert a vague "it's broken" into a proper bug report

---

## Exercise 4: AI Ethics Scenarios — Think and Discuss

For each scenario, answer: Is this ethical? Who could be harmed? What safeguards should exist?

### Scenario 1: Hiring AI
A company uses AI to screen resumes. The AI was trained on data of previously successful employees (mostly male, mostly from Tier-1 colleges). Now it rejects most female candidates and non-Tier-1 graduates.

**Think about:**
- Is the AI biased or is the data biased?
- Who is harmed?
- How could this be fixed?

### Scenario 2: Deepfake Detection
A student uses AI to generate a fake video of their principal saying "School is canceled tomorrow" and shares it on WhatsApp.

**Think about:**
- What laws does this violate?
- What's the real-world impact?
- How can deepfakes be detected?

### Scenario 3: AI Content in Assignments
A student uses ChatGPT to write their entire exam project. They submit it as their own work.

**Think about:**
- Is using AI for learning different from using AI to cheat?
- Where's the line between "AI-assisted" and "AI-generated"?
- What's the right policy for educational use of AI?

### Scenario 4: Medical AI
An AI diagnoses a patient's X-ray as "no cancer." The doctor, trusting the AI, doesn't look closely. The patient actually has cancer, and the late diagnosis reduces survival chances.

**Think about:**
- Should AI replace doctors or assist them?
- Who is responsible — the AI company, the doctor, or the hospital?
- What safeguards should exist?

---

## Exercise 5: Build an AI-Powered Mini Tool

### Tool: Smart Study Planner

Using ChatGPT or Claude, build a study planner through conversation:

**Step 1:** Tell the AI your exam subjects, dates, and current preparation level
**Step 2:** Ask it to create a day-by-day study schedule
**Step 3:** Ask it to generate 5 practice questions per subject
**Step 4:** After "studying," ask it to quiz you and evaluate your answers
**Step 5:** Ask it to adjust the plan based on your weak areas

This exercise teaches you to use AI as a **thinking partner**, not just a content generator.

---

## Key Concepts to Remember for Interviews

### "Explain AI vs ML vs DL vs GenAI"

```
AI (Artificial Intelligence)
└── ML (Machine Learning) — learns from data
    └── DL (Deep Learning) — learns using neural networks
        └── GenAI (Generative AI) — creates new content
            └── LLMs (Large Language Models) — understands & generates text
                └── ChatGPT, Claude, Gemini
```

> 🖼️ **IMAGE:** Nested circles/layers diagram — outermost circle is "AI" (largest), inside it "ML", inside that "DL", inside that "GenAI", innermost "LLMs" — each layer labeled with a one-line definition and 2-3 example tools/techniques
> `ai-ml-dl-genai-layers.png`

### "What are hallucinations in AI?"

When AI generates confident-sounding but **factually wrong** information.

**Example:** You ask "Who won the 2024 Nobel Prize in Chemistry?" and the AI names someone who doesn't exist.

**Why it happens:** AI predicts the next most likely word, not the most truthful word.

**How to handle:** Always verify AI outputs with reliable sources, especially for facts, dates, names, statistics, and code.

### "What are tokens?"

Tokens are how AI reads text — roughly 1 token = 3/4 of a word (in English).

```
"Hello, how are you?" = 6 tokens
"Namaste, aap kaise hain?" = 9 tokens (non-English uses more)
1000 tokens ≈ 750 words
```

Context window = how many tokens the AI can "remember" in one conversation.
- GPT-4: 128K tokens (~96,000 words)
- Claude: 200K tokens (~150,000 words)
