"""
Public content API for frontend (e.g. training landing page).
No auth required. Returns built-in default when DB has no content.
"""

import json
from typing import Any, Callable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db
from app.crud.app_setting import app_setting_crud
from app.schemas.content import (
    AboutHeroContent,
    AboutPageContent,
    AboutTeamMember,
    AboutValueItem,
    ContactHeroContent,
    ContactMethodItem,
    ContactPageContent,
    CtaButton,
    CtaContent,
    FaqItem,
    HeroContent,
    HomeCaseStudiesSection,
    HomeCtaContent,
    HomeFeatureItem,
    HomeHeroContent,
    HomeLandingContent,
    HomeServiceItem,
    HomeStatItem,
    HomeTestimonialItem,
    OfferBannerContent,
    PageSeoContent,
    PainPointItem,
    PainPointsContent,
    PricingHeroContent,
    PricingPageContent,
    PricingPlanItem,
    PolicyPageContent,
    SchemaDefaults,
    ServicesHeroContent,
    ServicesLandingContent,
    StoryItem,
    StoriesContent,
    TrustBadge,
    TrainingLandingContent,
    UspItem,
    UspsContent,
)

router = APIRouter()

TRAINING_LANDING_KEY = "training_landing_content"
HOME_LANDING_KEY = "home_landing_content"
ABOUT_PAGE_KEY = "about_page_content"
SERVICES_LANDING_KEY = "services_landing_content"
CONTACT_PAGE_KEY = "contact_page_content"
PRICING_PAGE_KEY = "pricing_page_content"
PRIVACY_PAGE_KEY = "privacy_page_content"
TERMS_PAGE_KEY = "terms_page_content"
COOKIE_PAGE_KEY = "cookie_page_content"


