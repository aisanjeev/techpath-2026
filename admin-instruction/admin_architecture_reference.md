# Admin Panel Architecture Reference & Visual Guide

**Supplementary Quick Reference for Cursor Implementation**

---

## DATA FLOW DIAGRAM

```
┌──────────────────────────────────────────────────────────────────┐
│                        NEXT.JS ADMIN PANEL                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      USER INTERFACE                        │ │
│  │  ┌──────────────────┐  ┌──────────────────────────────┐   │ │
│  │  │    Navigation    │  │   Main Content Area          │   │ │
│  │  │                  │  │  ┌──────────────────────────┐│   │ │
│  │  │  • Dashboard     │  │  │  Form / Table / Editor   ││   │ │
│  │  │  • Services      │  │  │                          ││   │ │
│  │  │  • Blog          │  │  │  Rich Text Editor        ││   │ │
│  │  │  • Case Studies  │  │  │  (Tiptap)                ││   │ │
│  │  │  • Contact       │  │  │                          ││   │ │
│  │  │  • Users         │  │  └──────────────────────────┘│   │ │
│  │  │  • Settings      │  │                              │   │ │
│  │  └──────────────────┘  └──────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              STATE MANAGEMENT (Zustand)                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐             │ │
│  │  │ Auth     │  │   UI     │  │   Editor     │             │ │
│  │  │ Store    │  │  Store   │  │   Store      │             │ │
│  │  └──────────┘  └──────────┘  └──────────────┘             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │            SERVICE LAYER & API CLIENTS                     │ │
│  │  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐        │ │
│  │  │ Auth    │ │ Services│ │  Blog    │ │ CaseStudy        │ │
│  │  │ Service │ │ Service │ │ Service  │ │ Service│        │ │
│  │  └─────────┘ └─────────┘ └──────────┘ └─────────┘        │ │
│  │               (Axios wrapper with interceptors)            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │            HTTP CLIENT (Axios)                             │ │
│  │  • JWT Token Management (Headers)                          │ │
│  │  • Request/Response Interceptors                           │ │
│  │  • Error Handling & Logging                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  BACKEND API       │
                    │  (FastAPI)         │
                    │                    │
                    │ /api/v1/...        │
                    │                    │
                    │ • Authentication   │
                    │ • Services CRUD    │
                    │ • Blog CRUD        │
                    │ • Case Studies     │
                    │ • Contacts         │
                    │ • Newsletter       │
                    │ • File Upload      │
                    │                    │
                    └────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   DATABASE         │
                    │   • PostgreSQL     │
                    │   • Redis (cache)  │
                    │   • S3/CDN Storage │
                    └────────────────────┘
```

---

## COMPONENT HIERARCHY

```
App (Root)
├── AuthProvider (middleware layer)
│   └── Layout
│       ├── TopNav
│       │   ├── BreadcrumbNav
│       │   ├── UserDropdown
│       │   └── NotificationBell
│       ├── Sidebar
│       │   ├── Logo
│       │   ├── Nav Items
│       │   └── Collapse Toggle
│       └── MainContent
│           ├── Page-specific content
│           │   ├── Dashboard (stats cards, charts)
│           │   ├── ResourceList (DataTable + filters)
│           │   └── ResourceForm (form + editor)
│           └── Toast Container

ServiceListPage
├── FilterBar
│   ├── SearchInput
│   ├── StatusFilter
│   └── Featured Toggle
├── DataTable
│   ├── TableHeader
│   ├── TableBody (rows)
│   │   └── TableRow
│   │       ├── Checkbox
│   │       ├── Status Badge
│   │       ├── Data Cells
│   │       └── Actions Menu
│   └── Pagination
└── BulkActionsBar

ServiceFormPage
├── FormHeader
├── Form
│   ├── TextField (title, slug)
│   ├── TextareaField (short_description)
│   ├── RichTextEditor (Tiptap)
│   ├── FeaturedImagePicker
│   │   ├── ImageUpload
│   │   └── ImageGallery
│   ├── FeaturesList (dynamic array)
│   ├── TagSelector (multi-select)
│   ├── MetaFields
│   └── FormActions
│       ├── SaveDraft
│       ├── Publish
│       └── Cancel
└── Preview Panel (optional)

BlogPostFormPage (extends Service Form)
├── TitleField
├── SlugField
├── RichTextEditor (Tiptap with all extensions)
│   ├── Toolbar
│   │   ├── TextFormat (B, I, U)
│   │   ├── HeadingLevels (H1-H6)
│   │   ├── Alignment (L, C, R, J)
│   │   ├── Lists (bullet, numbered)
│   │   ├── LinkInsertion
│   │   ├── ImageUpload
│   │   ├── CodeBlock
│   │   ├── Table
│   │   ├── Blockquote
│   │   └── MoreMenu
│   ├── EditorContent (main text area)
│   ├── CharacterCounter
│   ├── MarkdownToggle
│   └── FormatPreview
├── ExcerptField
├── FeaturedImagePicker
├── PublishSettings
│   ├── StatusSelect (draft/published/archived)
│   ├── PublishDate picker
│   ├── Featured toggle
│   └── ReadingTimeDisplay
├── SEOFields
│   ├── MetaTitle
│   └── MetaDescription
├── TagSelector
└── FormActions
```

