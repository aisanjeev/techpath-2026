# Feature Specification: Prevent Duplicate Session Publish

**Feature Branch**: `003-prevent-duplicate-publish`

**Created**: 2026-07-17

**Status**: Draft

**Input**: User description: "in same batch and for same Modules, trainer is able to publish material again - again because of this students portal same materials shows duplicate"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Prevent Duplicate Publish (Priority: P1)

As a trainer managing a session, I want the system to prevent me from publishing materials for the same batch and module multiple times, so that students do not see duplicate, confusing entries in their learning portal.

**Why this priority**: This directly addresses the bug causing poor UX (duplicates) for the students in the learning portal.

**Independent Test**: Can be fully tested by having a trainer attempt to publish a session that has already been published. The system should block the action and inform the trainer that it's already published.

**Acceptance Scenarios**:

1. **Given** a trainer is viewing a session that has *not* been published yet, **When** they click to publish the materials, **Then** the publish succeeds normally.
2. **Given** a trainer is viewing a session that *has already* been published, **When** they view the publish options, **Then** the system should indicate it is already published and either disable the publish button or warn them and prevent a duplicate record from being created.
3. **Given** a trainer attempts to force-publish (e.g., clicking twice quickly), **Then** the system safely handles the concurrent requests and only creates a single published session record for that batch and module.

---

### Edge Cases

- What happens if a trainer genuinely needs to update materials for a session? (They should be able to *update* the existing published session rather than creating a new duplicate record).
- How do we handle legacy duplicate records that already exist in the system? (Existing duplicates could be merged, or the frontend could group/deduplicate them by batch and module ID).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST enforce a uniqueness constraint so that a specific combination of Batch ID and Module ID can only have one published session record.
- **FR-002**: System MUST provide clear UI feedback to the trainer if a session has already been published.
- **FR-003**: System MUST NOT allow the creation of a new published session if one already exists for that batch and module.
- **FR-004**: System MUST handle duplicate requests gracefully (e.g., returning an appropriate error message rather than crashing or creating duplicates).

### Key Entities

- **Session/Published Materials**: The record that ties a Batch, a Module, and the published assets together.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The number of duplicate session cards appearing in a student's portal drops to zero for all newly published sessions.
- **SC-002**: Trainers attempting to publish a session twice are met with a clear, user-friendly validation error or UI state 100% of the time.

## Assumptions

- We are only preventing *new* duplicates from being created. Cleaning up historical duplicate data in the database will be handled separately or via a one-off database script.
- A "Session" in this context is uniquely identified by the combination of its Batch and its Module.
- If a trainer adds new files to an already published session, the system should allow updating the existing published record rather than requiring a brand new publish action.