def get_builtin_training_content() -> dict[str, Any]:
    """Return default training page content (same shape as API response)."""
    from datetime import datetime, timezone
    default_date = (datetime.now(timezone.utc).replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + "Z")
    content = TrainingLandingContent(
        seo=PageSeoContent(
            title="Online Tech Courses | Certificate Programs | TechPath Training",
            description="Learn Data Science, AI, Cloud, Web Development with live instructors. Courses from ₹7K. 94% job placement. 30-day money-back guarantee. Enroll now!",
        ),
        hero=HeroContent(
            title="Master In-Demand Tech Skills",
            subtitle="Live instructor training + Real-world projects + Job guarantee + 100% money back",
            headline_subline="Land High-Paying Jobs in 90 Days",
            badge_text="New Batch Starting Feb 2026",
            primary_cta=CtaButton(label="Start Free Trial", href="#enroll"),
            secondary_cta=CtaButton(label="View Course Catalog", href="#courses"),
            trust_badges=[
                TrustBadge(icon="⭐", value="4.9/5", label="2,000+ Reviews"),
                TrustBadge(icon="👨‍🎓", value="50,000+", label="Students Trained"),
                TrustBadge(icon="💼", value="94%", label="Job Placement"),
                TrustBadge(icon="🏆", value="Since 2019", label="Trusted Institute"),
            ],
        ),
        pain_points=PainPointsContent(
            section_title="Stuck Without a Clear Tech Career Path?",
            section_subtext="You're not alone. Thousands face these same challenges every day.",
            transition_text="Good news: There's a better way to break into tech — without breaking the bank or wasting months on theory.",
            items=[
                PainPointItem(
                    icon="📉",
                    title="Limited by Old Skills",
                    description="Your current tech stack is becoming obsolete. Companies demand modern frameworks like React, Python, and Cloud - skills you haven't mastered yet.",
                    color="text-red-400",
                    bg_color="bg-red-500/10",
                    border_color="border-red-500/30",
                ),
                PainPointItem(
                    icon="💸",
                    title="Expensive Bootcamps",
                    description="Other institutes charge ₹2-5 Lakhs for weak outcomes. 50% of graduates don't even get jobs. Why pay premium for uncertain results?",
                    color="text-orange-400",
                    bg_color="bg-orange-500/10",
                    border_color="border-orange-500/30",
                ),
                PainPointItem(
                    icon="📚",
                    title="No Real-World Experience",
                    description="Online courses feel theoretical. You watch videos but can't build anything. Without actual project portfolios, recruiters ignore your resume.",
                    color="text-yellow-400",
                    bg_color="bg-yellow-500/10",
                    border_color="border-yellow-500/30",
                ),
            ],
        ),
        usps=UspsContent(
            section_title="Why Top Companies Choose TechPath Graduates",
            section_subtext="We don't just teach — we transform careers with a proven methodology.",
            items=[
                UspItem(
                    icon="🎓",
                    title="Expert Instructors",
                    highlights=[
                        "Real engineers with 7+ years experience",
                        "Currently working in top tech companies",
                        "Teach current market-relevant skills",
                    ],
                    color="from-blue-500 to-cyan-500",
                ),
                UspItem(
                    icon="💻",
                    title="Live + Interactive",
                    highlights=[
                        "Daily doubt-clearing sessions",
                        "Real-time code reviews",
                        "Small batches (max 20 students)",
                    ],
                    color="from-purple-500 to-pink-500",
                ),
                UspItem(
                    icon="🚀",
                    title="Job-Ready Projects",
                    highlights=[
                        "Build 5-10 live projects",
                        "Add to your GitHub portfolio",
                        "Get job interviews faster",
                    ],
                    color="from-primary-500 to-secondary-500",
                ),
                UspItem(
                    icon="💰",
                    title="Transparent Pricing",
                    highlights=[
                        "No hidden charges ever",
                        "30-day money-back guarantee",
                        "Flexible EMI options available",
                    ],
                    color="from-green-500 to-emerald-500",
                ),
            ],
        ),
        faqs=[
            FaqItem(question="Do I need prior coding experience to enroll?", answer="It depends on the course. Our beginner-level courses like MERN Full Stack and Data Analytics are designed for absolute beginners. Intermediate and advanced courses may require basic programming knowledge. Each course page lists specific prerequisites."),
            FaqItem(question="What is your job guarantee policy?", answer="We offer placement assistance with a 94% success rate. While we can't legally guarantee a job, we provide resume building, mock interviews, and connect you with our 500+ hiring partners. If you don't get placed within 6 months of completion, you get a 50% refund."),
            FaqItem(question="What if I don't like the course?", answer="We offer a 30-day money-back guarantee. If you're not satisfied within the first 30 days, simply request a refund - no questions asked. We want you to 100% confident in your investment."),
            FaqItem(question="Can I access the course content after completion?", answer="Yes! You get lifetime access to all course materials, including any future updates. You can revisit lessons, download resources, and access recordings anytime."),
            FaqItem(question="What are the class timings?", answer="We offer flexible timing with both weekday (evening) and weekend batches. Live classes are recorded, so you can catch up if you miss a session. Most courses have 2-3 live sessions per week, each 2-3 hours long."),
            FaqItem(question="Is there EMI option available?", answer="Yes! We offer flexible EMI options starting from ₹2,000/month depending on the course. We've partnered with leading fintech providers to offer 0% interest EMI for select courses."),
            FaqItem(question="What projects will I build?", answer="Each course includes 5-10 hands-on projects that you'll add to your GitHub portfolio. Projects are industry-relevant and designed with input from hiring managers. You'll have real deployable applications by the end."),
            FaqItem(question="How are the live classes conducted?", answer="Classes are conducted via Zoom with small batches (max 15-25 students). You'll interact directly with instructors, participate in live coding, and get instant doubt resolution. All sessions are recorded for later viewing."),
        ],
        stories=StoriesContent(
            section_title="Real Students. Real Transformations.",
            section_subtext="Join thousands who've changed their careers with TechPath",
            items=[
                StoryItem(name="Priya Sharma", location="Mumbai", previous_role="Manual Tester", current_role="Senior Data Scientist", previous_salary="₹4.5 LPA", current_salary="₹18 LPA", course="Data Science Masterclass", duration="4 months", quote="TechPath completely transformed my career. The hands-on projects and mentorship helped me crack interviews at top companies.", rating=5, has_video=True),
                StoryItem(name="Rahul Verma", location="Bangalore", previous_role="Support Engineer", current_role="Cloud Architect", previous_salary="₹6 LPA", current_salary="₹24 LPA", course="AWS + DevOps", duration="3 months", quote="The live classes and real AWS projects gave me confidence to apply for senior roles. Best investment I've made!", rating=5, has_video=False),
                StoryItem(name="Ananya Reddy", location="Hyderabad", previous_role="Fresher (B.Tech)", current_role="ML Engineer", previous_salary="₹0", current_salary="₹12 LPA", course="AI/ML Bootcamp", duration="5 months", quote="As a fresher, I was lost. TechPath's structured curriculum and placement support helped me land my dream job.", rating=5, has_video=True),
                StoryItem(name="Vikram Singh", location="Delhi", previous_role="Backend Developer", current_role="Full Stack Lead", previous_salary="₹8 LPA", current_salary="₹22 LPA", course="MERN Full Stack", duration="3 months", quote="The project-based learning approach is incredible. I built 8 real projects that impressed every interviewer.", rating=5, has_video=False),
            ],
        ),
        offer_banner=OfferBannerContent(
            discount="₹15,000 OFF",
            savings="Save 30%",
            target_date=default_date,
            badge_text="EARLY BIRD OFFER - Limited Time Only",
            benefits=[
                "24/7 Doubt Support",
                "Job Interview Prep (3 sessions)",
                "Resume Building Help",
                "LinkedIn Profile Optimization",
                "Mock Interview Rounds (4)",
                "Lifetime Course Access",
                "30-Day Money-Back Guarantee",
                "Certificate of Completion",
            ],
        ),
        schema_defaults=SchemaDefaults(
            name="TechPath Training",
            description="Online tech courses and certification programs with live instructor training",
            rating_value="4.9",
            review_count="2000",
        ),
        cta=CtaContent(
            title="Ready to Transform Your Career?",
            description="Join 50,000+ students who've changed their lives with TechPath training.",
            primary_button=CtaButton(label="Explore Courses", href="#courses"),
            secondary_button=CtaButton(label="Talk to Counselor", href="/contact"),
        ),
    )
    return content.model_dump()


