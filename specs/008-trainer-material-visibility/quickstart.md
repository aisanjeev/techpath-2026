# Quickstart: Validation Guide

## Validation Scenario 1: Verify Button Appears for Module with Assets

1. **Prerequisites**: 
   - A `TrainingSession` exists with a valid `module_id`.
   - The associated `TrainingModule` has `LectureAsset` items linked via `TrainingModuleAsset`.
   - You are logged into `techpath-admin` as a trainer.
2. **Setup**:
   - Ensure the backend server and admin frontend are running locally.
3. **Execution**:
   - Navigate to the presentation logs (sessions view) in the admin dashboard.
4. **Expected Outcome**:
   - You should see a "View Published Material" button or link on the session record.
5. **Clicking the Button**:
   - Clicking the button should display a list of the associated assets (or open them directly if only one exists), allowing the trainer to view the materials used.

## Validation Scenario 2: Verify Button is Hidden/Disabled for Module without Assets

1. **Prerequisites**: 
   - A `TrainingSession` exists but its `module_id` is null, or the module has no assets.
2. **Execution**:
   - Navigate to the presentation logs in the admin dashboard.
3. **Expected Outcome**:
   - The "View Published Material" button should not be present, or it should be disabled with a tooltip indicating no materials are available.
