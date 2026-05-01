/**
 * Page content from API (GET /api/v1/content/{page}).
 * Fallback to inline default when API fails.
 */

const API_BASE =
  typeof import.meta.env !== 'undefined' && import.meta.env.PUBLIC_API_URL
    ? import.meta.env.PUBLIC_API_URL
    : 'http://localhost:8000';

// --- Shared SEO (from content API) ---

export interface PageSeoContent {
  title: string;
  description: string;
  image?: string | null;
  canonical_url?: string | null;
  no_index?: boolean;
}

// --- Home page ---

export interface HomeLandingContent {
  seo?: PageSeoContent;
  hero: {
    badge_text: string;
    headline: string;
    headline_highlight: string;
    subheadline: string;
    primary_cta_label: string;
    primary_cta_href: string;
    secondary_cta_label: string;
    secondary_cta_href: string;
  };
  stats: Array<{ value: string; label: string }>;
  services: Array<{ title: string; description: string; icon: string; href: string }>;
  case_studies_section?: {
    section_title: string;
    section_subtitle: string;
    limit?: number;
    view_all_label: string;
    view_all_href: string;
  };
  features: Array<{ title: string; description: string; icon: string }>;
  testimonials: Array<{
    quote: string;
    author: string;
    role: string;
    company: string;
    avatar: string;
  }>;
  faqs: Array<{ question: string; answer: string }>;
  cta: {
    title: string;
    description: string;
    primary_label: string;
    primary_href: string;
    secondary_label: string;
    secondary_href: string;
  };
}

function getDefaultHomeContent(): HomeLandingContent {
  return {
    seo: {
      title: 'AI-Powered IT Solutions',
      description:
        'TechPath delivers enterprise-grade AI solutions, cloud infrastructure, and custom software development for modern businesses.',
    },
    hero: {
      badge_text: 'Now offering GenAI Solutions',
      headline: 'AI-Powered IT Solutions for',
      headline_highlight: 'Modern Enterprises',
      subheadline:
        'Transform your business with cutting-edge AI, cloud infrastructure, and custom software solutions.',
      primary_cta_label: 'Start Your Project',
      primary_cta_href: '/contact',
      secondary_cta_label: 'Watch Demo',
      secondary_cta_href: '/case-studies',
    },
    stats: [
      { value: '150+', label: 'Projects Delivered' },
      { value: '98%', label: 'Client Satisfaction' },
      { value: '50+', label: 'Enterprise Clients' },
      { value: '24/7', label: 'Support Available' },
    ],
    services: [
      { title: 'AI & Machine Learning', description: 'Custom AI solutions powered by cutting-edge machine learning models.', icon: 'brain', href: '/services/ai-consulting' },
      { title: 'Cloud Infrastructure', description: 'Scalable cloud architecture on AWS, Azure, and Google Cloud.', icon: 'cloud', href: '/services/cloud-services' },
      { title: 'Web Development', description: 'Modern, performant web applications built with latest technologies.', icon: 'code', href: '/services/web-development' },
      { title: 'Data Analytics', description: 'Transform your data into actionable business insights.', icon: 'chart', href: '/services/data-analytics' },
    ],
    case_studies_section: {
      section_title: 'Featured Case Studies',
      section_subtitle: "Real stories of digital transformation. See how we've helped businesses achieve measurable results.",
      limit: 6,
      view_all_label: 'View All Case Studies',
      view_all_href: '/case-studies',
    },
    features: [
      { title: 'Enterprise-Grade Security', description: 'SOC 2 compliant infrastructure with end-to-end encryption.', icon: 'shield' },
      { title: 'Scalable Architecture', description: 'Built to grow with your business from startup to enterprise.', icon: 'scale' },
      { title: 'Expert Team', description: 'Senior engineers with 10+ years of industry experience.', icon: 'users' },
      { title: 'Agile Delivery', description: 'Rapid iteration with continuous integration and deployment.', icon: 'rocket' },
    ],
    testimonials: [
      { quote: 'TechPath transformed our legacy systems into a modern, AI-powered platform. The results exceeded our expectations.', author: 'Sarah Chen', role: 'CTO', company: 'FinanceFlow Inc.', avatar: '/images/testimonials/sarah.jpg' },
      { quote: 'Their expertise in cloud migration saved us 40% on infrastructure costs while improving performance.', author: 'Michael Roberts', role: 'VP Engineering', company: 'RetailMax', avatar: '/images/testimonials/michael.jpg' },
      { quote: 'The team delivered our AI chatbot ahead of schedule. Customer satisfaction improved by 35%.', author: 'Emily Watson', role: 'Director of Operations', company: 'HealthTech Solutions', avatar: '/images/testimonials/emily.jpg' },
    ],
    faqs: [
      { question: 'What industries do you specialize in?', answer: 'We work across multiple industries including healthcare, finance, retail, and technology. Our solutions are tailored to meet specific industry requirements and compliance standards.' },
      { question: 'How long does a typical project take?', answer: 'Project timelines vary based on scope and complexity. A typical MVP takes 8-12 weeks, while enterprise solutions may take 4-6 months. We provide detailed timelines during our initial consultation.' },
      { question: 'Do you offer ongoing support and maintenance?', answer: 'Yes, we offer 24/7 support packages including monitoring, updates, security patches, and performance optimization. Our team ensures your systems run smoothly post-launch.' },
      { question: 'What is your development methodology?', answer: 'We follow Agile methodology with 2-week sprints, regular demos, and continuous feedback loops. This ensures transparency and allows for quick adjustments based on your needs.' },
    ],
    cta: {
      title: 'Ready to Transform Your Business?',
      description: "Let's discuss how our AI-powered solutions can drive your digital transformation.",
      primary_label: 'Get Started',
      primary_href: '/contact',
      secondary_label: 'View Case Studies',
      secondary_href: '/case-studies',
    },
  };
}

