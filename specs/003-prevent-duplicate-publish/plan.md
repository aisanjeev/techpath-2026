# Implementation Plan: Prevent Duplicate Session Publish

## Overview

Currently, if a trainer creates multiple backend sessions for the same Module and Batch combination, they can publish all of them. This results in duplicate materials appearing in the student portal, causing confusion (as seen in the "Getting Started" duplicates). This plan introduces a database-level uniqueness check during the publish action to ensure that only **one** session per `(batch_id, module_id)` combination can be published.

## User Review Required

- **Error Message**: When a trainer tries to publish a duplicate, they will receive a `400 Bad Request` with the message: *"Materials for this module have already been published in this batch."* Is this phrasing acceptable?
- **Legacy Duplicates**: This fix prevents *new* duplicates from being created. Existing duplicates in the database will remain. If we need to clean up historical duplicates, a separate database migration/script will be required.

## Proposed Changes

### `techpath-backend`

#### [MODIFY] `app/crud/training_roster.py`
- Add a new method `get_published_by_batch_and_module(self, db: AsyncSession, batch_id: int, module_id: int) -> Optional[TrainingSession]` to `training_session_crud`.
- This method will query for the first `TrainingSession` matching the `batch_id` and `module_id` where `materials_published_at` is not null.

#### [MODIFY] `app/api/v1/endpoints/trainer.py`
- In the `publish_materials` route (`POST /sessions/{session_id}/materials/publish`):
  - Check if `session.module_id` is set.
  - If set, call `training_session_crud.get_published_by_batch_and_module(db, session.batch_id, session.module_id)`.
  - If a published session already exists and its ID is *different* from the current `session_id`, raise a `ValidationError` (HTTP 400) preventing the publish.

## Verification Plan

### Automated Tests
*(None - assuming we verify manually as per standard spec-kit flow unless unit tests are explicitly requested)*

### Manual Verification
1. Log in as a trainer.
2. Create two separate sessions for the same Batch (e.g., "BATCH MAY - 2026") and the same Module (e.g., "Getting Started").
3. End both sessions.
4. Publish the first session. Verify it succeeds.
5. Attempt to publish the second session. Verify it fails with the validation error message.
6. Verify the student portal only shows the single published session.
