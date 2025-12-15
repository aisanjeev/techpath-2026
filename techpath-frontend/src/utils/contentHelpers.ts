/**
 * Content Helper Utilities
 * Functions for processing and enhancing markdown content
 */

import type { CollectionEntry } from 'astro:content';

// ============================================
// Types
// ============================================

export interface TOCItem {
  title: string;
  level: number;
  id: string;
  children: TOCItem[];
}

export interface ImageMetadata {
  src: string;
  alt: string;
  title?: string;
}

export interface ArticleMeta {
  wordCount: number;
  readingTime: number;
  charCount: number;
}

// ============================================
// Reading Time Calculation
// ============================================

/**
 * Calculate reading time based on content
 * @param content - The text content (can be HTML or plain text)
 * @param wordsPerMinute - Reading speed (default: 200 wpm)
 * @returns Reading time in minutes
 */
export function calculateReadingTime(
  content: string,
  wordsPerMinute: number = 200
): number {
  // Strip HTML tags to get plain text
  const plainText = stripHtml(content);

  // Count words (split by whitespace)
  const words = plainText.trim().split(/\s+/).filter(Boolean);
  const wordCount = words.length;

  // Calculate reading time
  const minutes = Math.ceil(wordCount / wordsPerMinute);

  return Math.max(1, minutes); // Minimum 1 minute
}

/**
 * Get article statistics
 * @param content - The content to analyze
 * @returns Article metadata including word count and reading time
 */
export function getArticleStats(content: string): ArticleMeta {
  const plainText = stripHtml(content);
  const words = plainText.trim().split(/\s+/).filter(Boolean);

  return {
    wordCount: words.length,
    readingTime: calculateReadingTime(content),
    charCount: plainText.length,
  };
}

// ============================================
// Table of Contents Generation
// ============================================

/**
 * Extract headings from HTML content and build a TOC
 * @param html - HTML content string
 * @param maxLevel - Maximum heading level to include (default: 3)
 * @returns Array of TOC items with nested structure
 */
export function extractTableOfContents(
  html: string,
  maxLevel: number = 3
): TOCItem[] {
  const headingRegex = /<h([2-6])[^>]*id="([^"]*)"[^>]*>([\s\S]*?)<\/h[2-6]>/gi;
  const matches = [...html.matchAll(headingRegex)];

  const headings: { level: number; id: string; title: string }[] = matches
    .map((match) => ({
      level: parseInt(match[1], 10),
      id: match[2],
      title: stripHtml(match[3]).trim(),
    }))
    .filter((h) => h.level <= maxLevel && h.id && h.title);

  return buildTOCTree(headings);
}

/**
 * Build a nested TOC tree from flat heading list
 */
function buildTOCTree(
  headings: { level: number; id: string; title: string }[]
): TOCItem[] {
  const result: TOCItem[] = [];
  const stack: TOCItem[] = [];

  for (const heading of headings) {
    const item: TOCItem = {
      title: heading.title,
      level: heading.level,
      id: heading.id,
      children: [],
    };

    // Find the correct parent
    while (stack.length > 0 && stack[stack.length - 1].level >= heading.level) {
      stack.pop();
    }

    if (stack.length === 0) {
      result.push(item);
    } else {
      stack[stack.length - 1].children.push(item);
    }

    stack.push(item);
  }

  return result;
}

/**
 * Flatten a TOC tree into a simple list
 */
export function flattenTOC(toc: TOCItem[]): Omit<TOCItem, 'children'>[] {
  const result: Omit<TOCItem, 'children'>[] = [];

  function traverse(items: TOCItem[]) {
    for (const item of items) {
      result.push({ title: item.title, level: item.level, id: item.id });
      if (item.children.length > 0) {
        traverse(item.children);
      }
    }
  }

  traverse(toc);
  return result;
}

// ============================================
// Slug Generation
// ============================================

/**
 * Generate a URL-friendly slug from a title
 * @param title - The title to convert
 * @returns URL-safe slug
 */
export function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}

/**
 * Generate a slug with a prefix
 */
export function generatePrefixedSlug(title: string, prefix: string): string {
  return `${prefix}-${generateSlug(title)}`;
}

// ============================================
// Date Formatting
// ============================================

/**
 * Format a date for display
 * @param date - Date to format
 * @param format - Format style ('long', 'short', 'relative')
 * @returns Formatted date string
 */
export function formatDate(
  date: Date,
  format: 'long' | 'short' | 'relative' = 'long'
): string {
  if (format === 'relative') {
    return getRelativeTimeString(date);
  }

  const options: Intl.DateTimeFormatOptions =
    format === 'long'
      ? { year: 'numeric', month: 'long', day: 'numeric' }
      : { year: 'numeric', month: 'short', day: 'numeric' };

  return new Intl.DateTimeFormat('en-US', options).format(date);
}

