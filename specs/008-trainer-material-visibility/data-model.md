# Data Model: Trainer Material Visibility

No new database tables are required for this feature. The feature relies on existing relationships in the database.

## Existing Entities Utilized

### `TrainingSession` (table: `training_sessions`)
- **Fields used**: `id`, `module_id`
- **Purpose**: Represents the presentation log.

### `TrainingModule` (table: `training_modules`)
- **Fields used**: `id`, `title`
- **Purpose**: The module that was presented during the session.

### `TrainingModuleAsset` (table: `training_module_assets`)
- **Fields used**: `id`, `module_id`, `asset_id`
- **Purpose**: The mapping between a module and the published materials.

### `LectureAsset` (table: `lecture_assets`)
- **Fields used**: `id`, `title`, `asset_type`, `external_url`, `media_file_id`
- **Purpose**: The actual published materials (decks, videos, documents).

## State Transitions
No new state transitions.

## Validation Rules
- The UI should only display the "View Published Material" button if the session's `module_id` is not null.
- The API endpoint to fetch assets for a session must verify that the requesting user is a trainer and has access to the session's module materials.
