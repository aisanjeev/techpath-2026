/**
 * Application Constants
 */

// Site Information
export const SITE = {
  name: 'TechPath',
  tagline: 'AI-Powered IT Solutions for Modern Enterprises',
  description:
    'Transform your business with cutting-edge AI, cloud infrastructure, and custom software solutions.',
  url: 'https://techpath.biz',
  email: 'hello@techpath.biz',
  phone: '+1 (555) 123-4567',
  address: 'San Francisco, CA',
} as const;

// Social Links
export const SOCIAL_LINKS = {
  twitter: 'https://twitter.com/techpath',
  linkedin: 'https://linkedin.com/company/techpath',
  github: 'https://github.com/techpath',
} as const;

// Navigation Links
export const NAV_LINKS = [
  { label: 'Services', href: '/services' },
  { label: 'Solutions', href: '/solutions' },
  { label: 'Case Studies', href: '/case-studies' },
  { label: 'Blog', href: '/blog' },
  { label: 'About', href: '/about' },
  { label: 'Pricing', href: '/pricing' },
] as const;

// Services
export const SERVICES = [
  {
    slug: 'ai-consulting',
    title: 'AI & Machine Learning',
    shortDescription: 'Custom AI solutions powered by cutting-edge ML models.',
    icon: 'brain',
  },
  {
    slug: 'cloud-services',
    title: 'Cloud Infrastructure',
    shortDescription: 'Scalable cloud architecture on AWS, Azure, and GCP.',
    icon: 'cloud',
  },
  {
    slug: 'web-development',
    title: 'Web Development',
    shortDescription: 'Modern, performant web applications.',
    icon: 'code',
  },
  {
    slug: 'data-analytics',
    title: 'Data Analytics',
    shortDescription: 'Transform data into actionable insights.',
    icon: 'chart',
  },
  {
    slug: 'cybersecurity',
    title: 'Cybersecurity',
    shortDescription: 'Enterprise-grade security solutions.',
    icon: 'shield',
  },
  {
    slug: 'digital-transformation',
    title: 'Digital Transformation',
    shortDescription: 'End-to-end modernization consulting.',
    icon: 'transform',
  },
] as const;

// Animation Defaults
export const ANIMATION = {
  duration: {
    fast: 150,
    normal: 200,
    slow: 300,
  },
  easing: {
    default: 'ease-out',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

// Breakpoints (matching Tailwind)
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;

// Pagination Defaults
export const PAGINATION = {
  defaultLimit: 10,
  maxLimit: 100,
} as const;

