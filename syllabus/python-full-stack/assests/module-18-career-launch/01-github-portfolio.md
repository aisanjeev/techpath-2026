# GitHub Portfolio: Your Developer Resume

**Module 18 -- Career Launch & Professional Portfolio | Topic 1**

---

## Why GitHub Is Your Developer Resume

Think of GitHub as your professional showroom. Just like a carpenter shows their best furniture to get hired, a developer shows their best code on GitHub. In the Indian tech industry, hiring managers at companies like TCS, Infosys, Wipro, and startups in Bangalore and Pune now check your GitHub profile before even reading your resume.

Here is what a GitHub profile tells a recruiter:

| What They See | What They Judge |
|---|---|
| Contribution graph (green squares) | Consistency and work ethic |
| Pinned repositories | Quality and range of skills |
| README files | Communication and documentation skills |
| Stars and forks | Community validation |
| Commit messages | Professionalism and attention to detail |

A strong GitHub profile can be the difference between getting an interview call and getting ignored. Let us build one step by step.

---

## Setting Up a Professional GitHub Profile

### Step 1: Profile Basics

Your profile is the first thing people see. Make it count.

- **Profile Photo**: Use a clear, professional headshot. No sunglasses, no group photos, no cartoon avatars.
- **Name**: Use your full legal name (e.g., "Priya Sharma" not "priya_coder_2003").
- **Bio**: One line about what you do. Example: "Full Stack Python Developer | FastAPI + React | Open Source Contributor"
- **Location**: Add your city (e.g., "Bhopal, India").
- **Website**: Link to your portfolio site or LinkedIn.
- **Email**: Use a professional email.

### Step 2: Create a Profile README

GitHub allows a special repository (with the same name as your username) that displays as a profile README. This is your landing page.

Create a repository named exactly like your username (e.g., `priyasharma/priyasharma`) and add a `README.md`:

```markdown
# Hi, I am Priya Sharma

## About Me
- Full Stack Python Developer from Bhopal, India
- Graduate of TechPath Institute (Python Full Stack Program)
- Passionate about building web applications and AI-powered tools

## Tech Stack
**Backend:** Python, FastAPI, Django, PostgreSQL, SQLAlchemy
**Frontend:** React, TypeScript, Tailwind CSS, Astro
**AI/ML:** LangChain, LangGraph, OpenAI API
**DevOps:** Docker, GitHub Actions, AWS/Azure

## Featured Projects
- [TaskFlow](https://github.com/priyasharma/taskflow) - Project management app with AI task prioritization
- [ChatBot Builder](https://github.com/priyasharma/chatbot-builder) - No-code chatbot platform using LangGraph

## Connect With Me
- LinkedIn: linkedin.com/in/priyasharma
- Portfolio: priyasharma.dev
- Email: priya@email.com
```

---

## Writing READMEs That Impress

A README is the front door of your project. Recruiters spend about 30 seconds on each repo. Your README must grab attention fast.

### The Perfect README Structure

```markdown
# Project Name

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> One-line description of what the project does.

## Screenshots
![Dashboard](screenshots/dashboard.png)

## Live Demo
[Click here to try it](https://your-app.vercel.app)

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** React, Tailwind CSS
- **Deployment:** Docker, GitHub Actions

## Features
- User authentication with JWT
- Real-time notifications
- REST API with 20+ endpoints
- 90%+ test coverage

## Installation
1. Clone the repo: `git clone https://github.com/you/project.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn app.main:app --reload`

## API Documentation
Visit `/docs` for interactive Swagger documentation.

## Contributing
Pull requests are welcome. Please open an issue first.

