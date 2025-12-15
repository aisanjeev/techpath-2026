# Deployment Guide

## Overview

TechPath frontend is deployed to **Vercel** for optimal performance and seamless CI/CD integration.

## Prerequisites

- Node.js 20+
- npm or pnpm
- Vercel account
- GitHub repository access

## Environment Variables

Configure these in Vercel dashboard:

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_BASE_URL` | Backend API URL | Yes |
| `SITE_URL` | Production site URL | Yes |
| `VITE_GA_TRACKING_ID` | Google Analytics ID | No |
| `VITE_SENTRY_DSN` | Sentry error tracking | No |

## Deployment Methods

### 1. Automatic Deployment (Recommended)

1. Connect GitHub repository to Vercel
2. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
3. Push to `main` branch for production
4. Push to feature branches for preview deployments

### 2. Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Build Configuration

### `astro.config.mjs`

```javascript
export default defineConfig({
  site: 'https://techpath.biz',
  output: 'hybrid',
  // ...
});
```

### `vercel.json`

```json
{
  "framework": "astro",
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

## Performance Optimization

### Edge Caching

Static assets are cached at Vercel's edge:
- HTML pages: Cache with revalidation
- Static assets: Long-term caching
- API routes: No cache (dynamic)

### Image Optimization

Images are automatically optimized by Vercel:
- WebP/AVIF conversion
- Responsive sizing
- Lazy loading

## Monitoring

### Vercel Analytics

Enable in Vercel dashboard for:
- Real-time traffic analytics
- Performance insights
- Core Web Vitals tracking

### Error Tracking

Configure Sentry for production error tracking:
1. Add `VITE_SENTRY_DSN` environment variable
2. Errors automatically reported
3. Source maps uploaded during build

## Rollback

To rollback a deployment:
1. Go to Vercel dashboard → Deployments
2. Find previous stable deployment
3. Click "..." → "Promote to Production"

## Troubleshooting

### Build Failures

1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `package.json`
3. Run `npm run build` locally to reproduce

### Environment Variables

1. Verify variables are set in Vercel
2. Check variable names match code
3. Redeploy after changing variables

### Performance Issues

1. Run Lighthouse audit
2. Check for large JavaScript bundles
3. Verify image optimization is working