export async function fetchHomePageContent(): Promise<HomeLandingContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/home-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultHomeContent();
    const data = (await res.json()) as HomeLandingContent;
    return data;
  } catch {
    return getDefaultHomeContent();
  }
}

// --- About page ---

export interface AboutPageContent {
  seo?: PageSeoContent;
  hero: { title: string; title_highlight: string; subheadline: string };
  mission_title: string;
  mission_text: string;
  stats: Array<{ value: string; label: string }>;
  values: Array<{ title: string; description: string; icon: string }>;
  team: Array<{ name: string; role: string; bio: string; image: string }>;
  cta_title: string;
  cta_description: string;
  cta_primary_label: string;
  cta_primary_href: string;
  cta_secondary_label: string;
  cta_secondary_href: string;
}

function getDefaultAboutContent(): AboutPageContent {
  return {
    seo: {
      title: 'About Us',
      description:
        "Learn about TechPath's mission to deliver innovative AI and IT solutions. Meet our team of experts dedicated to your success.",
    },
    hero: {
      title: 'Building the Future of Technology',
      title_highlight: 'Future',
      subheadline:
        "We're a team of passionate technologists dedicated to helping businesses harness the power of AI, cloud computing, and modern software development.",
    },
    mission_title: 'Our Mission',
    mission_text:
      'To democratize access to cutting-edge technology solutions, enabling businesses of all sizes to compete and thrive in the digital age. We believe that the right technology, implemented thoughtfully, can transform industries and improve lives.',
    stats: [
      { value: '10+', label: 'Years Experience' },
      { value: '150+', label: 'Projects Completed' },
      { value: '50+', label: 'Team Members' },
      { value: '25+', label: 'Countries Served' },
    ],
    values: [
      { title: 'Innovation First', description: 'We embrace emerging technologies and creative solutions to solve complex problems.', icon: 'lightbulb' },
      { title: 'Client Success', description: 'Your success is our success. We measure ourselves by the impact we create for you.', icon: 'trophy' },
      { title: 'Transparency', description: 'Open communication and honest assessments are the foundation of our partnerships.', icon: 'eye' },
      { title: 'Excellence', description: 'We hold ourselves to the highest standards in code quality and delivery.', icon: 'star' },
    ],
    team: [
      { name: 'Alex Thompson', role: 'CEO & Founder', bio: '15+ years in tech leadership. Former VP Engineering at Fortune 500.', image: '/images/team/alex.jpg' },
      { name: 'Dr. Sarah Kim', role: 'Chief AI Officer', bio: 'PhD in Machine Learning. Published researcher with 50+ papers.', image: '/images/team/sarah.jpg' },
      { name: 'Marcus Chen', role: 'CTO', bio: 'Cloud architecture expert. AWS & Azure certified solutions architect.', image: '/images/team/marcus.jpg' },
      { name: 'Jessica Patel', role: 'VP of Engineering', bio: '12 years in full-stack development. Former tech lead at FAANG.', image: '/images/team/jessica.jpg' },
    ],
    cta_title: 'Ready to Build Something Great?',
    cta_description: "Let's discuss how we can help you achieve your technology goals.",
    cta_primary_label: 'Get in Touch',
    cta_primary_href: '/contact',
    cta_secondary_label: 'View Our Work',
    cta_secondary_href: '/case-studies',
  };
}

