# Implementation Plan: Fix Staging API URL Configuration

**Branch**: `001-fix-staging-api-url` | **Date**: 2026-07-17 | **Spec**: [spec.md](file:///D:/project/techpath/techpath-2026/specs/001-fix-staging-api-url/spec.md)

**Input**: Feature specification from `/specs/001-fix-staging-api-url/spec.md`

## Summary

The staging frontend (`staging.techpath.biz`) is incorrectly routing API requests to `http://localhost:8000`. This is caused by Astro's environment variable scoping rules: Astro only exposes variables prefixed with `PUBLIC_` to the client bundle. Several key files (like `api.ts` and `useClassroomSocket.ts`) are referencing `import.meta.env.VITE_API_BASE_URL`. Since it lacks the `PUBLIC_` prefix, Astro replaces it with `undefined` in the browser, causing the code to fall back to the hardcoded `http://localhost:8000` default. 

The fix is to standardize on `PUBLIC_API_URL` across the frontend codebase.

## User Review Required

> [!IMPORTANT]
> The root cause has been identified as an environment variable prefix issue. The solution is straightforward and involves standardizing all API URL references in the frontend to use `PUBLIC_API_URL`. I am ready to implement this fix. Please review and approve this plan.

## Proposed Changes

### techpath-frontend

#### [MODIFY] `src/utils/api.ts`
- Replace `import.meta.env.VITE_API_BASE_URL` with `import.meta.env.PUBLIC_API_URL`.

#### [MODIFY] `src/hooks/useClassroomSocket.ts`
- Replace `import.meta.env.VITE_API_BASE_URL` with `import.meta.env.PUBLIC_API_URL`.

#### [MODIFY] `src/pages/api/contact.ts`, `inquiry.ts`, `newsletter.ts`
- Replace `import.meta.env.VITE_API_BASE_URL` with `import.meta.env.PUBLIC_API_URL` for consistency, even though these are server-side endpoints.

#### [MODIFY] `astro.config.mjs`
- Remove the `__API_BASE_URL__` definition from the `vite.define` block as it's a workaround that isn't being used correctly, and switch `loadEnv` references to use `PUBLIC_API_URL`.

#### [MODIFY] `docs/DEPLOYMENT.md` and `src/env.d.ts`
- Update documentation and type definitions to replace `VITE_API_BASE_URL` with `PUBLIC_API_URL`.

## Verification Plan

### Automated Tests
- The frontend will be successfully built locally (`npm run build`) to ensure type checking and Astro compilation succeed with the updated environment variables.

### Manual Verification
- After deployment, opening the staging URL and attempting to log in will verify that the network request correctly points to the staging API instead of localhost.

## Technical Context

**Language/Version**: TypeScript / Astro 5
**Primary Dependencies**: Astro, React
**Storage**: N/A
**Testing**: Playwright (existing suite)
**Target Platform**: Node.js server (VPS)
**Project Type**: Web application
**Performance Goals**: N/A
**Constraints**: Must ensure all client-side code correctly reads the API URL.
**Scale/Scope**: Impacts all API requests originating from the frontend.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Public Frontend (techpath-frontend)**: Changes maintain the Zero-JS performance principles and Astro's SSR setup. The centralized API client (`api.ts`) is correctly updated to maintain the established pattern.
- **Backend API (techpath-backend)**: N/A
- **Admin Dashboard (techpath-admin)**: N/A

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-staging-api-url/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
techpath-frontend/
├── src/
│   ├── utils/
│   ├── hooks/
│   ├── pages/api/
│   └── env.d.ts
├── astro.config.mjs
└── docs/DEPLOYMENT.md
```

**Structure Decision**: The changes are strictly localized to the `techpath-frontend` application, fixing environment variable references.
