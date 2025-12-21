# Next.js Admin Panel - Best Practices & Architecture Guide

**For Cursor AI Agent Implementation**
**TechPath CMS Admin - Modern Enterprise Grade**

---

## 1. PROJECT STRUCTURE & ORGANIZATION

### Recommended Directory Layout
```
apps/admin/
├── src/
│   ├── app/
│   │   ├── layout.tsx                 # Root layout with auth wrapper
│   │   ├── page.tsx                   # Dashboard
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── setup/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx             # Sidebar + top nav layout
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── services/
│   │   │   │   ├── page.tsx           # List view
│   │   │   │   ├── [id]/page.tsx      # Detail/edit view
│   │   │   │   └── create/page.tsx    # Create view
│   │   │   ├── blog/
│   │   │   ├── case-studies/
│   │   │   ├── contact/inquiries/
│   │   │   ├── newsletter/
│   │   │   └── users/
│   │   └── api/                       # API routes for client-side operations
│   │       └── upload/route.ts        # Image upload handler
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── TopNav.tsx
│   │   │   ├── Breadcrumb.tsx
│   │   │   └── MainLayout.tsx
│   │   ├── editors/
│   │   │   ├── RichTextEditor.tsx     # Tiptap-based rich text + markdown
│   │   │   ├── MarkdownPreview.tsx
│   │   │   └── EditorToolbar.tsx
│   │   ├── forms/
│   │   │   ├── ServiceForm.tsx
│   │   │   ├── BlogPostForm.tsx
│   │   │   ├── CaseStudyForm.tsx
│   │   │   └── DynamicFormBuilder.tsx
│   │   ├── tables/
│   │   │   ├── DataTable.tsx          # Reusable table with sorting/pagination
│   │   │   ├── ServiceTable.tsx
│   │   │   └── BlogTable.tsx
│   │   ├── media/
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── ImageGallery.tsx
│   │   │   └── FeaturedImagePicker.tsx
│   │   ├── status/
│   │   │   ├── StatusBadge.tsx        # Published/Draft/Archived
│   │   │   ├── FeatureBadge.tsx
│   │   │   └── ActiveToggle.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Modal.tsx
│   │       ├── Dialog.tsx
│   │       ├── Toast.tsx
│   │       ├── Spinner.tsx
│   │       └── SkeletonLoader.tsx
│   ├── lib/
│   │   ├── api-client.ts              # Axios/Fetch wrapper for API calls
│   │   ├── auth.ts                    # JWT token management
│   │   ├── validations.ts             # Zod schemas for all forms
│   │   ├── constants.ts               # Status enums, default values
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useApi.ts              # Custom hook for API calls with loading/error
│   │   │   ├── usePagination.ts
│   │   │   ├── useDebounce.ts
│   │   │   └── useFormState.ts
│   │   └── utils/
│   │       ├── format.ts              # Formatting utilities
│   │       ├── slugify.ts
│   │       └── file-upload.ts         # File handling utilities
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── services.service.ts
│   │   ├── blog.service.ts
│   │   ├── case-studies.service.ts
│   │   ├── contacts.service.ts
│   │   └── newsletter.service.ts
│   ├── store/
│   │   ├── auth.store.ts              # Zustand for auth state
│   │   ├── ui.store.ts                # Sidebar collapsed, theme, etc.
│   │   └── editor.store.ts            # Editor draft state
│   ├── types/
│   │   ├── api.ts                     # API response types from Swagger
│   │   ├── forms.ts                   # Form schema types
│   │   └── ui.ts                      # UI component types
│   └── styles/
│       ├── globals.css                # Tailwind + custom properties
│       └── editor.css                 # Rich text editor styling
├── .env.local
├── tailwind.config.ts
└── next.config.ts
```

---

## 2. AUTHENTICATION & SECURITY

### JWT Token Management
- **Store tokens in HTTP-only cookies** (server-side, not localStorage)
- Implement token refresh mechanism (access token + refresh token)
- Create middleware for protected routes
- Clear tokens on logout
- Validate token expiration before API calls

### Authorization Pattern
```
Middleware flow:
User Request → Auth Middleware (verify JWT) → Check Role (RBAC) → Route Handler
```

