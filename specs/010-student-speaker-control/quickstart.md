# Quickstart Validation: Student Speaker Control

## Prerequisites
- MediaMTX running locally
- techpath-backend running (`npm run dev:backend` or equivalent)
- techpath-frontend and techpath-admin running

## Validation Scenario 1: Raise Hand and Approve

1. **Setup**:
   - Trainer logs into `techpath-admin` and starts Session 101.
   - Student logs into `techpath-frontend` and joins Session 101.

2. **Action**:
   - Student clicks "Raise Hand".
   - Trainer observes a notification/queue item in the admin dashboard for the student.

3. **Approval**:
   - Trainer clicks "Enable Audio".
   - Student's browser prompts for microphone access and starts publishing to `/class-101-doubt-<student_id>/whip`.
   - Trainer's browser automatically subscribes to `/class-101-doubt-<student_id>/whep` and hears the student.

4. **Teardown**:
   - Trainer clicks "Mute/Stop".
   - Audio connection is closed.
