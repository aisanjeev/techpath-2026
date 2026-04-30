// API Response Types

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  timestamp?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

// User Types
export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  avatar_url?: string;
  created_at: string;
  updated_at?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// Service Types
export interface ServicePricingPlanItem {
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export interface ServiceFAQItem {
  question: string;
  answer: string;
}

export interface Service {
  id: number;
  title: string;
  slug: string;
  description: string;
  short_description?: string;
  icon?: string;
  image_url?: string;
  features?: string[];
  pricing_plans?: ServicePricingPlanItem[];
  faqs?: ServiceFAQItem[];
  price?: string;
  cta_text: string;
  cta_url?: string;
  featured: boolean;
  display_order: number;
  is_active: boolean;
  meta_title?: string;
  meta_description?: string;
  og_image?: string;
  canonical_url?: string;
  no_index?: boolean;
  // Bento layout
  layout_size: 'large' | 'small' | 'wide';
  badge_label?: string | null;
  tags?: string[] | null;
  stat_label?: string | null;
  stat_value?: string | null;
  accent_color: 'purple' | 'cyan' | 'green' | 'amber' | 'blue';
  graphic_variant: 'orbital' | 'code-window' | 'bar-chart' | 'none';
  created_at: string;
  updated_at: string;
}

export interface ServiceCreate {
  title: string;
  slug: string;
  description: string;
  short_description?: string;
  icon?: string;
  image_url?: string;
  features?: string[];
  pricing_plans?: ServicePricingPlanItem[];
  faqs?: ServiceFAQItem[];
  price?: string;
  cta_text?: string;
  cta_url?: string;
  featured?: boolean;
  display_order?: number;
  is_active?: boolean;
  meta_title?: string;
  meta_description?: string;
  og_image?: string;
  canonical_url?: string;
  no_index?: boolean;
  // Bento layout
  layout_size?: 'large' | 'small' | 'wide';
  badge_label?: string | null;
  tags?: string[] | null;
  stat_label?: string | null;
  stat_value?: string | null;
  accent_color?: 'purple' | 'cyan' | 'green' | 'amber' | 'blue';
  graphic_variant?: 'orbital' | 'code-window' | 'bar-chart' | 'none';
}

export interface ServiceUpdate extends Partial<ServiceCreate> {}

// Blog Types
export interface BlogTag {
  id: number;
  name: string;
  slug: string;
}

export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  category_id: number;
  category: BlogCategory;
  content: string;
  content_type?: 'html' | 'markdown';
  excerpt?: string;
  featured_image?: string;
  status: 'draft' | 'published' | 'archived';
  featured: boolean;
  reading_time?: number;
  meta_title?: string;
  meta_description?: string;
  published_at?: string;
  author_id?: number;
  tags: BlogTag[];
  created_at: string;
  updated_at?: string;
}

export interface BlogPostCreate {
  title: string;
  slug: string;
  category_id: number;
  content: string;
  content_type?: 'html' | 'markdown';
  excerpt?: string;
  featured_image?: string;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  reading_time?: number;
  meta_title?: string;
  meta_description?: string;
  published_at?: string;
  tag_ids?: number[];
}

export interface BlogPostUpdate extends Partial<BlogPostCreate> {}

// Page Types (standalone CMS pages served at domain.com/{slug})
export interface Page {
  id: number;
  title: string;
  slug: string;
  content: string;
  content_type: 'html' | 'markdown';
  excerpt?: string;
  featured_image?: string;
  status: 'draft' | 'published' | 'archived';
  meta_title?: string;
  meta_description?: string;
  published_at?: string;
  author_id?: number;
  created_at: string;
  updated_at: string;
}

export interface PageListItem {
  id: number;
  title: string;
  slug: string;
  excerpt?: string;
  featured_image?: string;
  status: 'draft' | 'published' | 'archived';
  published_at?: string;
  created_at: string;
  updated_at: string;
}

export interface PageCreate {
  title: string;
  slug: string;
  content: string;
  content_type?: 'html' | 'markdown';
  excerpt?: string;
  featured_image?: string;
  status?: 'draft' | 'published' | 'archived';
  meta_title?: string;
  meta_description?: string;
  published_at?: string;
}

export interface PageUpdate extends Partial<PageCreate> {}

// Case Study Types
export interface CaseStudyTag {
  id: number;
  name: string;
  slug: string;
}

export interface CaseStudy {
  id: number;
  title: string;
  slug: string;
  client_name: string;
  industry: string;
  challenge: string;
  solution: string;
  results: string;
  content?: string;
  excerpt?: string;
  featured_image?: string;
  stat_value?: string;
  stat_label?: string;
  additional_stats?: Record<string, string>;
  testimonial_quote?: string;
  testimonial_author?: string;
  testimonial_role?: string;
  status: 'draft' | 'published' | 'archived';
  featured: boolean;
  published_at?: string;
  meta_title?: string;
  meta_description?: string;
  tags: CaseStudyTag[];
  created_at: string;
  updated_at?: string;
}

