#!/usr/bin/env python3
"""
Seed batch 2 courses into the TechPath database directly via ORM.

Courses:
  1. DevOps for Beginners
  2. Python Programming
  3. Gen AI Master

Run from the techpath-backend/ directory:
  python scripts/seed_courses_batch2.py   (or with venv: venv/Scripts/python.exe ...)

Idempotent — skips any course/category/skill that already exists.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.crud.course import course_category_crud, course_crud, skill_crud
from app.schemas.course import (
    CourseCategoryCreate,
    CourseCreate,
    CurriculumModule,
    FAQItem,
    ProjectItem,
)


async def get_or_create_category(db, name: str, slug: str, display_order: int = 0):
    cat = await course_category_crud.get_by_slug(db, slug=slug)
    if cat:
        print(f"  [skip] category already exists: {name}")
        return cat
    cat = await course_category_crud.create(
        db,
        obj_in=CourseCategoryCreate(name=name, slug=slug, display_order=display_order, is_active=True),
    )
    print(f"  [+] created category: {name}")
    return cat


# ---------------------------------------------------------------------------
# New skills for batch 2  (existing slugs from batch 1 are safe duplicates)
# ---------------------------------------------------------------------------
ALL_SKILLS = [
    # DevOps
    ("Linux", "linux"),
    ("Docker", "docker"),
    ("Jenkins", "jenkins"),
    ("CI/CD", "cicd"),
    ("AWS", "aws"),
    ("Kubernetes", "kubernetes"),
    ("Shell Scripting", "shell-scripting"),
    ("DevOps", "devops"),
    ("Cloud Computing", "cloud-computing"),
    ("Nginx", "nginx"),
    ("GitHub Actions", "github-actions"),
    # Python Programming
    ("Python 3", "python-3"),
    ("OOP", "oop"),
    ("File Handling", "file-handling"),
    ("Automation", "automation"),
    ("Web Scraping", "web-scraping"),
    ("CLI Apps", "cli-apps"),
    ("Beginner Programming", "beginner-programming"),
    # Gen AI Master
    ("Claude", "claude"),
    ("Gemini", "gemini"),
    ("Vibe Coding", "vibe-coding"),
    ("Cursor", "cursor"),
    ("Bolt", "bolt"),
    ("Lovable", "lovable"),
    ("Prompt Engineering", "prompt-engineering"),
    ("Midjourney", "midjourney"),
    ("AI Automation", "ai-automation"),
    ("Freelancing", "freelancing"),
    # Shared with batch 1 (safe — get_or_create skips duplicates)
    ("Gen AI", "gen-ai"),
    ("ChatGPT", "chatgpt"),
    ("Canva AI", "canva-ai"),
    ("Git", "git"),
    ("GitHub", "github"),
    ("Python", "python"),
]


# ---------------------------------------------------------------------------
# Descriptions
# ---------------------------------------------------------------------------

DEVOPS_DESCRIPTION = """\
**DevOps for Beginners** — a practical, hands-on course that takes you from "what is a server?" \
to building automated deployment pipelines, containerising applications, and managing cloud \
infrastructure. All in 4 months, with zero prior DevOps experience required.

---

### What is DevOps and why does it matter?

Every app, website, and software product you use — from Instagram to Zomato — needs someone to \
build it, test it, deploy it, and keep it running. That someone is a DevOps engineer.

DevOps bridges the gap between development (writing code) and operations (running servers). \
Companies pay premium salaries for DevOps skills because one good DevOps engineer saves an entire \
team hours of manual work every single day.

The demand is massive. The supply — especially from tier-2 and tier-3 cities — is almost zero. \
That is your opportunity.

---

### What you will learn

**Linux & Command Line**
Every server in the world runs Linux. You will learn to navigate, manage files, install software, \
and write shell scripts from the terminal — the foundation of all DevOps work.

**Git & Version Control**
Track code changes, collaborate with teams, manage branches, resolve merge conflicts, and work \
with GitHub like a professional developer.

**Docker & Containers**
Package any application into a portable container that runs the same way everywhere — your laptop, \
a test server, or the cloud. This is the most important DevOps skill of 2026.

**CI/CD Pipelines**
Automate the entire process from code commit to production deployment. Every time a developer pushes \
code, your pipeline tests it, builds it, and deploys it — automatically, without human intervention.

**Cloud Computing (AWS Basics)**
Understand how the cloud works. Launch EC2 instances, store files in S3, manage permissions with IAM, \
and deploy applications on AWS — the world's largest cloud platform.

**Kubernetes Introduction**
Learn the basics of container orchestration — how companies manage hundreds of containers running \
across multiple servers. Enough to understand the ecosystem and continue learning.

**Infrastructure as Code**
Write code that creates servers, networks, and databases automatically. No more clicking through \
dashboards — your infrastructure lives in version-controlled files.

---

### What you will build (real labs, not slides)

- A fully configured Linux server with users, permissions, and services
- Shell scripts that automate system administration tasks
- Dockerised web applications (Python Flask and Node.js)
- A complete CI/CD pipeline that tests and deploys code on every push
- A multi-container application using Docker Compose
- A cloud-hosted application on AWS EC2
- A final capstone: end-to-end DevOps pipeline from code to production

---

### Career outcomes

- Junior DevOps Engineer (starting at ₹25,000–₹50,000/month)
- Cloud Support Associate
- Linux System Administrator (₹20,000–₹40,000/month)
- Build and Release Engineer
- Site Reliability Engineer (SRE) — with further experience
- Freelance DevOps Consultant (₹15,000–₹50,000 per project)

DevOps roles are among the highest-paid in IT. Even at the junior level, salaries are significantly \
higher than general software development roles because the supply of skilled DevOps professionals is \
very low.

---

### Who should join?

- BCA, BSc IT, B.Tech students or graduates who want a high-paying specialisation
- Working developers who want to add DevOps to their skillset
- System administrators who want to modernise their skills
- Students from Mughalsarai, Chandauli, Varanasi, Ghazipur, and nearby areas
- Anyone who has basic computer knowledge and is comfortable learning from the command line

**Important:** This course assumes you have basic computer familiarity. You do not need to know \
programming, but you should be comfortable typing commands and learning new tools. If you have \
completed our Python or Full Stack course, this is an excellent next step.
"""

PYTHON_DESCRIPTION = """\
**Python Programming** — the most beginner-friendly programming language in the world, taught the \
TechPath way: hands-on, project-first, and in a language you understand. Available both **offline \
at our Mughalsarai centre** and **live online** — same instructor, same curriculum, same support.

In 3 months, you go from zero coding knowledge to writing real Python programs, automating boring \
tasks, and building projects you can show in any interview.

---

### Why Python?

