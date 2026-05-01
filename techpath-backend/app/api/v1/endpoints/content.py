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
    AboutArmItem,
    AboutHeroContent,
    AboutPageContent,
    AboutTeamMember,
    AboutTrustedByItem,
    AboutValueItem,
    BatchTiming,
    ContactBadge,
    ContactCtaBlock,
    ContactCtaItem,
    ContactHeroContent,
    ContactMethodItem,
    ContactPageContent,
    ContactSecondaryAction,
    ContactSocialProof,
    ContactSocialProofSection,
    ContactStatItem,
    ContactTab,
    ContactTabCta,
    CtaButton,
    CtaContent,
    DeliveryMode,
    FaqItem,
    HeadOfSolutions,
    HeroContent,
    HomeCaseStudiesSection,
    HomeCtaContent,
    HomeFeatureItem,
    HomeHeroContent,
    HomeLandingContent,
    HomeServiceItem,
    HomeStatItem,
    HomeTestimonialItem,
    OfficeHours,
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
    WhatToExpect,
    WhatToExpectStep,
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
    """Return default training page content for Techpath Academy Mughalsarai."""
    content = TrainingLandingContent(
        seo=PageSeoContent(
            title="IT Training Courses in Mughalsarai | Offline + Live Online | Techpath Academy",
            description="14 IT training courses in Mughalsarai and live online — Python, Data Science, Gen AI, Full Stack, DevOps, IoT, Digital Marketing. Starting ₹6,000. EMI available. 30-day refund.",
            image="/images/training-featured.jpg",
            canonical_url="https://techpath.biz/training/",
            no_index=False,
        ),
        hero=HeroContent(
            title="Job-Ready Tech Skills, Built in Mughalsarai",
            subtitle="14 IT courses · Offline + Live Online · Bilingual Hindi-English · Small batches max 25 students",
            headline_subline="From Computer Fundamentals to Python Full Stack with Gen AI",
            badge_text="🔥 New Batches Starting Soon — Free Demo Class Available",
            primary_cta=CtaButton(label="Book Free Demo Class", href="/contact"),
            secondary_cta=CtaButton(label="View All Courses", href="#courses"),
            trust_badges=[
                TrustBadge(icon="👨‍🎓", value="50,000+", label="Students Trained"),
                TrustBadge(icon="💼", value="94%", label="Placement Rate"),
                TrustBadge(icon="📚", value="14", label="Courses Available"),
                TrustBadge(icon="🔄", value="30 Days", label="Money-Back Guarantee"),
            ],
        ),
        pain_points=PainPointsContent(
            section_title="Stuck Without a Clear Tech Career Path?",
            section_subtext="If you're a student in Mughalsarai, Chandauli, Varanasi, or anywhere in eastern UP — these are the real challenges holding you back.",
            transition_text="Techpath fixes all three — with project-led courses, transparent fees, and live instructors who teach you the same skills companies hire for in 2026.",
            items=[
                PainPointItem(
                    icon="📉",
                    title="Outdated Skills, No Direction",
                    description="Your college taught theory from 10 years ago. The market wants Python, React, Cloud, and Gen AI. Without these, even a B.Tech or BCA degree won't get you interviews.",
                    color="text-red-400",
                    bg_color="bg-red-500/10",
                    border_color="border-red-500/30",
                ),
                PainPointItem(
                    icon="💸",
                    title="Expensive City Coaching",
                    description="Big-city institutes charge ₹2–5 lakhs for IT courses. For most students in eastern UP and Bihar, that's not realistic. You shouldn't have to leave home or take a loan to learn tech.",
                    color="text-orange-400",
                    bg_color="bg-orange-500/10",
                    border_color="border-orange-500/30",
                ),
                PainPointItem(
                    icon="📚",
                    title="Pre-Recorded Videos Don't Work",
                    description="YouTube tutorials and recorded courses sound easy but most students never finish them. Without a live instructor, weekly projects, and a real classroom, motivation dies in week three.",
                    color="text-yellow-400",
                    bg_color="bg-yellow-500/10",
                    border_color="border-yellow-500/30",
                ),
            ],
        ),
        usps=UspsContent(
            section_title="Why Students Across Eastern UP Choose Techpath",
            section_subtext="Project-first learning, bilingual instruction, and honest pricing — built for students from Mughalsarai, Varanasi, Ghazipur, Ballia, and Bihar.",
            items=[
                UspItem(
                    icon="🎓",
                    title="Live Instructors, Bilingual Teaching",
                    highlights=[
                        "Hindi + English instruction — language is never a barrier",
                        "Real engineers with industry experience",
                        "Direct doubt-clearing in every class",
                    ],
                    color="from-blue-500 to-cyan-500",
                ),
                UspItem(
                    icon="💻",
                    title="Offline + Live Online",
                    highlights=[
                        "Offline at Circus Road, Mughalsarai",
                        "Live online via Google Meet — same instructor, same certificate",
                        "Small batches: max 25 students per batch",
                    ],
                    color="from-purple-500 to-pink-500",
                ),
                UspItem(
                    icon="🚀",
                    title="Project-First Curriculum",
                    highlights=[
                        "Build real projects, hosted on your GitHub",
                        "Project reviews and code feedback every week",
                        "Resume, LinkedIn, and mock interview support",
                    ],
                    color="from-primary-500 to-secondary-500",
                ),
                UspItem(
                    icon="💰",
                    title="Transparent Pricing + EMI",
                    highlights=[
                        "Courses from ₹6,000 — no hidden charges",
                        "Monthly EMI on all courses",
                        "30-day money-back guarantee",
                    ],
                    color="from-green-500 to-emerald-500",
                ),
            ],
        ),
        faqs=[
            FaqItem(question="Do I need prior coding experience to enrol at Techpath?", answer="No. Beginner courses like Computer Fundamentals, Python Programming, ADCA with Gen AI, and Digital Marketing with Gen AI are designed for absolute beginners — including 12th-pass students. Intermediate courses like Data Science + AI/ML and Python Full Stack assume basic Python knowledge. Each course page lists specific prerequisites."),
            FaqItem(question="Does Techpath offer a job placement guarantee?", answer="Techpath offers placement assistance — including resume building, LinkedIn optimisation, GitHub portfolio review, mock interviews, and internship referrals. Our placement rate is 94% within 90 days of course completion. Placement assistance is a best-effort service and does not constitute a legal job guarantee — outcomes depend on individual effort, market conditions, and employer decisions."),
            FaqItem(question="What if I don't like the course in the first month?", answer="Techpath offers a 30-day money-back guarantee. If you're not satisfied within the first 30 days of a paid course, you can request a full refund — no questions asked. We want students to feel confident before committing fully."),
            FaqItem(question="Are the live online classes recorded?", answer="Live online classes at Techpath are conducted live via Google Meet or Zoom — same instructor, same timings, same curriculum as offline batches. Sessions are interactive with real-time doubt clearing and live coding. We do not run pre-recorded courses — every class is taught live."),
            FaqItem(question="What are the batch timings?", answer="Techpath runs three daily batches Monday to Saturday: Morning (9–11 AM), Afternoon (1–3 PM), and Evening (5–7 PM). Weekend doubt sessions are available for all enrolled students. You can switch batches if your schedule changes."),
            FaqItem(question="Is EMI available for course fees?", answer="Yes. Techpath offers monthly instalment options on all 14 courses. Specific EMI plans depend on the course duration and total fee. Call or WhatsApp +91 8299708052 to discuss EMI options for your chosen course."),
            FaqItem(question="How many projects will I build during the course?", answer="Every Techpath course is project-led. Students build real projects hosted on their personal GitHub — for example, Python Full Stack with Gen AI builds 10+ projects across Django, React, and Gen AI integrations. Projects are graded with code review feedback to make your portfolio interview-ready."),
            FaqItem(question="Can I join from outside Mughalsarai?", answer="Yes. All 14 courses are available as live online batches via Google Meet or Zoom — same instructor, same curriculum, same certificate as offline students in Mughalsarai. Students from Varanasi, Chandauli, Ghazipur, Ballia, Mirzapur, Bihar, and across India join online regularly."),
        ],
        stories=StoriesContent(
            section_title="What Our Students Say",
            section_subtext="Real students from Mughalsarai, Chandauli, Varanasi, and across eastern UP — sharing their Techpath experience.",
            items=[],
        ),
        offer_banner=OfferBannerContent(
            discount="Free Demo Class",
            savings="No Fees, No Obligation",
            target_date="",
            badge_text="🔥 NEW BATCH — Free Demo Available Offline + Online",
            benefits=[
                "Live instructor (not pre-recorded)",
                "Bilingual teaching — Hindi + English",
                "Small batches — max 25 students",
                "Real projects on your GitHub",
                "Resume + LinkedIn + Mock Interview support",
                "Weekend doubt sessions",
                "30-day money-back guarantee",
                "Course completion certificate",
            ],
        ),
        schema_defaults=SchemaDefaults(
            name="Techpath Academy",
            description="IT training institute in Mughalsarai, Chandauli — 14 courses including Python, Data Science, Gen AI, Full Stack, DevOps, IoT, and Digital Marketing. Offline + Live Online batches.",
            rating_value="",
            review_count="",
        ),
        cta=CtaContent(
            title="Ready to Start Your Tech Career?",
            description="Talk to our academic counsellor — free, no obligation, in Hindi or English. We'll help you pick the right course based on your background and goals.",
            primary_button=CtaButton(label="📞 Call +91 8299708052", href="tel:+918299708052"),
            secondary_button=CtaButton(label="💬 WhatsApp Us", href="https://wa.me/918299708052?text=Hi%2C%20I%20want%20free%20career%20counselling%20at%20Techpath%20Mughalsarai."),
        ),
    )
    return content.model_dump()


