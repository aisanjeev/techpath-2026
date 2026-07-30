import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { fetchBlogPosts } from '@services/blogService';
import { fetchPages } from '@services/pagesService';

export const GET: APIRoute = async () => {
  const siteUrl = import.meta.env.SITE_URL || 'https://techpath.biz';

  // 1. Static pages
  const staticPages = [
    '',
    '/about',
    '/blog',
    '/blog/archive',
    '/careers',
    '/case-studies',
    '/classroom',
    '/contact',
    '/cookie-policy',
    '/faq',
    '/pricing',
    '/privacy',
    '/services',
    '/solutions',
    '/support',
    '/terms-of-service',
    '/testimonials',
    '/training'
  ];

  const staticUrls = staticPages.map(page => ({ url: page }));

  // 2. Fetch CMS database pages
  const cmsPages = await fetchPages({ limit: 1000 });
  const cmsUrls = cmsPages.map(page => ({
    url: `/${page.slug}`,
    lastmod: page.updated_at || page.published_at || page.created_at
  }));

  // 3. Fetch API blog posts
  const apiBlogPosts = await fetchBlogPosts({ limit: 1000 });
  const apiBlogUrls = apiBlogPosts.map(post => ({
    url: `/blog/${post.slug}`,
    lastmod: post.published_at || post.created_at
  }));

  // 4. Fetch local markdown blog posts
  const localBlogPosts = await getCollection('blog');
  const localBlogUrls = localBlogPosts.map(post => ({
    url: `/blog/${post.slug}`,
    lastmod: post.data.pubDate ? new Date(post.data.pubDate).toISOString() : undefined
  }));

  // 5. Combine and remove duplicates
  const allUrlsMap = new Map();
  [...staticUrls, ...cmsUrls, ...apiBlogUrls, ...localBlogUrls].forEach(item => {
    if (!allUrlsMap.has(item.url)) {
      allUrlsMap.set(item.url, item);
    }
  });
  
  const allPaths = Array.from(allUrlsMap.values());

  // 6. Generate XML
  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${allPaths
    .map(
      (pathObj) => {
        let lastmodXml = '';
        if (pathObj.lastmod) {
          try {
            lastmodXml = `\n    <lastmod>${new Date(pathObj.lastmod).toISOString()}</lastmod>`;
          } catch (e) {
            // Ignore invalid dates
          }
        }
        return `
  <url>
    <loc>${siteUrl}${pathObj.url}/</loc>${lastmodXml}
    <changefreq>weekly</changefreq>
    <priority>${pathObj.url === '' ? '1.0' : '0.7'}</priority>
  </url>`;
      }
    )
    .join('')}
</urlset>`;

  return new Response(sitemapXml, {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, stale-while-revalidate=86400'
    },
  });
};
