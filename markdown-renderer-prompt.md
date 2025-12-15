# Cursor Instructions: Beautiful Markdown Content Rendering in Astro

## Problem Statement
Middle content is coming from `.md` files in Astro content collections, and the default rendering doesn't look professional or visually appealing. Need a complete design solution for markdown content display.

## Current Setup
- Using Astro content collections to load `.md` files
- Rendering markdown content via `getCollection()`
- Need custom styling and component enhancements
- Following TechPath design system guidelines

---

## Solution Architecture

### Step 1: Create a Custom Markdown Renderer Component

Create: `src/components/MarkdownRenderer.astro`

This component should:
- Accept parsed markdown HTML and frontmatter data
- Apply beautiful, semantic styling using Tailwind CSS
- Support all markdown elements (headers, lists, code blocks, blockquotes, tables)
- Include syntax highlighting for code blocks
- Add image optimization and lazy loading
- Implement responsive typography
- Add reading time estimation
- Include table of contents generation (optional)

### Step 2: Enhance Markdown Styling

Create: `src/styles/markdown.css`

This stylesheet should:
- Style all markdown elements with professional typography
- Create visual hierarchy with appropriate font sizes and weights
- Add proper spacing (margins, padding, line-height)
- Style code blocks with dark theme and syntax colors
- Add visual emphasis for blockquotes and callout boxes
- Style tables with alternating row colors and borders
- Add underlines/hover effects for links
- Implement responsive design for mobile devices

### Step 3: Create Content Layout

Modify: `src/layouts/BlogLayout.astro` or `src/layouts/DocumentationLayout.astro`

This layout should:
- Use the MarkdownRenderer component
- Add sidebar for table of contents (optional)
- Include author information and metadata
- Add share buttons (optional)
- Include related content suggestions
- Add comment section (optional)
- Responsive grid layout

### Step 4: Visual Enhancements

Additional elements to add:
- Syntax-highlighted code blocks (using Shiki or Highlight.js)
- Callout/admonition boxes (Note, Warning, Tip, Danger)
- Image galleries/lightbox support
- Embedded videos (YouTube, Vimeo)
- Social media embeds
- Custom dividers and spacing elements

---

## Cursor Commands to Execute

### Command 1: Create Beautiful Markdown Renderer Component

**File Path:** `src/components/MarkdownRenderer.astro`

```
Create a professional Astro component that renders markdown content with beautiful styling.

Requirements:
1. Accept these props:
   - content: HTML string (from astro:content)
   - title: string (from frontmatter)
   - description: string (from frontmatter)
   - author: string (from frontmatter, optional)
   - pubDate: Date (from frontmatter, optional)
   - readingTime: number (in minutes, optional)
   - image: string (cover image, optional)
   - tags: string[] (from frontmatter, optional)

2. Features:
   - Render HTML content with semantic markup
   - Calculate and display reading time
   - Show article metadata (author, date, tags)
   - Add breadcrumb navigation
   - Responsive typography (mobile, tablet, desktop)
   - Professional spacing and layout
   - Syntax highlighting for code blocks
   - Styled lists, tables, blockquotes
   - Image optimization with lazy loading
   - Link styling with hover effects

3. Design requirements (using TechPath design system):
   - Use Tailwind CSS utilities
   - Follow color scheme from guidelines
   - Ensure WCAG AA accessibility
   - Mobile-first responsive design
   - Professional fonts (Inter for sans-serif)
   - Code font (Fira Code for monospace)

4. Include these sections:
   - Header with title, metadata, featured image
   - Content wrapper with proper max-width and margins
   - Table of contents sidebar (optional, collapsible on mobile)
   - Reading time indicator
   - Author bio section
   - Tags display
   - Related posts section (optional)
   - Share buttons (optional)
   - Comment section placeholder

Use modern CSS Grid and Flexbox. Ensure excellent typography with proper line-height, letter-spacing, and font sizing.
```

### Command 2: Create Markdown-Specific Styling