Python is the #1 programming language on every global ranking — TIOBE, GitHub, Stack Overflow \
Developer Survey. It powers everything from Instagram's backend to NASA's data analysis to \
ChatGPT's training pipeline.

But here is the real reason to learn Python: **it reads like English.**

Compare printing "Hello World" in Java vs Python:

**Java:** `public class Main { public static void main(String[] args) { System.out.println("Hello, World!"); } }`

**Python:** `print("Hello, World!")`

One line. No boilerplate. No semicolons. That is why Python is the best first language for any \
beginner in Mughalsarai, Chandauli, Varanasi, or anywhere in eastern UP.

---

### What you will build (real projects, not just exercises)

By the end of 3 months, your GitHub will have these projects:

- **CLI Calculator** — a command-line calculator with error handling
- **Student Grade Manager** — input marks, calculate percentage, assign grades, save to CSV
- **File Organiser** — auto-sorts files in a folder by type (images, documents, videos)
- **To-Do App (CLI)** — add, delete, mark complete, and save tasks to JSON
- **Web Scraper** — extract data from a website and save as CSV
- **Mini Project of Your Choice** — a personal project for your portfolio

---

### Offline + Online — your choice

**Offline (Mughalsarai centre):**
Circus Road, Mughalsarai — walking distance from DDU Junction. Small batches of 25 students. \
Morning, afternoon, and evening batches. Lab access during class hours.

**Live Online:**
Same instructor, same curriculum, same batch timings. Join from anywhere — Chandauli, Varanasi, \
Ghazipur, Ballia, Bihar, or any city in India. Live interactive classes with screen sharing and \
real-time doubt clearing over Google Meet / Zoom.

Both modes include: WhatsApp doubt support, weekend doubt sessions, project reviews, and placement assistance.

---

### Career outcomes after Python

- Python Developer (₹15,000–₹35,000/month starting)
- Automation Engineer
- Backend Developer (Django / Flask — our Full Stack course is the next step)
- Data Analyst (with Pandas, NumPy)
- QA / Test Automation Engineer
- Freelancer (automation scripts, scrapers, bots — ₹2,000–₹15,000 per project)

Python is the gateway language. Once you know Python, every other course at TechPath — Full Stack, \
Data Science, DevOps, IoT — becomes easier because you already know the language.

---

### Who is this for?

- Class 10 / 12 pass students (any stream) taking their first step into programming
- BCA, BSc, B.Tech students who want practical skills beyond their college syllabus
- Graduates from Arts, Commerce, or Science who want to enter the tech industry
- Working professionals looking to automate their daily tasks
- Remote learners from any city in India joining our live online batch

No prior coding experience needed. We start from installing Python and end with you building real projects.
"""

GENAI_DESCRIPTION = """\
**Gen AI Master** — the only course in eastern UP that teaches you to build apps, websites, content, \
and businesses using AI tools — without writing hundreds of lines of code yourself.

Welcome to the age of **Vibe Coding**. You describe what you want. AI builds it. You refine, ship, and get paid.

---

### What is Vibe Coding?

Vibe Coding is a new way of building software where you **talk to AI** instead of writing code line \
by line. Tools like Cursor, Bolt.new, Lovable, Replit Agent, and v0 by Vercel let you describe an \
app in plain English (or Hindi) — and the AI generates a working application in minutes.

This isn't a shortcut. This is how software is being built in 2026 by real companies, real \
freelancers, and real startups worldwide. And you can learn it right here in Mughalsarai.

---

### What you'll master in 4 months

**AI Thinking & Prompt Engineering**
The foundation. Learn how to talk to AI so it gives you exactly what you want — first time, every \
time. Prompting is the #1 skill of 2026.

**AI Content Creation**
Generate blog posts, social media content, marketing copy, images, presentations, and videos — all \
using AI. One person with AI tools can do the work of a 5-person team.

**Vibe Coding — Build Apps Without Heavy Coding**
Use Cursor, Bolt.new, Lovable, v0, and Replit Agent to build real web apps, dashboards, landing \
pages, and tools. You guide the AI with prompts and light edits — no CS degree needed.

**AI Automation & Workflows**
Connect AI tools together to automate repetitive work — email sequences, data extraction, report \
generation, social media posting. Work smarter, not harder.

**AI for Business & Freelancing**
Turn your AI skills into income — freelance on Fiverr/Upwork, build micro-SaaS products, offer AI \
consulting to local businesses in Mughalsarai, Chandauli, and Varanasi.

---

### Tools you'll learn (hands-on, not just theory)

AI Chatbots: ChatGPT (GPT-4o), Claude, Gemini, Perplexity | \
Vibe Coding: Cursor, Bolt.new, Lovable, v0 by Vercel, Replit Agent | \
AI Images: Midjourney, DALL-E 3, Ideogram, Canva AI | \
AI Video: Runway, HeyGen, CapCut AI, Synthesia | \
AI Presentations: Gamma, Canva AI, Beautiful.ai | \
AI Writing: ChatGPT, Claude, Jasper, Copy.ai | \
AI Automation: Zapier AI, Make.com, n8n basics | \
AI Audio: ElevenLabs, NotebookLM, Suno AI | \
AI for Code: GitHub Copilot, Cursor AI, Claude Code | \
AI Design: Canva AI, Figma AI, Framer AI

---

### Who is this for?

- Students (Class 12+) who want the most future-proof skill of 2026
- Graduates who don't want to learn traditional coding but want to build tech products
- Small business owners in Mughalsarai, Chandauli, Varanasi who want to use AI for their work
- Freelancers who want to 10x their output and charge more
- Content creators, social media managers, and marketers
- Anyone curious about AI who wants to go from "I've heard of ChatGPT" to "I build with AI daily"

**No programming background needed. No engineering degree required. If you can type and think \
clearly, you can master Gen AI.**

---

### Career & income outcomes

- AI Content Creator (₹15,000–₹40,000/month)
- Prompt Engineer (₹25,000–₹60,000/month)
- Vibe Coder / AI App Builder (₹20,000–₹50,000/month or per-project freelancing)
- AI Automation Specialist (₹20,000–₹45,000/month)
- Freelancer on Fiverr/Upwork using AI (₹500–₹5,000 per task)
- AI Consultant for local businesses (₹5,000–₹25,000 per client/month)
- Micro-SaaS Builder — build small AI-powered tools and sell subscriptions

---

### Future secure karo — AI ke saath!