def get_builtin_home_content() -> dict[str, Any]:
    """Return default home page content."""
    content = HomeLandingContent(
        seo=PageSeoContent(
            title="AI-Powered IT Solutions",
            description="TechPath delivers enterprise-grade AI solutions, cloud infrastructure, and custom software development for modern businesses.",
        ),
        hero=HomeHeroContent(
            badge_text="Now offering GenAI Solutions",
            headline="AI-Powered IT Solutions for",
            headline_highlight="Modern Enterprises",
            subheadline="Transform your business with cutting-edge AI, cloud infrastructure, and custom software solutions. We help enterprises innovate faster and scale smarter.",
            primary_cta_label="Start Your Project",
            primary_cta_href="/contact",
            secondary_cta_label="Watch Demo",
            secondary_cta_href="/case-studies",
        ),
        stats=[
            HomeStatItem(value="150+", label="Projects Delivered"),
            HomeStatItem(value="98%", label="Client Satisfaction"),
            HomeStatItem(value="50+", label="Enterprise Clients"),
            HomeStatItem(value="24/7", label="Support Available"),
        ],
        services=[
            HomeServiceItem(title="AI & Machine Learning", description="Custom AI solutions powered by cutting-edge machine learning models.", icon="brain", href="/services/ai-consulting"),
            HomeServiceItem(title="Cloud Infrastructure", description="Scalable cloud architecture on AWS, Azure, and Google Cloud.", icon="cloud", href="/services/cloud-services"),
            HomeServiceItem(title="Web Development", description="Modern, performant web applications built with latest technologies.", icon="code", href="/services/web-development"),
            HomeServiceItem(title="Data Analytics", description="Transform your data into actionable business insights.", icon="chart", href="/services/data-analytics"),
        ],
        case_studies_section=HomeCaseStudiesSection(
            section_title="Featured Case Studies",
            section_subtitle="Real stories of digital transformation. See how we've helped businesses achieve measurable results.",
            limit=6,
            view_all_label="View All Case Studies",
            view_all_href="/case-studies",
        ),
        features=[
            HomeFeatureItem(title="Enterprise-Grade Security", description="SOC 2 compliant infrastructure with end-to-end encryption.", icon="shield"),
            HomeFeatureItem(title="Scalable Architecture", description="Built to grow with your business from startup to enterprise.", icon="scale"),
            HomeFeatureItem(title="Expert Team", description="Senior engineers with 10+ years of industry experience.", icon="users"),
            HomeFeatureItem(title="Agile Delivery", description="Rapid iteration with continuous integration and deployment.", icon="rocket"),
        ],
        testimonials=[
            HomeTestimonialItem(quote="TechPath transformed our legacy systems into a modern, AI-powered platform. The results exceeded our expectations.", author="Sarah Chen", role="CTO", company="FinanceFlow Inc.", avatar="/images/testimonials/sarah.jpg"),
            HomeTestimonialItem(quote="Their expertise in cloud migration saved us 40% on infrastructure costs while improving performance.", author="Michael Roberts", role="VP Engineering", company="RetailMax", avatar="/images/testimonials/michael.jpg"),
            HomeTestimonialItem(quote="The team delivered our AI chatbot ahead of schedule. Customer satisfaction improved by 35%.", author="Emily Watson", role="Director of Operations", company="HealthTech Solutions", avatar="/images/testimonials/emily.jpg"),
        ],
        faqs=[
            FaqItem(question="What industries do you specialize in?", answer="We work across multiple industries including healthcare, finance, retail, and technology. Our solutions are tailored to meet specific industry requirements and compliance standards."),
            FaqItem(question="How long does a typical project take?", answer="Project timelines vary based on scope and complexity. A typical MVP takes 8-12 weeks, while enterprise solutions may take 4-6 months. We provide detailed timelines during our initial consultation."),
            FaqItem(question="Do you offer ongoing support and maintenance?", answer="Yes, we offer 24/7 support packages including monitoring, updates, security patches, and performance optimization. Our team ensures your systems run smoothly post-launch."),
            FaqItem(question="What is your development methodology?", answer="We follow Agile methodology with 2-week sprints, regular demos, and continuous feedback loops. This ensures transparency and allows for quick adjustments based on your needs."),
        ],
        cta=HomeCtaContent(
            title="Ready to Transform Your Business?",
            description="Let's discuss how our AI-powered solutions can drive your digital transformation.",
            primary_label="Get Started",
            primary_href="/contact",
            secondary_label="View Case Studies",
            secondary_href="/case-studies",
        ),
    )
    return content.model_dump()


