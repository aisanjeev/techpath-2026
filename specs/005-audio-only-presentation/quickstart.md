# Quickstart: Audio-Only Presentation Validation

This guide outlines how to manually validate the Audio-Only Presentation feature end-to-end once implemented.

## Prerequisites
- Both `techpath-admin` (trainer UI) and `techpath-frontend` (student UI) must be running locally.
- `techpath-backend` must be running locally to handle signaling and state.
- A local or mock media server must be configured to receive WebRTC (WHIP) and serve it (WHEP).

## Scenario: Toggle Video Off Mid-Session

1. **Start the Trainer Session**:
   - Navigate to the Admin Dashboard (`http://localhost:3000`).
   - Open an active batch and click **Start Session**.
   - Grant camera and microphone permissions.
   - Note the 6-digit classroom join code displayed on the screen.

2. **Join as a Student**:
   - Open a new Incognito browser window.
   - Navigate to the Public Frontend classroom page (`http://localhost:4321/classroom`).
   - Enter the 6-digit join code and join as a guest.
   - Verify that you can see the trainer's live video and hear their audio.

3. **Toggle Audio-Only Mode**:
   - Return to the Admin Dashboard window.
   - Click the **Turn Off Camera** button in the trainer media controls.
   - **Expected Outcome**: The trainer's local video preview should disappear or show an avatar.

4. **Verify Student View**:
   - Switch back to the Incognito student window.
   - **Expected Outcome**: The live video feed should immediately be replaced by the "Camera off" placeholder text on a black background.
   - **Expected Outcome**: You should still be able to hear the trainer's microphone audio clearly.

5. **Toggle Video Back On**:
   - Return to the Admin Dashboard and click **Turn On Camera**.
   - Switch to the student window and verify the video feed resumes seamlessly.
