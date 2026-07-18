# Quickstart: Session Pagination

## Setup & Testing

To test the session pagination UI changes:

1. **Start the Frontend Development Server**:
   ```bash
   cd techpath-frontend
   npm run dev
   ```

2. **Access the Portal**:
   Open a browser and navigate to the portal route: `http://localhost:4321/portal`

3. **Simulate Login**:
   Sign in with a valid Google account tied to a student roster. 
   *(Note: Ensure your local `.env.local` points to a backend environment where your account has published sessions).*

4. **Verify Pagination**:
   - Open a session.
   - Verify that only one asset (page 1) is visible.
   - Click "Next" to navigate to the next asset.
   - The URL should update with a `?page=` parameter.
   - Test browser Back and Forward buttons to ensure they work smoothly.
