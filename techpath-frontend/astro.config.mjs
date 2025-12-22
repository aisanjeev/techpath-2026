import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';
import compress from 'astro-compress';
import vercel from '@astrojs/vercel';
import { loadEnv } from 'vite';

const env = loadEnv(process.env.NODE_ENV, process.cwd(), '');

export default defineConfig({
  site: 'https://techpath.biz',
  
  // Trailing slash configuration for consistent URLs
  trailingSlash: 'ignore',
  
  integrations: [
    react({ include: ['**/react-components/*.jsx'] }),
    tailwind({ applyBaseStyles: false }),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),
    robotsTxt(),
    compress({
      CSS: true,
      HTML: true,
      JavaScript: true,
      Image: false, // Let Vercel handle image optimization
      SVG: true,
    }),
  ],

  // Server mode with prerender = true by default for most pages
  // Use prerender = false for pages that need dynamic SSR
  output: 'server',
  adapter: vercel({
    // Enable Vercel's image optimization service
    imageService: true,
    // Enable Incremental Static Regeneration for better caching
    isr: {
      // Revalidate pages every hour (3600 seconds)
      expiration: 3600,
    },
    // Enable Vercel Web Analytics (free)
    webAnalytics: {
      enabled: true,
    },
    // Enable Vercel Speed Insights (free)
    speedInsights: {
      enabled: true,
    },
    // Max duration for serverless functions (seconds)
    maxDuration: 30,
  }),

  // Prefetch configuration for faster navigation
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'viewport',
  },

  vite: {
    define: {
      __API_BASE_URL__: JSON.stringify(env.VITE_API_BASE_URL || 'http://localhost:8000'),
    },
    build: {
      // Enable CSS code splitting for better caching
      cssCodeSplit: true,
      // Minify output
      minify: 'esbuild',
    },
  },

  image: {
    // Use Vercel's image optimization in production
    service: { entrypoint: 'astro/assets/services/sharp' },
    // Allowed remote image domains
    domains: ['techpath.biz'],
  },

  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },

  // Experimental features for better performance
  experimental: {
    clientPrerender: true,
  },
});

