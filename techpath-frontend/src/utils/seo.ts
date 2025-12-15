/**
 * SEO Utilities
 */

import { SITE } from './constants';

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

/**
 * Generates meta tags for SEO
 */
export function generateMetaTags(props: SEOProps) {
  const {
    title,
    description = SITE.description,
    image = '/images/og-image.jpg',
    canonicalUrl,
    noIndex = false,
    type = 'website',
    publishedTime,
    modifiedTime,
    author,
    tags = [],
  } = props;

  const fullTitle = `${title} | ${SITE.name}`;
  const fullUrl = canonicalUrl || SITE.url;
  const fullImageUrl = image.startsWith('http') ? image : `${SITE.url}${image}`;

  return {
    title: fullTitle,
    description,
    canonical: fullUrl,
    openGraph: {
      type,
      url: fullUrl,
      title: fullTitle,
      description,
      image: fullImageUrl,
      siteName: SITE.name,
      ...(publishedTime && { publishedTime }),
      ...(modifiedTime && { modifiedTime }),
      ...(author && { author }),
      ...(tags.length > 0 && { tags }),
    },
    twitter: {
      card: 'summary_large_image',
      url: fullUrl,
      title: fullTitle,
      description,
      image: fullImageUrl,
    },
    robots: noIndex ? 'noindex, nofollow' : 'index, follow',
  };
}

/**
 * Generates JSON-LD structured data for an organization
 */
export function generateOrganizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: SITE.name,
    url: SITE.url,
    logo: `${SITE.url}/images/logo.svg`,
    description: SITE.description,
    email: SITE.email,
    telephone: SITE.phone,
    address: {
      '@type': 'PostalAddress',
      addressLocality: SITE.address,
    },
    sameAs: [
      'https://twitter.com/techpath',
      'https://linkedin.com/company/techpath',
      'https://github.com/techpath',
    ],
  };
}

/**
 * Generates JSON-LD structured data for a blog post
 */
export function generateArticleSchema(props: {
  title: string;
  description: string;
  url: string;
  image?: string;
  publishedTime: string;
  modifiedTime?: string;
  author: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: props.title,
    description: props.description,
    url: props.url,
    image: props.image ? `${SITE.url}${props.image}` : undefined,
    datePublished: props.publishedTime,
    dateModified: props.modifiedTime || props.publishedTime,
    author: {
      '@type': 'Person',
      name: props.author,
    },
    publisher: {
      '@type': 'Organization',
      name: SITE.name,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE.url}/images/logo.svg`,
      },
    },
  };
}

/**
 * Generates JSON-LD structured data for a service
 */
export function generateServiceSchema(props: {
  name: string;
  description: string;
  url: string;
  price?: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name: props.name,
    description: props.description,
    url: props.url,
    provider: {
      '@type': 'Organization',
      name: SITE.name,
      url: SITE.url,
    },
    ...(props.price && {
      offers: {
        '@type': 'Offer',
        price: props.price,
        priceCurrency: 'USD',
      },
    }),
  };
}

/**
 * Generates JSON-LD structured data for breadcrumbs
 */
export function generateBreadcrumbSchema(items: { name: string; url: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `${SITE.url}${item.url}`,
    })),
  };
}

/**
 * Generates JSON-LD structured data for FAQ
 */
export function generateFAQSchema(faqs: { question: string; answer: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };
}