export async function fetchAboutPageContent(): Promise<AboutPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/about-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultAboutContent();
    const data = (await res.json()) as AboutPageContent;
    return data;
  } catch {
    return getDefaultAboutContent();
  }
}

// --- Services page ---

export interface ServicesLandingContent {
  seo?: PageSeoContent;
  hero: { title: string; title_highlight: string; subheadline: string };
  cta_title: string;
  cta_description: string;
  cta_primary_label: string;
  cta_primary_href: string;
  cta_secondary_label: string;
  cta_secondary_href: string;
}

function getDefaultServicesContent(): ServicesLandingContent {
  return {
    seo: {
      title: 'Our Services',
      description:
        "Explore TechPath's comprehensive IT services including AI solutions, cloud infrastructure, web development, and data analytics.",
    },
    hero: {
      title: 'Our Services',
      title_highlight: 'Services',
      subheadline:
        'From AI-powered solutions to cloud infrastructure, we provide end-to-end technology services that drive business growth and innovation.',
    },
    cta_title: 'Need a Custom Solution?',
    cta_description: "Let's discuss your unique requirements and build something amazing together.",
    cta_primary_label: 'Contact Us',
    cta_primary_href: '/contact',
    cta_secondary_label: 'View Pricing',
    cta_secondary_href: '/pricing',
  };
}

export async function fetchServicesPageContent(): Promise<ServicesLandingContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/services-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultServicesContent();
    const data = (await res.json()) as ServicesLandingContent;
    return data;
  } catch {
    return getDefaultServicesContent();
  }
}

// --- Contact page ---

export interface ContactBadge { label: string; href: string; }
export interface ContactTabCta { label: string; href: string; }
export interface ContactTab {
  id: string;
  label: string;
  headline: string;
  subtext: string;
  cta_primary: ContactTabCta;
  cta_secondary: ContactTabCta;
  urgency: string;
}
export interface ContactMethodItem {
  title: string;
  description: string;
  value: string;
  href: string;
  icon: string;
  secondary_action?: { label: string; href: string };
  note?: string;
  map_label?: string;
  landmark?: string;
}
export interface OfficeHours { weekdays: string; sunday: string; note: string; }
export interface BatchTiming { label: string; time: string; days: string; }
export interface DeliveryMode { id: string; label: string; description: string; icon: string; }
export interface WhatToExpectStep { step: number; label: string; detail: string; }
export interface ContactStatItem { value: string; label: string; }
export interface HeadOfSolutions { name: string; role: string; quote: string; image: string; }
export interface ContactSocialProofSection {
  stats: ContactStatItem[];
  head_of_solutions?: HeadOfSolutions;
}
export interface ContactCtaItem {
  headline: string;
  subtext: string;
  primary: ContactTabCta;
  secondary: ContactTabCta;
  urgency: string;
}

export interface ContactPageContent {
  seo?: PageSeoContent;
  hero: { title: string; title_highlight: string; subheadline: string; badges: ContactBadge[] };
  contact_tabs: ContactTab[];
  contact_methods: ContactMethodItem[];
  office_hours: OfficeHours;
  batch_timings: BatchTiming[];
  delivery_modes: DeliveryMode[];
  what_to_expect: { academy: WhatToExpectStep[]; services: WhatToExpectStep[] };
  faq: Array<{ question: string; answer: string }>;
  social_proof: { academy: ContactSocialProofSection; services: ContactSocialProofSection };
  cta_block: { academy: ContactCtaItem; services: ContactCtaItem };
}

