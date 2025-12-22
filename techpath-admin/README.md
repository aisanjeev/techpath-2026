# TechPath Admin Dashboard

Modern admin dashboard for TechPath CMS, built with Next.js 14, TypeScript, and Tailwind CSS.

## Features


- **Dashboard**: Overview with stats and quick actions
- **Services Management**: Full CRUD for service offerings
- **Blog Posts**: Rich text editor (Tiptap) for creating/editing blog content
- **Case Studies**: Manage client success stories
- **Contact Inquiries**: View and manage customer inquiries
- **Authentication**: JWT-based authentication with FastAPI backend
- **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod validation
- **Rich Text Editor**: Tiptap (ProseMirror)
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- TechPath Backend API running on port 8000

### Installation

1. Install dependencies:

```bash
cd techpath-admin
npm install
```

2. Create environment file:

```bash
cp .env.example .env.local
```

3. Update `.env.local` with your API URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

4. Start the development server:

```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
techpath-admin/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/             # Auth pages (login)
│   │   ├── (dashboard)/        # Dashboard pages
│   │   │   ├── blog/
│   │   │   ├── case-studies/
│   │   │   ├── contacts/
│   │   │   ├── dashboard/
│   │   │   ├── services/
│   │   │   └── settings/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── editors/            # Rich text editor
│   │   ├── forms/              # Form components
│   │   ├── layout/             # Layout components
│   │   ├── tables/             # Data table components
│   │   └── ui/                 # Base UI components
│   ├── lib/
│   │   ├── hooks/              # Custom React hooks
│   │   ├── utils/              # Utility functions
│   │   ├── api-client.ts       # Axios configuration
│   │   └── validations.ts      # Zod schemas
│   ├── services/               # API service layers
│   ├── store/                  # Zustand stores
│   └── types/                  # TypeScript types
└── tailwind.config.ts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The admin panel connects to the TechPath FastAPI backend:

| Endpoint | Description |
|----------|-------------|
| `/api/v1/auth/login` | User authentication |
| `/api/v1/services/` | Services CRUD |
| `/api/v1/blog/posts` | Blog posts CRUD |
| `/api/v1/case-studies/` | Case studies CRUD |
| `/api/v1/contact/inquiries` | Contact inquiries |

## Authentication

- JWT token stored in Zustand with localStorage persistence
- Axios interceptor automatically adds Authorization header
- 401 responses redirect to login page

## Customization

### Adding New Pages

1. Create page file in `src/app/(dashboard)/your-page/page.tsx`
2. Add navigation item in `src/components/layout/Sidebar.tsx`
3. Create service layer in `src/services/your-service.service.ts`

### Styling

- Modify `tailwind.config.ts` for theme customization
- Global styles in `src/app/globals.css`
- Component styles use Tailwind utility classes

## License

Private - TechPath Professional Services
