/**
 * Course Service - Fetches courses from FastAPI backend
 */

const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiSkill {
  id: number;
  name: string;
  slug: string;
}

export interface ApiCourseCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
}

export interface ApiCurriculumModule {
  title: string;
  topics: string[];
  duration?: string;
}

export interface ApiProjectItem {
  title: string;
  description?: string;
}

export interface ApiCourse {
  id: number;
  title: string;
  slug: string;
  short_description?: string;
  description: string;
  category_id: number;
  category: ApiCourseCategory;
  price: number;
  original_price?: number;
  emi_available: boolean;
  emi_amount?: number;
  currency: string;
  duration: string;
  duration_hours?: number;
  batch_size: number;
  level: 'beginner' | 'intermediate' | 'advanced';
  rating: number;
  review_count: number;
  enrollment_count: number;
  placement_rate?: number;
  featured_image?: string;
  video_url?: string;
  instructor_name?: string;
  instructor_title?: string;
  instructor_bio?: string;
  instructor_image?: string;
  curriculum?: ApiCurriculumModule[];
  learning_outcomes?: string[];
  prerequisites?: string[];
  projects?: ApiProjectItem[];
  certification_name?: string;
  certification_authority?: string;
  meta_title?: string;
  meta_description?: string;
  next_batch_date?: string;
  status: string;
  featured: boolean;
  is_active: boolean;
  skills: ApiSkill[];
  created_at: string;
  updated_at: string;
}

export interface ApiCourseList {
  id: number;
  title: string;
  slug: string;
  short_description?: string;
  category: ApiCourseCategory;
  price: number;
  original_price?: number;
  emi_available: boolean;
  currency: string;
  duration: string;
  batch_size: number;
  level: 'beginner' | 'intermediate' | 'advanced';
  rating: number;
  review_count: number;
  enrollment_count: number;
  placement_rate?: number;
  featured_image?: string;
  skills: ApiSkill[];
  next_batch_date?: string;
  status: string;
  featured: boolean;
  is_active: boolean;
  created_at: string;
}

/**
 * Normalize API course for frontend use
 */
export function normalizeApiCourse(course: ApiCourse | ApiCourseList) {
  return {
    slug: course.slug,
    name: course.title,
    category: course.category.slug,
    categoryName: course.category.name,
    rating: course.rating,
    reviewCount: course.review_count,
    duration: course.duration,
    batchSize: course.batch_size,
    price: course.price,
    originalPrice: course.original_price,
    emiAvailable: course.emi_available,
    placementRate: course.placement_rate,
    skills: course.skills.map(s => s.name),
    level: course.level,
    image: course.featured_image,
    featured: course.featured,
    // Full course details (only available for single course fetch)
    ...('description' in course && {
      description: course.description,
      shortDescription: course.short_description,
      curriculum: course.curriculum,
      learningOutcomes: course.learning_outcomes,
      prerequisites: course.prerequisites,
      projects: course.projects,
      instructorName: course.instructor_name,
      instructorTitle: course.instructor_title,
      instructorBio: course.instructor_bio,
      instructorImage: course.instructor_image,
      videoUrl: course.video_url,
      certificationName: course.certification_name,
      certificationAuthority: course.certification_authority,
      metaTitle: course.meta_title,
      metaDescription: course.meta_description,
      nextBatchDate: course.next_batch_date,
    }),
  };
}

/**
 * Fetch all published courses from API
 */
export async function fetchCourses(options?: {
  limit?: number;
  featured?: boolean;
  category?: string;
  level?: string;
}): Promise<ApiCourseList[]> {
  try {
    const params = new URLSearchParams();
    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.featured !== undefined) params.set('featured', options.featured.toString());
    if (options?.category) params.set('category', options.category);
    if (options?.level) params.set('level', options.level);

    const response = await fetch(`${API_BASE_URL}/api/v1/courses/?${params.toString()}`);

    if (!response.ok) {
      console.error('Failed to fetch courses from API:', response.status);
      return [];
    }

    const result = await response.json();
    // API returns { success: true, data: [...courses] }
    return result.data || [];
  } catch (error) {
    console.error('Error fetching courses from API:', error);
    return [];
  }
}

/**
 * Fetch a single course by slug from API
 */
export async function fetchCourseBySlug(slug: string): Promise<ApiCourse | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/courses/${slug}`);

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      console.error('Failed to fetch course from API:', response.status);
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching course from API:', error);
    return null;
  }
}

/**
 * Fetch course categories
 */
export async function fetchCourseCategories(): Promise<ApiCourseCategory[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/courses/categories`);

    if (!response.ok) {
      console.error('Failed to fetch course categories:', response.status);
      return [];
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching course categories:', error);
    return [];
  }
}

/**
 * Submit course enrollment/inquiry
 */
export async function submitEnrollment(data: {
  name: string;
  email: string;
  phone: string;
  education?: string;
  experience?: string;
  current_role?: string;
  course_id?: number;
  preferred_batch?: string;
  message?: string;
  source?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
}): Promise<{ success: boolean; error?: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/courses/enrollments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return { success: false, error: errorData.detail || 'Failed to submit enrollment' };
    }

    return { success: true };
  } catch (error) {
    console.error('Error submitting enrollment:', error);
    return { success: false, error: 'Network error. Please try again.' };
  }
}