function getDefaultContactContent(): ContactPageContent {
  return {
    seo: {
      title: 'Contact Techpath | IT Training & Professional IT Services — Mughalsarai, Chandauli',
      description: 'Contact Techpath — IT training courses in Mughalsarai + enterprise AI, web, and cloud services. Call, WhatsApp, or visit Circus Road.',
      canonical_url: 'https://techpath.biz/contact/',
    },
    hero: {
      title: 'Two Ways Techpath Can Help You',
      title_highlight: 'Help You',
      subheadline: 'Looking to start an IT career? Or build enterprise technology? Either way — reach out. Free career counselling for students. Free strategy call for businesses.',
      badges: [
        { label: '📍 Circus Road, Mughalsarai', href: 'https://share.google/orP0Vj2FvrJEvLSSW' },
        { label: '🎓 14 IT Courses', href: '/training/' },
        { label: '💼 7 Professional Services', href: '/services/' },
        { label: '4.9 ⭐ on Clutch', href: 'https://clutch.co' },
      ],
    },
    contact_tabs: [
      {
        id: 'academy',
        label: "🎓 I'm a Student / Parent",
        headline: 'Talk to Our Academic Counsellor',
        subtext: 'Free career guidance — in Hindi or English. No pressure, no obligation.',
        cta_primary: { label: '📞 Call Now: +91 8299708052', href: 'tel:+918299708052' },
        cta_secondary: { label: '💬 WhatsApp Us', href: 'https://wa.me/918299708052?text=Hi%2C%20I%20want%20free%20career%20counselling%20at%20Techpath%20Mughalsarai.' },
        urgency: '🔥 Free Demo Class — No Fees, No Obligation (Offline + Online)',
      },
      {
        id: 'services',
        label: '💼 I Need IT Services',
        headline: 'Book a Free Strategy Call',
        subtext: 'Talk directly to Sanjeev Kumar, Head of Solutions (14 years experience). Written scope + estimate in 48 hours.',
        cta_primary: { label: '📞 Book Strategy Call', href: 'tel:+918299708052' },
        cta_secondary: { label: '✉️ Email info@techpath.biz', href: 'mailto:info@techpath.biz' },
        urgency: '3 strategy slots open this week — NDA on request, no pitch deck, no obligation',
      },
    ],
    contact_methods: [
      { title: 'Call or WhatsApp', description: 'Mon–Sat, 9 AM to 7 PM. WhatsApp support available on Sundays for enrolled students.', value: '+91 8299708052', href: 'tel:+918299708052', icon: 'phone', secondary_action: { label: '💬 Open WhatsApp', href: 'https://wa.me/918299708052?text=Hi%2C%20I%20want%20to%20know%20more%20about%20Techpath.' } },
      { title: 'Email Us', description: 'We reply within 48 business hours.', value: 'info@techpath.biz', href: 'mailto:info@techpath.biz', icon: 'email', note: 'For privacy or legal queries: privacy@techpath.biz | legal@techpath.biz' },
      { title: 'Visit Our Centre', description: 'Walk in Mon–Sat, 9 AM–7 PM. No appointment needed. Walking distance from DDU Junction.', value: 'Circus Road, Mughalsarai, Chandauli, UP 232101', href: 'https://share.google/orP0Vj2FvrJEvLSSW', icon: 'location', map_label: 'Get Directions on Google Maps', landmark: 'Near DDU Junction (Pandit Deen Dayal Upadhyaya Nagar Railway Station)' },
    ],
    office_hours: { weekdays: 'Monday to Saturday — 9:00 AM to 7:00 PM', sunday: 'WhatsApp support for enrolled students only', note: 'Walk-ins welcome. Free career counselling available on the spot — no prior appointment needed.' },
    batch_timings: [
      { label: 'Morning Batch', time: '9:00 AM – 11:00 AM', days: 'Mon–Sat' },
      { label: 'Afternoon Batch', time: '1:00 PM – 3:00 PM', days: 'Mon–Sat' },
      { label: 'Evening Batch', time: '5:00 PM – 7:00 PM', days: 'Mon–Sat' },
      { label: 'Weekend Doubt Sessions', time: 'Saturday & Sunday', days: 'Enrolled students' },
    ],
    delivery_modes: [
      { id: 'offline', label: 'Offline — Mughalsarai Centre', description: 'Attend in person at Circus Road, Mughalsarai — walking distance from DDU Junction, Chandauli. Small batches of max 25 students. Lab access, face-to-face doubt clearing.', icon: 'building' },
      { id: 'online', label: 'Live Online — From Anywhere in India', description: 'Join from Varanasi, Ghazipur, Ballia, Bihar, or anywhere in India via Google Meet or Zoom. Same instructor, same curriculum, same certificate. Not pre-recorded — fully live and interactive.', icon: 'globe' },
    ],
    what_to_expect: {
      academy: [
        { step: 1, label: 'WhatsApp or call us', detail: "Tell us your background and the course you're interested in." },
        { step: 2, label: 'Free demo class', detail: 'Attend one free class — offline or online. Zero fees, zero obligation.' },
        { step: 3, label: 'Enrol & pick your batch', detail: 'Choose morning, afternoon, or evening batch. EMI available.' },
        { step: 4, label: 'Start building your career', detail: 'Real projects, live instructor, placement support from day one.' },
      ],
      services: [
        { step: 1, label: 'Email or call us', detail: 'We respond within 4 hours on business days.' },
        { step: 2, label: '30-min strategy call', detail: "Talk to Sanjeev Kumar directly — senior engineer, not a sales rep." },
        { step: 3, label: 'Written scope + estimate', detail: 'Delivered within 48 hours. NDA available on request.' },
        { step: 4, label: 'Discovery → Build → Ship', detail: '2-week sprints. First demo in 14 days. On-time, every time.' },
      ],
    },
    faq: [
      { question: 'Where is Techpath located?', answer: 'Techpath is located on Circus Road, Mughalsarai, Chandauli, Uttar Pradesh 232101 — walking distance from DDU Junction. We are open Monday to Saturday, 9 AM to 7 PM. Walk-ins are welcome — no appointment needed.' },
      { question: 'Can I join a Techpath course if I am not in Mughalsarai?', answer: 'Yes. All 14 Techpath courses are available as live online batches via Google Meet or Zoom — same instructor, same curriculum, same timings, same certificate. Students from Varanasi, Ghazipur, Ballia, Mirzapur, and Bihar join online regularly.' },
      { question: 'Is there a free demo class before I enrol?', answer: 'Yes — Techpath offers a free demo class for every course, both offline and online. No fees, no obligation, no pressure. Call or WhatsApp +91 8299708052 to book your free demo class today.' },
      { question: "What are Techpath's batch timings?", answer: 'Techpath runs three daily batches Monday to Saturday: Morning (9–11 AM), Afternoon (1–3 PM), and Evening (5–7 PM). Weekend doubt sessions are available for all enrolled students.' },
      { question: 'Does Techpath offer IT services for businesses or only training?', answer: 'Techpath operates two arms — Academy (14 IT courses) and Professional Services (AI/ML, cloud, web dev, data analytics, cybersecurity) for businesses. Call +91 8299708052 or email info@techpath.biz for a free strategy call.' },
      { question: 'Techpath mein admission kaise lein Mughalsarai mein?', answer: 'Techpath Mughalsarai mein admission ke liye aap seedha Circus Road centre par aa sakte hain ya WhatsApp kar sakte hain — +91 8299708052 par. Pehle ek free demo class attend karein, phir apna batch choose karein. EMI bhi available hai.' },
      { question: 'How quickly does Techpath respond to business enquiries?', answer: 'For professional services enquiries, Techpath responds within 4 hours on business days. Email info@techpath.biz or call +91 8299708052. A written scope and estimate is delivered within 48 hours of your strategy call.' },
    ],
    social_proof: {
      academy: {
        stats: [
          { value: '50,000+', label: 'Students Trained' },
          { value: '94%', label: 'Placement Rate' },
          { value: '25', label: 'Max Batch Size' },
          { value: '14', label: 'Courses Available' },
        ],
      },
      services: {
        stats: [
          { value: '150+', label: 'Projects Delivered' },
          { value: '98%', label: 'Client Satisfaction' },
          { value: '50+', label: 'Enterprise Clients' },
          { value: '4.9', label: 'Clutch Rating' },
        ],
        head_of_solutions: {
          name: 'Sanjeev Kumar',
          role: 'Head of Solutions · 14yr experience',
          quote: "You'll talk to me, not a sales rep. I'll tell you straight if we can help.",
          image: '/team/sanjeev-ceo-techpath.png',
        },
      },
    },
    cta_block: {
      academy: {
        headline: 'Not Sure Which Course Is Right for You?',
        subtext: 'Our academic counsellor will guide you — free, in Hindi or English, no obligation.',
        primary: { label: '📞 Call Now: +91 8299708052', href: 'tel:+918299708052' },
        secondary: { label: '💬 WhatsApp Us', href: 'https://wa.me/918299708052?text=Hi%2C%20I%20want%20free%20career%20counselling%20at%20Techpath%20Mughalsarai.' },
        urgency: '🔥 Free Demo Class — No Fees, No Obligation (Offline + Online)',
      },
      services: {
        headline: "Let's Scope Your Project in 30 Minutes",
        subtext: 'Free strategy call. No pitch deck, no obligation — just a senior engineer reviewing your problem.',
        primary: { label: '📞 Book a Call: +91 8299708052', href: 'tel:+918299708052' },
        secondary: { label: '✉️ Email info@techpath.biz', href: 'mailto:info@techpath.biz' },
        urgency: '3 strategy slots open this week — reply within 4 hours guaranteed',
      },
    },
  };
}

