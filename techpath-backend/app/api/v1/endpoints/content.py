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
            HomeTestimonialItem(quote="TechPath built our entire booking platform from scratch. Traveller sign-ups jumped 3× within 60 days of launch.", author="Rahul Mehta", role="Founder & CEO", company="Himalayan Tripsters", logo="/images/trusted/himalayan-tripsters.png"),
            HomeTestimonialItem(quote="Our patient management system went live in 8 weeks. Staff productivity improved and patient wait times dropped by 40%.", author="Dr. Priya Sharma", role="Director of Operations", company="Octavia Hospital", logo="/images/trusted/octavia-hospital.png"),
            HomeTestimonialItem(quote="The AI-powered SEO dashboard TechPath delivered gives us insights our competitors simply don't have. Game-changing work.", author="Amit Khatri", role="Head of Growth", company="Digital Assassin", logo="/images/trusted/digital-assassin.png"),
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
    return """At **Techpath Research and Development Pvt Ltd** ('Techpath', 'we', 'us', or 'our'), your privacy matters to us. This Privacy Policy explains what personal data we collect when you visit [techpath.biz](https://techpath.biz) or enrol in any of our IT training courses — offline at our Mughalsarai centre or via live online batches — and how we use, store, and protect that data.

This policy is aligned with India's **Digital Personal Data Protection (DPDP) Act 2023** and applicable rules.

If you have any questions, contact us at [privacy@techpath.biz](mailto:privacy@techpath.biz) or call [+91 8299708052](tel:+918299708052).

---

## 1. Information We Collect

### 1.1 Information You Give Us Directly

When you enquire about a course, register for a batch, or contact us, we may collect:

- **Identity data:** Full name, date of birth, gender
- **Contact data:** Mobile number, email address, postal address
- **Educational data:** Highest qualification, stream (Arts / Commerce / Science), previous institute
- **Payment data:** Fee payment records, UPI transaction IDs, receipt numbers *(we do not store full card or bank account details)*
- **Communication data:** Messages sent via our enquiry form, WhatsApp, or email
- **Guardian data:** Parent or guardian name and contact number (for students under 18)

### 1.2 Information Collected Automatically

When you visit [techpath.biz](https://techpath.biz), our systems and third-party tools may automatically collect:

- IP address and approximate location
- Device type, operating system, and browser version
- Pages visited, time spent on each page, and referring URL
- Cookie data (see our [Cookie Policy](/cookie-policy) for full details)

### 1.3 Information from Third Parties

We may receive information about you from:

- **Google / Meta** — if you interact with our ads on Google Search, YouTube, Instagram, or Facebook
- **WhatsApp** — messages you send us via our WhatsApp Business number
- **Word of mouth** — if a friend or family member provides your contact details when enquiring on your behalf (we will only contact you with your consent)

---

## 2. How We Use Your Information

We use your personal data only for the following purposes:

| Purpose | Legal Basis |
|---------|-------------|
| Processing your course enrolment and confirming your seat | Contractual necessity |
| Sending batch schedules, class links, and study materials | Contractual necessity |
| Responding to your enquiries and providing student support | Legitimate interest |
| Processing fee payments and issuing receipts | Contractual necessity |
| Issuing course completion certificates | Contractual necessity |
| Providing placement assistance (resume, mock interviews, referrals) | Contractual necessity |
| Sending course updates, new batch announcements, or promotional offers | Consent (you may opt out at any time) |
| Improving our website and course content based on usage patterns | Legitimate interest |
| Detecting and preventing fraud or misuse of our services | Legitimate interest / Legal obligation |
| Complying with applicable Indian law | Legal obligation |

We do **not** use your data for automated decision-making or profiling that produces legal or similarly significant effects on you.

---

## 3. How We Share Your Information

We do **not sell** your personal data. We may share it only in the following limited circumstances:

### 3.1 Service Providers

We work with trusted third-party providers who help us operate our services. They process your data only on our instructions:

- **Google Workspace** — email and class scheduling
- **Google Meet / Zoom** — live online class delivery
- **Google Analytics** — website usage analytics (anonymised)
- **Meta Pixel** — ad performance measurement (with your cookie consent)
- **Payment gateways** — processing course fee transactions

All service providers are contractually bound to keep your data confidential and secure.

### 3.2 Legal Requirements

We may disclose your data if required to do so by a court order, government authority, or applicable Indian law (including the DPDP Act 2023 and IT Act 2000).

### 3.3 Business Transfers

In the event of a merger, acquisition, or sale of assets, your data may be transferred to the acquiring entity. We will notify you via email or a prominent notice on [techpath.biz](https://techpath.biz) before your data is transferred and becomes subject to a different privacy policy.

### 3.4 With Your Consent

For any other sharing not described above, we will ask for your explicit consent first.

---

## 4. Data Retention

We retain your personal data only for as long as necessary for the purposes described in this policy:

| Data Type | Retention Period |
|-----------|------------------|
| Enrolment and student records | 5 years after course completion |
| Payment and fee records | 7 years (as required by Indian accounting law) |
| Certificate records | Indefinitely (for verification purposes) |
| Website analytics data | 26 months (Google Analytics default) |
| Marketing communication preferences | Until you opt out |
| Enquiry and contact messages | 2 years |

After the retention period ends, data is securely deleted or anonymised.

---

## 5. Data Security

We take the security of your personal data seriously. Our measures include:

- **SSL/TLS encryption** on all pages of [techpath.biz](https://techpath.biz) (HTTPS)
- **Restricted access** — only authorised Techpath staff can access student records
- **Secure storage** — student data is stored on password-protected, access-controlled systems
- **No storage of full payment credentials** — we do not store card numbers, CVVs, or full bank account details
- **Regular reviews** of our data handling practices

While we take every reasonable precaution, no method of transmission over the internet is 100% secure. If you suspect any unauthorised access to your data, please notify us immediately at [privacy@techpath.biz](mailto:privacy@techpath.biz).

---

## 6. Your Rights Under the DPDP Act 2023

As a data principal under India's Digital Personal Data Protection Act 2023, you have the following rights:

### Right to Access
You may request a summary of the personal data we hold about you and how it is being processed.

### Right to Correction
You may request correction of any inaccurate or incomplete personal data we hold.

### Right to Erasure
You may request deletion of your personal data where it is no longer necessary for the purpose for which it was collected, subject to legal retention obligations.

### Right to Withdraw Consent
Where we rely on your consent to process data (e.g., marketing communications), you may withdraw that consent at any time. Withdrawal does not affect the lawfulness of processing before withdrawal.

### Right to Grievance Redressal
You have the right to raise a grievance with us regarding our data processing practices. We will respond within **30 days**.

### Right to Nominate
You may nominate another individual to exercise your rights on your behalf in the event of your death or incapacity.

**To exercise any of these rights**, email us at [privacy@techpath.biz](mailto:privacy@techpath.biz) with your name, enrolled course, and the specific right you wish to exercise. We will respond within **30 days**.

---

## 7. Cookies and Tracking Technologies

We use cookies and similar technologies on [techpath.biz](https://techpath.biz) to keep the site running, understand how visitors use it, and (with your consent) show relevant course ads. For full details on the types of cookies we use and how to manage them, see our [Cookie Policy](/cookie-policy).

---

## 8. Third-Party Links

Our website may contain links to external websites — for example, links to government portals, industry resources, or social media platforms. We are not responsible for the privacy practices of those websites. We encourage you to read their privacy policies before sharing any personal data with them.

---

## 9. Children's Privacy

Techpath's courses are open to students from age 10 upwards, with parental or guardian consent required for anyone under 18. We do not knowingly collect personal data directly from children under 13 without explicit parental consent.

If you believe we have inadvertently collected data from a child without appropriate consent, please contact us immediately at [privacy@techpath.biz](mailto:privacy@techpath.biz) and we will delete it promptly.

---

## 10. Changes to This Policy

We may update this Privacy Policy from time to time — for example, when we add new services, when the law changes, or when we want to make our explanations clearer. When we make changes, we will:

1. Update the **'Last Updated'** date at the top of this page
2. Post a notice on [techpath.biz](https://techpath.biz) for material changes
3. Where required by law, seek your fresh consent

We encourage you to review this page periodically to stay informed about how we protect your data.

---

## 11. Grievance Officer

In accordance with the Information Technology Act 2000 and applicable rules, Techpath has designated a Grievance Officer for data-related concerns:

**Grievance Officer:** Director, Techpath Research and Development Pvt Ltd
📍 Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101, India
📧 [privacy@techpath.biz](mailto:privacy@techpath.biz)
📞 [+91 8299708052](tel:+918299708052)

Complaints will be acknowledged within **48 hours** and resolved within **30 days**.

---

## 12. Contact Us

For any questions, requests, or concerns about this Privacy Policy or your personal data:

**Techpath Research and Development Pvt Ltd**
📍 Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101, India
📧 [privacy@techpath.biz](mailto:privacy@techpath.biz)
📞 [+91 8299708052](tel:+918299708052)
💬 [WhatsApp Us](https://wa.me/918299708052?text=Hi%2C+I+have+a+question+about+the+Techpath+Privacy+Policy.)
🌐 [techpath.biz](https://techpath.biz)
"""