Language is never a barrier — classes are in Hindi + English. Small batch of 25 students. Morning, \
afternoon, and evening batches. You'll use AI tools in every single class — no boring theory lectures.
"""


# ---------------------------------------------------------------------------
# Course definitions
# ---------------------------------------------------------------------------
COURSES = [
    # ── 1. DevOps for Beginners ─────────────────────────────────────────────
    dict(
        category_slug="programming",
        data=CourseCreate(
            title="DevOps for Beginners",
            slug="devops-for-beginners",
            category_id=0,
            level="beginner",
            short_description=(
                "Learn DevOps from scratch in 4 months. Master Linux, Git, Docker, Jenkins, CI/CD "
                "pipelines, AWS basics, Kubernetes intro, and infrastructure automation. Hands-on labs "
                "in every class. No prior DevOps experience needed. Offline classes in Mughalsarai."
            ),
            description=DEVOPS_DESCRIPTION,
            price=15000,
            original_price=22000,
            currency="INR",
            emi_available=True,
            emi_amount=3750,
            duration="4 months",
            duration_hours=96,
            batch_size=25,
            rating=5.0,
            review_count=6,
            enrollment_count=8,
            placement_rate=80,
            instructor_name="TechPath Instructor",
            instructor_title="DevOps & Cloud Infrastructure Trainer",
            instructor_bio=(
                "Experienced in building CI/CD pipelines, managing containerised workloads, and automating "
                "cloud infrastructure on AWS. Has trained students across Mughalsarai, Chandauli, and Varanasi "
                "in Linux administration, Docker, and deployment automation with a hands-on, lab-first approach."
            ),
            status="published",
            featured=False,
            is_active=True,
            certification_name="DevOps for Beginners Certificate",
            certification_authority="TechPath",
            meta_title="DevOps for Beginners – Docker, AWS, CI/CD | TechPath Mughalsarai",
            meta_description=(
                "Learn DevOps in 4 months at TechPath Mughalsarai. Linux, Docker, Jenkins, AWS, CI/CD "
                "pipelines. Hands-on labs, beginner-friendly. EMI available. Enrol now."
            ),
            learning_outcomes=[
                "Navigate the Linux filesystem and manage files, users, and permissions from the terminal",
                "Write Bash shell scripts to automate repetitive system administration tasks",
                "Use Git for version control — branching, merging, pull requests, and collaboration on GitHub",
                "Build Docker images, run containers, and manage multi-container applications with Docker Compose",
                "Set up and configure Jenkins for automated build, test, and deployment workflows",
                "Build a complete CI/CD pipeline using GitHub Actions or Jenkins",
                "Launch and manage virtual servers on AWS (EC2, S3, IAM basics)",
                "Deploy a web application to a cloud server with Nginx as a reverse proxy",
                "Understand the basics of Kubernetes — pods, deployments, and services",
                "Write infrastructure configuration files that can be version-controlled and reused",
                "Monitor application logs and troubleshoot deployment failures systematically",
            ],
            prerequisites=[
                "Basic computer familiarity (file management, using a browser, typing)",
                "Comfort with learning from the command line (we will teach you, but willingness matters)",
                "No prior programming or DevOps experience required",
                "Class 12 pass (BCA / BSc IT / B.Tech students will find it especially valuable)",
                "Laptop with at least 8 GB RAM (required for running Docker and virtual machines)",
            ],
            curriculum=[
                CurriculumModule(
                    title="Linux Fundamentals",
                    duration="3 weeks",
                    topics=["What is Linux", "Installing Ubuntu (VM or WSL)", "Terminal navigation",
                            "File and directory commands", "Permissions (chmod chown)", "Users and groups",
                            "Package management (apt)", "Process management", "Cron jobs", "SSH basics"],
                ),
                CurriculumModule(
                    title="Shell Scripting",
                    duration="2 weeks",
                    topics=["Bash scripting basics", "Variables", "Conditionals (if else)",
                            "Loops (for while)", "Functions", "Input and output", "Reading files",
                            "Automating backups", "Log rotation script", "System monitoring script"],
                ),
                CurriculumModule(
                    title="Git & GitHub",
                    duration="2 weeks",
                    topics=["Git init add commit", "Branching and merging", "Merge conflicts",
                            ".gitignore", "Remote repositories", "GitHub push pull",
                            "Pull requests", "Code review workflow", "Tags and releases",
                            "Collaboration best practices"],
                ),
                CurriculumModule(
                    title="Networking & Web Server Basics",
                    duration="1 week",
                    topics=["IP addresses and ports", "DNS basics", "HTTP and HTTPS", "curl and wget",
                            "Firewall basics (ufw)", "Nginx installation", "Serving a static site with Nginx",
                            "Reverse proxy concept", "SSL with Let's Encrypt (overview)"],
                ),
                CurriculumModule(
                    title="Docker — Containers from Scratch",
                    duration="3 weeks",
                    topics=["What are containers", "Docker install", "Docker images and containers",
                            "Dockerfile writing", "Building custom images", "Port mapping",
                            "Volumes and data persistence", "Environment variables",
                            "Docker Hub push pull", "Dockerising a Python Flask app",
                            "Dockerising a Node.js app"],
                ),
                CurriculumModule(
                    title="Docker Compose & Multi-Container Apps",
                    duration="2 weeks",
                    topics=["What is Docker Compose", "docker-compose.yml structure",
                            "Multi-container setup (app + database)", "Networking between containers",
                            "Environment files",
                            "Deploying a full stack app (frontend + backend + PostgreSQL)",
                            "Compose commands (up down logs exec)"],
                ),
                CurriculumModule(
                    title="CI/CD Pipelines — Jenkins",
                    duration="3 weeks",
                    topics=["What is CI/CD", "Jenkins installation (Docker)", "Jenkins dashboard",
                            "Freestyle jobs", "Pipeline as code (Jenkinsfile)",
                            "Build triggers (webhook)", "Automated testing in pipeline",
                            "Build artifacts", "Notifications on failure", "Pipeline best practices"],
                ),
                CurriculumModule(
                    title="CI/CD with GitHub Actions",
                    duration="1 week",
                    topics=["GitHub Actions overview", "Workflow YAML syntax",
                            "Triggers (push pull_request)", "Jobs and steps",
                            "Running tests automatically", "Building Docker images in CI",
                            "Deploying from GitHub Actions", "Secrets management",
                            "Comparing Jenkins vs GitHub Actions"],
                ),
                CurriculumModule(
                    title="AWS Cloud Basics",
                    duration="3 weeks",
                    topics=["What is cloud computing", "AWS free tier signup", "AWS Console overview",
                            "EC2 (launch connect manage)", "Security groups", "Key pairs",
                            "S3 (storage buckets)", "IAM (users roles policies)",
                            "Deploying an app on EC2", "Nginx + app on EC2", "Elastic IP",
                            "Cost monitoring"],
                ),
                CurriculumModule(
                    title="Kubernetes Introduction",
                    duration="2 weeks",
                    topics=["Why Kubernetes", "Minikube setup (local)", "kubectl basics",
                            "Pods", "Deployments", "Services (ClusterIP NodePort)",
                            "Scaling replicas", "YAML manifests",
                            "Deploying a containerised app on Kubernetes",
                            "Dashboard overview", "When to use Kubernetes vs Docker Compose"],
                ),
                CurriculumModule(
                    title="Monitoring, Logging & Infrastructure as Code",
                    duration="1 week",
                    topics=["Application logging best practices", "Docker logs",
                            "CloudWatch basics (AWS)", "Uptime monitoring concepts",
                            "Infrastructure as Code concept", "Terraform overview",
                            "Ansible overview", "Choosing the right tool for the job"],
                ),
                CurriculumModule(
                    title="Capstone Project & Career Preparation",
                    duration="3 weeks",
                    topics=["Capstone project (end-to-end pipeline)", "Project documentation",
                            "Architecture diagram", "Resume building for DevOps roles",
                            "LinkedIn optimisation", "GitHub portfolio with CI/CD projects",
                            "Mock interviews (scenario-based)", "Freelance DevOps consulting basics",
                            "Career roadmap (junior to senior)"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Do I need to know programming before joining this course?",
                    answer=(
                        "No. This course does not require prior programming knowledge. You will learn shell "
                        "scripting (Bash) as part of the curriculum, which is enough for DevOps work. However, "
                        "if you already know Python or any other language, it will help you understand certain "
                        "concepts faster. If you have completed our Python course, this is an excellent next step."
                    ),
                ),
                FAQItem(
                    question="What is the difference between DevOps and software development?",
                    answer=(
                        "Software developers write the application code. DevOps engineers make sure that code "
                        "is tested, packaged, deployed, and running reliably on servers — automatically. Think "
                        "of developers as people who build the car, and DevOps engineers as people who build "
                        "the road, the traffic system, and the fuel station. Both are essential, and both are well-paid."
                    ),
                ),
                FAQItem(
                    question="Is DevOps in demand in India? Can I get a job from a small town?",
                    answer=(
                        "DevOps is one of the most in-demand and highest-paid IT specialisations in India. "
                        "There is a significant shortage of DevOps professionals. Most DevOps work is done "
                        "remotely — you can work from Mughalsarai for a company in Bangalore, Pune, or even "
                        "internationally. What matters is your skills and your GitHub portfolio, not your city."
                    ),
                ),
                FAQItem(
                    question="What kind of laptop do I need for this course?",
                    answer=(
                        "You need a laptop with at least 8 GB RAM (16 GB recommended) to run Docker and virtual "
                        "machines smoothly. Any operating system works — Windows (with WSL2), macOS, or Linux. "
                        "We will help you set everything up in the first week. If you do not have a laptop, our "
                        "lab computers are available during class hours."
                    ),
                ),
                FAQItem(
                    question="Will I learn AWS in this course? Do I need to pay for it?",
                    answer=(
                        "Yes, we cover AWS basics — EC2, S3, IAM, and deploying applications. AWS offers a free "
                        "tier that is sufficient for all our labs and projects. You will not need to spend any "
                        "money on cloud services during the course. We guide you through the free tier setup and "
                        "teach you how to monitor costs so you never get an unexpected bill."
                    ),
                ),
                FAQItem(
                    question="What is the fee structure? Is EMI available?",
                    answer=(
                        "The course fee is Rs.15,000 (discounted from Rs.22,000). EMI is available at Rs.3,750 "
                        "per month for 4 months. A free demo class is available so you can experience the "
                        "teaching style before enrolling. Contact us at +91 8299708052 to book your demo."
                    ),
                ),
                FAQItem(
                    question="How deep does the Kubernetes module go?",
                    answer=(
                        "We cover the fundamentals — enough for you to understand what Kubernetes does, run "
                        "applications on a local Minikube cluster, and read Kubernetes YAML manifests. This is "
                        "a beginner course, so we do not cover advanced topics like Helm charts, Istio, or "
                        "production cluster management. After completing this course, you will have a solid "
                        "foundation to continue learning Kubernetes on your own."
                    ),
                ),
                FAQItem(
                    question="I am a working professional. Are evening batches available?",
                    answer=(
                        "Yes. We offer morning (9-11 AM), afternoon (1-3 PM), and evening (5-7 PM) batches. "
                        "Weekend doubt-clearing sessions are free for all enrolled students. The course is "
                        "designed to be manageable alongside a job or college schedule if you can dedicate "
                        "1-2 hours of daily practice outside class."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="Linux Server Setup & Automation",
                    description=(
                        "Set up a Linux server (Ubuntu VM or WSL), create users with specific permissions, "
                        "install Nginx, configure a firewall, and write a Bash script that automates daily "
                        "log backups with email notification on failure."
                    ),
                ),
                ProjectItem(
                    title="Dockerised Full Stack Application",
                    description=(
                        "Take a simple web application (Python Flask backend + static frontend + PostgreSQL "
                        "database) and containerise the entire stack using Docker. Write a Dockerfile for each "
                        "component and a docker-compose.yml that brings everything up with a single command."
                    ),
                ),
                ProjectItem(
                    title="CI/CD Pipeline with Jenkins",
                    description=(
                        "Set up a Jenkins server (running in Docker), connect it to a GitHub repository, and "
                        "build a pipeline that automatically runs tests, builds a Docker image, and deploys it "
                        "to a staging server on every code push. Include failure notifications."
                    ),
                ),
                ProjectItem(
                    title="Deploy to AWS Cloud",
                    description=(
                        "Launch an EC2 instance on AWS, configure security groups, install Docker, deploy your "
                        "containerised application, set up Nginx as a reverse proxy, and assign an Elastic IP. "
                        "The application should be accessible from a public URL."
                    ),
                ),
                ProjectItem(
                    title="Kubernetes Local Deployment",
                    description=(
                        "Deploy a multi-container application on a local Minikube cluster. Write Kubernetes YAML "
                        "manifests for pods, deployments, and services. Scale the application up and down. "
                        "Access it through a NodePort service from your browser."
                    ),
                ),
                ProjectItem(
                    title="Capstone — End-to-End DevOps Pipeline",
                    description=(
                        "Build a complete DevOps pipeline from scratch for an application of your choice. The "
                        "pipeline must include: source code on GitHub, automated tests on every push (GitHub "
                        "Actions or Jenkins), Docker image build and push to Docker Hub, deployment to an AWS "
                        "EC2 instance, Nginx reverse proxy, and basic monitoring/logging. Document the entire "
                        "architecture with a diagram. This project becomes the centrepiece of your portfolio."
                    ),
                ),
            ],
            skill_ids=[],
        ),
        skill_slugs=["linux", "git", "docker", "jenkins", "cicd", "aws", "kubernetes",
                     "shell-scripting", "devops", "cloud-computing", "nginx", "github-actions"],
    ),

    # ── 2. Python Programming ───────────────────────────────────────────────
    dict(
        category_slug="programming",
        data=CourseCreate(
            title="Python Programming",
            slug="python-programming",
            category_id=0,
            level="beginner",
            short_description=(
                "Learn Python from scratch in 3 months. Covers Python 3.x, variables, loops, functions, "
                "OOP, file handling, modules, and real projects. Offline classes in Mughalsarai + live "
                "online batches available. Beginner-friendly, project-led, instructor-led training."
            ),
            description=PYTHON_DESCRIPTION,
            price=6000,
            original_price=10000,
            currency="INR",
            emi_available=True,
            emi_amount=2000,
            duration="3 months",
            duration_hours=72,
            batch_size=25,
            rating=5.0,
            review_count=15,
            enrollment_count=25,
            placement_rate=70,
            instructor_name="TechPath Instructor",
            instructor_title="Senior Python Developer",
            instructor_bio=(
                "Experienced in teaching Python and building production applications. Has trained 200+ students "
                "across Mughalsarai, Chandauli, and Varanasi — both offline and online. Specialises in making "
                "programming accessible to first-time coders through real-world projects and Hindi + English instruction."
            ),
            status="published",
            featured=True,
            is_active=True,
            certification_name="Python Programming Certificate",
            certification_authority="TechPath",
            meta_title="Python Programming Course – 3 Months Offline & Online | TechPath",
            meta_description=(
                "Learn Python in 3 months at TechPath Mughalsarai or live online. From basics to OOP, "
                "file handling, and real projects. Beginner-friendly. EMI available. Enrol now."
            ),
            learning_outcomes=[
                "Install Python, set up VS Code, and write your first program from scratch",
                "Use variables, data types, operators, and string formatting confidently",
                "Write conditional logic (if / elif / else) and loops (for / while) to solve real problems",
                "Define and use functions with parameters, return values, and default arguments",
                "Work with lists, tuples, dictionaries, and sets for data storage and manipulation",
                "Handle files — read, write, append text files and work with CSV and JSON data",
                "Understand and apply Object-Oriented Programming — classes, objects, inheritance, encapsulation",
                "Handle errors gracefully using try / except / finally",
                "Use Python modules and install third-party packages with pip",
                "Use Git and GitHub for version control and project hosting",
                "Build 5+ real projects and host them on GitHub as a portfolio",
            ],
            prerequisites=[
                "Basic computer use (files, folders, browser, typing)",
                "No prior coding or programming experience required",
                "Class 10 pass (recommended, not mandatory)",
                "Laptop for practice (required for online students, recommended for offline)",
                "For online batch: stable internet connection and a quiet study space",
            ],
            curriculum=[
                CurriculumModule(
                    title="Getting Started with Python",
                    duration="1 week",
                    topics=["What is Python", "Installing Python 3.12", "VS Code setup",
                            "Running your first script", "print()", "comments",
                            "Python shell vs script mode", "Input/Output basics"],
                ),
                CurriculumModule(
                    title="Variables, Data Types & Operators",
                    duration="2 weeks",
                    topics=["Variables", "int float str bool", "Type casting",
                            "Arithmetic operators", "Comparison operators", "Logical operators",
                            "Assignment operators", "f-strings", "String methods", "Input from user"],
                ),
                CurriculumModule(
                    title="Control Flow — Conditions & Loops",
                    duration="2 weeks",
                    topics=["if elif else", "Nested conditions", "for loop", "while loop",
                            "break continue pass", "range()", "Nested loops",
                            "Pattern printing", "Loop exercises", "Real-world decision programs"],
                ),
                CurriculumModule(
                    title="Functions & Modules",
                    duration="2 weeks",
                    topics=["Defining functions", "Parameters and return", "Default arguments",
                            "*args **kwargs", "Lambda functions", "map() filter()",
                            "Scope (local global)", "Importing modules",
                            "math random os datetime", "Installing packages with pip",
                            "Virtual environments"],
                ),
                CurriculumModule(
                    title="Data Structures",
                    duration="2 weeks",
                    topics=["Lists (create append remove sort slice)", "Tuples", "Sets",
                            "Dictionaries (keys values items)", "Nested data structures",
                            "List comprehension", "Dictionary comprehension",
                            "When to use which data structure", "Practice problems"],
                ),
                CurriculumModule(
                    title="File Handling & Data Formats",
                    duration="1 week",
                    topics=["open() read write append", "Reading line by line", "with statement",
                            "CSV read and write", "JSON load dump", "os module (file paths directories)",
                            "Building a file organiser script", "Error handling with files"],
                ),
                CurriculumModule(
                    title="Exception Handling & Debugging",
                    duration="1 week",
                    topics=["try except finally", "Catching specific exceptions", "raise",
                            "Custom exceptions", "Debugging with print", "VS Code debugger",
                            "Common Python errors and how to fix them", "Writing robust code"],
                ),
                CurriculumModule(
                    title="Object-Oriented Programming",
                    duration="2 weeks",
                    topics=["Classes and objects", "__init__ and self", "Attributes and methods",
                            "Inheritance", "Method overriding", "Encapsulation (public private)",
                            "Polymorphism", "@property decorator", "__str__ __repr__",
                            "OOP project (BankAccount or Library system)"],
                ),
                CurriculumModule(
                    title="Working with External Libraries",
                    duration="1 week",
                    topics=["requests (HTTP calls)", "BeautifulSoup (web scraping basics)",
                            "pandas basics (reading CSV)", "matplotlib basics (simple charts)",
                            "Building a web scraper project",
                            "API basics (fetching weather or news data)"],
                ),
                CurriculumModule(
                    title="Git, GitHub & Project Work",
                    duration="2 weeks",
                    topics=["Git init add commit", "Branching and merging", ".gitignore",
                            "GitHub repository", "Push pull", "README writing",
                            "GitHub profile setup",
                            "Project: build and upload 2 complete projects",
                            "Code review with instructor", "Portfolio presentation"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="I have never written a single line of code. Can I still join?",
                    answer=(
                        "Absolutely. This course is designed for complete beginners. We start from installing "
                        "Python and writing print('Hello'). By the end of 3 months, you will be writing programs "
                        "with functions, classes, file handling, and real projects. Hundreds of students with "
                        "zero coding background have successfully completed this course at TechPath."
                    ),
                ),
                FAQItem(
                    question="Is this course available online or only in Mughalsarai?",
                    answer=(
                        "Both. We offer offline classes at our Mughalsarai centre on Circus Road (near DDU "
                        "Junction) and live online classes with the same instructor and curriculum. Online "
                        "students join via Google Meet or Zoom — live, interactive classes with real-time screen "
                        "sharing and doubt clearing. WhatsApp support and weekend doubt sessions are included."
                    ),
                ),
                FAQItem(
                    question="How is an online batch different from YouTube tutorials?",
                    answer=(
                        "YouTube gives you videos with no structure, no feedback, and no accountability. Our "
                        "online batch gives you a live instructor, a fixed schedule, assignments with deadlines, "
                        "code reviews, project guidance, and WhatsApp doubt support. You also get a certificate "
                        "and placement assistance — none of which YouTube provides."
                    ),
                ),
                FAQItem(
                    question="What can I do after completing this Python course?",
                    answer=(
                        "You have several paths. You can take our Python Full Stack course to become a web "
                        "developer. You can move to Data Science + AI/ML for analytics and machine learning. "
                        "You can take DevOps for cloud and infrastructure. Or you can start freelancing "
                        "immediately — Python automation scripts, web scrapers, and data processing jobs are "
                        "always in demand on Fiverr and Upwork."
                    ),
                ),
                FAQItem(
                    question="What is the fee? Is EMI available?",
                    answer=(
                        "The course fee is Rs.6,000 (discounted from Rs.10,000). EMI is available at Rs.2,000 "
                        "per month for 3 months. The fee is the same for both offline and online batches. "
                        "A free demo class is available — contact us at +91 8299708052 to book."
                    ),
                ),
                FAQItem(
                    question="Which version of Python will I learn?",
                    answer=(
                        "Python 3.12 (latest stable version). We keep the curriculum updated with every major "
                        "Python release. You will use VS Code as your editor, which is the most popular code "
                        "editor used by professional developers worldwide."
                    ),
                ),
                FAQItem(
                    question="I am from Arts / Commerce stream. Is this course suitable for me?",
                    answer=(
                        "Yes. Programming has nothing to do with your school stream. Python reads like English "
                        "— if you can write 'if age >= 18: print(You can vote)', you can learn Python. We have "
                        "had successful students from BA, BCom, BSc, and even students who did not attend "
                        "college. What matters is your willingness to practice."
                    ),
                ),
                FAQItem(
                    question="Will I get a certificate? Is it valid for jobs?",
                    answer=(
                        "You will receive a Python Programming Certificate from TechPath upon course completion. "
                        "More importantly, you will have a GitHub profile with 5+ real projects — and that is "
                        "what employers actually look at during hiring. We also help you build your resume and "
                        "prepare for technical interviews."
                    ),
                ),
                FAQItem(
                    question="What are the batch timings?",
                    answer=(
                        "We offer three batch slots — morning (9-11 AM), afternoon (1-3 PM), and evening "
                        "(5-7 PM). The same timings apply for both offline and online batches. Weekend "
                        "doubt-clearing sessions are free for all enrolled students."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="CLI Calculator",
                    description=(
                        "Build a command-line calculator that supports addition, subtraction, multiplication, "
                        "division, and modulus. Handle edge cases like division by zero and invalid input. "
                        "Use functions for each operation and a loop-based menu system."
                    ),
                ),
                ProjectItem(
                    title="Student Grade Manager",
                    description=(
                        "A program that takes student names and marks for 5 subjects, calculates percentage, "
                        "assigns grades (A/B/C/D/F), and saves the results to a CSV file. Includes a search "
                        "function to look up any student's results by name."
                    ),
                ),
                ProjectItem(
                    title="File Organiser Script",
                    description=(
                        "A Python script that scans a messy folder and automatically sorts files into subfolders "
                        "by type — Images, Documents, Videos, Audio, Code, and Others. Uses the os and shutil "
                        "modules. Run it once and your Downloads folder is clean forever."
                    ),
                ),
                ProjectItem(
                    title="To-Do App (CLI with JSON Storage)",
                    description=(
                        "A command-line to-do application where you can add tasks, mark them complete, delete "
                        "them, and view all tasks. Data is stored in a JSON file so tasks persist between "
                        "sessions. Uses functions, dictionaries, file handling, and a menu-driven interface."
                    ),
                ),
                ProjectItem(
                    title="Web Scraper",
                    description=(
                        "Build a Python script using requests and BeautifulSoup that scrapes data from a public "
                        "website (such as quotes, news headlines, or product prices), cleans the data, and saves "
                        "it as a formatted CSV file. Includes error handling for network failures."
                    ),
                ),
                ProjectItem(
                    title="Mini Project — Your Choice",
                    description=(
                        "Choose your own project idea and build it from scratch. Examples: a quiz game, a "
                        "password generator, a contact book, a weather app using an API, an expense tracker, "
                        "or a simple chatbot. Must use functions, file handling or an API, and be hosted on "
                        "GitHub with a proper README. This is your portfolio showpiece."
                    ),
                ),
            ],
            skill_ids=[],
        ),
        skill_slugs=["python", "python-3", "oop", "file-handling", "git", "github",
                     "automation", "web-scraping", "cli-apps", "beginner-programming"],
    ),

    # ── 3. Gen AI Master ────────────────────────────────────────────────────
    dict(
        category_slug="artificial-intelligence",
        data=CourseCreate(
            title="Gen AI Master",
            slug="gen-ai-master",
            category_id=0,
            level="beginner",
            short_description=(
                "Master every Gen AI tool in 4 months — ChatGPT, Claude, Gemini, Midjourney, Cursor, "
                "Bolt, Lovable, v0, Canva AI, Gamma, and more. Learn vibe coding, AI app building, "
                "prompt engineering, and AI-powered business skills. No heavy coding needed. Offline in Mughalsarai."
            ),
            description=GENAI_DESCRIPTION,
            price=15000,
            original_price=22000,
            currency="INR",
            emi_available=True,
            emi_amount=3750,
            duration="4 months",
            duration_hours=96,
            batch_size=25,
            rating=5.0,
            review_count=10,
            enrollment_count=15,
            placement_rate=75,
            instructor_name="TechPath Instructor",
            instructor_title="Gen AI & Vibe Coding Specialist",
            instructor_bio=(
                "Specialises in building products, content, and automations using Gen AI tools. Has built 30+ "
                "web apps using vibe coding (Cursor, Bolt, Lovable), created AI-powered content workflows, and "
                "trained students across Mughalsarai, Chandauli, and Varanasi to turn AI skills into real income."
            ),
            status="published",
            featured=True,
            is_active=True,
            certification_name="Gen AI Master Certificate",
            certification_authority="TechPath",
            meta_title="Gen AI Master Course – Vibe Coding & AI Tools | TechPath Mughalsarai",
            meta_description=(
                "Master ChatGPT, Claude, Cursor, Bolt, Midjourney & 20+ AI tools in 4 months at TechPath "
                "Mughalsarai. Vibe coding, prompt engineering, AI freelancing. Enrol now."
            ),
            learning_outcomes=[
                "Write expert-level prompts for ChatGPT, Claude, and Gemini to get precise outputs every time",
                "Build complete web apps, landing pages, and dashboards using vibe coding tools (Cursor, Bolt.new, Lovable, v0)",
                "Generate professional images, logos, and social media creatives using Midjourney, DALL-E, and Canva AI",
                "Create AI-powered presentations in minutes using Gamma and Canva AI",
                "Produce short-form and long-form video content using AI video tools",
                "Set up no-code AI automation workflows using Zapier AI and Make.com",
                "Build and deploy a micro-SaaS product or AI-powered tool without traditional coding",
                "Offer AI freelance services on Fiverr and Upwork with a ready portfolio",
                "Consult local businesses on how to use AI to save time and money",
                "Understand AI ethics, limitations, hallucinations, and when NOT to trust AI output",
            ],
            prerequisites=[
                "Basic computer use (browser, typing, file management)",
                "A smartphone with internet access",
                "No coding or programming experience required",
                "No specific educational qualification needed — Class 10+ is enough",
                "Curiosity about AI and willingness to experiment",
            ],
            curriculum=[
                CurriculumModule(
                    title="AI Foundations & Prompt Engineering",
                    duration="2 weeks",
                    topics=["What is Gen AI", "How LLMs work (simple explanation)",
                            "ChatGPT vs Claude vs Gemini comparison", "Account setup",
                            "Prompt engineering basics", "Zero-shot Few-shot Chain-of-thought prompting",
                            "System prompts", "Prompt templates library",
                            "Getting perfect outputs first time"],
                ),
                CurriculumModule(
                    title="Advanced Prompting & AI Thinking",
                    duration="1 week",
                    topics=["Role-based prompting", "Mega-prompts", "Prompt chaining",
                            "Multi-step reasoning", "Handling hallucinations",
                            "Fact-checking AI output", "When NOT to trust AI",
                            "Context window management", "Custom GPTs", "Claude Projects"],
                ),
                CurriculumModule(
                    title="AI Content Writing & Copywriting",
                    duration="2 weeks",
                    topics=["Blog writing with AI", "Social media captions", "Ad copy",
                            "Email sequences", "Product descriptions", "SEO content",
                            "LinkedIn posts", "YouTube scripts",
                            "Rewriting and humanising AI text", "Plagiarism checking",
                            "Building a content portfolio"],
                ),
                CurriculumModule(
                    title="AI Image & Design",
                    duration="2 weeks",
                    topics=["Midjourney prompts and styles", "DALL-E 3 via ChatGPT",
                            "Ideogram for text-in-images",
                            "Canva AI (Magic Design Magic Write Magic Edit)",
                            "Logo creation", "Social media templates", "Poster design",
                            "AI background removal", "Image upscaling",
                            "Building a design portfolio"],
                ),
                CurriculumModule(
                    title="AI Video & Audio",
                    duration="1 week",
                    topics=["Runway Gen-3 basics", "HeyGen AI avatars", "CapCut AI editing",
                            "Synthesia for explainer videos", "ElevenLabs voice cloning",
                            "Suno AI music", "NotebookLM audio overview",
                            "AI subtitles and translation", "Reels and Shorts workflow with AI"],
                ),
                CurriculumModule(
                    title="AI Presentations & Documents",
                    duration="1 week",
                    topics=["Gamma AI presentations", "Canva AI decks", "Beautiful.ai",
                            "AI-generated reports", "Pitch decks for startups",
                            "Client proposals with AI", "Resume and cover letter with AI",
                            "One-click formatting and design"],
                ),
                CurriculumModule(
                    title="Vibe Coding — Build Apps with AI (Part 1)",
                    duration="3 weeks",
                    topics=["What is vibe coding",
                            "HTML CSS JS basics (just enough to understand AI output)",
                            "Cursor AI setup", "Building a landing page with Cursor",
                            "Bolt.new — describe and deploy",
                            "Lovable — full app from prompt",
                            "v0 by Vercel — UI components from text",
                            "Editing AI-generated code (light touch)",
                            "Debugging with AI help"],
                ),
                CurriculumModule(
                    title="Vibe Coding — Build & Ship (Part 2)",
                    duration="2 weeks",
                    topics=["Replit Agent — full app generation", "Building a calculator app",
                            "Building a quiz app", "Building a portfolio site",
                            "Building a dashboard", "Adding database (Supabase basics)",
                            "Deploying to Vercel or Netlify", "Custom domains",
                            "Sharing your live app", "GitHub basics for saving projects"],
                ),
                CurriculumModule(
                    title="AI Automation & Workflows",
                    duration="2 weeks",
                    topics=["Zapier AI basics", "Make.com scenarios",
                            "Connecting AI tools together", "Auto-post to social media",
                            "Auto-reply emails with AI", "Data scraping to spreadsheet",
                            "Google Sheets AI formulas", "WhatsApp automation basics",
                            "n8n self-hosted intro", "Building a personal AI assistant workflow"],
                ),
                CurriculumModule(
                    title="AI for Business & Freelancing",
                    duration="1 week",
                    topics=["Fiverr profile setup", "Upwork proposal writing with AI",
                            "Pricing AI services", "Client communication",
                            "AI consulting for local businesses (shops clinics coaching)",
                            "Micro-SaaS concept", "Selling AI-generated templates",
                            "Building recurring income with AI skills"],
                ),
                CurriculumModule(
                    title="Capstone Projects & Portfolio",
                    duration="2 weeks",
                    topics=["Capstone project 1 (vibe coded app)",
                            "Capstone project 2 (AI content or automation)",
                            "Portfolio website with all projects", "GitHub profile",
                            "LinkedIn optimisation", "Resume with AI skills",
                            "Mock interviews", "Freelance pitch practice",
                            "Course completion presentation"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Kya mujhe coding aani chahiye is course ke liye?",
                    answer=(
                        "Bilkul nahi. Yahi is course ki khaas baat hai. Vibe coding mein aap AI ko bolte ho "
                        "kya banana hai — aur AI code likh deta hai. Aapko sirf samajhna hai ki output sahi "
                        "hai ya nahi, aur thoda edit karna hai. Hum basic HTML/CSS sikhayenge (1 class mein) "
                        "taaki aap AI ka output samajh sakein. Heavy coding bilkul nahi hai."
                    ),
                ),
                FAQItem(
                    question="What exactly is vibe coding? Is it real or a gimmick?",
                    answer=(
                        "Vibe coding is how a growing number of real apps are being built in 2026. Tools like "
                        "Cursor, Bolt.new, and Lovable let you describe what you want in plain English, and AI "
                        "generates a working app. Y Combinator startups, indie hackers, and freelancers worldwide "
                        "are using this daily. It's not a replacement for traditional coding — it's a new, faster "
                        "way to build things, especially for people who think well but don't want to memorise syntax."
                    ),
                ),
                FAQItem(
                    question="Is this course only for tech people?",
                    answer=(
                        "Not at all. We've designed this for anyone — commerce students, arts graduates, small "
                        "business owners, content creators, homemakers. If you use a smartphone and can explain "
                        "what you want clearly, you can use AI tools. Half the course is about content, design, "
                        "automation, and business — not coding at all."
                    ),
                ),
                FAQItem(
                    question="Course ki fees kitni hai? EMI milegi?",
                    answer=(
                        "Course fees Rs.15,000 hai (original Rs.22,000 se discounted). EMI available hai — "
                        "Rs.3,750 per month x 4 months. Free demo class bhi available hai — WhatsApp karo "
                        "+91 8299708052 par."
                    ),
                ),
                FAQItem(
                    question="Will these AI tools remain relevant or will they change in 6 months?",
                    answer=(
                        "Individual tools may update, but the core skill we teach — AI thinking and prompt "
                        "engineering — is permanent. Once you learn how to communicate with AI effectively, you "
                        "can pick up any new tool in a day. We focus on principles (how to prompt, how to verify, "
                        "how to chain tools) rather than just button clicks. We also keep the curriculum updated "
                        "quarterly — if a new tool replaces an old one, we swap it in."
                    ),
                ),
                FAQItem(
                    question="Kya main is course ke baad paise kama sakta/sakti hoon?",
                    answer=(
                        "Haan, bilkul. Bahut se students course ke dauraan hi freelancing shuru kar dete hain. "
                        "Fiverr par AI content writing Rs.500-Rs.2,000 per article milta hai. Vibe coding se ek "
                        "landing page banana Rs.3,000-Rs.10,000 ka kaam hai. Local business ko AI consulting dena "
                        "Rs.5,000-Rs.25,000/month ka kaam hai. Hum aapko freelance profile banana aur pehla client "
                        "paana — dono sikhayenge."
                    ),
                ),
                FAQItem(
                    question="How is this different from watching YouTube tutorials on ChatGPT?",
                    answer=(
                        "YouTube shows you one tool at a time, with no structure, no projects, and no "
                        "accountability. This course gives you a structured 4-month journey across 20+ tools, "
                        "with hands-on projects in every class, instructor feedback, portfolio building, and "
                        "freelance/placement support. You also learn things YouTube doesn't teach — prompt "
                        "chaining, AI automation, vibe coding, and how to actually charge money for AI skills."
                    ),
                ),
                FAQItem(
                    question="Is there an age limit? I'm 35 and work in a shop.",
                    answer=(
                        "No age limit. We have students from 16 to 45+. If you run a shop, AI can help you write "
                        "WhatsApp marketing messages, create product photos, build a simple website, and automate "
                        "customer follow-ups — all things we cover in this course. You don't need to become a "
                        "'tech person.' You just need to know how to use the tools."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="Prompt Engineering Portfolio",
                    description=(
                        "Create a documented collection of 30+ expert prompts across categories — writing, coding, "
                        "image generation, analysis, and business. Each prompt includes the input, output, and a "
                        "note on why it works. Hosted as a Notion page or GitHub repo."
                    ),
                ),
                ProjectItem(
                    title="AI Content Machine",
                    description=(
                        "Using only AI tools, produce a full week's content package for a fictional brand — "
                        "7 Instagram posts with AI-generated images, 3 blog articles, 5 LinkedIn posts, "
                        "2 email newsletters, and 1 YouTube script. Total production time target: under 4 hours."
                    ),
                ),
                ProjectItem(
                    title="Vibe Coded Web App",
                    description=(
                        "Build and deploy a working web application using Cursor, Bolt.new, or Lovable — choose "
                        "from: a quiz app, a recipe finder, a habit tracker, a local business directory, or your "
                        "own idea. Must be live on a real URL. No traditional coding — only AI-assisted building."
                    ),
                ),
                ProjectItem(
                    title="AI Automation Workflow",
                    description=(
                        "Build a 5-step automation using Zapier or Make.com — for example: when a Google Form is "
                        "submitted, AI generates a personalised email reply, logs the data in Google Sheets, posts "
                        "a summary to a channel, and sends a WhatsApp notification. Document the workflow with screenshots."
                    ),
                ),
                ProjectItem(
                    title="Local Business AI Makeover",
                    description=(
                        "Partner with a real local business in Mughalsarai or Chandauli (shop, clinic, tutor, "
                        "restaurant). Deliver: an AI-generated logo, a one-page website (vibe coded), 5 social "
                        "media creatives, a WhatsApp marketing message sequence, and a 1-page AI adoption plan. "
                        "Present as a client case study."
                    ),
                ),
                ProjectItem(
                    title="Capstone — Your AI Product or Service",
                    description=(
                        "Choose one path and execute it fully. Path A (Product): Build a micro-SaaS tool or "
                        "AI-powered app using vibe coding, deploy it, create a landing page, and get at least "
                        "5 real users. Path B (Service): Set up your Fiverr/Upwork profile, complete at least "
                        "2 paid gigs (or mock gigs), and document earnings and client feedback. This is your "
                        "graduation proof that you can turn AI skills into income."
                    ),
                ),
            ],
            skill_ids=[],
        ),
        skill_slugs=["gen-ai", "chatgpt", "claude", "gemini", "vibe-coding", "cursor",
                     "bolt", "lovable", "prompt-engineering", "midjourney", "canva-ai",
                     "ai-automation", "freelancing"],
    ),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    async with AsyncSessionLocal() as db:
        print("\n--- Categories ---")
        cat_prog = await get_or_create_category(db, "Programming",          "programming",          display_order=2)
        cat_ai   = await get_or_create_category(db, "Artificial Intelligence", "artificial-intelligence", display_order=4)
        await db.commit()

        cat_map = {
            "programming":            cat_prog,
            "artificial-intelligence": cat_ai,
        }

        print("\n--- Skills ---")
        skill_map: dict = {}
        for name, slug in ALL_SKILLS:
            existing = await skill_crud.get_by_slug(db, slug=slug)
            skill = await skill_crud.get_or_create(db, name=name, slug=slug)
            skill_map[slug] = skill
            print(f"  [{'skip' if existing else '+'}] {name}")
        await db.commit()
        for slug, skill in skill_map.items():
            await db.refresh(skill)

        print("\n--- Courses ---")
        for entry in COURSES:
            course_obj: CourseCreate = entry["data"]
            if await course_crud.get_by_slug(db, course_obj.slug):
                print(f"  [skip] already exists: {course_obj.title}")
                continue
            course_obj.category_id = cat_map[entry["category_slug"]].id
            course_obj.skill_ids   = [skill_map[s].id for s in entry["skill_slugs"]]
            await course_crud.create(db, obj_in=course_obj)
            print(f"  [+] created: {course_obj.title}")

        print("\nDone.\n")


if __name__ == "__main__":
    asyncio.run(main())
