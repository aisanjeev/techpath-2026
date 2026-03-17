import { z } from 'zod';

// Auth validations
export const loginSchema = z.object({
  username: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

export type LoginFormData = z.infer<typeof loginSchema>;

// Service validations
const servicePricingPlanItemSchema = z.object({
  name: z.string(),
  description: z.string(),
  price: z.string(),
  period: z.string(),
  features: z.array(z.string()),
  cta: z.string(),
  highlighted: z.boolean().optional(),
});

const serviceFAQItemSchema = z.object({
  question: z.string().min(1, 'Question is required'),
  answer: z.string().min(1, 'Answer is required'),
});

export const serviceSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title is too long'),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'Slug must be lowercase letters, numbers, and hyphens only'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  short_description: z.string().max(500, 'Short description is too long').optional().or(z.literal('')),
  icon: z.string().optional().or(z.literal('')),
  image_url: z.string().url('Invalid URL').optional().or(z.literal('')),
  features: z.array(z.string()).optional(),
  pricing_plans: z.array(servicePricingPlanItemSchema).optional(),
  faqs: z.array(serviceFAQItemSchema).optional(),
  price: z.string().optional().or(z.literal('')),
  cta_text: z.string().optional().or(z.literal('')),
  cta_url: z.string().url('Invalid URL').optional().or(z.literal('')),
  featured: z.boolean(),
  display_order: z.number().int().min(0),
  is_active: z.boolean(),
  meta_title: z.string().max(70, 'Meta title should be under 70 characters').optional().or(z.literal('')),
  meta_description: z.string().max(160, 'Meta description should be under 160 characters').optional().or(z.literal('')),
  og_image: z.string().url('Invalid URL').optional().or(z.literal('')),
  canonical_url: z.string().url('Invalid URL').optional().or(z.literal('')),
  no_index: z.boolean(),
});

export type ServiceFormData = z.infer<typeof serviceSchema>;

// Blog post validations
export const blogPostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title is too long'),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'Slug must be lowercase letters, numbers, and hyphens only'),
  category_id: z.number({ message: 'Category is required' }).min(1, 'Category is required'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  content_type: z.enum(['html', 'markdown']).optional(),
  excerpt: z.string().max(500, 'Excerpt is too long').optional().or(z.literal('')),
  featured_image: z.string().url('Invalid URL').optional().or(z.literal('')),
  status: z.enum(['draft', 'published', 'archived']),
  featured: z.boolean(),
  reading_time: z.number().optional(),
  meta_title: z.string().max(70, 'Meta title should be under 70 characters').optional().or(z.literal('')),
  meta_description: z.string().max(160, 'Meta description should be under 160 characters').optional().or(z.literal('')),
  published_at: z.string().optional().or(z.literal('')),
  tag_ids: z.array(z.number()).optional(),
});

export type BlogPostFormData = z.infer<typeof blogPostSchema>;

// Case study validations
export const caseStudySchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title is too long'),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'Slug must be lowercase letters, numbers, and hyphens only'),
  client_name: z.string().min(1, 'Client name is required').max(255),
  industry: z.string().min(1, 'Industry is required').max(100),
  challenge: z.string().min(10, 'Challenge must be at least 10 characters'),
  solution: z.string().min(10, 'Solution must be at least 10 characters'),
  results: z.string().min(10, 'Results must be at least 10 characters'),
  content: z.string().optional().or(z.literal('')),
  excerpt: z.string().max(500, 'Excerpt is too long').optional().or(z.literal('')),
  featured_image: z.string().url('Invalid URL').optional().or(z.literal('')),
  stat_value: z.string().optional().or(z.literal('')),
  stat_label: z.string().optional().or(z.literal('')),
  testimonial_quote: z.string().optional().or(z.literal('')),
  testimonial_author: z.string().optional().or(z.literal('')),
  testimonial_role: z.string().optional().or(z.literal('')),
  status: z.enum(['draft', 'published', 'archived']),
  featured: z.boolean(),
  meta_title: z.string().max(70, 'Meta title should be under 70 characters').optional().or(z.literal('')),
  meta_description: z.string().max(160, 'Meta description should be under 160 characters').optional().or(z.literal('')),
  published_at: z.string().optional().or(z.literal('')),
  tag_ids: z.array(z.number()).optional(),
});