def _default_terms_markdown() -> str:
    return """Welcome to **Techpath Research and Development Pvt Ltd** ('Techpath', 'we', 'us', or 'our'). These Terms of Service ('Terms') govern your access to and use of our website at [techpath.biz](https://techpath.biz), our IT training courses, and all related services.

By visiting our website or enrolling in any course — whether offline at our Mughalsarai centre or via live online batches — you confirm that you have read, understood, and agreed to these Terms. If you do not agree, please do not use our services.

For any questions about these Terms, contact us at [legal@techpath.biz](mailto:legal@techpath.biz) or call [+91 8299708052](tel:+918299708052).

---

## 1. Acceptance of Terms

By accessing [techpath.biz](https://techpath.biz) or enrolling in any Techpath course or programme, you agree to be bound by these Terms and our [Privacy Policy](/privacy) and [Cookie Policy](/cookie-policy).

If you are enrolling on behalf of a minor (a student under 18 years of age), you — as the parent or guardian — represent that you have the authority and consent to agree to these Terms on their behalf.

These Terms apply to:
- Students enrolled in offline classes at our Mughalsarai centre
- Students enrolled in live online batches
- Visitors browsing [techpath.biz](https://techpath.biz)
- Any individual or organisation making an enquiry or purchase through our platform

---

## 2. Our Services

Techpath Research and Development Pvt Ltd is an IT training institute located at **Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101**, offering courses in:

- Programming & Development (Python, Full-Stack Web Development, DevOps)
- Data & AI (Data Science + AI/ML, Gen AI Master)
- Hardware & IoT (IoT Essentials, IoT, Robotics)
- Digital Skills (Digital Marketing with Gen AI, ADCA with Gen AI, Computer Fundamentals)

Courses are delivered in two modes: **offline** (at our Mughalsarai centre) and **live online** (via Google Meet or Zoom — same instructor, same curriculum). Specific course details, durations, fees, and batch schedules are published on [techpath.biz](https://techpath.biz) and may be updated from time to time.

We reserve the right to modify, suspend, or discontinue any course or service with reasonable prior notice.

---

## 3. Enrolment & Eligibility

- You must be at least 10 years old to enrol in any Techpath course. Students under 18 require parental or guardian consent.
- You agree to provide accurate, complete, and current information during registration.
- You are responsible for maintaining the confidentiality of any login credentials provided to you for online classes or course materials.
- Techpath reserves the right to refuse enrolment or cancel a registration at its discretion.

---

## 4. Fees, Payment & Refund Policy

### 4.1 Fees

Course fees are as published on [techpath.biz](https://techpath.biz) or as communicated in writing at the time of enrolment. Fees are the same for both offline and live online modes.

### 4.2 Payment Terms

- A **registration fee or advance** (as specified at enrolment) is required to confirm your seat in a batch.
- The remaining balance is payable as per the instalment schedule agreed at enrolment.
- **EMI options** are available for all courses — details provided at our centre or via [+91 8299708052](tel:+918299708052).
- Late payment may result in temporary suspension of access to classes or course materials until dues are cleared.

### 4.3 Refund Policy

- Refund requests made **before the batch start date** will be considered on a case-by-case basis. Registration fees are non-refundable.
- Refund requests made **after the batch has started** will not be entertained except in exceptional circumstances (medical emergency, relocation), at Techpath's sole discretion.
- No refund is applicable once course materials, access credentials, or certificates have been issued.

To raise a refund request, email [legal@techpath.biz](mailto:legal@techpath.biz) with your enrolment details.

---

## 5. User Responsibilities

By using Techpath's services, you agree to:

- Attend classes regularly and complete assignments in good faith
- Treat instructors and fellow students with respect — harassment or disruptive behaviour will result in immediate termination of enrolment without refund
- Not record, redistribute, or commercially use any live class session, recorded material, or course content without written permission from Techpath
- Not share your login credentials or class access links with any person not enrolled in the batch
- Use Techpath's website and services only for lawful purposes and in compliance with applicable Indian law
- Not attempt to reverse-engineer, scrape, or interfere with any part of [techpath.biz](https://techpath.biz)

---

## 6. Intellectual Property

All content on [techpath.biz](https://techpath.biz) — including text, course curricula, videos, code samples, graphics, logos, and brand marks — is the intellectual property of **Techpath Research and Development Pvt Ltd** or its licensors, and is protected under applicable Indian copyright and trademark law.

You may not copy, reproduce, distribute, publish, or create derivative works from any Techpath content without prior written permission, except for personal, non-commercial reference during your enrolled course.

Student projects created during a Techpath course remain the intellectual property of the student. By submitting projects for review or showcase, you grant Techpath a non-exclusive, royalty-free licence to display your work for promotional purposes (e.g., on our website or social media), with attribution.

---

## 7. Certificates & Placement Assistance

### 7.1 Certificates

A course completion certificate is issued upon successful completion of the course, including attendance requirements and project submissions. Techpath certificates are issued by Techpath Research and Development Pvt Ltd and are not equivalent to university degrees or government certifications unless explicitly stated.

### 7.2 Placement Assistance

Techpath provides placement support including resume building, mock interviews, LinkedIn profile guidance, and internship referrals. **Placement assistance is a best-effort service and does not constitute a guarantee of employment.** Job outcomes depend on individual effort, market conditions, and employer decisions beyond Techpath's control.

---

## 8. Limitation of Liability

To the fullest extent permitted under applicable Indian law:

- Techpath's total liability to you for any claim arising out of or related to these Terms or our services shall not exceed the **total fees paid by you** for the specific course in question.
- Techpath shall not be liable for any indirect, incidental, special, consequential, or punitive damages — including loss of income, loss of data, or loss of opportunity — arising from your use of or inability to use our services.
- Techpath is not responsible for internet connectivity issues, device problems, or third-party platform outages (e.g., Google Meet, Zoom) that may affect live online classes. In such cases, makeup classes or recorded sessions will be provided where feasible.

---

## 9. Termination

**By Techpath:** We may suspend or terminate your access to classes, materials, or our website if you breach these Terms, fail to make payments, or engage in misconduct — with or without prior notice depending on the severity of the breach.

**By you:** You may withdraw from a course at any time by notifying us in writing at [legal@techpath.biz](mailto:legal@techpath.biz). Refund eligibility is governed by Section 4.3 above.

Upon termination, any licences granted to you under these Terms will immediately cease. Provisions that by their nature should survive termination (intellectual property, limitation of liability, governing law) will continue to apply.

---

## 10. Governing Law & Dispute Resolution

These Terms are governed by and construed in accordance with the laws of **India**, specifically applicable to the state of **Uttar Pradesh**.

Any dispute arising out of or in connection with these Terms shall first be attempted to be resolved amicably through direct communication with us at [legal@techpath.biz](mailto:legal@techpath.biz) or [+91 8299708052](tel:+918299708052).

If a dispute cannot be resolved amicably within 30 days, it shall be subject to the exclusive jurisdiction of the courts located in **Chandauli, Uttar Pradesh, India**.

---

## 11. Changes to These Terms

We may update these Terms from time to time to reflect changes in our services, applicable law, or our business practices. When we do:

1. We will update the **'Last Updated'** date at the top of this page
2. We will post a notice on [techpath.biz](https://techpath.biz) for material changes
3. Continued use of our services after the updated Terms are posted constitutes your acceptance of the revised Terms

We encourage you to review this page periodically.

---

## 12. Contact Us

If you have any questions, concerns, or feedback about these Terms, please reach out:

**Techpath Research and Development Pvt Ltd**
📍 Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101, India
📧 [legal@techpath.biz](mailto:legal@techpath.biz)
📞 [+91 8299708052](tel:+918299708052)
💬 [WhatsApp Us](https://wa.me/918299708052?text=Hi%2C+I+have+a+question+about+the+Techpath+Terms+of+Service.)
🌐 [techpath.biz](https://techpath.biz)

We aim to respond to all legal and policy queries within **48 business hours**.
"""