### Environment Variables
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
API_BASE_URL=http://backend:8000  # For server-side calls
JWT_SECRET=your-secret-key
NEXT_PUBLIC_APP_NAME=TechPath Admin
```

---

## 3. RICH TEXT EDITOR & MARKDOWN STRATEGY

### Editor Technology Stack
**Choose: Tiptap + ProseMirror** (not Quill/Draft.js)

**Why Tiptap:**
- Native Markdown support
- Headless architecture (complete UI control)
- ProseMirror foundation (battle-tested)
- Extension ecosystem
- Works perfectly with Next.js 13+ App Router

### Core Extensions to Include
```
✓ Starter Kit (basic formatting)
✓ Markdown (parse/export markdown)
✓ Link (configurable, open in new tab)
✓ Image (inline images with resizing)
✓ Code Block with Syntax Highlighting (with Lowlight)
✓ Table (for structured content)
✓ Text Align (left/center/right/justify)
✓ Heading (h1-h6)
✓ Bullet List & Ordered List
✓ Blockquote
✓ Horizontal Rule
✓ Subscript/Superscript
✓ Color highlighting
✓ Collaboration (optional, for multi-editor support)
```

### Editor UI/UX Pattern
```
┌─────────────────────────────────────────────┐
│ Toolbar (Fixed)                             │
│ [B][I][U] | [H1][H2][H3] | [L][C][R][J]   │
│ [Link] [Code] [Quote] | [Undo][Redo]      │
│ [Image Upload] [Table] [More...]          │
├─────────────────────────────────────────────┤
│ Editor Content (Scrollable)                 │
│ Rich text editing area with placeholder     │
│ Character count: 245/5000                   │
├─────────────────────────────────────────────┤
│ [Toggle Preview] [Save Draft]  [Publish]  │
└─────────────────────────────────────────────┘
```

### Dual Mode Editor
Implement toggle between:
1. **Rich Text Mode** (WYSIWYG - default)
2. **Markdown Source Mode** (Raw markdown with syntax highlighting)

### Image Handling in Editor
- **Image Upload**: Drag-drop or click to upload
- **Supported formats**: JPG, PNG, WebP, GIF (max 5MB)
- **Storage**: Upload to CDN or S3, store URL in database
- **Optimization**: Serve via image CDN with responsive sizing
- **Fallback**: Unsplash integration for placeholder selection

### Content Validation
```
For BlogPost content field:
- Minimum: 10 characters
- Maximum: 50,000 characters
- Must contain at least one heading or paragraph
- No empty code blocks
- All links validated (regex check, optional DNS check)
```

---

## 4. FORM MANAGEMENT & VALIDATION

### Schema-Based Validation (Zod)
Define schemas for every resource:
```
✓ ServiceCreate / ServiceUpdate schemas
✓ BlogPostCreate / BlogPostUpdate schemas
✓ CaseStudyCreate / CaseStudyUpdate schemas
✓ ContactInquiry schemas
✓ Newsletter schemas
✓ User schemas
```

### Form State Management
- **Use React Hook Form** (lightweight, performant)
- Integrate with Zod for validation
- Handle nested arrays (tags, features, stats)
- Implement autosave drafts to localStorage
- Show validation errors inline with clear messages

### Form Patterns by Resource Type

**Services Form:**
- Title (required, max 255)
- Slug (auto-generate from title, allow edit)
- Description (rich text, min 10 chars)
- Short description (optional, textarea, max 500)
- Features (array of strings - dynamic add/remove)
- Icon (selector from icon library or upload)
- Image URL (featured image picker)
- Price (optional)
- CTA Text & URL
- Featured toggle
- Display order (number)
- Active toggle
- Meta title & description (SEO fields)

**Blog Post Form:**
- Title, Slug (same pattern)
- Content (rich text editor - Tiptap)
- Excerpt (optional, textarea)
- Featured image picker
- Status dropdown (draft/published/archived)
- Published date (datetime picker)
- Featured toggle
- Reading time (auto-calculated)
- Tags (multi-select with tag manager)
- Meta fields (title, description)

**Case Study Form:**
- Title, Slug
- Client name (required)
- Industry (dropdown or text)
- Challenge, Solution, Results (rich text fields)
- Excerpt, Content
- Featured image
- Statistics section (stat_value, stat_label, additional_stats JSON)
- Testimonial section (quote, author, role)
- Status, featured, published date
- Tags
- Meta fields

---

## 5. DATA TABLE & LIST VIEW PATTERNS

### Generic DataTable Component
```
Props:
- columns: ColumnDef<T>[]
- data: T[]
- isLoading: boolean
- onEdit: (row: T) => void
- onDelete: (id: number) => void
- onView: (row: T) => void
- pagination: { page, limit, total }
- onPaginationChange: (page, limit) => void
- sorting: { field, direction }
- onSortChange: (field, direction) => void
- filtering: { searchTerm, filters }
- onFilterChange: (filters) => void
```

### Table Features
- **Column sorting** (click header to sort ascending/descending)
- **Pagination** (10/20/50 items per page)
- **Row selection** (multi-select with checkbox, bulk actions)
- **Search** (client-side + server-side filtering)
- **Status badges** (color-coded: draft, published, active, etc.)
- **Inline actions** (edit, view, delete in row actions menu)
- **Loading skeleton** (show while fetching)
- **Empty state** (helpful message + CTA)
- **Responsive** (horizontal scroll on mobile)

### Bulk Actions
- Select multiple rows
- Bulk publish/unpublish
- Bulk delete with confirmation
- Bulk status change
- Bulk tag assignment

---

## 6. UI COMPONENT LIBRARY & DESIGN SYSTEM

### Use shadcn/ui + Tailwind CSS
**Why:**
- Unstyled, accessible components
- Full control over styling
- Tailwind-first approach
- Copy-paste components (not a dependency)
- Great TypeScript support

### Core Components to Implement
```
✓ Button (variants: primary, secondary, outline, ghost, destructive)
✓ Card (base layout component)
✓ Input (text, email, number, password)
✓ Textarea
✓ Select (dropdown)
✓ Checkbox
✓ Radio
✓ Dialog/Modal (for confirmations)
✓ Dropdown Menu
✓ Toast/Notification (for feedback)
✓ Tooltip
✓ Tabs
✓ Badge (status indicators)
✓ Spinner/Loading
✓ Skeleton (loading state)
✓ Breadcrumb
✓ Pagination
✓ Alert (for warnings/info)
✓ Form helpers (error messages, labels)
```

### Color System (from your design system)
- Primary: Teal (for actions)
- Success: Green (confirmation)
- Error: Red (destructive)
- Warning: Orange (alerts)
- Info: Blue (informational)
- Neutral: Gray (secondary)
- Background, surface, text colors

---

## 7. STATE MANAGEMENT

### Zustand Stores
```
✓ auth.store.ts
  - user: User | null
  - token: string | null
  - role: 'admin' | 'user'
  - login(), logout(), checkAuth()