/**
 * Get relative time string (e.g., "2 days ago")
 */
export function getRelativeTimeString(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;

  return `${Math.floor(diffDays / 365)} years ago`;
}

// ============================================
// Image Processing
// ============================================

/**
 * Extract all images from HTML content
 * @param html - HTML content string
 * @returns Array of image metadata
 */
export function parseMarkdownImages(html: string): ImageMetadata[] {
  const imgRegex = /<img[^>]*src="([^"]*)"[^>]*(?:alt="([^"]*)")?[^>]*(?:title="([^"]*)")?[^>]*>/gi;
  const images: ImageMetadata[] = [];

  let match;
  while ((match = imgRegex.exec(html)) !== null) {
    images.push({
      src: match[1],
      alt: match[2] || '',
      title: match[3],
    });
  }

  return images;
}

// ============================================
// Related Posts
// ============================================

type BlogEntry = CollectionEntry<'blog'>;

/**
 * Get related posts based on matching tags
 * @param currentPost - The current post
 * @param allPosts - All available posts
 * @param limit - Maximum number of related posts to return
 * @returns Array of related posts sorted by relevance
 */
export function getRelatedPosts(
  currentPost: BlogEntry,
  allPosts: BlogEntry[],
  limit: number = 3
): BlogEntry[] {
  const currentTags = currentPost.data.tags || [];

  if (currentTags.length === 0) {
    // Return random posts if no tags
    return allPosts
      .filter((post) => post.slug !== currentPost.slug)
      .slice(0, limit);
  }

  // Calculate relevance score based on matching tags
  const postsWithScore = allPosts
    .filter((post) => post.slug !== currentPost.slug)
    .map((post) => {
      const postTags = post.data.tags || [];
      const matchingTags = currentTags.filter((tag) => postTags.includes(tag));
      return {
        post,
        score: matchingTags.length,
      };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score);

  return postsWithScore.slice(0, limit).map((item) => item.post);
}

// ============================================
// Content Enhancement
// ============================================

/**
 * Add IDs to headings that don't have them
 * @param html - HTML content
 * @returns HTML with IDs added to headings
 */
export function addHeadingIds(html: string): string {
  return html.replace(
    /<h([2-6])([^>]*)>([^<]+)<\/h[2-6]>/gi,
    (match, level, attrs, text) => {
      // Check if already has an ID
      if (attrs.includes('id="')) {
        return match;
      }
      const id = generateSlug(text);
      return `<h${level}${attrs} id="${id}">${text}</h${level}>`;
    }
  );
}

/**
 * Wrap tables in a responsive container
 * @param html - HTML content
 * @returns HTML with tables wrapped
 */
export function wrapTables(html: string): string {
  return html.replace(
    /<table([^>]*)>/gi,
    '<div class="table-wrapper overflow-x-auto"><table$1>'
  );
}

/**
 * Add target="_blank" to external links
 * @param html - HTML content
 * @param domain - Your site's domain to identify internal links
 * @returns HTML with external link attributes
 */
export function enhanceExternalLinks(html: string, domain: string = ''): string {
  return html.replace(
    /<a([^>]*)href="(https?:\/\/[^"]+)"([^>]*)>/gi,
    (match, before, url, after) => {
      if (domain && url.includes(domain)) {
        return match; // Internal link
      }
      // Check if already has target
      if (before.includes('target=') || after.includes('target=')) {
        return match;
      }
      return `<a${before}href="${url}"${after} target="_blank" rel="noopener noreferrer">`;
    }
  );
}

// ============================================
// Utility Functions
// ============================================

/**
 * Strip HTML tags from a string
 * @param html - HTML string
 * @returns Plain text without HTML tags
 */
export function stripHtml(html: string): string {
  return html
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/&nbsp;/g, ' ') // Replace non-breaking spaces
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

/**
 * Truncate text to a certain length
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @param suffix - Suffix to add when truncated
 * @returns Truncated text
 */
export function truncateText(
  text: string,
  maxLength: number = 150,
  suffix: string = '...'
): string {
  if (text.length <= maxLength) return text;

  const truncated = text.substring(0, maxLength - suffix.length);
  // Try to break at a word boundary
  const lastSpace = truncated.lastIndexOf(' ');

  if (lastSpace > maxLength * 0.7) {
    return truncated.substring(0, lastSpace) + suffix;
  }

  return truncated + suffix;
}

/**
 * Extract excerpt from content
 * @param content - HTML or plain text content
 * @param maxLength - Maximum length of excerpt
 * @returns Plain text excerpt
 */
export function extractExcerpt(content: string, maxLength: number = 160): string {
  const plainText = stripHtml(content);
  return truncateText(plainText, maxLength);
}

/**
 * Convert content to plain text suitable for search indexing
 * @param html - HTML content
 * @returns Normalized plain text
 */
export function toSearchableText(html: string): string {
  return stripHtml(html)
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

