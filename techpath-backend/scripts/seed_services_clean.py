#!/usr/bin/env python3
"""Seed services with SEO data via API"""
import requests
import json
import sys

API_BASE = "http://localhost:8000"
EMAIL = "admin@techpath.biz"
PASSWORD = "TechPath2025!"

print("=" * 50)
print("TechPath Services Seeding Script")
print("=" * 50)

# Login
print("\n[1/4] Logging in...")
try:
    response = requests.post(
        f"{API_BASE}/api/v1/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("      Login successful")
except Exception as e:
    print(f"      ERROR: {e}")
    sys.exit(1)

# Delete existing services
print("\n[2/4] Deleting existing services...")
try:
    response = requests.get(f"{API_BASE}/api/v1/services/?limit=100", headers=headers)
    existing = response.json()
    for svc in existing:
        requests.delete(f"{API_BASE}/api/v1/services/{svc['id']}", headers=headers)
        print(f"      Deleted: {svc['title']}")
    print(f"      Total deleted: {len(existing)}")
except Exception as e:
    print(f"      Note: {e}")

# Services data
services = [
    {
        "title": "AI Machine Learning Solutions",
        "slug": "ai-machine-learning",
        "description": "<h2>Transform Your Business with AI</h2><p>Harness artificial intelligence and machine learning to drive innovation, automate processes, and unlock new insights from your data.</p><h3>Our AI Services Include:</h3><ul><li><strong>Custom ML Model Development:</strong> Build tailored models for classification, prediction, and recommendation systems</li><li><strong>Natural Language Processing (NLP):</strong> Text analysis, sentiment analysis, chatbots, and language understanding</li><li><strong>Computer Vision:</strong> Image recognition, object detection, facial recognition, and visual search</li><li><strong>GenAI Integration:</strong> Deploy ChatGPT, Claude, and other LLMs into your applications</li><li><strong>AI Strategy Consulting:</strong> Roadmap development, use case identification, and ROI analysis</li></ul>",
        "short_description": "Custom AI and ML solutions to automate processes, predict outcomes, and drive intelligent decision-making across your organization.",
        "icon": "brain",
        "features": ["Custom ML models", "NLP and GenAI", "Computer vision", "Predictive analytics"],
        "cta_text": "Schedule Free Consultation",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 1,
        "is_active": True,
        "meta_title": "AI Machine Learning Services - Custom ML Solutions",
        "meta_description": "Build custom AI solutions with our expert ML team. NLP, computer vision, GenAI integration for your business.",
        "og_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630&fit=crop",
        "canonical_url": "https://techpath.com/services/ai-machine-learning",
        "faqs": [
            {"question": "What AI technologies do you specialize in?", "answer": "We specialize in machine learning (supervised/unsupervised), deep learning (CNNs, RNNs, transformers), natural language processing, computer vision, and generative AI (ChatGPT, Claude, Stable Diffusion integration)."},
            {"question": "Do I need a data science team to work with you?", "answer": "No. We handle the entire AI development lifecycle. However, having a technical point of contact helps with domain knowledge and deployment coordination."},
            {"question": "How much data do I need for an AI project?", "answer": "It depends on the use case. Some projects work with hundreds of samples (transfer learning), while others need thousands. We'll assess your data during the consultation and recommend the best approach."},
            {"question": "Can you integrate AI into our existing systems?", "answer": "Yes. We build APIs and microservices that integrate seamlessly with your current tech stack (REST, GraphQL, webhooks). We support cloud and on-premise deployments."},
            {"question": "What's the ROI timeline for AI projects?", "answer": "Most clients see measurable improvements within 3-6 months. We focus on high-impact use cases first (e.g., automating repetitive tasks, improving accuracy) to deliver quick wins while building toward larger goals."},
        ]
    },
    {
        "title": "Cloud Infrastructure & DevOps",
        "slug": "cloud-infrastructure",
        "description": "<h2>Scalable Cloud Solutions</h2><p>Build, migrate, and optimize your cloud infrastructure with our expert team. We specialize in AWS, Azure, and Google Cloud Platform.</p><h3>Cloud Services:</h3><ul><li><strong>Cloud Migration:</strong> Seamless migration from on-premise to cloud with zero downtime</li><li><strong>Infrastructure as Code (IaC):</strong> Terraform, CloudFormation, and Pulumi automation</li><li><strong>Kubernetes Orchestration:</strong> Docker, EKS, AKS, GKE deployment and management</li><li><strong>CI/CD Pipeline Setup:</strong> Jenkins, GitLab CI, GitHub Actions, and ArgoCD</li><li><strong>Cloud Cost Optimization:</strong> Reduce cloud spend by 30-50%% through rightsizing</li></ul>",
        "short_description": "Expert cloud migration, infrastructure automation, and DevOps services for AWS, Azure, and GCP. Scale with confidence.",
        "icon": "cloud",
        "features": ["AWS, Azure, GCP", "Kubernetes & Docker", "CI/CD automation", "Cost optimization"],
        "cta_text": "Get Cloud Assessment",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 2,
        "is_active": True,
        "meta_title": "Cloud Infrastructure Services - AWS, Azure, GCP Migration",
        "meta_description": "Expert cloud migration and DevOps services. Kubernetes, CI/CD, infrastructure automation for enterprise.",
        "og_image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=630&fit=crop",
        "canonical_url": "https://techpath.com/services/cloud-infrastructure",
        "faqs": [
            {"question": "Which cloud platform is best for my business?", "answer": "It depends on your needs. AWS offers the most services, Azure integrates well with Microsoft tools, and GCP excels at data/AI workloads. We'll assess your requirements and recommend the best fit."},
            {"question": "How long does a cloud migration take?", "answer": "Simple migrations (lift-and-shift) take 4-8 weeks. Complex re-architecture projects take 3-6 months. We create a phased migration plan to minimize downtime and risk."},
            {"question": "Will you train our team on cloud technologies?", "answer": "Yes. We provide comprehensive training and documentation so your team can manage the infrastructure independently. We also offer ongoing support packages if needed."},
            {"question": "How do you ensure zero downtime during migration?", "answer": "We use blue-green deployments, canary releases, and load balancer strategies to gradually shift traffic. Critical systems run in parallel until we verify stability."},
            {"question": "Can you reduce our current cloud costs?", "answer": "Yes. Most clients save 30-50% through rightsizing instances, using reserved capacity, implementing auto-scaling, and optimizing storage. We audit your current setup and identify cost-saving opportunities."},
        ]
    },
    {
        "title": "Custom Web Development",
        "slug": "web-development",
        "description": "<h2>Modern Web Applications</h2><p>Build fast, scalable, and beautiful web applications with cutting-edge technologies.</p><h3>Our Expertise:</h3><ul><li><strong>Full-Stack Development:</strong> React, Next.js, Vue, Angular frontends with Node.js, Python, Go backends</li><li><strong>E-commerce Platforms:</strong> Shopify, WooCommerce, custom solutions with payment integration</li><li><strong>Progressive Web Apps (PWAs):</strong> Offline-first, mobile-responsive applications</li><li><strong>API Development:</strong> RESTful and GraphQL APIs with documentation</li><li><strong>Performance Optimization:</strong> 90+ Lighthouse scores, SEO optimization</li></ul>",
        "short_description": "High-performance web applications with modern frameworks. Full-stack development from MVP to enterprise-scale solutions.",
        "icon": "code",
        "features": ["React, Next.js, Astro", "Full-stack development", "E-commerce solutions", "API development"],
        "cta_text": "Discuss Your Project",
        "cta_url": "/contact",
        "featured": True,
        "display_order": 3,
        "is_active": True,
        "meta_title": "Custom Web Development - React, Next.js, Full-Stack Services",
        "meta_description": "Build modern web applications with React, Next.js, and Astro. Full-stack development and API services.",
        "og_image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&h=630&fit=crop",
        "canonical_url": "https://techpath.com/services/web-development",
        "faqs": [
            {"question": "What's the difference between a website and a web application?", "answer": "A website is mostly informational (blog, portfolio). A web application has interactive features (user accounts, dashboards, real-time updates). We build both, depending on your needs."},
            {"question": "Do you offer ongoing maintenance after launch?", "answer": "Yes. We offer monthly maintenance packages covering security updates, bug fixes, performance optimization, and feature enhancements. You can also choose pay-as-you-go support."},
            {"question": "Can you redesign our existing website without starting from scratch?", "answer": "Absolutely. We can refresh the UI/UX, improve performance, add new features, or migrate to a modern tech stack while preserving your content and SEO rankings."},
            {"question": "How do you ensure our website is secure?", "answer": "We follow OWASP security guidelines: input validation, parameterized queries, HTTPS, secure authentication, regular dependency updates, and security testing before launch."},
            {"question": "Will our website be mobile-friendly?", "answer": "Yes. All our websites are responsive and mobile-first. We test on multiple devices and screen sizes to ensure a seamless experience. We also optimize for Core Web Vitals and SEO."},
        ]
    },
    {
        "title": "Data Analytics & Business Intelligence",
        "slug": "data-analytics",
        "description": "<h2>Data-Driven Decision Making</h2><p>Transform raw data into actionable insights with our advanced analytics and BI solutions.</p><h3>Analytics Services:</h3><ul><li><strong>Data Warehouse Setup:</strong> Snowflake, BigQuery, Redshift architecture</li><li><strong>ETL Pipelines:</strong> Airflow, dbt, Fivetran for automated data processing</li><li><strong>BI Dashboard Development:</strong> Tableau, Power BI, Looker, Metabase dashboards</li><li><strong>Predictive Analytics:</strong> Forecasting, trend analysis, and anomaly detection</li><li><strong>Real-time Analytics:</strong> Kafka, Spark streaming for instant insights</li></ul>",
        "short_description": "Turn data into insights with BI dashboards, data warehouses, ETL pipelines, and predictive analytics. Make smarter decisions faster.",
        "icon": "chart",
        "features": ["BI dashboards", "Data warehousing", "ETL pipelines", "Predictive analytics"],
        "cta_text": "Start Data Journey",
        "cta_url": "/contact",
        "featured": False,
        "display_order": 4,
        "is_active": True,
        "meta_title": "Data Analytics & BI Services - Dashboards, Warehouses, ETL",
        "meta_description": "Data analytics and business intelligence services. Build data warehouses, BI dashboards, and ETL pipelines.",
        "og_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop",
        "canonical_url": "https://techpath.com/services/data-analytics",
        "faqs": [
            {"question": "What's the difference between data analytics and business intelligence?", "answer": "Business intelligence focuses on reporting historical data (dashboards, KPIs). Data analytics includes predictive modeling and advanced analysis to uncover insights and forecast trends."},
            {"question": "Do we need a data warehouse?", "answer": "If you're analyzing data from multiple sources (databases, APIs, spreadsheets), a data warehouse centralizes everything for faster queries and better consistency. We'll assess if you need one."},
            {"question": "Can you work with our existing data tools?", "answer": "Yes. We integrate with popular tools like Tableau, Power BI, Looker, Excel, and custom databases. We can also recommend better alternatives if your current setup is limiting."},
            {"question": "How do you handle data privacy and compliance?", "answer": "We follow GDPR, CCPA, and industry-specific regulations (HIPAA for healthcare, PCI-DSS for payments). We implement data anonymization, access controls, and audit logs as needed."},
            {"question": "What if our data is messy or incomplete?", "answer": "Most data is messy! We include data cleaning, validation, and enrichment as part of the project. We build automated pipelines to maintain data quality over time."},
        ]
    }
]

# Create services
print(f"\n[3/4] Creating {len(services)} services...")
created_count = 0
for service in services:
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/services/",
            headers=headers,
            json=service
        )
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"      Created: {result['title']}")
            created_count += 1
        else:
            print(f"      ERROR: {service['title']} - {response.text}")
    except Exception as e:
        print(f"      ERROR: {service['title']} - {e}")

print(f"      Total created: {created_count}")

# Verify
print("\n[4/4] Verification...")
try:
    response = requests.get(f"{API_BASE}/api/v1/services/?limit=100", headers=headers)
    services_list = response.json()
    print(f"      Total services in database: {len(services_list)}\n")
    
    for svc in services_list:
        meta_title = svc.get('meta_title') or 'Not set'
        meta_desc = svc.get('meta_description') or 'Not set'
        faq_count = len(svc.get('faqs', []))
        print(f"      [{svc['id']}] {svc['title']}")
        print(f"          Slug: {svc['slug']}")
        print(f"          SEO Title: {meta_title}")
        print(f"          SEO Desc: {meta_desc[:60]}...")
        print(f"          FAQs: {faq_count} questions")
        print()
except Exception as e:
    print(f"      ERROR during verification: {e}")

print("=" * 50)
print("Seeding Complete!")
print("=" * 50)