✓ ui.store.ts
  - sidebarCollapsed: boolean
  - theme: 'light' | 'dark'
  - activeModule: string
  - toggleSidebar(), setTheme()

✓ editor.store.ts
  - drafts: Map<resourceId, draftContent>
  - saveDraft(id, content)
  - loadDraft(id)
  - clearDraft(id)
```

### API State Management
Use custom hook `useApi<T>()`:
```
const { data, loading, error, refetch } = useApi(
  () => api.getServices({ skip: 0, limit: 20 }),
  { dependencies: [page, sort] }
)
```

---

## 8. PAGINATION & FILTERING

### Backend-Driven Pagination
- Query params: `?skip=0&limit=20`
- Server returns: `{ items: [...], total: 150 }`
- Calculate total pages: `Math.ceil(total / limit)`

### Filtering Strategy
- Store filter state in URL query params
- Reset pagination to page 1 when filters change
- Debounce search input (300ms)
- Support multi-field filtering
- Show active filter badges

### Common Filters by Module
```
Services:
- Active/Inactive
- Featured
- Search by title

Blog:
- Status (draft/published/archived)
- Featured
- Tags (multi-select)
- Date range
- Search

Case Studies:
- Status
- Featured
- Industry
- Tags
- Search

Contact Inquiries:
- Status (new/in_progress/resolved/closed)
- Date range
- Service interest filter
```

---

## 9. ERROR HANDLING & VALIDATION FEEDBACK

### API Error Handling Pattern
```
try {
  const response = await api.updateService(id, data)
  // Success
} catch (error) {
  if (error.status === 422) {
    // Validation error - show field-level errors
    showFieldErrors(error.data.detail)
  } else if (error.status === 401) {
    // Unauthorized - redirect to login
    redirectToLogin()
  } else if (error.status === 403) {
    // Forbidden - show permission denied
    showErrorToast('You do not have permission')
  } else {
    // Generic error
    showErrorToast(error.message)
  }
}
```

### Form Validation Feedback
- **Inline field errors** (red text below field)
- **Visual indicators** (red border on error field)
- **Real-time validation** (on blur)
- **Submit-time validation** (before API call)
- **API error mapping** (422 errors → field errors)

---

## 10. LOADING & SKELETON STATES

### Skeleton Patterns
```
✓ Table skeleton (rows with animated placeholders)
✓ Card skeleton (blocks of gray)
✓ Form skeleton (input fields with placeholder)
✓ Editor skeleton (toolbar + content area)
```

### Loading Indicators
- Page-level spinner (for full page loads)
- Button loading state (disabled + spinner)
- Inline spinners (for quick operations)
- Skeleton screens (for better UX than spinners)

---

## 11. RESPONSIVE DESIGN

### Breakpoints (Tailwind)
- Mobile: < 640px (sm)
- Tablet: 640px - 1024px (md, lg)
- Desktop: > 1024px (xl, 2xl)

### Layout Adaptation
```
Mobile:
- Sidebar hidden (slide-out menu or bottom nav)
- Single column layout
- Full-width forms
- Stacked tables (horizontal scroll)

