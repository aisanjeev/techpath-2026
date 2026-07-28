# Interview Preparation — Complete Guide

**Module 16 — Career Readiness | Get Hired**

---

## Why This Matters

> You have the skills. You have the projects. But if you freeze in an interview or give vague answers, none of that matters. This guide prepares you for the exact flow of IT fresher interviews in India.

---

## How IT Interviews Work (The Full Process)

```
Apply → Resume Shortlist → HR Screening Call → Technical Round →
→ Coding/Practical Test → Manager Round → Offer
```

| Round | Duration | What They Test |
|-------|----------|---------------|
| **HR Screening** | 15-20 min | Communication, salary expectation, cultural fit |
| **Technical** | 30-60 min | Core concepts, projects, problem-solving |
| **Practical/Coding** | 30-60 min | Write code on the spot (on paper, laptop, or HackerRank) |
| **Manager** | 20-30 min | Personality, growth potential, team fit |

---

## HR Round — Word-for-Word Preparation

### "Tell me about yourself" (Asked in 100% of interviews)

**Formula:** Present → Past → Future (60 seconds max)

```
"I'm Rahul Sharma, a full-stack developer with skills in 
Python, JavaScript, and AI tools. [PRESENT]

I recently completed my ADCA from TechPath Institute where I 
built 6 projects including a Student Management API with FastAPI 
and a data analysis dashboard using Python and Pandas. [PAST]

I'm looking for a role where I can apply my backend development 
and AI skills to build products that solve real problems." [FUTURE]
```

**Customize for each company:** Replace the last line with something specific about them.

