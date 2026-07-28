# Choosing Your Capstone Project Idea

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 1**

---

## Why the Right Idea Matters

Your capstone project is the crown jewel of your portfolio. It is the first thing recruiters and hiring managers will look at. Choosing the right idea is not about picking the flashiest technology — it is about picking a real problem, solving it well, and shipping a working product in four weeks.

Think of it like choosing what restaurant to open. You would not open a French fine-dining place in a small town where everyone eats dosa and idli. You would pick a cuisine you understand, in a location where people are hungry for it, and at a price they can afford. Your capstone idea works the same way — pick what you know, what solves a real problem, and what you can actually build in the time you have.

---

## Step 1: Brainstorming Techniques

Before you judge any idea, generate as many as you can. Quantity comes first, quality comes later.

### Technique 1: Problem-First Thinking

Write down 10 problems you or people around you face daily. Do not think about technology yet.

| Problem | Who faces it? | How do they solve it now? |
|---------|--------------|--------------------------|
| Students cannot find past exam papers easily | College students in Bhopal | WhatsApp groups, photocopies |
| Freelancers struggle to track invoices | Freelancers in Pune | Excel sheets, paper bills |
| Small grocery stores have no online presence | Kirana store owners in Delhi | Word of mouth, phone calls |
| Job seekers do not get resume feedback | Fresh graduates in Bangalore | Ask friends, no structured feedback |
| Coaching classes cannot manage attendance | Coaching center owners in Mumbai | Paper registers |

### Technique 2: "I Wish This Existed" List

Think about apps or tools you wished existed but could not find. Ask your friends and family the same question.

### Technique 3: Improve Something Broken

Pick an existing app or service that frustrates you. What would you do differently? A simpler UI? Better search? An AI feature that is missing?

### Technique 4: Combine Two Things

Take two unrelated ideas and combine them. "LinkedIn + AI resume review" becomes a smart career platform. "Zomato + meal planning" becomes a diet-aware food ordering app.

---

## Step 2: Validating Your Idea

Not every idea is worth building. Use this validation checklist before you commit.

### The REAL Test

| Criteria | Question | Good Sign | Bad Sign |
|----------|----------|-----------|----------|
| **R**eal Problem | Does this solve an actual pain point? | People complain about this regularly | "It would be cool if..." |
| **E**xisting Users | Can you name 5 people who would use this? | Yes, and they confirmed it | You are the only user |
| **A**chievable | Can you build an MVP in 4 weeks? | Core feature is 2-3 pages | Needs 20+ pages to be useful |
| **L**earnable | Does building this teach you new skills? | Uses full-stack + AI | Only uses HTML/CSS |

### Questions to Ask Yourself

1. Can I explain this idea in one sentence?
2. What is the ONE core feature that makes this useful?
3. Does it need AI, or am I adding AI just for the sake of it?
4. Can I get test data for this easily?
5. Is this idea too similar to a tutorial project?

---

## Step 3: Scope Assessment — MVP vs Full Product

The biggest mistake capstone students make is trying to build everything. You are not building the next Flipkart. You are building a working MVP (Minimum Viable Product) that demonstrates your skills.

### What is MVP?

An MVP is the smallest version of your product that delivers value. It has just enough features to be useful and demonstrate your technical ability.

### Scope Comparison

| Feature | MVP (Build This) | Full Product (Skip This) |
|---------|-------------------|--------------------------|
| User auth | Email + password login | Google, Facebook, OTP login |
| Search | Basic text search | AI-powered semantic search with filters |
| Payments | Show pricing page | Full Razorpay integration |
| Admin panel | Simple CRUD dashboard | Role-based access, analytics |
| AI feature | One focused AI feature (chatbot OR summarizer) | Multiple AI agents working together |
| Deployment | Single server deploy | Kubernetes, load balancing, CDN |

### The 4-Week Rule

If you cannot build the core feature in Week 1 and spend Weeks 2-4 polishing, integrating AI, adding tests, and deploying — the scope is too large. Cut features, not corners.

---

## Step 4: Indian Market Project Ideas