def get_builtin_about_content() -> dict[str, Any]:
    """Return default about page content."""
    content = AboutPageContent(
        seo=PageSeoContent(
            title="About Us",
            description="Learn about TechPath's mission to deliver innovative AI and IT solutions. Meet our team of experts dedicated to your success.",
        ),
        hero=AboutHeroContent(
            title="Building the Future of Technology",
            title_highlight="Future",
            subheadline="We're a team of passionate technologists dedicated to helping businesses harness the power of AI, cloud computing, and modern software development.",
        ),
        mission_title="Our Mission",
        mission_text="To democratize access to cutting-edge technology solutions, enabling businesses of all sizes to compete and thrive in the digital age. We believe that the right technology, implemented thoughtfully, can transform industries and improve lives.",
        stats=[
            HomeStatItem(value="10+", label="Years Experience"),
            HomeStatItem(value="150+", label="Projects Completed"),
            HomeStatItem(value="50+", label="Team Members"),
            HomeStatItem(value="25+", label="Countries Served"),
        ],
        values=[
            AboutValueItem(title="Innovation First", description="We embrace emerging technologies and creative solutions to solve complex problems.", icon="lightbulb"),
            AboutValueItem(title="Client Success", description="Your success is our success. We measure ourselves by the impact we create for you.", icon="trophy"),
            AboutValueItem(title="Transparency", description="Open communication and honest assessments are the foundation of our partnerships.", icon="eye"),
            AboutValueItem(title="Excellence", description="We hold ourselves to the highest standards in code quality and delivery.", icon="star"),
        ],
        team=[
            AboutTeamMember(name="Alex Thompson", role="CEO & Founder", bio="15+ years in tech leadership. Former VP Engineering at Fortune 500.", image="/images/team/alex.jpg"),
            AboutTeamMember(name="Dr. Sarah Kim", role="Chief AI Officer", bio="PhD in Machine Learning. Published researcher with 50+ papers.", image="/images/team/sarah.jpg"),
            AboutTeamMember(name="Marcus Chen", role="CTO", bio="Cloud architecture expert. AWS & Azure certified solutions architect.", image="/images/team/marcus.jpg"),
            AboutTeamMember(name="Jessica Patel", role="VP of Engineering", bio="12 years in full-stack development. Former tech lead at FAANG.", image="/images/team/jessica.jpg"),
        ],
        cta_title="Ready to Build Something Great?",
        cta_description="Let's discuss how we can help you achieve your technology goals.",
        cta_primary_label="Get in Touch",
        cta_primary_href="/contact",
        cta_secondary_label="View Our Work",
        cta_secondary_href="/case-studies",
    )
    return content.model_dump()


