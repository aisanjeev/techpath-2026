# Quickstart: Toggle Recording Validation

This guide outlines how to manually validate the Toggle Recording feature end-to-end.

## Prerequisites
- Local backend, frontend, and admin apps running.
- Local MinIO running with the `classroom-recordings` bucket.
- Local MediaMTX running with `record: yes`.

## Scenario 1: Unwanted Recording is Deleted

1. **Start the Session**:
   - Go to Admin Dashboard (`http://localhost:3000`).
   - Start a live session. Do **not** click the "Record" button.
   - Wait 10 seconds (so a `.mp4` file is generated in MinIO).

2. **Verify MinIO (Pre-End)**:
   - Check the MinIO bucket. You should see the `.mp4` file being actively written.

3. **End the Session**:
   - Click "End Session" in the Admin Dashboard.

4. **Verify MinIO (Post-End)**:
   - Check the MinIO bucket again. The `.mp4` file should be **deleted**.

## Scenario 2: Wanted Recording is Kept

1. **Start the Session**:
   - Start a live session.
   - Click the **Record** button in the trainer UI.
   - Wait 10 seconds.

2. **End the Session**:
   - Click "End Session".

3. **Verify MinIO (Post-End)**:
   - Check the MinIO bucket. The `.mp4` file should **still exist**.
   - (Optional) Check the backend logs to ensure the transcode job was triggered.