def _default_cookie_markdown() -> str:
    return """This Cookie Policy explains how **Techpath Research and Development Pvt Ltd** ('Techpath', 'we', 'us', or 'our') uses cookies and similar tracking technologies on [techpath.biz](https://techpath.biz). Please read this alongside our [Privacy Policy](/privacy).

If you have questions at any point, reach us at [privacy@techpath.biz](mailto:privacy@techpath.biz) or call us at [+91 8299708052](tel:+918299708052).

---

## 1. What Are Cookies?

Cookies are small text files that a website saves on your device (computer, phone, or tablet) when you visit it. They help the site remember your actions and preferences so you don't have to re-enter them every time you come back.

Cookies can be:

- **Session cookies** — Temporary. They are deleted automatically when you close your browser.
- **Persistent cookies** — These stay on your device for a set period (days, weeks, or months) or until you delete them manually.

We also use similar technologies like **web beacons**, **pixel tags**, and **local storage** that work in a comparable way to cookies.

---

## 2. Why Does Techpath Use Cookies?

We use cookies to:

- Keep the website running smoothly and securely
- Remember your settings and preferences between visits
- Understand how visitors use our site so we can improve it
- Show relevant course information and ads to people who have visited our site

We do **not** sell your data. Cookies help us serve you better — not to profit from your personal information.

---

## 3. Types of Cookies We Use

### 3.1 Essential Cookies *(Always Active)*

These cookies are required for the website to function. Without them, services like login sessions, security checks, and page loading cannot work. You cannot disable these through our cookie settings, though you may block them via your browser (which may break parts of the site).

| Cookie Name | Purpose | Duration |
|-------------|---------|----------|
| `session_id` | Maintains your login or enquiry session | Session |
| `csrf_token` | Protects against cross-site request forgery attacks | Session |
| `lb_route` | Load balancing — distributes traffic across our servers | Session |

### 3.2 Performance & Analytics Cookies *(Optional)*

These help us understand how visitors find and use [techpath.biz](https://techpath.biz) — which pages are most visited, how long people stay, and where errors occur. All data is aggregated and anonymous.

| Cookie Name | Provider | Purpose | Duration |
|-------------|----------|---------|----------|
| `_ga`, `_gid` | Google Analytics | Page views, session counts, traffic sources | 2 years / 24 hrs |
| `_gat` | Google Analytics | Request rate throttling | 1 minute |

You can disable these in your [cookie preferences](#manage).

### 3.3 Functional Cookies *(Optional)*

These remember choices you make to give you a better, more personalised experience — such as your preferred language or region.

| Cookie Name | Purpose | Duration |
|-------------|---------|----------|
| `lang_pref` | Stores your language preference (English or Hindi) | 1 year |
| `region` | Remembers your city/region for localised content | 6 months |

### 3.4 Marketing & Targeting Cookies *(Optional, with consent)*

We use these only with your consent to show course-related ads on platforms like Google and Meta (Facebook/Instagram) that may be relevant to you. They help us measure whether our advertising is working.

| Cookie Name | Provider | Purpose | Duration |
|-------------|----------|---------|----------|
| `_fbp`, `_fbc` | Meta Pixel | Tracks conversions from Facebook/Instagram ads | 3 months |
| `IDE` | Google Ads | Measures ad effectiveness | 13 months |

You can withdraw this consent at any time by visiting [your cookie preferences](#manage).

---

## 4. How to Manage or Disable Cookies {#manage}

You are in control. Here are your options:

### Through Our Cookie Preference Centre

When you first visit [techpath.biz](https://techpath.biz), a cookie banner appears. You can choose to accept all, accept only essential cookies, or manage your choices category by category. You can change your mind at any time using the **'Cookie Settings'** link in our website footer.

### Through Your Browser Settings

All major browsers let you block or delete cookies directly:

- **Google Chrome:** Settings → Privacy and Security → Cookies and other site data
- **Mozilla Firefox:** Settings → Privacy & Security → Cookies and Site Data
- **Safari:** Preferences → Privacy → Manage Website Data
- **Microsoft Edge:** Settings → Cookies and site permissions

> ⚠️ **Note:** Blocking essential cookies will affect core website functionality. Features like the enquiry form and course registration may not work correctly.

### Opt Out of Analytics

You can install the [Google Analytics Opt-Out Browser Add-on](https://tools.google.com/dlpage/gaoptout) to prevent Google Analytics from collecting data about your visits.

### Opt Out of Targeted Advertising

- **Google:** [My Ad Center](https://myadcenter.google.com/) or [Google Ads Settings](https://adssettings.google.com/)
- **Meta:** [Facebook Ad Preferences](https://www.facebook.com/settings/?tab=ads)
- **Industry opt-out:** [YourOnlineChoices.com](https://www.youronlinechoices.com/)

---

## 5. Third-Party Cookies

Some cookies on our site are placed by third-party services we use — such as Google Analytics, Google Ads, and Meta Pixel. We do not control these cookies directly. Each third party has its own privacy policy:

- [Google Privacy Policy](https://policies.google.com/privacy)
- [Meta Privacy Policy](https://www.facebook.com/policy)

These third parties may also collect data about your activity on other websites as part of their own advertising networks. We only use third-party cookies where necessary for the purposes described above.

---

## 6. Cookies and Children

Techpath's website is not directed at children under 13. We do not knowingly use cookies to collect personal data from anyone under 13. If you believe we have inadvertently collected data from a child, please contact us immediately at [privacy@techpath.biz](mailto:privacy@techpath.biz).

---

## 7. Changes to This Policy

We may update this Cookie Policy from time to time — for example, if we add new tools to our website, if the law changes, or if we want to make our explanations clearer. When we make a change, we will:

1. Update the **'Last Updated'** date at the top of this page
2. Post a notice on our website for significant changes
3. Ask for your consent again if we start using cookies in a new, material way

We encourage you to check this page periodically.

---

## 8. Contact Us

If you have any questions about how we use cookies — or would like to exercise any of your data rights — please get in touch:

**Techpath Research and Development Pvt Ltd**
📍 Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101, India
📧 [privacy@techpath.biz](mailto:privacy@techpath.biz)
📞 [+91 8299708052](tel:+918299708052)
💬 [WhatsApp Us](https://wa.me/918299708052?text=Hi%2C+I+have+a+question+about+the+Techpath+Cookie+Policy.)
🌐 [techpath.biz](https://techpath.biz)

We aim to respond to all privacy-related queries within **48 business hours**.
"""