export async function fetchContactPageContent(): Promise<ContactPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/contact-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultContactContent();
    const data = (await res.json()) as ContactPageContent;
    return data;
  } catch {
    return getDefaultContactContent();
  }
}

// --- Pricing page ---

export interface PricingPlanItem {
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export interface PricingPageContent {
  seo?: PageSeoContent;
  hero: { title: string; title_highlight: string; subheadline: string };
  plans: PricingPlanItem[];
  faq_section_title: string;
  faqs: Array<{ question: string; answer: string }>;
  cta_title: string;
  cta_description: string;
  cta_primary_label: string;
  cta_primary_href: string;
  cta_secondary_label: string;
  cta_secondary_href: string;
}

function getDefaultPricingContent(): PricingPageContent {
  return {
    seo: {
      title: 'Pricing',
      description:
        "Transparent pricing for TechPath's IT services. From startup projects to enterprise solutions, find the right plan for your needs.",
    },
    hero: {
      title: 'Simple, Transparent Pricing',
      title_highlight: 'Pricing',
      subheadline:
        'Choose the plan that fits your needs. All plans include our commitment to quality and your success.',
    },
    plans: [
      {
        name: 'Starter',
        description: 'Perfect for small projects and startups',
        price: '$2,500',
        period: 'per project',
        features: [
          'Up to 5 pages',
          'Basic SEO optimization',
          'Mobile responsive design',
          'Contact form integration',
          '30 days support',
          'Source code delivery',
        ],
        cta: 'Get Started',
        highlighted: false,
      },
      {
        name: 'Professional',
        description: 'Ideal for growing businesses',
        price: '$7,500',
        period: 'per project',
        features: [
          'Up to 15 pages',
          'Advanced SEO optimization',
          'Custom design system',
          'CMS integration',
          'API development',
          '90 days support',
          'Performance optimization',
          'Analytics setup',
        ],
        cta: 'Get Started',
        highlighted: true,
      },
      {
        name: 'Enterprise',
        description: 'For large-scale applications',
        price: 'Custom',
        period: 'contact us',
        features: [
          'Unlimited pages',
          'Custom AI solutions',
          'Dedicated team',
          'Priority support 24/7',
          'SLA guarantee',
          'Security audits',
          'Load testing',
          'Training & documentation',
        ],
        cta: 'Contact Sales',
        highlighted: false,
      },
    ],
    faq_section_title: 'Frequently Asked Questions',
    faqs: [
      {
        question: 'What payment methods do you accept?',
        answer:
          'We accept all major credit cards, bank transfers, and can accommodate purchase orders for enterprise clients. Payment terms are typically 50% upfront and 50% on project completion.',
      },
      {
        question: 'Can I upgrade my plan later?',
        answer:
          "Yes, you can upgrade your plan at any time. We'll work with you to seamlessly transition your project to include additional features and capabilities.",
      },
      {
        question: 'What happens after the support period ends?',
        answer:
          'After your included support period, you can purchase extended support packages. We also offer maintenance retainers for ongoing updates and improvements.',
      },
      {
        question: 'Do you offer refunds?',
        answer:
          "We offer a satisfaction guarantee on our work. If you're not happy with the initial concepts, we'll work with you to make it right or provide a partial refund.",
      },
    ],
    cta_title: 'Need a Custom Quote?',
    cta_description: "Every project is unique. Let's discuss your specific requirements.",
    cta_primary_label: 'Schedule a Call',
    cta_primary_href: '/contact',
    cta_secondary_label: 'View Services',
    cta_secondary_href: '/services',
  };
}

export async function fetchPricingPageContent(): Promise<PricingPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/pricing-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultPricingContent();
    const data = (await res.json()) as PricingPageContent;
    return data;
  } catch {
    return getDefaultPricingContent();
  }
}

