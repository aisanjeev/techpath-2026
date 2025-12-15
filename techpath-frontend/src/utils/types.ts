/**
 * TypeScript Type Definitions
 */

// API Response Types
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  timestamp?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Contact Form
export interface ContactFormData {
  name: string;
  email: string;
  company?: string;
  message: string;
  service?: string;
}

// Newsletter
export interface NewsletterSubscription {
  email: string;
}

// Service Inquiry
export interface ServiceInquiry {
  name: string;
  email: string;
  company?: string;
  service: string;
  budget?: string;
  timeline?: string;
  description: string;
}

// Blog Post
export interface BlogPost {
  slug: string;
  title: string;
  description: string;
  content: string;
  pubDate: Date;
  author: string;
  image?: string;
  tags: string[];
  readingTime?: number;
}

// Service
export interface Service {
  slug: string;
  title: string;
  description: string;
  icon: string;
  features: string[];
  price?: string;
  cta: string;
}

// Team Member
export interface TeamMember {
  name: string;
  role: string;
  bio: string;
  image?: string;
  social?: {
    twitter?: string;
    linkedin?: string;
    github?: string;
  };
}

// Testimonial
export interface Testimonial {
  quote: string;
  author: string;
  role: string;
  company: string;
  avatar?: string;
  rating?: number;
}

// Case Study
export interface CaseStudy {
  slug: string;
  title: string;
  description: string;
  client: string;
  industry: string;
  image?: string;
  tags: string[];
  results: {
    metric: string;
    value: string;
    description?: string;
  }[];
}

// Job Opening
export interface JobOpening {
  title: string;
  department: string;
  location: string;
  type: 'Full-time' | 'Part-time' | 'Contract';
  href: string;
  description?: string;
  requirements?: string[];
}

// Pricing Plan
export interface PricingPlan {
  name: string;
  description: string;
  price: string;
  period: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

// FAQ
export interface FAQ {
  question: string;
  answer: string;
}

// Navigation
export interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}

// Breadcrumb
export interface BreadcrumbItem {
  label: string;
  href: string;
  current?: boolean;
}

// Stat Counter
export interface Stat {
  value: string;
  label: string;
}

// Feature
export interface Feature {
  title: string;
  description: string;
  icon: string;
}

// Social Link
export interface SocialLink {
  label: string;
  href: string;
  icon: string;
}

// SEO Props
export interface SEOProps {
  title: string;
  description?: string;
  image?: string;
  canonicalUrl?: string;
  noIndex?: boolean;
  type?: 'website' | 'article' | 'product';
  publishedTime?: string;
  modifiedTime?: string;
  author?: string;
  tags?: string[];
}