## License
MIT
```

### Badges That Matter

Badges are small status indicators at the top of your README. They show professionalism.

| Badge Type | What It Shows | Example |
|---|---|---|
| Build status | Your CI/CD works | `build-passing` |
| Code coverage | You write tests | `coverage-85%` |
| Python version | Tech stack clarity | `python-3.11` |
| License | Open source readiness | `MIT` |
| Last commit | Project is active | `last commit: 2 days ago` |

---

## The 5-Repo Strategy

Pinning the right 5 repositories on your profile is like putting your best work in a shop window. Here is the strategy that works for Indian fresher developers:

### Repo 1: Full-Stack Application

This is your flagship project. A complete web application with frontend, backend, database, and deployment.

**Example:** "TaskFlow - A project management tool built with FastAPI + React"

- Must have: User auth, CRUD operations, responsive UI, deployed and live
- Bonus: Real-time features, payment integration, email notifications

### Repo 2: AI/ML Project

AI skills are in massive demand. Show you can build with modern AI tools.

**Example:** "SmartResume - AI-powered resume analyzer using LangChain and OpenAI"

- Must have: API integration, practical use case, clean code
- Bonus: Streaming responses, conversation memory, RAG implementation

### Repo 3: Open Source Contribution

Contributing to open source shows you can work with other developers' code.

**Example:** Fork a popular Python library, fix a bug or add a feature, and get your PR merged.

- Must have: At least 1 merged pull request
- Bonus: Multiple contributions, issue discussions, code reviews

### Repo 4: Scripting / Automation Tool

Show you can solve real problems with code.

**Example:** "AutoReport - Python script that generates daily sales reports from Excel files"

- Must have: Practical use case, well-documented, command-line interface
- Bonus: Scheduled execution, email delivery, error handling

### Repo 5: Personal / Creative Project

Show your personality and passion for coding.

**Example:** "CricketStats - Live IPL score tracker with historical data analysis"

- Must have: Something unique, shows creativity
- Bonus: Data visualization, API usage, mobile responsive

---

## GitHub Contribution Graph

The green squares on your profile tell a story. Here is how to keep them green:

| Activity | Counts as Contribution |
|---|---|
| Committing to a repo | Yes |
| Opening a pull request | Yes |
| Opening an issue | Yes |
| Reviewing a pull request | Yes |
| Forking a repo | No |
| Starring a repo | No |

**Tips for a consistent contribution graph:**

1. Commit small changes daily rather than large changes weekly.
2. Work on side projects during weekends.
3. Contribute to open source issues labeled "good first issue."
4. Write documentation -- it counts as a contribution too.
5. Do not fake contributions with empty commits. Recruiters can tell.

---

## GitHub Pages Portfolio Site

GitHub Pages lets you host a free website directly from a repository. This is perfect for a personal portfolio.

### Quick Setup

1. Create a repository named `yourusername.github.io`.
2. Add an `index.html` file with your portfolio.
3. Go to Settings > Pages > Enable GitHub Pages.
4. Your site is live at `https://yourusername.github.io`.

### What to Include on Your Portfolio Site

- **Hero section**: Your name, title, and a one-line pitch.
- **About**: Brief background, education (TechPath Institute), skills.
- **Projects**: Cards linking to your GitHub repos with screenshots.
- **Experience**: Internships, freelance work, certifications.
- **Contact**: Email, LinkedIn, GitHub links.
- **Resume**: A downloadable PDF link.

---

## Real-World Example: Priya's Portfolio That Got Her Hired

Priya was a fresher from Bhopal who completed the Python Full Stack program at TechPath Institute. She had no work experience. Here is what she did:

**Month 1: Set up her GitHub profile**
- Professional photo and bio
- Created a profile README with her tech stack

**Month 2: Built her 5 pinned repos**
- Full-stack expense tracker (FastAPI + React)
- AI-powered study planner (LangChain)
- Contributed to a FastAPI plugin (open source)
- Automated attendance system (Python + OpenCV)
- Recipe sharing app (Django + HTMX)

**Month 3: Polish and deploy**
- Added badges, screenshots, and live demo links to all READMEs
- Deployed all projects (Vercel, Railway, GitHub Pages)
- Built a portfolio site on GitHub Pages
- Maintained daily contributions for 90 days straight

**Result:** A startup in Pune found her GitHub profile through a job portal. The CTO said, "Her GitHub profile told us more than any resume could." She got a Python developer role at 5,00,000 per year -- above average for a fresher.

The key lesson: Your GitHub profile is not just a code storage. It is a living portfolio that works for you 24 hours a day, 7 days a week. Start building it today.

---

*TechPath Institute -- Building Careers in Technology*
