# Data Model: Live Questions

## Entities

### `TrainingSessionQuestion`

Represents a question submitted by a student during a live virtual classroom session.

**Table Name**: `training_session_questions`

| Field | Type | Modifiers | Description |
|-------|------|-----------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the question |
| `session_id` | Integer | Foreign Key (`training_sessions.id`), Not Null | The session this question was asked in |
| `student_id` | Integer | Foreign Key (`users.id` / `students.id`), Not Null | The student who asked the question |
| `question_text` | String(500) | Not Null | The actual question text |
| `is_answered` | Boolean | Default `False`, Not Null | Whether the trainer has marked this as answered |
| `upvotes` | Integer | Default `0`, Not Null | Number of upvotes from other students |
| `created_at` | DateTime(UTC) | Default `now()`, Not Null | When the question was asked |
| `updated_at` | DateTime(UTC) | Default `now()`, On Update `now()`, Not Null | When the question was last modified |

### Changes to Existing Entities

#### `TrainingSession`
- Add field: `questions_are_public` (Boolean, Default `True`, Not Null). Controls whether students can see each other's questions and upvote them.

## Validation Rules

1. `question_text` must not be empty.
2. `question_text` length must be <= 500 characters.
3. Only the trainer assigned to `session_id` can modify `is_answered` or `questions_are_public`.
4. Only enrolled students of the session can submit questions.
5. Students can only upvote a question once (this might require an additional join table `question_upvotes` if strict upvote tracking is needed, or just rely on a simple increment if anonymous/loose tracking is acceptable. For accuracy, a `question_upvotes` table is recommended).

### `QuestionUpvote` (Optional but recommended for strict tracking)
**Table Name**: `question_upvotes`
- `question_id` (FK to `training_session_questions`)
- `student_id` (FK to `users`)
- PK is `(question_id, student_id)`
