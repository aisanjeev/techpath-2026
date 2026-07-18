# Data Model: Audio-Only Presentation Mode

No new database tables or core data models are required for this feature. The existing models will be utilized.

## Existing Entity: MediaStateView (Frontend) / ClassroomMediaState (Backend)

The feature leverages the existing media state representation:

```typescript
export interface MediaStateView {
  whep_url?: string | null;
  hls_url?: string | null;
  mic_muted: boolean;
  camera_off: boolean;
  screen_sharing: boolean;
}
```

The fields `camera_off` and `mic_muted` already exist.

## State Transitions
1. **Trainer clicks "Turn Off Camera"**: 
   - Trainer UI calls API to update media state (`camera_off = true`).
   - Backend broadcasts `media_state_changed` event to the classroom via WebSockets.
   - Student UI receives event, updates local state.
   - `ClassroomVideoTile` re-renders, displaying the "Camera off" placeholder and hiding the video element.

2. **Trainer clicks "Turn On Camera"**:
   - Trainer UI calls API to update media state (`camera_off = false`).
   - Backend broadcasts `media_state_changed` event.
   - Student UI receives event, updates local state.
   - `ClassroomVideoTile` re-renders, removing the placeholder and making the video element visible.