Tablet:
- Sidebar collapsed to icons
- 2-column layout where applicable

Desktop:
- Full sidebar
- Multi-column layouts
- All features visible
```

---

## 12. PERFORMANCE OPTIMIZATION

### Code Splitting
- Lazy load heavy components (editors, media galleries)
- Route-based code splitting (already done by Next.js)
- Dynamic imports for optional features

### Image Optimization
- Use Next.js Image component
- Responsive images with srcSet
- WebP format with fallbacks
- Optimize uploaded images on server

### Debouncing & Memoization
- Debounce search input (300ms)
- Debounce form auto-save (2s)
- Memoize expensive components (React.memo, useMemo)
- Memoize callbacks (useCallback)

### Caching Strategy
- Browser cache for images (long TTL)
- API response caching (use stale-while-revalidate)
- Service worker for offline support (optional)

---

## 13. ACCESSIBILITY (a11y)

### WCAG 2.1 Level AA Compliance
```
✓ Semantic HTML (use <button>, <form>, <nav>, etc.)
✓ ARIA labels (aria-label, aria-describedby)
✓ Keyboard navigation (Tab, Enter, Esc)
✓ Focus management (visible focus indicator)
✓ Color contrast (4.5:1 normal text, 3:1 large text)
✓ Alt text for all images
✓ Form labels properly associated
✓ Error messages linked to fields (aria-invalid)
✓ Skip to main content link
✓ Headings hierarchy (h1 → h2 → h3)
✓ Table headers with scope attribute
✓ Reduced motion support (@media prefers-reduced-motion)
```

### Testing
- Keyboard-only navigation test
- Screen reader test (NVDA, JAWS, VoiceOver)
- Color contrast checker
- Automated testing (axe, jest-axe)

---

## 14. BROWSER COMPATIBILITY

### Target Browsers
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome mobile)

### Polyfills & Fallbacks
- Use @vitejs/plugin-legacy (if needed)
- CSS fallbacks (Grid → Flexbox)
- No IE 11 support needed

---

## 15. DEPLOYMENT & ENVIRONMENT

### Development Environment
```
npm run dev
# Runs on http://localhost:3000
# Auto-reload on file changes
```

### Build & Production
```
npm run build
npm run start