> 🖼️ **IMAGE:** A visual "60-second pitch" template — three horizontal sections labeled "Present" (who you are now), "Past" (what you've done), "Future" (what you want) — each with example text and a timer showing 20 seconds per section
> `60-second-pitch-template.png`

### "Why should we hire you?"

```
"Three reasons:

First, I have hands-on project experience — not just theory. 
I've built and deployed real applications including [mention 
best project with specific details].

Second, I'm skilled in modern tools — Python, FastAPI, React, 
and AI tools like ChatGPT and Claude. I can build faster 
because I use AI-assisted development.

Third, I'm a fast learner. During my ADCA program, I went from 
zero coding knowledge to building full-stack applications in 
12 months. I pick up new technologies quickly."
```

### "What are your weaknesses?"

**Rule:** Pick a real weakness + show how you're fixing it.

```
Good: "I sometimes spend too much time trying to make code 
perfect before moving on. I've learned to set time limits for 
myself — get the working version first, optimize later."

Good: "Public speaking used to make me nervous. I've been 
practicing by presenting my projects to classmates, and I 
volunteered to present at our batch demo day."

Bad: "I'm a perfectionist" (too cliché)
Bad: "I have no weaknesses" (nobody believes this)
Bad: "I'm lazy sometimes" (too honest in the wrong way)
```

### Salary Negotiation

**Research first:** Check Glassdoor, AmbitionBox, LinkedIn for the role's salary range in your city.

| If they ask | You say |
|-------------|---------|
| "What's your expected salary?" | "Based on my research and the market rate for this role, I'm looking at ₹X to ₹Y. But I'm open to discussing based on the complete compensation package." |
| "That's above our budget" | "I understand. Could you share what the range is? I'm flexible and also value learning opportunities and growth." |
| "We can offer ₹X" | Take a moment (don't answer immediately). "Thank you. Can I have a day to consider?" |

---

## Technical Round — Core Questions & Answers

### Python (Most Asked)

**Q: What is the difference between a list and a tuple?**
```
"Lists are mutable — you can add, remove, or change elements after 
creation. Tuples are immutable — once created, you can't modify them. 
Tuples are faster and use less memory, so they're good for fixed 
data like coordinates or database records."
```

**Q: What are decorators?**
```
"A decorator is a function that takes another function and adds 
behavior to it without modifying the original function. For example, 
in FastAPI, @app.get('/') is a decorator that turns a regular 
function into an API endpoint. I used decorators in my Student 
Management API project for authentication checks."
```

**Q: Explain list comprehension with an example.**
```python
# Regular loop
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension (Pythonic way)
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### Web Development

**Q: What happens when you type a URL in the browser?**
```
"First, the browser checks its cache. If the URL isn't cached, 
it sends a DNS query to find the server's IP address. Then it 
establishes a TCP connection with that server (the three-way 
handshake). The browser sends an HTTP GET request. The server 
processes it and sends back HTML, CSS, and JS files. The browser 
renders the HTML, applies CSS styling, and executes JavaScript. 
The whole process takes about 1-3 seconds."
```

**Q: What is REST API?**
```
"REST is an architectural style for designing web APIs. It uses 
standard HTTP methods — GET for reading, POST for creating, PUT 
for updating, DELETE for removing. Each URL represents a resource. 
For example, GET /api/students returns all students, 
GET /api/students/1 returns student with ID 1. In my project, 
I built a REST API with 12 endpoints using FastAPI."
```

### Database/SQL

**Q: Write a query to find the second highest salary.**
```sql
SELECT MAX(salary) FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Q: What is normalization?**
```
"Normalization is organizing database tables to reduce data 
redundancy. For example, instead of storing a student's address 
in every order row, you keep addresses in a separate table and 
reference it by ID. This prevents inconsistencies — if the 
address changes, you update it in one place."
```

---

## Coding/Practical Round — What to Expect

### Format

| Company Type | Test Format |
|-------------|------------|
| Service (TCS, Infosys) | HackerRank/Cocubes online test |
| Product (Flipkart, Razorpay) | Whiteboard / live coding |
| Startup | Take-home assignment or pair programming |
| Freelance | "Build this in 3 days and show me" |

### During the Test

1. **Read the problem twice** — don't start coding immediately
2. **Think out loud** — "I'm thinking of using a dictionary to track frequency..."
3. **Start with brute force** — get a working solution first
4. **Test with examples** — walk through your code with sample input
5. **Handle edge cases** — empty input, single element, all same values
6. **Optimize if asked** — "I could improve this from O(n²) to O(n) using a hash set"

### Common Practical Tasks

| Task | Skills Tested |
|------|--------------|
| "Build a to-do app" | DOM manipulation, event handling, localStorage |
| "Create an API endpoint" | FastAPI/Django, database, validation |
| "Parse this CSV file" | File I/O, string processing, data structures |
| "Write a function to..." | Logic, algorithms, clean code |
| "Fix this bug" | Debugging, reading others' code |
| "Design a database schema" | Normalization, relationships, SQL |

---

## Mock Interview Script (Practice with a Friend)

### Round 1: HR (10 minutes)

Have a friend ask these in order:
1. "Tell me about yourself"
2. "Why do you want to work here?" (pick a real company)
3. "What are your strengths?"
4. "What's your biggest weakness?"
5. "Where do you see yourself in 3 years?"
6. "What's your salary expectation?"

### Round 2: Technical (15 minutes)

1. "What programming languages do you know? Rate yourself 1-10."
2. "Explain how a REST API works."
3. "What's the difference between SQL and NoSQL?"
4. "Tell me about your best project — architecture, challenges, outcome."
5. "Write a function to find duplicates in a list." (whiteboard)
6. "How would you design a database for a library system?"

### Round 3: Behavioral (5 minutes)

1. "Tell me about a time you faced a difficult problem and solved it."
2. "How do you handle tight deadlines?"
3. "How do you learn new technologies?"

---

## After the Interview

| Action | When |
|--------|------|
| Send thank-you email | Same day |
| Follow up (if no response) | After 5-7 days |
| Continue applying | Don't wait for one company |
| Reflect on what went well/poorly | Same evening |
| Practice weak areas | Before next interview |

### Thank You Email Template

```
Subject: Thank you — [Role] Interview

Hi [Interviewer Name],

Thank you for taking the time to interview me for the [Role] 
position today. I enjoyed learning about [specific thing from 
the interview].

I'm excited about the opportunity to contribute to [Company] 
with my skills in [relevant skills]. I believe my experience 
building [specific project] aligns well with what your team 
is working on.

Looking forward to hearing from you.

Best regards,
[Your Name]
[Phone] | [LinkedIn URL]
```

---

## The Math of Job Hunting

```
Average interviews to get first offer: 8-15
Average applications to get one interview: 10-15
Therefore: Apply to 100-200 positions over 1-2 months

5 applications/day × 20 working days = 100 applications/month
```

**It's a numbers game.** Rejection isn't personal — it's statistics. Keep applying, keep improving.
