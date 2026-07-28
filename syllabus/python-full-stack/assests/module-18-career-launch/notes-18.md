# Module 18: Career Launch & Professional Portfolio

## 1. GitHub Portfolio

Your GitHub profile is your developer resume. Recruiters and hiring managers will look at it before your actual resume.

### The 5 Pinned Repositories Strategy

Pin exactly 5 repositories that showcase your range:

| Slot | Type | Example |
|------|------|---------|
| 1 | **Capstone Project** (full-stack) | SmartAttend — FastAPI + HTMX + LangChain |
| 2 | **Backend/API Project** | REST API for a specific domain |
| 3 | **Frontend Project** | Responsive portfolio site or interactive dashboard |
| 4 | **AI/Data Project** | RAG chatbot, data analysis, or ML project |
| 5 | **Utility/Tool** | CLI tool, automation script, or open-source contribution |

### Professional README Template

Every pinned repo needs a README that sells the project in 30 seconds:

```markdown
# Project Name

> One-line description of what this does

![CI](https://github.com/username/repo/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Live Demo
https://your-deployed-app.com

## Screenshots
[Include 2-3 screenshots showing key features]

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Frontend | HTML/CSS/JS + HTMX |
| AI | LangChain + OpenAI |
| CI/CD | GitHub Actions |
| Hosting | Render |

## Quick Start
\```bash
git clone https://github.com/username/repo.git
cd repo
cp .env.example .env
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
\```

## Features
- Feature 1 with brief description
- Feature 2 with brief description
- Feature 3 with brief description

## Architecture
[Simple architecture diagram]

## Author
**Your Name** — [LinkedIn](link) | [Portfolio](link)
```

### GitHub Profile README

Create a repository with the same name as your username (e.g., `rahulsharma/rahulsharma`). Add a `README.md`:

```markdown
## Hi, I am Rahul Sharma

Full-stack Python developer from Bhopal, India.

- Currently learning: FastAPI, LangChain, Docker
- Open to: Full-time roles, internships, freelance projects
- Reach me: rahul@example.com | [LinkedIn](link)

### Tech Stack
Python | FastAPI | Django | PostgreSQL | HTML/CSS/JS | HTMX | Docker | LangChain | Git

### Featured Projects
| Project | Description | Tech |
|---------|------------|------|
| [SmartAttend](link) | Student attendance management with AI chatbot | FastAPI, LangChain |
| [JobTracker](link) | Job application tracker with analytics | Django, PostgreSQL |
| [Portfolio](link) | Personal portfolio website | HTML, CSS, JavaScript |
```

### GitHub Activity Tips

- **Commit regularly** — a green contribution graph shows consistency
- **Write good commit messages** — `"Add attendance report endpoint"` not `"update"`
- **Use branches and PRs** — shows you know professional workflows
- **Add topics/tags** to repositories — helps with discoverability
- **Star and fork** interesting projects — shows you are active in the community

---

## 2. LinkedIn for Developers

### Profile Optimization

| Section | What to Write |
|---------|--------------|
| **Headline** | "Python Full-Stack Developer | FastAPI | Django | AI/ML | Open to Opportunities" |
| **About** | 3-4 sentences: who you are, what you build, what you are looking for. Include keywords. |
| **Experience** | List projects as experience: "Full-Stack Developer — SmartAttend (Capstone Project)" |
| **Skills** | Add: Python, FastAPI, Django, PostgreSQL, REST API, Git, Docker, LangChain, SQL |
| **Projects** | Link to live demos and GitHub repos |
| **Education** | TechPath Institute — Python Full Stack Developer Course |

### About Section Example

```
Full-stack Python developer with hands-on experience building web applications
using FastAPI, Django, PostgreSQL, and LangChain. Completed a 6-month intensive
course at TechPath Institute, Bhopal, where I built SmartAttend — a student
attendance management system with an AI chatbot.

I am actively looking for full-time roles or internships where I can apply my
skills in backend development, API design, and AI integration.

Tech: Python, FastAPI, Django, PostgreSQL, HTML/CSS/JS, Docker, LangChain, Git
```

### LinkedIn Content Strategy

Post 1-2 times per week about:

| Post Type | Example |
|-----------|---------|
| Project showcase | "Built a student attendance tracker with FastAPI and LangChain. Here is what I learned..." |
| Learning update | "Just completed Module 16 on API-first development. The biggest takeaway was..." |
| Tutorial/tip | "3 things I wish I knew before my first FastAPI project..." |
| Industry insight | "Why every developer should learn prompt engineering in 2026..." |