def get_builtin_services_content() -> dict[str, Any]:
    """Return default services landing page content."""
    content = ServicesLandingContent(
        seo=PageSeoContent(
            title="Our Services",
            description="Explore TechPath's comprehensive IT services including AI solutions, cloud infrastructure, web development, and data analytics.",
        ),
        hero=ServicesHeroContent(
            title="Our Services",
            title_highlight="Services",
            subheadline="From AI-powered solutions to cloud infrastructure, we provide end-to-end technology services that drive business growth and innovation.",
        ),
        cta_title="Need a Custom Solution?",
        cta_description="Let's discuss your unique requirements and build something amazing together.",
        cta_primary_label="Contact Us",
        cta_primary_href="/contact",
        cta_secondary_label="View Pricing",
        cta_secondary_href="/pricing",
    )
    return content.model_dump()


def get_builtin_contact_content() -> dict[str, Any]:
    """Return default contact page content."""
    content = ContactPageContent(
        seo=PageSeoContent(
            title="Contact Us",
            description="Get in touch with TechPath. We'd love to discuss your project and how we can help transform your business with AI-powered solutions.",
        ),
        hero=ContactHeroContent(
            title="Let's Talk",
            title_highlight="Talk",
            subheadline="Have a project in mind? We'd love to hear about it. Get in touch and let's create something amazing together.",
        ),
        contact_methods=[
            ContactMethodItem(title="Email", description="Send us an email anytime", value="hello@techpath.biz", href="mailto:hello@techpath.biz", icon="email"),
            ContactMethodItem(title="Phone", description="Mon-Fri from 9am to 6pm", value="+1 (555) 123-4567", href="tel:+15551234567", icon="phone"),
            ContactMethodItem(title="Office", description="Visit our headquarters", value="San Francisco, CA", href="https://maps.google.com", icon="location"),
        ],
    )
    return content.model_dump()


def get_builtin_pricing_content() -> dict[str, Any]:
    """Return default pricing page content."""
    content = PricingPageContent(
        seo=PageSeoContent(
            title="Pricing",
            description="Transparent pricing for TechPath's IT services. From startup projects to enterprise solutions, find the right plan for your needs.",
        ),
        hero=PricingHeroContent(
            title="Simple, Transparent Pricing",
            title_highlight="Pricing",
            subheadline="Choose the plan that fits your needs. All plans include our commitment to quality and your success.",
        ),
        plans=[
            PricingPlanItem(
                name="Starter",
                description="Perfect for small projects and startups",
                price="$2,500",
                period="per project",
                features=[
                    "Up to 5 pages",
                    "Basic SEO optimization",
                    "Mobile responsive design",
                    "Contact form integration",
                    "30 days support",
                    "Source code delivery",
                ],
                cta="Get Started",
                highlighted=False,
            ),
            PricingPlanItem(
                name="Professional",
                description="Ideal for growing businesses",
                price="$7,500",
                period="per project",
                features=[
                    "Up to 15 pages",
                    "Advanced SEO optimization",
                    "Custom design system",
                    "CMS integration",
                    "API development",
                    "90 days support",
                    "Performance optimization",
                    "Analytics setup",
                ],
                cta="Get Started",
                highlighted=True,
            ),
            PricingPlanItem(
                name="Enterprise",
                description="For large-scale applications",
                price="Custom",
                period="contact us",
                features=[
                    "Unlimited pages",
                    "Custom AI solutions",
                    "Dedicated team",
                    "Priority support 24/7",
                    "SLA guarantee",
                    "Security audits",
                    "Load testing",
                    "Training & documentation",
                ],
                cta="Contact Sales",
                highlighted=False,
            ),
        ],
        faq_section_title="Frequently Asked Questions",
        faqs=[
            FaqItem(
                question="What payment methods do you accept?",
                answer="We accept all major credit cards, bank transfers, and can accommodate purchase orders for enterprise clients. Payment terms are typically 50% upfront and 50% on project completion.",
            ),
            FaqItem(
                question="Can I upgrade my plan later?",
                answer="Yes, you can upgrade your plan at any time. We'll work with you to seamlessly transition your project to include additional features and capabilities.",
            ),
            FaqItem(
                question="What happens after the support period ends?",
                answer="After your included support period, you can purchase extended support packages. We also offer maintenance retainers for ongoing updates and improvements.",
            ),
            FaqItem(
                question="Do you offer refunds?",
                answer="We offer a satisfaction guarantee on our work. If you're not happy with the initial concepts, we'll work with you to make it right or provide a partial refund.",
            ),
        ],
        cta_title="Need a Custom Quote?",
        cta_description="Every project is unique. Let's discuss your specific requirements.",
        cta_primary_label="Schedule a Call",
        cta_primary_href="/contact",
        cta_secondary_label="View Services",
        cta_secondary_href="/services",
    )
    return content.model_dump()