// --- Policy pages (Privacy, Terms, Cookie) - content as markdown ---

export interface PolicyPageContent {
  seo?: PageSeoContent;
  page_title: string;
  last_updated: string;
  markdown_content: string;
}

function getDefaultPolicyContent(
  pageTitle: string,
  seoTitle: string,
  seoDescription: string,
  markdown: string
): PolicyPageContent {
  return {
    seo: { title: seoTitle, description: seoDescription },
    page_title: pageTitle,
    last_updated: 'December 15, 2025',
    markdown_content: markdown,
  };
}

const DEFAULT_PRIVACY_MD = `At TechPath we are committed to protecting your privacy. See our full policy below.

## 1. Information We Collect

Personal and automatically collected information as described in our policy.

## 2. How We Use Your Information

To provide services, process transactions, support, and improve our website.

## Contact

Email: privacy@techpath.biz
`;

const DEFAULT_TERMS_MD = `Welcome to TechPath. These Terms govern your use of our services.

## 1. Acceptance of Terms

By using our services you agree to these Terms and our Privacy Policy.

## 2. Contact

Questions? legal@techpath.biz
`;

const DEFAULT_COOKIE_MD = `This Cookie Policy explains how TechPath uses cookies. Read with our [Privacy Policy](/privacy).

## 1. What Are Cookies?

Small text files stored on your device when you visit our website.

## 2. Contact

privacy@techpath.biz
`;

