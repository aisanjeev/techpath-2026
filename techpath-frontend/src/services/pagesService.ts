/**
 * Pages Service — fetches standalone CMS pages from the FastAPI backend.
 * Pages are served at domain.com/{slug} via src/pages/[slug].astro.
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiPage {
  id: number;
  title: string;
  slug: string;
  content: string;
  content_type: 'html' | 'markdown';
  excerpt: string | null;
  featured_image: string | null;
  status: string;
  published_at: string | null;
  meta_title: string | null;
  meta_description: string | null;
  author_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface ApiPageListItem {
  id: number;
  title: string;
  slug: string;
  excerpt: string | null;
  featured_image: string | null;
  status: string;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Fetch a single page by slug. Returns null on 404 or any network error so the
 * caller can fall through to Astro's default 404 handler.
 */
export async function fetchPageBySlug(slug: string): Promise<ApiPage | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/pages/${slug}`, {
      // Bust cache per-request so an admin can preview edits instantly.
      headers: { 'Cache-Control': 'no-cache' },
    });

    if (!response.ok) {
      if (response.status !== 404) {
        console.error('Failed to fetch page from API:', response.status);
      }
      return null;
    }

    const page: ApiPage = await response.json();
    return page;
  } catch (error) {
    console.error('Error fetching page from API:', error);
    return null;
  }
}

/**
 * List published pages. Used by sitemap generation at build time.
 */
export async function fetchPages(options?: {
  limit?: number;
  skip?: number;
}): Promise<ApiPageListItem[]> {
  try {
    const params = new URLSearchParams();
    params.set('limit', String(options?.limit ?? 100));
    params.set('skip', String(options?.skip ?? 0));

    const response = await fetch(`${API_BASE_URL}/api/v1/pages?${params.toString()}`);
    if (!response.ok) {
      console.error('Failed to fetch pages from API:', response.status);
      return [];
    }

    const pages: ApiPageListItem[] = await response.json();
    return pages;
  } catch (error) {
    console.error('Error fetching pages from API:', error);
    return [];
  }
}