# Default markdown for policy pages (full content; edit via admin)
def _default_privacy_markdown() -> str:
    return """At TechPath ("we," "our," or "us"), we are committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information.

## 1. Information We Collect

**Personal Information:** Name, contact information, company, job title, billing and payment information, communication preferences.

**Automatically Collected:** IP address, device information, browser type, pages visited, referring URLs, cookies and similar technologies.

## 2. How We Use Your Information

- To provide and maintain our services
- To process transactions and send related information
- To respond to inquiries and provide customer support
- To send promotional communications (with your consent)
- To improve our website and services
- To detect and prevent fraud or abuse
- To comply with legal obligations

## 3. Information Sharing and Disclosure

We may share information with service providers, in connection with business transfers, when required by law, or with your consent. We do not sell your personal information.

## 4. Data Security

We implement SSL/TLS encryption, secure storage with access controls, regular security assessments, and employee training on data protection.

## 5. Your Rights and Choices

You have rights to access, correction, deletion, opt-out, and data portability. Contact privacy@techpath.biz to exercise these rights.

## 6. Cookies and Tracking

See our [Cookie Policy](/cookies) for details.

## 7. Third-Party Links

We are not responsible for the privacy practices of external sites.

## 8. Children's Privacy

Our services are not directed to individuals under 16. We do not knowingly collect data from children.

## 9. Changes to This Policy

We may update this policy from time to time. We will post changes on this page and update the "Last updated" date.

## 10. Contact Us

**TechPath** — Email: [privacy@techpath.biz](mailto:privacy@techpath.biz) — Phone: +1 (555) 123-4567
"""


def _default_terms_markdown() -> str:
    return """Welcome to TechPath. These Terms of Service govern your access to and use of our website, products, and services. By using our services, you agree to these Terms.

## 1. Acceptance of Terms

By using TechPath's services, you agree to these Terms and our Privacy Policy. If using on behalf of an organization, you represent that you have authority to bind that organization.

## 2. Description of Services

TechPath provides IT services including web development, AI consulting, cloud services, data analytics, cybersecurity, and technical consulting. Scope is defined in individual agreements or statements of work.

## 3. User Responsibilities

You agree to: provide accurate information; maintain confidentiality of credentials; use services lawfully; not interfere with or disrupt services; not attempt unauthorized access.

## 4. Intellectual Property

Content, trademarks, and materials on our site are owned by TechPath or licensors. You may not copy, modify, or distribute without permission.

## 5. Payment and Fees

Fees are as agreed in your agreement. Payment terms typically 50% upfront, 50% on completion. Late payments may incur interest.

## 6. Limitation of Liability

To the maximum extent permitted by law, TechPath shall not be liable for indirect, incidental, special, or consequential damages.

## 7. Termination

We may suspend or terminate access for breach of these Terms. You may terminate by ceasing use and notifying us.

## 8. Governing Law

These Terms are governed by the laws of the State of California, without regard to conflict of law principles.

## 9. Contact

Questions? Contact us at [legal@techpath.biz](mailto:legal@techpath.biz).
"""


