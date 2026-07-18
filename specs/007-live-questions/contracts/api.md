# API Contracts: Live Questions

## REST Endpoints

### 1. Submit a Question (Student)
- **POST** `/api/v1/student/sessions/{session_id}/questions`
- **Request Body**:
  ```json
  {
    "question_text": "Could you explain the difference between a process and a thread again?"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": 123,
    "session_id": 45,
    "student_id": 789,
    "student_name": "John Doe",
    "question_text": "Could you explain the difference between a process and a thread again?",
    "is_answered": false,
    "upvotes": 0,
    "created_at": "2026-07-18T10:30:00Z"
  }
  ```

### 2. Upvote a Question (Student)
- **POST** `/api/v1/student/sessions/{session_id}/questions/{question_id}/upvote`
- **Response** (200 OK):
  ```json
  {
    "id": 123,
    "upvotes": 1
  }
  ```

### 3. Get Questions (Trainer & Student)
- **GET** `/api/v1/trainer/sessions/{session_id}/questions`
- **GET** `/api/v1/student/sessions/{session_id}/questions`
  *(Note: Student endpoint only returns questions if `questions_are_public` is true for the session)*
- **Response** (200 OK):
  ```json
  [
    {
      "id": 123,
      "student_name": "John Doe",
      "question_text": "...",
      "is_answered": false,
      "upvotes": 0,
      "created_at": "..."
    }
  ]
  ```

### 4. Mark as Answered (Trainer)
- **POST** `/api/v1/trainer/sessions/{session_id}/questions/{question_id}/answer`
- **Response** (200 OK):
  ```json
  {
    "id": 123,
    "is_answered": true
  }
  ```

### 5. Toggle Public Questions (Trainer)
- **PATCH** `/api/v1/trainer/sessions/{session_id}/settings` (or existing session patch endpoint)
- **Request Body**:
  ```json
  {
    "questions_are_public": false
  }
  ```

## WebSocket Events (Classroom Broadcaster)

All question actions broadcast events via the existing WebSocket channel (`bus`).

### `question_asked`
Broadcast to: All users in session (if public) or just trainer (if private).
```json
{
  "type": "question_asked",
  "data": {
    "id": 123,
    "student_name": "John Doe",
    "question_text": "...",
    "created_at": "..."
  }
}
```

### `question_upvoted`
Broadcast to: All users in session (if public) or just trainer.
```json
{
  "type": "question_upvoted",
  "data": {
    "question_id": 123,
    "upvotes": 2
  }
}
```

### `question_answered`
Broadcast to: All users in session.
```json
{
  "type": "question_answered",
  "data": {
    "question_id": 123
  }
}
```

### `questions_visibility_changed`
Broadcast to: Students (so they can enable/disable the upvote/public view).
```json
{
  "type": "questions_visibility_changed",
  "data": {
    "is_public": false
  }
}
```
