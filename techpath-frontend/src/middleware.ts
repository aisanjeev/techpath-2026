import { defineMiddleware } from 'astro:middleware';

/**
 * On non-production environments, inject X-Robots-Tag: noindex, nofollow
 * on every response. This is the most authoritative signal for crawlers
 * (takes precedence over meta tags and complements robots.txt).
 *
 * Set PUBLIC_SITE_ENV=production in the Vercel production project env vars
 * to enable indexing. All other values (staging, development, etc.) block it.
 */
export const onRequest = defineMiddleware(async (_context, next) => {
  const response = await next();

  if (import.meta.env.PUBLIC_SITE_ENV !== 'production') {
    response.headers.set('X-Robots-Tag', 'noindex, nofollow');
  }

  return response;
});