def get_builtin_home_content() -> dict[str, Any]:
    """Return default home page content for Techpath."""
    content = HomeLandingContent(
        seo=PageSeoContent(
            title="Techpath — IT Training in Mughalsarai + Enterprise AI & IT Services India",
            description="Techpath: 14 IT courses in Mughalsarai (offline + live online) and enterprise AI, cloud, web, and DevOps services. 50,000+ students trained. 150+ projects delivered.",
            image="/images/homepage-featured.jpg",
            canonical_url="https://techpath.biz/",
            no_index=False,
        ),
        hero=HomeHeroContent(
            badge_text="Training + Enterprise IT Services — Now with GenAI",
            headline="AI-Powered IT Solutions for",
            headline_highlight="Modern Enterprises",
            subheadline="Techpath delivers enterprise AI, cloud, and software solutions for businesses — and hands-on IT training courses for students in Mughalsarai and online across India. Two ways we can help. One team you can trust.",
            primary_cta_label="Start Your Project",
            primary_cta_href="/contact",
            secondary_cta_label="Explore Courses",
            secondary_cta_href="/training",
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
            HomeFeatureItem(title="Enterprise-grade security", description="SOC 2 Type II compliant. End-to-end encryption. Zero breaches in 6 years.", icon="shield"),
            HomeFeatureItem(title="Senior-only team", description="Average 10+ years experience. No outsourcing, no juniors on client projects.", icon="users"),
            HomeFeatureItem(title="Scales 100× without rewrites", description="Same architecture from startup to enterprise. Auto-scaling, 99.99% uptime.", icon="scale"),
            HomeFeatureItem(title="Ship every two weeks", description="Continuous delivery, not waterfall surprises. 2-week sprints, demos every cycle.", icon="rocket"),
        ],
        testimonials=[
            HomeTestimonialItem(quote="TechPath built our entire booking platform from scratch. Traveller sign-ups jumped 3× within 60 days of launch.", author="Ghanshyam", role="Founder & CEO", company="Himalayan Tripsters", logo="/images/trusted/himalayan-tripsters.png"),
            HomeTestimonialItem(quote="Our patient management system went live in 8 weeks. Staff productivity improved and patient wait times dropped by 40%.", author="Dr. Priya Sharma", role="Director of Operations", company="Octavia Hospital", logo="/images/trusted/octavia-hospital.png"),
            HomeTestimonialItem(quote="The AI-powered SEO dashboard TechPath delivered gives us insights our competitors simply don't have. Game-changing work.", author="Rob Lowson", role="Head of Growth", company="Digital Assassin", logo="/images/trusted/digital-assassin.png"),
            HomeTestimonialItem(quote="TechPath modernised our entire member management system. Renewals are now automated and our team saves 20+ hours a week.", author="Sandeep Talwalkar", role="Managing Director", company="Talwalkar Square", logo="/images/trusted/talwalkar-square.png"),
            HomeTestimonialItem(quote="From discovery to deployment in under 10 weeks. The team understood our domain deeply and delivered a rock-solid platform.", author="Saurabh Maurya", role="Founder", company="NREM", logo="/images/trusted/nrem.png"),
            HomeTestimonialItem(quote="Our AI assistant now handles 70% of customer queries autonomously. TechPath's integration work was seamless and well-documented.", author="Sanjeev Kumar", role="Product Lead", company="Conwerz AI", logo="/images/trusted/conwerz-ai.png"),
            HomeTestimonialItem(quote="TechPath built our event and travel booking portal end-to-end. Booking volume doubled in the first quarter post-launch.", author="Sravan Mishra", role="CEO", company="Global Events Travels", logo="/images/trusted/global-events-travels.png"),
        ],
        faqs=[
            FaqItem(question="What industries does Techpath specialise in?", answer="Techpath Professional Services works across healthcare, finance, retail, travel, and technology. We've delivered systems for Octavia Hospital, Himalayan Tripsters, Talwalkar Square, and more. Solutions are tailored to industry-specific requirements and compliance standards including ISO 27001 and DPDPA."),
            FaqItem(question="How long does a typical project take?", answer="A typical MVP takes 8–12 weeks. Enterprise solutions take 4–6 months. Every engagement starts with a free 30-minute strategy call and a written scope delivered within 48 hours — so you know exactly what you're getting before work begins."),
            FaqItem(question="Do you offer ongoing support after the project is delivered?", answer="Yes. Techpath offers 24/7 post-launch support packages covering monitoring, security patches, performance optimisation, and updates. Our team stays with you after go-live — not just until delivery."),
            FaqItem(question="What is Techpath's development methodology?", answer="We follow Agile with 2-week sprints and a demo at the end of every sprint. You see working software every 14 days — not a progress report. This keeps projects on track and lets you course-correct in real time."),
            FaqItem(question="Does Techpath offer IT training courses as well as services?", answer="Yes. Techpath Academy offers 14 IT training courses — from Python and Full-Stack Web Development to Data Science, Gen AI, DevOps, IoT, and Digital Marketing — available offline in Mughalsarai and live online across India. Courses start from ₹6,000 with EMI options available."),
            FaqItem(question="Can students from outside Mughalsarai join Techpath courses?", answer="Yes. All 14 courses are available as live online batches via Google Meet or Zoom — same instructor, same curriculum, same certificate as offline students. Students from Varanasi, Ghazipur, Ballia, Bihar, and across India join online. Call or WhatsApp +91 8299708052 to enrol."),
        ],
        cta=HomeCtaContent(
            title="Let's scope your project in 30 minutes.",
            description="Free strategy call. No pitch deck, no obligation — just a senior engineer reviewing your problem and telling you what's actually buildable.",
            primary_label="Book a Free Strategy Call",
            primary_href="/contact",
            secondary_label="See case studies",
            secondary_href="/case-studies",
        ),
    )
    return content.model_dump()