export async function fetchPrivacyPageContent(): Promise<PolicyPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/privacy-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultPolicyContent('Privacy Policy', 'Privacy Policy', "Learn how TechPath collects, uses, and protects your personal information. Our commitment to your privacy and data security.", DEFAULT_PRIVACY_MD);
    return (await res.json()) as PolicyPageContent;
  } catch {
    return getDefaultPolicyContent('Privacy Policy', 'Privacy Policy', "Learn how TechPath collects, uses, and protects your personal information. Our commitment to your privacy and data security.", DEFAULT_PRIVACY_MD);
  }
}

export async function fetchTermsPageContent(): Promise<PolicyPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/terms-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultPolicyContent('Terms of Service', 'Terms of Service', "Read the terms and conditions governing the use of TechPath's website and services.", DEFAULT_TERMS_MD);
    return (await res.json()) as PolicyPageContent;
  } catch {
    return getDefaultPolicyContent('Terms of Service', 'Terms of Service', "Read the terms and conditions governing the use of TechPath's website and services.", DEFAULT_TERMS_MD);
  }
}

export async function fetchCookiePageContent(): Promise<PolicyPageContent> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/cookie-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return getDefaultPolicyContent('Cookie Policy', 'Cookie Policy', 'Learn about how TechPath uses cookies and similar technologies on our website.', DEFAULT_COOKIE_MD);
    return (await res.json()) as PolicyPageContent;
  } catch {
    return getDefaultPolicyContent('Cookie Policy', 'Cookie Policy', 'Learn about how TechPath uses cookies and similar technologies on our website.', DEFAULT_COOKIE_MD);
  }
}
