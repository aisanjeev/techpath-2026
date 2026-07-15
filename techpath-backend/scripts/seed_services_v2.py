#!/usr/bin/env python3
"""Seed all 7 Techpath services (April 2026 content) — direct DB insert."""
import asyncio
import json
import os
import sys
from pathlib import Path

# Allow running from repo root or scripts/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load .env.local before importing app config
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env.local")

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.models.service import Service

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./data/techpath.db",
)

SERVICES = [
    {
        "title": "AI Machine Learning Solutions",
        "slug": "ai-machine-learning",
        "short_description": "Custom AI and ML solutions that automate processes, predict outcomes, and drive intelligent decision-making across your organisation. From NLP and computer vision to GenAI integration and AI strategy consulting — Techpath Research and Development delivers production-ready AI systems built for Indian enterprises, startups, and global clients.",
        "description": """<h2>Transform Your Business with Custom AI &amp; Machine Learning</h2>

<p>India's AI market is projected to grow from <strong>USD 1,597 million in 2025 to USD 13,245 million by 2034</strong> at a CAGR of 26.5% — and the organisations that deploy AI today will own that advantage tomorrow. At <strong>Techpath Research and Development Pvt Ltd</strong>, we build AI and ML systems that move from proof-of-concept to production — not just demos.</p>

<p>Whether you need a recommendation engine, a document intelligence system, a computer vision pipeline, or a GenAI-powered product feature, our team designs, trains, and deploys models tailored to your data, your domain, and your business goals.</p>

<h3>Our AI &amp; ML Services Include</h3>
<ul>
  <li><strong>Custom ML Model Development:</strong> Classification, regression, clustering, forecasting, and recommendation systems trained on your proprietary data</li>
  <li><strong>Natural Language Processing (NLP):</strong> Text classification, sentiment analysis, named entity recognition, document parsing, and chatbot development</li>
  <li><strong>Computer Vision:</strong> Image recognition, object detection, facial recognition, quality inspection, and visual search systems</li>
  <li><strong>GenAI Integration:</strong> Deploy ChatGPT, Claude, and Gemini APIs into your products with custom prompt engineering, RAG pipelines, and fine-tuning</li>
  <li><strong>AI Strategy Consulting:</strong> Use-case identification, ROI analysis, data readiness assessment, and implementation roadmaps</li>
  <li><strong>MLOps &amp; Model Maintenance:</strong> Continuous monitoring, retraining pipelines, drift detection, and performance dashboards</li>
</ul>

<h3>Why Choose Techpath for AI Development?</h3>
<p>We combine domain expertise with engineering rigour. Our models are built to run in real environments — not just notebooks. Every engagement begins with your data and ends with a deployed, monitored, documented system your team can own and operate.</p>

<blockquote>
  <p>"AI-related activities could add $450–500 billion to India's GDP, requiring a workforce and technology transformation that touches every professional domain." — McKinsey, 2024</p>
</blockquote>

<p>From Mughalsarai and Chandauli to clients across India and beyond, Techpath delivers AI solutions that are practical, explainable, and built for scale. <strong>Schedule a free consultation today — call or WhatsApp +91 8299708052.</strong></p>""",
        "icon": "Brain",
        "features": [
            "Custom ML models",
            "NLP and GenAI",
            "Computer vision",
            "Predictive analytics",
            "MLOps & monitoring",
        ],
        "cta_text": "Schedule Free Consultation",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 1,
        "is_active": True,
        "meta_title": "AI Machine Learning Solutions | Custom ML Development — Techpath",
        "meta_description": "Custom AI & ML solutions — NLP, computer vision, GenAI integration & MLOps. Techpath builds production-ready AI systems for Indian enterprises. Get a free consultation.",
        "canonical_url": "https://techpathrd.com/services/ai-machine-learning",
        "layout_size": "large",
        "accent_color": "purple",
        "graphic_variant": "orbital",
        "badge_label": "FEATURED",
        "tags": ["GenAI", "Computer Vision", "NLP"],
        "stat_label": "projects",
        "stat_value": "42+",
        "faqs": [
            {
                "question": "What types of AI solutions does Techpath build?",
                "answer": "Techpath Research and Development builds custom ML models, NLP systems, computer vision pipelines, GenAI integrations, and AI strategy roadmaps. We work with classification, forecasting, recommendation, and language models — trained on your data and deployed into your production environment. Every solution is documented and handed over with full ownership. Call +91 8299708052 to discuss your use case.",
            },
            {
                "question": "How long does it take to build a custom ML model?",
                "answer": "Timeline depends on data readiness and complexity. A focused ML model with clean data typically takes 4-8 weeks from kickoff to deployment. GenAI integrations using existing APIs (ChatGPT, Claude, Gemini) can be delivered in 2-3 weeks. We provide a detailed project plan with milestones before any work begins. Contact Techpath at +91 8299708052 for a scoping call.",
            },
            {
                "question": "Do you offer AI consulting without full development?",
                "answer": "Yes. Techpath offers standalone AI strategy consulting — use-case identification, data readiness assessment, ROI analysis, and implementation roadmaps — without committing to a full development project. This is ideal for organisations exploring AI adoption or needing an independent technical audit. WhatsApp us at +91 8299708052 to schedule a consulting session.",
            },
            {
                "question": "Can you integrate AI into our existing software?",
                "answer": "Absolutely. We specialise in GenAI integration — deploying ChatGPT, Claude, Gemini, and other LLMs into existing products via API. We also build RAG (Retrieval-Augmented Generation) pipelines, custom prompt layers, and fine-tuned models that plug into your current stack. Call Techpath Research and Development at +91 8299708052 to discuss integration requirements.",
            },
            {
                "question": "What industries do you serve with AI solutions?",
                "answer": "Techpath serves clients across fintech, healthcare, e-commerce, manufacturing, education, and logistics. AI use cases differ by sector — from fraud detection in banking to visual quality inspection in manufacturing — and we tailor each engagement to the specific domain, data type, and regulatory environment. Call +91 8299708052 or visit techpathrd.com to explore industry-specific solutions.",
            },
        ],
    },
    {
        "title": "Cloud Infrastructure & DevOps",
        "slug": "cloud-infrastructure",
        "short_description": "Scalable cloud infrastructure design, migration, and DevOps automation for businesses that need reliable, cost-optimised, and secure cloud environments. Techpath Research and Development delivers AWS, Azure, and GCP solutions — CI/CD pipelines, Kubernetes orchestration, Terraform IaC, and 24/7 infrastructure management — for startups and enterprises across India.",
        "description": """<h2>Cloud Infrastructure &amp; DevOps Engineering — Built for Scale, Designed for Speed</h2>

<p>NASSCOM projects <strong>14 million cloud jobs in India through 2026</strong> — a number driven directly by enterprise cloud migration and AI workload infrastructure demand. The organisations winning today are the ones whose infrastructure can scale in minutes, deploy in hours, and recover in seconds. Techpath Research and Development builds that infrastructure for you.</p>

<p>From startups running their first cloud workload to enterprises migrating legacy systems at scale, we design, deploy, and manage cloud environments that are secure, cost-efficient, and engineered for the demands of modern software delivery.</p>

<h3>Our Cloud &amp; DevOps Services</h3>
<ul>
  <li><strong>Cloud Architecture Design:</strong> Multi-cloud and hybrid cloud architecture on AWS, Azure, and GCP — designed for availability, security, and cost optimisation</li>
  <li><strong>Cloud Migration:</strong> Lift-and-shift, re-platforming, and re-architecting of existing workloads to cloud-native environments</li>
  <li><strong>CI/CD Pipeline Engineering:</strong> Automated build, test, and deployment pipelines using GitHub Actions, Jenkins, GitLab CI, and Azure DevOps</li>
  <li><strong>Container Orchestration:</strong> Docker containerisation and Kubernetes (EKS, AKS, GKE) cluster management for microservices architectures</li>
  <li><strong>Infrastructure as Code (IaC):</strong> Terraform and Ansible scripts for reproducible, version-controlled infrastructure provisioning</li>
  <li><strong>Monitoring &amp; Observability:</strong> Prometheus, Grafana, CloudWatch, and ELK stack setup for full-stack visibility and alerting</li>
  <li><strong>FinOps &amp; Cost Optimisation:</strong> Right-sizing, reserved instance planning, and cloud spend analysis to reduce your bill by 20-40%</li>
</ul>

<h3>The DevOps Advantage</h3>
<p>Companies that invest in DevOps automation reduce deployment cycles by <strong>40-50%</strong> and cut infrastructure costs significantly versus manual provisioning. Our engineers bring AWS, Azure, CKA, and Terraform certifications — so your infrastructure is built to industry standards, not improvised.</p>

<p>Serving clients from Chandauli and Varanasi to pan-India and global remote engagements, Techpath delivers cloud environments that give your development team the speed and your business the reliability it needs. <strong>Call +91 8299708052 to start your cloud journey.</strong></p>""",
        "icon": "Cloud",
        "features": [
            "AWS, Azure & GCP architecture",
            "CI/CD pipeline automation",
            "Kubernetes & Docker",
            "Terraform IaC",
            "FinOps & cost optimisation",
        ],
        "cta_text": "Get Free Cloud Assessment",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 2,
        "is_active": True,
        "meta_title": "Cloud Infrastructure & DevOps Services | AWS Azure GCP — Techpath",
        "meta_description": "Cloud architecture, migration & DevOps automation on AWS, Azure & GCP. CI/CD, Kubernetes, Terraform & FinOps. Get a free cloud assessment from Techpath today.",
        "canonical_url": "https://techpathrd.com/services/cloud-infrastructure",
        "layout_size": "small",
        "accent_color": "cyan",
        "graphic_variant": "code-window",
        "faqs": [
            {
                "question": "Which cloud platforms does Techpath support?",
                "answer": "Techpath Research and Development works across all three major cloud platforms — AWS, Microsoft Azure, and Google Cloud Platform (GCP). We also support multi-cloud and hybrid cloud architectures. Our engineers hold AWS, Azure, and GCP certifications, ensuring your infrastructure meets industry standards. Call +91 8299708052 or WhatsApp to discuss which platform fits your workload.",
            },
            {
                "question": "Can you migrate our existing on-premise infrastructure to the cloud?",
                "answer": "Yes. Techpath handles cloud migrations from discovery and planning through to cutover and post-migration optimisation. We assess your current workloads and choose the right migration strategy — lift-and-shift for speed, re-platforming for efficiency, or re-architecting for full cloud-native benefits. Migrations are planned to minimise downtime. Call +91 8299708052 for a migration scoping session.",
            },
            {
                "question": "How much can we save on cloud costs after optimisation?",
                "answer": "Most clients see a 20-40% reduction in cloud spend after right-sizing, reserved instance planning, and architecture optimisation. Techpath's FinOps service includes a full audit of your current cloud bill, identification of waste, and a cost optimisation roadmap with projected savings. This is delivered before any implementation work begins. Contact us at +91 8299708052.",
            },
            {
                "question": "Do you offer ongoing infrastructure management after the build?",
                "answer": "Yes. Techpath offers retainer-based DevOps support — covering infrastructure monitoring, incident response, security patching, cost reviews, and pipeline maintenance. This gives you a dedicated DevOps partner without the cost of a full-time hire. Monitoring is set up with Prometheus and Grafana so you have full visibility. WhatsApp +91 8299708052 to discuss support plans.",
            },
            {
                "question": "What is Infrastructure as Code and why does it matter?",
                "answer": "Infrastructure as Code (IaC) means your entire cloud environment — servers, networks, databases, security groups — is defined in version-controlled code (Terraform or Ansible). This makes your infrastructure reproducible, auditable, and disaster-recoverable. You can spin up identical environments in minutes and track every change in Git. Techpath implements IaC as standard on all cloud projects. Call +91 8299708052.",
            },
        ],
    },
    {
        "title": "Custom Web Development",
        "slug": "web-development",
        "short_description": "Full-stack web development services for businesses that need more than a template. Techpath Research and Development builds high-performance, scalable web applications using React, Node.js, Python, and PostgreSQL — designed for conversion, engineered for speed, and built to grow with your business.",
        "description": """<h2>Custom Web Development — Performance-First, Business-Ready</h2>

<p>Your website is not a brochure. It is the first conversation your business has with every potential customer, partner, and investor. At <strong>Techpath Research and Development Pvt Ltd</strong>, we build web applications that are engineered to perform — fast load times, clean architecture, secure backends, and conversion-focused interfaces.</p>

<p>From MVPs and SaaS platforms to enterprise portals and e-commerce systems, we deliver full-stack web applications that scale from 100 users to 1 million without architectural rewrites.</p>

<h3>Our Web Development Stack &amp; Services</h3>
<ul>
  <li><strong>Frontend Development:</strong> React, Next.js, and Tailwind CSS — pixel-perfect UIs with sub-2-second load times, Core Web Vitals optimised</li>
  <li><strong>Backend Engineering:</strong> Node.js, Python (Django / FastAPI), and REST or GraphQL APIs — structured, documented, and version-controlled</li>
  <li><strong>Database Design:</strong> PostgreSQL, MongoDB, and Redis — normalised schemas, indexed queries, and backup strategies built in from day one</li>
  <li><strong>SaaS &amp; Product Development:</strong> Multi-tenant architecture, subscription billing (Razorpay / Stripe), role-based access, and admin dashboards</li>
  <li><strong>E-Commerce Development:</strong> Custom storefronts, payment gateway integration, inventory management, and order processing systems</li>
  <li><strong>CMS Integration:</strong> Headless CMS setups (Strapi, Sanity, Contentful) so your team can update content without touching code</li>
  <li><strong>Web Performance &amp; SEO:</strong> Core Web Vitals, server-side rendering, image optimisation, schema markup, and structured data implementation</li>
</ul>

<h3>How We Work</h3>
<p>We start with a scoping workshop to understand your users, your business logic, and your technical constraints. Every project is delivered with full documentation, a Git repository your team owns, and a deployment pipeline you can manage. No lock-in, no black boxes.</p>

<p>Techpath serves businesses in Chandauli, Varanasi, eastern UP, and clients across India via our live-remote delivery model. <strong>Call +91 8299708052 to discuss your project — we respond same day.</strong></p>""",
        "icon": "Code",
        "features": [
            "React & Next.js frontend",
            "Node.js & Python backend",
            "PostgreSQL & MongoDB",
            "SaaS product development",
            "Core Web Vitals optimised",
        ],
        "cta_text": "Discuss Your Project",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 3,
        "is_active": True,
        "meta_title": "Custom Web Development Services | React Node.js Python — Techpath",
        "meta_description": "Full-stack web development with React, Node.js & Python. SaaS platforms, e-commerce & enterprise portals. Fast, scalable, SEO-ready. Talk to Techpath today.",
        "canonical_url": "https://techpathrd.com/services/web-development",
        "layout_size": "small",
        "accent_color": "green",
        "graphic_variant": "code-window",
        "faqs": [
            {
                "question": "What types of web applications does Techpath build?",
                "answer": "Techpath Research and Development builds SaaS platforms, e-commerce systems, enterprise portals, admin dashboards, MVPs, and CMS-driven websites. We work across the full stack — React and Next.js on the frontend, Node.js or Python (Django/FastAPI) on the backend, and PostgreSQL or MongoDB for data storage. Every project is scoped and priced clearly before work begins. Call +91 8299708052.",
            },
            {
                "question": "How long does a custom web application take to build?",
                "answer": "A focused MVP typically takes 6-10 weeks. A full-featured SaaS platform or enterprise portal takes 12-20 weeks depending on complexity. We use agile delivery — you see working software at the end of every two-week sprint, not just at the end. This means early feedback and no surprises at launch. Call Techpath at +91 8299708052 to get a timeline estimate for your specific project.",
            },
            {
                "question": "Will I own the code and the hosting?",
                "answer": "Completely. Techpath delivers all source code in a Git repository under your account. Hosting is set up on infrastructure you own and control — AWS, Azure, GCP, or any VPS provider. We do not lock you into proprietary platforms or monthly hosting fees. You have full ownership of everything we build. Contact +91 8299708052 for more details on our delivery process.",
            },
            {
                "question": "Do you build mobile-responsive and SEO-optimised websites?",
                "answer": "Yes, by default. Every web application Techpath builds is fully responsive across all screen sizes and engineered for Core Web Vitals — the Google ranking signals for page speed, interactivity, and visual stability. We also implement structured data (schema markup) and server-side rendering where appropriate for maximum search engine visibility. Call +91 8299708052.",
            },
            {
                "question": "Can you take over and improve an existing web application?",
                "answer": "Yes. Techpath handles code audits, refactoring, performance optimisation, and feature additions on existing codebases. We begin with a technical audit to understand the current architecture, identify bottlenecks and security gaps, and provide a clear improvement roadmap. This service is available for React, Node.js, Django, and WordPress-based applications. WhatsApp +91 8299708052 to get started.",
            },
        ],
    },
    {
        "title": "Data Analytics & Business Intelligence",
        "slug": "data-analytics",
        "short_description": "Turn your raw data into decisions. Techpath Research and Development delivers end-to-end data analytics and business intelligence solutions — from data pipeline engineering and warehousing to interactive dashboards and predictive analytics — so your leadership team has the right numbers at the right time.",
        "description": """<h2>Data Analytics &amp; Business Intelligence — Stop Guessing, Start Knowing</h2>

<p>Most businesses are sitting on data they cannot read. Reports are delayed, dashboards are outdated, and decisions are made on gut feel. <strong>Techpath Research and Development</strong> fixes that. We build data infrastructure and analytics systems that give your team accurate, real-time visibility into what is driving your business — and what is holding it back.</p>

<p>From startups tracking their first KPIs to enterprises consolidating data from a dozen source systems, we design analytics solutions that are fast to query, easy to understand, and built to evolve with your business.</p>

<h3>Our Data &amp; BI Services</h3>
<ul>
  <li><strong>Data Pipeline Engineering:</strong> ETL and ELT pipelines using Apache Airflow, dbt, and Python — structured to move data from source systems to your warehouse reliably and on schedule</li>
  <li><strong>Data Warehousing:</strong> Cloud data warehouse setup and optimisation on BigQuery, Redshift, and Snowflake — designed for fast analytical queries at any scale</li>
  <li><strong>Dashboard &amp; Reporting:</strong> Interactive dashboards in Power BI, Tableau, Looker, and Metabase — built for the questions your leadership team actually asks</li>
  <li><strong>Predictive Analytics:</strong> Statistical modelling and ML-based forecasting for revenue, churn, demand, inventory, and customer behaviour</li>
  <li><strong>Data Quality &amp; Governance:</strong> Data validation pipelines, lineage tracking, access controls, and documentation so your team trusts the numbers</li>
  <li><strong>Customer &amp; Product Analytics:</strong> Funnel analysis, cohort analysis, A/B testing frameworks, and event tracking setup (Mixpanel, Amplitude, GA4)</li>
</ul>

<h3>The Business Case for Data Investment</h3>
<p>Organisations with mature data practices make faster decisions, identify revenue leakage earlier, and outperform peers on growth metrics. Our analytics engagements typically pay back within the first quarter through cost savings, conversion improvements, or operational efficiencies uncovered in the data.</p>

<p>Techpath serves clients across India — from eastern UP and Varanasi to pan-India remote engagements. <strong>Call +91 8299708052 to book a free data readiness assessment.</strong></p>""",
        "icon": "BarChart",
        "features": [
            "Data pipelines & ETL",
            "Power BI & Tableau dashboards",
            "BigQuery & Snowflake warehousing",
            "Predictive analytics",
            "Customer & product analytics",
        ],
        "cta_text": "Book Free Data Assessment",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 4,
        "is_active": True,
        "meta_title": "Data Analytics & Business Intelligence Services | BI Dashboards",
        "meta_description": "Data pipelines, BI dashboards, predictive analytics & data warehousing. Power BI, Tableau, BigQuery & dbt. Free data assessment from Techpath — call today.",
        "canonical_url": "https://techpathrd.com/services/data-analytics",
        "layout_size": "wide",
        "accent_color": "amber",
        "graphic_variant": "bar-chart",
        "badge_label": "TRENDING",
        "stat_label": "avg. revenue lift",
        "stat_value": "35%",
        "faqs": [
            {
                "question": "What data sources can Techpath connect to our analytics system?",
                "answer": "Techpath connects virtually any source — CRMs (Salesforce, HubSpot), ERPs (SAP, Tally), databases (MySQL, PostgreSQL, MongoDB), SaaS tools (Shopify, Stripe, Google Ads), spreadsheets, and custom APIs. Our pipeline engineering team handles extraction, transformation, and loading into your data warehouse so all your data is in one queryable place. Call +91 8299708052 to discuss your sources.",
            },
            {
                "question": "How long does it take to set up a BI dashboard?",
                "answer": "A focused dashboard covering 5-8 KPIs from a clean data source takes 2-3 weeks. A full analytics stack — pipelines, warehouse, and multiple department dashboards — typically takes 6-10 weeks. We deliver in phases so your team has working dashboards early in the project. Every dashboard is documented and comes with training so your team can use it independently. Call +91 8299708052.",
            },
            {
                "question": "Which BI tools do you work with?",
                "answer": "Techpath builds dashboards in Power BI, Tableau, Looker, Metabase, and Grafana — we recommend the right tool based on your team's technical level, data volume, and budget. For organisations wanting open-source and zero licensing cost, Metabase is a strong choice. For enterprise-grade analysis, Power BI and Tableau deliver the most flexibility. Contact +91 8299708052 to discuss options.",
            },
            {
                "question": "Can you help us with real-time analytics?",
                "answer": "Yes. Techpath builds real-time analytics using streaming data pipelines (Apache Kafka, AWS Kinesis) connected to live dashboards. This is valuable for e-commerce order monitoring, live event tracking, fraud detection, and operational alerting. Real-time setups require slightly more infrastructure investment but deliver immediate business value. WhatsApp us at +91 8299708052 for a scoping discussion.",
            },
            {
                "question": "Do you offer predictive analytics and forecasting?",
                "answer": "Yes. Techpath's predictive analytics service includes revenue forecasting, demand planning, customer churn prediction, and product recommendation modelling. We use Python-based statistical and ML models (scikit-learn, Prophet, XGBoost) and deliver outputs either as API endpoints your product can call or as dashboard visualisations your team can read. Call +91 8299708052 to explore use cases.",
            },
        ],
    },
    {
        "title": "DevOps & Automation",
        "slug": "devops-automation",
        "short_description": "End-to-end DevOps engineering and process automation for software teams that need to ship faster, break less, and scale confidently. Techpath Research and Development implements CI/CD pipelines, container orchestration, automated testing, and infrastructure automation — eliminating manual bottlenecks across your entire software delivery lifecycle.",
        "description": """<h2>DevOps &amp; Automation — Ship Faster. Break Less. Scale with Confidence.</h2>

<p>In 2026, DevOps engineering is one of India's highest-paying and most in-demand IT specialisations. Senior DevOps engineers command <strong>18-35 LPA</strong>, with top architects exceeding 60 LPA — because the skill is rare and the impact is direct. At <strong>Techpath Research and Development</strong>, we bring that same expertise to your software delivery process.</p>

<p>If your team is manually deploying to production, spending hours debugging environment differences, or waiting days between code commit and release — DevOps automation is the fastest path to reclaiming that time and reducing risk.</p>

<h3>Our DevOps &amp; Automation Services</h3>
<ul>
  <li><strong>CI/CD Pipeline Implementation:</strong> Automated build, test, and deployment pipelines using GitHub Actions, Jenkins, GitLab CI, and Azure DevOps — from commit to production in minutes</li>
  <li><strong>Containerisation:</strong> Docker image creation, optimisation, and registry management for consistent, portable application environments</li>
  <li><strong>Kubernetes Orchestration:</strong> Cluster setup, deployment configuration, auto-scaling, rolling updates, and health monitoring on EKS, AKS, or GKE</li>
  <li><strong>Infrastructure Automation:</strong> Terraform and Ansible scripts that provision, configure, and manage your entire infrastructure as code</li>
  <li><strong>Automated Testing Integration:</strong> Unit, integration, and end-to-end test automation wired into your CI pipeline so bugs are caught before production</li>
  <li><strong>GitOps &amp; Release Management:</strong> GitOps workflows (ArgoCD, Flux) for declarative, auditable, rollback-safe deployments</li>
  <li><strong>AIOps &amp; Monitoring:</strong> Prometheus, Grafana, ELK stack, and AI-assisted alerting to detect and resolve incidents before users notice</li>
</ul>

<h3>Measurable Results</h3>
<p>Companies implementing proper DevOps automation reduce deployment cycle time by <strong>40-50%</strong> and significantly cut production incident rates. Every pipeline Techpath builds is designed to reduce your team's cognitive load — so engineers spend time building, not firefighting.</p>

<p>From Mughalsarai to clients across India on live remote engagements, Techpath delivers DevOps transformation that sticks. <strong>Call +91 8299708052 to audit your current pipeline and find out where you are losing time.</strong></p>""",
        "icon": "GitBranch",
        "features": [
            "CI/CD pipeline automation",
            "Docker & Kubernetes",
            "Terraform & Ansible IaC",
            "GitOps & release management",
            "AIOps monitoring & alerting",
        ],
        "cta_text": "Get Free Pipeline Audit",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 5,
        "is_active": True,
        "meta_title": "DevOps & Automation Services | CI/CD Kubernetes Terraform — Techpath",
        "meta_description": "CI/CD pipelines, Kubernetes, Docker, Terraform & AIOps. Techpath's DevOps engineering cuts deployment time by 40-50%. Free pipeline audit — call today.",
        "canonical_url": "https://techpathrd.com/services/devops-automation",
        "faqs": [
            {
                "question": "What does DevOps automation actually change for our development team?",
                "answer": "DevOps automation eliminates manual, error-prone steps in your software delivery process. Code that passes tests is deployed automatically. Environments are provisioned identically every time. Incidents trigger alerts before customers notice. The result is faster releases, fewer production bugs, and engineers who spend time on product work instead of deployment firefighting. Call Techpath at +91 8299708052 to start with a pipeline audit.",
            },
            {
                "question": "Which CI/CD tools do you use?",
                "answer": "Techpath works with GitHub Actions, Jenkins, GitLab CI/CD, Azure DevOps, and CircleCI. We recommend the right tool based on your current repository setup and team workflow. GitHub Actions is our default recommendation for most teams due to its tight Git integration and large marketplace of pre-built actions. All pipelines are documented and your team is trained to manage them. Call +91 8299708052.",
            },
            {
                "question": "Can you migrate us from manual deployments to full CI/CD without breaking our current system?",
                "answer": "Yes, and this is one of our most common engagements. Techpath implements CI/CD incrementally — we start with automated testing, then staging deployment, then production deployment — so there is never a risky big-bang cutover. We maintain your existing deployment capability throughout until the new pipeline is fully validated and your team is confident. WhatsApp +91 8299708052 to plan your migration.",
            },
            {
                "question": "Do you offer Kubernetes setup and management?",
                "answer": "Yes. Techpath designs and deploys Kubernetes clusters on AWS EKS, Azure AKS, and Google GKE. We handle cluster setup, namespace configuration, deployment manifests, ingress controllers, horizontal pod autoscaling, and persistent volume management. We also set up monitoring (Prometheus + Grafana) and alerting so you have full visibility into cluster health. Call +91 8299708052 for a scoping discussion.",
            },
            {
                "question": "What is GitOps and do we need it?",
                "answer": "GitOps is a deployment model where your Git repository is the single source of truth for your infrastructure and application state — tools like ArgoCD or Flux continuously reconcile your live environment with what is declared in Git. This gives you automatic drift detection, one-command rollbacks, and a full audit trail of every change. Techpath recommends GitOps for any team deploying to Kubernetes. Call +91 8299708052.",
            },
        ],
    },
    {
        "title": "Mobile App Development",
        "slug": "mobile-app-development",
        "short_description": "Native and cross-platform mobile applications built for iOS and Android. Techpath Research and Development delivers performance-first mobile apps using React Native and Flutter — from consumer apps and SaaS mobile clients to enterprise field tools and AI-powered mobile experiences — with full backend API integration and App Store deployment.",
        "description": """<h2>Mobile App Development — Apps That Perform, Not Just Launch</h2>

<p>India's mobile app market generated <strong>over $300 million in in-app purchase revenue in Q1 2026 alone</strong> — growing 33% year-on-year. Consumer expectations are higher than ever: apps must load in under 2 seconds, handle poor network conditions gracefully, and deliver a native-quality experience on every device. <strong>Techpath Research and Development</strong> builds apps that meet that bar.</p>

<p>Whether you need a customer-facing consumer app, a mobile extension of your SaaS product, an enterprise field tool, or an AI-powered mobile experience, we design, develop, test, and deploy mobile applications that your users will actually use.</p>

<h3>Our Mobile Development Services</h3>
<ul>
  <li><strong>React Native Development:</strong> Cross-platform apps with near-native performance — one codebase for iOS and Android, reducing cost and time-to-market by up to 40%</li>
  <li><strong>Flutter Development:</strong> Beautiful, highly customisable UIs with Flutter's widget system — ideal for apps where visual differentiation matters</li>
  <li><strong>Backend &amp; API Integration:</strong> REST and GraphQL API development, real-time data sync, push notifications, and third-party service integration (payment gateways, maps, CRMs)</li>
  <li><strong>AI-Powered Features:</strong> On-device ML with TensorFlow Lite or CoreML, GenAI chat integration, image recognition, and voice interfaces</li>
  <li><strong>App Store Deployment:</strong> Full App Store (Apple) and Play Store (Google) submission process — including store listing optimisation (ASO) for discoverability</li>
  <li><strong>Performance Optimisation:</strong> Bundle size reduction, lazy loading, offline-first architecture, and crash monitoring with Sentry or Firebase Crashlytics</li>
  <li><strong>Maintenance &amp; Updates:</strong> OTA updates, OS version compatibility, feature additions, and bug triage on a retainer basis</li>
</ul>

<h3>From Concept to App Store in 12 Weeks</h3>
<p>Our mobile development process starts with a UX design sprint — wireframes and user flows reviewed and approved before a line of code is written. Every app is built with a test suite, CI/CD for app builds, and beta testing via TestFlight and Firebase App Distribution before public launch.</p>

<p>Serving clients from Chandauli and eastern UP to global remote engagements, Techpath delivers mobile apps on schedule and on budget. <strong>Call +91 8299708052 to discuss your app idea today.</strong></p>""",
        "icon": "Smartphone",
        "features": [
            "React Native & Flutter",
            "iOS & Android",
            "AI-powered features",
            "Backend API integration",
            "App Store deployment & ASO",
        ],
        "cta_text": "Get Free App Scoping Call",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 6,
        "is_active": True,
        "meta_title": "Mobile App Development | React Native & Flutter — Techpath R&D",
        "meta_description": "iOS & Android app development with React Native & Flutter. AI features, backend APIs & App Store deployment. Talk to Techpath — free app scoping call today.",
        "canonical_url": "https://techpathrd.com/services/mobile-app-development",
        "faqs": [
            {
                "question": "Should we build a native app or a cross-platform app?",
                "answer": "For most businesses, React Native or Flutter delivers 90% of native performance at 50-60% of the cost — because one codebase serves both iOS and Android. We recommend native development (Swift/Kotlin) only when you need deep platform-specific features like AR, advanced haptics, or complex hardware integration. Techpath will assess your requirements and recommend the right approach. Call +91 8299708052.",
            },
            {
                "question": "How long does it take to build a mobile app?",
                "answer": "A focused MVP with core features typically takes 10-14 weeks from design to App Store submission. A full-featured consumer app takes 16-24 weeks. Timeline depends on feature complexity, backend requirements, and design iteration cycles. Techpath delivers in two-week sprints with working builds at each stage, so you have visibility throughout. Call +91 8299708052 for a project estimate.",
            },
            {
                "question": "Do you integrate payment gateways into mobile apps?",
                "answer": "Yes. Techpath integrates Razorpay, Stripe, PayU, and other payment gateways into mobile apps — including in-app purchases, subscription billing, UPI, and wallet payments. We handle both the frontend payment UI and the backend webhook processing so your revenue flows securely and reliably. Payment integration is tested extensively before App Store submission. Call +91 8299708052.",
            },
            {
                "question": "Can you add AI features to our existing mobile app?",
                "answer": "Absolutely. Techpath integrates AI into existing apps — adding GenAI chat interfaces, image recognition, voice commands, personalisation engines, and recommendation systems. We can work with on-device ML (TensorFlow Lite, CoreML) for privacy-sensitive use cases or cloud-based AI APIs for more complex reasoning tasks. WhatsApp us at +91 8299708052 to discuss your current app and desired features.",
            },
            {
                "question": "Do you handle App Store and Play Store submission?",
                "answer": "Yes, completely. Techpath manages the full App Store (Apple) and Play Store (Google) submission process — including provisioning profiles, code signing, store listing creation, screenshot design, keyword optimisation (ASO), and review process management. We have experience navigating both stores' review guidelines and resolving rejection issues. Call +91 8299708052 to get started.",
            },
        ],
    },
    {
        "title": "Cybersecurity & Compliance",
        "slug": "cybersecurity-compliance",
        "short_description": "End-to-end cybersecurity services for businesses that cannot afford a breach. Techpath Research and Development delivers security audits, penetration testing, cloud security hardening, compliance readiness (ISO 27001, SOC 2, DPDPA), and ongoing threat monitoring — protecting your applications, infrastructure, and data from the threats that matter most in 2026.",
        "description": """<h2>Cybersecurity &amp; Compliance — Protect What You've Built</h2>

<p>Cybersecurity professionals in India command salaries from <strong>3 LPA for freshers to 60+ LPA for senior experts</strong> — because the demand is acute and the talent is scarce. India's rapid digital transformation, the Digital Personal Data Protection Act (DPDPA), and increasing ransomware and supply-chain attacks have made security non-negotiable for every business with a digital presence. <strong>Techpath Research and Development</strong> closes that gap for you.</p>

<p>We do not just scan and report. We find real vulnerabilities, explain what they mean in business terms, and help your team fix them — then we help you build the processes and governance to stay secure as you grow.</p>

<h3>Our Cybersecurity Services</h3>
<ul>
  <li><strong>Security Audit &amp; Risk Assessment:</strong> Comprehensive review of your applications, infrastructure, and processes — identifying vulnerabilities, misconfigurations, and compliance gaps with a prioritised remediation roadmap</li>
  <li><strong>Penetration Testing (Pentesting):</strong> Authorised simulated attacks on your web applications, APIs, mobile apps, and network infrastructure — OWASP Top 10, SANS Top 25, and beyond</li>
  <li><strong>Cloud Security Hardening:</strong> AWS, Azure, and GCP security configuration review — IAM policy audit, S3/blob storage access controls, network security group review, and GuardDuty/Defender setup</li>
  <li><strong>DevSecOps Integration:</strong> Security scanning (SAST, DAST, SCA) wired into your CI/CD pipeline so vulnerabilities are caught at code commit, not at production launch</li>
  <li><strong>Compliance Readiness:</strong> ISO 27001, SOC 2 Type II, India DPDPA (Digital Personal Data Protection Act), PCI-DSS, and HIPAA gap analysis and readiness assessment</li>
  <li><strong>Incident Response:</strong> 24/7 incident response retainer — containment, forensic analysis, root cause identification, and post-incident hardening</li>
  <li><strong>Security Awareness Training:</strong> Phishing simulation, social engineering awareness, and security culture programmes for your team</li>
</ul>

<h3>Compliance Is Not Optional Anymore</h3>
<p>India's DPDPA is now in effect, with significant penalties for data breaches and non-compliance. Enterprise clients, investors, and large enterprise procurement teams are increasingly requiring ISO 27001 or SOC 2 certification before signing contracts. Techpath's compliance readiness service gives you a clear, actionable path to certification — without the confusion and overwhelm of starting from scratch.</p>

<p>Serving clients from Chandauli and Varanasi to pan-India and international engagements, Techpath delivers cybersecurity that is practical, thorough, and built around your actual risk profile. <strong>Call +91 8299708052 to schedule a free security consultation.</strong></p>""",
        "icon": "Shield",
        "features": [
            "Security audits & risk assessment",
            "Penetration testing (OWASP)",
            "Cloud security hardening",
            "ISO 27001 & DPDPA compliance",
            "DevSecOps pipeline integration",
        ],
        "cta_text": "Schedule Free Security Consultation",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 7,
        "is_active": True,
        "meta_title": "Cybersecurity & Compliance Services | Pentesting ISO 27001 — Techpath",
        "meta_description": "Security audits, penetration testing, cloud hardening & ISO 27001/DPDPA compliance. Techpath protects your business from real threats. Free security consult.",
        "canonical_url": "https://techpathrd.com/services/cybersecurity-compliance",
        "faqs": [
            {
                "question": "What is included in a security audit?",
                "answer": "Techpath's security audit covers your web applications, APIs, cloud infrastructure, and internal processes. We check for OWASP Top 10 vulnerabilities, cloud misconfigurations (open S3 buckets, weak IAM policies), insecure dependencies, network exposure, and access control gaps. You receive a prioritised report with every finding explained in plain English — risk level, business impact, and specific remediation steps. Call +91 8299708052.",
            },
            {
                "question": "How is penetration testing different from a security audit?",
                "answer": "A security audit reviews your security posture — configurations, policies, code, and processes. Penetration testing goes further: our engineers actively attempt to exploit vulnerabilities using the same techniques real attackers use. This confirms whether a vulnerability is actually exploitable and shows you exactly what a successful attack would look like. Techpath conducts pentests under a formal rules-of-engagement agreement. Call +91 8299708052.",
            },
            {
                "question": "Do you help with India's Digital Personal Data Protection Act (DPDPA) compliance?",
                "answer": "Yes. Techpath's DPDPA compliance service includes a gap analysis of your current data collection, processing, storage, and deletion practices against the Act's requirements. We identify gaps, help implement the required controls (consent management, data localisation, breach notification processes), and document your compliance posture. This is particularly critical for businesses handling personal data of Indian residents. Call +91 8299708052.",
            },
            {
                "question": "Can you integrate security into our DevOps pipeline (DevSecOps)?",
                "answer": "Yes. Techpath implements DevSecOps by adding automated security scanning at every stage of your CI/CD pipeline — static analysis (SAST) on code commits, dependency scanning (SCA) for known CVEs, dynamic testing (DAST) on deployed environments, and container image scanning before production push. This catches vulnerabilities at the lowest-cost moment to fix them. WhatsApp +91 8299708052 to discuss your current pipeline.",
            },
            {
                "question": "What compliance certifications do you help businesses achieve?",
                "answer": "Techpath supports compliance readiness for ISO 27001, SOC 2 Type I and Type II, India DPDPA, PCI-DSS (for businesses handling card payments), and HIPAA (for healthcare data). We conduct gap assessments, help implement required controls, create the necessary documentation, and prepare your team for auditor interviews. We work alongside your chosen certification body, not as a replacement for them. Call +91 8299708052.",
            },
        ],
    },
]