def get_builtin_about_content() -> dict[str, Any]:
    """Return default about page content for Techpath Mughalsarai."""
    content = AboutPageContent(
        seo=PageSeoContent(
            title="About Techpath | IT Training + Professional IT Services — Mughalsarai, Chandauli",
            description="Techpath Research and Development Pvt Ltd — IT training institute and enterprise IT services company in Mughalsarai, Chandauli, UP. 50,000+ students trained. 150+ projects delivered.",
            image="/images/about-featured.jpg",
            canonical_url="https://techpath.biz/about/",
            no_index=False,
        ),
        hero=AboutHeroContent(
            title="We Build Tech. We Build the People Who Do.",
            title_highlight="People Who Do",
            subheadline="Techpath Research and Development Pvt Ltd is two things at once — an IT training institute turning students into job-ready professionals in Mughalsarai, and a professional IT services company delivering AI, cloud, and software solutions for enterprises across India and globally.",
        ),
        mission_title="Our Mission",
        mission_text="To make world-class technology education and enterprise IT solutions accessible from eastern Uttar Pradesh — and beyond. We believe that where you are from should never limit what you can build. From Circus Road, Mughalsarai, we train the next generation of Indian tech professionals and deliver production-grade AI, cloud, and software solutions to businesses that demand results.",
        stats=[
            HomeStatItem(value="50,000+", label="Students Trained"),
            HomeStatItem(value="150+", label="Projects Delivered"),
            HomeStatItem(value="94%", label="Placement Rate"),
            HomeStatItem(value="98%", label="Client Satisfaction"),
        ],
        arms=[
            AboutArmItem(
                title="Techpath Academy",
                subtitle="IT Training Institute",
                description="Offline classes at Circus Road, Mughalsarai and live online batches for students across India. 14 courses from Computer Fundamentals to Python Full Stack with Gen AI. Small batches of max 25 students. Bilingual instruction in Hindi and English. 94% placement rate within 90 days of course completion.",
                href="/training/",
                cta_label="Explore All Courses",
                stats=[
                    HomeStatItem(value="50,000+", label="Students Trained"),
                    HomeStatItem(value="14", label="Courses"),
                    HomeStatItem(value="94%", label="Placement Rate"),
                    HomeStatItem(value="₹6,000", label="Starting Price"),
                ],
            ),
            AboutArmItem(
                title="Techpath Professional Services",
                subtitle="Enterprise IT Services",
                description="AI/ML, cloud infrastructure, custom web development, data analytics, DevOps, mobile apps, and cybersecurity for Indian enterprises and global clients. Senior-only team averaging 10+ years experience. 2-week sprint delivery. SOC 2 Type II compliant. 4.9 on Clutch.",
                href="/services/",
                cta_label="Explore All Services",
                stats=[
                    HomeStatItem(value="150+", label="Projects Delivered"),
                    HomeStatItem(value="50+", label="Enterprise Clients"),
                    HomeStatItem(value="98%", label="Client Satisfaction"),
                    HomeStatItem(value="4.9 ★", label="Clutch Rating"),
                ],
            ),
        ],
        values=[
            AboutValueItem(title="Proof Over Promise", description="98% client satisfaction. 94% student placement rate. 4.9 on Clutch. Zero security breaches since 2019. We let results speak.", icon="trophy"),
            AboutValueItem(title="Accessible Excellence", description="World-class IT training from ₹6,000. Enterprise-grade software built from Mughalsarai. Geography is not a barrier here.", icon="globe"),
            AboutValueItem(title="Senior-Only Delivery", description="No outsourcing. No juniors on client projects. Average 10+ years of experience across our engineering team.", icon="star"),
            AboutValueItem(title="Radical Transparency", description="Fixed-scope estimates. 2-week sprint demos. Honest assessments — we tell you straight if something isn't buildable.", icon="eye"),
        ],
        trusted_by=[
            AboutTrustedByItem(name="Himalayan Tripsters", logo="/images/trusted/himalayan-tripsters.png"),
            AboutTrustedByItem(name="Octavia Hospital", logo="/images/trusted/octavia-hospital.png"),
            AboutTrustedByItem(name="Digital Assassin", logo="/images/trusted/digital-assassin.png"),
            AboutTrustedByItem(name="Talwalkar Square", logo="/images/trusted/talwalkar-square.png"),
            AboutTrustedByItem(name="NREM", logo="/images/trusted/nrem.png"),
            AboutTrustedByItem(name="Conwerz AI", logo="/images/trusted/conwerz-ai.png"),
            AboutTrustedByItem(name="Global Events Travels", logo="/images/trusted/global-events-travels.png"),
        ],
        team=[
            AboutTeamMember(
                name="Sanjeev Kumar",
                role="Head of Solutions",
                bio="14 years of experience in IT solutions and software delivery. Leads all client strategy, project scoping, and solution architecture at Techpath Professional Services.",
                image="/team/sanjeev-ceo-techpath.png",
            ),
        ],
        cta_title="Ready to Start — as a Student or as a Business?",
        cta_description="Free career counselling for students. Free 30-minute strategy call for businesses. Talk to us — in Hindi or English, no obligation.",
        cta_primary_label="Contact Us",
        cta_primary_href="/contact",
        cta_secondary_label="View Our Work",
        cta_secondary_href="/case-studies",
    )
    return content.model_dump()