**File Path:** `src/styles/markdown.css`

```
Create a comprehensive CSS file for styling markdown-rendered content.

Include styling for:
1. Typography:
   - h1, h2, h3, h4, h5, h6 (with proper hierarchy)
   - Paragraphs with good line-height (1.6-1.8)
   - Letter-spacing and font-weight variations
   - Text colors (primary, secondary, muted)

2. Lists:
   - Unordered lists with custom bullets
   - Ordered lists with proper numbering
   - Nested lists with indentation
   - List item spacing

3. Code:
   - Inline code styling
   - Code block styling (dark background)
   - Syntax highlighting colors
   - Line numbers (optional)
   - Copy-to-clipboard button (optional)

4. Blockquotes:
   - Left border accent
   - Italic styling
   - Background color
   - Proper spacing

5. Tables:
   - Responsive table design
   - Alternating row colors
   - Border styling
   - Header styling
   - Overflow handling for mobile

6. Links:
   - Color styling
   - Underline styling
   - Hover effects
   - Visited state
   - External link indicators (optional)

7. Horizontal Rules:
   - Styled dividers
   - Proper spacing

8. Images:
   - Responsive sizing
   - Rounded corners
   - Subtle shadows
   - Captions support
   - Lazy loading

9. Special Boxes:
   - Info boxes
   - Warning boxes
   - Success boxes
   - Tip boxes
   - Danger boxes

All styling should use Tailwind utilities where possible and CSS custom properties for colors.
```

### Command 3: Create Callout/Admonition Component

**File Path:** `src/components/Callout.astro`

```
Create an Astro component for styled callout/admonition boxes.

Types:
- info (blue)
- warning (yellow/orange)
- success (green)
- danger/error (red)
- tip (purple)
- note (gray)

Props:
- type: 'info' | 'warning' | 'success' | 'danger' | 'tip' | 'note'
- title: string (optional)

Features:
- Icon for each type
- Colored left border
- Subtle background color
- Proper spacing
- Support for nested markdown

Can be used in markdown files like:
<Callout type="warning" title="Important">
  This is a warning message with important information.
</Callout>
```

### Command 4: Create Blog/Documentation Layout

**File Path:** `src/layouts/ArticleLayout.astro`

```
Create a comprehensive Astro layout for blog posts and documentation pages.

Structure:
1. Breadcrumb navigation at top
2. Title and metadata (author, date, reading time)
3. Featured image (if provided)
4. Table of contents sidebar (sticky, collapsible on mobile)
5. Main content area with MarkdownRenderer component
6. Post metadata (tags, categories)
7. Author bio section
8. Related posts/articles section
9. Navigation to previous/next posts
10. Share buttons
11. Comments section
12. Footer

Features:
- Responsive grid layout (sidebar + content)
- Sticky TOC on desktop
- Mobile-optimized navigation
- SEO-optimized metadata
- Schema markup (Article, BreadcrumbList)
- Dark mode support (optional)
- Print-friendly styling

Should accept props:
- frontmatter (title, author, date, etc.)
- content (rendered HTML)
- relatedPosts (array of related articles)
- onPage (current page path for breadcrumbs)
```

### Command 5: Create Code Block Component (Enhanced)

**File Path:** `src/components/CodeBlock.astro`

```
Create an enhanced code block component with syntax highlighting.

Features:
1. Syntax highlighting using Shiki
2. Language badge (showing which language)
3. Copy-to-clipboard button
4. Line numbers (toggle option)
5. Highlight specific lines
6. Support for code block titles/filenames
7. Dark theme styling
8. Responsive overflow handling

Props:
- code: string (the code to display)
- language: string (programming language)
- title: string (optional filename or title)
- highlightLines: number[] (optional lines to highlight)
- showLineNumbers: boolean (default: true)

Usage:
<CodeBlock
  language="typescript"
  title="example.ts"
  code={`const greeting = "Hello, World!";`}
  highlightLines={[1]}
/>
```

