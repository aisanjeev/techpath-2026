# Demo and Presentation: Showcasing Your Capstone

**Module 17 — Full-Stack AI Product: Capstone Development | Topic 7**

---

## Why the Demo Matters

You have spent four weeks building your capstone project. The demo is your chance to show the world what you built and why it matters. A great demo can turn a good project into a memorable one. A bad demo can make even an excellent project look mediocre.

Think of the demo like a movie trailer. A trailer does not show every scene in the movie — it shows the most exciting parts in a logical sequence that makes you want to see more. Your demo should do the same: show the highlights, tell a story, and leave the audience impressed.

---

## Structuring a 15-Minute Demo

A 15-minute demo has three acts, just like a movie. Here is the breakdown:

| Section | Duration | What to Cover |
|---------|----------|--------------|
| **Act 1: The Problem** | 2-3 minutes | What problem you are solving and for whom |
| **Act 2: The Solution** | 8-10 minutes | Live demo + code walkthrough |
| **Act 3: The Wrap-Up** | 2-3 minutes | Tech stack summary, learnings, Q&A |

### Minute-by-Minute Breakdown

| Minute | Activity | Example (Student Exam Portal) |
|--------|----------|-------------------------------|
| 0-1 | Introduce yourself and the project name | "Hi, I am Priya from Bhopal. I built the Student Exam Portal." |
| 1-3 | Explain the problem with a real scenario | "Every semester, students at RGPV spend hours searching WhatsApp groups for past papers..." |
| 3-5 | Live demo: Show the happy path (main feature) | Search for "Data Structures 2024", download a paper |
| 5-7 | Live demo: Show the AI feature | Ask the chatbot "What topics were covered in the 2024 DS paper?" |
| 7-9 | Live demo: Show admin/upload feature | Upload a new paper, show it appears in search |
| 9-11 | Code walkthrough: Show architecture | Show the project structure, explain key files |
| 11-12 | Code walkthrough: Show one interesting code snippet | Show the RAG pipeline or a complex query |
| 12-13 | Show CI/CD: Push a commit, show tests running | GitHub Actions running tests |
| 13-14 | Tech stack summary + what you learned | "I learned FastAPI, PostgreSQL, and RAG architecture" |
| 14-15 | Thank the audience + Q&A | "Thank you. I am happy to answer questions." |

---

## Opening with the Problem Statement

Never start your demo with "So I built this app using FastAPI and React..." Nobody cares about the tech stack until they understand the problem.

### Bad Opening

"Hello, my name is Rahul. I used FastAPI for the backend, PostgreSQL for the database, and React for the frontend. Let me show you the login page."

### Good Opening

"Hello, my name is Rahul. I am from Bhopal. Every year, over 50 lakh students in India appear for university exams, and most of them waste hours searching for past exam papers. They dig through WhatsApp groups, ask seniors, and sometimes pay for photocopies of papers that should be freely available. I built the Student Exam Portal to solve this problem. Let me show you how it works."

### The Problem Statement Formula

```
[Audience] face [specific problem].
Currently, they solve it by [current painful solution].
My project [project name] solves this by [your solution in one sentence].
```

### More Examples

**Freelancer Invoice Manager (Sneha, Pune)**:
"Freelancers in India send over 10 crore invoices every year, and most of them track payments using Excel sheets or WhatsApp messages. My Invoice Manager lets freelancers create, send, and track invoices in one place — with AI-powered expense categorization."

**Course Recommendation System (Arjun, Bangalore)**:
"TechPath Institute offers 50+ courses, and new students often feel overwhelmed choosing where to start. I built a course recommendation system with an AI chatbot that asks about your goals and suggests a personalized learning path."

---

## Live Demo Flow: Happy Path First

The golden rule of demos: show the happy path first. The happy path is the main use case working perfectly, with no errors or edge cases.

### Demo Flow Checklist

| Step | What to Show | Why |
|------|-------------|-----|
| 1. Landing page | The app is deployed and accessible | Proves it works in production |
| 2. User registration/login | Create an account or log in | Shows auth works |
| 3. Core feature | The main thing your app does | This is the star of the show |
| 4. AI feature | The AI-powered functionality | The wow factor |
| 5. Admin feature (if applicable) | Manage content, approve items | Shows full-stack capability |
| 6. Mobile view (bonus) | Show it works on a phone | Shows responsive design |

### Pre-Demo Setup

Before your demo, prepare everything:

```
Pre-Demo Checklist:
[ ] App is deployed and accessible (not just localhost)
[ ] Test data is loaded (do not demo with an empty database)
[ ] You have tested the exact flow you will show
[ ] Browser is open with the right tabs
[ ] No embarrassing browser history or bookmarks visible
[ ] Terminal is open with the right directory
[ ] API docs page (/docs) is open in a tab
[ ] Phone/notifications are on silent
[ ] Internet connection is stable (have a mobile hotspot backup)
```

---

## Code Walkthrough Tips

The code walkthrough is where you show that you understand what you built, not just that it works.

### What to Show

| Show | Do Not Show |
|------|------------|
| Project folder structure (30 seconds) | Every single file |
| One model with its relationships | All 10 models |
| The most complex/interesting endpoint | Basic CRUD endpoints |
| Your AI integration code | The OpenAI SDK internals |
| Your test file (show tests passing) | Every test case |
| Your CI/CD pipeline YAML | GitHub Actions documentation |

### How to Explain Code

Use the "What, Why, How" framework:

1. **What**: "This is the RAG service that powers our chatbot."
2. **Why**: "We use RAG instead of plain GPT because we need answers based on our actual course data, not general knowledge."
3. **How**: "It loads documents, splits them into chunks, stores them in ChromaDB, and retrieves relevant chunks when the user asks a question."