def get_builtin_services_content() -> dict[str, Any]:
    """Return default services landing page content."""
    content = ServicesLandingContent(
        seo=PageSeoContent(
            title="IT Services | AI, Cloud, Web Development & More — Techpath Research and Development",
            description="Techpath delivers AI/ML, cloud infrastructure, custom web development, data analytics, DevOps, mobile apps, and cybersecurity for Indian enterprises and global clients.",
            image="/images/services-featured.jpg",
            canonical_url="https://techpath.biz/services/",
            no_index=False,
        ),
        hero=ServicesHeroContent(
            title="Our Services",
            title_highlight="Services",
            subheadline="AI, cloud, web, data, DevOps, mobile, and cybersecurity — end-to-end technology services for Indian enterprises and global teams. Senior-only engineers. 2-week sprints. 150+ projects delivered.",
        ),
        trust_bar=[
            HomeStatItem(value="150+", label="Projects Delivered"),
            HomeStatItem(value="98%", label="Client Satisfaction"),
            HomeStatItem(value="50+", label="Enterprise Clients"),
            HomeStatItem(value="4.9 ★", label="Clutch Rating"),
            HomeStatItem(value="0", label="Breaches Since 2019"),
        ],
        cta_title="Need a Custom Solution?",
        cta_description="Talk to Sanjeev Kumar, our Head of Solutions — 14 years experience, no sales rep, no pitch deck. Free 30-minute strategy call. Written scope and estimate within 48 hours.",
        cta_primary_label="Book a Free Strategy Call",
        cta_primary_href="/contact",
        cta_secondary_label="View Pricing",
        cta_secondary_href="/pricing",
    )
    return content.model_dump()


