/**
 * Blog Service - Fetches blog posts from FastAPI backend
 * Works alongside Astro Content Collections for hybrid approach
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiBlogCategory {
  id: number;
  name: string;
  slug: string;
}

export interface ApiBlogPost {
  id: number;
  title: string;
  slug: string;
  category_id: number;
  category: ApiBlogCategory;
  excerpt: string | null;
  content: string;
  content_type: 'html' | 'markdown';
  featured_image: string | null;
  status: string;
  featured: boolean;
  reading_time: number | null;
  published_at: string | null;
  meta_title: string | null;
  meta_description: string | null;
  tags: { id: number; name: string; slug: string }[];
  created_at: string;
  updated_at?: string;
}

export interface ApiBlogPostList {
  id: number;
  title: string;
  slug: string;
  category_id: number;
  category: ApiBlogCategory;
  excerpt: string | null;
  featured_image: string | null;
  status: string;
  featured: boolean;
  reading_time: number | null;
  published_at: string | null;
  tags: { id: number; name: string; slug: string }[];
  created_at: string;
}

/**
 * Convert API blog post to format compatible with Astro content collections
 */
export function normalizeApiPost(post: ApiBlogPost | ApiBlogPostList) {
  return {
    slug: post.slug,
    data: {
      title: post.title,
      description: post.excerpt || '',
      pubDate: new Date(post.published_at || post.created_at),
      author: 'TechPath Team',
      image: post.featured_image,
      tags: post.tags.map((t) => t.name),
      category: post.category?.name || 'Uncategorized',
      categorySlug: post.category?.slug || 'uncategorized',
      readingTime: post.reading_time,
      draft: post.status !== 'published',
    },
    body: 'content' in post ? post.content : '',
    contentType: 'content_type' in post ? post.content_type : 'markdown',
    source: 'api' as const,
  };
}

/**
 * Fetch all published blog posts from API
 */
export async function fetchBlogPosts(options?: {
  limit?: number;
  skip?: number;
  featured?: boolean;
  tag?: string;
}): Promise<ApiBlogPostList[]> {
  try {
    const params = new URLSearchParams();
    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.skip != null) params.set('skip', options.skip.toString());
    if (options?.featured !== undefined) params.set('featured', options.featured.toString());
    if (options?.tag) params.set('tag', options.tag);

    const response = await fetch(`${API_BASE_URL}/api/v1/blog/posts?${params.toString()}`);
    
    if (!response.ok) {
      console.error('Failed to fetch blog posts from API:', response.status);
      return [];
    }

    const posts: ApiBlogPostList[] = await response.json();
    return posts;
  } catch (error) {
    console.error('Error fetching blog posts from API:', error);
    return [];
  }
}

/**
 * Fetch published blog posts with pagination; returns posts and total count.
 * Use for archive/list pages that need pagination UI.
 */
export async function fetchBlogPostsPaginated(options: {
  limit: number;
  skip: number;
  tag?: string;
}): Promise<{ posts: ApiBlogPostList[]; total: number }> {
  try {
    const params = new URLSearchParams();
    params.set('limit', options.limit.toString());
    params.set('skip', options.skip.toString());
    if (options.tag) params.set('tag', options.tag);

    const response = await fetch(`${API_BASE_URL}/api/v1/blog/posts?${params.toString()}`);
    
    if (!response.ok) {
      console.error('Failed to fetch blog posts from API:', response.status);
      return { posts: [], total: 0 };
    }

    const totalHeader = response.headers.get('X-Total-Count');
    const total = totalHeader != null ? parseInt(totalHeader, 10) : 0;
    const posts: ApiBlogPostList[] = await response.json();
    return {
      posts,
      total: Number.isNaN(total) ? posts.length : total,
    };
  } catch (error) {
    console.error('Error fetching blog posts from API:', error);
    return { posts: [], total: 0 };
  }
}

/**
 * Fetch a single blog post by slug from API
 */
export async function fetchBlogPostBySlug(slug: string): Promise<ApiBlogPost | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/blog/posts/${slug}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      console.error('Failed to fetch blog post from API:', response.status);
      return null;
    }

    const post: ApiBlogPost = await response.json();
    return post;
  } catch (error) {
    console.error('Error fetching blog post from API:', error);
    return null;
  }
}

/**
 * Check if API is available
 */
export async function isApiAvailable(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(3000), // 3 second timeout
    });
    return response.ok;
  } catch {
    return false;
  }
}

