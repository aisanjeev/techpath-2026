/**
 * Training page content from API (GET /api/v1/content/training-page).
 * Fallback to null so the page can use inline default when API fails.
 */

const API_BASE = typeof import.meta.env !== 'undefined' && import.meta.env.PUBLIC_API_URL
  ? import.meta.env.PUBLIC_API_URL
  : 'http://localhost:8000';

export interface TrainingLandingContent {
  seo?: {
    title: string;
    description: string;
    image?: string | null;
    canonical_url?: string | null;
    no_index?: boolean;
  };
  hero: {
    title: string;
    subtitle: string;
    headline_subline: string;
    badge_text: string;
    primary_cta: { label: string; href: string };
    secondary_cta: { label: string; href: string };
    trust_badges: Array<{ icon: string; value: string; label: string }>;
  };
  pain_points: {
    section_title: string;
    section_subtext: string;
    transition_text: string;
    items: Array<{
      icon: string;
      title: string;
      description: string;
      color: string;
      bg_color: string;
      border_color: string;
    }>;
  };
  usps: {
    section_title: string;
    section_subtext: string;
    items: Array<{
      icon: string;
      title: string;
      highlights: string[];
      color: string;
    }>;
  };
  faqs: Array<{ question: string; answer: string }>;
  stories: {
    section_title: string;
    section_subtext: string;
    items: Array<{
      name: string;
      location: string;
      previous_role: string;
      current_role: string;
      previous_salary: string;
      current_salary: string;
      course: string;
      duration: string;
      quote: string;
      rating: number;
      has_video: boolean;
    }>;
  };
  offer_banner: {
    discount: string;
    savings: string;
    target_date: string | null;
    badge_text: string;
    benefits: string[];
  };
  schema_defaults: {
    name: string;
    description: string;
    rating_value: string;
    review_count: string;
  };
  cta: {
    title: string;
    description: string;
    primary_button: { label: string; href: string };
    secondary_button: { label: string; href: string };
  };
}

