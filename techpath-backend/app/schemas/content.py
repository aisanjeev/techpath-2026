"""
Pydantic schemas for public content API (e.g. training landing page).
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class TrustBadge(BaseModel):
    icon: str = ""
    value: str = ""
    label: str = ""


class CtaButton(BaseModel):
    label: str = ""
    href: str = ""


class HeroContent(BaseModel):
    title: str = "Master In-Demand Tech Skills"
    subtitle: str = "Live instructor training + Real-world projects + Job guarantee + 100% money back"
    headline_subline: str = "Land High-Paying Jobs in 90 Days"
    badge_text: str = "New Batch Starting Feb 2026"
    primary_cta: CtaButton = Field(default_factory=lambda: CtaButton(label="Start Free Trial", href="#enroll"))
    secondary_cta: CtaButton = Field(default_factory=lambda: CtaButton(label="View Course Catalog", href="#courses"))
    trust_badges: List[TrustBadge] = Field(default_factory=list)


class PainPointItem(BaseModel):
    icon: str = ""
    title: str = ""
    description: str = ""
    color: str = "text-red-400"
    bg_color: str = "bg-red-500/10"
    border_color: str = "border-red-500/30"


class PainPointsContent(BaseModel):
    section_title: str = "Stuck Without a Clear Tech Career Path?"
    section_subtext: str = "You're not alone. Thousands face these same challenges every day."
    transition_text: str = "Good news: There's a better way to break into tech — without breaking the bank or wasting months on theory."
    items: List[PainPointItem] = Field(default_factory=list)


class UspItem(BaseModel):
    icon: str = ""
    title: str = ""
    highlights: List[str] = Field(default_factory=list)
    color: str = "from-primary-500 to-secondary-500"


class UspsContent(BaseModel):
    section_title: str = "Why Top Companies Choose TechPath Graduates"
    section_subtext: str = "We don't just teach — we transform careers with a proven methodology."
    items: List[UspItem] = Field(default_factory=list)


class FaqItem(BaseModel):
    question: str = ""
    answer: str = ""


class StoryItem(BaseModel):
    name: str = ""
    location: str = ""
    previous_role: str = ""
    current_role: str = ""
    previous_salary: str = ""
    current_salary: str = ""
    course: str = ""
    duration: str = ""
    quote: str = ""
    rating: int = 5
    has_video: bool = False


class StoriesContent(BaseModel):
    section_title: str = "Real Students. Real Transformations."
    section_subtext: str = "Join thousands who've changed their careers with TechPath"
    items: List[StoryItem] = Field(default_factory=list)


class OfferBannerContent(BaseModel):
    discount: str = "₹15,000 OFF"
    savings: str = "Save 30%"
    target_date: Optional[str] = None
    badge_text: str = "EARLY BIRD OFFER - Limited Time Only"
    benefits: List[str] = Field(default_factory=list)


class SchemaDefaults(BaseModel):
    name: str = "TechPath Training"
    description: str = "Online tech courses and certification programs with live instructor training"
    rating_value: str = "4.9"
    review_count: str = "2000"


class CtaContent(BaseModel):
    title: str = "Ready to Transform Your Career?"
    description: str = "Join 50,000+ students who've changed their lives with TechPath training."
    primary_button: CtaButton = Field(default_factory=lambda: CtaButton(label="Explore Courses", href="#courses"))
    secondary_button: CtaButton = Field(default_factory=lambda: CtaButton(label="Talk to Counselor", href="/contact"))


class PageSeoContent(BaseModel):
    """SEO meta for a page: title, description, optional og_image, canonical_url, no_index."""
    title: str = ""
    description: str = ""
    image: Optional[str] = None
    canonical_url: Optional[str] = None
    no_index: bool = False


class TrainingLandingContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: HeroContent = Field(default_factory=HeroContent)
    pain_points: PainPointsContent = Field(default_factory=PainPointsContent)
    usps: UspsContent = Field(default_factory=UspsContent)
    faqs: List[FaqItem] = Field(default_factory=list)
    stories: StoriesContent = Field(default_factory=StoriesContent)
    offer_banner: OfferBannerContent = Field(default_factory=OfferBannerContent)
    schema_defaults: SchemaDefaults = Field(default_factory=SchemaDefaults)
    cta: CtaContent = Field(default_factory=CtaContent)


# --- Home page ---


class HomeHeroContent(BaseModel):
    badge_text: str = "Now offering GenAI Solutions"
    headline: str = "AI-Powered IT Solutions for"
    headline_highlight: str = "Modern Enterprises"
    subheadline: str = "Transform your business with cutting-edge AI, cloud infrastructure, and custom software solutions. We help enterprises innovate faster and scale smarter."
    primary_cta_label: str = "Start Your Project"
    primary_cta_href: str = "/contact"
    secondary_cta_label: str = "Watch Demo"
    secondary_cta_href: str = "/case-studies"


class HomeServiceItem(BaseModel):
    title: str = ""
    description: str = ""
    icon: str = "code"
    href: str = ""


class HomeStatItem(BaseModel):
    value: str = ""
    label: str = ""


class HomeFeatureItem(BaseModel):
    title: str = ""
    description: str = ""
    icon: str = ""


class HomeTestimonialItem(BaseModel):
    quote: str = ""
    author: str = ""
    role: str = ""
    company: str = ""
    avatar: str = ""


class HomeCtaContent(BaseModel):
    title: str = "Ready to Transform Your Business?"
    description: str = "Let's discuss how our AI-powered solutions can drive your digital transformation."
    primary_label: str = "Get Started"
    primary_href: str = "/contact"
    secondary_label: str = "View Case Studies"
    secondary_href: str = "/case-studies"


class HomeCaseStudiesSection(BaseModel):
    section_title: str = "Featured Case Studies"
    section_subtitle: str = "Real stories of digital transformation. See how we've helped businesses achieve measurable results."
    limit: int = 6
    view_all_label: str = "View All Case Studies"
    view_all_href: str = "/case-studies"


class HomeLandingContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: HomeHeroContent = Field(default_factory=HomeHeroContent)
    stats: List[HomeStatItem] = Field(default_factory=list)
    services: List[HomeServiceItem] = Field(default_factory=list)
    case_studies_section: HomeCaseStudiesSection = Field(
        default_factory=HomeCaseStudiesSection
    )
    features: List[HomeFeatureItem] = Field(default_factory=list)
    testimonials: List[HomeTestimonialItem] = Field(default_factory=list)
    faqs: List[FaqItem] = Field(default_factory=list)
    cta: HomeCtaContent = Field(default_factory=HomeCtaContent)


# --- About page ---


class AboutHeroContent(BaseModel):
    title: str = "Building the Future of Technology"
    title_highlight: str = "Future"
    subheadline: str = "We're a team of passionate technologists dedicated to helping businesses harness the power of AI, cloud computing, and modern software development."


class AboutValueItem(BaseModel):
    title: str = ""
    description: str = ""
    icon: str = ""


class AboutTeamMember(BaseModel):
    name: str = ""
    role: str = ""
    bio: str = ""
    image: str = ""


class AboutPageContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: AboutHeroContent = Field(default_factory=AboutHeroContent)
    mission_title: str = "Our Mission"
    mission_text: str = "To democratize access to cutting-edge technology solutions, enabling businesses of all sizes to compete and thrive in the digital age. We believe that the right technology, implemented thoughtfully, can transform industries and improve lives."
    stats: List[HomeStatItem] = Field(default_factory=list)
    values: List[AboutValueItem] = Field(default_factory=list)
    team: List[AboutTeamMember] = Field(default_factory=list)
    cta_title: str = "Ready to Build Something Great?"
    cta_description: str = "Let's discuss how we can help you achieve your technology goals."
    cta_primary_label: str = "Get in Touch"
    cta_primary_href: str = "/contact"
    cta_secondary_label: str = "View Our Work"
    cta_secondary_href: str = "/case-studies"


# --- Services landing page ---


class ServicesHeroContent(BaseModel):
    title: str = "Our Services"
    title_highlight: str = "Services"
    subheadline: str = "From AI-powered solutions to cloud infrastructure, we provide end-to-end technology services that drive business growth and innovation."


class ServicesLandingContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: ServicesHeroContent = Field(default_factory=ServicesHeroContent)
    cta_title: str = "Need a Custom Solution?"
    cta_description: str = "Let's discuss your unique requirements and build something amazing together."
    cta_primary_label: str = "Contact Us"
    cta_primary_href: str = "/contact"
    cta_secondary_label: str = "View Pricing"
    cta_secondary_href: str = "/pricing"


# --- Contact page ---


class ContactHeroContent(BaseModel):
    title: str = "Let's Talk"
    title_highlight: str = "Talk"
    subheadline: str = "Have a project in mind? We'd love to hear about it. Get in touch and let's create something amazing together."


class ContactMethodItem(BaseModel):
    title: str = ""
    description: str = ""
    value: str = ""
    href: str = ""
    icon: str = ""


class ContactPageContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: ContactHeroContent = Field(default_factory=ContactHeroContent)
    contact_methods: List[ContactMethodItem] = Field(default_factory=list)


# --- Pricing page ---


class PricingHeroContent(BaseModel):
    title: str = "Simple, Transparent Pricing"
    title_highlight: str = "Pricing"
    subheadline: str = "Choose the plan that fits your needs. All plans include our commitment to quality and your success."


class PricingPlanItem(BaseModel):
    name: str = ""
    description: str = ""
    price: str = ""
    period: str = ""
    features: List[str] = Field(default_factory=list)
    cta: str = "Get Started"
    highlighted: bool = False


class PricingPageContent(BaseModel):
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    hero: PricingHeroContent = Field(default_factory=PricingHeroContent)
    plans: List[PricingPlanItem] = Field(default_factory=list)
    faq_section_title: str = "Frequently Asked Questions"
    faqs: List[FaqItem] = Field(default_factory=list)
    cta_title: str = "Need a Custom Quote?"
    cta_description: str = "Every project is unique. Let's discuss your specific requirements."
    cta_primary_label: str = "Schedule a Call"
    cta_primary_href: str = "/contact"
    cta_secondary_label: str = "View Services"
    cta_secondary_href: str = "/services"


# --- Policy pages (Privacy, Terms, Cookie) - content as markdown ---


class PolicyPageContent(BaseModel):
    """SEO + page title + last_updated + markdown body for legal/policy pages."""
    seo: PageSeoContent = Field(default_factory=PageSeoContent)
    page_title: str = ""
    last_updated: str = ""
    markdown_content: str = ""