### LinkedIn Post Template

```
Excited to share my latest project: SmartAttend

What it does:
- Trainers mark attendance in under 2 minutes
- Students check their attendance percentage anytime
- AI chatbot answers attendance queries in natural language

Tech stack: FastAPI + PostgreSQL + HTMX + LangChain

What I learned:
1. API-first development saves time (write spec before code)
2. HTMX is amazing for simple dynamic UIs without React
3. RAG is the easiest way to add AI to any product

Live demo: [link]
GitHub: [link]

#Python #FastAPI #WebDevelopment #AI #LangChain #OpenToWork
```

---

## 3. ATS-Friendly Resume

### What is ATS?

ATS (Applicant Tracking System) is software that companies use to filter resumes before a human sees them. If your resume is not ATS-friendly, it gets rejected automatically.

### ATS Rules

| Rule | Why |
|------|-----|
| Use a simple format (no tables, columns, graphics) | ATS cannot parse fancy layouts |
| Use standard section headings | ATS looks for "Experience", "Skills", "Education" |
| Include keywords from the job description | ATS matches keywords |
| Save as PDF (not Word) | PDF preserves formatting |
| No headers/footers | ATS often ignores these |
| No images or icons | ATS cannot read images |

### One-Page Resume Template (Fresher)

```
RAHUL SHARMA
Python Full-Stack Developer
Bhopal, India | rahul@example.com | +91-9876543210
GitHub: github.com/rahulsharma | LinkedIn: linkedin.com/in/rahulsharma

──────────────────────────────────────────────────

SKILLS
Python, FastAPI, Django, Django REST Framework, PostgreSQL, SQLAlchemy,
HTML, CSS, JavaScript, HTMX, Docker, Git, GitHub Actions, LangChain,
REST API Design, OpenAPI/Swagger, Linux, Redis

──────────────────────────────────────────────────

PROJECTS

SmartAttend — Student Attendance Management System        Jul 2026
FastAPI | PostgreSQL | HTMX | LangChain | GitHub Actions
- Built a full-stack web app for tracking student attendance at
  TechPath Institute, reducing manual work by 80%
- Developed 8 REST API endpoints with JWT authentication, pagination,
  and Swagger documentation
- Integrated an AI chatbot using LangChain RAG that answers natural
  language queries about attendance data
- Set up CI/CD pipeline with GitHub Actions (linting, testing, deployment)
- Deployed on Render with PostgreSQL, achieving 99.5% uptime
Live: smartattend.example.com | Code: github.com/rahulsharma/smartattend

Job Application Tracker                                   Jun 2026
Django | PostgreSQL | HTML/CSS/JS
- Built a web app for tracking job applications, interviews, and follow-ups
- Implemented user authentication, CRUD operations, and analytics dashboard
- Added AI-powered resume analysis feature using LangChain
Code: github.com/rahulsharma/job-tracker

Portfolio Website                                         May 2026
HTML | CSS | JavaScript
- Designed a responsive personal website with project showcase
- Implemented dark mode toggle and smooth scroll animations
- Deployed on GitHub Pages with custom domain
Live: rahulsharma.dev

──────────────────────────────────────────────────

EDUCATION

Python Full Stack Developer Course                     Jan-Jul 2026
TechPath Institute, Bhopal
- Python, Django, FastAPI, PostgreSQL, Docker, CI/CD, AI/ML
- Capstone: Full-stack AI product (SmartAttend)

Bachelor of Computer Applications (BCA)                2022-2025
[University Name], [City]

──────────────────────────────────────────────────

CERTIFICATIONS (Optional)
- Python for Everybody — Coursera (University of Michigan)
- Introduction to Git and GitHub — Google (Coursera)
```

### Resume Writing Tips

1. **Quantify everything** — "Reduced manual work by 80%" not "Improved efficiency"
2. **Start bullets with action verbs** — Built, Developed, Implemented, Deployed, Designed
3. **Include live demo links** — a working app is worth more than a description
4. **Match job description keywords** — if the JD says "FastAPI", your resume should say "FastAPI"
5. **One page only for freshers** — recruiters spend 6 seconds on a resume
6. **Projects before education** — your code matters more than your degree

---

## 4. Technical Interview Preparation

### Python DSA (Easy Level)

You need to solve easy-level DSA problems confidently. Focus on these topics:

| Topic | Key Concepts | Practice Count |
|-------|-------------|---------------|
| Arrays/Lists | Two pointers, sliding window, frequency count | 10 problems |
| Strings | Reverse, palindrome, anagram, character count | 8 problems |
| Dictionaries/Hashmaps | Frequency count, two sum, group anagrams | 8 problems |
| Sorting | Built-in sort, custom key, bubble sort | 5 problems |
| Searching | Linear search, binary search | 5 problems |
| Stacks/Queues | Bracket matching, min stack | 5 problems |
| Linked Lists | Reverse, detect cycle, merge | 5 problems |
| Recursion | Factorial, fibonacci, power | 5 problems |

### Common DSA Problems

```python
# 1. Two Sum — Find two numbers that add up to target
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Example: prices of items at a shop in Bhopal
prices = [120, 350, 80, 200, 150]
print(two_sum(prices, 500))  # [1, 3] — items at ₹350 + ₹200 = ₹500


# 2. Reverse a String
def reverse_string(s):
    return s[::-1]

print(reverse_string("TechPath"))  # "htaPceT"


# 3. Check Palindrome
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("madam"))     # True
print(is_palindrome("Rahul"))     # False


# 4. Find Most Frequent Element
def most_frequent(lst):
    freq = {}
    for item in lst:
        freq[item] = freq.get(item, 0) + 1
    return max(freq, key=freq.get)

cities = ["Bhopal", "Pune", "Delhi", "Bhopal", "Pune", "Bhopal"]
print(most_frequent(cities))  # "Bhopal"


# 5. FizzBuzz
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

print(fizzbuzz(15))
```

### System Design Basics

For fresher interviews, know these concepts at a high level:

| Concept | One-Line Explanation |
|---------|---------------------|
| Monolith vs Microservices | One big app vs many small apps talking to each other |
| REST API | Standard way to communicate between frontend and backend via HTTP |
| Database Indexing | Makes queries faster by creating a lookup table (like a book index) |
| Caching | Store frequently accessed data in memory (Redis) to avoid DB queries |
| Load Balancer | Distributes traffic across multiple servers |
| CDN | Stores static files (images, CSS) close to users for faster loading |
| Message Queue | Handles async tasks (send email later, process file in background) |
| Rate Limiting | Prevents abuse by limiting API calls per user/minute |

### Django/FastAPI Interview Questions

| Question | Key Points to Cover |
|----------|-------------------|
| What is FastAPI? | Async Python framework, auto-docs, Pydantic validation, high performance |
| FastAPI vs Django? | FastAPI: lightweight, async, API-focused. Django: batteries-included, ORM, admin panel |
| What is ORM? | Object-Relational Mapping — write Python classes instead of SQL queries |
| What is a migration? | Version control for database schema changes |
| What is JWT? | JSON Web Token — stateless authentication, no server-side session storage |
| What is CORS? | Cross-Origin Resource Sharing — browser security for cross-domain API calls |
| What is middleware? | Code that runs before/after every request (logging, auth, CORS) |
| Explain REST API design | Resources as nouns, HTTP verbs, status codes, pagination, versioning |

---

## 5. AI-Era Job Hunting

### Using AI Tools for Job Search

| Task | AI Tool | How to Use |
|------|---------|-----------|
| Cover letter | Claude / ChatGPT | "Write a cover letter for [role] at [company]. My skills: [list]. My project: [capstone]" |
| Resume tailoring | Claude / ChatGPT | "Tailor my resume for this job description: [paste JD]" |
| Interview prep | Claude / ChatGPT | "Ask me 10 Python interview questions for a fresher backend developer role" |
| Company research | Claude / ChatGPT | "Summarize what [company] does and their tech stack" |
| Mock interview | Claude / ChatGPT | "Conduct a mock technical interview for a Python developer position" |

### Cover Letter Template (AI-Assisted)

```
Dear Hiring Manager,

I am writing to apply for the [Role] position at [Company].
I recently completed a 6-month Python Full Stack Developer course
at TechPath Institute, where I built [Capstone Project Name] —
a full-stack web application using [tech stack].

What excites me about [Company] is [specific thing about the company].
I believe my experience with [relevant skill 1], [relevant skill 2],
and [relevant skill 3] makes me a strong fit for this role.

You can see my work at:
- Live demo: [link]
- GitHub: [link]
- LinkedIn: [link]

I would welcome the opportunity to discuss how I can contribute
to your team.

Best regards,
[Your Name]
[Phone] | [Email]
```

---

## 6. Freelancing

### Platforms for Indian Developers

