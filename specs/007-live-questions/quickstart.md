# Quickstart: Validation Guide for Live Questions

This guide demonstrates how to validate the Live Questions feature end-to-end locally.

## Prerequisites
- Both `techpath-backend` and `techpath-admin` are running locally.
- `techpath-frontend` (if available locally) is running, or you are simulating a student via a REST client / WebSocket client.

## Validation Scenarios

### Scenario 1: Student Asks a Question

1. **Setup**: 
   - Start a live session in `techpath-admin` as a trainer.
   - Join the same session as a student in `techpath-frontend`.
2. **Action**: 
   - In the student view, click the `❓` (Ask Question) button.
   - Type "What is the difference between a process and a thread?" and hit submit.
3. **Expected Outcome**:
   - The question appears in the student's own view.
   - The trainer's `techpath-admin` Classroom Panel instantly displays the new question.
   - The database table `training_session_questions` contains the new entry.

### Scenario 2: Public Questions & Upvoting

1. **Setup**:
   - Trainer ensures "Public Questions" toggle is **ON** in the Classroom Panel.
   - Student A and Student B are in the session.
2. **Action**:
   - Student A submits a question.
   - Student B sees the question appear in their view.
   - Student B clicks the "Upvote" button next to Student A's question.
3. **Expected Outcome**:
   - The upvote count increments to `1` for Student B, Student A, and the Trainer in real-time.

### Scenario 3: Trainer Marks as Answered

1. **Setup**:
   - The session has an active, unanswered question.
2. **Action**:
   - Trainer clicks the "Mark Answered" checkmark next to the question in `techpath-admin`.
3. **Expected Outcome**:
   - The question visually updates (e.g., gets checked off or moved to an "Answered" tab) for both the trainer and the students.

### Scenario 4: Private Questions Toggle

1. **Setup**:
   - Trainer toggles "Public Questions" to **OFF** in `techpath-admin`.
2. **Action**:
   - Student A asks a question.
3. **Expected Outcome**:
   - Student A sees their own question.
   - The Trainer sees Student A's question.
   - Student B does **NOT** see Student A's question.
