# TechPath Frontend Architecture

## Overview

TechPath's frontend is built with **Astro 5**, a modern web framework that prioritizes performance through its static-first approach with optional server-side rendering.

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Astro 5 | Static site generation + SSR |
| UI Components | Astro Components | Reusable UI elements |
| Styling | Tailwind CSS | Utility-first CSS |
| Interactivity | React (Islands) | Interactive components |
| Content | Content Collections | Markdown/MDX content |
| Type Safety | TypeScript | Static type checking |

## Directory Structure

```
src/
├── layouts/           # Page layouts (MainLayout, BlogLayout, etc.)
├── pages/            # File-based routing
│   ├── api/          # API endpoints
│   ├── services/     # Service pages
│   │   └── _components/  # Page-specific components
│   ├── blog/         # Blog pages
│   └── ...
├── components/       # Reusable components
│   ├── shared/       # Global components (Header, Footer)
│   ├── sections/     # Page sections (Hero, Features)
│   ├── ui/           # Base UI components (Button, Card)
│   └── forms/        # Form components (Input, Select)
├── content/          # Content Collections
│   ├── blog/         # Blog posts (Markdown)
│   ├── services/     # Service content
│   └── config.ts     # Collection schemas
├── styles/           # Global styles
├── utils/            # Utility functions
└── env.d.ts          # Environment type definitions
```

## Key Concepts

### Astro Islands

Interactive components are rendered as "islands" of interactivity in a sea of static HTML:

```astro
---
import InteractiveWidget from '../components/InteractiveWidget.tsx';
---

<div>
  <!-- Static HTML -->
  <h1>Welcome</h1>
  
  <!-- Interactive Island -->
  <InteractiveWidget client:load />
</div>
```

### Content Collections

Type-safe content management with Zod schemas:

```typescript
// src/content/config.ts
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    // ...
  }),
});
```

### API Routes

Server-side API endpoints in `/pages/api/`:

```typescript
// src/pages/api/contact.ts
export const POST: APIRoute = async ({ request }) => {
  const data = await request.json();
  // Handle form submission
  return new Response(JSON.stringify({ success: true }));
};
```

## Performance Targets

- **Lighthouse Performance**: 95+
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Cumulative Layout Shift**: < 0.1

## Deployment

- **Platform**: Vercel
- **Build Command**: `npm run build`
- **Output**: `dist/`
- **Environment**: Node.js 20+

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