---

## FORM STATE FLOW

```
User Input
   │
   ▼
Input Event
   │
   ▼
React Hook Form Value Update
   │
   ├─→ Zod Validation (debounced)
   │   │
   │   ├─→ Valid: Clear field error
   │   └─→ Invalid: Show field error
   │
   └─→ Trigger Auto-Save (debounced 2s)
       │
       ▼
   Save Draft to localStorage
   │
   ▼
Submit Form
   │
   ├─→ Client-side Validation (Zod)
   │   │
   │   ├─→ Valid: Proceed to API
   │   └─→ Invalid: Show inline errors
   │
   ├─→ API Call (POST/PUT)
   │   │
   │   ├─→ 200 OK: Success toast + redirect
   │   ├─→ 422: Show field-specific errors
   │   ├─→ 401: Redirect to login
   │   ├─→ 403: Show permission error
   │   └─→ 500: Show generic error
   │
   ▼
Clear Draft from localStorage
│
▼
Success State
```

---

## AUTHENTICATION FLOW

```
┌─────────────────────────────────────────────────────────┐
│              AUTHENTICATION FLOW                        │
└─────────────────────────────────────────────────────────┘

1. INITIAL REQUEST
   ├─ User navigates to /admin
   └─ Middleware checks for JWT token in HTTP-only cookie

2. NO TOKEN OR EXPIRED
   ├─ Redirect to /auth/login
   └─ Show login form

3. LOGIN FORM SUBMIT
   ├─ POST /api/v1/auth/login { email, password }
   ├─ Backend validates credentials
   ├─ Returns { access_token, token_type, expires_in }
   └─ Set HTTP-only cookie: Authorization=bearer_token

4. TOKEN STORED
   ├─ Cookie set by Set-Cookie header (HTTP-only, SameSite=Strict)
   ├─ Frontend stores user info in Zustand (auth.store)
   └─ Axios interceptor adds token to all subsequent requests

5. AUTHENTICATED REQUESTS
   ├─ GET /api/v1/services
   ├─ Headers: Authorization: Bearer {token}
   ├─ Backend validates token
   └─ Returns protected resource

6. TOKEN EXPIRATION
   ├─ API returns 401 Unauthorized
   ├─ Axios interceptor catches 401
   ├─ POST /api/v1/auth/refresh-token
   ├─ Backend returns new token
   ├─ Retry original request
   └─ (If refresh fails → redirect to login)

7. LOGOUT
   ├─ User clicks logout
   ├─ Delete HTTP-only cookie (backend side)
   ├─ Clear Zustand auth store
   ├─ Redirect to /auth/login
   └─ Local state cleared

AXIOS INTERCEPTOR PATTERN:
- Request: Add Authorization header
- Response: Catch 401, attempt refresh, retry
- Error: Show appropriate error message
```

