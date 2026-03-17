#!/usr/bin/env python3
"""Seed services with SEO data via API"""
import requests
import json

API_BASE = "http://localhost:8000"
EMAIL = "admin@techpath.biz"
PASSWORD = "TechPath2025!"

# Login
print("Logging in...")
response = requests.post(
    f"{API_BASE}/api/v1/auth/login",
    json={"email": EMAIL, "password": PASSWORD}
)
token = response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
print("OK Logged in successfully\n")

# Delete existing services
print("Deleting existing services...")
try:
    response = requests.get(f"{API_BASE}/api/v1/services/?limit=100", headers=headers)
    existing = response.json()
    for svc in existing:
        requests.delete(f"{API_BASE}/api/v1/services/{svc['id']}", headers=headers)
        print(f"  Deleted: {svc['title']}")
    print(f"Deleted {len(existing)} existing services\n")
except Exception as e:
    print(f"Note: {e}\n")

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
        "canonical_url": "https://techpath.com/services/ai-machine-learning"
    },
    {
        "title": "Cloud Infrastructure & DevOps",
        "slug": "cloud-infrastructure",
        "description": "<h2>Scalable Cloud Solutions</h2><p>Build, migrate, and optimize your cloud infrastructure with our expert team. We specialize in AWS, Azure, and Google Cloud Platform.</p><h3>Cloud Services:</h3><ul><li><strong>Cloud Migration:</strong> Seamless migration from on-premise to cloud with zero downtime</li><li><strong>Infrastructure as Code (IaC):</strong> Terraform, CloudFormation, and Pulumi automation</li><li><strong>Kubernetes Orchestration:</strong> Docker, EKS, AKS, GKE deployment and management</li><li><strong>CI/CD Pipeline Setup:</strong> Jenkins, GitLab CI, GitHub Actions, and ArgoCD</li><li><strong>Cloud Cost Optimization:</strong> Reduce cloud spend by 30-50% through rightsizing</li></ul>",
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
        "canonical_url": "https://techpath.com/services/cloud-infrastructure"
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
        "canonical_url": "https://techpath.com/services/web-development"
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
        "canonical_url": "https://techpath.com/services/data-analytics"
    }
]

# Create services
print("Creating services...\n")
for service in services:
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/services/",
            headers=headers,
            json=service
        )
        result = response.json()
        print(f"[OK] Created: {result['title']}")
    except Exception as e:
        print(f"ERROR - Failed to create {service['title']}: {e}")

# Verify
print("\n=== Verification ===")
response = requests.get(f"{API_BASE}/api/v1/services/?limit=100", headers=headers)
services_list = response.json()
print(f"Total services: {len(services_list)}\n")
for svc in services_list:
    print(f"OK - {svc['title']}")
    print(f"  Slug: {svc['slug']}")
    print(f"  SEO Title: {svc.get('meta_title', 'Not set')}")
    print(f"  SEO Description: {svc.get('meta_description', 'Not set')[:50]}...")
    print()

print("DONE - Seeding complete!")