### Command 6: Update Content Collections Config

**File Path:** `src/content/config.ts`

```
Update the Content Collections configuration to include:

1. Schema extensions:
   - author: string or reference to authors collection
   - image: string (cover image path)
   - tags: string[] (for categorization)
   - draft: boolean (for draft posts)
   - readingTime: number (calculate automatically)
   - description: string (better than auto-generated)
   - category: string (blog category)

2. Add slug validation:
   - Enforce consistent slug format
   - Validate no spaces or special characters
   - Ensure uniqueness

3. Add computed fields:
   - Automatic reading time calculation
   - Automatic word count
   - Automatic URL slug generation

This ensures consistency across all markdown content.
```

### Command 7: Create Content Processing Utility

**File Path:** `src/utils/contentHelpers.ts`

```
Create utility functions for content processing:

Functions needed:
1. calculateReadingTime(content: string): number
   - Returns reading time in minutes
   - Based on average reading speed (200 words/min)

2. extractTableOfContents(html: string): TOCItem[]
   - Extracts headers from HTML
   - Creates TOC tree structure
   - Includes heading levels and IDs

3. generateSlug(title: string): string
   - Creates URL-friendly slug from title
   - Handles special characters and spaces

4. formatDate(date: Date): string
   - Formats date for display
   - Supports different formats

5. highlightCode(code: string, language: string): string
   - Applies syntax highlighting
   - Uses Shiki or similar library

6. parseMarkdownImages(html: string): ImageMetadata[]
   - Extracts all images from markdown
   - Useful for image optimization and gallery

7. getRelatedPosts(currentPost: Post, allPosts: Post[], limit: number): Post[]
   - Finds related posts by tags or category
   - Returns top N results

These utilities make content handling consistent and reusable.
```

### Command 8: Create Article Type Definitions

**File Path:** `src/types/article.ts`

```
Create TypeScript type definitions for article/blog posts.

Types needed:
1. ArticleFrontmatter
   - title: string
   - description: string
   - pubDate: Date
   - author: string
   - image: string
   - tags: string[]
   - category: string
   - draft: boolean
   - readingTime: number

2. Article
   - id: string
   - slug: string
   - data: ArticleFrontmatter
   - body: string
   - render: () => Promise<RenderedContent>

3. RenderedContent
   - html: string
   - metadata: ArticleFrontmatter

4. TOCItem
   - title: string
   - level: number
   - id: string
   - children: TOCItem[]

5. RelatedPost
   - slug: string
   - title: string
   - image: string
   - category: string

These types provide type safety across the application.
```

### Command 9: Create Page Component for Blog/Docs Pages

**File Path:** `src/pages/blog/[slug].astro` or `src/pages/docs/[slug].astro`

```
Create a dynamic page component that:

1. Gets all articles from content collection
2. For each article:
   - Render using ArticleLayout
   - Pass frontmatter, content, and related posts
   - Generate breadcrumbs
   - Generate table of contents

3. Features:
   - Syntax highlighting in code blocks
   - Responsive images
   - Mobile-friendly layout
   - SEO optimization (title, meta, schema)
   - Social media meta tags
   - Reading time estimation
   - Author information
   - Related articles sidebar

4. Error handling:
   - 404 for missing articles
   - Fallback for rendering errors
   - Proper error messages

5. Performance:
   - Pre-render at build time
   - Cache static assets
   - Lazy load images
   - Minimal JavaScript

This creates the actual pages that display your markdown content.
```

### Command 10: Styling Framework Setup

**File Path:** `src/styles/globals.css`

