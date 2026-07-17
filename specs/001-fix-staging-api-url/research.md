# Research Notes: Fix Staging API URL Configuration

## Investigation
- **Symptom**: Staging frontend (`staging.techpath.biz`) makes API calls to `http://localhost:8000`.
- **Cause**: The API client and socket hook use `import.meta.env.VITE_API_BASE_URL`. In Astro, any environment variable exposed to the client bundle must be prefixed with `PUBLIC_`. Because `VITE_API_BASE_URL` lacks this prefix, Astro replaces it with `undefined` in the client build.
- **Resolution**: The codebase fallback triggers: `undefined || 'http://localhost:8000'`, defaulting to localhost.

## Decisions

### Environment Variable Standardization
- **Decision**: Standardize entirely on `PUBLIC_API_URL` for the frontend.
- **Rationale**: Astro specifically documents that only `PUBLIC_` prefixed variables are exposed to the client. The frontend has a mix of `PUBLIC_API_URL` and `VITE_API_BASE_URL`. Standardizing on `PUBLIC_API_URL` ensures the URL is correctly embedded in both SSR and client-side chunks.
- **Alternatives considered**: Prefixing it as `PUBLIC_VITE_API_BASE_URL` (redundant) or configuring Vite define explicitly (error-prone).
