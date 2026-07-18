# Data Model: Student Speaker Control

## Entities

### DoubtRequest (New or added to SessionParticipant)
Since `SessionParticipant` already tracks participants in a session, we can add a state column or create a separate table.
Given the ephemeral nature, adding fields to `SessionParticipant` or a lightweight `DoubtRequest` table works.

**Table**: `doubt_request`
- `id`: Primary Key
- `session_id`: Foreign Key to Classroom Session
- `participant_id`: Foreign Key to SessionParticipant (the student)
- `status`: Enum (`pending`, `approved`, `rejected`, `completed`)
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Events (Classroom Event Bus)
- `DOUBT_REQUESTED`: Fired when a student raises hand. Payload: `{ participant_id, name }`
- `DOUBT_APPROVED`: Fired when trainer approves. Payload: `{ participant_id, whep_url }`
- `DOUBT_REJECTED`: Fired when trainer rejects/dismisses. Payload: `{ participant_id }`
- `DOUBT_COMPLETED`: Fired when audio session ends. Payload: `{ participant_id }`