---

## RICH TEXT EDITOR - DETAILED FLOW

```
┌───────────────────────────────────────┐
│   TIPTAP RICH TEXT EDITOR             │
└───────────────────────────────────────┘

INITIALIZATION
  ├─ useEditor hook
  ├─ Extensions: Markdown, Link, Image, Code, Table, etc.
  ├─ Initial content (from DB or draft)
  └─ EditorContent component renders

USER INTERACTIONS

1. TEXT FORMATTING
   ├─ Select text
   ├─ Click toolbar button (Bold, Italic, etc.)
   └─ editor.chain().focus().toggleBold().run()

2. MARKDOWN MODE TOGGLE
   ├─ Tiptap content ↔ Raw Markdown
   ├─ editor.getMarkdown() - export to markdown
   ├─ setContent() - import from markdown
   └─ Show source editor in textarea

3. IMAGE INSERTION
   ├─ Click Image button
   ├─ Upload modal or drag-drop
   ├─ Upload to /api/upload (server route)
   ├─ Get back image URL
   ├─ editor.chain().focus().setImage({ src }).run()
   └─ Image appears in editor

4. LINK INSERTION
   ├─ Select text or click Link button
   ├─ Open link dialog
   ├─ Enter URL
   ├─ editor.chain().focus().setLink({ href }).run()
   └─ Text becomes blue link

5. CODE BLOCK
   ├─ Click Code button or ```
   ├─ Language selector dropdown
   ├─ Syntax highlighting (Lowlight)
   └─ User types code

6. TABLE INSERTION
   ├─ Click Table button
   ├─ Select grid size
   ├─ Table appears in editor
   ├─ Tab to navigate cells
   └─ Add/delete rows/columns

VALIDATION & PERSISTENCE

Content → Zod Validation
  ├─ Min 10 characters
  ├─ Max 50,000 characters
  ├─ At least one paragraph/heading
  └─ No empty code blocks

Auto-save Draft
  ├─ Debounce editor changes (2s)
  ├─ Save to localStorage: blog_post_1_draft
  ├─ Show "Draft saved" toast
  └─ On mount: check for draft, offer restore

On Form Submit
  ├─ Get editor.getHTML() - HTML content
  ├─ Get editor.getMarkdown() - Markdown version
  ├─ Include both in API payload
  └─ API stores both formats for flexibility

OUTPUT
  ├─ Database: Store HTML + Markdown
  ├─ Frontend display: Render HTML with sanitization
  └─ API export: Provide Markdown for portability
```

---

## API ERROR HANDLING MATRIX

```
HTTP STATUS │ SCENARIO              │ FRONTEND ACTION
─────────────┼──────────────────────┼──────────────────────────
200 OK       │ Success              │ Show success toast, redirect
201 Created  │ Resource created     │ Show success toast, redirect
204 No Cont. │ Deleted/updated      │ Show success toast
─────────────┼──────────────────────┼──────────────────────────
400 Bad Req. │ Invalid request      │ Log error, show generic msg
401 Unauth.  │ Token expired/invalid│ Clear auth, redirect login
403 Forbidden│ No permission        │ Show permission denied msg
404 Not Fnd. │ Resource not found   │ Show not found, redirect
422 Validat. │ Validation errors    │ Show field-level errors
─────────────┼──────────────────────┼──────────────────────────
429 Too Many │ Rate limited         │ Show retry message, queue
500 Server E.│ Server error         │ Show error, offer retry
503 Unavail. │ Service down         │ Show maintenance message
```

---

## PAGINATION PATTERN

```
Backend Response:
{
  "items": [...],
  "total": 150
}

Frontend Calculation:
totalPages = Math.ceil(total / limit)

URL Query Params:
/admin/blog?page=1&limit=20

Pagination Control:
┌──────────────────────────────────────┐
│ ◀ Previous  [1][2][3][4][5]  Next ▶ │
│            Showing 1-20 of 150       │
│            Items per page: [10▼]     │
└──────────────────────────────────────┘