/** Minimal fallback when API is unavailable (same shape as API response). */
export function getDefaultTrainingContent(): TrainingLandingContent {
  return {
    seo: {
      title: 'IT Training in Mughalsarai | Techpath Academy — Live Classes, Real Projects',
      description:
        'Join Techpath Academy in Mughalsarai for hands-on IT training — Python, Web Dev, Data Science & more. Live batches, bilingual instruction, project-based learning. Free demo class available.',
      canonical_url: 'https://techpath.biz/training/',
    },
    hero: {
      title: 'Job-Ready Tech Skills, Built in Mughalsarai',
      subtitle: 'Live classroom + online batches · Hindi & English · Real projects · Placement support',
      headline_subline: 'Start with a Free Demo Class — No Commitment',
      badge_text: 'New Batch Starting Soon — Limited Seats',
      primary_cta: { label: 'Book Free Demo Class', href: '#enroll' },
      secondary_cta: { label: 'View All Courses', href: '#courses' },
      trust_badges: [
        { icon: 'users', value: '500+', label: 'Students Trained' },
        { icon: 'briefcase', value: '85%+', label: 'Placement Rate' },
        { icon: 'star', value: '4.8/5', label: 'Student Rating' },
        { icon: 'calendar', value: 'Since 2019', label: 'Est.' },
      ],
    },
    pain_points: {
      section_title: 'Is This Stopping You From Getting a Tech Job?',
      section_subtext: 'Most students in Mughalsarai and nearby districts face the same roadblocks.',
      transition_text: 'Techpath Academy was built to solve exactly these problems — right here in your city.',
      items: [
        {
          icon: 'alert-triangle',
          title: 'Your Degree Isn\'t Enough Anymore',
          description: 'B.Tech and BCA graduates are finding that college theory doesn\'t match what companies actually want. Employers test practical skills — frameworks, tools, and real code — that most colleges don\'t teach.',
          color: 'text-red-400',
          bg_color: 'bg-red-500/10',
          border_color: 'border-red-500/30',
        },
        {
          icon: 'map-pin',
          title: 'Good Coaching Is Too Far (and Too Expensive)',
          description: 'Quality IT training institutes are mostly in Varanasi, Lucknow, or Delhi. Relocating or commuting costs ₹20,000–₹50,000 extra per year — on top of already high course fees.',
          color: 'text-orange-400',
          bg_color: 'bg-orange-500/10',
          border_color: 'border-orange-500/30',
        },
        {
          icon: 'video-off',
          title: 'Pre-Recorded Videos Don\'t Actually Teach You',
          description: 'Platforms like YouTube and Udemy are full of courses you start but never finish. Without a live teacher, doubt-clearing sessions, and peer accountability, most self-learners give up within weeks.',
          color: 'text-yellow-400',
          bg_color: 'bg-yellow-500/10',
          border_color: 'border-yellow-500/30',
        },
      ],
    },
    usps: {
      section_title: 'Why Students Choose Techpath Academy',
      section_subtext: 'We designed every part of our training around what actually gets you hired.',
      items: [
        {
          icon: 'languages',
          title: 'Taught in Hindi + English',
          highlights: [
            'Concepts explained in Hindi for clarity',
            'Technical terms and documentation in English',
            'Interview prep in both languages',
            'No language barrier slowing you down',
          ],
          color: 'from-primary-500 to-secondary-500',
        },
        {
          icon: 'layers',
          title: 'Offline + Online — Your Choice',
          highlights: [
            'Live classroom batches in Mughalsarai',
            'Synchronous online batches (same schedule)',
            'All sessions recorded for revision',
            'Switch modes anytime without losing progress',
          ],
          color: 'from-secondary-500 to-primary-500',
        },
        {
          icon: 'code-2',
          title: 'Project-First Curriculum',
          highlights: [
            'Build real projects from Week 1',
            'Portfolio-ready work by graduation',
            'Industry tools: Git, Docker, cloud platforms',
            'Code reviews by working engineers',
          ],
          color: 'from-primary-500 to-secondary-500',
        },
        {
          icon: 'indian-rupee',
          title: 'Transparent, Affordable Pricing',
          highlights: [
            'No hidden fees — one flat course price',
            'EMI options available (0% interest)',
            'Free demo class before you commit',
            'Partial refund if you drop in Week 1',
          ],
          color: 'from-secondary-500 to-primary-500',
        },
      ],
    },
    faqs: [
      {
        question: 'Do I need prior coding experience to join?',
        answer: 'No. Our foundation courses start from absolute zero. If you can use a smartphone and basic computer, you\'re ready. We\'ll teach you everything from setting up your environment to writing your first program.',
      },
      {
        question: 'Are classes in Hindi or English?',
        answer: 'Both. We teach concepts in Hindi so nothing gets lost in translation, while keeping technical terms, code, and documentation in English — because that\'s what you\'ll use on the job. You get the best of both.',
      },
      {
        question: 'Can I attend online if I\'m not in Mughalsarai?',
        answer: 'Yes. Our online batches run on the same live schedule as the classroom batches. You join a Zoom/Google Meet session, interact with the instructor in real time, and submit the same assignments. All sessions are also recorded.',
      },
      {
        question: 'What is the fee structure and are EMIs available?',
        answer: 'Course fees vary by program (typically ₹8,000–₹25,000 for the full course). We offer 0% interest EMI split over 2–3 months. Call or WhatsApp us at +91 82997 08052 for the exact fee of the course you\'re interested in.',
      },
      {
        question: 'Do you help with job placement after the course?',
        answer: 'Yes. We provide resume building, mock interviews, LinkedIn profile review, and referrals to our hiring-partner network. We don\'t guarantee a specific salary, but we actively work to get you interviews. Our current placement rate is 85%+.',
      },
      {
        question: 'How do I register for the free demo class?',
        answer: 'Call or WhatsApp +91 82997 08052 to reserve your seat. Demo classes run every Saturday. Alternatively, fill in the enquiry form on this page and we\'ll call you back within a few hours.',
      },
      {
        question: 'Kya main working professional hoon toh bhi join kar sakta hoon? (Can working professionals join?)',
        answer: 'Bilkul. Hamare weekend aur evening batches specifically working professionals ke liye design kiye gaye hain. Saturday-Sunday batches available hain. (Absolutely. Our weekend and evening batches are designed for working professionals.)',
      },
      {
        question: 'What courses do you currently offer?',
        answer: 'We currently offer: Python Programming, Web Development (HTML/CSS/JS + React), Data Science & Machine Learning, Java Full Stack, and a DevOps Fundamentals module. New batches start monthly. Check the courses section above or call us for the latest schedule.',
      },
    ],
    stories: {
      // section_title / section_subtext are used as the Google Reviews section heading.
      // items is always [] — live reviews come from the Google Places API.
      section_title: 'What Our Students Say on Google',
      section_subtext:
        'Real reviews from verified students — Mughalsarai, Chandauli, Varanasi, and across eastern UP.',
      items: [],
    },
    offer_banner: {
      discount: 'Free Demo Class',
      savings: 'Zero Risk',
      target_date: null,
      badge_text: 'ATTEND BEFORE YOU COMMIT — Every Saturday',
      benefits: [
        'Meet your instructor before paying',
        'See the actual curriculum and projects',
        'Get all your doubts cleared',
        'No sales pressure — decide in your own time',
      ],
    },
    schema_defaults: {
      name: 'Techpath Academy',
      description: 'IT training institute in Mughalsarai offering live classroom and online courses in Python, Web Development, Data Science, and more.',
      rating_value: '',
      review_count: '',
    },
    cta: {
      title: 'Ready to Start Your Tech Career?',
      description: 'Book a free demo class this Saturday — meet the instructor, see the curriculum, and decide with zero pressure.',
      primary_button: { label: 'Call Now: +91 82997 08052', href: 'tel:+918299708052' },
      secondary_button: { label: 'WhatsApp Us', href: 'https://wa.me/918299708052' },
    },
  };
}

export async function fetchTrainingPageContent(): Promise<TrainingLandingContent | null> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/content/training-page`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) return null;
    const data = await res.json();
    return data as TrainingLandingContent;
  } catch {
    return null;
  }
}
