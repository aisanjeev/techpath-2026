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
      title: 'Online Tech Courses | Certificate Programs | TechPath Training',
      description:
        'Learn Data Science, AI, Cloud, Web Development with live instructors. Courses from ₹7K. 94% job placement. 30-day money-back guarantee. Enroll now!',
    },
    hero: {
      title: 'Master In-Demand Tech Skills',
      subtitle: 'Live instructor training + Real-world projects + Job guarantee.',
      headline_subline: 'Land High-Paying Jobs in 90 Days',
      badge_text: 'New Batch Starting Soon',
      primary_cta: { label: 'Start Free Trial', href: '#enroll' },
      secondary_cta: { label: 'View Course Catalog', href: '#courses' },
      trust_badges: [
        { icon: '⭐', value: '4.9/5', label: 'Reviews' },
        { icon: '👨‍🎓', value: '50,000+', label: 'Students' },
        { icon: '💼', value: '94%', label: 'Placement' },
        { icon: '🏆', value: 'Since 2019', label: 'Trusted' },
      ],
    },
    pain_points: {
      section_title: 'Stuck Without a Clear Tech Career Path?',
      section_subtext: "You're not alone.",
      transition_text: 'There\'s a better way to break into tech.',
      items: [],
    },
    usps: {
      section_title: 'Why Choose TechPath',
      section_subtext: 'We transform careers with a proven methodology.',
      items: [],
    },
    faqs: [],
    stories: {
      section_title: 'Success Stories',
      section_subtext: 'Join thousands who\'ve changed their careers.',
      items: [],
    },
    offer_banner: {
      discount: '₹15,000 OFF',
      savings: 'Save 30%',
      target_date: null,
      badge_text: 'Limited Time Offer',
      benefits: [],
    },
    schema_defaults: {
      name: 'TechPath Training',
      description: 'Online tech courses and certification programs',
      rating_value: '4.9',
      review_count: '2000',
    },
    cta: {
      title: 'Ready to Transform Your Career?',
      description: 'Join thousands who\'ve changed their lives with TechPath.',
      primary_button: { label: 'Explore Courses', href: '#courses' },
      secondary_button: { label: 'Talk to Counselor', href: '/contact' },
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