State Update Pattern:
1. User clicks page 2
2. Set skip = (page - 1) * limit = 20
3. Fetch with new skip parameter
4. Update data table
5. Update pagination UI

On Filter/Sort Change:
1. Reset to page 1
2. Update skip = 0
3. Fetch with new filters/sort
4. Show loading skeleton
5. Update results
```

---

## RESPONSIVE GRID SYSTEM

```
MOBILE (< 640px)
┌─────────────────────┐
│ ☰ | TechPath | ⊗ ⊙  │  Header (fixed)
├─────────────────────┤
│                     │
│  Single Column      │
│  Full Width Content │
│                     │
│  1. Form field      │
│  2. Form field      │
│  3. Submit button   │
│                     │
├─────────────────────┤
│ [Nav Items]         │  Drawer/Menu (slide-out)
└─────────────────────┘


TABLET (640px - 1024px)
┌──────────────────────────┐
│ ≡ | TechPath Admin | ⊗ ⊙ │
├──────────────────────────┤
│ │                        │
│ │  Two Column            │
│ │  Layout                │
│ │                        │
│ ├──────────────────────┤ │
│ │ Sidebar (collapsed)  │ │
│ │ Icons only           │ │
│ └──────────────────────┘ │


DESKTOP (> 1024px)
┌──────────────────────────────────────┐
│ TechPath Logo | Dashboard | ⊗ ⊙      │
├────────────┬─────────────────────────┤
│ Nav        │ Main Content            │
│ • Services │                         │
│ • Blog     │ Title                   │
│ • Cases    │ ┌─────┬─────┐          │
│ • Contact  │ │ Col │ Col │          │
│ • Users    │ │  1  │  2  │          │
│            │ └─────┴─────┘          │
│            │                         │
│            │ Full-width content      │
│            │                         │
└────────────┴─────────────────────────┘
```

---

## FORM VALIDATION - ZYGOTE SCHEMA EXAMPLES

```typescript
// Service Validation
const serviceSchema = z.object({
  title: z.string().min(1).max(255),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  description: z.string().min(10),
  short_description: z.string().max(500).optional(),
  features: z.array(z.string()).optional(),
  featured: z.boolean(),
  is_active: z.boolean(),
})

// Blog Post Validation
const blogPostSchema = z.object({
  title: z.string().min(1).max(255),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  content: z.string().min(10).max(50000),
  excerpt: z.string().max(500).optional(),
  status: z.enum(['draft', 'published', 'archived']),
  featured: z.boolean(),
  published_at: z.date().optional(),
  tag_ids: z.array(z.number()).optional(),
})

// Case Study Validation
const caseStudySchema = z.object({
  title: z.string().min(1).max(255),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  client_name: z.string().min(1).max(255),
  industry: z.string().min(1).max(100),
  challenge: z.string().min(10),
  solution: z.string().min(10),
  results: z.string().min(10),
  featured_image: z.string().url().optional(),
  status: z.enum(['draft', 'published', 'archived']),
})
```

---

## ZUSTAND STORE PATTERNS

```typescript
// auth.store.ts
interface AuthState {
  user: UserResponse | null
  token: string | null
  isLoading: boolean
  setUser: (user: UserResponse) => void
  setToken: (token: string) => void
  logout: () => void
  checkAuth: () => Promise<void>
}

// ui.store.ts
interface UIState {
  sidebarCollapsed: boolean
  theme: 'light' | 'dark'
  activeModule: string
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
  setActiveModule: (module: string) => void
}

// editor.store.ts
interface EditorState {
  drafts: Record<string, EditorDraft>
  saveDraft: (id: string, content: EditorDraft) => void
  loadDraft: (id: string) => EditorDraft | null
  clearDraft: (id: string) => void
}