export interface CaseStudyCreate {
  title: string;
  slug: string;
  client_name: string;
  industry: string;
  challenge: string;
  solution: string;
  results: string;
  content?: string;
  excerpt?: string;
  featured_image?: string;
  stat_value?: string;
  stat_label?: string;
  additional_stats?: Record<string, string>;
  testimonial_quote?: string;
  testimonial_author?: string;
  testimonial_role?: string;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  published_at?: string;
  meta_title?: string;
  meta_description?: string;
  tag_ids?: number[];
}

export interface CaseStudyUpdate extends Partial<CaseStudyCreate> {}

// Contact Types
export interface ContactInquiry {
  id: number;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  subject?: string;
  message: string;
  service_interest?: string;
  status: 'new' | 'in_progress' | 'resolved' | 'closed';
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface ContactInquiryUpdate {
  status?: 'new' | 'in_progress' | 'resolved' | 'closed';
  notes?: string;
}

// Newsletter Types
export interface NewsletterSubscriber {
  id: number;
  email: string;
  is_active: boolean;
  subscribed_at: string;
  unsubscribed_at?: string;
}

// Course Types
export interface Skill {
  id: number;
  name: string;
  slug: string;
}

export interface CourseCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  parent_id?: number;
  display_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CourseCategoryTree extends CourseCategory {
  children: CourseCategoryTree[];
  course_count: number;
}

export interface CurriculumModule {
  title: string;
  topics: string[];
  duration?: string;
}

export interface ProjectItem {
  title: string;
  description?: string;
}

export interface FAQItem {
  question: string;
  answer: string;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  short_description?: string;
  description: string;
  category_id: number;
  category: CourseCategory;
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
  curriculum?: CurriculumModule[];
  learning_outcomes?: string[];
  prerequisites?: string[];
  projects?: ProjectItem[];
  faqs?: FAQItem[];
  certification_name?: string;
  certification_authority?: string;
  meta_title?: string;
  meta_description?: string;
  next_batch_date?: string;
  status: 'draft' | 'published' | 'archived';
  featured: boolean;
  is_active: boolean;
  skills: Skill[];
  created_at: string;
  updated_at: string;
}

export interface CourseCreate {
  title: string;
  slug: string;
  short_description?: string;
  description: string;
  category_id: number;
  price: number;
  original_price?: number;
  emi_available?: boolean;
  emi_amount?: number;
  currency?: string;
  duration: string;
  duration_hours?: number;
  batch_size?: number;
  level?: 'beginner' | 'intermediate' | 'advanced';
  rating?: number;
  review_count?: number;
  enrollment_count?: number;
  placement_rate?: number;
  featured_image?: string;
  video_url?: string;
  instructor_name?: string;
  instructor_title?: string;
  instructor_bio?: string;
  instructor_image?: string;
  curriculum?: CurriculumModule[];
  learning_outcomes?: string[];
  prerequisites?: string[];
  projects?: ProjectItem[];
  faqs?: FAQItem[];
  certification_name?: string;
  certification_authority?: string;
  meta_title?: string;
  meta_description?: string;
  next_batch_date?: string;
  status?: 'draft' | 'published' | 'archived';
  featured?: boolean;
  is_active?: boolean;
  skill_ids?: number[];
}

export interface CourseUpdate extends Partial<CourseCreate> {}

export interface CourseEnrollment {
  id: number;
  name: string;
  email: string;
  phone: string;
  education?: string;
  experience?: string;
  current_role?: string;
  linkedin_url?: string;
  course_id?: number;
  course?: Course;
  preferred_batch?: string;
  source?: string;
  utm_campaign?: string;
  utm_source?: string;
  utm_medium?: string;
  message?: string;
  status: 'new' | 'contacted' | 'interested' | 'enrolled' | 'not_interested' | 'closed';
  notes?: string;
  assigned_to?: string;
  last_contacted_at?: string;
  next_followup_at?: string;
  created_at: string;
  updated_at: string;
}

export interface CourseEnrollmentCreate {
  name: string;
  email: string;
  phone: string;
  education?: string;
  experience?: string;
  current_role?: string;
  linkedin_url?: string;
  course_id?: number;
  preferred_batch?: string;
  source?: string;
  utm_campaign?: string;
  utm_source?: string;
  utm_medium?: string;
  message?: string;
}

export interface CourseEnrollmentUpdate {
  status?: 'new' | 'contacted' | 'interested' | 'enrolled' | 'not_interested' | 'closed';
  notes?: string;
  assigned_to?: string;
  last_contacted_at?: string;
  next_followup_at?: string;
}

