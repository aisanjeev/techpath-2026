/**
 * Case Study Service - Fetches case studies from FastAPI backend
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiCaseStudyTag {
  id: number;
  name: string;
  slug: string;
}

export interface ApiCaseStudy {
  id: number;
  title: string;
  slug: string;
  client_name: string;
  industry: string;
  excerpt: string | null;
  challenge: string;
  solution: string;
  results: string;
  content: string | null;
  featured_image: string | null;
  stat_value: string | null;
  stat_label: string | null;
  additional_stats: string | null;
  testimonial_quote: string | null;
  testimonial_author: string | null;
  testimonial_role: string | null;
  status: string;
  featured: boolean;
  published_at: string | null;
  tags: ApiCaseStudyTag[];
  created_at: string;
  updated_at?: string;
}

export interface ApiCaseStudyList {
  id: number;
  title: string;
  slug: string;
  client_name: string;
  industry: string;
  excerpt: string | null;
  featured_image: string | null;
  stat_value: string | null;
  stat_label: string | null;
  status: string;
  featured: boolean;
  published_at: string | null;
  tags: ApiCaseStudyTag[];
  created_at: string;
}

/**
 * Normalize API case study to a consistent format
 */
export function normalizeCaseStudy(caseStudy: ApiCaseStudy | ApiCaseStudyList) {
  return {
    id: caseStudy.id,
    slug: caseStudy.slug,
    title: caseStudy.title,
    clientName: caseStudy.client_name,
    industry: caseStudy.industry,
    description: caseStudy.excerpt || '',
    image: caseStudy.featured_image,
    stats: {
      value: caseStudy.stat_value || '',
      label: caseStudy.stat_label || '',
    },
    tags: caseStudy.tags.map((t) => t.name),
    href: `/case-studies/${caseStudy.slug}`,
    featured: caseStudy.featured,
    publishedAt: caseStudy.published_at ? new Date(caseStudy.published_at) : new Date(caseStudy.created_at),
    source: 'api' as const,
  };
}

/**
 * Fetch all published case studies from API
 */
export async function fetchCaseStudies(options?: {
  limit?: number;
  featured?: boolean;
  industry?: string;
  tag?: string;
}): Promise<ApiCaseStudyList[]> {
  try {
    const params = new URLSearchParams();
    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.featured !== undefined) params.set('featured', options.featured.toString());
    if (options?.industry) params.set('industry', options.industry);
    if (options?.tag) params.set('tag', options.tag);

    const response = await fetch(`${API_BASE_URL}/api/v1/case-studies/?${params.toString()}`);
    
    if (!response.ok) {
      console.error('Failed to fetch case studies from API:', response.status);
      return [];
    }

    const caseStudies: ApiCaseStudyList[] = await response.json();
    return caseStudies;
  } catch (error) {
    console.error('Error fetching case studies from API:', error);
    return [];
  }
}

/**
 * Fetch a single case study by slug from API
 */
export async function fetchCaseStudyBySlug(slug: string): Promise<ApiCaseStudy | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/case-studies/${slug}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      console.error('Failed to fetch case study from API:', response.status);
      return null;
    }

    const caseStudy: ApiCaseStudy = await response.json();
    return caseStudy;
  } catch (error) {
    console.error('Error fetching case study from API:', error);
    return null;
  }
}

/**
 * Fetch all case study tags from API
 */
export async function fetchCaseStudyTags(): Promise<ApiCaseStudyTag[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/case-studies/tags/`);
    
    if (!response.ok) {
      console.error('Failed to fetch case study tags from API:', response.status);
      return [];
    }

    const tags: ApiCaseStudyTag[] = await response.json();
    return tags;
  } catch (error) {
    console.error('Error fetching case study tags from API:', error);
    return [];
  }
}

