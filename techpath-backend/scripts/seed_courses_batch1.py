#!/usr/bin/env python3
"""
Seed 3 courses into the TechPath database directly via ORM (no API auth needed).

Courses:
  1. Digital Marketing with Gen AI
  2. IoT Essentials (Internet of Things)
  3. Python Full Stack with Gen AI

Run from the techpath-backend/ directory:
  poetry run python scripts/seed_courses_batch1.py

Idempotent — skips any course whose slug already exists.
To add future courses: append to ALL_SKILLS and add a course block.
"""

import asyncio
import os
import sys

# Allow imports from the app package when run from techpath-backend/
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def get_or_create_category(db, name: str, slug: str, display_order: int = 0):
    cat = await course_category_crud.get_by_slug(db, slug=slug)
    if cat:
        print(f"  [skip] category already exists: {name}")
        return cat
    cat = await course_category_crud.create(
        db,
        obj_in=CourseCategoryCreate(
            name=name,
            slug=slug,
            display_order=display_order,
            is_active=True,
        ),
    )
    print(f"  [+] created category: {name}")
    return cat


# ---------------------------------------------------------------------------
# Skills master list  (name, slug)
# Add new skills here before adding a new course — duplicates are safe.
# ---------------------------------------------------------------------------
ALL_SKILLS = [
    # ── Digital Marketing ───────────────────────────────────────────────────
    ("SEO", "seo"),
    ("Social Media", "social-media"),
    ("Google Ads", "google-ads"),
    ("Meta Ads", "meta-ads"),
    ("ChatGPT", "chatgpt"),
    ("Gen AI", "gen-ai"),
    ("Content Marketing", "content-marketing"),
    ("Canva AI", "canva-ai"),
    ("Analytics", "analytics"),
    # ── IoT ─────────────────────────────────────────────────────────────────
    ("Arduino", "arduino"),
    ("NodeMCU", "nodemcu"),
    ("Raspberry Pi", "raspberry-pi"),
    ("IoT", "iot"),
    ("Sensors", "sensors"),
    ("Blynk", "blynk"),
    ("ThingSpeak", "thingspeak"),
    ("Embedded C", "embedded-c"),
    ("Electronics", "electronics"),
    # ── Python Full Stack ────────────────────────────────────────────────────
    ("Python", "python"),
    ("Django", "django"),
    ("React", "react"),
    ("JavaScript", "javascript"),
    ("HTML CSS", "html-css"),
    ("PostgreSQL", "postgresql"),
    ("REST API", "rest-api"),
    ("Git", "git"),
    ("GitHub", "github"),
    ("ChatGPT API", "chatgpt-api"),
    ("GitHub Copilot", "github-copilot"),
    ("Full Stack", "full-stack"),
]


# ---------------------------------------------------------------------------
# Course data
# ---------------------------------------------------------------------------

DM_DESCRIPTION = """\
Master **Digital Marketing powered by Generative AI** — the most in-demand skill combo of 2026. \
This 4-month, offline, instructor-led course covers SEO, social media marketing, paid ads, \
email marketing, content creation, and the AI tools that 10x a marketer's output. \
Designed for students, graduates, and small business owners in Mughalsarai, Chandauli, and Varanasi.

---

### What you'll build

- A live SEO-optimised blog with 10+ ranking articles
- Real Meta + Google Ads campaigns with measurable ROI
- A complete social media brand kit (Instagram, YouTube, LinkedIn)
- AI-powered content workflows using ChatGPT, Gemini, Claude, and Canva AI
- A client-ready freelance portfolio with case studies

---

### From beginner to job-ready

No marketing background needed. We start from "what is digital marketing" and take you to running \
real campaigns for real businesses. Hindi + English teaching means language is never a barrier.

You'll learn the same tools used by agencies in Mumbai, Bangalore, and Delhi — taught right here in Mughalsarai.

---

### Why Gen AI changes everything

A marketer who uses AI does in 1 hour what others do in 8. We teach you how to use ChatGPT for ad copy, \
Midjourney for creatives, Canva AI for designs, and analytics AI for insights — so you stand out the day you apply for jobs.

---

### Career outcomes

- Digital Marketing Executive (₹15,000–₹35,000/month starting)
- SEO Specialist
- Social Media Manager
- Performance Marketer (Meta + Google Ads)
- Freelance Content Marketer (₹500–₹2,000 per article)
- AI Content Strategist (emerging role, premium pay)
"""

