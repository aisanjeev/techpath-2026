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
  
  integrations: [
    react({ include: ['**/react-components/*.jsx'] }),
    tailwind({ applyBaseStyles: false }),
    sitemap(),
    robotsTxt(),
    compress(),
  ],

  // Server mode with prerender = true by default for most pages
  // Use prerender = false for pages that need dynamic SSR
  output: 'server',
  adapter: vercel({
    // Enable image optimization on Vercel
    imageService: true,
    // Use serverless functions for dynamic routes
    isr: true,
  }),

  vite: {
    define: {
      __API_BASE_URL__: JSON.stringify(env.VITE_API_BASE_URL || 'http://localhost:8000'),
    },
  },

  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
  },

  markdown: {
    syntaxHighlight: 'shiki',
  },
});

