# Cheat Sheet: Career Launch & Professional Portfolio

**Module 18 -- Quick Reference**

---

## GitHub Profile Checklist

| Item | Status |
|---|---|
| Professional headshot as profile photo | |
| Full name (not a username-style alias) | |
| Bio with role + top skills + focus area | |
| Location, website, email filled in | |
| Profile README repository created | |
| 5 pinned repositories selected | |
| Each pinned repo has a polished README | |
| Badges on READMEs (build, coverage, version) | |
| Screenshots or GIFs in project READMEs | |
| Live demo links for deployed projects | |
| Contribution graph has consistent activity | |
| GitHub Pages portfolio site set up | |

### The 5-Repo Strategy

| Slot | Type | Example |
|---|---|---|
| 1 | Full-stack application | Project management app (FastAPI + React) |
| 2 | AI/ML project | AI resume analyzer (LangChain + OpenAI) |
| 3 | Open source contribution | PR merged in a popular Python library |
| 4 | Scripting / automation | Daily report generator from Excel |
| 5 | Personal / creative | IPL score tracker with data viz |

### README Template

```markdown
# Project Name
![Badge](https://img.shields.io/badge/status-active-green)

> One-line description

## Screenshots | Live Demo | Tech Stack
## Features | Installation | API Docs
## Contributing | License
```

---

## LinkedIn Optimization Checklist

| Item | Status |
|---|---|
| Professional headline with keywords | |
| About section (4 paragraphs: intro, skills, projects, CTA) | |
| 15+ skills listed in order of strength | |
| 3-4 projects added with links and descriptions | |
| Education section completed | |
| Profile photo (professional headshot) | |
| Custom LinkedIn URL set | |
| 10+ skill endorsements | |
| Posting 2-4 times per week | |
| 200+ relevant connections | |

### Headline Formula

```
[Role] | [Top 3 Skills] | [What You Do or Want]
```

Example: "Python Full Stack Developer | FastAPI, React, LangChain | Building AI-Powered Web Apps"

### Post Schedule

| Time Slot | IST |
|---|---|
| Morning sweet spot | 8:00 AM - 9:00 AM |
| Evening sweet spot | 6:00 PM - 7:00 PM |
| Minimum frequency | 2 posts per week |
| Ideal frequency | 4-5 posts per week |

---

## ATS Resume Format

### Section Order (for freshers)

1. Header (name, phone, email, LinkedIn, GitHub, location)
2. Professional Summary (3-4 lines)
3. Technical Skills (grouped by category)
4. Projects (2-3, with links, dates, and bullet points)
5. Education
6. Certifications (optional)

### Formatting Rules

| Rule | Specification |
|---|---|
| Length | 1 page only |
| Font | Arial or Calibri, 10-11pt |
| Margins | 0.5 to 0.75 inches |
| Format | PDF (unless told otherwise) |
| Layout | Single column only |
| No | Tables, images, icons, colors, headers/footers |

### Action Verbs for Bullet Points

```
Built | Designed | Deployed | Implemented | Developed
Optimized | Automated | Integrated | Reduced | Achieved
```

Bad: "Worked on a web application."
Good: "Built a full-stack web app with 25 REST endpoints serving 100+ users."

---

## Top 10 Interview Questions -- Quick Answers

| Question | Key Points |
|---|---|
| Tell me about yourself | Present-Past-Future format, under 90 seconds |
| Why this company? | Mention specific product/service + how your skills match |
| Strengths? | 2-3 with concrete examples |
| Weaknesses? | Real weakness + what you are doing to improve |
| Where in 5 years? | Senior developer, system design, mentoring |
| Salary expectations? | State a range based on research, show flexibility |
| Why should we hire you? | Skills match + projects prove ability + eagerness to learn |
| Difficult problem? | Use STAR method (Situation, Task, Action, Result) |
| Why Python? | Versatile, readable, strong ecosystem, industry demand |
| Any questions for us? | Ask about team, tech stack, growth opportunities |

### STAR Method

```
S - Situation: Set the scene (where, when, what was happening)
T - Task: Your responsibility or challenge
A - Action: What you specifically did
R - Result: Outcome with numbers if possible
```

---

## Top 10 DSA Patterns -- Quick Reference

| Pattern | When to Use | Example Problem |
|---|---|---|
| HashMap/Dictionary | Fast lookups, counting | Two Sum, Character Frequency |
| Two Pointers | Sorted arrays, pairs | Remove Duplicates, Palindrome |
| Sliding Window | Subarray/substring problems | Max Sum Subarray |
| Stack | Matching, nesting | Valid Parentheses |
| Binary Search | Sorted data, find target | Search in Sorted Array |
| Recursion | Tree/divide problems | Fibonacci, Tree Traversal |
| Sorting | Order-dependent problems | Merge Sort, Quick Sort |
| BFS/DFS | Graph/tree traversal | Level Order, Connected Components |
| Greedy | Local optimal = global | Activity Selection |
| Dynamic Programming | Overlapping subproblems | Longest Common Subsequence |

### Two Sum (most asked)

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
```

### Valid Parentheses

```python
def is_valid(s):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for c in s:
        if c in "({[":
            stack.append(c)
        elif not stack or stack.pop() != pairs[c]:
            return False
    return not stack
```

---

## Freelancing Pricing Guide

### Hourly Rates (INR)

| Level | Rate |
|---|---|
| Starting (0-3 months) | 500 - 800/hr |
| Building reputation (3-12 months) | 800 - 1,500/hr |
| Established (1-2 years) | 1,500 - 3,000/hr |
| Expert (2+ years) | 3,000 - 5,000/hr |

### Project Rates (INR)

| Project Type | Fresher | Experienced |
|---|---|---|
| Landing page | 5,000 - 10,000 | 15,000 - 30,000 |
| Web scraping script | 3,000 - 8,000 | 10,000 - 25,000 |
| REST API (10-15 endpoints) | 15,000 - 30,000 | 40,000 - 80,000 |
| Full-stack web app | 30,000 - 60,000 | 80,000 - 2,00,000 |
| AI chatbot | 20,000 - 40,000 | 50,000 - 1,50,000 |

### Platform Comparison

| Platform | Commission | Best For |
|---|---|---|
| Fiverr | 20% | Small, defined gigs |
| Upwork | 20% then 10% then 5% | Longer projects |
| Toptal | 0% (client pays) | Expert-level work |
| Freelancer.com | 10% | Indian market |

---

## Mock Interview Prep Checklist

### Before

- [ ] Laptop charged, camera and mic working
- [ ] Stable internet connection
- [ ] Clean, professional background
- [ ] Resume open on screen or printed
- [ ] Company research notes ready
- [ ] Water bottle nearby
- [ ] IDE open for coding round

### During

- [ ] Greet with a smile and maintain eye contact (look at camera)
- [ ] Keep answers under 2 minutes
- [ ] Use specific examples, not generalizations
- [ ] Think out loud during coding problems
- [ ] Ask for clarification if question is unclear

### After

- [ ] Send thank-you email within 24 hours
- [ ] Note all questions asked
- [ ] Prepare better answers for weak points
- [ ] Follow up after 1 week if no response

### Salary Ranges for Freshers (2026, India)

| Company Type | Range |
|---|---|
| Product startup (Bangalore/Pune) | 4 - 8 LPA |
| Service company (TCS, Infosys) | 3 - 4.5 LPA |
| Mid-size company (Delhi/Mumbai) | 4 - 6 LPA |
| Remote / International | 5 - 10 LPA |

---

*TechPath Institute -- Building Careers in Technology*