IOT_DESCRIPTION = """\
**IoT Essentials** — a beginner-friendly, hands-on course that teaches you to build smart devices \
using Arduino, NodeMCU (ESP8266), and Raspberry Pi. In 4 months, you'll go from "what is a sensor?" \
to building a working smart home prototype — all without needing any prior coding or electronics background.

---

### What makes this course special?

We don't just show you circuit diagrams on a whiteboard. You get your own components kit from Day 1. \
Every class is 70% hands-on — you solder, wire, code, break things, fix them, and actually *build*.

Most IoT courses in Mughalsarai, Chandauli, and Varanasi either teach only Arduino or only theory. \
We cover **three platforms** — Arduino for basics, NodeMCU for WiFi-connected projects, and Raspberry Pi \
for mini-computer projects — so you understand the full IoT ecosystem.

---

### What you'll build (real projects, not simulations)

- LED patterns and traffic light controller (Arduino)
- Temperature & humidity monitor with LCD display (Arduino)
- WiFi-controlled LED from your phone (NodeMCU)
- Live sensor data on ThingSpeak cloud dashboard (NodeMCU)
- Smart home prototype — fan, light, buzzer controlled via app (NodeMCU + Blynk)
- Raspberry Pi as a mini server — host a local webpage
- Final project: Complete IoT system of your choice

---

### No background needed — seriously

If you can use a smartphone, you can learn IoT. We start from absolute basics:
- What is a circuit? What is a resistor?
- How to read a sensor datasheet (we'll teach you)
- How to write simple code in Arduino IDE and Python

Teaching is in **Hindi + English**. Small batch of 25 students. Morning, afternoon, and evening batches available.

---

### Career & opportunity after IoT

- IoT Technician / Developer (₹15,000–₹30,000/month starting)
- Embedded Systems Intern
- Smart Agriculture / Smart City project roles
- Freelance IoT prototype builder (₹5,000–₹25,000 per project)
- Higher studies: B.Tech / M.Tech in Embedded Systems, Electronics
- Startup: build and sell IoT products (smart irrigation, security systems)

India's IoT market is growing fast — Varanasi Smart City project, PM Kisan drone programme, Digital India — \
and trained IoT professionals are in short supply in eastern UP.
"""

PY_DESCRIPTION = """\
**Python Full Stack with Gen AI** — the most complete developer course at TechPath. In 8 months, you go \
from writing your first `print("Hello")` to deploying a full web application with a Python backend, \
React frontend, database, REST API, and AI-powered features — all built by you.

---

### Why Python Full Stack in 2026?

Python is the #1 language on every ranking — TIOBE, GitHub, Stack Overflow. Companies don't just want \
"Python coders" anymore. They want developers who can build the **entire application** — frontend, backend, \
database, API, deployment. That's a Full Stack Developer. Add Gen AI skills on top, and you become the \
person every startup and IT company in India is trying to hire.

---

### What you'll learn across 8 months

**Phase 1 — Python Core (Months 1–2)**
From zero to confident Python programmer. Variables, loops, functions, OOP, file handling, error handling, \
modules, and your first 5+ mini projects.

**Phase 2 — Frontend (Month 3)**
HTML5, CSS3, JavaScript, responsive design, and React basics. You'll build interactive UIs that look professional on any device.

**Phase 3 — Backend with Django (Months 4–5)**
Django framework, URL routing, templates, models, forms, authentication, admin panel, and REST APIs using \
Django REST Framework. This is where you become a real backend developer.

**Phase 4 — Database & Deployment (Month 6)**
PostgreSQL, database design, ORM queries, hosting on Render/Railway, domain setup, and going live with your project.

**Phase 5 — Gen AI Integration (Month 7)**
ChatGPT API, GitHub Copilot, Claude for code review, AI-powered features inside your app (chatbot, \
auto-summariser, smart search), prompt engineering for developers.

**Phase 6 — Capstone & Career (Month 8)**
Build a complete production app from scratch. Resume, GitHub portfolio, LinkedIn optimisation, mock interviews, and placement support.

---

### What you'll build (real projects, not tutorials)

- A personal portfolio website (HTML, CSS, JS)
- A to-do app with React frontend
- A blog platform with Django + PostgreSQL
- A REST API consumed by a React frontend
- An AI-powered chatbot integrated into your web app
- A capstone project: full stack app of your choice — deployed live with a real URL

All projects go on your **GitHub** — your portfolio that employers actually check.

---

### Career outcomes

- Python Developer (₹20,000–₹45,000/month starting)
- Full Stack Developer (₹25,000–₹60,000/month)
- Django Backend Developer
- React Frontend Developer
- API Developer
- AI-integrated App Developer (premium, emerging role)
- Freelance Web Developer (₹10,000–₹50,000 per project)

---

### Who is this for?

- Class 12 pass students (any stream) wanting a high-paying tech career
- BCA / BSc / B.Tech students who want practical skills beyond college syllabus
- Graduates from Mughalsarai, Chandauli, Varanasi, Ghazipur, and Bihar border areas
- Working professionals wanting a career switch into software development
- Anyone who tried learning coding on YouTube but couldn't finish or build anything real

---

### Why TechPath for this course?

- **8 months offline, instructor-led** — not a video dump
- **Hindi + English** — language is never a barrier
- **25 students max** — personal code reviews, not a 200-student Zoom call
- **70% hands-on** — you code every single day
- **Gen AI built in** — not a separate "AI workshop" bolted on at the end
- **Placement support** — resume, GitHub, LinkedIn, mock interviews, referrals
- **EMI available** — ₹3,750/month, lighter than a prepaid recharge plan
- **Location** — Circus Road, Mughalsarai, walking distance from DDU Junction
"""