def _default_cookie_markdown() -> str:
    return """This Cookie Policy explains how TechPath uses cookies and similar technologies. Read alongside our [Privacy Policy](/privacy).

## 1. What Are Cookies?

Cookies are small text files stored on your device when you visit a website. They can be "session" (expire when you close the browser) or "persistent" (remain for a set period).

## 2. Types of Cookies We Use

**Essential:** Necessary for the site to function (session management, security, load balancing). Cannot be disabled.

**Performance:** Help us understand how visitors interact (page views, errors, performance). Can be disabled in cookie preferences.

**Functional:** Remember your preferences (language, region). Can be disabled.

**Marketing:** Used to deliver relevant ads (with your consent). Can be disabled.

## 3. How to Manage Cookies

You can block or delete cookies via your browser settings. Blocking essential cookies may affect site functionality.

## 4. Updates

We may update this policy. We will post changes here and update the "Last updated" date.

## 5. Contact

Questions? [privacy@techpath.biz](mailto:privacy@techpath.biz)
"""


def get_builtin_privacy_content() -> dict[str, Any]:
    """Return default privacy page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Privacy Policy",
            description="Learn how TechPath collects, uses, and protects your personal information. Our commitment to your privacy and data security.",
        ),
        page_title="Privacy Policy",
        last_updated="December 15, 2025",
        markdown_content=_default_privacy_markdown(),
    )
    return content.model_dump()


def get_builtin_terms_content() -> dict[str, Any]:
    """Return default terms page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Terms of Service",
            description="Read the terms and conditions governing the use of TechPath's website and services.",
        ),
        page_title="Terms of Service",
        last_updated="December 15, 2025",
        markdown_content=_default_terms_markdown(),
    )
    return content.model_dump()


def get_builtin_cookie_content() -> dict[str, Any]:
    """Return default cookie page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Cookie Policy",
            description="Learn about how TechPath uses cookies and similar technologies on our website.",
        ),
        page_title="Cookie Policy",
        last_updated="December 15, 2025",
        markdown_content=_default_cookie_markdown(),
    )
    return content.model_dump()


async def _get_content_or_default(
    db: AsyncSession,
    key: str,
    validator: type,
    builtin: Callable[[], dict[str, Any]],
) -> dict[str, Any]:
    """Fetch content from DB or return built-in default."""
    raw = await app_setting_crud.get_value(db, key)
    if raw and raw.strip():
        try:
            data = json.loads(raw)
            validated = validator.model_validate(data)
            return validated.model_dump()
        except (json.JSONDecodeError, Exception):
            pass
    return builtin()


@router.get("/training-page")
async def get_training_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get training landing page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, TRAINING_LANDING_KEY, TrainingLandingContent, get_builtin_training_content)


@router.get("/home-page")
async def get_home_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get home page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, HOME_LANDING_KEY, HomeLandingContent, get_builtin_home_content)


@router.get("/about-page")
async def get_about_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get about page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, ABOUT_PAGE_KEY, AboutPageContent, get_builtin_about_content)


@router.get("/services-page")
async def get_services_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get services landing page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, SERVICES_LANDING_KEY, ServicesLandingContent, get_builtin_services_content)


@router.get("/contact-page")
async def get_contact_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get contact page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, CONTACT_PAGE_KEY, ContactPageContent, get_builtin_contact_content)


@router.get("/pricing-page")
async def get_pricing_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get pricing page content (public, no auth).
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, PRICING_PAGE_KEY, PricingPageContent, get_builtin_pricing_content)


@router.get("/privacy-page")
async def get_privacy_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get privacy policy page content (public, no auth). Body is markdown.
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, PRIVACY_PAGE_KEY, PolicyPageContent, get_builtin_privacy_content)


@router.get("/terms-page")
async def get_terms_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get terms of service page content (public, no auth). Body is markdown.
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, TERMS_PAGE_KEY, PolicyPageContent, get_builtin_terms_content)


@router.get("/cookie-page")
async def get_cookie_page_content(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get cookie policy page content (public, no auth). Body is markdown.
    Returns DB value if key exists and is valid JSON; otherwise returns built-in default.
    """
    return await _get_content_or_default(db, COOKIE_PAGE_KEY, PolicyPageContent, get_builtin_cookie_content)