interface EditorDraft {
  content: string
  markdown: string
  lastSaved: number
}
```

---

## COMMON PATTERNS - CODE SNIPPETS

### Service Layer Pattern
```typescript
// services/blog.service.ts
export const blogService = {
  async list(skip: number, limit: number, filters?: object) {
    const { data } = await apiClient.get('/api/v1/blog/posts', {
      params: { skip, limit, ...filters }
    })
    return data
  },

  async create(payload: BlogPostCreate) {
    const { data } = await apiClient.post('/api/v1/blog/posts', payload)
    return data
  },

  async update(id: number, payload: BlogPostUpdate) {
    const { data } = await apiClient.put(`/api/v1/blog/posts/${id}`, payload)
    return data
  },

  async delete(id: number) {
    const { data } = await apiClient.delete(`/api/v1/blog/posts/${id}`)
    return data
  }
}
```

### Custom Hook Pattern
```typescript
// hooks/useApi.ts
export function useApi<T>(
  fn: () => Promise<T>,
  options?: { dependencies?: any[]; onError?: (err: any) => void }
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<any>(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    try {
      const result = await fn()
      setData(result)
      setError(null)
    } catch (err) {
      setError(err)
      options?.onError?.(err)
    } finally {
      setLoading(false)
    }
  }, [fn, options])

  useEffect(() => {
    fetch()
  }, options?.dependencies || [])

  return { data, loading, error, refetch: fetch }
}
```

### Axios Interceptor Pattern
```typescript
// lib/api-client.ts
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL
})

apiClient.interceptors.request.use((config) => {
  const token = getTokenFromCookie()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
    }
    return Promise.reject(error)
  }
)
```

---

## TABLE COLUMN DEFINITIONS

```typescript
// For DataTable component
const serviceColumns: ColumnDef<ServiceResponse>[] = [
  {
    id: 'select',
    header: ({ table }) => <Checkbox {...table.getHeaderProps()} />,
    cell: ({ row }) => <Checkbox {...row.getProps()} />,
  },
  {
    accessorKey: 'title',
    header: 'Service Name',
    cell: (info) => info.getValue(),
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: (info) => <StatusBadge status={info.getValue()} />,
  },
  {
    accessorKey: 'featured',
    header: 'Featured',
    cell: (info) => <FeatureBadge featured={info.getValue()} />,
  },
  {
    accessorKey: 'created_at',
    header: 'Created',
    cell: (info) => formatDate(info.getValue()),
  },
  {
    id: 'actions',
    header: 'Actions',
    cell: ({ row }) => (
      <ActionMenu>
        <EditAction onClick={() => handleEdit(row.original)} />
        <DeleteAction onClick={() => handleDelete(row.original.id)} />
      </ActionMenu>
    ),
  },
]
```

---

## FILE UPLOAD FLOW

```
User selects image
  │
  ▼
Validate file
  ├─ Check size (max 5MB)
  ├─ Check MIME type (jpg, png, webp, gif)
  └─ Show error if invalid

  ▼
Upload to /api/upload
  ├─ Send FormData with file
  ├─ Show progress bar
  └─ Backend processes image

  ▼
Backend Response
  ├─ Compress/optimize image
  ├─ Upload to S3/CDN
  └─ Return image URL

  ▼
Update Editor
  ├─ Insert image into Tiptap
  ├─ Display image preview
  └─ Store image URL in form data

  ▼
On Form Submit
  ├─ Include image URLs in payload
  └─ API stores image URLs in database
```

---

## DEPLOYMENT CHECKLIST

```
□ Environment variables configured for production
□ API endpoints updated (backend URL)
□ Debug mode disabled
□ Console logs removed from production code
□ Error boundaries implemented
□ 404 page created
□ Loading/error states polished
□ Accessibility audit completed
□ Performance optimized (bundle size < 500kb)
□ SEO meta tags added
□ Analytics tracking implemented
□ Security headers set (CSP, HSTS, etc.)
□ HTTPS enforced
□ Database migrations run
□ API rate limiting enabled
□ Backup strategy in place
□ Monitoring/logging configured
□ Documentation updated
□ Team trained on admin panel
```

---

**Version**: 1.0
**Status**: Ready for Cursor AI Implementation