COURSES = [
    # ── 1. Digital Marketing with Gen AI ────────────────────────────────────
    dict(
        category_slug="marketing",
        data=CourseCreate(
            title="Digital Marketing with Gen AI",
            slug="digital-marketing-with-gen-ai",
            category_id=0,  # replaced at runtime
            level="beginner",
            short_description=(
                "Master Digital Marketing with Gen AI in 4 months offline. Learn SEO, social media, "
                "paid ads, content creation, and AI tools like ChatGPT, Gemini, and Canva AI. "
                "Beginner-friendly, project-led training in Mughalsarai."
            ),
            description=DM_DESCRIPTION,
            price=12000,
            original_price=18000,
            currency="INR",
            emi_available=True,
            emi_amount=3000,
            duration="4 months",
            duration_hours=96,
            batch_size=25,
            rating=5.0,
            review_count=8,
            enrollment_count=12,
            placement_rate=75,
            instructor_name="TechPath Instructor",
            instructor_title="Senior Digital Marketing Strategist",
            instructor_bio=(
                "Experienced in running paid campaigns, SEO projects, and AI-powered content workflows "
                "for Indian SMEs and startups. Trained 100+ students across Mughalsarai, Chandauli, and Varanasi."
            ),
            status="published",
            featured=True,
            is_active=True,
            certification_name="Digital Marketing with Gen AI Certificate",
            certification_authority="TechPath",
            meta_title="Digital Marketing with Gen AI Course – 4 Months Offline | TechPath Mughalsarai",
            meta_description=(
                "Join our 4-month offline Digital Marketing course with Gen AI tools at TechPath Mughalsarai. "
                "Learn SEO, ads, social media + ChatGPT. EMI available. Enrol now."
            ),
            learning_outcomes=[
                "Plan and execute a complete digital marketing strategy from scratch",
                "Rank websites on Google using on-page and off-page SEO",
                "Run profitable Meta (Facebook + Instagram) and Google Ads campaigns",
                "Use ChatGPT, Gemini, and Claude for ad copy, blogs, and email sequences",
                "Create scroll-stopping creatives using Canva AI and Midjourney",
                "Build and grow social media accounts on Instagram, YouTube, and LinkedIn",
                "Set up Google Analytics 4 and read campaign performance data",
                "Write SEO blogs that get traffic from Google and AI search (ChatGPT, Perplexity)",
                "Build an email marketing funnel with automation",
                "Launch a freelance career or land a digital marketing job",
            ],
            prerequisites=[
                "Basic computer use (browser, files, typing)",
                "A smartphone with Instagram and YouTube installed",
                "Email account (we'll help you set one up if needed)",
                "No prior marketing or coding experience required",
                "Laptop for practice (optional for in-class)",
            ],
            curriculum=[
                CurriculumModule(
                    title="Digital Marketing Foundations",
                    duration="2 weeks",
                    topics=["What is digital marketing", "Customer journey", "Marketing funnel",
                            "Buyer persona", "Channels overview", "Goal setting"],
                ),
                CurriculumModule(
                    title="Website & SEO",
                    duration="3 weeks",
                    topics=["Domain & hosting", "WordPress basics", "Keyword research",
                            "On-page SEO", "Off-page SEO", "Technical SEO", "Local SEO",
                            "Google Search Console"],
                ),
                CurriculumModule(
                    title="Content Marketing & AI Writing",
                    duration="2 weeks",
                    topics=["Content strategy", "Blog writing", "ChatGPT prompts", "Gemini",
                            "Claude", "AI editing", "AEO (AI search)", "GEO"],
                ),
                CurriculumModule(
                    title="Social Media Marketing",
                    duration="3 weeks",
                    topics=["Instagram", "YouTube", "LinkedIn", "Reels strategy", "Hashtags",
                            "Posting schedule", "Community management", "Influencer basics"],
                ),
                CurriculumModule(
                    title="Paid Ads — Meta & Google",
                    duration="3 weeks",
                    topics=["Meta Ads Manager", "Audience targeting", "Pixel setup", "Google Ads",
                            "Search ads", "Display ads", "YouTube ads", "Budget & bidding"],
                ),
                CurriculumModule(
                    title="Gen AI Tools & Automation",
                    duration="2 weeks",
                    topics=["ChatGPT", "Gemini", "Claude", "Canva AI", "Midjourney",
                            "AI video", "Prompt engineering", "Workflow automation"],
                ),
                CurriculumModule(
                    title="Email Marketing & Analytics",
                    duration="1 week",
                    topics=["Mailchimp", "Email sequences", "Lead magnets",
                            "Google Analytics 4", "Conversion tracking", "Reporting"],
                ),
                CurriculumModule(
                    title="Freelancing, Portfolio & Capstone",
                    duration="2 weeks",
                    topics=["Upwork", "Fiverr", "LinkedIn profile", "Resume",
                            "Live client project", "Case study", "Mock interviews"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Do I need a marketing or coding background to join this course?",
                    answer=(
                        "No. This course is designed for absolute beginners. If you can use a smartphone "
                        "and browse the internet, you can learn digital marketing with us. Teaching is in "
                        "Hindi + English, so language is never a barrier."
                    ),
                ),
                FAQItem(
                    question="What makes this different from a regular digital marketing course?",
                    answer=(
                        "We integrate Generative AI tools like ChatGPT, Gemini, Claude, Canva AI, and "
                        "Midjourney into every module. You'll learn how to do in 1 hour what regular "
                        "marketers do in 8 — which is the exact skill employers in 2026 are paying premium for."
                    ),
                ),
                FAQItem(
                    question="Will I be able to get a job after completing this course?",
                    answer=(
                        "Yes. We provide placement support including resume building, LinkedIn optimisation, "
                        "mock interviews, and freelance project guidance. Starting roles range from ₹15,000 "
                        "to ₹35,000/month for full-time jobs in Varanasi, Lucknow, Noida, and remote roles. "
                        "Many students also start freelancing during the course itself."
                    ),
                ),
                FAQItem(
                    question="Course ki fees kitni hai aur EMI available hai kya?",
                    answer=(
                        "Course fees ₹12,000 hai (₹18,000 se discount ke saath). EMI bhi available hai — "
                        "sirf ₹3,000 per month. Free demo class le sakte ho — call karo +91 8299708052 "
                        "par ya WhatsApp karo."
                    ),
                ),
                FAQItem(
                    question="What tools and software will I learn?",
                    answer=(
                        "WordPress, Google Search Console, Google Analytics 4, Meta Ads Manager, Google Ads, "
                        "Mailchimp, Canva AI, ChatGPT, Gemini, Claude, Midjourney, and more. All tools have "
                        "free or affordable plans we'll guide you through."
                    ),
                ),
                FAQItem(
                    question="How is this course delivered — online or offline?",
                    answer=(
                        "This is an offline, in-person course at our Mughalsarai centre on Circus Road. "
                        "Morning, afternoon, and evening batches available. Weekend doubt-clearing sessions "
                        "are free for enrolled students."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="Live SEO Blog Site",
                    description=(
                        "Build a WordPress blog from scratch, publish 10 SEO-optimised articles, and get "
                        "them ranked on Google using real keyword research."
                    ),
                ),
                ProjectItem(
                    title="Meta Ads Campaign with Real Budget",
                    description=(
                        "Plan, launch, and optimise a real Facebook and Instagram ad campaign with a small "
                        "live budget (₹500–₹1,000) and track ROI."
                    ),
                ),
                ProjectItem(
                    title="AI Content Workflow",
                    description=(
                        "Build a complete content production system using ChatGPT, Canva AI, and Midjourney "
                        "— produce a week's worth of social media content in 2 hours."
                    ),
                ),
                ProjectItem(
                    title="Freelance Client Capstone",
                    description=(
                        "Take on a real local business (shop, clinic, coaching centre) in Mughalsarai or "
                        "Chandauli and deliver a full digital marketing audit + 30-day execution plan as your portfolio piece."
                    ),
                ),
            ],
            skill_ids=[],  # filled at runtime
        ),
        skill_slugs=["seo", "social-media", "google-ads", "meta-ads", "chatgpt",
                     "gen-ai", "content-marketing", "canva-ai", "analytics"],
    ),

    # ── 2. IoT Essentials ───────────────────────────────────────────────────
    dict(
        category_slug="iot-hardware",
        data=CourseCreate(
            title="IoT Essentials (Internet of Things)",
            slug="iot-essentials",
            category_id=0,
            level="beginner",
            short_description=(
                "Learn IoT from scratch in 4 months with hands-on projects using Arduino, NodeMCU, and "
                "Raspberry Pi. Build real smart devices — no prior coding or electronics experience needed. "
                "Offline classes in Mughalsarai."
            ),
            description=IOT_DESCRIPTION,
            price=10000,
            original_price=15000,
            currency="INR",
            emi_available=True,
            emi_amount=2500,
            duration="4 months",
            duration_hours=96,
            batch_size=25,
            rating=5.0,
            review_count=6,
            enrollment_count=10,
            placement_rate=65,
            instructor_name="TechPath Instructor",
            instructor_title="IoT & Embedded Systems Trainer",
            instructor_bio=(
                "Experienced in teaching Arduino, NodeMCU, and Raspberry Pi to beginners across Mughalsarai, "
                "Chandauli, and Varanasi. Built 50+ working IoT prototypes including smart irrigation, "
                "home automation, and environment monitoring systems."
            ),
            status="published",
            featured=False,
            is_active=True,
            certification_name="IoT Essentials Certificate",
            certification_authority="TechPath",
            meta_title="IoT Essentials Course – Arduino, NodeMCU, Raspberry Pi | TechPath",
            meta_description=(
                "Learn IoT in 4 months at TechPath Mughalsarai. Hands-on Arduino, NodeMCU, Raspberry Pi "
                "projects. Beginner-friendly, Hindi + English. EMI available. Enrol now."
            ),
            learning_outcomes=[
                "Understand basic electronics — resistors, LEDs, breadboard wiring, multimeter use",
                "Write and upload simple programs using Arduino IDE",
                "Connect and read data from sensors (temperature, humidity, ultrasonic, IR, LDR)",
                "Build WiFi-connected IoT devices using NodeMCU (ESP8266)",
                "Send live sensor data to ThingSpeak cloud and visualise it on dashboards",
                "Control devices remotely using the Blynk mobile app",
                "Set up Raspberry Pi, install Raspbian OS, and run Python scripts on it",
                "Use Raspberry Pi as a mini web server to host a local dashboard",
                "Design and build a complete IoT prototype from idea to working demo",
                "Present and document a project for portfolio or college submission",
            ],
            prerequisites=[
                "Basic computer use (browser, file management)",
                "No prior coding or electronics experience required",
                "Class 10 pass (recommended, not mandatory)",
                "Curiosity about how devices and gadgets work",
                "Laptop for home practice (optional — lab available in centre)",
            ],
            curriculum=[
                CurriculumModule(
                    title="Electronics & Circuit Basics",
                    duration="2 weeks",
                    topics=["What is IoT", "Current Voltage Resistance", "Breadboard", "LED circuits",
                            "Resistors", "Multimeter", "Series Parallel circuits", "Safety rules"],
                ),
                CurriculumModule(
                    title="Arduino — Getting Started",
                    duration="2 weeks",
                    topics=["Arduino Uno board", "Arduino IDE setup", "Digital pins", "Blink LED",
                            "digitalRead digitalWrite", "Push button", "Buzzer", "Variables basics"],
                ),
                CurriculumModule(
                    title="Arduino — Sensors & Displays",
                    duration="2 weeks",
                    topics=["Analog pins", "analogRead", "LDR light sensor", "Temperature sensor (DHT11)",
                            "Ultrasonic sensor (HC-SR04)", "LCD display (16x2 I2C)", "Servo motor basics"],
                ),
                CurriculumModule(
                    title="Arduino — Mini Projects",
                    duration="2 weeks",
                    topics=["Traffic light controller", "Intruder alarm (PIR + buzzer)",
                            "Temperature monitor with LCD", "Automatic street light (LDR)",
                            "Line follower concept", "Serial monitor debugging"],
                ),
                CurriculumModule(
                    title="NodeMCU (ESP8266) — WiFi & Cloud",
                    duration="3 weeks",
                    topics=["NodeMCU board intro", "WiFi connect", "ESP8266WiFi library",
                            "HTTP requests", "ThingSpeak cloud", "API keys",
                            "Live sensor dashboard", "Data logging"],
                ),
                CurriculumModule(
                    title="NodeMCU — App Control with Blynk",
                    duration="2 weeks",
                    topics=["Blynk app setup", "Virtual pins", "Control LED from phone",
                            "Control fan relay from phone", "Sensor data on Blynk dashboard",
                            "Notifications", "Automation rules"],
                ),
                CurriculumModule(
                    title="Raspberry Pi — Mini Computer",
                    duration="2 weeks",
                    topics=["Raspberry Pi board", "Raspbian OS install", "Terminal basics",
                            "Python on Pi", "GPIO pins", "LED blink with Python",
                            "Pi as web server (Flask basics)", "VNC remote access"],
                ),
                CurriculumModule(
                    title="Final Project & Portfolio",
                    duration="2 weeks",
                    topics=["Project idea selection", "Circuit design", "Code writing",
                            "Testing debugging", "Project documentation", "Presentation",
                            "Video demo", "GitHub upload", "Portfolio building"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Kya mujhe electronics ya coding aani chahiye pehle se?",
                    answer=(
                        "Bilkul nahi. Hum zero se shuru karte hain — LED kya hai, resistor kya karta hai, "
                        "code kaise likhte hain — sab sikhayenge. Bas curiosity chahiye. Class Hindi + English "
                        "mein hoti hai. Call karein +91 8299708052 free demo ke liye."
                    ),
                ),
                FAQItem(
                    question="Will I get components to practice at home or only in the lab?",
                    answer=(
                        "You'll work with real components in our lab during every class. We also guide you on "
                        "buying an affordable starter kit (₹800–₹1,500) for home practice. All lab access "
                        "during class hours is included in your fees."
                    ),
                ),
                FAQItem(
                    question="What is the difference between Arduino, NodeMCU, and Raspberry Pi?",
                    answer=(
                        "Arduino is a simple microcontroller — great for learning sensors and basic circuits. "
                        "NodeMCU adds WiFi so your projects can connect to the internet and be controlled from "
                        "your phone. Raspberry Pi is a full mini-computer that runs Linux and Python. We teach "
                        "all three so you understand which one to pick for any real project."
                    ),
                ),
                FAQItem(
                    question="IoT course ki fees kitni hai aur EMI milegi?",
                    answer=(
                        "Course fees ₹10,000 hai (original ₹15,000 se discounted). EMI available hai — "
                        "₹2,500 per month × 4 months. Free demo class le sakte ho — WhatsApp karo +91 8299708052 par."
                    ),
                ),
                FAQItem(
                    question="Can this course help me in B.Tech or engineering college projects?",
                    answer=(
                        "Absolutely. Many of our students use their IoT project as their semester project or "
                        "final year submission. You'll build a working prototype with documentation and a video "
                        "demo — ready to present in any college. Students from Varanasi, Chandauli, and "
                        "Ghazipur engineering colleges have used our training for exactly this."
                    ),
                ),
                FAQItem(
                    question="Is IoT useful for getting a job, or is it just a hobby course?",
                    answer=(
                        "IoT is one of the fastest-growing tech sectors in India. Smart City projects, "
                        "agriculture automation, industrial monitoring — all need trained IoT people. Starting "
                        "roles pay ₹15,000–₹30,000/month. Even if you don't take a full-time job, you can "
                        "freelance building IoT prototypes for local businesses and farms in eastern UP."
                    ),
                ),
                FAQItem(
                    question="What will I have in my portfolio after completing this course?",
                    answer=(
                        "You'll have 6–8 working projects documented with photos, circuit diagrams, code on "
                        "GitHub, and video demos. Your final capstone project will be a complete IoT system "
                        "you design yourself — this is what you show in interviews, college submissions, or "
                        "to freelance clients."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="Smart Traffic Light Controller",
                    description=(
                        "Build a working traffic light system using Arduino, LEDs, and timed sequences. "
                        "Add a pedestrian button that interrupts the cycle — exactly how real traffic signals work."
                    ),
                ),
                ProjectItem(
                    title="Temperature & Humidity Monitor with LCD",
                    description=(
                        "Connect a DHT11 sensor to Arduino and display live temperature and humidity readings "
                        "on a 16×2 LCD screen. Add a buzzer alert when temperature crosses a threshold."
                    ),
                ),
                ProjectItem(
                    title="WiFi-Controlled Smart Home (NodeMCU + Blynk)",
                    description=(
                        "Build a mini smart home setup — control an LED (light), DC fan, and buzzer (alarm) "
                        "from your smartphone using NodeMCU and Blynk app. Works over WiFi from anywhere in the house."
                    ),
                ),
                ProjectItem(
                    title="Cloud Sensor Dashboard (NodeMCU + ThingSpeak)",
                    description=(
                        "Send live temperature, humidity, and light sensor data from NodeMCU to ThingSpeak cloud. "
                        "Visualise it as real-time charts accessible from any browser — your first IoT cloud project."
                    ),
                ),
                ProjectItem(
                    title="Raspberry Pi Local Web Server",
                    description=(
                        "Set up Raspberry Pi, install Flask (Python), and host a simple web page on your local "
                        "network that shows live sensor data. Access the dashboard from your phone's browser."
                    ),
                ),
                ProjectItem(
                    title="Capstone — Your Own IoT System",
                    description=(
                        "Choose your own idea — smart irrigation, room security alarm, air quality monitor, "
                        "smart attendance, or anything you want. Design the circuit, write the code, build the "
                        "prototype, document it, and present it with a video demo. This becomes your portfolio centerpiece."
                    ),
                ),
            ],
            skill_ids=[],
        ),
        skill_slugs=["arduino", "nodemcu", "raspberry-pi", "iot", "sensors",
                     "blynk", "thingspeak", "embedded-c", "python", "electronics"],
    ),

    # ── 3. Python Full Stack with Gen AI ────────────────────────────────────
    dict(
        category_slug="programming",
        data=CourseCreate(
            title="Python Full Stack with Gen AI",
            slug="python-full-stack-with-gen-ai",
            category_id=0,
            level="beginner",
            short_description=(
                "Master Python Full Stack Development with Gen AI in 8 months. Learn Python, Django, React, "
                "PostgreSQL, REST APIs, Git, and AI tools like ChatGPT, GitHub Copilot, and Claude. "
                "Build 10+ real projects. Offline classes in Mughalsarai."
            ),
            description=PY_DESCRIPTION,
            price=30000,
            original_price=45000,
            currency="INR",
            emi_available=True,
            emi_amount=3750,
            duration="8 months",
            duration_hours=192,
            batch_size=25,
            rating=5.0,
            review_count=8,
            enrollment_count=12,
            placement_rate=80,
            instructor_name="TechPath Instructor",
            instructor_title="Senior Full Stack Python Developer",
            instructor_bio=(
                "Experienced in building and deploying production web applications using Python, Django, React, "
                "and PostgreSQL. Trained 150+ students across Mughalsarai, Chandauli, and Varanasi in full stack "
                "development with a project-first teaching approach."
            ),
            status="published",
            featured=True,
            is_active=True,
            certification_name="Python Full Stack Developer with Gen AI Certificate",
            certification_authority="TechPath",
            meta_title="Python Full Stack with Gen AI – 8 Months Offline | TechPath Mughalsarai",
            meta_description=(
                "Join our 8-month Python Full Stack course with Gen AI at TechPath Mughalsarai. "
                "Django, React, PostgreSQL, ChatGPT API. Projects + placement. EMI available."
            ),
            learning_outcomes=[
                "Write clean, efficient Python code using functions, OOP, modules, and error handling",
                "Build responsive, interactive frontends using HTML5, CSS3, JavaScript, and React",
                "Develop complete backend applications using Django framework",
                "Design and query relational databases using PostgreSQL and Django ORM",
                "Build and consume RESTful APIs using Django REST Framework",
                "Use Git and GitHub for version control and collaborative development",
                "Integrate ChatGPT API and AI features into web applications",
                "Use GitHub Copilot and Claude to accelerate coding and debugging",
                "Deploy full stack applications to cloud platforms (Render / Railway)",
                "Build a production-ready capstone project with a live URL",
                "Prepare a job-ready portfolio with GitHub, resume, and LinkedIn profile",
            ],
            prerequisites=[
                "Basic computer use (browser, file management, typing)",
                "No prior programming experience required — we start from zero",
                "Class 12 pass (any stream — Science, Commerce, Arts all welcome)",
                "Laptop for practice (recommended — lab also available in centre)",
                "Willingness to practice 1–2 hours daily outside class",
            ],
            curriculum=[
                CurriculumModule(
                    title="Python Fundamentals",
                    duration="3 weeks",
                    topics=["Python setup", "VS Code", "Variables", "Data types", "Input Output",
                            "Operators", "Type casting", "String methods", "f-strings", "Comments"],
                ),
                CurriculumModule(
                    title="Control Flow & Loops",
                    duration="2 weeks",
                    topics=["if elif else", "Nested conditions", "for loop", "while loop",
                            "break continue pass", "range()", "List comprehension", "Pattern programs"],
                ),
                CurriculumModule(
                    title="Functions & Modules",
                    duration="2 weeks",
                    topics=["Defining functions", "Parameters return", "Default args", "*args **kwargs",
                            "Lambda", "map filter", "Modules import", "pip install",
                            "Standard library", "Virtual environments"],
                ),
                CurriculumModule(
                    title="Data Structures",
                    duration="2 weeks",
                    topics=["Lists", "Tuples", "Sets", "Dictionaries", "Nested structures",
                            "Sorting searching", "JSON handling", "File read write",
                            "CSV handling", "Exception handling try except"],
                ),
                CurriculumModule(
                    title="OOP in Python",
                    duration="2 weeks",
                    topics=["Classes objects", "__init__ self", "Attributes methods", "Inheritance",
                            "Polymorphism", "Encapsulation", "Magic methods", "@property",
                            "Real-world OOP project"],
                ),
                CurriculumModule(
                    title="Git & GitHub",
                    duration="1 week",
                    topics=["Git init add commit", "Branches merge", ".gitignore", "GitHub repo",
                            "Push pull", "Pull requests", "README writing",
                            "Collaboration workflow", "GitHub profile setup"],
                ),
                CurriculumModule(
                    title="HTML5 & CSS3",
                    duration="2 weeks",
                    topics=["HTML tags structure", "Forms tables", "Semantic HTML", "CSS selectors",
                            "Flexbox", "Grid", "Responsive design", "Media queries",
                            "Google Fonts", "CSS variables", "Build a portfolio page"],
                ),
                CurriculumModule(
                    title="JavaScript Essentials",
                    duration="2 weeks",
                    topics=["Variables let const", "Data types", "Functions arrow functions",
                            "DOM manipulation", "Events", "Fetch API", "Async await",
                            "LocalStorage", "ES6+ features", "JSON"],
                ),
                CurriculumModule(
                    title="React Basics",
                    duration="3 weeks",
                    topics=["Create React App", "JSX", "Components props", "useState useEffect",
                            "Conditional rendering", "Lists keys", "Forms controlled inputs",
                            "React Router", "API calls with fetch", "Build a to-do app"],
                ),
                CurriculumModule(
                    title="Django — Backend Development",
                    duration="4 weeks",
                    topics=["Django setup", "Project vs App", "URL routing", "Views", "Templates",
                            "Static files", "Models ORM", "Migrations", "Django Admin",
                            "Forms", "User authentication login signup", "CSRF", "Sessions"],
                ),
                CurriculumModule(
                    title="Django REST Framework & PostgreSQL",
                    duration="3 weeks",
                    topics=["REST concepts", "Serializers", "APIView", "ViewSets routers",
                            "Token authentication", "CORS", "PostgreSQL setup",
                            "Database design", "Relationships ForeignKey",
                            "Queries filters", "Connecting React frontend to Django API"],
                ),
                CurriculumModule(
                    title="Deployment & DevOps Basics",
                    duration="1 week",
                    topics=["Environment variables", "DEBUG False", "Static files for production",
                            "Gunicorn", "Render deployment", "Railway deployment",
                            "Custom domain", "HTTPS", "Basic CI/CD concept"],
                ),
                CurriculumModule(
                    title="Gen AI for Developers",
                    duration="3 weeks",
                    topics=["ChatGPT API (OpenAI)", "API keys", "Prompt engineering",
                            "Building a chatbot endpoint", "AI-powered search feature",
                            "Auto-summariser in Django", "GitHub Copilot setup",
                            "Claude for code review", "AI debugging workflow",
                            "Prompt templates for developers"],
                ),
                CurriculumModule(
                    title="Capstone Project & Career Prep",
                    duration="4 weeks",
                    topics=["Project idea finalisation", "Database schema design",
                            "Backend API build", "Frontend React build", "AI feature integration",
                            "Testing", "Deployment to live URL", "Documentation",
                            "Resume building", "LinkedIn optimisation", "GitHub portfolio",
                            "Mock interviews", "Freelancing guide"],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Kya mujhe coding aani chahiye pehle se?",
                    answer=(
                        'Bilkul nahi. Hum `print("Hello")` se shuru karte hain. 8 months mein aap poora '
                        "web application bana lenge — frontend, backend, database, API, sab. Hindi + English "
                        "mein padhate hain. Free demo class ke liye call karein +91 8299708052."
                    ),
                ),
                FAQItem(
                    question="Why Python Full Stack and not MERN or Java Full Stack?",
                    answer=(
                        "Python is the easiest language to learn as a beginner, and Django is the fastest "
                        "framework to go from idea to working app. Python also powers AI/ML — so when you add "
                        "ChatGPT API features to your app, you're using the same language, not switching to "
                        "something new. MERN is great too, but for a beginner in Mughalsarai starting from zero, "
                        "Python Full Stack gives you the smoothest path to your first job."
                    ),
                ),
                FAQItem(
                    question="What is the Gen AI part? Is it just a ChatGPT tutorial?",
                    answer=(
                        "No. You'll actually build AI features inside your web app — a chatbot that answers "
                        "user questions, an auto-summariser that condenses long text, a smart search that "
                        "understands natural language. You'll use the OpenAI API (ChatGPT), GitHub Copilot for "
                        "faster coding, and Claude for code reviews. These are real developer skills, not just "
                        "'how to use ChatGPT.'"
                    ),
                ),
                FAQItem(
                    question="Course ki fees kitni hai? EMI milegi?",
                    answer=(
                        "Course fees ₹30,000 hai (original ₹45,000 se discounted). EMI available hai — sirf "
                        "₹3,750 per month × 8 months. Yeh Mughalsarai ka sabse complete full stack course hai. "
                        "WhatsApp karo +91 8299708052 par details ke liye."
                    ),
                ),
                FAQItem(
                    question="What kind of job can I get after this course?",
                    answer=(
                        "Python Full Stack Developers start at ₹20,000–₹45,000/month in cities like Varanasi, "
                        "Lucknow, Noida, Pune, and Bangalore. Remote jobs are also very common — many of our "
                        "students work from Mughalsarai for companies in Delhi and Bangalore. You can also "
                        "freelance — building websites and web apps pays ₹10,000–₹50,000 per project."
                    ),
                ),
                FAQItem(
                    question="Arts / Commerce stream se hoon — kya main kar sakta/sakti hoon?",
                    answer=(
                        "100%. Programming mein stream se koi farak nahi padta. Hum zero se padhate hain. "
                        "Hamari class mein BA, BCom, BSc — sab stream ke students hain. Aapko sirf interest "
                        "chahiye aur daily 1–2 ghante practice karne ki tayyari. Baaki hum sambhal lenge."
                    ),
                ),
                FAQItem(
                    question="Will I have real projects to show in interviews?",
                    answer=(
                        "Yes — you'll build 10+ projects throughout the course, all hosted on your GitHub with "
                        "live deployed URLs. Your capstone project will be a complete full stack app with AI "
                        "features that you designed, built, and deployed yourself. This portfolio is more "
                        "valuable than any certificate in a developer interview."
                    ),
                ),
                FAQItem(
                    question="How is this different from your 3-month Python course?",
                    answer=(
                        "The 3-month Python course covers only Python programming — scripting, automation, "
                        "data handling. This 8-month course covers Python + Django backend + React frontend + "
                        "PostgreSQL database + REST APIs + Git + Gen AI + deployment + capstone. It's the "
                        "difference between knowing a language and knowing how to build complete products. "
                        "If your goal is a developer job, this is the course."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="CLI Task Manager",
                    description=(
                        "Build a command-line to-do app in pure Python using functions, file handling, and "
                        "JSON storage. Add, delete, mark complete, and filter tasks — your first real program."
                    ),
                ),
                ProjectItem(
                    title="Personal Portfolio Website",
                    description=(
                        "Design and code a responsive portfolio website using HTML5, CSS3, and JavaScript. "
                        "Sections: hero, about, skills, projects, contact form. Deployed live on GitHub Pages."
                    ),
                ),
                ProjectItem(
                    title="React To-Do App",
                    description=(
                        "Build an interactive to-do application using React with useState, props, conditional "
                        "rendering, and localStorage. Add, edit, delete, and filter tasks with a clean UI."
                    ),
                ),
                ProjectItem(
                    title="Django Blog Platform",
                    description=(
                        "Build a multi-user blog platform with Django — user registration, login, "
                        "create/edit/delete posts, comments, categories, search, and Django admin panel. "
                        "Uses PostgreSQL."
                    ),
                ),
                ProjectItem(
                    title="REST API + React Frontend",
                    description=(
                        "Build a Django REST Framework API for a notes/bookmarks app and connect it to a "
                        "React frontend. Full CRUD operations, token authentication, and CORS setup."
                    ),
                ),
                ProjectItem(
                    title="AI-Powered Feature Module",
                    description=(
                        "Integrate OpenAI (ChatGPT) API into a Django app — build one of: a chatbot that "
                        "answers questions about your site, an auto-summariser for blog posts, or a smart "
                        "search feature that understands natural language queries."
                    ),
                ),
                ProjectItem(
                    title="Capstone — Full Stack App (Your Choice)",
                    description=(
                        "Design, build, and deploy a complete full stack web application from scratch. Choose "
                        "your own idea — job board, e-commerce store, event booking, student portal, or anything "
                        "you want. Must include: React frontend, Django backend, PostgreSQL database, REST API, "
                        "at least one AI-powered feature, user authentication, and deployment to a live URL. "
                        "This is your flagship portfolio piece."
                    ),
                ),
            ],
            skill_ids=[],
        ),
        skill_slugs=["python", "django", "react", "javascript", "html-css", "postgresql",
                     "rest-api", "git", "github", "chatgpt-api", "github-copilot",
                     "gen-ai", "full-stack"],
    ),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    async with AsyncSessionLocal() as db:
        print("\n--- Categories ---")
        cat_mkt  = await get_or_create_category(db, "Marketing",      "marketing",     display_order=1)
        cat_iot  = await get_or_create_category(db, "IoT & Hardware",  "iot-hardware",  display_order=3)
        cat_prog = await get_or_create_category(db, "Programming",    "programming",   display_order=2)
        await db.commit()

        cat_map = {
            "marketing":    cat_mkt,
            "iot-hardware": cat_iot,
            "programming":  cat_prog,
        }

        print("\n--- Skills ---")
        skill_map: dict = {}
        for name, slug in ALL_SKILLS:
            existing_skill = await skill_crud.get_by_slug(db, slug=slug)
            skill = await skill_crud.get_or_create(db, name=name, slug=slug)
            skill_map[slug] = skill
            action = "skip" if existing_skill else "+"
            print(f"  [{action}] {name}")
        await db.commit()
        # Refresh IDs after commit
        for slug, skill in skill_map.items():
            await db.refresh(skill)

        print("\n--- Courses ---")
        for entry in COURSES:
            course_obj: CourseCreate = entry["data"]
            slug = course_obj.slug

            existing = await course_crud.get_by_slug(db, slug)
            if existing:
                print(f"  [skip] already exists: {course_obj.title}")
                continue

            # Wire category and skill IDs
            course_obj.category_id = cat_map[entry["category_slug"]].id
            course_obj.skill_ids = [skill_map[s].id for s in entry["skill_slugs"]]

            await course_crud.create(db, obj_in=course_obj)
            print(f"  [+] created: {course_obj.title}")

        print("\nDone.\n")


if __name__ == "__main__":
    asyncio.run(main())