def get_builtin_privacy_content() -> dict[str, Any]:
    """Return default privacy page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Privacy Policy | Techpath Research and Development Pvt Ltd",
            description="Learn how Techpath collects, uses, and protects your personal data at techpath.biz — fully aligned with India's Digital Personal Data Protection Act 2023.",
            canonical_url="https://techpath.biz/privacy/",
            no_index=False,
        ),
        page_title="Privacy Policy",
        last_updated="April 25, 2026",
        markdown_content=_default_privacy_markdown(),
    )
    return content.model_dump()


def get_builtin_terms_content() -> dict[str, Any]:
    """Return default terms page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Terms of Service | Techpath Research and Development Pvt Ltd",
            description="Read the terms and conditions governing your use of Techpath's website, IT training courses, and services at techpath.biz.",
            canonical_url="https://techpath.biz/terms-of-service/",
            no_index=False,
        ),
        page_title="Terms of Service",
        last_updated="April 25, 2026",
        markdown_content=_default_terms_markdown(),
    )
    return content.model_dump()


def get_builtin_cookie_content() -> dict[str, Any]:
    """Return default cookie page content (markdown)."""
    content = PolicyPageContent(
        seo=PageSeoContent(
            title="Cookie Policy | Techpath Research and Development Pvt Ltd",
            description="Understand how Techpath uses cookies on techpath.biz — what data we collect, why we collect it, and how you can manage your preferences.",
            canonical_url="https://techpath.biz/cookie-policy/",
            no_index=False,
        ),
        page_title="Cookie Policy",
        last_updated="April 25, 2026",
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
