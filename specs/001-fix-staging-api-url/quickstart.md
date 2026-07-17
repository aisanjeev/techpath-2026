# Quickstart & Validation Guide: Fix Staging API URL

This guide outlines how to validate the fix for the API URL routing bug.

## Prerequisites
- Node.js and npm installed.
- Access to the `techpath-frontend` directory.

## Validation Steps

### Step 1: Local Build Validation
We must verify that the client bundle correctly bakes in the `PUBLIC_API_URL` environment variable.

1. Navigate to the frontend directory:
   ```bash
   cd techpath-frontend
   ```
2. Build the project using a dummy production API URL to simulate a deployment:
   ```bash
   PUBLIC_API_URL=https://dummy-staging-api.techpath.biz npm run build
   ```
3. Preview the production build locally:
   ```bash
   npm run preview
   ```
4. Open your browser and navigate to the preview URL.
5. Attempt to trigger an API call (e.g., trying to log in).
6. **Expected Outcome**: The network tab should show the request going to `https://dummy-staging-api.techpath.biz/...`, NOT `http://localhost:8000`.

### Step 2: Staging Deployment Validation
1. Deploy the `001-fix-staging-api-url` branch to the staging environment.
2. Navigate to `https://staging.techpath.biz/portal`.
3. Attempt to log in.
4. **Expected Outcome**: The API request correctly routes to `https://staging.api.techpath.biz/api/v1/student/auth/login` and authentication succeeds.