# Or deploy to Vercel (recommended for Next.js)
```

### Environment Variables by Stage
```
Development:
- API_BASE_URL=http://localhost:8000
- DEBUG=true

Staging:
- API_BASE_URL=https://api-staging.techpath.io
- DEBUG=false

Production:
- API_BASE_URL=https://api.techpath.io
- DEBUG=false
- ANALYTICS enabled
```

---

## 16. API INTEGRATION PATTERNS

### Service Layer Architecture
```
useComponent
    ↓
useApi hook
    ↓
Service layer (e.g., services.service.ts)
    ↓
API client (axios wrapper)
    ↓
Backend API
```

### Service Method Pattern
```typescript
// services/blog.service.ts
export class BlogService {
  async listPosts(skip: number, limit: number, filters?: object) {
    return this.client.get('/api/v1/blog/posts', {
      params: { skip, limit, ...filters }
    })
  }

  async createPost(data: BlogPostCreate) {
    return this.client.post('/api/v1/blog/posts', data)
  }

  async updatePost(id: number, data: BlogPostUpdate) {
    return this.client.put(`/api/v1/blog/posts/${id}`, data)
  }

  async deletePost(id: number) {
    return this.client.delete(`/api/v1/blog/posts/${id}`)
  }

  async uploadImage(postId: number, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return this.client.post(
      `/api/v1/blog/posts/${postId}/upload-image`,
      formData
    )
  }
}
```

---

## 17. MODULES IMPLEMENTATION ORDER

### Phase 1: Foundation (Week 1)
```
1. Auth (login/logout/token management)
2. Layout (sidebar, top nav, breadcrumb)
3. Dashboard (overview with stats)
4. UI component library setup
```

### Phase 2: Content Management (Weeks 2-3)
```
5. Services CRUD
6. Blog Posts CRUD (with rich text editor)
7. Case Studies CRUD (with rich text editor)
```

### Phase 3: Additional Features (Week 4)
```
8. Contact Inquiries management
9. Newsletter subscribers management
10. User management (admin only)
11. File upload/media management
```

### Phase 4: Polish & Optimization (Week 5)
```
12. Performance optimization
13. Accessibility audit & fixes
14. Error handling refinement
15. Documentation & deployment
```

---

## 18. KEY LIBRARIES & DEPENDENCIES

### Core Framework
```
next: ^14.0.0
react: ^18.2.0
react-dom: ^18.2.0
```

### State Management
```
zustand: ^4.4.0
```

### Forms & Validation
```
react-hook-form: ^7.50.0
zod: ^3.22.0
```

### Rich Text Editor
```
@tiptap/react: ^2.1.0
@tiptap/starter-kit: ^2.1.0
@tiptap/extension-markdown: ^2.1.0
@tiptap/extension-image: ^2.1.0
@tiptap/extension-code-block-lowlight: ^2.1.0
lowlight: ^2.20.0
```

### UI Components & Styling
```
tailwindcss: ^3.4.0
@tailwindcss/forms: ^0.5.0
@tailwindcss/typography: ^0.5.0
shadcn-ui: (copy-paste, not npm)
```

### HTTP Client
```
axios: ^1.6.0
```

### Utilities
```
clsx: ^2.0.0
date-fns: ^2.30.0
react-hot-toast: ^2.4.0
```

### Development
```
typescript: ^5.0.0
@types/react: ^18.2.0
@types/node: ^20.0.0
tailwind-css: ^3.4.0
autoprefixer: ^10.4.0
postcss: ^8.4.0
```

---

## 19. TESTING STRATEGY

### Unit Tests (Jest + React Testing Library)
- Component rendering
- User interactions
- Form validation
- API call mocking

### Integration Tests
- Form submission flow
- CRUD operations
- Authentication flow

### E2E Tests (Playwright/Cypress)
- Complete user workflows
- Cross-browser testing

### Performance Tests
- Lighthouse CI
- Bundle size monitoring

---

## 20. SECURITY BEST PRACTICES

### Input Sanitization
- Sanitize rich text output (use DOMPurify or HTML parser)
- Validate all inputs server-side
- No eval() or dangerous functions

### CSRF Protection
- Use SameSite cookies
- CSRF tokens for state-changing requests

### Content Security Policy
```
default-src 'self'
script-src 'self' 'unsafe-inline' (for Tiptap)
style-src 'self' 'unsafe-inline' (for Tailwind)
img-src 'self' data: https:
font-src 'self'
```

### Rate Limiting
- Implement on backend
- Show friendly errors on frontend

---

## 21. EXAMPLE COMPONENT PATTERNS

### Service Form Component Pattern
```
<ServiceForm 
  mode="create" | "edit"
  initialData={service}
  onSubmit={(data) => handleSubmit(data)}
  isLoading={false}