Here are proven project ideas that work well for capstone projects in the Indian context.

### Tier 1: Recommended (Well-Scoped, Impressive)

| Project Idea | Core Feature | AI Feature | Complexity |
|-------------|-------------|------------|------------|
| Student Exam Portal | Upload/search past papers by subject | AI-powered question paper summarizer | Medium |
| Freelancer Invoice Manager | Create, send, track invoices in INR | AI expense categorizer | Medium |
| Kirana Store Online Catalog | Product listing + WhatsApp order button | AI product description generator | Medium |
| Resume Review Platform | Upload resume, get structured feedback | AI resume scorer + suggestions | Medium-High |
| Course Recommendation System | Browse courses, get recommendations | RAG-based course chatbot | Medium-High |

### Tier 2: Ambitious but Achievable

| Project Idea | Core Feature | AI Feature | Complexity |
|-------------|-------------|------------|------------|
| Code Learning Platform | Interactive coding challenges | AI code review assistant | High |
| Local Event Finder | List/search events in your city | AI event recommendation based on interests | High |
| Meal Planning App | Weekly meal planner with Indian recipes | AI nutrition advisor | High |

### Tier 3: Too Ambitious for 4 Weeks (Avoid)

- Full e-commerce platform with payments
- Social media clone
- Real-time multiplayer game
- Video streaming platform

---

## Step 5: Defining Success Criteria

Before you start coding, write down what "done" looks like. This prevents scope creep and gives you a clear finish line.

### Example: Student Exam Portal

```
Project: Student Exam Portal
Success Criteria:
1. User can sign up and log in
2. User can upload a PDF exam paper with subject, year, and college tags
3. User can search papers by subject and year
4. AI feature: User can ask questions about a paper and get AI-generated summaries
5. Admin can approve/reject uploaded papers
6. App is deployed and accessible via a public URL
7. README with setup instructions exists
8. At least 10 backend tests pass
```

### Writing Your Own Success Criteria

Use this template:

```
Project: [Your Project Name]

Must Have (Week 1-2):
1. [Core feature 1]
2. [Core feature 2]
3. [User authentication]

Should Have (Week 3):
4. [AI feature]
5. [Search/filter functionality]
6. [Basic admin panel]

Nice to Have (Week 4, if time permits):
7. [Extra polish feature]
8. [Email notifications]
```

---

## Step 6: Time Estimation for the 4-Week Capstone

Rahul, a student from Bhopal, planned his capstone like this:

| Week | Focus | Deliverables |
|------|-------|-------------|
| Week 1 | Backend + Database | Models, APIs, auth, database migrations, test data |
| Week 2 | Frontend + Integration | UI pages, API integration, form validation |
| Week 3 | AI Feature + Testing | AI integration, unit tests, API tests, bug fixes |
| Week 4 | Deploy + Document + Demo | CI/CD pipeline, deployment, README, demo prep |

### Time Allocation Per Day (Assuming 4-5 hours/day)

| Activity | Time |
|----------|------|
| Coding new features | 2-3 hours |
| Debugging and testing | 1 hour |
| Documentation and commits | 30 minutes |
| Learning/research for blockers | 30 minutes |

### Common Time Traps

| Trap | How to Avoid |
|------|-------------|
| Spending 3 days on CSS | Use Tailwind CSS — pick a template and move on |
| Rewriting code from scratch | Plan your models and API before writing code |
| Perfectionism on AI feature | Get a basic version working first, then improve |
| Not deploying until the last day | Deploy in Week 1 with a basic "Hello World" page |

---

## Final Checklist Before You Start

Before you write a single line of code, make sure you can check every box:

| Check | Status |
|-------|--------|
| I can explain my project in one sentence | _ |
| I have identified the ONE core feature | _ |
| I know what AI feature I will add | _ |
| I have written success criteria | _ |
| I have a 4-week plan | _ |
| I have chosen my tech stack | _ |
| I have created a GitHub repo with a README | _ |

Once all boxes are checked, you are ready to move to Topic 2 and set up your backend.

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
