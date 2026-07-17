# Implementation Plan: Session Pagination

## Overview

The student portal's session materials view (`MaterialsScreen` within `StudentPortalApp.jsx`) currently displays all content items (`materials.assets`) simultaneously in a vertically scrolling list. To improve the user experience, this will be changed to a paginated "Next/Previous" view, displaying one item at a time. State will be managed using URL query parameters (e.g., `?page=0`) to enable bookmarking and browser back/forward navigation.

## User Review Required

- **UI Layout for Pagination**: Are we okay with placing the "Next" and "Previous" buttons at the bottom of the content? 
- **Page Indexing**: The query string will use 0-indexed values for simplicity (`?page=0` for the first item). Is this acceptable, or should it be 1-indexed?

## Proposed Changes

### `techpath-frontend/src/components/react-components/StudentPortalApp.jsx`

#### [MODIFY] `StudentPortalApp.jsx`
1. **URL State Parsing**: Update `getSessionIdFromUrl` to also parse a `page` parameter (e.g., `getPageFromUrl()`), returning a 0-indexed integer (defaulting to 0).
2. **`StudentPortalApp` State**: 
   - Add a `currentPage` state variable to `StudentPortalApp`.
   - Update `openSession` to accept an optional `page` parameter and update `window.history.pushState` with both `session` and `page`.
   - Update the `popstate` event listener to extract the `page` from the URL and update the `currentPage` state.
3. **`MaterialsScreen` Component**:
   - Change the `materials.assets.map` loop to only render a single asset based on `currentPage`.
   - Add a navigation bar below the asset containing "Previous" and "Next" buttons.
   - The "Previous" button is disabled (or hidden) if `currentPage === 0`.
   - The "Next" button is disabled (or hidden) if `currentPage === materials.assets.length - 1`.
   - Pass a `onPageChange` callback from `StudentPortalApp` to `MaterialsScreen` to update the state and URL.

## Verification Plan

### Manual Verification
1. Open the student portal and navigate to a session with multiple assets.
2. Verify that only the first asset is displayed initially.
3. Click "Next" and verify that the next asset appears and the URL updates to `?session=9&page=1`.
4. Click the browser's "Back" button and verify that the previous asset is displayed.
5. Verify that the "Previous" button is disabled on the first page, and the "Next" button is disabled on the final page.