| Platform | Best For | Commission |
|----------|---------|-----------|
| Fiverr | Small fixed-price gigs (₹500-₹50,000) | 20% |
| Upwork | Hourly or project-based work | 10-20% |
| Toptal | Senior developers (screening required) | 0% (client pays) |
| Freelancer.com | Competitive bidding | 10% |
| LinkedIn | Direct client connections | 0% |

### First Gig Strategy

1. **Start with small gigs** (₹2,000-₹5,000) to build reviews
2. **Over-deliver** on first 5 gigs — reviews are everything
3. **Specialize** — "Python FastAPI developer" beats "full-stack developer"
4. **Build a portfolio gig** — offer to build a small project at a discount

### Pricing Guide (Indian Market, 2026)

| Experience Level | Hourly Rate (₹) | Project Rate (₹) |
|-----------------|-----------------|------------------|
| Fresher (0-6 months) | ₹300-₹500/hr | ₹5,000-₹15,000 per project |
| Junior (6-18 months) | ₹500-₹1,000/hr | ₹15,000-₹50,000 per project |
| Mid-level (2-4 years) | ₹1,000-₹2,500/hr | ₹50,000-₹2,00,000 per project |
| Senior (4+ years) | ₹2,500-₹5,000/hr | ₹2,00,000+ per project |

### Proposal Writing Template

```
Hi [Client Name],

I read your project description carefully and I understand you need
[restate what they need in your own words].

I can help with this because:
1. I have built [similar project] using [relevant tech]
2. I am comfortable with [specific skill they mentioned]
3. I can deliver in [timeline] with [specific deliverables]

Here is my approach:
- Week 1: [What you will do]
- Week 2: [What you will do]
- Delivery: [Final deliverables]

You can see my previous work at: [GitHub/portfolio link]

Looking forward to discussing this further.

Best,
[Your Name]
```

---

## 7. Mock Interviews

### HR Round Preparation

Common HR questions and how to answer:

| Question | How to Answer |
|----------|--------------|
| "Tell me about yourself" | 2-minute pitch: background, course, capstone, what you are looking for |
| "Why this company?" | Research the company, mention specific products/values |
| "What is your greatest strength?" | Name a skill + give a specific example from your capstone |
| "What is your weakness?" | Name a real area for growth + what you are doing about it |
| "Where do you see yourself in 5 years?" | Senior developer / tech lead, mention continuous learning |
| "Why should we hire you?" | Your projects prove you can build real products, not just solve textbook problems |
| "What is your expected salary?" | Research market rate, give a range (e.g., ₹3-4.5 LPA for freshers in Bhopal) |

### The STAR Method for Behavioral Questions

```
S — Situation: Describe the context
T — Task: What was your responsibility?
A — Action: What did you do?
R — Result: What was the outcome?
```

**Example:**

> Q: "Tell me about a time you solved a difficult technical problem."
>
> S: During my capstone project, our AI chatbot was giving wrong attendance numbers.
> T: I needed to find and fix the bug before the demo presentation.
> A: I added logging to trace the data flow and discovered the query was not filtering by batch. I fixed the SQLAlchemy query and added a test case.
> R: The chatbot gave accurate results in the demo, and we now have a regression test to prevent this bug from returning.

### Technical Round Topics

| Category | What to Prepare |
|----------|----------------|
| Python basics | Data types, OOP, decorators, generators, error handling |
| DSA (easy level) | Arrays, strings, hashmaps, sorting, searching |
| Database | SQL queries (JOIN, GROUP BY, subqueries), normalization |
| API design | REST principles, status codes, authentication, pagination |
| Framework | FastAPI or Django specific questions (see list above) |
| System design (basic) | Monolith vs microservices, caching, load balancing |
| Git | Branching, merging, rebasing, resolving conflicts |
| Live coding | Be ready to share screen and code a small problem |

### Salary Expectations (India, 2026)

| City | Fresher Range (LPA) | With AI Skills (LPA) |
|------|--------------------|--------------------|
| Bhopal / Indore | ₹2.5-4.0 | ₹3.5-5.0 |
| Pune / Hyderabad | ₹3.0-5.0 | ₹4.0-6.5 |
| Bangalore / Delhi NCR | ₹3.5-6.0 | ₹5.0-8.0 |
| Mumbai | ₹3.5-5.5 | ₹5.0-7.5 |
| Remote (Indian company) | ₹3.0-5.0 | ₹4.0-7.0 |
| Remote (US/EU company) | ₹8.0-15.0 | ₹12.0-25.0 |

*LPA = Lakhs Per Annum. Ranges are approximate and depend on company size, role, and negotiation.*
