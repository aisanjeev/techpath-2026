import type { APIRoute } from 'astro';

export const GET: APIRoute = () => {
  const isProduction = import.meta.env.PUBLIC_SITE_ENV === 'production';
  const siteUrl = import.meta.env.SITE_URL || 'https://techpath.biz';

  const content = isProduction
    ? [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /api/',
        'Disallow: /_astro/',
        '',
        `Sitemap: ${siteUrl}/sitemap-index.xml`,
      ].join('\n')
    : [
        '# Non-production environment — block all crawlers',
        'User-agent: *',
        'Disallow: /',
      ].join('\n');

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