/>
```

### Blog Post Form with Rich Editor
```
<BlogPostForm
  mode="create" | "edit"
  initialData={post}
  onSubmit={(data) => {
    // data includes HTML content from Tiptap
    // and markdown representation
  }}
  onDraftSave={(draft) => {
    // Auto-save to localStorage
  }}
/>
```

### Reusable DataTable
```
<DataTable<ServiceResponse>
  columns={serviceColumns}
  data={services}
  isLoading={loading}
  pagination={{ page, limit, total }}
  onPaginationChange={(p, l) => setPagination(p, l)}
  onEdit={(service) => router.push(`/services/${service.id}`)}
  onDelete={(id) => deleteService(id)}
/>
```

---

## 22. QUICK START CHECKLIST

For Cursor Agent - Start Here:

```
□ Initialize Next.js 14 with App Router
□ Set up Tailwind CSS + shadcn/ui
□ Create directory structure per Section 1
□ Implement auth middleware & JWT handling
□ Create Zustand stores (auth, ui, editor)
□ Build layout components (Sidebar, TopNav)
□ Set up API client wrapper (axios)
□ Create service layer for each resource
□ Build auth pages (login, setup)
□ Build dashboard overview
□ Implement Services CRUD
□ Integrate Tiptap editor for Blog/Case Studies
□ Build Blog CRUD with editor
□ Build Case Studies CRUD with editor
□ Add Contact Inquiries view
□ Add Newsletter subscribers view
□ Implement image upload/media handling
□ Add form validation with Zod + React Hook Form
□ Build DataTable component with filtering/sorting
□ Add error handling & toast notifications
□ Implement accessibility audit
□ Performance optimization (code splitting, caching)
□ Deploy to Vercel
□ Set up monitoring & logging
```

---

## 23. COMMON PITFALLS TO AVOID

```
❌ Storing JWT in localStorage (use HTTP-only cookies)
❌ Mixing client-side & server-side logic in components
❌ Not implementing loading/error states
❌ Complex nested component structures (keep flat)
❌ Not validating on both client & server
❌ Hardcoding API URLs (use env variables)
❌ Not handling 422 validation errors properly
❌ Inline styles instead of Tailwind
❌ Not implementing debouncing for search/filters
❌ Missing ARIA labels on form fields
❌ Not implementing optimistic updates
❌ Ignoring TypeScript strict mode
```

---

## 24. RESOURCES & REFERENCES

### Documentation
- Next.js App Router: https://nextjs.org/docs/app
- Tiptap: https://tiptap.dev
- React Hook Form: https://react-hook-form.com
- Tailwind CSS: https://tailwindcss.com
- shadcn/ui: https://ui.shadcn.com
- Zod: https://zod.dev

### Best Practices
- Web Accessibility: https://www.w3.org/WAI/
- Next.js Security: https://nextjs.org/docs/security
- React Performance: https://react.dev/reference/react

---

## Implementation Notes for Cursor

This guide is designed to be followed step-by-step by an AI coding assistant. Each section provides:
- **What to build** (features & components)
- **How to organize** (file structure)
- **Best practices** (patterns & approaches)
- **Tools & libraries** (dependencies)
- **Decisions** (why certain choices)

**The Cursor agent should reference these sections when implementing each module, ensuring consistency and following industry best practices for modern Next.js applications.**

---

**Last Updated**: December 2025
**Version**: 1.0
**Status**: Production Ready