def get_builtin_contact_content() -> dict[str, Any]:
    """Return default contact page content for Techpath Mughalsarai."""
    content = ContactPageContent(
        seo=PageSeoContent(
            title="Contact Techpath | IT Training & Professional IT Services — Mughalsarai, Chandauli",
            description="Contact Techpath — IT training courses in Mughalsarai + enterprise AI, web, and cloud services. Call, WhatsApp, or visit Circus Road. Free demo class & free strategy call.",
            image="/images/contact-featured.jpg",
            canonical_url="https://techpath.biz/contact/",
            no_index=False,
        ),
        hero=ContactHeroContent(
            title="Two Ways Techpath Can Help You",
            title_highlight="Help You",
            subheadline="Looking to start an IT career? Or build enterprise technology? Either way — reach out. Free career counselling for students. Free strategy call for businesses.",
            badges=[
                ContactBadge(label="📍 Circus Road, Mughalsarai", href="https://share.google/orP0Vj2FvrJEvLSSW"),
                ContactBadge(label="🎓 14 IT Courses", href="https://techpath.biz/training/"),
                ContactBadge(label="💼 7 Professional Services", href="https://techpath.biz/services/"),
                ContactBadge(label="4.9 ⭐ on Clutch", href="https://clutch.co"),
            ],
        ),
        contact_tabs=[
            ContactTab(
                id="academy",
                label="🎓 I'm a Student / Parent",
                headline="Talk to Our Academic Counsellor",
                subtext="Free career guidance — in Hindi or English. No pressure, no obligation.",
                cta_primary=ContactTabCta(label="📞 Call Now: +91 8299708052", href="tel:+918299708052"),
                cta_secondary=ContactTabCta(label="💬 WhatsApp Us", href="https://wa.me/918299708052?text=Hi%2C%20I%20want%20free%20career%20counselling%20at%20Techpath%20Mughalsarai."),
                urgency="🔥 Free Demo Class — No Fees, No Obligation (Offline + Online)",
            ),
            ContactTab(
                id="services",
                label="💼 I Need IT Services",
                headline="Book a Free Strategy Call",
                subtext="Talk directly to Sanjeev Kumar, Head of Solutions (14 years experience). Written scope + estimate in 48 hours.",
                cta_primary=ContactTabCta(label="📞 Book Strategy Call", href="tel:+918299708052"),
                cta_secondary=ContactTabCta(label="✉️ Email info@techpath.biz", href="mailto:info@techpath.biz"),
                urgency="3 strategy slots open this week — NDA on request, no pitch deck, no obligation",
            ),
        ],
        contact_methods=[
            ContactMethodItem(
                title="Call or WhatsApp",
                description="Mon–Sat, 9 AM to 7 PM. WhatsApp support available on Sundays for enrolled students.",
                value="+91 8299708052",
                href="tel:+918299708052",
                icon="phone",
                secondary_action=ContactSecondaryAction(
                    label="💬 Open WhatsApp",
                    href="https://wa.me/918299708052?text=Hi%2C%20I%20want%20to%20know%20more%20about%20Techpath.",
                ),
            ),
            ContactMethodItem(
                title="Email Us",
                description="We reply within 48 business hours.",
                value="info@techpath.biz",
                href="mailto:info@techpath.biz",
                icon="email",
                note="For privacy or legal queries: privacy@techpath.biz | legal@techpath.biz",
            ),
            ContactMethodItem(
                title="Visit Our Centre",
                description="Walk in Mon–Sat, 9 AM–7 PM. No appointment needed. Walking distance from DDU Junction.",
                value="Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101",
                href="https://share.google/orP0Vj2FvrJEvLSSW",
                icon="location",
                map_label="Get Directions on Google Maps",
                landmark="Near DDU Junction (Pandit Deen Dayal Upadhyaya Nagar Railway Station)",
            ),
        ],
        office_hours=OfficeHours(
            weekdays="Monday to Saturday — 9:00 AM to 7:00 PM",
            sunday="WhatsApp support for enrolled students only",
            note="Walk-ins welcome. Free career counselling available on the spot — no prior appointment needed.",
        ),
        batch_timings=[
            BatchTiming(label="Morning Batch", time="9:00 AM – 11:00 AM", days="Mon–Sat"),
            BatchTiming(label="Afternoon Batch", time="1:00 PM – 3:00 PM", days="Mon–Sat"),
            BatchTiming(label="Evening Batch", time="5:00 PM – 7:00 PM", days="Mon–Sat"),
            BatchTiming(label="Weekend Doubt Sessions", time="Saturday & Sunday", days="Enrolled students"),
        ],
        delivery_modes=[
            DeliveryMode(
                id="offline",
                label="Offline — Mughalsarai Centre",
                description="Attend in person at Circus Road, Mughalsarai — walking distance from DDU Junction, Chandauli. Small batches of max 25 students. Lab access, face-to-face doubt clearing.",
                icon="building",
            ),
            DeliveryMode(
                id="online",
                label="Live Online — From Anywhere in India",
                description="Join from Varanasi, Ghazipur, Ballia, Bihar, or anywhere in India via Google Meet or Zoom. Same instructor, same curriculum, same certificate. Not pre-recorded — fully live and interactive.",
                icon="globe",
            ),
        ],
        what_to_expect=WhatToExpect(
            academy=[
                WhatToExpectStep(step=1, label="WhatsApp or call us", detail="Tell us your background and the course you're interested in."),
                WhatToExpectStep(step=2, label="Free demo class", detail="Attend one free class — offline or online. Zero fees, zero obligation."),
                WhatToExpectStep(step=3, label="Enrol & pick your batch", detail="Choose morning, afternoon, or evening batch. EMI available."),
                WhatToExpectStep(step=4, label="Start building your career", detail="Real projects, live instructor, placement support from day one."),
            ],
            services=[
                WhatToExpectStep(step=1, label="Email or call us", detail="We respond within 4 hours on business days."),
                WhatToExpectStep(step=2, label="30-min strategy call", detail="Talk to Sanjeev Kumar directly — senior engineer, not a sales rep."),
                WhatToExpectStep(step=3, label="Written scope + estimate", detail="Delivered within 48 hours. NDA available on request."),
                WhatToExpectStep(step=4, label="Discovery → Build → Ship", detail="2-week sprints. First demo in 14 days. On-time, every time."),
            ],
        ),
        faq=[
            FaqItem(question="Where is Techpath located?", answer="Techpath is located on Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101 — walking distance from DDU Junction (Pandit Deen Dayal Upadhyaya Nagar railway station). We are open Monday to Saturday, 9 AM to 7 PM. Walk-ins are welcome — no appointment needed."),
            FaqItem(question="Can I join a Techpath course if I am not in Mughalsarai?", answer="Yes. All 14 Techpath courses are available as live online batches via Google Meet or Zoom — same instructor, same curriculum, same timings, same certificate. Students from Varanasi, Ghazipur, Ballia, Mirzapur, and Bihar join online regularly. Fees are identical for both modes."),
            FaqItem(question="Is there a free demo class before I enrol?", answer="Yes — Techpath offers a free demo class for every course, both offline and online. No fees, no obligation, no pressure. Call or WhatsApp +91 8299708052 to book your free demo class today."),
            FaqItem(question="What are Techpath's batch timings?", answer="Techpath runs three daily batches Monday to Saturday: Morning (9–11 AM), Afternoon (1–3 PM), and Evening (5–7 PM). Weekend doubt sessions are available for all enrolled students. You can switch batches if your schedule changes."),
            FaqItem(question="Does Techpath offer IT services for businesses or only training?", answer="Techpath operates two arms. Techpath Academy offers 14 IT training courses for students and professionals. Techpath Professional Services offers enterprise-grade AI/ML, cloud infrastructure, web development, data analytics, DevOps, mobile apps, and cybersecurity services for businesses. Call +91 8299708052 or email info@techpath.biz for a free strategy call."),
            FaqItem(question="Techpath mein admission kaise lein Mughalsarai mein?", answer="Techpath Mughalsarai mein admission ke liye aap seedha Circus Road centre par aa sakte hain ya WhatsApp kar sakte hain — +91 8299708052 par. Pehle ek free demo class attend karein, phir apna batch choose karein (morning, afternoon, ya evening). EMI bhi available hai sabhi courses ke liye."),
            FaqItem(question="How quickly does Techpath respond to business enquiries?", answer="For professional services enquiries, Techpath responds within 4 hours on business days. Email info@techpath.biz or call +91 8299708052. A written project scope and estimate is delivered within 48 hours of your strategy call."),
        ],
        social_proof=ContactSocialProof(
            academy=ContactSocialProofSection(
                stats=[
                    ContactStatItem(value="50,000+", label="Students Trained"),
                    ContactStatItem(value="94%", label="Placement Rate"),
                    ContactStatItem(value="25", label="Max Batch Size"),
                    ContactStatItem(value="14", label="Courses Available"),
                ],
            ),
            services=ContactSocialProofSection(
                stats=[
                    ContactStatItem(value="150+", label="Projects Delivered"),
                    ContactStatItem(value="98%", label="Client Satisfaction"),
                    ContactStatItem(value="50+", label="Enterprise Clients"),
                    ContactStatItem(value="4.9", label="Clutch Rating"),
                ],
                head_of_solutions=HeadOfSolutions(
                    name="Sanjeev Kumar",
                    role="Head of Solutions · 14yr experience",
                    quote="You'll talk to me, not a sales rep. I'll tell you straight if we can help.",
                    image="/team/sanjeev-ceo-techpath.png",
                ),
            ),
        ),
        cta_block=ContactCtaBlock(
            academy=ContactCtaItem(
                headline="Not Sure Which Course Is Right for You?",
                subtext="Our academic counsellor will guide you — free, in Hindi or English, no obligation.",
                primary=ContactTabCta(label="📞 Call Now: +91 8299708052", href="tel:+918299708052"),
                secondary=ContactTabCta(label="💬 WhatsApp Us", href="https://wa.me/918299708052?text=Hi%2C%20I%20want%20free%20career%20counselling%20at%20Techpath%20Mughalsarai."),
                urgency="🔥 Free Demo Class — No Fees, No Obligation (Offline + Online)",
            ),
            services=ContactCtaItem(
                headline="Let's Scope Your Project in 30 Minutes",
                subtext="Free strategy call. No pitch deck, no obligation — just a senior engineer reviewing your problem.",
                primary=ContactTabCta(label="📞 Book a Call: +91 8299708052", href="tel:+918299708052"),
                secondary=ContactTabCta(label="✉️ Email info@techpath.biz", href="mailto:info@techpath.biz"),
                urgency="3 strategy slots open this week — reply within 4 hours guaranteed",
            ),
        ),
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