export type CaseStudyFormData = z.infer<typeof caseStudySchema>;

// Contact inquiry validations
export const contactInquiryUpdateSchema = z.object({
  status: z.enum(['new', 'in_progress', 'resolved', 'closed']).optional(),
  notes: z.string().optional().or(z.literal('')),
});

export type ContactInquiryUpdateFormData = z.infer<typeof contactInquiryUpdateSchema>;

// Course validations
export const courseSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title is too long'),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'Slug must be lowercase letters, numbers, and hyphens only'),
  short_description: z.string().max(500, 'Short description is too long').optional().or(z.literal('')),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  category_id: z.number({ message: 'Category is required' }).min(1, 'Category is required'),
  price: z.number({ message: 'Price is required' }).min(0, 'Price must be positive'),
  original_price: z.number().min(0).optional(),
  emi_available: z.boolean(),
  emi_amount: z.number().min(0).optional(),
  currency: z.string().max(3).optional(),
  duration: z.string().min(1, 'Duration is required').max(50),
  duration_hours: z.number().min(0).optional(),
  batch_size: z.number().min(1).optional(),
  level: z.enum(['beginner', 'intermediate', 'advanced']),
  rating: z.number().min(0).max(5).optional(),
  review_count: z.number().min(0).optional(),
  enrollment_count: z.number().min(0).optional(),
  placement_rate: z.number().min(0).max(100).optional(),
  featured_image: z.string().url('Invalid URL').optional().or(z.literal('')),
  video_url: z.string().url('Invalid URL').optional().or(z.literal('')),
  instructor_name: z.string().max(255).optional().or(z.literal('')),
  instructor_title: z.string().max(255).optional().or(z.literal('')),
  instructor_bio: z.string().optional().or(z.literal('')),
  instructor_image: z.string().url('Invalid URL').optional().or(z.literal('')),
  certification_name: z.string().max(255).optional().or(z.literal('')),
  certification_authority: z.string().max(255).optional().or(z.literal('')),
  meta_title: z.string().max(70, 'Meta title should be under 70 characters').optional().or(z.literal('')),
  meta_description: z.string().max(160, 'Meta description should be under 160 characters').optional().or(z.literal('')),
  next_batch_date: z.string().optional().or(z.literal('')),
  status: z.enum(['draft', 'published', 'archived']),
  featured: z.boolean(),
  is_active: z.boolean(),
  skill_ids: z.array(z.number()).optional(),
  // Complex fields
  learning_outcomes: z.array(z.string()).optional(),
  prerequisites: z.array(z.string()).optional(),
  curriculum: z.array(z.object({
    title: z.string().min(1),
    topics: z.array(z.string()),
    duration: z.string().optional(),
  })).optional(),
  projects: z.array(z.object({
    title: z.string().min(1),
    description: z.string().optional(),
  })).optional(),
  faqs: z.array(z.object({
    question: z.string().min(1),
    answer: z.string().min(1),
  })).optional(),
});

export type CourseFormData = z.infer<typeof courseSchema>;

// Course enrollment update validations
export const courseEnrollmentUpdateSchema = z.object({
  status: z.enum(['new', 'contacted', 'interested', 'enrolled', 'not_interested', 'closed']).optional(),
  notes: z.string().optional().or(z.literal('')),
  assigned_to: z.string().max(255).optional().or(z.literal('')),
  next_followup_at: z.string().optional().or(z.literal('')),
});

export type CourseEnrollmentUpdateFormData = z.infer<typeof courseEnrollmentUpdateSchema>;

