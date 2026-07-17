# Feature Specification: Fix Staging API URL Configuration

**Feature Branch**: `001-fix-staging-api-url`

**Created**: 2026-07-17

**Status**: Draft

**Input**: User description: "i deployed on staging https://staging.techpath.biz/portal, but geeetting local url why Request URL http://localhost:8000/api/v1/student/auth/login Referrer Policy same-origin"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Staging Authentication (Priority: P1)

As a student on the staging environment, I want my authentication requests to be routed to the staging API so that I can successfully log in and use the portal.

**Why this priority**: Without correct API routing, the staging environment is entirely broken and unusable.

**Independent Test**: Can be fully tested by attempting to log in on the staging frontend and verifying the network request goes to `staging.api.techpath.biz` instead of `localhost:8000`.

**Acceptance Scenarios**:

1. **Given** I am on the staging frontend (`staging.techpath.biz`), **When** I attempt to log in or make any API request, **Then** the request is sent to the staging API URL (`staging.api.techpath.biz`) instead of `localhost:8000`.

### Edge Cases

- What happens if the environment variables are missing during the build process? (Build should fail or fallback gracefully, but ideally it should use the correct production/staging URLs).
- Does this issue affect the Admin dashboard as well, or just the student frontend?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The staging frontend deployment MUST use the staging API endpoint for all backend communications.
- **FR-002**: Environment configurations MUST correctly differentiate between local development (`localhost:8000`) and deployed environments (staging/production).
- **FR-003**: The build process for the frontend MUST correctly inject the staging API URL into the deployed artifact.

### Key Entities

- **Environment Configuration**: The set of variables that dictate where the frontend routes its API requests (e.g., `PUBLIC_API_URL`, `NEXT_PUBLIC_API_BASE_URL`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API requests originating from the staging frontend (`staging.techpath.biz`) are directed to the staging API (`staging.api.techpath.biz`).
- **SC-002**: Users can successfully log in and authenticate on the staging environment without network errors related to `localhost`.

## Assumptions

- The issue is caused by incorrect environment variable configuration or hardcoded URLs during the build/deployment process for the frontend.
- The staging API (`staging.api.techpath.biz`) is currently deployed and accessible.
- The codebase uses standard environment variable patterns for configuring API URLs.