### Example Code Walkthrough Script

```
"Let me show you the most interesting part of the codebase — the RAG pipeline.

[Open app/services/rag_service.py]

This file has three main functions:
1. load_and_split_documents — takes a PDF and breaks it into 500-character
   chunks. We overlap by 50 characters so we do not lose context at boundaries.

2. create_vector_store — converts each chunk into a numerical vector using
   OpenAI embeddings and stores them in ChromaDB.

3. create_rag_chain — this is where the magic happens. When a user asks a
   question, we search ChromaDB for the 3 most similar chunks, put them
   into a prompt as context, and send it to GPT.

The key design decision here was using 'stuff' chain type instead of
'map_reduce' — since our chunks are small, we can fit 3 of them in a
single prompt. This is simpler and gives better answers.

Let me show you it working in the Swagger docs..."
```

---

## Handling Q&A

Q&A can be the most nerve-wracking part, but with preparation, it becomes the most impressive part.

### Common Questions and How to Answer Them

| Question | Good Answer | Bad Answer |
|----------|------------|------------|
| "Why did you choose FastAPI over Django?" | "I needed async support for AI API calls, and FastAPI's auto-generated Swagger docs saved me time on documentation." | "Because the instructor said so." |
| "How do you handle errors in the AI feature?" | "I wrap AI calls in try/except blocks and return a fallback message. I also cache responses in Redis to reduce API failures." | "It does not crash." |
| "What would you add if you had more time?" | "I would add user analytics to track which papers are most popular, and implement semantic search using vector similarity." | "Everything is done." |
| "How does your authentication work?" | "Users register with email and password. Passwords are hashed with bcrypt. On login, a JWT token is issued with a 60-minute expiry." | "It uses JWT." |
| "What was the hardest part?" | "Getting the RAG pipeline to return relevant answers. I had to experiment with chunk sizes — 500 characters with 50-character overlap gave the best results." | "Everything was hard." |

### If You Do Not Know the Answer

It is perfectly fine to say:

- "That is a great question. I have not explored that yet, but I would approach it by..."
- "I am not sure about the specifics, but I can look into it and follow up."
- "I did not implement that in this version, but my plan would be to..."

Never make up an answer. Interviewers respect honesty far more than bluffing.

---

## Common Demo Disasters and How to Avoid Them

| Disaster | Prevention | Recovery Plan |
|----------|-----------|---------------|
| App crashes during demo | Test the exact flow 3 times before | Have screenshots ready as backup |
| Internet goes down | Have a mobile hotspot ready | Switch to localhost demo |
| Database is empty | Load test data before the demo | Have a script that seeds test data |
| AI feature returns bad answer | Pre-test with the exact questions you will ask | Have a pre-recorded video of it working |
| Login does not work | Create a demo account beforehand, test it | Have credentials written down |
| "It works on my machine" | Deploy and test on production URL | Always demo from the deployed version |
| You forget what to say | Have a written script/outline | Keep notes on your phone (not on screen) |

---

## Recording a Demo Video

Even if your demo is live, recording a backup video is essential.

### Recording Tools

| Tool | Platform | Cost | Best For |
|------|----------|------|----------|
| OBS Studio | Windows/Mac/Linux | Free | Full-featured screen recording |
| Loom | Browser extension | Free (25 min limit) | Quick recordings with webcam |
| Windows Game Bar | Windows | Free (built-in) | Simple screen recording |

### Demo Video Structure

```
0:00 - 0:30  Title card (project name, your name, TechPath Institute)
0:30 - 1:30  Problem statement (voice over a slide)
1:30 - 4:00  Live demo of the app (screen recording with narration)
4:00 - 5:00  Quick code walkthrough (show 2-3 key files)
5:00 - 5:30  Tech stack summary (slide or README)
5:30 - 6:00  Thank you + contact information
```

### Tips for a Good Recording

| Tip | Why |
|-----|-----|
| Use a clean desktop with no personal files visible | Looks professional |
| Speak slowly and clearly | Viewers can always speed up, but they cannot slow down |
| Zoom in on important parts of the screen | Small text is hard to read in recordings |
| Record audio separately if your mic is noisy | Better audio makes a huge difference |
| Keep it under 6 minutes for portfolio | Recruiters will not watch longer videos |

---

## Demo Script Template

Use this template to plan your demo. Fill it in with your project details.

```
DEMO SCRIPT

Project: ___________________________________
Duration: 15 minutes
Date: ______________________________________

OPENING (2 minutes):
"Hello, I am [name] from [city]. I built [project name] to solve [problem]."
[Explain the problem with a specific example]
[Show one statistic or fact about the problem]

LIVE DEMO (8 minutes):
Step 1: Show [landing page / deployed URL]
Step 2: [Register / Login]
Step 3: [Core feature demonstration]
Step 4: [AI feature demonstration]
Step 5: [Admin / secondary feature]

CODE WALKTHROUGH (3 minutes):
Show 1: [Project structure — 30 seconds]
Show 2: [Most interesting file — 1 minute]
Show 3: [Tests passing — 30 seconds]
Show 4: [CI/CD pipeline — 1 minute]

CLOSING (2 minutes):
Tech stack: [List 5-6 key technologies]
Key learning: [What you learned building this]
Future plans: [What you would add next]
"Thank you. Happy to answer any questions."

BACKUP PLAN:
If app crashes: [Show screenshots / pre-recorded video]
If internet fails: [Switch to localhost]
If AI feature fails: [Explain how it works with architecture diagram]
```

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
