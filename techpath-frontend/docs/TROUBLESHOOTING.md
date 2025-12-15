# Troubleshooting Guide

## Common Issues

### Build Errors

#### "Cannot find module" Error

**Symptom:** Build fails with module not found error.

**Solution:**
1. Clear node_modules: `rm -rf node_modules`
2. Clear package lock: `rm package-lock.json`
3. Reinstall: `npm install`

#### TypeScript Errors

**Symptom:** Type errors during build.

**Solution:**
1. Run `npm run check` to see all errors
2. Fix type issues in source files
3. Update type definitions if needed

### Development Issues

#### Hot Reload Not Working

**Symptom:** Changes don't appear in browser.

**Solution:**
1. Restart dev server: `npm run dev`
2. Clear browser cache
3. Check for syntax errors in console

#### Styles Not Applying

**Symptom:** Tailwind classes not working.

**Solution:**
1. Verify class names are correct
2. Check `tailwind.config.js` content paths
3. Restart dev server

### Content Collection Issues

#### Content Not Found

**Symptom:** Blog posts or services not appearing.

**Solution:**
1. Check file is in correct directory
2. Verify frontmatter matches schema
3. Ensure file extension is `.md` or `.mdx`

#### Schema Validation Errors

**Symptom:** Content fails validation.

**Solution:**
1. Check frontmatter against schema in `config.ts`
2. Required fields must be present
3. Date formats: `YYYY-MM-DD`

### Deployment Issues

#### Build Succeeds Locally, Fails on Vercel

**Symptom:** CI build fails but local works.

**Solution:**
1. Check Node.js version matches
2. Verify environment variables are set
3. Check for case-sensitivity issues (Linux vs Mac)

#### 404 on Dynamic Routes

**Symptom:** Service pages return 404.

**Solution:**
1. Verify `getStaticPaths` is implemented
2. Check content files exist
3. Rebuild and redeploy

### API Route Issues

#### CORS Errors

**Symptom:** API requests blocked by browser.

**Solution:**
1. Add CORS headers to API routes
2. Configure backend CORS settings
3. Use same-origin requests if possible

#### Form Submissions Failing

**Symptom:** Contact form doesn't submit.

**Solution:**
1. Check browser console for errors
2. Verify API endpoint is correct
3. Test with backend running locally

### Performance Issues

#### Slow Page Load

**Symptom:** Pages take too long to load.

**Solution:**
1. Run Lighthouse audit
2. Check for large images
3. Minimize JavaScript bundles
4. Enable caching headers

#### High Lighthouse Scores But Slow

**Symptom:** Good scores but feels slow.

**Solution:**
1. Check Core Web Vitals
2. Look for render-blocking resources
3. Optimize largest contentful paint

## Debugging Tools

### Browser DevTools

- Network tab: API requests
- Console: JavaScript errors
- Elements: DOM inspection

### Astro CLI

```bash
# Check for issues
npm run check

# Verbose build
DEBUG=* npm run build
```

### Environment Checks

```bash
# Check Node version
node --version  # Should be 20+

# Check npm version
npm --version

# List installed packages
npm list --depth=0
```

## Getting Help

1. Check Astro Discord: https://astro.build/chat
2. Review Astro docs: https://docs.astro.build
3. Search GitHub issues
4. Contact TechPath support