async def run():
    print("=" * 60)
    print("TechPath Services Seed - v2 (April 2026 content)")
    print("=" * 60)
    print(f"\nDatabase: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as db:
        # Delete existing services
        print("\n[1/2] Removing existing services...")
        result = await db.execute(select(Service))
        existing = result.scalars().all()
        for svc in existing:
            await db.delete(svc)
        await db.flush()
        print(f"      Removed {len(existing)} existing service(s)")

        # Insert new services
        print("\n[2/2] Creating 7 services...")
        success = 0
        for data in SERVICES:
            svc = Service(
                title=data["title"],
                slug=data["slug"],
                short_description=data.get("short_description"),
                description=data["description"],
                icon=data.get("icon"),
                features=json.dumps(data["features"]) if data.get("features") else None,
                faqs=json.dumps(data["faqs"]) if data.get("faqs") else None,
                cta_text=data.get("cta_text", "Learn More"),
                cta_url=data.get("cta_url"),
                featured=data.get("featured", False),
                display_order=data.get("display_order", 0),
                is_active=data.get("is_active", True),
                meta_title=data.get("meta_title"),
                meta_description=data.get("meta_description"),
                canonical_url=data.get("canonical_url"),
                no_index=False,
                layout_size=data.get("layout_size", "small"),
                badge_label=data.get("badge_label"),
                tags=json.dumps(data["tags"]) if data.get("tags") else None,
                stat_label=data.get("stat_label"),
                stat_value=data.get("stat_value"),
                accent_color=data.get("accent_color", "blue"),
                graphic_variant=data.get("graphic_variant", "none"),
            )
            db.add(svc)
            print(f"      [{data['display_order']}/7] {data['title']}")
            success += 1

        await db.commit()

    await engine.dispose()

    print(f"\n{'=' * 60}")
    print(f"Done: {success}/7 services inserted successfully")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run())