```
Create or update the global styles file to include:

1. CSS Reset:
   - Normalize default browser styles
   - Box-sizing: border-box for all elements
   - Remove default margins/paddings

2. Theme Variables:
   - Define CSS custom properties
   - Colors (primary, secondary, gray scale)
   - Typography (font families, sizes, weights)
   - Spacing (margins, padding scale)
   - Shadows
   - Border radius

3. Typography Styles:
   - Base font family and size
   - Line height for body text
   - Letter spacing
   - Font smoothing (antialiasing)

4. Color System:
   - Light mode colors
   - Dark mode colors (with prefers-color-scheme)
   - Semantic colors (success, error, warning, info)

5. Utility Classes:
   - Content wrapper (.content-wrapper, max-width, margins)
   - Typography utilities
   - Spacing utilities
   - Responsive utilities

6. Animation/Transitions:
   - Smooth transitions for interactive elements
   - Keyframe animations if needed
   - Reduced motion preferences

This creates the visual foundation for beautiful markdown rendering.
```

---

## Implementation Order

1. **First:** Create markdown styling CSS (Command 2)
2. **Second:** Create markdown renderer component (Command 1)
3. **Third:** Create callout/admonition component (Command 3)
4. **Fourth:** Create code block component (Command 5)
5. **Fifth:** Create article layout (Command 4)
6. **Sixth:** Update content config (Command 6)
7. **Seventh:** Create utility functions (Command 7)
8. **Eighth:** Create type definitions (Command 8)
9. **Ninth:** Update globals styles if needed (Command 10)
10. **Tenth:** Update page components to use new layout (Command 9)

---

## Key Design Principles for Cursor

When asking Cursor to build these components, emphasize:

1. **Professional Typography:**
   - Use proper font hierarchy
   - Implement good line-height (1.6-1.8 for body)
   - Consistent letter-spacing
   - Responsive font sizes

2. **Visual Hierarchy:**
   - Clear h1, h2, h3 differentiation
   - Color contrast for readability
   - Proper use of white space
   - Clear separation between sections

3. **Accessibility:**
   - WCAG AA color contrast
   - Semantic HTML
   - Proper heading hierarchy
   - Keyboard navigation support
   - Screen reader friendly

4. **Responsive Design:**
   - Mobile-first approach
   - Readable on all screen sizes
   - Proper touch targets
   - Adaptive layouts

5. **Performance:**
   - Lazy-load images
   - Syntax highlighting at build time
   - Minimal JavaScript
   - CSS-only animations

6. **User Experience:**
   - Clear call-to-action buttons
   - Related content suggestions
   - Easy navigation
   - Social sharing options
   - Comment capability (optional)

---

## Example Prompt for Cursor

You can copy-paste this entire prompt into Cursor and say:

> "Using the Astro-FastAPI guidelines document I've shared, and following the TechPath design system, please help me implement a beautiful markdown content renderer. Start by creating the components and styles in the order specified. I want my blog posts and documentation pages to look professional and be highly readable. Include code syntax highlighting, responsive design, and all the components listed. Make sure everything integrates seamlessly with my current Astro setup."

---

## Testing Checklist After Implementation

- [ ] Markdown renders with proper styling
- [ ] Code blocks have syntax highlighting
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Images load and display properly
- [ ] Links are styled and clickable
- [ ] Tables display correctly
- [ ] Blockquotes are visually distinct
- [ ] Lists are properly indented
- [ ] Reading time is calculated correctly
- [ ] Author info displays
- [ ] Tags are clickable
- [ ] Related posts show
- [ ] TOC generates correctly
- [ ] Accessibility is maintained
- [ ] Performance is good
- [ ] Dark mode works (if implemented)
- [ ] Share buttons work
- [ ] SEO meta tags are correct

---

## Additional Resources

- [Tailwind Typography Plugin](https://tailwindcss.com/docs/plugins#typography)
- [Shiki Syntax Highlighter](https://shiki.matsu.io/)
- [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Web Typography Best Practices](https://www.smashingmagazine.com/category/typography)

---

## Notes

- This approach keeps markdown content separate from styling
- All styling uses Tailwind CSS for consistency
- Components are reusable across different content types
- Designed for SEO optimization with proper semantic HTML
- Follows TechPath design system guidelines
- Performance optimized with lazy loading and build-time processing
- Accessibility-first approach with WCAG AA compliance
